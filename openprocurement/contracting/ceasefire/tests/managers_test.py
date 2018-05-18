# -*- coding: utf-8 -*-
import unittest

from datetime import datetime, timedelta, date
from mock import (
    Mock,
)
from openprocurement.api.constants import (
    SANDBOX_MODE,
)
from openprocurement.auctions.core.utils import (
    calculate_business_date,
)
from openprocurement.contracting.core.utils import (
    get_milestone_by_type,
)
from openprocurement.contracting.ceasefire.adapters import (
    CeasefireContractManager,
    CeasefireMilestoneManager,
)
from openprocurement.contracting.ceasefire.models import (
    Contract,
)
from openprocurement.contracting.ceasefire.constants import (
    MILESTONE_APPROVAL_DUEDATE_OFFSET,
    MILESTONE_FINANCING_DUEDATE_OFFSET,
    MILESTONE_REPORTING_DUEDATE_OFFSET_YEARS,
    MILESTONE_TYPES,
)

from .fixtures.data import contract_create_data


class CeasefireContractManagerTest(unittest.TestCase):

    def setUp(self):
        self.contract = Contract(contract_create_data)
        self.contract.validate()
        self.mocked_request = Mock()
        self.mocked_request.validated = {'contract': self.contract}

    def test_create_contract(self):
        manager = CeasefireContractManager(Mock())

        manager.create_contract(self.mocked_request)

        self.assertEqual(self.contract.status, 'active.confirmation')


