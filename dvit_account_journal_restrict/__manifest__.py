# -*- coding: utf-8 -*-

{
    'name': "Journal Restrictions",
    'summary': """Restrict users to certain journals  convert from 10 : 15""",
    'description': """Restrict users to certain journals.""",
    'author': "DVIT.ME  edit by mohsen s.hassan",
    'website': "http://www.dvit.me",
    'license': 'AGPL-3',
    'category': 'account',
    'version': '10.0.3.0',
    'depends': ['account'],
    'data': [
        'views/users.xml',
        'security/security.xml',
    ],
    "images": [
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
