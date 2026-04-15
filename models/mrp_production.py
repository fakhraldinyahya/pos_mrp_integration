from odoo import models, fields

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    pos_order_id = fields.Many2one(
        'pos.order', 'POS Order',
        readonly=True, copy=False)
    
    
    def action_view_pos_order(self):
        """
        Smart Button Action: Opens the associated POS Order.
        
        Returns:
            dict: The action dictionary to open the POS Order form view.
        """
        self.ensure_one()
        return {
            'name': "POS Order",
            'type': 'ir.actions.act_window',
            'res_model': 'pos.order',
            'view_mode': 'form',
            'res_id': self.pos_order_id.id,
            "target": 'current',
        }