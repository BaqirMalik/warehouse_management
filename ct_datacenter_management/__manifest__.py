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
    'depends': ['mail'],
    'data': [
            'security/ir.model.access.csv',
            'views/internet.xml',
            'views/rack_server_view.xml'
    ],
}

