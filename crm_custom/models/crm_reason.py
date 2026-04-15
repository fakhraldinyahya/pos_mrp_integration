# -*- coding: utf-8 -*-
from odoo import models, fields

class CrmWonReason(models.Model):
    _name = 'crm.won.reason'
    _description = 'Won Reason'
    _order = 'name'

    name = fields.Char('Won Reason', required=True, translate=True)

class CrmChurnReason(models.Model):
    _name = 'crm.churn.reason'
    _description = 'Non-Renewal Reason'
    _order = 'name'

    name = fields.Char('Non-Renewal Reason', required=True, translate=True)
