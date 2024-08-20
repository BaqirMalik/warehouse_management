# -*- coding: utf-8 -*-
{
    'name': "product_customization",
    'summary': "Short (1 phrase/line) summary of the module's purpose",
    'description': """Long description of module's purpose""",
    'author': "Crecentech Systems",
    'website': "https://crecentech.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['product', 'account', 'point_of_sale'],
    'data': [
        'views/product_form_inherit.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'product_customization/static/src/**/*',
    ],
    },
}
