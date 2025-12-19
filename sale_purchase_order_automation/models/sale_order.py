from odoo import fields, models, _, api

MAP_INVOICE_TYPE_PARTNER_TYPE = {
    'out_invoice': 'customer',
    'out_refund': 'customer',
    'out_receipt': 'customer',
    'in_invoice': 'supplier',
    'in_refund': 'supplier',
    'in_receipt': 'supplier',
}


class AccountPayment(models.Model):
    _inherit = "account.payment"

    sale_id = fields.Many2one(comodel_name="sale.order")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_journal = fields.Many2one(comodel_name="account.journal", string="Payment Method", )
    payment_count = fields.Integer(string='Payment Count', compute='compute_payment_count')
    pay_type = fields.Selection(string="Payment Type", selection=[('cash', 'Cash'), ('credit', 'Credit'), ],
                                required=False, default='credit')

    @api.onchange('pay_type')
    def onchange_pay_type(self):
        if self.pay_type == 'credit':
            self.payment_journal = False

    def compute_payment_count(self):
        for rec in self:
            rec.payment_count = 0
            payments = self.env['account.payment'].search([('sale_id', '=', rec.id)])
            if payments:
                rec.payment_count = len(payments)

    def action_view_payments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Order Payments'),
            'res_model': 'account.payment',
            'domain': [('sale_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current'
        }

    def action_confirm(self):
        res = super(SaleOrder, self.with_context(default_immediate_transfer=True)).action_confirm()
        for order in self:
            warehouse = order.warehouse_id
            if warehouse.is_delivery_set_to_done and order.picking_ids:
                for picking in self.picking_ids:
                    if picking.state == 'cancel':
                        continue
                    for move in picking.move_ids:
                        move.quantity = move.product_qty
                    picking._autoconfirm_picking()
                    picking.button_validate()
                    for move_line in picking.move_ids_without_package:
                        move_line.quantity = move_line.product_uom_qty
                    for mv_line in picking.move_ids.mapped('move_line_ids'):
                        mv_line.quantity = mv_line.quantity_product_uom

                    picking._action_done()

            if warehouse.create_invoice and not order.invoice_ids:
                order._create_invoices()
            if warehouse.validate_invoice and order.invoice_ids:
                for invoice in order.invoice_ids:
                    invoice.action_post()
                    if warehouse.pay_invoice and order.payment_journal:
                        payment = self.env['account.payment'].create({
                            'currency_id': invoice.currency_id.id,
                            'amount': invoice.amount_total,
                            'payment_type': 'inbound',
                            'partner_id': invoice.commercial_partner_id.id,
                            'partner_type': MAP_INVOICE_TYPE_PARTNER_TYPE[invoice.move_type],
                            'ref': invoice.payment_reference or invoice.name,
                            'journal_id': order.payment_journal.id,
                            'sale_id': order.id
                        })

                        payment.action_post()
                        line_id = payment.line_ids.filtered(lambda l: l.credit)
                        invoice.js_assign_outstanding_line(line_id.id)

        return res

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        if res:
            res['pay_type'] = self.pay_type or False
            res['payment_journal'] = self.payment_journal.id if self.payment_journal else False
        return res


class AccountMove(models.Model):
    _inherit = 'account.move'

    pay_type = fields.Selection(string="Payment Type", selection=[('cash', 'Cash'), ('credit', 'Credit'), ],
                                required=False, )
    payment_journal = fields.Many2one(comodel_name="account.journal", string="Payment Method", )
