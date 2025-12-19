# -*- coding: utf-8 -*-
from odoo import models, fields, api
import base64
import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


class AccountMove(models.Model):
    _inherit = 'account.move'

    is_oil_drive_company = fields.Boolean(
        string='Is Oil Drive Company',
        compute='_compute_is_oil_drive_company',
        store=False
    )

    oil_label_image = fields.Binary(
        string='Oil Label Image',
        compute='_compute_oil_label_image'
    )

    @api.depends('company_id')
    def _compute_is_oil_drive_company(self):
        """Check if current company is Oil Drive"""
        for record in self:
            company_name = record.company_id.name if record.company_id else ''
            record.is_oil_drive_company = any(word in company_name for word in ['أويل', 'درايف', 'Oil', 'oil', 'Drive', 'drive'])

    @api.depends('track', 'next_track')
    def _compute_oil_label_image(self):
        """Load the oil label template image and draw track and next_track on it"""
        module_path = os.path.dirname(os.path.dirname(__file__))
        image_path = os.path.join(module_path, 'static', 'src', 'img', 'oil_label_template.png')

        for record in self:
            if os.path.exists(image_path):
                # Open and use image AS IS - don't resize
                img = Image.open(image_path)
                draw = ImageDraw.Draw(img)

                # Load font
                try:
                    font = ImageFont.truetype("arial.ttf", 36)
                except:
                    try:
                        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
                    except:
                        try:
                            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 36)
                        except:
                            font = ImageFont.load_default()

                # Draw track
                if record.track:
                    track_text = str(record.track)
                    draw.text((569, 280), track_text, fill='black', font=font)

                # Draw next_track
                if record.next_track:
                    next_track_text = str(record.next_track)
                    draw.text((155, 280), next_track_text, fill='black', font=font)

                # Convert to base64 WITHOUT resizing
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                record.oil_label_image = base64.b64encode(buffer.getvalue())
            else:
                record.oil_label_image = False

    def action_print_oil_label(self):
        """Print the oil change label with the template image"""
        return self.env.ref('print_oil_drive.action_report_oil_label').report_action(self)