class CeasefireMilestoneManagerTest(unittest.TestCase):

    def prepare_mocked_contract(self):
        self.contract = Contract(contract_create_data)
        self.contract.validate()
        self.mocked_request = Mock()
        self.mocked_request.validated = {'contract': self.contract}

    def test_create_milestones(self):
        self.prepare_mocked_contract()
        manager = CeasefireMilestoneManager(Mock())
        self.contract.dateSigned = datetime.now()

        manager.create_milestones(self.mocked_request)

        self.assertEqual(len(self.contract.milestones), 3, 'milestones were not created')

    def test_populate_milestones(self):
        self.prepare_mocked_contract()
        manager = CeasefireMilestoneManager(Mock())

        self.contract.dateSigned = datetime.now()

        milestones = manager.populate_milestones(self.contract)

        self.assertEqual(len(milestones), 3, '3 milestones must be generated')
        generated_types = [milestone.type_ for milestone in milestones]
        self.assertEqual(
            set(MILESTONE_TYPES),
            set(generated_types),
            'types of generated milestones are wrong')

        financing_milestone = get_milestone_by_type(milestones, 'financing')
        self.assertNotEqual(
            financing_milestone.dueDate,
            None,
            'dueDate of financing milestone has not been generated')

    def test_set_dueDate_financing(self):
        self.prepare_mocked_contract()
        manager = CeasefireMilestoneManager(Mock())

        milestone_mock = Mock()
        milestone_mock.type_ = 'financing'

        self.contract.dateSigned = datetime.now()
        target_dueDate = calculate_business_date(
            self.contract.dateSigned,
            MILESTONE_FINANCING_DUEDATE_OFFSET,
            context=None,
            working_days=True,
            specific_hour=18)
        manager.set_dueDate(milestone_mock, self.contract)
        self.assertEqual(milestone_mock.dueDate, target_dueDate, 'dueDate has been calculated incorrectly')

    def test_set_dueDate_approval(self):
        self.prepare_mocked_contract()
        manager = CeasefireMilestoneManager(Mock())

        financing_milestone_mock = Mock()
        financing_milestone_mock.type_ = 'financing'
        financing_milestone_mock.get.return_value = 'financing'
        financing_milestone_mock.dateMet = datetime.now()
        approval_milestone_mock = Mock()
        approval_milestone_mock.type_ = 'approval'
        self.contract.milestones = (financing_milestone_mock, approval_milestone_mock)

        self.contract.dateSigned = datetime.now()
        target_dueDate = calculate_business_date(
            financing_milestone_mock.dateMet,
            MILESTONE_APPROVAL_DUEDATE_OFFSET,
            context=None,
            working_days=True,
            specific_hour=18)
        manager.set_dueDate(approval_milestone_mock, self.contract)
        self.assertEqual(approval_milestone_mock.dueDate, target_dueDate, 'dueDate has been calculated incorrectly')

    def test_set_dueDate_reporting_auto(self):
        self.prepare_mocked_contract()
        manager = CeasefireMilestoneManager(Mock())

        approval_milestone_mock = Mock()
        approval_milestone_mock.type_ = 'approval'
        approval_milestone_mock.get.return_value = 'approval'
        approval_milestone_mock.dateMet = datetime.now()
        reporting_milestone_mock = Mock()
        reporting_milestone_mock.type_ = 'reporting'
        reporting_milestone_mock.dueDate = None
        self.contract.milestones = (approval_milestone_mock, reporting_milestone_mock)
        self.contract.dateSigned = datetime.now()

        target_dueDate = datetime.combine(
            date(
                approval_milestone_mock.dateMet.year + MILESTONE_REPORTING_DUEDATE_OFFSET_YEARS,
                approval_milestone_mock.dateMet.month,
                approval_milestone_mock.dateMet.day,
            ),
            approval_milestone_mock.dateMet.time()
        )
        manager.set_dueDate(reporting_milestone_mock, self.contract)
        self.assertEqual(reporting_milestone_mock.dueDate, target_dueDate, 'dueDate has been calculated incorrectly')

    def test_set_dueDate_financing_with_accelerator(self):
        self.prepare_mocked_contract()
        manager = CeasefireMilestoneManager(Mock())

        milestone_mock = Mock()
        milestone_mock.type_ = 'financing'

        if SANDBOX_MODE:
            self.contract.sandbox_parameters = 'quick, accelerator=1440'
        self.contract.dateSigned = datetime.now()

        target_dueDate = calculate_business_date(
            self.contract.dateSigned,
            MILESTONE_FINANCING_DUEDATE_OFFSET,
            context=self.contract,
            working_days=True,
            specific_hour=18)
        manager.set_dueDate(milestone_mock, self.contract)
        self.assertEqual(milestone_mock.dueDate, target_dueDate, 'dueDate has been calculated incorrectly')

    def test_change_milestone_to_not_met(self):
        manager = CeasefireMilestoneManager(Mock())
        mocked_request = Mock()
        mocked_milestone = Mock()
        mocked_contract = Mock()
        mocked_milestone.__parent__ = mocked_contract
        mocked_milestone.status = 'processing'
        mocked_request.context = mocked_milestone
        mocked_request.validated = {'data': {}}
        mocked_request.json = {'data': {'status': 'notMet'}}

        manager.change_milestone(mocked_request)

        self.assertEqual(mocked_milestone.status, 'notMet')
        self.assertEqual(mocked_contract.status, 'unsuccessful')

    def test_choose_status_to_met(self):
        manager = CeasefireMilestoneManager(Mock())
        mocked_milestone = Mock()
        mocked_milestone.dueDate = datetime.now()
        # set `dateMet` before `dueDate` to acquire `met` status
        dateMet_to_set = mocked_milestone.dueDate - timedelta(days=5)
        manager.choose_status(mocked_milestone, dateMet_to_set)
        assert mocked_milestone.status == 'met', 'Milestone status was not choosed correctly'

    def test_choose_status_to_partially_met(self):
        manager = CeasefireMilestoneManager(Mock())
        mocked_milestone = Mock()
        mocked_milestone.dueDate = datetime.now()
        # set `dateMet` after `dueDate` to acquire `partiallyMet` status
        dateMet_to_set = mocked_milestone.dueDate + timedelta(days=2)
        manager.choose_status(mocked_milestone, dateMet_to_set)
        assert mocked_milestone.status == 'partiallyMet', 'Milestone status was not choosed correctly'
