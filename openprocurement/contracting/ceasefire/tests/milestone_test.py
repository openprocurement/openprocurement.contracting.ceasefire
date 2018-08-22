# -*- coding: utf-8 -*-
from uuid import uuid4
from datetime import timedelta
from webtest.app import AppError
from openprocurement.contracting.ceasefire.tests.base import (
    BaseWebTest
)
from openprocurement.contracting.ceasefire.constants import (
    ENDPOINTS,
)
from openprocurement.contracting.ceasefire.models import (
    Milestone,
)
from openprocurement.contracting.ceasefire.tests.fixtures.helpers import (
    create_contract,
    get_contract,
    get_milestone,
    patch_milestone,
    patch_milestone_document,
    post_milestone_document,
    prepare_milestones,
    prepare_milestones_approval,
    prepare_milestones_reporting,
)


class MilestoneResourceTest(BaseWebTest):

    docservice = True

    def setUp(self):
        super(MilestoneResourceTest, self).setUp()
        self.app.authorization = ('Basic', ('broker5', ''))

    def test_milestone_post(self):
        contract = create_contract(self)
        self.app.post_json(
            ENDPOINTS['milestones_collection'].format(
                contract_id=contract.data.id
            ),
            status=404
        )

    def test_milestone_get(self):
        contract, milestones = prepare_milestones(self)
        response = self.app.get(
            ENDPOINTS['milestones'].format(
                contract_id=contract.data.id,
                milestone_id=milestones[0]['id']
            )
        )
        assert response.status == '200 OK', 'Cannot get milestone'
        assert response.json['data']['status'] == 'processing', \
            'Financing milestone must be created with status `processing`'

    def test_milestone_patch_financing_dateMet(self):
        contract, milestones = prepare_milestones(self)
        financing_milestone = Milestone(milestones[0])
        assert financing_milestone.type_ == 'financing'
        dateMet_to_set = financing_milestone.dueDate - timedelta(days=5)

        response = patch_milestone(
            self,
            contract,
            financing_milestone.id,
            {'data': {'dateMet': dateMet_to_set.isoformat()}}
        )

        self.assertEqual(response.status, '200 OK')
        patched_financing_milestone = get_milestone(self, contract.data.id, financing_milestone.id)
        assert patched_financing_milestone.dateMet == dateMet_to_set, 'dateMet was not set'
        assert patched_financing_milestone.status == 'met', 'dateMet was not set'
        approval_milestone = get_milestone(self, contract.data.id, milestones[1]['id'])
        assert approval_milestone.status == 'processing'
        assert approval_milestone.dueDate is not None
        updated_contract = get_contract(self, contract.data.id)
        assert updated_contract.status == 'active.approval', 'Contract status was not updated'

    def test_milestone_patch_financing_dateMet_partially_met(self):
        contract, milestones = prepare_milestones(self)
        financing_milestone = Milestone(milestones[0])
        assert financing_milestone.type_ == 'financing'
        dateMet_to_set = financing_milestone.dueDate + timedelta(days=5)

        response = patch_milestone(
            self,
            contract,
            financing_milestone.id,
            {'data': {'dateMet': dateMet_to_set.isoformat()}}
        )

        self.assertEqual(response.status, '200 OK')
        patched_financing_milestone = get_milestone(self, contract.data.id, financing_milestone.id)
        assert patched_financing_milestone.dateMet == dateMet_to_set, 'dateMet was not set'
        assert patched_financing_milestone.status == 'partiallyMet', 'dateMet was not set'
        approval_milestone = get_milestone(self, contract.data.id, milestones[1]['id'])
        assert approval_milestone.status == 'processing'
        assert approval_milestone.dueDate is not None
        updated_contract = get_contract(self, contract.data.id)
        assert updated_contract.status == 'active.approval', 'Contract status was not updated'

    def test_milestone_patch_approval_dateMet(self):
        contract, milestones = prepare_milestones_approval(self)
        approval_milestone = Milestone(milestones[1])
        assert approval_milestone.type_ == 'approval'
        dateMet_to_set = approval_milestone.dueDate - timedelta(days=5)

        response = patch_milestone(
            self,
            contract,
            approval_milestone.id,
            {'data': {'dateMet': dateMet_to_set.isoformat()}}
        )

        self.assertEqual(response.status, '200 OK')
        patched_approval_milestone = get_milestone(self, contract.data.id, approval_milestone['id'])
        assert patched_approval_milestone.dateMet == dateMet_to_set, 'dateMet was not set'
        assert patched_approval_milestone.status == 'met'
        reporting_milestone = get_milestone(self, contract.data.id, milestones[2]['id'])
        assert reporting_milestone.status == 'processing', 'Reporting milestone status must be `processing`'
        assert reporting_milestone.dueDate is not None
        updated_contract = get_contract(self, contract.data.id)
        assert updated_contract.status == 'active', 'Contract status was not updated'

    def test_milestone_patch_approval_dateMet_partially_met(self):
        contract, milestones = prepare_milestones_approval(self)
        approval_milestone = Milestone(milestones[1])
        assert approval_milestone.type_ == 'approval'
        dateMet_to_set = approval_milestone.dueDate + timedelta(days=5)

        response = patch_milestone(
            self,
            contract,
            approval_milestone.id,
            {'data': {'dateMet': dateMet_to_set.isoformat()}}
        )

        self.assertEqual(response.status, '200 OK')
        patched_approval_milestone = get_milestone(self, contract.data.id, approval_milestone['id'])
        assert patched_approval_milestone.dateMet == dateMet_to_set, 'dateMet was not set'
        assert patched_approval_milestone.status == 'partiallyMet'
        reporting_milestone = get_milestone(self, contract.data.id, milestones[2]['id'])
        assert reporting_milestone.status == 'processing', 'Reporting milestone status must be `processing`'
        assert reporting_milestone.dueDate is not None
        updated_contract = get_contract(self, contract.data.id)
        assert updated_contract.status == 'active', 'Contract status was not updated'

    def test_milestone_patch_reporting_dateMet(self):
        contract, milestones = prepare_milestones_reporting(self)
        reporting_milestone = milestones[2]
        assert reporting_milestone.type_ == 'reporting'
        dateMet_to_set = reporting_milestone.dueDate - timedelta(days=5)

        response = patch_milestone(
            self,
            contract,
            reporting_milestone.id,
            {'data': {'dateMet': dateMet_to_set.isoformat()}}
        )

        self.assertEqual(response.status, '200 OK')
        patched_reporting_milestone = get_milestone(self, contract.data.id, reporting_milestone['id'])
        assert patched_reporting_milestone.dateMet == dateMet_to_set, 'dateMet was not set'
        assert patched_reporting_milestone.status == 'met'
        updated_contract = get_contract(self, contract.data.id)
        assert updated_contract.status == 'pending.terminated', 'Contract status was not updated'

    def test_milestone_patch_reporting_dateMet_partiallyMet(self):
        contract, milestones = prepare_milestones_reporting(self)
        reporting_milestone = milestones[2]
        assert reporting_milestone.type_ == 'reporting'
        dateMet_to_set = reporting_milestone.dueDate + timedelta(days=5)

        response = patch_milestone(
            self,
            contract,
            reporting_milestone.id,
            {'data': {'dateMet': dateMet_to_set.isoformat()}}
        )

        self.assertEqual(response.status, '200 OK')
        patched_reporting_milestone = get_milestone(self, contract.data.id, reporting_milestone['id'])
        assert patched_reporting_milestone.dateMet == dateMet_to_set, 'dateMet was not set'
        assert patched_reporting_milestone.status == 'partiallyMet'
        updated_contract = get_contract(self, contract.data.id)
        assert updated_contract.status == 'pending.terminated', 'Contract status was not updated'

    def test_milestone_patch_reporting_invalid_dateMet(self):
        contract, milestones = prepare_milestones_reporting(self)
        reporting_milestone = milestones[2]
        assert reporting_milestone.type_ == 'reporting'
        dateMet_to_set = reporting_milestone.dueDate - timedelta(days=10000)

        patch_milestone(
            self,
            contract,
            reporting_milestone.id,
            {'data': {'dateMet': dateMet_to_set.isoformat()}},
            status=422
        )

    def test_milestone_patch_financing_wrong_dateMet(self):
        contract, milestones = prepare_milestones(self)
        financing_milestone = Milestone(milestones[0])
        assert financing_milestone.type_ == 'financing'
        dateMet_to_set = financing_milestone.dueDate - timedelta(days=500)

        patch_milestone(
            self,
            contract,
            financing_milestone.id,
            {'data': {'dateMet': dateMet_to_set.isoformat()}},
            status=422
        )

    def test_patch_notMet(self):
        contract, milestones = prepare_milestones(self)
        financing_milestone = Milestone(milestones[0])
        assert financing_milestone.type_ == 'financing'

        response = patch_milestone(
            self,
            contract,
            financing_milestone.id,
            {'data': {'status': 'notMet'}},
        )

        self.assertEqual(response.status, '200 OK')
        related_contract = get_contract(self, contract.data.id)
        self.assertEqual(related_contract.status, 'pending.unsuccessful')

    def test_patch_status(self):
        contract, milestones = prepare_milestones_approval(self)
        reporting_milestone = Milestone(milestones[2])
        assert reporting_milestone.type_ == 'reporting'

        patch_milestone(
            self,
            contract,
            reporting_milestone.id,
            {'data': {'status': 'met'}},
        )
        patched_milestone = get_milestone(self, contract.data.id, reporting_milestone.id)
        self.assertEqual(patched_milestone.status, 'scheduled')

    def test_patch_description(self):
        contract, milestones = prepare_milestones_approval(self)
        reporting_milestone = Milestone(milestones[2])
        assert reporting_milestone.type_ == 'reporting'

        patch_milestone(
            self,
            contract,
            reporting_milestone.id,
            {'data': {'description': '937-99-92'}},
        )
        patched_milestone = get_milestone(self, contract.data.id, reporting_milestone.id)
        self.assertEqual(patched_milestone.description, '937-99-92')

    def test_milestone_patch_reporting_dueDate_when_scheduled(self):
        contract, milestones = prepare_milestones_approval(self)
        approval_milestone = milestones[1]
        assert approval_milestone.type_ == 'approval'
        reporting_milestone = milestones[2]
        dueDate_to_set = approval_milestone.dueDate + timedelta(days=500)

        response = patch_milestone(
            self,
            contract,
            reporting_milestone['id'],
            {'data': {'dueDate': dueDate_to_set.isoformat()}}
        )

        self.assertEqual(response.status, '200 OK')
        patched_reporting_milestone = get_milestone(self, contract.data.id, reporting_milestone['id'])
        assert patched_reporting_milestone.dueDate == dueDate_to_set, 'dueDate was not patched'

    def test_milestone_patch_dateMet_when_it_already_set(self):
        contract, milestones = prepare_milestones_approval(self)
        approval_milestone = milestones[1]
        assert approval_milestone.type_ == 'approval'
        reporting_milestone = milestones[2]
        dueDate_to_set = approval_milestone.dueDate + timedelta(days=500)
        approval_dateMet = approval_milestone.dueDate - timedelta(days=5)

        # patch dueDate
        response = patch_milestone(
            self,
            contract,
            reporting_milestone['id'],
            {'data': {'dueDate': dueDate_to_set.isoformat()}}
        )

        self.assertEqual(response.status, '200 OK')
        patched_reporting_milestone = get_milestone(self, contract.data.id, reporting_milestone['id'])
        assert patched_reporting_milestone.dueDate == dueDate_to_set, 'dueDate was not patched'

        response = patch_milestone(
            self,
            contract,
            approval_milestone['id'],
            {'data': {'dateMet': approval_dateMet.isoformat()}}
        )

        reporting_milestone = get_milestone(self, contract.data.id, reporting_milestone.id)
        assert reporting_milestone.dueDate == dueDate_to_set, 'dueDate must not be changed'

    def test_update_dateModified(self):
        contract, milestones = prepare_milestones_approval(self)
        reporting_milestone = Milestone(milestones[2])
        assert reporting_milestone.type_ == 'reporting'
        old_dateModified = reporting_milestone.dateModified

        patch_milestone(
            self,
            contract,
            reporting_milestone['id'],
            {'data': {'description': '937-99-92'}},
        )
        patched_milestone = get_milestone(self, contract.data.id, reporting_milestone.id)
        assert old_dateModified != patched_milestone.dateModified, 'dateModified must be updated'

    def test_update_dateModified_forbidden(self):
        contract, milestones = prepare_milestones_approval(self)
        reporting_milestone = Milestone(milestones[2])
        assert reporting_milestone.type_ == 'reporting'
        old_dateModified = reporting_milestone.dateModified

        patch_milestone(
            self,
            contract,
            reporting_milestone.id,
            {'data': {'type_': '937-99-92'}},
            status=422
        )
        patched_milestone = get_milestone(self, contract.data.id, reporting_milestone.id)
        assert old_dateModified == patched_milestone.dateModified, 'dateModified must not be updated'

    def test_patch_financing_milestone_without_document(self):
        contract, milestones = prepare_milestones(self, doc_preload=False)
        financing_milestone = Milestone(milestones[0])
        assert financing_milestone.type_ == 'financing'
        dateMet_to_set = financing_milestone.dueDate - timedelta(days=5)

        patch_milestone(
            self,
            contract,
            financing_milestone.id,
            {'data': {'dateMet': dateMet_to_set.isoformat()}},
            status=200
        )

    def test_patch_approval_milestone_without_document(self):
        contract, milestones = prepare_milestones_approval(self)
        approval_milestone = milestones[1]
        assert approval_milestone.type_ == 'approval'
        dateMet_to_set = approval_milestone.dueDate - timedelta(days=5)

        # all milestones have documents attached, so we need to unattach one from the approval milestone
        approval_milestone_document_id = None
        for document in contract.data.documents:
            if document.relatedItem == approval_milestone.id:
                approval_milestone_document_id = document.id

        patch_milestone_document(
            self,
            contract,
            approval_milestone.id,
            approval_milestone_document_id,
            {'data': {'relatedItem': milestones[0].id}}
        )

        # now milestone has no documents, so we are welcome to test
        patch_milestone(
            self,
            contract,
            approval_milestone.id,
            {'data': {'dateMet': dateMet_to_set.isoformat()}},
            status=403
        )

    def test_patch_not_met_to_met(self):
        contract, milestones = prepare_milestones(self)
        financing_milestone = Milestone(milestones[0])
        assert financing_milestone.type_ == 'financing'
        dateMet_to_set = financing_milestone.dueDate - timedelta(days=5)

        patch_milestone(
            self,
            contract,
            financing_milestone.id,
            {'data': {'status': 'notMet'}},
        )

        patch_milestone(
            self,
            contract,
            financing_milestone.id,
            {'data': {'dateMet': dateMet_to_set.isoformat()}},
            status=403
        )

    def test_patch_met_to_notMet(self):
        contract, milestones = prepare_milestones_approval(self)
        financing_milestone = Milestone(milestones[0])
        assert financing_milestone.type_ == 'financing'
        assert financing_milestone.status == 'met'
        patch_milestone(
            self,
            contract,
            financing_milestone.id,
            {'data': {'status': 'notMet'}},
            status=403
        )

    def test_upload_documents_with_milestone_related_types(self):
        contract, milestones = prepare_milestones_approval(self)
        reporting_milestone = Milestone(milestones[2])
        assert reporting_milestone.type_ == 'reporting'
        protocol_types = ('approvalProtocol', 'rejectionProtocol')

        for protocol_type in protocol_types:
            doc_id = post_milestone_document(
                self,
                contract,
                reporting_milestone.id,
                documentType=protocol_type
            ).json['data']['id']

            contract_after_post = get_contract(self, contract.data.id)

            found_doc = None
            for doc in contract_after_post.documents:
                if doc.id == doc_id:
                    found_doc = doc
            assert found_doc, 'document was not attached to the contract'
            assert found_doc.documentType == protocol_type

    def test_milestone_patch_attrs(self):
        contract, milestones = prepare_milestones(self)
        financing_milestone = Milestone(milestones[0])
        assert financing_milestone.type_ == 'financing'
        attrs = (
            'description_en',
            'description_ru',
            'title_en',
            'title_ru',
        )

        for attr in attrs:
            target_attr = uuid4().hex[:7]  # generate unique attr value
            patch_milestone(
                self,
                contract,
                financing_milestone.id,
                {'data': {attr: target_attr}}
            )

            patched_financing_milestone = get_milestone(self, contract.data.id, financing_milestone.id)
            assert getattr(patched_financing_milestone, attr) == target_attr

    def test_upload_document_in_terminal_status(self):
        contract, milestones = prepare_milestones_approval(self)
        financing_milestone = milestones[0]  # now it's in terminal status
        self.assertEqual(financing_milestone.type_, 'financing')
        self.assertEqual(financing_milestone.status, 'met')

        try:
            post_milestone_document(
                self,
                contract,
                financing_milestone.id,
            )
        except AppError:
            return  # we're looking for an exception
        self.fail('Document was uploaded in the milestone with terminal status')
