# -*- coding: utf-8 -*-
{
    'name': "account_customization",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Ahmed Said",
    'website': "https://www.yourcompany.com",
    'category': 'account',
    'version': '17.0',

    'depends': ['base' , 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

