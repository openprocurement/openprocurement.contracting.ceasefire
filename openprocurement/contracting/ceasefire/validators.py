# -*- coding: utf-8 -*-
from openprocurement.api.validation import validate_data
from openprocurement.api.utils import error_handler
from openprocurement.contracting.ceasefire.predicates import (
    allowed_contract_status_changes,
)


def validate_patch_milestone_data(request, **kwargs):
    model = type(request.context)
    return validate_data(request, model)


def validate_allowed_contract_statuses(request, **kwargs):
    """Only one status change of particular contract is allowed
    """
    contract = request.contract
    new_status = request.validated['data'].get('status')

    if not allowed_contract_status_changes(contract.status, new_status, request.authenticated_userid):
        request.errors.add('body', 'status', 'Status change is not allowed.')
        request.errors.status = 403
        raise error_handler(request)
