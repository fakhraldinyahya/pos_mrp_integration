from odoo import models, fields

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    
    product_id = fields.Many2one(
        'product.product', 'Product',
        domain=[('type', '=', 'consu'),('to_manufacture','=',True)],
        compute='_compute_product_id', store=True, copy=True, precompute=True,
        readonly=False, required=True, check_company=True)