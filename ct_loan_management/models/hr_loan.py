from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class HrLoan(models.Model):
    """ Model for managing loan requests."""
    _name = 'hr.loan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Loan Request"


    @api.model
    def default_get(self, field_list):
        result = super(HrLoan, self).default_get(field_list)
        if result.get('user_id'):
            user_id = result['user_id']
        else:
            user_id = self.env.context.get('user_id', self.env.user.id)
        result['employee_id'] = self.env['hr.employee'].search(
            [('user_id', '=', user_id)], limit=1).id
        return result

    name = fields.Char(string="Loan Name", default="New", readonly=True,
                       help="Name of the loan")
    date = fields.Date(string="Date", default=fields.Date.today(),
                       readonly=True, help="Date of the loan request")
    employee_id = fields.Many2one('hr.employee', string="Employee",
                                  required=True, help="Employee Name")
    installment = fields.Integer(string="No Of Installments", default=1,
                                 help="Number of installments")
    payment_date = fields.Date(string="Payment Start Date", required=True,
                               default=fields.Date.today(),
                               help="Date of the payment")
    loan_lines = fields.One2many('hr.loan.line', 'loan_id',
                                 string="Loan Line",
                                 help="Details of installment lines "
                                      "associated with the loan.",
                                 index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 help="Company",
                                 default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  required=True, help="Currency",
                                  default=lambda self: self.env.user.
                                  company_id.currency_id)
    loan_amount = fields.Float(string="Loan Amount", required=True,
                               help="Loan amount")
    total_amount = fields.Float(string="Total Amount", store=True,
                                readonly=True, compute='_compute_total_amount',
                                help="The total amount of the loan")
    balance_amount = fields.Float(string="Balance Amount", store=True,
                                  compute='_compute_total_amount',
                                  help="""The remaining balance amount of the 
                                  loan after deducting 
                                  the total paid amount.""")
    total_paid_amount = fields.Float(string="Total Paid Amount",
                                     compute='_compute_total_amount',
                                     help="The total amount that has been "
                                          "paid towards the loan.")
    state = fields.Selection(
        [('draft', 'Draft'), ('waiting_approval_1', 'Submitted'),
         ('approve', 'Approved'), ('refuse', 'Refused'), ('cancel', 'Canceled'),
         ], string="State", default='draft', help="The current state of the "
                                                  "loan request.", copy=False)
    loan_description= fields.Html(string='Loan Description', required=True)
    redirect_link = fields.Char(string='Redirect Link')

    @api.depends('loan_lines')
    def _compute_total_amount(self):
        calculate_amount = 0.0
        total_paid = 0.0
        for loan in self:
            for line in loan.loan_lines:
                if line.paid:
                    total_paid += line.amount
                if line.amount:
                    calculate_amount += line.amount
            loan.total_amount = round(calculate_amount)
            balance_amount = loan.loan_amount - total_paid
            loan.balance_amount = balance_amount
            loan.total_paid_amount = total_paid


    @api.model
    def create(self, values):
        loan_count = self.env['hr.loan'].search_count(
            [('employee_id', '=', values['employee_id']),
             ('state', '=', 'approve'),
             ('balance_amount', '!=', 0)])
        if loan_count:
            raise ValidationError(
                _("The Employee has already a pending installment"))
        active_contract = self.env['hr.contract'].sudo().search([('employee_id','=',values.get('employee_id'))])
        if active_contract.sudo().state != 'open':
            raise ValidationError(f"No Active Contract Found for this Employee{self.employee_id.name}")
        else:
            values['name'] = self.env['ir.sequence'].get('hr.loan.seq') or ' '
            res = super(HrLoan, self).create(values)
            base_url = self.sudo().env['ir.config_parameter'].get_param('web.base.url')
            redirect_link = '%s/web#id=%d&view_type=form&model=%s' % (base_url, res.id, res._name)
            res.write({'redirect_link': redirect_link})
            return res


    def action_compute_installment(self):
        for loan in self:
            loan.loan_lines.unlink()
            date_start = datetime.strptime(str(loan.payment_date), '%Y-%m-%d')
            amount = "{:.2f}".format(loan.loan_amount / loan.installment)
            for i in range(1, loan.installment + 1):
                self.env['hr.loan.line'].create({
                    'date': date_start,
                    'amount': amount,
                    'employee_id': loan.employee_id.id,
                    'loan_id': loan.id})
                date_start = date_start + relativedelta(months=1)
            loan._compute_total_amount()
        return True

    def action_draft(self):
        return self.write({'state': 'draft'})

    def action_refuse(self):
        return self.write({'state': 'refuse'})

    def action_submit(self):
        self.sudo().write({'state': 'waiting_approval_1'})
        template = self.sudo().env().ref('ct_loan_management.loan_email_template_manager')
        IrMailServer = self.env['ir.mail_server'].sudo().search([('name', '=', 'Crecentech Outgoing Email Server')])
        template.sudo().write({'email_from': IrMailServer.smtp_user})
        users = self.env['res.users'].search(
            [('groups_id', 'in', [self.env.ref('ct_loan_management.group_hr_loan_manager').id])]
        )
        for user in users:
            template.sudo().write({'email_to': user.login})
        action_submit = template.sudo().send_mail(self.id, force_send=True)
        if action_submit:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _("Successfully"),
                    'type': 'success',
                    'message': _("Submission Email Send Successfully"),
                    'sticky': True,
                },
            }


    def action_cancel(self):
        """ Function to cancel loan request"""
        self.write({'state': 'cancel'})

    def action_approve(self):
        for data in self:
            if not data.loan_lines:
                raise ValidationError(_("Please Compute installment"))
            else:
                self.write({'state': 'approve'})
        template = self.env().ref('ct_loan_management.loan_email_template_user')
        IrMailServer = self.env['ir.mail_server'].search([('name', '=', 'Crecentech Outgoing Email Server')])
        template.sudo().write({'email_from': IrMailServer.smtp_user})
        employee_email = self.employee_id.work_email
        template.sudo().write({'email_to': employee_email})
        action_approve = template.send_mail(self.id, force_send=True)
        if action_approve:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _("Successfully"),
                    'type': 'success',
                    'message': _("Approval Email Send Successfully"),
                    'sticky': True,
                },
            }


    def unlink(self):
        """ Function which restrict the deletion of approved or submitted
                loan request"""
        for loan in self:
            if loan.state not in ('draft', 'cancel'):
                raise UserError(_(
                    'You cannot delete a loan which is not in draft '
                    'or cancelled state'))
        return super(HrLoan, self).unlink()

    def update_loans(self):
        total_paid_amount = 0
        loans = self.env["hr.loan"].search([('state', '=', 'approve')])
        for rec in loans:
            for line in rec.loan_lines:
                # Check if the status is 'pending' and the date is the 11th of the current month
                if line.status == 'pending' and line.date == date.today().replace(day=11):
                    line.status = 'paid'
                    line.paid = True
                    rec.employee_id.contract_id.wage = True
                    total_paid_amount += line.amount  # If you have an amount field

    @api.model
    def write(self, values):
        res = super(HrLoan, self).write(values)
        for rec in self:
            lines_sum_amount = sum(line.amount for line in rec.loan_lines)
            if lines_sum_amount:
                if not values.get('loan_amount'):
                    if round(lines_sum_amount) != self.loan_amount:
                        raise ValidationError(
                            f"ERROR: Total amount of lines ({lines_sum_amount}) must be equal to Loan amount ({self.loan_amount}).")
            return res



class HrLoanLine(models.Model):
    """ Model for managing details of loan request installments"""
    _name = "hr.loan.line"
    _description = "Installment Line"

    date = fields.Date(string="Payment Date", required=True,
                       help="Date of the payment")
    employee_id = fields.Many2one('hr.employee', string="Employee",
                                  help="Employee")
    amount = fields.Float(string="Amount", required=True, help="Amount")
    paid = fields.Boolean(string="Paid", help="Indicates whether the "
                                              "installment has been paid.")
    loan_id = fields.Many2one('hr.loan', string="Loan Ref.",
                              help="Reference to the associated loan.")
    status = fields.Selection([('pending', 'Pending'), ('paid', 'Paid')], string='Status', default='pending', readonly=True)

