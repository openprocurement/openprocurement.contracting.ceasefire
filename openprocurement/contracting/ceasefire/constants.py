# -*- coding: utf-8 -*-
from datetime import timedelta
# Endpoints
ENDPOINTS = {
    'contracts': '/contracts/{contract_id}',
    'contracts_collection': '/contracts',
    'milestones': '/contracts/{contract_id}/milestones/{milestone_id}',
    'milestones_collection': '/contracts/{contract_id}/milestones',
}
# Model constants
## Contract
CONTRACT_STATUSES = (  # ORDER MATTERS -- ПОРЯДОК СТАТУСІВ ВАЖЛИВИЙ
    'active.confirmation',
    'active.payment',
    'active.approval',
    'active',
    'terminated',
    'unsuccessful',
)
DEFAULT_CONTRACT_STATUS = 'active.confirmation'
CONTRACT_TYPE = 'ceasefire'
## Milestone
MILESTONE_TYPES = (  # ORDER MATTERS -- ПОРЯДОК ТИПІВ ВАЖЛИВИЙ
    'financing',
    'approval',
    'reporting',
)
MILESTONE_STATUSES = (
    'scheduled',
    'processing',
    'met',
    'partiallyMet',
    'notMet',
)
MILESTONE_FINANCING_DUEDATE_OFFSET = timedelta(days=60)
MILESTONE_APPROVAL_DUEDATE_OFFSET = timedelta(days=20)
MILESTONE_REPORTING_DUEDATE_OFFSET_YEARS = 3
