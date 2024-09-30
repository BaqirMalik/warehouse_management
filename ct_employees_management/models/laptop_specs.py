from typing import Dict, List

from odoo import api, fields, _, models


class LaptopCore(models.Model):
    _name = 'laptop.core'
    _rec_name = 'name'

    sequence = fields.Integer("Sequence")
    name = fields.Char(string='Name', required="1")
    code = fields.Char(string='Code', compute="_compute_code", store=True)

    @api.depends('name')
    def _compute_code(self):
        for record in self:
            if record.name and len(record.name) >= 2:
                record.code = record.name[-3:]
            else:
                record.code = ''



class LaptopGeneration(models.Model):
    _name = 'laptop.generation'
    _rec_name = 'name'

    sequence = fields.Integer("Sequence")
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', compute="_compute_code", store=True)

    @api.depends('name')
    def _compute_code(self):
        for record in self:
            if record.name and len(record.name) >= 2:
                record.code = record.name[0:4]  # Get the First Four characters of the name
            else:
                record.code = ''