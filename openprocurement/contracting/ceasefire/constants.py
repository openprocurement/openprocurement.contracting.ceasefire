# -*- coding: utf-8 -*-
from datetime import timedelta
# Endpoints
ENDPOINTS = {
    'contracts': 'contracts/{contract_id}',
    'contracts_collection': 'contracts',
    'milestones': 'contracts/{contract_id}/milestones/{milestone_id}',
    'milestones_collection': 'contracts/{contract_id}/milestones',
    'transfers_collection': 'transfers',
    'contracts_documents': 'contracts/{contract_id}/documents/{document_id}',
    'contracts_documents_collection': 'contracts/{contract_id}/documents',
}
# Model constants
# Contract
CONTRACT_STATUSES = (
    'active.confirmation',
    'active.payment',
    'active.approval',
    'active',
    'pending.terminated',
    'pending.unsuccessful',
    'terminated',
    'unsuccessful',
)
CONTRACT_TERMINAL_STATUSES = (
    'terminated',
    'unsuccessful',
)
CONTRACT_PRE_TERMINAL_STATUSES = (
    'pending.terminated',
    'pending.unsuccessful',
)

# Roles, allowed to change contract status to terminal
CONTRACT_ALLOW_TERMINAL_STATUS_SET_USERIDS = (
    'caravan',
)
DEFAULT_CONTRACT_STATUS = 'active.confirmation'
CONTRACT_DEFAULT_TYPE = 'ceasefire'
# Milestone
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
MILESTONE_TYPES_REQUIRE_DOCUMENT_TO_PATCH = (
    'approval',
)
MILESTONE_TERMINAL_STATUSES = (
    'met',
    'patriallyMet',
    'notMet',
)

DEFAULT_LEVEL_OF_ACCREDITATION = {'create': [5],
                                  'edit': [6]}
