from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    to_manufacture = fields.Boolean(
        string='Manufacturing',
        help=_("If checked, this product becomes manufacturable and selling it in Point of Sale will automatically trigger a Manufacturing Order.")
    )

    @api.constrains("available_in_pos", "to_manufacture","is_kits")
    def _check_exist_bom(self):
        """
        Prevent enabling POS availability for manufactured products
        without a valid manufacturing Bill of Materials.
        """
        for product in self:
            
            if product.available_in_pos and product.to_manufacture:
                valid_bom = any(
                    bom.bom_line_ids
                    for bom in product.bom_ids
                )
                if product.is_kits:
                    raise UserError(
                        _("You cannot enable availability in Point of Sale for this product unless it has a Bill of Materials with the option 'Manufacture this product' enabled")
                    )
                if not valid_bom:
                    raise UserError(
                        _("You cannot enable availability in Point of Sale for a manufactured product without a valid Bill of Materials")
                    )