# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    opening_balance = fields.Float(string="Opening Balance", compute='_compute_opening_balance', store= True )

    @api.depends('account_id', 'date')
    def _compute_opening_balance(self):
        for rec in self:
            total_debit = total_credit = 0
            rec.opening_balance = 0
            company = self.env.company.id
            if rec.account_id:
                move_ids = self.env['account.move.line'].search(
                    [('date', '<', rec.date), ('parent_state', '=', 'posted'), ('company_id', '=', company),
                     ('account_id', '=', rec.account_id.id)], order='date')

                for move in move_ids:
                    total_debit = total_debit + move.debit
                    total_credit = total_credit + move.credit

                open_balance = total_debit - total_credit
                rec.opening_balance = open_balance
