# -*- coding: utf-8 -*-
from zope.interface import implementer

from openprocurement.contracting.core.interfaces import (
    IDocumentManager,
)


@implementer(IDocumentManager)
class CeasefireContractDocumentManager(object):

    def create_document(self, request):
        document = request.validated['document']
        contract = request.context

        contract.documents.append(document)

    def change_document(self, request):
        pass
