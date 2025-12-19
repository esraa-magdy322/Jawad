from odoo import fields, models


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    # sales
    is_delivery_set_to_done = fields.Boolean(string="Delivery Done?")
    create_invoice = fields.Boolean(string='Create Invoice?')
    validate_invoice = fields.Boolean(string='Validate invoice?')
    pay_invoice = fields.Boolean(string='Payment invoice?')
    # purchase
    reception_done = fields.Boolean(string="Receipt Done?")
    create_bill = fields.Boolean(string='Create Bill?')
    validate_bill = fields.Boolean(string='Validate Bill?')
    pay_bill = fields.Boolean(string='Payment Bill?')
