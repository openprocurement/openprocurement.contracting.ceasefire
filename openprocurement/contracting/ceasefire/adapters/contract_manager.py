# -*- coding: utf-8 -*-
from zope.interface import implementer

from openprocurement.api.utils.data_engine import DataEngine
from openprocurement.api.utils.ownership import OwnershipOperator
from openprocurement.api.exceptions import CorniceErrors
from openprocurement.api.auth import is_accreditated
from openprocurement.contracting.core.interfaces import (
    IContractManager,
)
from openprocurement.contracting.ceasefire.adapters.milestone_manager import (
    CeasefireMilestoneManager,
)
from openprocurement.contracting.ceasefire.adapters.document_manager import (
    CeasefireContractDocumentManager,
)
from openprocurement.contracting.ceasefire.models.schema import Contract
from openprocurement.contracting.ceasefire.predicates import allowed_contract_status_changes


@implementer(IContractManager)
class CeasefireContractManager(object):

    _data_engine_cls = DataEngine
    milestone_manager = CeasefireMilestoneManager
    document_manager = CeasefireContractDocumentManager

    def __init__(self):
        self.de = DataEngine()
        self._create_accreditations = (5,)
        self._edit_accreditations = (6,)

    def create_contract(self, event):
        # validation
        if not is_accreditated(event.auth.accreditations, self._create_accreditations):
            raise CorniceErrors(
                403,
                (
                    'body',
                    'accreditation',
                    'Broker Accreditation level does not permit contract creation'
                )
            )
        # validation end
        contract = self.de.create_model(event, Contract)
        self._add_documents_to_contract(contract, event.data)

        ownersip_operator = OwnershipOperator(contract)
        acc = ownersip_operator.set_ownership(
            event.auth.user_id, event.data.get('transfer_token')
        )
        saved = self.de.save(event, contract)
        if saved:
            # TODO log it
            return {
                'access': acc,
                'data': contract.serialize('view')
            }

    def _add_documents_to_contract(self, contract, data):
        for i in data.get('documents', []):
            doc = type(contract).documents.model_class(i)
            doc.__parent__ = contract
            contract.documents.append(doc)

    def change_contract(self, event):
        # validation
        contract = event.ctx.high
        new_status = event.data.get('status', contract.status)
        user_id = event.auth.user_id
        if not allowed_contract_status_changes(contract.status, new_status, user_id):
            raise CorniceErrors(403, ('body', 'status', 'Status change is not allowed.'))
        # validation end
        contract_upd = self.de.apply_data_on_context(event)
        new_status = contract_upd.get('status')
        if new_status == 'active.payment':
            milestone_manager = self.milestone_manager()
            milestone_manager.create_milestones(contract)
        self.de.update(event)

        return {'data': event.ctx.high.serialize('view')}
