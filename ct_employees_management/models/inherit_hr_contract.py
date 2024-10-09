from odoo import models, fields, api, _

class InheritHrContract(models.Model):
    _inherit = 'hr.contract'

    total_salary = fields.Float("Total Salary", compute="_compute_total_salary")


    @api.depends("wage","hra","da","travel_allowance","meal_allowance","medical_allowance","other_allowance")
    def _compute_total_salary(self):
        for rec in self:
            rec.total_salary = rec.wage + rec.hra + rec.da + rec.travel_allowance + rec.meal_allowance + rec.medical_allowance + rec.other_allowance