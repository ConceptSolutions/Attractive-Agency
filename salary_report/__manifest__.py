# -*- coding: utf-8 -*-
{
    'name': "salary_report",
    'summary': "Salary Report in Details",


    'author': "Marwa Abouzaid",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Reporting',
    'version': '16.0.0',
    "license": "AGPL-3",

    # any module necessary for this one to work correctly
    'depends': ['base','hr_payroll','Add_Rule_Category'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/excel_report.xml',
        'views/salary_report_category_view.xml',
        'views/salary_report_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
