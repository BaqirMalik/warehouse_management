# -*- coding: utf-8 -*-
{
    'name': "CT Inventory Consumption",
    'summary': "Adjust the inventory in warehouse on consumption",
    'description': """
        This Application Is developed to record direct consumption of Material Used by the entity. 
        Through this application you Can add material Consumed cost To Cost of 
        Sales and deduct it from Inventory cost at specific warehouse or location.
    """,
    'author': "Crecentech",
    'website': "https://crecentech.com/",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['stock','product','account','purchase'],
    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/send_email_for_consumption_request.xml',
        'views/inventory_consumption_request_views.xml',
        'views/inherit_consumption_views.xml',
        'views/inherit_product_supplier_info.xml',
        'views/inherit_stock_move.xml',
        'views/inherit_purchase_order.xml',
        'views/inherit_new_quantity_wizard.xml',
        'views/menus.xml',
    ],
'assets': {
        'web.assets_backend': [
            'ct_inventory_consumption/static/src/scss/inventory_consumption_requests.scss',
        ],
}
}

