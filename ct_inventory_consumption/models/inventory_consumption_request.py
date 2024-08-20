# -*- coding: utf-8 -*-

from odoo import fields, models, _, api
from odoo.exceptions import RedirectWarning, ValidationError


class InventoryConsumptionRequest(models.Model):
    _name = 'inventory.consumption.request'
    _description = 'Inventory Consumption Request'
    _rec_name = "reference"

    reference = fields.Char(string='Reference', required=True, copy=False, readonly=True, index=True,
                            default=lambda self: _('New'))

    requester_id = fields.Many2one('res.users', string='Requester', default=lambda self: self.env.user, required=True)
    Inventory_consumption_request_lines = fields.One2many('inventory.consumption.request.lines',
                                                          "consumption_request_id", string='Request Consumption Lines',
                                                          required=True)

    date = fields.Datetime('Date', required=True, default=fields.Datetime.now)

    status = fields.Selection([('draft', 'Draft'), ('pending', 'Pending Approval'), ('approved', 'Approved'),
                               ('cancelled', 'Cancelled')], string='Status',
                              default='draft', copy=False)

    stock_move_count = fields.Integer(string="Stock Move Count", compute="_compute_stock_move_count")
    account_move_count = fields.Integer(string="Stock Move Count", compute="_compute_account_move_count")

    redirect_link = fields.Char(string='Redirect Link')

    def unlink(self):
        for record in self:
            if self.env.user.has_group('ct_inventory_consumption.group_invnetory_consumption_user'):
                raise ValidationError('You are not allowed to delete this request.')
            if record.status == 'approved':
                raise ValidationError("Approved Request can't be deleted")
        return super(InventoryConsumptionRequest, self).unlink()

    def action_open_related_account_move(self):
        account_moves = self.env['account.move'].search(
            [('inventory_consumption_request_id', '=', self.id)])  # Adjust 'your_field' according to your model

        action = {
            'name': _("Account Moves"),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', account_moves.ids)],
            'context': {'create': False,
                        'default_name': self.reference,
                        },
        }
        return action

    def action_open_related_stock_move(self):
        stock_moves = self.env['stock.move'].search(
            [('inventory_consumption_request_id', '=', self.id)])

        action = {
            'name': _("Stock Moves"),
            'type': 'ir.actions.act_window',
            'res_model': 'stock.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', stock_moves.ids)],
            'context': {'create': False,
                        'default_origin': self.reference,
                        },
        }
        return action

    def _compute_account_move_count(self):
        for record in self:
            record.account_move_count = self.env['account.move'].search_count(
                [('inventory_consumption_request_id', '=', record.id)])

    def _compute_stock_move_count(self):
        for record in self:
            record.stock_move_count = self.env['stock.move'].search_count(
                [('inventory_consumption_request_id', '=', record.id)])

    def action_request(self):
        if not self.Inventory_consumption_request_lines:
            raise ValidationError(_('Please Add Line Before Requesting'))
        for rec in self.Inventory_consumption_request_lines:
            if rec.qty_available == 0:
                raise ValidationError(_('Quantity of %(product_name)s is Not Avaialable in Store',
                                        product_name=rec.product_id.name))
            if rec.qty_demand == 0:
                raise ValidationError(_('Demand Quantity of %(product_name)s is 0\n'
                                        'Please Add Some Quanitity',
                                        product_name=rec.product_id.name))
            if rec.qty_demand > rec.qty_available:
                raise ValidationError(_('Demand Quantity %(product_name)s is Greater than Available Quantity',
                                        product_name=rec.product_id.name))
        mail_server = self.sudo().env['ir.mail_server'].search([], limit=1)
        for rec in self:
            users = self.env['res.users'].search(
                [('groups_id', 'in', [self.env.ref('ct_inventory_consumption.group_manager').id])])

            # Send email notification to each user in the group
            template = self.env.ref('ct_inventory_consumption.mail_template_for_inventory_consumption_request')
            for user in users:
                template.write({'email_from': mail_server.smtp_user})
                template.write({'email_to': user.email})
                template.send_mail(rec.id, force_send=True)
        self.status = 'pending'

        message = _(
            "Inventory Consumption Request Submitted Successfully!")
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'target': 'new',
            'params': {
                'message': message,
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }

    def action_approve(self):
        internal_location_ids = self.env['stock.location'].search([('usage', '=', 'internal')]).ids
        domain = [
            ('product_id', 'in', self.Inventory_consumption_request_lines.mapped('product_id').ids),
            ('location_id', 'in', internal_location_ids)
        ]
        action = {
            'name': _('Inventory Adjustments'),
            'view_mode': 'list',
            'view_id': self.env.ref(
                'ct_inventory_consumption.view_stock_quant_consume_quanity_tree_inventory_editable').id,
            'res_model': 'stock.quant',
            'type': 'ir.actions.act_window',
            'context': {
                'consumption_request_id': self.id,
            },
            'domain': domain,
        }
        self.update_stock_quantities()
        return action

    def update_stock_quantities(self):
        for line in self.Inventory_consumption_request_lines:
            quants = self.env['stock.quant'].search([
                ('product_id', '=', line.product_id.id),
                ('location_id.usage', '=', 'internal')
            ])
            for quant in quants:
                quant.write({'quantity_to_consume': line.qty_demand})

    def action_cancel(self):
        self.status = 'cancelled'

    def action_reset(self):
        self.status = 'draft'

    # @api.model
    # def create(self, vals):
    #     if vals.get('reference', _('New')) == _('New'):
    #         vals['reference'] = self.env['ir.sequence'].next_by_code('inventory.consumption.request') or _('New')
    #     return super(InventoryConsumptionRequest, self).create(vals)

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('inventory.consumption.request') or _('New')
        record = super().create(vals)
        base_url = self.sudo().env['ir.config_parameter'].get_param('web.base.url')
        redirect_link = '%s/web#id=%d&view_type=form&model=%s' % (base_url, record.id, record._name)
        record.write({'redirect_link': redirect_link})
        return record


    def action_generate_sequence_numbers(self):
        for record in self:
            if record.reference == 'New':
                new_reference = self.env['ir.sequence'].next_by_code('inventory.consumption.request') or _('New')
                record.write({'reference': new_reference})
