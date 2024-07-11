from odoo import models, api, _
from odoo.exceptions import ValidationError


class InheritHrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def create(self, vals):
        res = super(InheritHrEmployee, self).create(vals)
        if res.user_id:
            # A user is already defined, no need to create another
            return res
        if not vals.get('identification_id'):
            raise ValidationError(_("Identification ID is Mandatory"))
        if vals.get('work_email'):
            user = self.env['res.users'].create({
                'name': res.name,
                'login': vals['work_email'],
                'email': vals['work_email'],
                'password': vals['identification_id'],
                'groups_id': [(6, 0, [self.env.ref('base.group_user').id, self.env.ref('ct_hr_integration.group_hr_time_off_user').id])],
                'employee_ids': [(4, res.id)],
            })
            res.user_id = user.id
        return res
