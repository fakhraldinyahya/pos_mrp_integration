from odoo import models, _, api
from odoo.exceptions import ValidationError

class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.constrains('lines')
    def _check_mrp_product_bom(self):
        """
        Constraint to ensure that all products configured to be manufactured
        have a valid Bill of Materials available.
        """
        for order in self:
            # Collect products that need manufacturing
            mrp_products = order.lines.mapped('product_id').filtered('to_manufacture')
            
            if not mrp_products:
                continue

            # Batch search for BoMs
            # _bom_find returns a dict: {product: bom}
            boms_by_product = self.env['mrp.bom']._bom_find(mrp_products, company_id=order.company_id.id)

            for product in mrp_products:
                if not boms_by_product.get(product):
                    raise ValidationError(_(
                        "Cannot validate POS Order %s.\n"
                        "Product '%s' is set to manufacture but has no active Bill of Materials."
                    ) % (order.name, product.display_name))
