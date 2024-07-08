# -*- coding: utf-8 -*-

from odoo import fields, models, _, api

class InheritStockMove(models.Model):
    _inherit = 'stock.move'

    inventory_consumption_request_id = fields.Many2one('inventory.consumption.request', string='Inventory Consumption')

    @api.depends('product_id')
    def _compute_last_serial_number(self):
        for rec in self:
            last_record = self.env['stock.lot'].search([('product_id', '=', rec.product_id.id)], limit=1, order='id DESC')
            if last_record:
                rec.last_assigned_serial_number = last_record.name
            else:
                rec.last_assigned_serial_number = False


    last_assigned_serial_number = fields.Char("Last Assigned Serial Number", compute='_compute_last_serial_number')



