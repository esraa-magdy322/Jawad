{
    'name': 'Print Oil Change Label',
    'version': '17.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Print oil change reminder labels for invoices',
    'description': """
        Print Oil Change Label
        ======================
        This module adds a button to print oil change reminder labels (8x4 cm)
        for automotive service invoices.

        Features:
        - Print label with current odometer reading
        - Calculate and display next oil change mileage
        - QR code generation for tracking
        - Oil Drive branding
    """,
    'author': 'BDC Solutions',
    'depends': ['account', 'custom_algwad_v17'],
    'data': [
        'report/oil_label_report.xml',
        'report/oil_label_template_v2.xml',
        'views/account_move_view.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'print_oil_drive/static/src/css/oil_label.css',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
