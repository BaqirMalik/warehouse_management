# -*- coding: utf-8 -*-
{
    'name': "CT Expense Management",
    'summary': "Crecentech Expense Management",
    'description': """
        This Application Is developed to record direct expense of Company Used by the entity. .
    """,
    'license': 'LGPL-3',
    'author': "Crecentech",
    'website': "https://crecentech.com/",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['hr_expense'],
    'data': [
        'data/send_email_for_expense_request.xml',
        'views/inherit_hr_expense_form_view.xml',
    ],
}

