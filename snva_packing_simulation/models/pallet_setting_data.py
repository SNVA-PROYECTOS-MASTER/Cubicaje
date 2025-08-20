from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SnvaPalletSettingData(models.Model):
    _name = 'snva.pallet.setting.data'
    _description = 'Pallet or stowage configuration'
    _rec_name = "snva_pallet_name"

    # Creamos los campos respectivos
    snva_pallet_name = fields.Char(string="Pallet Name", required=True, help="Descriptive name of the pallet or storage container.")
    snva_pallet_length = fields.Float(string="Pallet Length (m)", required=True, help="Total usable length of the pallet or container, in meters.")
    snva_pallet_width = fields.Float(string="Pallet Width (m)", required=True, help="Total usable width of the pallet or container, in meters.")
    snva_pallet_height = fields.Float(string="Pallet Height (m)", required=True, help="Total usable height of the pallet or container, in meters.")
    snva_pallet_weight = fields.Float(string="Pallet Weight (kg)", required=True, help="Maximum load capacity of the pallet or container, in kilograms.")
    snva_pallet_image = fields.Binary(string="Pallet Image", required=True)