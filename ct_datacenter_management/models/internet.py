from odoo import fields,models,_

class Internet(models.Model):
    _name = 'internet.internet'
    _rec_name = 'provider'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    provider = fields.Char(string='Provider', required=True, tracking=True)
    speed = fields.Char(string='Speed', required=True, tracking=True)
    type = fields.Selection([
        ('dedicated', 'Dedicated'),
        ('shared', 'Shared')
    ])
    connection = fields.Selection([
        ('wired', 'Wired'),
        ('wireless', 'Wireless')
    ])
    backup_connection = fields.Selection([
        ('wired', 'Wired'),
        ('wireless', 'Wireless')
    ])
    status = fields.Selection([
        ('primary', 'Primary'),
        ('secondary', 'Secondary')
    ])