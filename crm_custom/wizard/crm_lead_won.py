# -*- coding: utf-8 -*-
from odoo import models, fields

class CrmLeadWon(models.TransientModel):
    _name = 'crm.lead.won'
    _description = 'Won Reasons Wizard'

    lead_id = fields.Many2one('crm.lead', string='Lead', required=True)
    won_reason_ids = fields.Many2many('crm.won.reason', string='Won Reasons', required=True)
    won_feedback = fields.Html('Won Feedback')

    def action_won_reason_apply(self):
        """ মার্ক as won and return the rainbow-man result from the lead model """
        self.ensure_one()
        self.lead_id.write({
            'won_reason_ids': [(6, 0, self.won_reason_ids.ids)],
        })
        # Execute finalizing success logic
        return self.lead_id._apply_won_success_logic()
