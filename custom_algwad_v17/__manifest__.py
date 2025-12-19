# -*- coding: utf-8 -*-
{
    'name': "Custom Invoice Report elgwad",

    'summary': """
    Invoice VAT
\t""",
    'description': """
    Invoice VAT  
    """,
    'version': '17.0.1.0.1',
   
    'license': 'LGPL-3',
    'category': 'Accounting',
    'depends': ['l10n_sa','base','account','sale'],

    # always loaded
    'data': [

        'report/report_layouts.xml',
        'report/invoice_report_template.xml',
        'report/sale_order_report_template.xml',
        'views/account_move_views.xml',
        'views/sale_order_views.xml',
           ],
    "assets": {
        'web.report_assets_common': [
            "custom_algwad_v17/static/src/css/style.css",
            # "invoice_vat/static/src/css/stock_report_style.css",
        ],

    }
    # only loaded in demonstration mode

}
