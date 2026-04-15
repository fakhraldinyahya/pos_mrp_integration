# -*- coding: utf-8 -*-
{
    'name': 'CRM Customization',
    'version': '1.0',
    'category': 'Sales/CRM',
    'summary': 'Customizes CRM Kanban, Form views and Multiple Lost/Won Reasons',
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'data/crm_reason_data.xml',
        'wizard/crm_lead_won_views.xml',
        'wizard/crm_lead_lost_views.xml',
        'views/crm_lead_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
