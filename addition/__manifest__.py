# -*- coding: utf-8 -*-
{
    'name': "Addition",
    'summary': """Addition""",
    'description': """Addition""",
    'author': "Abdulrhman Mohammed",
    'website': "http://www.almoasherbiz.com",
    'category': 'HR',
    'version': '13.0.0.1',
    'depends': ['base', 'hr','hr_payroll'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/bounce.xml',
        'views/bounce_type.xml',
        'views/contract.xml',
    ],

    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': True,
}
