# -*- coding: utf-8 -*-
import os
import iso8601

from copy import deepcopy
from time import sleep
from datetime import timedelta

from openprocurement.api.tests.blanks.json_data import test_document_data
from openprocurement.api.tests.base import PrefixedRequestClass
from openprocurement.contracting.ceasefire.constants import ENDPOINTS
from openprocurement.contracting.ceasefire.tests import base
from openprocurement.contracting.ceasefire.tests.fixtures.data import contract_create_data
from openprocurement.contracting.ceasefire.utils import view_milestones_by_type


class CeasefireTest(base.BaseWebTest):

    mock_config = base.MOCK_CONFIG
    record_http = True
    docservice = True

    def setUp(self):
        self.relative_to = os.path.dirname(base.__file__)
        self.app.RequestClass = PrefixedRequestClass
        self.app.authorization = ('Basic', ('broker', ''))
        self.couchdb_server = self.app.app.registry.couchdb_server
        self.db = self.app.app.registry.db
        if self.docservice:
            self.setUpDS()
            self.app.app.registry.docservice_url = 'http://public.docs-sandbox.ea.openprocurement.org'

    def endpoint(self, name, acc_token=None):
        prefixed = '/' + ENDPOINTS[name]
        if acc_token:
            return prefixed + '?acc_token=' + acc_token
        return prefixed

    @staticmethod
    def get_dateMet(dueDate_str, partiallyMet=False):
        due_date = iso8601.parse_date(dueDate_str)
        days_to_add = 2 if partiallyMet else -2
        tdelta = timedelta(days=days_to_add)
        date_met = due_date + tdelta
        return date_met.isoformat()

    def update_milestones(self):
        response = self.app.get(
            self.endpoint('contracts').format(
                contract_id=self.contract_id
            )
        )
        self.assertEqual(response.status, '200 OK')
        milestones = response.json['data']['milestones']
        self.milestones = view_milestones_by_type(milestones, 'type')

    def test_docs_tutorial(self):

        out_dir = 'docs/source/tutorial/'

        with open(out_dir + 'contracts-listing-empty.http', 'w') as self.app.file_obj:
            response = self.app.get(self.endpoint('contracts_collection'))
            self.assertEqual(response.status, '200 OK')

        #  Create contract as a bot
        self.app.authorization = ('Basic', ('contracting', ''))
        response = self.app.post_json(
            self.endpoint('contracts_collection'),
            {'data': contract_create_data}
        )
        self.contract_id = response.json['data']['id']
        access = response.json['access']
        self.assertEqual(response.status, '201 Created')

        self.app.authorization = ('Basic', ('broker', ''))

        with open(out_dir + 'get-created-contract.http', 'w') as self.app.file_obj:
            response = self.app.get(
                self.endpoint('contracts').format(
                    contract_id=self.contract_id
                )
            )
            self.assertEqual(response.status, '200 OK')

        with open(out_dir + 'create-transfer.http', 'w') as self.app.file_obj:
            transfer = self.app.post_json('/transfers', {'data': {}}).json

        with open(out_dir + 'use-transfer.http', 'w') as self.app.file_obj:
            self.app.post_json(
                '/contracts/{0}/ownership'.format(self.contract_id),
                {'data': {
                    'id': transfer['data']['id'],
                    'transfer': access['transfer']
                }}
            )

        acc_token = transfer['access']['token']

        with open(out_dir + 'patch-contract-to-active-payment.http', 'w') as self.app.file_obj:
            response = self.app.patch_json(
                self.endpoint('contracts', acc_token).format(
                    contract_id=self.contract_id
                ),
                {'data': {'status': 'active.payment'}})

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~Milestones~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.update_milestones()

        self.app.get(self.endpoint('contracts_collection'))
        sleep(0.31415926)  # must use some delay to give DB time to build index

        with open(out_dir + 'view-contracts-after-create.http', 'w') as self.app.file_obj:
            response = self.app.get(self.endpoint('contracts_collection'))
            self.assertEqual(response.status, '200 OK')

        with open(out_dir + 'get-financing-milestone-processing.http', 'w') as self.app.file_obj:
            response = self.app.get(
                self.endpoint('milestones').format(
                    contract_id=self.contract_id,
                    milestone_id=self.milestones['financing']['id']))

        with open(out_dir + 'patch-financing-to-met.http', 'w') as self.app.file_obj:
            response = self.app.patch_json(
                self.endpoint('milestones', acc_token).format(
                    contract_id=self.contract_id,
                    milestone_id=self.milestones['financing']['id']
                ),
                {'data': {'dateMet': self.get_dateMet(self.milestones['financing']['dueDate'])}}
            )

        with open(out_dir + 'patch-financing-to-partially-met.http', 'w') as self.app.file_obj:
            response = self.app.patch_json(
                self.endpoint('milestones', acc_token).format(
                    contract_id=self.contract_id,
                    milestone_id=self.milestones['financing']['id']
                ),
                {'data': {'dateMet': self.get_dateMet(self.milestones['financing']['dueDate'], partiallyMet=True)}}
            )

        with open(out_dir + 'get-contract-after-financing-partiallyMet.http', 'w') as self.app.file_obj:
            response = self.app.get(
                self.endpoint('contracts').format(
                    contract_id=self.contract_id
                )
            )
            self.assertEqual(response.status, '200 OK')

        with open(out_dir + 'get-approval-milestone.http', 'w') as self.app.file_obj:
            response = self.app.get(
                self.endpoint('milestones').format(
                    contract_id=self.contract_id,
                    milestone_id=self.milestones['approval']['id']))

        self.update_milestones()
        target_reporting_due_date = iso8601.parse_date(self.milestones['approval']['dueDate']) + timedelta(days=1200)

        with open(out_dir + 'patch-reporting-due-date.http', 'w') as self.app.file_obj:
            response = self.app.patch_json(
                self.endpoint('milestones', acc_token).format(
                    contract_id=self.contract_id,
                    milestone_id=self.milestones['reporting']['id']
                ),
                {'data': {'dueDate': target_reporting_due_date.isoformat()}}
            )

        with open(out_dir + 'patch-approval-to-met.http', 'w') as self.app.file_obj:
            response = self.app.patch_json(
                self.endpoint('milestones', acc_token).format(
                    contract_id=self.contract_id,
                    milestone_id=self.milestones['approval']['id']
                ),
                {'data': {'dateMet': self.get_dateMet(self.milestones['approval']['dueDate'])}}
            )

        with open(out_dir + 'get-contract-after-approval-met.http', 'w') as self.app.file_obj:
            response = self.app.get(
                self.endpoint('contracts').format(
                    contract_id=self.contract_id
                )
            )
            self.assertEqual(response.status, '200 OK')

        with open(out_dir + 'get-reporting-processing.http', 'w') as self.app.file_obj:
            response = self.app.get(
                self.endpoint('milestones').format(
                    contract_id=self.contract_id,
                    milestone_id=self.milestones['reporting']['id']))

        self.update_milestones()

        with open(out_dir + 'patch-reporting-to-met.http', 'w') as self.app.file_obj:
            response = self.app.patch_json(
                self.endpoint('milestones', acc_token).format(
                    contract_id=self.contract_id,
                    milestone_id=self.milestones['reporting']['id']
                ),
                {'data': {'dateMet': self.get_dateMet(self.milestones['reporting']['dueDate'])}}
            )

        with open(out_dir + 'get-contract-after-reporting-met.http', 'w') as self.app.file_obj:
            response = self.app.get(
                self.endpoint('contracts').format(
                    contract_id=self.contract_id
                )
            )
            self.assertEqual(response.status, '200 OK')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~Document operations~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        document_data = deepcopy(test_document_data)
        document_data.update({
            'url': self.generate_docservice_url(),
            'documentOf': 'milestone',
            'relatedItem': self.milestones['financing']['id']
        })

        with open(out_dir + 'upload-document-to-milestone.http', 'w') as self.app.file_obj:
            response = self.app.post_json(
                self.endpoint('contracts_documents_collection', acc_token).format(
                    contract_id=self.contract_id,
                    milestone_id=self.milestones['financing']['id']
                ),
                {'data': document_data}
            )
            self.assertEqual(response.status, '201 Created')

        document_1_id = response.json['data']['id']

        with open(out_dir + 'get-contract-documents.http', 'w') as self.app.file_obj:
            response = self.app.get(
                self.endpoint('contracts_documents', acc_token).format(
                    contract_id=self.contract_id,
                    document_id=document_1_id
                )
            )
