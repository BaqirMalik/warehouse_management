from datetime import datetime, date
from odoo import models, fields, api
from odoo.exceptions import UserError


class EmployeePF(models.Model):
    _name = 'employee.pf'
    _description = 'Employee Provident Fund'

    employee_id = fields.Many2one('hr.employee', string='Employee', readonly=True)
    employee_contribution_amount = fields.Float(string='Employee Contribution Amount', readonly=True)
    company_contribution_amount = fields.Float(string='Company Contribution Amount', readonly=True)
    contribution_date = fields.Date(string='Contribution Date', readonly=True)
    total_contribution = fields.Float(string="Total Contribution", compute='_compute_total_contribution')

    @api.model
    def update_provident_fund(self):
        # Get the current date
        current_date = date.today()
        for employee in self.env['hr.employee'].search([]):
            contract_start_date = employee.contract_id.date_start if employee.contract_id else False
            if contract_start_date:
                difference_in_months = (current_date.year - contract_start_date.year) * 12 + (
                            current_date.month - contract_start_date.month)
                if 1 <= difference_in_months <= 12:
                    contribution_config = self.env['provident.fund.contribution'].search([('year', '=', '1st_year')],
                                                                                         limit=1)
                elif 13 <= difference_in_months <= 24:
                    contribution_config = self.env['provident.fund.contribution'].search([('year', '=', '2nd_year')],
                                                                                         limit=1)
                elif difference_in_months >= 25:
                    contribution_config = self.env['provident.fund.contribution'].search([('year', '=', '3rd_year')],
                                                                                         limit=1)
                else:
                    contribution_config = None

                if contribution_config:
                    employee_salary = employee.contract_id.wage if employee.contract_id else 0
                    employee_contribution = (employee_salary * contribution_config.employee_contrib) / 100
                    company_contribution = (employee_contribution * contribution_config.company_contrib) / 100
                    check_contribution = self.env['employee.pf'].search([
                        ('employee_id', '=', employee.id),
                        ('contribution_date', '=', current_date)
                    ])
                    if not check_contribution:
                        self.env['employee.pf'].create({
                            'employee_id': employee.id,
                            'employee_contribution_amount': employee_contribution,
                            'company_contribution_amount': company_contribution,
                            'contribution_date': current_date,
                        })

    @api.depends('employee_contribution_amount','company_contribution_amount')
    def _compute_total_contribution(self):
        for rec in self:
            rec.total_contribution = rec.employee_contribution_amount + rec.company_contribution_amount




    def unlink(self):
        for rec in self:
            raise UserError("Not allowed to Delete the Provident Fund")
        return super(EmployeePF, self).unlink()



