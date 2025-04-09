# -*- coding: utf-8 -*-
{
    'name': "Job Cost Customization",

    'summary': "Job Cost Customization"
       """,

    'description': "Job Cost Customization"
       
    """,

    'author': "Enas Yasser",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','odoo_job_costing_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sales_view.xml',
        'views/stock.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
