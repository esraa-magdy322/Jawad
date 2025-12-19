# -*- coding: utf-8 -*-
from odoo import fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    invoice_bank_info = fields.Text(
        string='Bank Information',
        help='Bank information to appear on invoices'
    )
