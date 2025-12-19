# -*- coding: utf-8 -*-
from collections import defaultdict
from odoo import models, api


class ReportDymoTaxLabel(models.AbstractModel):
    _name = 'report.dymo_label_tax.report_dymo_tax_label_template'
    _description = 'DYMO Tax Label Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        products = self.env['product.template'].browse(docids)
        
        quantity_by_product = defaultdict(list)
        for product in products:
            # Use default_code (Internal Reference) as barcode
            barcode_value = product.default_code or product.barcode or ''
            quantity_by_product[product].append((barcode_value, 1))
        
        # Get default pricelist
        pricelist = self.env['product.pricelist'].search([], limit=1)
        
        return {
            'doc_ids': docids,
            'doc_model': 'product.template',
            'docs': products,
            'quantity': quantity_by_product,
            'pricelist': pricelist,
        }
