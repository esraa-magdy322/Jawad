# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Sale Purchase Order Automation',
    'version': '17.0',
    'author': 'Ahmed Said',
    'category': 'Sales',
    'summary': """Enable auto sale and purchase order workflow  confirmation.
     Include operations like Auto Create Invoice, Auto Validate Invoice and Auto Transfer Delivery Order.""",
    'description': """
        You can directly create invoice and set done to delivery order by single click
    """,
    'license': 'LGPL-3',
    'depends': ['sale_stock', 'account', 'sale', 'purchase', 'account'],
    'data': [
        'views/stock_warehouse.xml',
        'views/setting.xml',
        'views/account_move.xml',
        'views/sales_order.xml',
        'views/purchase_order.xml',
        # 'report/invoice_report.xml',
    ],

    'installable': True,
    'application': True,

}
