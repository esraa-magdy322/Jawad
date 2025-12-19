# -*- coding: utf-8 -*-
from odoo import models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def get_price_with_tax(self):
        """Calculate and return the product price including tax"""
        self.ensure_one()
        # Get the sale taxes for this product
        taxes = self.taxes_id.filtered(lambda t: t.company_id == self.env.company)
        if not taxes:
            return self.list_price
        
        # Calculate price with tax
        price = self.list_price
        tax_results = taxes.compute_all(price, currency=self.currency_id, quantity=1, product=self)
        return tax_results['total_included']

    def action_print_dymo_tax_label(self):
        """Print DYMO label with tax price directly"""
        return self.env.ref('dymo_label_tax.action_report_dymo_tax_label').report_action(self)
