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


def validate_document_is_present_on_milestone_status_change(request, **kwargs):
    new_status = request.json['data'].get('status')
    new_dateMet = request.validated['data'].get('dateMet')
    current_status = request.context.status
    current_dateMet = request.context.dateMet

    is_status_change = (new_status != current_status) or (new_dateMet != current_dateMet)

    contract_documents = request.context.__parent__.documents
    related_document = None
    for document in contract_documents:
        if (
            document.relatedItem == request.context.id
            and document.documentOf == 'milestone'
        ):
            related_document = document
            break

    if is_status_change and not related_document:
        request.errors.add(
            'body',
            'status',
            'Status change could not be completed. Add a document to this milestone'
        )
        request.errors.status = 403
        raise error_handler(request)
