from odoo import fields,models,_

class RackServer(models.Model):
    _name = 'rack.server'
    _rec_name = 'server_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    server_name = fields.Char(string='Server Name', required=True, tracking=True)
    ip_address = fields.Char(string='IP Address', tracking=True)
    no_of_nics = fields.Integer(string='Number of NICs', tracking=True)
    virtual_machines = fields.Integer(string='Number of VM', tracking=True)
    storage_capacity = fields.Char(string='Data Storage (TB)', tracking=True)
    model = fields.Char(string='Model', tracking=True)
    processor_info = fields.Char(string='Processor Info', tracking=True)
    total_memory = fields.Char(string='Total Memory (GB)', tracking=True)
    vm_specs_ids = fields.One2many('vm.specs','rack_server_id')
    racks_maintenance_ids = fields.One2many('rack.maintenance','rack_id')
    operating_system = fields.Char(string='Operating System', tracking=True)
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'In Active')
    ],string='Status', tracking=True)






class VMSpec(models.Model):
    _name = 'vm.specs'
    _description = 'VMs Spec Details'

    name = fields.Char(string='VM Name', required=True, tracking=True)
    operating_system = fields.Char(string='Operating System', tracking=True)
    cpu_cores = fields.Integer(string='CPU Cores', tracking=True)
    ram = fields.Char(string='RAM (GB)', tracking=True)
    storage = fields.Char(string='Storage (GB)', tracking=True)
    ip_address = fields.Char(string='IP Address', tracking=True)
    status = fields.Selection(
        [('active', 'Active'), ('inactive', 'Inactive'), ('maintenance', 'Under Maintenance')],
        string='Status', default='active', tracking=True)
    rack_server_id = fields.Many2one('rack.server',string='VM Spec')
    ownership = fields.Char(string='Ownership', tracking=True)