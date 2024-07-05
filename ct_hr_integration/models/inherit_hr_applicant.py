from odoo import fields, models, api


class InheritHrApplicant(models.Model):
    _inherit = "hr.applicant"

    redirect_link = fields.Char(string='Redirect Link')

    @api.model
    def create(self, vals):
        record = super().create(vals)
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        base_url += '/web#id=%d&view_type=form&model=%s' % (record.id, record._name)
        record.write({'redirect_link': base_url})
        return record