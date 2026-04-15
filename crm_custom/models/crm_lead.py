# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    lost_reason_ids = fields.Many2many(
        'crm.lost.reason', 
        'crm_lead_lost_reason_rel', 
        'lead_id', 
        'tag_id', 
        string='Lost Reasons',
        help="Multiple selection for reasons why this opportunity was lost."
    )

    won_reason_ids = fields.Many2many(
        'crm.won.reason', 
        string='Won Reasons',
        help="Success factors for winning this opportunity."
    )

    churn_reason_ids = fields.Many2many(
        'crm.churn.reason', 
        string='Non-Renewal Reasons',
        help="Reasons why a renewal opportunity did not move forward (Churn)."
    )

    opportunity_type = fields.Selection([
        ('new', 'New Business'), 
        ('renewal', 'Renewal')
    ], string='Opportunity Type', default='new', required=True, 
       help="Categorize the deal as a first-time sale or a contract renewal.")

    def action_set_lost(self, **additional_values):
        """
        Overrides the standard loss action to support multi-reason tracking.
        Maps the first selected reason to the standard many2one field for report compatibility.
        """
        if 'lost_reason_ids' in additional_values:
            lost_reasons = additional_values.get('lost_reason_ids')
            # Extract ID from Many2many command (6, 0, [ids])
            if lost_reasons and lost_reasons[0][0] == 6:
                ids = lost_reasons[0][2]
                if ids:
                    additional_values['lost_reason_id'] = ids[0]
        
        return super(CrmLead, self).action_set_lost(**additional_values)

    @api.onchange('lost_reason_ids')
    def _onchange_lost_reason_ids(self):
        """Dynamic sync for UI consistency during editing."""
        if self.lost_reason_ids:
            self.lost_reason_id = self.lost_reason_ids[0]
        else:
            self.lost_reason_id = False

    def action_set_won_rainbowman(self):
        """
        Intercepts the 'Won' button to launch the verification wizard.
        The wizard will eventually call _action_set_won_success.
        """
        self.ensure_one()
        return {
            'name': 'Mark as Won',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'crm.lead.won',
            'target': 'new',
            'context': {'default_lead_id': self.id}
        }

    def _apply_won_success_logic(self):
        """
        Finalizes the Won status. 
        Separate method to decouple the logic from the wizard. 
        """
        self.ensure_one()
        won_stage = self._stage_find(domain=[('is_won', '=', True)], limit=1)
        self.write({
            'stage_id': won_stage.id, 
            'probability': 100,
            'active': True # Ensure it's not archived if it was somehow
        })
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Won! Congratulations',
                'type': 'rainbow_man',
            }
        }
