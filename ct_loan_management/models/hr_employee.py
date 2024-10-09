from odoo import fields, models, _


class HrEmployee(models.Model):
    """Extends the 'hr.employee' model to include loan_count."""
    _inherit = "hr.employee"

    loan_count = fields.Integer(
        string="Loan Count",
        help="Number of loans associated with the employee",
        compute='_compute_loan_count')
    provident_fund_count = fields.Integer(
        string="Provident Fund Count",
        help="Provident Fund associated with the employee",
        compute='_compute_provident_fund_count')

    def _compute_loan_count(self):
        self.loan_count = self.env['hr.loan'].search_count(
            [('employee_id', '=', self.id)])

    def _compute_provident_fund_count(self):
        self.provident_fund_count = self.env['employee.pf'].search_count(
            [('employee_id', '=', self.id)])

    def action_loan_view(self):
        """ Opens a view to list all documents related to the current
         employee."""
        self.ensure_one()
        return {
            'name': _('Loan'),
            'domain': [('employee_id', '=', self.id)],
            'res_model': 'hr.loan',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'help': _('''<p class="oe_view_nocontent_create">
                           Click to Create for New Loan
                        </p>'''),
            'limit': 80,
            'context': {'default_employee_id': self.id,}
        }

    def action_provident_fund_view(self):
        self.ensure_one()
        return {
            'name': _('Provident Fund'),
            'domain': [('employee_id', '=', self.id)],
            'res_model': 'employee.pf',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree',
            'help': _('''<p class="oe_view_nocontent_create"></p>'''),
            'limit': 80,
            'context': "{'default_employee_id': %s}" % self.id
        }



