# -*- coding: utf-8 -*-
from schematics.transforms import whitelist, blacklist
from openprocurement.contracting.core.models import (
    contract_create_role,
    contract_view_role,
    contract_edit_role,
)


MILESTONE_ROLES = {
    'create':
        blacklist(
            'dateMet',
            'dateModified',
            'dueDate',
            'id',
            'status',
            'type_',
        ),
    'edit':
        blacklist(
            'dateModified',
            'dueDate',
            'id',
            'status',
            'type_',
        ),
}

CONTRACT_ROLES = {
    'create':
        contract_create_role +
        whitelist('contractType', 'buyers') +
        blacklist('milestones'),
    'view':
        contract_view_role +
        whitelist('contractType', 'milestones'),
    'edit_active.confirmation':
        contract_edit_role +
        blacklist('buyers', 'milestones'),
    'edit_active.payment':
        contract_edit_role +
        blacklist('buyers', 'milestones'),
    'edit_active.approval':
        contract_edit_role +
        blacklist('buyers', 'milestones'),
    'edit_active':
        contract_edit_role +
        blacklist('buyers', 'milestones'),
    'edit_terminated':
        whitelist(),
    'edit_unsuccessful':
        whitelist(),
}
