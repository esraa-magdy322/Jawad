# -*- coding: utf-8 -*-

from odoo import models, fields, _

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

    purchase_order_id = fields.Many2one(comodel_name="purchase.order")


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    payment_journal = fields.Many2one(comodel_name="account.journal", string="Payment Method", )
    payment_count = fields.Integer(string='Payment Count', compute='compute_payment_count')
    pay_type = fields.Selection(string="Payment Type", selection=[('cash', 'Cash'), ('credit', 'Credit'), ],
                                required=False, default='credit')

    def compute_payment_count(self):
        for rec in self:
            rec.payment_count = 0
            payments = self.env['account.payment'].search([('purchase_order_id', '=', rec.id)])
            if payments:
                rec.payment_count = len(payments)

    def action_view_payments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Order Payments'),
            'res_model': 'account.payment',
            'domain': [('purchase_order_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current'
        }

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for order in self:
            warehouse_id = order.picking_type_id.warehouse_id
            if warehouse_id.reception_done and order.picking_ids:
                for picking_id in self.picking_ids:
                    if picking_id.state == 'assigned':
                        picking_id.action_assign()
                        picking_id.button_validate()
            if warehouse_id.create_bill and not order.invoice_ids:
                order.action_create_invoice()
            if warehouse_id.validate_bill and order.invoice_ids:
                bill = order.invoice_ids[0]
                if bill.state == 'draft':
                    bill.action_post()
                if warehouse_id.pay_bill and order.payment_journal and order.pay_type == 'cash':
                    payment = self.env['account.payment'].create({
                        'currency_id': bill.currency_id.id,
                        'amount': bill.amount_total,
                        'payment_type': 'outbound',
                        'partner_id': bill.commercial_partner_id.id,
                        'partner_type': MAP_INVOICE_TYPE_PARTNER_TYPE[bill.move_type],
                        'ref': bill.payment_reference or bill.name,
                        'journal_id': order.payment_journal.id,
                        'purchase_order_id': order.id
                    })
                    payment.action_post()
                    line_id = payment.line_ids.filtered(lambda l: l.debit)
                    bill.js_assign_outstanding_line(line_id.id)
        return res

    # def button_approve(self, force=False):
    #     parent_result = super(PurchaseOrder, self).button_approve(force=force)
    #     self._create_picking()
    #     self.button_confirm()
    #     return parent_result

    def _approval_allowed(self):
        parent_result = super(PurchaseOrder, self)._approval_allowed()
        done_without_approval = True if self.company_id.done_without_approval == 'yes' else False
        if done_without_approval:
            return True
        return parent_result

    def _prepare_invoice(self):
        parent_result = super(PurchaseOrder, self)._prepare_invoice()
        parent_result.update(invoice_date=fields.Date.today())
        return parent_result
