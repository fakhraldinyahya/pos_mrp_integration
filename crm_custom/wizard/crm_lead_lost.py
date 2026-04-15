# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CrmLeadLost(models.TransientModel):
    _inherit = 'crm.lead.lost'

    lost_reason_ids = fields.Many2many(
        'crm.lost.reason', 
        string='Lost Reasons'
    )

    churn_reason_ids = fields.Many2many(
        'crm.churn.reason', 
        string='Non-Renewal Reasons'
    )

    is_renewal = fields.Boolean(compute='_compute_is_renewal')

    @api.depends('lead_ids')
    def _compute_is_renewal(self):
        for wizard in self:
            wizard.is_renewal = any(lead.opportunity_type == 'renewal' for lead in wizard.lead_ids)

    def action_lost_reason_apply(self):
        """ Override to pass multiple reasons or churn reasons """
        self.ensure_one()
        vals = {
            'lost_reason_ids': [(6, 0, self.lost_reason_ids.ids)],
            'churn_reason_ids': [(6, 0, self.churn_reason_ids.ids)],
        }
        res = self.lead_ids.action_set_lost(**vals)
        return res
