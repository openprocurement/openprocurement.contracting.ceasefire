# -*- coding: utf-8 -*-
from zope.interface import implementer

from openprocurement.api.utils import validate_with
from openprocurement.contracting.core.interfaces import (
    IContractManager,
)
from openprocurement.contracting.ceasefire.validators import (
    validate_allowed_contract_statuses,
)
from openprocurement.contracting.ceasefire.adapters.milestone_manager import (
    CeasefireMilestoneManager,
)
from openprocurement.contracting.ceasefire.adapters.document_manager import (
    CeasefireContractDocumentManager,
)


@implementer(IContractManager)
class CeasefireContractManager(object):

    def __init__(self, context):
        self.context = context
        self.document_manager = CeasefireContractDocumentManager

    def create_contract(self, request):
        pass

    change_validators = (
        validate_allowed_contract_statuses,
    )

    @validate_with(change_validators)
    def change_contract(self, request):
        new_status = request.validated['data'].get('status')
        if new_status == 'active.payment':
            milestone_manager = CeasefireMilestoneManager(request.context)
            milestone_manager.create_milestones(request)
