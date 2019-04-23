# -*- coding: utf-8 -*-
from zope.interface import implementer

from openprocurement.api.utils.searchers import search_list_with_dicts
from openprocurement.contracting.core.interfaces import (
    IDocumentManager,
)
from openprocurement.api.exceptions import CorniceErrors
from openprocurement.contracting.ceasefire.validators import (
    validate_document_upload_contract_not_terminal_status,
    validate_document_upload_milestone_not_terminal_status,
)
from openprocurement.api.utils.data_engine import DataEngine
from openprocurement.contracting.ceasefire.constants import (
    CONTRACT_PRE_TERMINAL_STATUSES,
    CONTRACT_TERMINAL_STATUSES,
    MILESTONE_TERMINAL_STATUSES,
)


@implementer(IDocumentManager)
class CeasefireContractDocumentManager(object):

    data_engine_cls = DataEngine

    def __init__(self):
        self.de = DataEngine()

    create_validators = (
        validate_document_upload_contract_not_terminal_status,
        validate_document_upload_milestone_not_terminal_status,
    )

    # @validate_with(create_validators)
    def create_document(self, event):
        # validation
        self._validate_document_upload_milestone_not_terminal_status(event)
        self._validate_document_upload_contract_not_terminal_status(event)
        # validation end
        contract = event.ctx.high
        document = event.ctx.cache.document
        contract.documents.append(document)

        self.de.save(event)
        return {'data': document.serialize('view')}

    def change_document(self, event):
        self.de.apply_data_on_context(event)
        self.de.update(event)
        return {'data': event.ctx.low.serialize('view')}

    def put_document(self, event):
        document = event.ctx.cache.document
        contract = event.ctx.high

        contract.documents.append(document)

        self.de.save(event)
        return {'data': document.serialize('view')}

    def _validate_document_upload_milestone_not_terminal_status(self, event):
        # test_upload_document_in_terminal_status
        contract = event.ctx.high
        document_data = event.data

        document_of = document_data.get('documentOf')
        if not document_of == 'milestone':
            return

        milestone_id = document_data.get('relatedItem')

        # document could be uploaded to the contract, not a milestone
        contract_has_milestones = contract.milestones is not None
        if not contract_has_milestones:
            return

        milestone = search_list_with_dicts(contract.milestones, 'id', milestone_id)
        terminal_status = milestone.status in MILESTONE_TERMINAL_STATUSES

        if terminal_status:
            raise CorniceErrors(
                403,
                (
                    'body',
                    'status',
                    "Can\'t attach document to milestone in current ({0}) status".format(milestone.status)
                )
            )

    def _validate_document_upload_contract_not_terminal_status(self, event):
        contract = event.ctx.high
        document_data = event.data

        document_of = document_data.get('documentOf')
        if not document_of == 'contract':
            return

        forbidden_statuses = CONTRACT_TERMINAL_STATUSES + CONTRACT_PRE_TERMINAL_STATUSES

        if contract.status in forbidden_statuses:
            raise CorniceErrors(
                403,
                (
                    'body',
                    'status',
                    "Can\'t attach document to contract in current ({0}) status".format(contract.status)
                )
            )
