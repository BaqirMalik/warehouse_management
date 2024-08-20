# -*- coding: utf-8 -*-

from odoo import fields, models, _, api
from odoo.exceptions import RedirectWarning, ValidationError


class HrExpenseSheetInherit(models.Model):
    _inherit = 'hr.expense.sheet'
    _description = 'Expense Sheet'

    redirect_link = fields.Char(string='Redirect Link')

    def unlink(self):
        for record in self:
            if record.status != 'draft':
                raise ValidationError("Request can only be deleted in Submit State")
        return super(HrExpenseSheetInherit, self).unlink()

    def action_submit_sheet(self):
        res = super(HrExpenseSheetInherit, self).action_submit_sheet()
        # Sending Email Notifications
        mail_server = self.sudo().env['ir.mail_server'].search([], limit=1)
        users = self.env['res.users'].search(
            [('groups_id', 'in', [self.env.ref('hr_expense.group_hr_expense_manager').id])]
        )
        # Send email notifications to each user in the group
        template = self.env.ref('ct_expense_management.mail_template_for_expense_management_request')
        for user in users:
            template.write({'email_from': mail_server.smtp_user})
            template.write({'email_to': user.email})
            template.send_mail(self.id, force_send=True)

        # Return a notification message
        message = _("Expense Request Submitted to Manager Successfully!")
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'target': 'new',
            'params': {
                'message': message,
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }


    @api.model
    def create(self, vals):
        record = super(HrExpenseSheetInherit, self).create(vals)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        redirect_link = '%s/web#id=%d&view_type=form&model=%s' % (base_url, record.id, record._name)
        record.write({'redirect_link': redirect_link})
        return record
