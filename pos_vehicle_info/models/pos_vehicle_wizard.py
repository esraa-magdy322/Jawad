# -*- coding: utf-8 -*-
from odoo import models, fields

class PosVehicleWizard(models.TransientModel):
    _name = 'pos.vehicle.wizard'
    _description = 'POS Vehicle Information Wizard'

    plate_number = fields.Char(string='رقم السيارة')
    car_type = fields.Char(string='نوع السيارة')
    car_model = fields.Integer(string='موديل السيارة')
    track = fields.Integer(string='الممشى')
    next_track = fields.Integer(string='الممشى القادم')
