# -*- coding: utf-8 -*-
from openprocurement.api.validation import validate_data
from openprocurement.api.utils import error_handler


def validate_patch_milestone_data(request, **kwargs):
    model = type(request.context)
    return validate_data(request, model)

def validate_allowed_contract_statuses(request, **kwargs):
    """Only one status change of particular contract is allowed
    """
    contract = request.contract
    new_status = request.validated['data'].get('status')
    if contract.status != 'active.confirmation' and new_status != 'active.payment':
        request.errors.add('body', 'status', 'Wrong status change')
        request.errors.status = 403
        raise error_handler(request)
