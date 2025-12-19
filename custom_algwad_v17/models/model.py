from odoo import api, fields, models, _
from odoo.tools import float_repr
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import base64
import pytz
from odoo.osv.expression import AND
from collections import defaultdict
import qrcode
import binascii
from io import BytesIO


class AccountMove(models.Model):
    _inherit = 'account.move'

    total_tax_company_currency = fields.Monetary(compute="_compute_total_tax_company_currency", readonly=True,
                                                 currency_field='company_currency_id', store=True)
    add_debit_note = fields.Boolean(default=False)
    add_credit_note = fields.Boolean(default=False)
    amount_discount_total = fields.Monetary(string="Amount discount total", compute="_compute_total", store='True',
                                            help="")
    amount_sale_total = fields.Monetary(string="Amount sale total", compute="_compute_total", store='True', help="")
    qr_code = fields.Binary(string="QR Code", attachment=True, compute="_compute_qr_code")
    plate_number = fields.Char(string='اللوحة')
    car_type = fields.Char(string='نوع السيارة')
    car_model = fields.Integer(string='الموديل')
    track = fields.Integer(string='الممشى')
    next_track = fields.Integer(string='الممشى القادم')
    terms_conditions = fields.Html(string='Terms & Conditions / الشروط والأحكام', compute='_compute_terms_and_bank', store=False)
    default_bank = fields.Html(string='Bank Information', compute='_compute_terms_and_bank', store=False)
    @api.depends("company_id", "company_id.invoice_terms", "company_id.invoice_bank_info")
    def _compute_terms_and_bank(self):
        for rec in self:
            rec.terms_conditions = rec.company_id.invoice_terms or ""
            rec.default_bank = rec.company_id.invoice_bank_info or ""


    @api.depends('company_id.name', 'company_id.vat', 'partner_id.name', 'partner_id.vat',
                 'create_date', 'amount_total', 'amount_tax', 'move_type')
    def _compute_qr_code(self):
        for rec in self:
            if rec.move_type in ('out_invoice', 'out_refund', 'in_invoice', 'in_refund'):
                try:
                    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
                    qr.add_data(rec.get_qr_code_data())
                    qr.make(fit=True)
                    img = qr.make_image()
                    temp = BytesIO()
                    img.save(temp, format="PNG")
                    qr_image = base64.b64encode(temp.getvalue())
                    rec.qr_code = qr_image
                except Exception as e:
                    rec.qr_code = False
            else:
                rec.qr_code = False

    def get_qr_code_data(self):
        if self.move_type in ('out_invoice', 'out_refund'):
            sellername = str(self.company_id.name)
            seller_vat_no = self.company_id.vat or ''
            if self.partner_id.company_type == 'company':
                customer_name = self.partner_id.name
                customer_vat = self.partner_id.vat
        else:
            sellername = str(self.partner_id.name)
            seller_vat_no = self.partner_id.vat
        seller_hex = self._get_hex("01", "0c", sellername)
        vat_hex = self._get_hex("02", "0f", seller_vat_no) or ""
        time_stamp = str(self.create_date)
        date_hex = self._get_hex("03", "14", time_stamp)
        total_with_vat_hex = self._get_hex("04", "0a", str(round(self.amount_total, 2))) or 0
        total_vat_hex = self._get_hex("05", "09", str(round(self.amount_tax, 2))) or 0
        print(vat_hex)
        qr_hex = seller_hex + vat_hex + date_hex + total_with_vat_hex + total_vat_hex
        encoded_base64_bytes = base64.b64encode(bytes.fromhex(qr_hex)).decode()
        return encoded_base64_bytes

    def _get_hex(self, tag, length, value):
        if tag and length and value:
            hex_string = self._string_to_hex(value)
            length = int(len(hex_string) / 2)
            conversion_table = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
            hexadecimal = ''
            while (length > 0):
                remainder = length % 16
                hexadecimal = conversion_table[remainder] + hexadecimal
                length = length // 16
            # print(hexadecimal)
            if len(hexadecimal) == 1:
                hexadecimal = "0" + hexadecimal
            return tag + hexadecimal + hex_string

    def _string_to_hex(self, value):
        if value:
            string = str(value)
            string_bytes = string.encode("UTF-8")
            encoded_hex_value = binascii.hexlify(string_bytes)
            hex_value = encoded_hex_value.decode("UTF-8")
            return hex_value

    def action_print_empty_invoice(self):
        """Print Empty Invoice Template"""
        return self.sudo().env.ref("custom_algwad_v17.action_report_empty_invoice").report_action(self.sudo())

    def _get_name_invoice_report(self):
        """ This method need to be inherit by the localizations if they want to print a custom invoice report instead of
        the default one. For example please review the l10n_ar module """
        self.ensure_one()
        super()._get_name_invoice_report()

        return 'account.report_invoice_document'

    @api.depends('currency_id', 'amount_tax', 'company_currency_id', 'invoice_date', 'company_id')
    def _compute_total_tax_company_currency(self):
        for rec in self:
            rec.total_tax_company_currency = rec.currency_id._convert(
                rec.amount_tax, rec.company_currency_id, rec.company_id,
                rec.invoice_date or fields.Date.context_today(self), round=False)

    @api.depends('invoice_line_ids', 'amount_total')
    def _compute_total(self):
        for r in self:
            r.amount_sale_total = r.amount_untaxed + sum(line.amount_discount for line in r.invoice_line_ids)
            r.amount_discount_total = sum(line.amount_discount for line in r.invoice_line_ids)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    #
    price_tax = fields.Monetary(string='Invoice Tax Amount', compute='_compute_price_tax', store=True)
    amount_discount = fields.Monetary(string="Amount discount", compute="_compute_amount_discount", store='True',
                                      help="")

    def _get_price_tax(self, tax_id):
        price = (self.price_unit * self.quantity) * (1 - (self.discount or 0.0) / 100.0)
        # Simplified calculation for display purposes
        return price * (tax_id.amount / 100.0) if tax_id.amount_type == 'percent' else 0

    @api.depends('price_unit', 'discount', 'tax_ids', 'quantity',
                 'product_id', 'move_id.partner_id', 'move_id.currency_id', 'move_id.company_id',
                 'move_id.invoice_date', 'move_id.date', 'price_total')
    def _compute_price_tax(self):
        for rec in self:
            try:
                rec.price_tax = sum([rec._get_price_tax(tax) for tax in rec.tax_ids])
            except:
                rec.price_tax = 0.0

    @api.depends('discount', 'quantity', 'price_unit')
    def _compute_amount_discount(self):
        for r in self:
            r.amount_discount = r.quantity * r.price_unit * (r.discount / 100)
