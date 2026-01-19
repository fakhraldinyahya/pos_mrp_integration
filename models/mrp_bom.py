from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

from collections import defaultdict


class MrpBom(models.Model):
    
    _inherit = 'mrp.bom'
    

    product_tmpl_id = fields.Many2one(
        'product.template', 'Product',
        check_company=True, index=True,
        domain=[('type', '=', 'consu'),('to_manufacture','=',True)] , required=True)