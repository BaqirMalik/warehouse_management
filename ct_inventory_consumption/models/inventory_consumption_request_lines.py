# -*- coding: utf-8 -*-

from odoo import fields, models


class InventoryConsumptionRequestLines(models.Model):
    _name = 'inventory.consumption.request.lines'
    _description = 'Inventory Consumption Request Lines'

    product_id = fields.Many2one('product.product', "Product", required=True)
    consumption_request_id = fields.Many2one('inventory.consumption.request', "Inventory Consumption Request")
    qty_available = fields.Float(
        "Qty Available",
        help="Total quantity Available in product's UoM", related="product_id.qty_available")
    qty_demand = fields.Float(
        "Qty Demand",
        help="Total quantity demanded in product's UoM")
