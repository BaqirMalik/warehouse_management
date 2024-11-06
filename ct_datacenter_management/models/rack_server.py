import io
import json

import xlsxwriter

from odoo import fields, models, _, api
from odoo.tools import date_utils


class RackServer(models.Model):
    _name = 'rack.server'
    _rec_name = 'server_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    server_name = fields.Char(string='Server Name', required=True, tracking=True)
    ip_address = fields.Char(string='IP Address', tracking=True)
    no_of_nics = fields.Integer(string='Number of NICs', tracking=True)
    virtual_machines = fields.Integer(string='Number of VM', compute='_compute_count')
    storage_capacity = fields.Char(string='Data Storage (TB)', tracking=True)
    model = fields.Char(string='Model', tracking=True)
    processor_info = fields.Char(string='Processor Info', tracking=True)
    total_memory = fields.Char(string='Total Memory (GB)', tracking=True)
    vm_specs_ids = fields.One2many('vm.specs', 'rack_server_id')
    racks_maintenance_ids = fields.One2many('rack.maintenance', 'rack_id')
    operating_system = fields.Char(string='Operating System', tracking=True)
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'In Active')
    ], string='Status', tracking=True)

    @api.depends('vm_specs_ids')
    def _compute_count(self):
        for record in self:
            record.virtual_machines = len(record.vm_specs_ids)


    def print_excel_report(self):
        data = self._context['active_ids']
        return {
            'type': 'ir.actions.report',
            'report_type': 'xlsx',
            'data': {'model': 'rack.server',
                     'output_format': 'xlsx',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'report_name': 'DataCenter/Excel Report', }, }

    def get_xlsx_report(self, datas, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        for servers in self.env['rack.server'].browse(datas):
            sheet_name = servers.server_name
            sheet = workbook.add_worksheet(sheet_name)
            # Set column width and headers
            sheet.set_column(0, 4, 25)
            sheet.set_column(5, 8, 15)
            txt = workbook.add_format({'bold': True})

            sheet.write('A3', 'Server Name:', txt)
            sheet.write('A4', 'Model:', txt)
            sheet.write('A5', 'OS:', txt)
            sheet.write('A6', 'No of NICs:', txt)
            sheet.write('C3', 'Processor:', txt)
            sheet.write('C4', 'IP Address:', txt)
            sheet.write('C5', 'Storage:', txt)
            sheet.write('C6', 'No of VMs:', txt)
            sheet.write('A10', 'VM Name', txt)
            sheet.write('B10', 'Operating System', txt)
            sheet.write('C10', 'CPU Cores', txt)
            sheet.write('D10', 'RAM (GB)', txt)
            sheet.write('E10', 'Storage (GB)', txt)
            sheet.write('F10', 'IP Address', txt)
            sheet.write('G10', 'Status', txt)
            sheet.write('H10', 'Ownership', txt)

            sheet.merge_range('B1:C1', servers.server_name, txt)
            sheet.write('B3', servers.server_name)
            sheet.write('B4', servers.model)
            sheet.write('B5', servers.operating_system)
            sheet.write('B6', servers.no_of_nics)
            sheet.write('D3', servers.processor_info)
            sheet.write('D4', servers.ip_address)
            sheet.write('D5', servers.storage_capacity)
            sheet.write('D6', servers.virtual_machines)
            row = 10

            for line in servers.vm_specs_ids:
                # For adding value of the sale order lines

                sheet.write(row, 0, line.name)
                sheet.write(row, 1, line.operating_system)
                sheet.write(row, 2, line.cpu_cores)
                sheet.write(row, 3, line.ram)
                sheet.write(row, 4, line.storage)
                sheet.write(row, 5, line.ip_address)
                sheet.write(row, 6, line.status.capitalize())
                sheet.write(row, 7, line.ownership)

                row += 1
            row += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()



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
    rack_server_id = fields.Many2one('rack.server', string='VM Spec')
    ownership = fields.Char(string='Ownership', tracking=True)

