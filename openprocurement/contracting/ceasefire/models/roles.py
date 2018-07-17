# -*- coding: utf-8 -*-
from schematics.transforms import whitelist, blacklist
from openprocurement.contracting.core.models import (
    contract_create_role,
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
        whitelist(
            'contractType',
            'suppliers',
            'merchandisingObject',
        ),
    'view':
        whitelist(
            'awardID',
            'relatedProcessID'
            'suppliers',
            'changes',
            'contractID',
            'contractNumber',
            'contractType',
            'dateSigned',
            'description',
            'documents',
            'id',
            'items',
            'merchandisingObject',
            'milestones',
            'milestones',
            'procuringEntity',
            'status',
            'title',
            'type',
            'value',
            'owner',
        ),
    'edit_active.confirmation':
        contract_edit_role +
        blacklist('suppliers', 'milestones'),
    'edit_active.payment':
        contract_edit_role +
        blacklist('suppliers', 'milestones'),
    'edit_active.approval':
        contract_edit_role +
        blacklist('suppliers', 'milestones'),
    'edit_active':
        contract_edit_role +
        blacklist('suppliers', 'milestones'),
    'edit_pending.terminated':
        whitelist('status'),
    'edit_pending.unsuccessful':
        whitelist('status'),
    'edit_terminated':
        whitelist(),
    'edit_unsuccessful':
        whitelist(),
    'caravan':
        whitelist('status'),
}
