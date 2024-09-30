from odoo import models, fields

class EmployeeAssetsHistory(models.Model):
    _name = 'employee.assets.history'
    _description = 'Employee Assets History'

    employee_id = fields.Many2one('hr.employee')
    asset_id = fields.Many2one('employee.assets', "Assets")
    name = fields.Char('Asset Name', related="asset_id.name")
    core = fields.Many2one('laptop.core', string='Core', related="asset_id.core")
    generation = fields.Many2one('laptop.generation', string='Generation', related="asset_id.generation")
    ram = fields.Char(string='RAM', related="asset_id.ram")
    rom = fields.Char(string='ROM', related="asset_id.rom")
    is_graphic_card = fields.Boolean(string='Is Graphic Card?', related="asset_id.is_graphic_card")
    graphic_card = fields.Char(string='Graphic Card', related="asset_id.graphic_card")
    date = fields.Date("Issue Date")