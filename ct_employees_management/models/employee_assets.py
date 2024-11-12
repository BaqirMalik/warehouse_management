import io
import json

import xlsxwriter

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools import date_utils


def check_boolean_value(value):
    if value:
        result = 'yes'
    else:
        result = 'No'
    return result
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

    def print_excel_report(self):
        data = self._context['active_ids']
        return {
            'type': 'ir.actions.report',
            'report_type': 'xlsx',
            'data': {'model': 'employee.assets',
                     'output_format': 'xlsx',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'report_name': 'Assets/Detail Excel Report', }, }

    def get_xlsx_report(self, datas, response):
        """ From this function we can create and design the Excel file template
                 and the map the values in the corresponding cells
            :param datas: Selected record ids
            :param response: Response after creating excel
        """
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        # Create a single worksheet for all assets
        sheet = workbook.add_worksheet('Employee Assets')

        # Set column width and headers
        sheet.set_column(0, 2, 25)
        sheet.set_column(3, 10, 15)
        txt = workbook.add_format({'bold': True})
        sheet.write('A1', 'Assets Name', txt)
        sheet.write('B1', 'Employee Name', txt)
        sheet.write('C1', 'Pseudo Name', txt)
        sheet.write('D1', 'Core', txt)
        sheet.write('E1', 'Generation', txt)
        sheet.write('F1', 'RAM', txt)
        sheet.write('G1', 'ROM', txt)
        sheet.write('H1', 'Mouse', txt)
        sheet.write('I1', 'Charger', txt)
        sheet.write('J1', 'HeadPhone', txt)
        sheet.write('K1', 'Status', txt)

        row = 1  # Start writing data from the second row
        for assets in self.env['employee.assets'].browse(datas):
            sheet.write(row, 0, assets.name)
            sheet.write(row, 1, assets.employee_id.name)
            sheet.write(row, 2, assets.employee_id.pseudo_name)
            sheet.write(row, 3, assets.core.name)
            sheet.write(row, 4, assets.generation.name)
            sheet.write(row, 5, assets.ram)
            sheet.write(row, 6, assets.rom)
            sheet.write(row, 7, check_boolean_value(assets.mouse))
            sheet.write(row, 8, check_boolean_value(assets.charger))
            sheet.write(row, 9, check_boolean_value(assets.headphone))
            sheet.write(row, 10, assets.state.capitalize())
            row += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()


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
        )
        invoice_pdf_report_file_name = fields.Char("File Name")

