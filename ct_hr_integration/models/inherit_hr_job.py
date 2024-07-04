from odoo import fields, models, api


class InheritHrJob(models.Model):
    _inherit = "hr.job"

    crecentech_career_id = fields.Integer(string='Crecentect Career ID')
    crecentech_career_name = fields.Char(string='Crecentect Career Name')

