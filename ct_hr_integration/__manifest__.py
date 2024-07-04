# -*- coding: utf-8 -*-
{
    'name': "CT Inventory Consumption",
    'summary': "Adjust the inventory in warehouse on consumption",
    'description': """
        This Application Is developed to Customize the HR Module in Odoo17.
    """,
    'author': "Crecentech",
    'website': "https://crecentech.com/",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['website','hr_recruitment'],
    'data': [
        'data/custom_hr_integration_data.xml',
        'views/menus.xml',
        'views/inherit_hr_job_views.xml',
    ],
}

