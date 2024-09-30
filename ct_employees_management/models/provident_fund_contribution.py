from odoo import models,fields, _


class ProvidentFundContribution(models.Model):
    _name = 'provident.fund.contribution'

    year = fields.Selection([
        ('1st_year' ,'1st Year'),
        ('2nd_year' , '2nd Year'),
        ('3rd_year' , '3rd Year')
    ])
    employee_contrib = fields.Float(string='Employee Contribution (%)')
    company_contrib = fields.Float(string='Company Contribution (%)')
