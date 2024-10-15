from datetime import date

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class InheritHrEmployee(models.Model):
    _inherit = 'hr.employee'

    employee_assets = fields.Many2one('employee.assets', string="Employee Asset",tracking=True, ondelete="restrict")
    provident_fund_ids = fields.One2many('employee.pf','employee_id', string='Provident Funds')

    employee_assets_history_ids = fields.One2many('employee.assets.history','employee_id', string='Employee Assets History')
    pseudo_name = fields.Char("Pseudo Name", tracking=True)
    joining_date = fields.Date(string="DOJ", help="Joining Date", tracking=True)
    redirect_link = fields.Char(string='Redirect Link')
    is_readonly = fields.Boolean("Is Readonly", compute="_compute_is_field_readonly")
    is_it_user = fields.Boolean("Is It/User", default=False)

    def _compute_is_field_readonly(self):
        for record in self:
            if not self.env.user.has_group("hr.group_hr_manager"):
                record.is_readonly = True
            else:
                record.is_readonly = False

    def create(self, vals):
        res = super(InheritHrEmployee, self).create(vals)
        asset_id = vals.get('employee_assets')
        if not self.env.user.has_group("hr.group_hr_manager"):
            raise ValidationError(_("You don't Have Permission to Create the Employee"))
        if asset_id:
            self.env['employee.assets.history'].create({
                'employee_id': res.id,
                'asset_id': asset_id,
                'date': date.today()
            })
            res.employee_assets.employee_id = res.id
            res.employee_assets.state = 'assigned'
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        redirect_link = '%s/web#id=%d&view_type=form&model=%s' % (base_url, res.id, res._name)
        res.write({'redirect_link': redirect_link})

        template = self.sudo().env().ref('ct_employees_management.employee_email_template')
        IrMailServer = self.sudo().env['ir.mail_server'].search([('name', '=', 'Crecentech Outgoing Email Server')])
        template.sudo().write({'email_from': IrMailServer.smtp_user})
        users = self.env['res.users'].search(
            [('groups_id', 'in', [self.env.ref('ct_employees_management.group_hr_it_employee').id])]
        )
        for user in users:
            template.sudo().write({'email_to': user.login})
            template.send_mail(res.id, force_send=True)
        return res

    def write(self, vals):
        res = super(InheritHrEmployee, self).write(vals)
        asset_id = vals.get('employee_assets')
        if asset_id:
            for employee in self:
                self.env['employee.assets.history'].create({
                    'employee_id': employee.id,
                    'asset_id': asset_id,
                    'date': date.today()
                })
            self.employee_assets.employee_id = self.id
            self.employee_assets.state = 'assigned'
        else:
            previous_asset = self.env['employee.assets.history'].search([
                ('employee_id', '=', self.id)
            ], limit=1, order='id desc')
            if previous_asset:
                previous_asset.asset_id.state = 'ready'
        return res

    def unlink(self):
        for rec in self:
            if not self.env.user.has_group("hr.group_hr_manager"):
                raise ValidationError(_("You don't Have Permission to Delete the Employee"))
            if not rec.employee_assets:
                return super(InheritHrEmployee, self).unlink()
            else:
                raise ValidationError(_('You have to un-allocate the Employee Assets first'))


