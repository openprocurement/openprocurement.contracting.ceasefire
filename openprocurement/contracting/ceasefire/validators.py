# -*- coding: utf-8 -*-
from openprocurement.api.utils import error_handler
from openprocurement.api.validation import validate_data
from openprocurement.contracting.ceasefire.predicates import (
    allowed_contract_status_changes,
)
from openprocurement.contracting.ceasefire.constants import (
    MILESTONE_TERMINAL_STATUSES,
    MILESTONE_TYPES_REQUIRE_DOCUMENT_TO_PATCH,
)
from openprocurement.contracting.ceasefire.utils import (
    search_list_with_dicts,
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
    milestone_type = request.context.type_

    is_status_change = (new_status != current_status) or (new_dateMet != current_dateMet)
    milestone_requires_document = milestone_type in MILESTONE_TYPES_REQUIRE_DOCUMENT_TO_PATCH

    contract_documents = request.context.__parent__.documents
    related_document = None
    for document in contract_documents:
        if (
            document.relatedItem == request.context.id
            and document.documentOf == 'milestone'
        ):
            related_document = document
            break

    if is_status_change and not related_document and milestone_requires_document:
        request.errors.add(
            'body',
            'status',
            'Status change could not be completed. Add a document to this milestone'
        )
        request.errors.status = 403
        raise error_handler(request)


def validate_milestone_is_not_in_terminal_status(request, **kwargs):
    milestone = request.context

    if milestone.status in MILESTONE_TERMINAL_STATUSES:
        request.errors.add(
            'body',
            'status',
            "Can\'t update milestone in current ({0}) status".format(milestone.status)
        )
        request.errors.status = 403
        raise error_handler(request)


def validate_document_upload_milestone_not_terminal_status(request, **kwargs):
    contract = request.context
    milestone_id = request.validated['document'].relatedItem

    # document could be uploaded to the contract, not a milestone
    contract_has_milestones = contract.milestones is not None
    if not contract_has_milestones:
        return

    milestone = search_list_with_dicts(contract.milestones, 'id', milestone_id)
    terminal_status = milestone.status in MILESTONE_TERMINAL_STATUSES

    if terminal_status:
        request.errors.add(
            'body',
            'status',
            "Can\'t attach document to milestone in current ({0}) status".format(milestone.status)
        )
        request.errors.status = 403
        raise error_handler(request)
