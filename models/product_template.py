from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    mrp_from_pos = fields.Boolean(
        string='Manufacturing from POS',
        help=_("If checked, this product becomes manufacturable and selling it in Point of Sale will automatically trigger a Manufacturing Order.")
    )

    @api.constrains("mrp_from_pos", "is_kits","bom_ids")
    def _check_exist_bom(self):
        """
        Ensure that products which require manufacturing from POS (mrp_from_pos)
        must have a valid Bill of Materials (BoM).
        """
        for product in self.filtered('mrp_from_pos'):
            if product.is_kits:
                raise UserError(
                    _("You cannot enable manufacturing from POS for this product unless it has a Bill of Materials with the option 'Manufacture this product' enabled.")
                )

            if not product.bom_ids:
                raise UserError(
                    _("A manufactured product requiring POS integration must have a valid Bill of Materials (BoM) configured.")
                )
                
    