# -*- coding: utf-8 -*-
import os

from openprocurement.contracting.ceasefire.tests.base import (
    BaseWebTest
)
from openprocurement.contracting.ceasefire.tests.helpers import (
    get_contract,
    get_document,
    post_document,
)
from openprocurement.contracting.ceasefire.tests.fixtures.contract_fixtures import (
    create_contract,
)
from openprocurement.contracting.ceasefire.tests.fixtures.document_fixtures import (
    prepare_contract_with_document,
)
from openprocurement.contracting.core.constants import (
    ENDPOINTS as CORE_ENDPOINTS,
)


class CeasefireDocumentResourceTest(BaseWebTest):

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

    def test_get_ok(self):
        contract_id, document_id = prepare_contract_with_document(self)
        response = self.app.get(
            CORE_ENDPOINTS['documents'].format(
                contract_id=contract_id,
                document_id=document_id
            )
        )
        assert response.status == '200 OK'
