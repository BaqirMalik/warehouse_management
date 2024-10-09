# -*- coding: utf-8 -*-
{
    'name': "ct_employees_management",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'hr', 'hr_contract', 'om_hr_payroll','hr_gamification','account','hr_holidays'],
    'data': [
        'security/ir.model.access.csv',
        'security/hr_employee_security.xml',
        'data/ir_sequence_data.xml',
        'data/laptop_specs.xml',
        'data/provident_fund_conf.xml',
        'data/ir_cron.xml',
        'data/employee_mail_temp.xml',
        'views/employee_assets.xml',
        'views/inherit_hr_employee.xml',
        'views/employee_pf_views.xml',
        'views/laptop_specs.xml',
        'views/provident_fund_contribution.xml',
        'views/inherit_hr_contract.xml',
    ],
}
