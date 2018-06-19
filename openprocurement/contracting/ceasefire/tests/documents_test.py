# -*- coding: utf-8 -*-
import os

from openprocurement.api.tests.base import (
    BaseResourceWebTest,
)
from openprocurement.contracting.ceasefire.tests.helpers import (
    get_contract,
    get_document,
    post_document,
)
from openprocurement.contracting.ceasefire.tests.fixtures.contract_fixtures import (
    create_contract,
)


class CeasefireDocumentResourceTest(BaseResourceWebTest):

    docservice = True
    relative_to = os.path.dirname(__file__)

    def test_post_ok(self):
        contract_id = create_contract(self)
        contract_before_document_post = get_contract(self, contract_id)
        assert contract_before_document_post.documents == []

        response = post_document(self, contract_id)
        assert response.status == '201 Created'

        contract_after_document_post = get_contract(self, contract_id)
        assert len(contract_after_document_post.documents) == 1
