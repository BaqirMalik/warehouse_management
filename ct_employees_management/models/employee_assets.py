from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class EmployeeAssets(models.Model):
    _name = 'employee.assets'
    _description = 'employee assets'
    _rec_name = "sequence"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char('Asset Name', required=True, tracking=True)
    image = fields.Binary("Image")
    employee_id = fields.Many2one('hr.employee', string='Employee', tracking=True)
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'In active')
    ], string='Status', required=True, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ready', 'Ready'),
        ('assigned', 'Assigned')
    ], default='draft', tracking=True)
    mouse = fields.Boolean(string='Mouse', tracking=True)
    mouse_brand = fields.Char(string='Mouse Detail', tracking=True)
    keyboard = fields.Boolean(string='Keyboard', tracking=True)
    lcd = fields.Boolean(string='LCD Display', tracking=True)
    lcd_brand = fields.Char(string='LCD Detail', tracking=True)
    charger = fields.Boolean(string='Charger', tracking=True)
    headphone = fields.Boolean(string='HeadPhone', tracking=True)
    handsfree = fields.Boolean(string='Handsfree', tracking=True)
    headphone_brand = fields.Char(string='HeadPhone Detail', tracking=True)
    headphone_issue_date = fields.Date(string='HeadPhone Issue Date', tracking=True)
    core = fields.Many2one('laptop.core',string='Core', tracking=True)
    generation = fields.Many2one('laptop.generation',string='Generation', tracking=True)
    ram = fields.Char(string='RAM', tracking=True)
    rom = fields.Char(string='ROM / SSD / HDD', tracking=True)
    is_graphic_card = fields.Boolean(string='Is Graphic Card?', tracking=True)
    graphic_card = fields.Char(string='Graphic Card', tracking=True)
    assets_lines = fields.One2many('employee.assets.lines', 'assets_id', tracking=True)

    sequence = fields.Char(string='Sequence', required=True, copy=False, readonly=True, index=True,
                            default=lambda self: _('New'))

    display_name = fields.Char(compute='_compute_display_name')
    battery_health = fields.Char("Battery Health", tracking=True)
    other_notes = fields.Text("Other Notes", tracking=True)
    any_hardware_issue = fields.Text("Any Hardware Issue", tracking=True)

    @api.depends('name','display_name')  # this definition is recursive
    def _compute_display_name(self):
        for rec in self:
            if rec.name:
                rec.display_name = f"{rec.sequence} - {rec.name} - {rec.core.code} - {rec.generation.code} - {rec.ram} - {rec.rom}"
            else:
                rec.display_name = False

    def action_ready(self):
        self.state = 'ready'

    def action_assigned(self):
        if self.employee_id.id == False:
            raise ValidationError(_("Employee is mandatory to assigned the asset"))
        elif self.employee_id.employee_assets:
            raise ValidationError(_("Assets already Assigned to this Employee"))
        else:
            self.employee_id.employee_assets = self.id
            self.state = 'assigned'

    def action_returned(self):
        self.employee_id.employee_assets = False
        self.state = 'returned'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sequence', _('New')) == _('New'):
                vals['sequence'] = self.env['ir.sequence'].next_by_code('employee.assets') or _('New')
        res = super(EmployeeAssets, self).create(vals_list)
        return res

    def unlink(self):
        for rec in self:
            if rec.employee_id:
                raise ValidationError(_('You Cannot Delete an asset that is Assigned to Employee!'))
        return super(EmployeeAssets, self).unlink()


    class EmployeeAssitsLines(models.Model):
        _name = 'employee.assets.lines'
        _description = 'employee assets lines'

        employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
        date = fields.Date(string='Date')
        notes = fields.Char(string='Repair Notes')
        assets_id = fields.Many2one('employee.assets')
        expense_amount = fields.Float(string='Expense Amount')

        invoice_pdf_report_file = fields.Binary(
            attachment=True,
            string="Receipt Attachment",
            copy=False,
            required=True,
        )
        invoice_pdf_report_file_name = fields.Char("File Name")

