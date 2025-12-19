# -*- coding: utf-8 -*-
{
    'name': 'DYMO Label with Tax',
    'version': '17.0.1.0.0',
    'summary': 'Print DYMO product labels with price including tax',
    'description': '''
        This module adds a button to print DYMO labels 
        with the product price including tax (VAT).
    ''',
    'category': 'Sales/Sales',
    'author': 'BDC Solutions',
    'license': 'LGPL-3',
    'depends': ['product', 'account'],
    'data': [
        'report/dymo_tax_label_report.xml',
        'report/dymo_tax_label_template.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
