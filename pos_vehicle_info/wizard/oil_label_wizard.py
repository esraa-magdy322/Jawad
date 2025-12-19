# -*- coding: utf-8 -*-
from odoo import models, fields, api

class OilLabelWizard(models.TransientModel):
    _name = 'oil.label.wizard'
    _description = 'Oil Label Print Wizard'

    plate_number = fields.Char(string="Plate Number")
    car_type = fields.Char(string="Car Type")
    car_model = fields.Integer(string="Car Model")
    track = fields.Integer(string="Current Mileage")
    next_track = fields.Integer(string="Next Mileage")

    def action_print_label(self):
        """Print the oil label"""
        report = self.env.ref('print_oil_drive.action_report_oil_label')
        
        # Create temporary account.move for printing
        temp_invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'state': 'draft',
            'plate_number': self.plate_number,
            'car_type': self.car_type,
            'car_model': self.car_model,
            'track': self.track,
            'next_track': self.next_track,
        })
        
        # Generate PDF
        pdf_content, pdf_type = report._render_qweb_pdf(temp_invoice.ids)
        
        # Delete temp invoice
        temp_invoice.unlink()
        
        # Return PDF
        return {
            'type': 'ir.actions.report',
            'report_type': 'qweb-pdf',
            'report_name': 'print_oil_drive.report_oil_label_template',
            'report_file': 'print_oil_drive.report_oil_label_template',
            'data': pdf_content,
        }
