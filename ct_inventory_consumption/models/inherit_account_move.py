# -*- coding: utf-8 -*-

from odoo import fields, models, _, api

class InheritAccountMove(models.Model):
    _inherit = 'account.move'

    inventory_consumption_request_id = fields.Many2one('inventory.consumption.request', string='Inventory Consumption')

