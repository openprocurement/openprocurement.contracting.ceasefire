import time
import unittest

from copy import copy

from schematics.exceptions import ModelConversionError
from openprocurement.api.constants import (
    SANDBOX_MODE,
)
from openprocurement.api.utils import (
    calculate_business_date,
)
from openprocurement.contracting.ceasefire.tests.base import (
    BaseWebTest
)
from openprocurement.contracting.ceasefire.constants import (
    ENDPOINTS,
    DEFAULT_CONTRACT_STATUS,
    MILESTONE_FINANCING_DUEDATE_OFFSET
)
from .fixtures.data import contract_create_data
from .fixtures.contract_fixtures import (
    create_contract,
)
from openprocurement.contracting.ceasefire.models import (
    Contract,
)
from openprocurement.contracting.ceasefire.tests.constants import (
    CONTRACT_FIELDS_TO_HIDE,
)


class ContractResourceTest(BaseWebTest):

    def setUp(self):
        super(ContractResourceTest, self).setUp()
        self.app.authorization = ('Basic', ('broker5', ''))

    def check_forbidden_contract_fields(self, fields):
        for response_field in fields:
            if response_field in CONTRACT_FIELDS_TO_HIDE:
                self.fail(
                    'Unexpectedly found {0} field in PATCH response of Ceasefire contract'.format(
                        response_field
                    )
                )

    def test_contract_post_by_contracting(self):
        self.app.authorization = ('Basic', ('contracting', ''))
        response = self.app.post_json(
            ENDPOINTS['contracts_collection'],
            {
                'data': contract_create_data,
            }
        )
        response_data = response.json['data']
        self.assertEqual(response.status, '201 Created', 'Contract not created')
        self.assertEqual(response_data['awardID'], contract_create_data['awardID'])
        self.assertEqual(response_data['status'], DEFAULT_CONTRACT_STATUS)

    def test_contract_post_by_broker(self):
        response = self.app.post_json(
            ENDPOINTS['contracts_collection'],
            {
                'data': contract_create_data,
            }
        )
        self.assertEqual(response.status, '201 Created', 'Contract not created')

    def test_set_sandbox_parameters(self):
        contract_data = copy(contract_create_data)
        contract_data['sandbox_parameters'] = 'some_params'
        if SANDBOX_MODE:
            response = self.app.post_json(
                ENDPOINTS['contracts_collection'],
                {
                    'data': contract_data,
                }
            )
            self.assertEqual(response.status, '201 Created', 'Contract not created')
            contract_data = response.json['data']
            self.assertEqual(contract_data.get('sandbox_parameters'), 'some_params')
        else:
            response = self.app.post_json(
                ENDPOINTS['contracts_collection'],
                {
                    'data': contract_data,
                },
                status=422
            )

    def test_get_contract(self):
        contract_id = create_contract(self)
        self.app.authorization = ('Basic', ('broker1', ''))
        response = self.app.get(
            ENDPOINTS['contracts'].format(
                contract_id=contract_id))
        assert response.status == '200 OK'
        assert '_internal_type' not in response.json['data'].keys()

    def test_get_contracts(self):
        # This test relies on delayed indexation after 1st GET request to the DB,
        # so if it falls - try to increase sleep time.
        # P.S. I didn't use docstring to not override nosetest's output with it
        self.app.authorization = ('Basic', ('contracting', ''))
        contract_id_1 = create_contract(self)
        contract_id_2 = create_contract(self)
        self.app.get(ENDPOINTS['contracts_collection'])
        time.sleep(0.05)  # wait for delayed indexation of listing, seconds
        response = self.app.get(ENDPOINTS['contracts_collection'])
        keys_returned = [result['id'] for result in response.json['data']]
        assert contract_id_1 in keys_returned
        assert contract_id_2 in keys_returned

    def test_patch_contract_status_active_payment(self):
        contract_id = create_contract(self)
        contract = Contract(contract_create_data)
        response = self.app.patch_json(
            ENDPOINTS['contracts'].format(contract_id=contract_id),
            {'data': {'status': 'active.payment'}},
        )
        self.assertEqual(response.status, '200 OK')
        response_data = response.json['data']
        self.assertEqual(response_data['status'], 'active.payment')
        self.assertTrue(
            isinstance(response_data.get('milestones'), list),
            "Milestones weren't created"
        )
        financial_milestone = response_data['milestones'][0]
        target_dueDate = calculate_business_date(
            contract.dateSigned,
            MILESTONE_FINANCING_DUEDATE_OFFSET,
            context=None,
            working_days=True,
            specific_hour=18
        )
        self.assertEqual(
            financial_milestone['dueDate'],
            target_dueDate.isoformat(),
            "dueDate of financial milestone wasn't calculated right"
        )

    def test_patch_response_have_not_excessive_fields(self):
        contract_id = create_contract(self)
        response = self.app.patch_json(
            ENDPOINTS['contracts'].format(contract_id=contract_id),
            {'data': {'status': 'active.payment'}},
        )
        self.assertEqual(response.status, '200 OK')
        response_data_keys = response.json['data'].keys()
        self.check_forbidden_contract_fields(response_data_keys)

    def test_patch_contract_forbidden_status(self):
        contract_id = create_contract(self)
        # set allowed status
        self.app.patch_json(
            ENDPOINTS['contracts'].format(contract_id=contract_id),
            {'data': {'status': 'active.payment'}},
        )
        self.app.patch_json(
            ENDPOINTS['contracts'].format(contract_id=contract_id),
            {'data': {'status': 'active.approval'}},
            status=403
        )

    def test_create_contract_with_insufficient_acceditation(self):
        self.app.authorization = ('Basic', ('broker2', ''))
        self.app.post_json(
            ENDPOINTS['contracts_collection'],
            {
                'data': contract_create_data,
            },
            status=403
        )

    def test_create_contract_with_all_accreditations(self):
        self.app.authorization = ('Basic', ('broker', ''))
        response = self.app.post_json(
            ENDPOINTS['contracts_collection'],
            {
                'data': contract_create_data,
            },
        )
        assert response.status == '201 Created'

    def test_post_internal_type(self):
        self.app.authorization = ('Basic', ('contracting', ''))
        contract_data = copy(contract_create_data)
        contract_data.update({'_internal_type': '42'})
        response = self.app.post_json(
            ENDPOINTS['contracts_collection'],
            {
                'data': contract_data,
            },
            status=422
        )
        self.assertEqual(response.status, '422 Unprocessable Entity')

    def test_patch_internal_type(self):
        contract_id = create_contract(self)
        # set allowed status
        response = self.app.patch_json(
            ENDPOINTS['contracts'].format(contract_id=contract_id),
            {'data': {'_internal_type': 'lucy_lu'}},
            status=422
        )
        self.assertEqual(response.status, '422 Unprocessable Entity')


class ContractSandboxParametersTest(unittest.TestCase):
    """Test Ceasefire Contract model sandbox_parameters attribute

    Contract model with `sandbox_parameters` attibute present cannot be tested with
    this testcase simultaneously, because SANDBOX_MODE constant from
    `openprocurement.api.constants` will be initialized before tests execution.
    So, particular test must have two Act & Assert blocks with shared Arrange.
    """

    def test_create_contract_with_sandbox_parameters_without_sanbox_var(self):
        contract_data = copy(contract_create_data)
        contract_data['sandbox_parameters'] = 'details'
        if SANDBOX_MODE:
            contract = Contract(contract_data)
            self.assertEqual(contract.sandbox_parameters, 'details')
        else:
            with self.assertRaises(ModelConversionError):
                Contract(contract_data)
