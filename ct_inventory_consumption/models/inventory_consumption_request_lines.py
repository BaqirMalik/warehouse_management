# -*- coding: utf-8 -*-

from odoo import fields, models, api


class InventoryConsumptionRequestLines(models.Model):
    _name = 'inventory.consumption.request.lines'
    _description = 'Inventory Consumption Request Lines'

    product_id = fields.Many2one('product.product', "Product", required=True)
    consumption_request_id = fields.Many2one('inventory.consumption.request', "Inventory Consumption Request")
    qty_available = fields.Float(
        "Total Quantity",
        help="Total quantity Available in product's UoM", related="product_id.qty_available")
    reserve_qty = fields.Float(
        "Reserved Quantity", related="product_id.reserve_qty")
    qty_demand = fields.Float(
        "Qty Demand",
        help="Total quantity demanded in product's UoM")
    current_qty = fields.Float(
        "Current Available Qty", related="product_id.current_qty")


    # @api.onchange("qty_demand")
    # def onchange_qty_demand(self):
    #     self.product_id.reserve_qty = self.product_id.reserve_qty + self.qty_demand
    #     self.product_id.current_qty = self.qty_available - self.product_id.reserve_qty

    # @api.depends("product_id")
    # def compute_current_qty(self):
    #     for rec in self:
    #         if rec.product_id:
    #             rec.current_qty = rec.qty_available - rec.reserve_qty
    #         else:
    #             rec.current_qty = 0

