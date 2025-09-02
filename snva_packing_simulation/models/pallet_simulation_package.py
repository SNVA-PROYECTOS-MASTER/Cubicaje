from odoo import models, fields, api, _
import random
import re



class SnvaPalletSimulationPackage(models.Model):
    _name = 'snva.pallet.simulation.packages'
    _description = 'Package for Simulation'

    
    snva_package_brand = fields.Char(string="Brand")
    # Creamos los campos relacionados
    snva_package_name = fields.Many2one('product.template', string="Select Product", required=True)
    snva_package_width = fields.Float(string="Width (cm)", required=True)
    snva_package_height = fields.Float(string="Height (cm)", required=True)
    snva_package_length = fields.Float(string="Length (cm)", required=True)
    snva_package_weight = fields.Float(string="Weight (kg)", required=True)
    snva_package_quantity = fields.Integer(string="Quantity", default=1, required=True)
    
    # Usa un método de modelo como default (Odoo le pasará 'self' sin romper)
    def _default_color(self):
        return self._rand_hex_color()
    # Color aleatorio por defecto; widget color en la vista ya está configurado
    snva_package_color = fields.Char(string="Color", default=_default_color, required=True)

    # Creamos el campo relacionado con el modelo donde quiero que aparezca
    snva_package_simulation_id = fields.Many2one('snva.pallet.simulation', string="Related Simulation")
    
    # --- Utilidades ---
    @api.model
    def _rand_hex_color(self):
        """#RRGGBB aleatorio."""
        return "#{:06X}".format(random.randint(0, 0xFFFFFF))

    @staticmethod
    def _sanitize_hex(color):
        """Normaliza texto a #RRGGBB o None."""
        if not color:
            return None
        color = str(color).strip()
        m = re.match(r'^#?([0-9A-Fa-f]{6})$', color)
        return f"#{m.group(1).upper()}" if m else None

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