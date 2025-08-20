from odoo import models, fields, api, _

class SnvaPalletSimulationPackage(models.Model):
    _name = 'snva.pallet.simulation.packages'
    _description = 'Package for Simulation'

    # Creamos los campos relacionados
    snva_package_name = fields.Many2one('product.template', string="Select Product", required=True)
    snva_package_width = fields.Float(string="Width (cm)", required=True)
    snva_package_height = fields.Float(string="Height (cm)", required=True)
    snva_package_length = fields.Float(string="Length (cm)", required=True)
    snva_package_weight = fields.Float(string="Weight (kg)", required=True)
    snva_package_quantity = fields.Integer(string="Quantity", default=1, required=True)
    snva_package_color = fields.Char(string="Color", default="#000000", required=True)

    # Creamos el campo relacionado con el modelo donde quiero que aparezca
    snva_package_simulation_id = fields.Many2one('snva.pallet.simulation', string="Related Simulation")

    @api.onchange('snva_package_name')
    def _onchange_snva_package_name(self):
        """Auto-fill dimensions from company-specific configuration."""
        if not self.snva_package_name:
            return

        # Obtenemos la configuración actial
        company = self.env.company
        config = self.env['snva.product.pallet.config'].search([
            ('snva_product_ref_company_id', '=', company.id)
        ], limit=1)

        # Se valida si existe referencia asociada al campo actual
        if config:
            product = self.snva_package_name

            # Leer campos desde la configuración
            width_field = config.snva_product_ref_width
            height_field = config.snva_product_ref_height
            length_field = config.snva_product_ref_length
            weight_field = config.snva_product_ref_weight

            # Asignamos los valores actuales
            self.snva_package_width = getattr(product, width_field, 0.0)
            self.snva_package_height = getattr(product, height_field, 0.0)
            self.snva_package_length = getattr(product, length_field, 0.0)
            self.snva_package_weight = getattr(product, weight_field, 0.0)