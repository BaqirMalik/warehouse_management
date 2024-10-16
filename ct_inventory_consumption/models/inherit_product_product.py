from odoo import fields, models

class InheritProductProduct(models.Model):
    _inherit = 'product.product'

    consumption_request_id = fields.Many2one('inventory.consumption.request.lines', "Inventory Consumption Request Lines")
    reserve_qty = fields.Float('Reserved')
    current_qty = fields.Float('Current Quantity')