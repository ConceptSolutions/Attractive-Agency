# -*- coding: utf-8 -*-
{
    'name': "SW - HR Attendance ZKTeco",
    'summary': """Integration with ZKTeco Biometric Devices""",
    'description': "",
    'license':  "Other proprietary",
    'author': "Smart Way Business Solutions",
    'website': "http://www.smartway-jo.com",
    'category': 'Human Resources',
    'version': '13.0.0.1',
    'depends': ['base', 'hr', 'hr_payroll', 'hr_contract', 'hr_attendance', 'mail', 'resource'],
    'data': [
        'data/get_attendance.xml',
        'security/biometricdevice_security.xml',
        'security/ir.model.access.csv',
        'views/company_view.xml',
        'views/hr_attendance_view.xml',
        'views/biometricdevice_view.xml',
        'views/hr_extensionview.xml',
        'views/settings.xml',
        'wizard/move_attendance_wizard_view.xml',
        'wizard/generate_missing_attendance.xml',
    ],
    'images':  ["static/description/image.png"],
    'price' : 160,
    'currency' :  'EUR',
    'installable': True,
    'auto_install': False,
    'application':False,    
}
