# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.tools import float_repr


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    default_bank = fields.Char(string='default bank')   
    # Terms and Conditions
    terms_conditions = fields.Text(string='Terms & Conditions / الشروط والأحكام')
    
    # Computed fields for discount and sale totals
    amount_discount_total = fields.Monetary(
        string="Amount Discount Total", 
        compute="_compute_amount_discount_total", 
        store=True,
        help="Total discount amount"
    )
    amount_sale_total = fields.Monetary(
        string="Amount Sale Total", 
        compute="_compute_amount_sale_total", 
        store=True,
        help="Total sale amount before discount"
    )

    @api.depends('order_line.price_subtotal', 'order_line.discount')
    def _compute_amount_discount_total(self):
        for order in self:
            discount_total = 0.0
            for line in order.order_line:
                if line.discount > 0:
                    price_unit = line.price_unit
                    discount_amount = price_unit * line.product_uom_qty * (line.discount / 100.0)
                    discount_total += discount_amount
            order.amount_discount_total = discount_total

    @api.depends('order_line.price_unit', 'order_line.product_uom_qty')
    def _compute_amount_sale_total(self):
        for order in self:
            sale_total = 0.0
            for line in order.order_line:
                sale_total += line.price_unit * line.product_uom_qty
            order.amount_sale_total = sale_total

    def action_print_order(self):
        """Print hello world when button is clicked"""
        print("hello world")
        return True
