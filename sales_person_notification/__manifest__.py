{
    'name': 'Sales Person Notification',
    'version': '17.0.1.0.0',
    'category': 'Sales/CRM',
    'summary': 'Automated sales follow-up reminders based on customer invoice history',
    'description': """
Sales Person Notification
==========================
This module creates automatic To-do activities for salespeople to follow up with customers
after a specified period since their last invoice.

Key Features:
* Configure reminder period per customer (in days)
* Automatic daily cron job to check and create activities
* Assigns activities to responsible salesperson
* Prevents duplicate activity creation
    """,
    'author': 'Ahmed Ben Nagy',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
        'mail',
    ],
    'data': [
        'data/ir_cron.xml',
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
