# -*- coding: utf-8 -*-
from odoo import models, fields, api
import io
import base64

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class TaxReportWizard(models.TransientModel):
    _name = "tax.report.wizard"
    _description = "Tax Report Excel Export Wizard"

    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company
    )
    excel_file = fields.Binary(string="Excel File", readonly=True)
    excel_filename = fields.Char(string="Filename", readonly=True)
    state = fields.Selection([
        ("draft", "Draft"),
        ("done", "Done"),
    ], default="draft")

    def action_export_excel(self):
        """Generate and download Excel report"""
        self.ensure_one()

        # Create Excel file in memory
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet("Invoices Report")

        # Define formats
        header_format = workbook.add_format({
            "bold": True,
            "bg_color": "#4472C4",
            "font_color": "white",
            "align": "center",
            "valign": "vcenter",
            "border": 1,
            "font_size": 12
        })

        cell_format = workbook.add_format({
            "align": "left",
            "valign": "vcenter",
            "border": 1
        })

        number_format = workbook.add_format({
            "align": "right",
            "valign": "vcenter",
            "border": 1,
            "num_format": "#,##0.00"
        })

        date_format = workbook.add_format({
            "align": "center",
            "valign": "vcenter",
            "border": 1,
            "num_format": "dd/mm/yyyy"
        })

        # Set column widths
        worksheet.set_column("A:A", 15)  # Invoice Date
        worksheet.set_column("B:B", 20)  # Number
        worksheet.set_column("C:C", 20)  # Reference
        worksheet.set_column("D:D", 35)  # Partner
        worksheet.set_column("E:E", 20)  # Partner/Tax ID
        worksheet.set_column("F:F", 18)  # Untaxed Amount
        worksheet.set_column("G:G", 15)  # Tax
        worksheet.set_column("H:H", 15)  # Total

        # Write headers
        worksheet.write(0, 0, "Invoice Date", header_format)
        worksheet.write(0, 1, "Number", header_format)
        worksheet.write(0, 2, "Reference", header_format)
        worksheet.write(0, 3, "Partner", header_format)
        worksheet.write(0, 4, "Partner/Tax ID", header_format)
        worksheet.write(0, 5, "Untaxed Amount", header_format)
        worksheet.write(0, 6, "Tax", header_format)
        worksheet.write(0, 7, "Total", header_format)

        # Get invoices data - Only Customer Invoices and Credit Notes
        domain = [
            ("move_type", "in", ["out_invoice", "out_refund"]),
            ("state", "=", "posted"),
            ("invoice_date", ">=", self.date_from),
            ("invoice_date", "<=", self.date_to),
            ("company_id", "=", self.company_id.id),
        ]

        # Use sudo() to bypass access rights issues
        invoices = self.env["account.move"].sudo().search(domain, order="invoice_date, name")

        # Write data
        row = 1
        for invoice in invoices:
            # Get partner data safely with sudo
            partner_name = invoice.partner_id.name if invoice.partner_id else ""
            partner_vat = invoice.partner_id.vat if invoice.partner_id else ""

            # Write invoice date
            if invoice.invoice_date:
                worksheet.write_datetime(row, 0, invoice.invoice_date, date_format)
            else:
                worksheet.write(row, 0, "", cell_format)

            worksheet.write(row, 1, invoice.name or "", cell_format)
            worksheet.write(row, 2, invoice.ref or "", cell_format)
            worksheet.write(row, 3, partner_name, cell_format)
            worksheet.write(row, 4, partner_vat or "", cell_format)
            worksheet.write(row, 5, invoice.amount_untaxed, number_format)
            worksheet.write(row, 6, invoice.amount_tax, number_format)
            worksheet.write(row, 7, invoice.amount_total, number_format)
            row += 1

        workbook.close()
        output.seek(0)

        # Save to wizard
        excel_data = output.read()
        output.close()

        filename = "Invoices_Report_%s_to_%s.xlsx" % (
            self.date_from.strftime("%Y%m%d"),
            self.date_to.strftime("%Y%m%d")
        )

        self.write({
            "excel_file": base64.b64encode(excel_data),
            "excel_filename": filename,
            "state": "done"
        })

        return {
            "type": "ir.actions.act_window",
            "res_model": "tax.report.wizard",
            "view_mode": "form",
            "res_id": self.id,
            "views": [(False, "form")],
            "target": "new",
        }
