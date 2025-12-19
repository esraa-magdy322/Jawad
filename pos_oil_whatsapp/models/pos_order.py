# -*- coding: utf-8 -*-
import logging
import requests
import json
import base64
import os
import tempfile
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = 'pos.order'
    
    oil_whatsapp_sent = fields.Boolean(
        string='Oil Label WhatsApp Sent',
        default=False,
        help='Indicates if oil label WhatsApp was sent to customer'
    )
    
    def _is_oil_drive_company(self):
        company_name = self.company_id.name if self.company_id else ''
        is_oil_drive = any(word in company_name for word in ['أويل', 'درايف', 'Oil', 'oil', 'Drive', 'drive'])
        return is_oil_drive
    
    def write(self, vals):
        result = super(PosOrder, self).write(vals)
        
        for order in self:
            if order.track and order.next_track and not order.oil_whatsapp_sent:
                _logger.info(f"Order {order.name} has vehicle data - checking WhatsApp send")
                try:
                    order.send_oil_label_whatsapp()
                except Exception as e:
                    _logger.error(f"Failed to send WhatsApp for {order.name}: {e}")
        
        return result
    
    def send_oil_label_whatsapp(self):
        self.ensure_one()
        
        _logger.info(f"Starting WhatsApp send for order {self.name}")
        
        if not self._is_oil_drive_company():
            _logger.info("Not Oil Drive company - skipping")
            return
        
        ICP = self.env['ir.config_parameter'].sudo()
        enabled = ICP.get_param('pos_oil_whatsapp.enabled', 'False').lower() == 'true'
        if not enabled:
            _logger.info("Oil WhatsApp is disabled")
            return
        
        if not self.track or not self.next_track:
            _logger.info("No vehicle data - skipping")
            return
        
        if not self.partner_id or not self.partner_id.phone:
            _logger.warning("No customer/phone")
            return
        
        phone_number = self._format_phone_number(self.partner_id.phone)
        
        try:
            oil_image_base64 = self._generate_oil_label_image()
            if not oil_image_base64:
                return
            
            _logger.info(f"Oil label image generated ({len(oil_image_base64)} bytes)")
        except Exception as e:
            _logger.error(f"Error generating label: {e}")
            return
        
        instance_id = ICP.get_param('pos_oil_whatsapp.instance_id')
        access_token = ICP.get_param('pos_oil_whatsapp.access_token')
        
        if not instance_id or not access_token:
            _logger.error("Credentials not configured")
            return
        
        customer_name = self.partner_id.name or 'عميل'
        car_info = ""
        if self.plate_number:
            car_info += f"رقم {self.plate_number}"
        if self.car_type:
            car_info += f" - {self.car_type}"
        
        caption = f"مرحباً {customer_name}, هذا تذكير تغيير الزيت لسيارتك {car_info}"
        
        try:
            success = self._send_whatsapp_image(phone_number, caption, oil_image_base64, instance_id, access_token)
            if success:
                self.oil_whatsapp_sent = True
                _logger.info(f"WhatsApp sent successfully for {self.name}")
        except Exception as e:
            _logger.error(f"Error sending: {e}")
    
    def _generate_oil_label_image(self):
        try:
            temp_invoice = self.env['account.move'].sudo().create({
                'move_type': 'out_invoice',
                'plate_number': self.plate_number or '',
                'car_type': self.car_type or '',
                'car_model': self.car_model or 0,
                'track': self.track or 0,
                'next_track': self.next_track or 0,
            })
            
            temp_invoice._compute_oil_label_image()
            oil_image = temp_invoice.oil_label_image
            temp_invoice.unlink()
            return oil_image
        except Exception as e:
            _logger.error(f"Error: {e}")
            return None
    
    def _send_whatsapp_image(self, phone_number, caption, image_base64, instance_id, access_token):
        api_url = "https://app.smartwats.com/api/send"
        
        # Decode base64
        if isinstance(image_base64, str):
            image_str = image_base64
        else:
            image_str = image_base64.decode('utf-8')
        
        # Send image with caption
        payload = {
            "number": phone_number,
            "type": "media",
            "message": caption,
            "media_url": f"data:image/png;base64,{image_str}",
            "filename": "oil_label.png",
            "instance_id": instance_id,
            "access_token": access_token
        }
        
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        
        _logger.info(f"Sending WhatsApp image to {phone_number}")
        _logger.info(f"Image size: {len(image_str)} chars")
        
        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=30)
            result = response.json()
            _logger.info(f"WhatsApp API response: {result}")
            
            if result.get('status') == 'success':
                return True
            else:
                _logger.error(f"API returned error: {result}")
                return False
        except Exception as e:
            _logger.error(f"API error: {e}")
            return False
    
    def _format_phone_number(self, phone):
        if not phone:
            return ""
        phone = ''.join(filter(str.isdigit, phone))
        if phone.startswith('00'):
            phone = phone[2:]
        if len(phone) > 10:
            return phone
        if len(phone) == 10 and phone.startswith('1'):
            return '20' + phone
        if len(phone) == 9 and phone.startswith('5'):
            return '966' + phone
        return phone
