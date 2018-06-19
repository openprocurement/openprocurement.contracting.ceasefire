# -*- coding: utf-8 -*-
from zope.interface import implementer

from openprocurement.auctions.core.utils import validate_with
from openprocurement.contracting.core.interfaces import (
    IDocumentManager,
)
from openprocurement.contracting.ceasefire.validators import (
    validate_allowed_contract_statuses,
)


@implementer(IDocumentManager)
class CeasefireContractDocumentManager(object):

    def __init__(self, context):
        self.context = context

    def create_document(self, request):
        document = request.validated['document']
        contract = request.context

        contract.documents.append(document)

    def change_document(self, request):
        pass
