from odoo import fields, models, _, api
from odoo.exceptions import RedirectWarning, ValidationError


class InheritHrExpense(models.Model):
    _inherit = 'hr.expense'
    _description = 'HR Expense'

    def _get_payment_mode_selection(self):
        # Define the selection values and filter out 'own_account'
        return [
            ('company_account', "Company")
        ]


    payment_mode = fields.Selection(
        selection=_get_payment_mode_selection,
        string="Paid By",
        default='company_account',
        tracking=True,
    )