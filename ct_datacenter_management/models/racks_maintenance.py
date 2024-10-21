from odoo import models, fields

class RackMaintenance(models.Model):
    _name = 'rack.maintenance'
    _description = 'Maintenance Records for Racks'

    rack_id = fields.Many2one('rack.server', string='Rack', required=True)  # Replace 'rack.model' with your actual rack model name
    responsible_id = fields.Many2one('res.users', string='Responsible')
    maintenance_date = fields.Date(string='Maintenance Date', required=True)
    maintenance_cost = fields.Float(string='Cost')
    notes = fields.Text(string='Maintenance Notes')
