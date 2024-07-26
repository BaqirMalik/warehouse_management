# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class InheritStockQuant(models.Model):
    _inherit = 'stock.quant'
    _description = 'Stock Quanitity'

    quantity_to_consume = fields.Integer(string="Qty to Consume", default=0)

    def action_apply_inventory(self):
        active_ids = self.env.context.get('active_ids')
        consumption_request_id = self.env.context.get('consumption_request_id')
        if active_ids:
            location_dest_id = self.env['stock.location'].search([('usage', '=', 'production')], limit=1)
            for stock_quant in self.env['stock.quant'].browse(active_ids):
                if stock_quant.quantity_to_consume:
                    available_quantity = stock_quant.quantity
                    if available_quantity < stock_quant.quantity_to_consume:
                        raise ValidationError(_('Demand Quantity of %(product_name)s is greater than\n'
                                                'Available Quantity',
                                                product_name=stock_quant.product_id.name))
                    consume_quantity = min(stock_quant.quantity_to_consume,
                                           available_quantity)  # Ensure not to consume more than available

                    stock_move = self.env['stock.move'].create({
                        'name': 'Inventory Consumption',
                        'product_id': stock_quant.product_id.id,
                        'product_uom_qty': consume_quantity,
                        'quantity': consume_quantity,
                        'product_uom': stock_quant.product_id.uom_id.id,
                        'location_id': stock_quant.location_id.id,
                        'location_dest_id': location_dest_id.id,
                        'state': 'done',
                        'inventory_consumption_request_id': consumption_request_id,
                    })
                    stock_move._action_confirm()
                    stock_move._action_done()

                    journal_entry = self.env['account.move'].create({
                        'move_type': 'entry',
                        'ref': 'Inventory Consumption',
                        'date': fields.Date.today(),
                        'inventory_consumption_request_id': consumption_request_id,
                    })
                    journal_entry_line = self.env['account.move.line'].create({
                        'move_id': journal_entry.id,
                        'name': 'Inventory Consumption',
                        'product_id': stock_quant.product_id.id,
                        'account_id': self.env.company['transfer_account_id'].id,
                        'quantity': consume_quantity,
                        'debit': stock_quant.product_id.list_price * consume_quantity,
                        'credit': stock_quant.product_id.list_price * consume_quantity,
                    })
                    journal_entry.action_post()
                consumption_request = self.env['inventory.consumption.request'].sudo().search(
                    [('id', '=', consumption_request_id)])
                consumption_request.status = 'approved'
                return {
                    'effect': {
                    'type': 'rainbow_man',
                    'message': _("Consumption Request Approved Successfully!"),
                    }
                }
        else:
            print("No active ID found in the context")
        res = super(InheritStockQuant, self).action_apply_inventory()
        print(res)
