# -*- coding: utf-8 -*-
{
    'name': 'Elgawad Tax Report',
    'version': '17.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Export Tax Report to Excel',
    'description': """
        Export Tax Report to Excel
        This module adds menu items in Accounting Configuration
        to export tax reports to Excel format for both Sales and Vendor Bills.
    """,
    'author': 'Elgawad',
    'website': '',
    'depends': ['account', 'account_reports'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/tax_report_wizard_view.xml',
        'wizard/vendor_tax_report_wizard_view.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
