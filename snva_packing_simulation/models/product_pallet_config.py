from odoo import models, fields, api, _
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SnvaProductPalletConfig(models.Model):
    _name = 'snva.product.pallet.config'
    _description = 'Default Pallet Configuration per Company'
    _rec_name = 'snva_product_ref_name'

    snva_product_ref_name = fields.Char(
        string="Name",
        required=True,
        default=lambda self: "%s - Default Mapping" % (self.env.company.name or "Company")
    )

    snva_product_ref_width = fields.Selection(
        selection=lambda self: self._get_product_field_selection_sudo(),
        string="Width related field",
        required=True
    )
    snva_product_ref_height = fields.Selection(
        selection=lambda self: self._get_product_field_selection_sudo(),
        string="Height related field",
        required=True
    )
    snva_product_ref_length = fields.Selection(
        selection=lambda self: self._get_product_field_selection_sudo(),
        string="Length related field",
        required=True
    )
    snva_product_ref_weight = fields.Selection(
        selection=lambda self: self._get_product_field_selection_sudo(),
        string="Weight related field",
        required=True
    )

    snva_product_ref_company_id = fields.Many2one(
        comodel_name='res.company',
        string="Company",
        required=True,
        default=lambda self: self.env.company,
        ondelete='cascade',
    )

    _sql_constraints = [
        ('snva_company_unique',
        'unique(snva_product_ref_company_id)',
        'Ya existe una configuración de pallet para esta compañía.')
    ]

    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         missing_fields = [
    #             f for f in ['snva_product_ref_width', 'snva_product_ref_height',
    #                         'snva_product_ref_length', 'snva_product_ref_weight']
    #             if not vals.get(f)
    #         ]
    #         if missing_fields:
    #             raise ValidationError(_("Missing required fields: %s") % ", ".join(missing_fields))
    #     return super().create(vals_list)

    @api.model
    def _get_product_field_selection_sudo(self):
        model = self.env['ir.model'].sudo().search([('model', '=', 'product.template')], limit=1)
        fields_obj = self.env['ir.model.fields'].sudo().search([
            ('model_id', '=', model.id),
            ('ttype', 'in', ['float', 'integer']),
        ])
        return [(f.name, f.field_description or f.name) for f in fields_obj]


class ResCompany(models.Model):
    _inherit = 'res.company'

    snva_group_pallet_product_ref_ids = fields.One2many(
        string="Grouped block of fields",
        comodel_name="snva.product.pallet.config",
        inverse_name="snva_product_ref_company_id",
    )

    snva_packing_license_token = fields.Char(
        string="Packing License Token",
        help="Token de licencia usado por el visor de Packing."
    )
