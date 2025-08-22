from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import json
import base64
from urllib.parse import quote

class SnvaPalletSimulation(models.Model):
    _name = 'snva.pallet.simulation'
    _description = 'Pallet Simulation'
    _rec_name = "snva_simulation_name"

    # Campos
    snva_simulation_name = fields.Char(string="Simulation Name", required=True)
    snva_simulation_pallet = fields.Many2one(
        'snva.pallet.setting.data',
        string="Select Pallet to Use",
        required=True,
        help="Choose the pallet configuration to use in this simulation."
    )

    # Related del pallet
    snva_simulation_pallet_width = fields.Float(
        related='snva_simulation_pallet.snva_pallet_width',
        string="Pallet Width (m)", readonly=True)
    snva_simulation_pallet_height = fields.Float(
        related='snva_simulation_pallet.snva_pallet_height',
        string="Pallet Height (m)", readonly=True)
    snva_simulation_pallet_length = fields.Float(
        related='snva_simulation_pallet.snva_pallet_length',
        string="Pallet Length (m)", readonly=True)
    snva_simulation_pallet_weight = fields.Float(
        related='snva_simulation_pallet.snva_pallet_weight',
        string="Pallet Weight (kg)", readonly=True)
    snva_simulation_pallet_image = fields.Binary(
        related='snva_simulation_pallet.snva_pallet_image',
        string="Pallet Image", readonly=True)

    # One2many de paquetes
    snva_simulation_package_ids = fields.One2many(
        'snva.pallet.simulation.packages',
        'snva_package_simulation_id',
        string="Packages"
    )

    def open_simulation_packing(self):
        '''
        Abre la URL con los parámetros para simular los datos
        '''
        self.ensure_one()

        # Validaciones
        if not self.snva_simulation_pallet:
            raise ValidationError(_("Please select a pallet before continuing."))

        if not self.snva_simulation_package_ids or len(self.snva_simulation_package_ids) == 0:
            raise ValidationError(_("Please select at least one product before continuing."))
        # Token de licencia desde la compañía
        licence_key = self.env.company.snva_packing_license_token
        if not licence_key:
            raise ValidationError(_("Please configure the Packing License Token in Settings."))

        # Objeto base (pallet en m/kg → JSON mm/g)
        result = {
            "palletName": self.snva_simulation_pallet.snva_pallet_name or "",
            "palletWidth": self.safe_div(self.snva_simulation_pallet_width, 1000),   # m → mm
            "palletHeight": self.safe_div(self.snva_simulation_pallet_height, 1000), # m → mm
            "palletLength": self.safe_div(self.snva_simulation_pallet_length, 1000), # m → mm
            # Peso máximo en KG (capacidad)
            "palletMaxWeight": self.snva_simulation_pallet_weight or 0.0,
            "packages": []
        }

        # Construcción de paquetes (v14: producto en cm / g → JSON: mm / g)
        for package in self.snva_simulation_package_ids:
            result["packages"].append({
                "productName": package.snva_package_name.name or "",
                "productWidth":  self.safe_div(package.snva_package_width,  10),  # cm → mm
                "productHeight": self.safe_div(package.snva_package_height, 10),  # cm → mm
                "productLength": self.safe_div(package.snva_package_length, 10),  # cm → mm
                "productWeight": package.snva_package_weight,                     # g (YA en gramos)
                "productQuantity": package.snva_package_quantity or 0,
                "productColor": package.snva_package_color or "#000000"
            })

        # JSON → base64 URL-safe
        json_str = json.dumps(result)
        json_bytes = json_str.encode("utf-8")
        encoded_data = base64.urlsafe_b64encode(json_bytes).decode("utf-8")

        # URL del visor (ajusta host/puerto según tu entorno)
        target_url = f"https://demo.sinova.co/packing/viewer?key={licence_key}&q={quote(encoded_data)}"

        # Acción
        return {
            "type": "ir.actions.act_url",
            "url": target_url,
            "target": "new",
        }

    def safe_div(self, value, divisor):
        '''
        Multiplicación protegida (nombre histórico).
        '''
        if not value:
            return 0.0
        return value * divisor
