# -*- coding: utf-8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    invoice_bank_info = fields.Text(
        related='company_id.invoice_bank_info',
        string='Bank Information',
        readonly=False,
        help='Bank information to appear on invoices'
    )
