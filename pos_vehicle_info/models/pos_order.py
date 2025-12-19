# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class PosOrder(models.Model):
    _inherit = "pos.order"

    plate_number = fields.Char(string="Plate Number / رقم السيارة")
    car_type = fields.Char(string="Car Type / نوع السيارة")
    car_model = fields.Integer(string="Car Model / موديل السيارة")
    track = fields.Integer(string="Current Mileage / الممشى")
    next_track = fields.Integer(string="Next Mileage / الممشى القادم")

    @api.model
    def _order_fields(self, ui_order):
        """Add vehicle fields to order data received from POS"""
        order_fields = super(PosOrder, self)._order_fields(ui_order)
        
        # Add vehicle data from POS
        order_fields['plate_number'] = ui_order.get('plate_number', '')
        order_fields['car_type'] = ui_order.get('car_type', '')
        order_fields['car_model'] = ui_order.get('car_model', 0)
        order_fields['track'] = ui_order.get('track', 0)
        order_fields['next_track'] = ui_order.get('next_track', 0)
        
        _logger.info(f"Order fields from POS: plate={order_fields.get('plate_number')}, track={order_fields.get('track')}, next_track={order_fields.get('next_track')}")
        
        return order_fields

    def _prepare_invoice_vals(self):
        """Override to add vehicle info to invoice"""
        vals = super(PosOrder, self)._prepare_invoice_vals()
        vals.update({
            "plate_number": self.plate_number,
            "car_type": self.car_type,
            "car_model": self.car_model,
            "track": self.track,
            "next_track": self.next_track,
        })
        return vals
    
    @api.model
    def action_print_oil_label_from_pos(self, label_data):
        """Print oil label from POS data"""
        try:
            _logger.info(f"Received label data: {label_data}")
            
            # Create temp invoice for printing
            AccountMove = self.env['account.move'].sudo()
            
            temp_invoice = AccountMove.create({
                'move_type': 'out_invoice',
                'plate_number': label_data.get('plate_number', ''),
                'car_type': label_data.get('car_type', ''),
                'car_model': label_data.get('car_model', 0),
                'track': label_data.get('track', 0),
                'next_track': label_data.get('next_track', 0),
            })
            
            _logger.info(f"Created temp invoice ID: {temp_invoice.id}")
            
            # Compute oil label image
            temp_invoice._compute_oil_label_image()
            
            _logger.info(f"Oil label image computed: {bool(temp_invoice.oil_label_image)}")
            
            # Get report
            report = self.env.ref('print_oil_drive.action_report_oil_label').sudo()
            
            return report.report_action(temp_invoice)
            
        except Exception as e:
            _logger.error(f"Error printing oil label: {str(e)}", exc_info=True)
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'خطأ في الطباعة',
                    'message': str(e),
                    'type': 'danger',
                }
            }
