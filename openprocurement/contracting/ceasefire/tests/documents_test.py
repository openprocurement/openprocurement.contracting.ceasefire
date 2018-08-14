# -*- coding: utf-8 -*-
import os

from openprocurement.contracting.ceasefire.tests.base import (
    BaseWebTest
)
from openprocurement.contracting.ceasefire.tests.fixtures.helpers import (
    create_contract,
    get_contract,
    get_document,
    post_document,
    prepare_contract_with_document,
)
from openprocurement.contracting.core.constants import (
    ENDPOINTS as CORE_ENDPOINTS,
)


class CeasefireDocumentResourceTest(BaseWebTest):

    docservice = True
    relative_to = os.path.dirname(__file__)

    def setUp(self):
        super(CeasefireDocumentResourceTest, self).setUp()
        self.app.authorization = ('Basic', ('broker5', ''))

    def test_post_ok(self):
        contract = create_contract(self)
        contract_id = contract.data.id
        contract_before_document_post = get_contract(self, contract_id)
        assert contract_before_document_post.documents == []

        response = post_document(self, contract)
        assert response.status == '201 Created'

        contract_after_document_post = get_contract(self, contract_id)
        assert len(contract_after_document_post.documents) == 1

    def test_get_ok(self):
        contract, document = prepare_contract_with_document(self)
        response = self.app.get(
            CORE_ENDPOINTS['documents'].format(
                contract_id=contract.data.id,
                document_id=document.data.id
            )
        )
        assert response.status == '200 OK'

    def test_patch_ok(self):
        target_tile = 'trololo'

        contract, document = prepare_contract_with_document(self)
        contract_id = contract.data.id
        document_id = document.data.id

        title_before_patch = get_document(self, contract_id, document_id).title
        response = self.app.patch_json(
            CORE_ENDPOINTS['documents'].format(
                contract_id=contract_id,
                document_id=document_id
            ) + "?acc_token={}".format(contract.access.token),
            {'data': {'title': target_tile}}
        )
        title_after_patch = response.json['data']['title']
        assert response.status == '200 OK'
        assert title_before_patch != target_tile
        assert title_after_patch == target_tile

    def test_patch_forbidden_field(self):
        new_id = 'abcd' * 8

        contract, document = prepare_contract_with_document(self)
        contract_id = contract.data.id
        document_id = document.data.id
        pre_patch_document_id = get_document(self, contract_id, document_id).id
        self.app.patch_json(
            CORE_ENDPOINTS['documents'].format(
                contract_id=contract_id,
                document_id=document_id
            ) + "?acc_token={}".format(contract.access.token),
            {'data': {'id': new_id}}
        )
        document_id = get_document(self, contract_id, document_id).id
        assert document_id != new_id
        assert document_id == pre_patch_document_id, 'id must remain unchanged'

    def test_post_with_wrong_user(self):
        contract = create_contract(self)
        self.app.authorization = ('Basic', ('petro', ''))

        post_document(self, contract, status_code=403)

    def test_patch_with_wrong_user(self):
        contract, document = prepare_contract_with_document(self)
        self.app.authorization = ('Basic', ('petro', ''))

        self.app.patch_json(
            CORE_ENDPOINTS['documents'].format(
                contract_id=contract.data.id,
                document_id=document.data.id
            ),
            {'data': {'title': 'lalal'}},
            status=403
        )
