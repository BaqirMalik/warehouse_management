{
    'name': 'CT Loan Management',
    'version': '17.0.0.0.0',
    'category': 'Human Resources',
    'summary': 'Manage Employee Loan Requests',
    'description': """This module facilitates the creation and management of employee loan requests. 
    The loan amount is automatically deducted from the salary""",
    'author': "Crecentech",
    'company': 'Crecentech',
    'website': "https://crecentech.com/",
    'depends': ['hr','base','hr_contract','account','ct_employees_management','om_account_accountant'],
    'data': [
        'security/hr_loan_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/ir_cron.xml',
        'data/loan_email_tempelate.xml',
        'views/hr_loan_views.xml',
        'views/hr_employee_views.xml',
    ],

    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
