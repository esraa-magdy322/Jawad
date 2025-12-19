# -*- coding: utf-8 -*-
{
    "name": "POS Vehicle Information",
    "version": "1.0",
    "category": "Point of Sale",
    "summary": "Add vehicle information button in POS",
    "description": "Add a Vehicle button in POS interface",
    "author": "BDC Solutions",
    "depends": ["point_of_sale", "print_oil_drive", "custom_algwad_v17"],
    "data": [
        "security/ir.model.access.csv",
        "views/pos_vehicle_wizard.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_vehicle_info/static/src/js/models.js",
            "pos_vehicle_info/static/src/js/VehiclePopup.js",
            "pos_vehicle_info/static/src/js/vehicle_button.js",
            "pos_vehicle_info/static/src/js/PrintOilButton.js",
            "pos_vehicle_info/static/src/xml/VehiclePopup.xml",
            "pos_vehicle_info/static/src/xml/vehicle_button.xml",
            "pos_vehicle_info/static/src/xml/payment_screen_inherit.xml",
        ],
    },
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
