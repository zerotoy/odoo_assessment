# -*- coding: utf-8 -*-
{
    'name': "room_module",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','odoo-rest-api-master'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/room_reservation_views.xml',
        'views/room_views.xml',
        'views/views.xml',
    
        'data/room_reservation_seq.xml',
        'data/inject_data_dummy.xml',
    ],
    # 'pre_init_hook': 'pre_init_hook',
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
