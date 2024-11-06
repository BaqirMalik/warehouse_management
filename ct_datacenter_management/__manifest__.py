# -*- coding: utf-8 -*-
{
    'name': "CT Datacenter Management",
    'summary': "Manage Datacenter Infrastructure-Hardware",
    'description': """
    
    """,
    'author': "Crecentech",
    'license': 'LGPL-3',
    'website': "https://crecentech.com/",
    'category': 'inventory',
    'version': '0.1',
    'depends': ['mail', 'ct_employees_management'],
    'data': [
        'security/ir.model.access.csv',
        'report/ir_actions_report.xml',
        'report/ir_actions_report_templates.xml',
        'views/internet.xml',
        'views/rack_server_view.xml'
    ],
    'assets':
        {
            'web.assets_backend': [
                'ct_datacenter_management/static/src/js/excel_report.js'
            ],
        },
}
