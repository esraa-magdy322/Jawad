# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    pos_oil_whatsapp_enabled = fields.Boolean(
        string='Enable Oil Label WhatsApp Notifications',
        config_parameter='pos_oil_whatsapp.enabled',
        default=True,
        help='Send WhatsApp notifications with oil label image when selling in POS (Oil Drive only)'
    )
    
    pos_oil_smartwhatsapp_instance_id = fields.Char(
        string='Smart WhatsApp Instance ID',
        config_parameter='pos_oil_whatsapp.instance_id',
        help='Your Smart WhatsApp Instance ID'
    )
    
    pos_oil_smartwhatsapp_access_token = fields.Char(
        string='Smart WhatsApp Access Token',
        config_parameter='pos_oil_whatsapp.access_token',
        help='Your Smart WhatsApp Access Token'
    )
    
    pos_oil_message_template = fields.Char(
        string='WhatsApp Message Template',
        config_parameter='pos_oil_whatsapp.message_template',
        default='مرحباً {customer_name}, هذا تذكير تغيير الزيت لسيارتك {car_info}',
        help='Message template. Variables: {customer_name}, {car_info}, {plate_number}, {track}, {next_track}'
    )
