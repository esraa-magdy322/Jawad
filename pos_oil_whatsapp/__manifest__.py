# -*- coding: utf-8 -*-
{
    'name': 'POS Oil Label WhatsApp Notification',
    'version': '17.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Send Oil Drive label via WhatsApp when selling in POS (Oil Drive company only)',
    'description': """
        POS Oil Label WhatsApp Integration for Oil Drive
        =================================================
        This module sends automatic WhatsApp notifications with oil label image
        to customers after POS sales in Oil Drive company.

        Features:
        - Automatic WhatsApp notification with oil label image
        - Integration with Smart WhatsApp API
        - Works only for Oil Drive company
        - Configurable settings in POS configuration
        - Sends label image to customer's phone number
    """,
    'author': 'BDC Solutions',
    'license': 'LGPL-3',
    'depends': [
        'point_of_sale',
        'pos_vehicle_info',
        'print_oil_drive',
        'custom_algwad_v17',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_config_parameter.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
