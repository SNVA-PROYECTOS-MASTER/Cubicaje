from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # O2M related a compañía (editable). OJO: O2M en Ajustes es frágil, pero dejamos tu enfoque.
    snva_pallet_product_config_ids = fields.One2many(
        string="Grouped block of fields",
        related="company_id.snva_group_pallet_product_ref_ids",
        readonly=False
    )

    snva_packing_license_token = fields.Char(
        string="Packing License Token",
        related="company_id.snva_packing_license_token",
        readonly=False
    )
