from datetime import date

from odoo import models, fields, api, _

class InheritHrEmployee(models.Model):
    _inherit = 'hr.employee'

    employee_assets = fields.Many2one('employee.assets', string="Employee Asset", required=True)
    provident_fund_ids = fields.One2many('employee.pf','employee_id', string='Provident Funds')

    employee_assets_history_ids = fields.One2many('employee.assets.history','employee_id', string='Employee Assets History')

    def create(self, vals):
        res = super(InheritHrEmployee, self).create(vals)
        asset_id = vals.get('employee_assets')
        if asset_id:
            self.env['employee.assets.history'].create({
                'employee_id': res.id,
                'asset_id': asset_id,
                'date': date.today()
            })
            res.employee_assets.employee_id = self.id
            res.employee_assets.state = 'assigned'
        return res

    def write(self, vals):
        res = super(InheritHrEmployee, self).write(vals)
        asset_id = vals.get('employee_assets')
        if asset_id:
            previous_asset = self.env['employee.assets.history'].search([
                ('employee_id', '=', self.id)
            ], limit=1, order='id desc')
            if len(previous_asset) > 0:
                previous_asset.asset_id.state = 'ready'
            for employee in self:
                self.env['employee.assets.history'].create({
                    'employee_id': employee.id,
                    'asset_id': asset_id,
                    'date': date.today()
                })
            self.employee_assets.employee_id = self.id
            self.employee_assets.state = 'assigned'
        return res
