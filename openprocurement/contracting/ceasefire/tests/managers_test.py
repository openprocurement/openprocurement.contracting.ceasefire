# -*- coding: utf-8 -*-
import unittest

from datetime import datetime, timedelta, date
from mock import (
    MagicMock,
    Mock,
    patch,
)
from openprocurement.api.constants import (
    SANDBOX_MODE,
)
from openprocurement.api.utils import (
    calculate_business_date,
)
from openprocurement.contracting.core.utils import (
    get_milestone_by_type,
)
from openprocurement.contracting.ceasefire.adapters.contract_manager import (
    CeasefireContractManager,
)
from openprocurement.contracting.ceasefire.adapters.milestone_manager import (
    CeasefireMilestoneManager,
)
from openprocurement.contracting.ceasefire.constants import (
    MILESTONE_APPROVAL_DUEDATE_OFFSET,
    MILESTONE_FINANCING_DUEDATE_OFFSET,
    MILESTONE_REPORTING_DUEDATE_OFFSET_YEARS,
    MILESTONE_TYPES,
)
from openprocurement.contracting.ceasefire.tests.fixtures.helpers import (
    prepare_contract_with_milestones,
    prepare_contract,
)
from openprocurement.api.tests.fixtures.mocks import event_mock


class CeasefireContractManagerTest(unittest.TestCase):

    @patch('openprocurement.contracting.ceasefire.adapters.contract_manager.is_accreditated')
    def test_create_contract(self, is_accr_mock):
        is_accr_mock.return_value = True

        event = event_mock()
        del event.ctx.cache  # ctx on POST has no cache at all
        contract = prepare_contract()
        event.data = contract.serialize()

        manager = CeasefireContractManager()

        with patch.object(manager.de, 'save') as save_mock:
            save_mock.return_value = True
            manager.create_contract(event)

        self.assertEqual(contract.status, 'active.confirmation')


class CeasefireMilestoneManagerTest(unittest.TestCase):

    def test_create_milestones(self):
        event = event_mock()
        contract = prepare_contract()
        contract.dateSigned = datetime.now()
        event.ctx.high = contract
        manager = CeasefireMilestoneManager()

        manager.create_milestones(event.ctx.high)

        self.assertEqual(len(contract.milestones), 3, 'milestones were not created')

    def test_populate_milestones(self):
        contract = prepare_contract()
        manager = CeasefireMilestoneManager()

        contract.dateSigned = datetime.now()

        milestones = manager.populate_milestones(contract)

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
        contract = prepare_contract_with_milestones()
        manager = CeasefireMilestoneManager()

        milestone = contract.milestones[0]

        contract.dateSigned = datetime.now()
        target_dueDate = calculate_business_date(
            contract.dateSigned,
            MILESTONE_FINANCING_DUEDATE_OFFSET,
            context=None,
            working_days=False,
            specific_hour=18,
            result_is_working_day=True)
        manager.set_dueDate(milestone, contract)
        self.assertEqual(milestone.dueDate, target_dueDate, 'dueDate has been calculated incorrectly')

    def test_set_dueDate_approval(self):
        contract = prepare_contract_with_milestones()

        manager = CeasefireMilestoneManager()

        financing_milestone, approval_milestone = contract.milestones[:2]
        financing_milestone.dateMet = datetime.now()

        contract.dateSigned = datetime.now()
        target_dueDate = calculate_business_date(
            financing_milestone.dateMet,
            MILESTONE_APPROVAL_DUEDATE_OFFSET,
            context=None,
            working_days=False,
            specific_hour=18,
            result_is_working_day=True)
        manager.set_dueDate(approval_milestone, contract)
        self.assertEqual(approval_milestone.dueDate, target_dueDate, 'dueDate has been calculated incorrectly')

    def test_set_dueDate_reporting_auto(self):
        contract = prepare_contract_with_milestones()
        manager = CeasefireMilestoneManager()

        approval_milestone = contract.milestones[1]
        approval_milestone.dateMet = datetime.now()
        reporting_milestone = contract.milestones[2]
        contract.dateSigned = datetime.now()

        target_dueDate = datetime.combine(
            date(
                approval_milestone.dateMet.year + MILESTONE_REPORTING_DUEDATE_OFFSET_YEARS,
                approval_milestone.dateMet.month,
                approval_milestone.dateMet.day,
            ),
            approval_milestone.dateMet.time()
        )
        manager.set_dueDate(reporting_milestone, contract)
        self.assertEqual(reporting_milestone.dueDate, target_dueDate, 'dueDate has been calculated incorrectly')

    def test_set_dueDate_financing_with_accelerator(self):
        contract = prepare_contract_with_milestones()
        manager = CeasefireMilestoneManager()

        milestone = contract.milestones[0]

        if SANDBOX_MODE:
            contract.sandbox_parameters = 'quick, accelerator=1440'
        contract.dateSigned = datetime.now()

        target_dueDate = calculate_business_date(
            contract.dateSigned,
            MILESTONE_FINANCING_DUEDATE_OFFSET,
            context=contract,
            working_days=False,
            specific_hour=18,
            result_is_working_day=True)
        manager.set_dueDate(milestone, contract)
        self.assertEqual(milestone.dueDate, target_dueDate, 'dueDate has been calculated incorrectly')

    def test_change_milestone_to_not_met(self):
        manager = CeasefireMilestoneManager()
        event = event_mock()
        contract = prepare_contract_with_milestones()
        milestone = contract.milestones[0]

        event.ctx.high = contract
        event.ctx.low = milestone
        event.ctx.low.id = 'fee5c030352541b094dd93ad4e643ed9'

        doc_mock = Mock()
        doc_mock.documentOf = 'milestone'
        doc_mock.relatedItem = 'fee5c030352541b094dd93ad4e643ed9'
        contract.documents = [doc_mock]

        milestone.__parent__ = contract

        event.data = {'status': 'notMet'}

        with patch.object(manager.de, 'save') as save_mock:
            save_mock.return_value = True
            manager.change_milestone(event)

        self.assertEqual(milestone.status, 'notMet')
        self.assertEqual(contract.status, 'pending.unsuccessful')

    def test_choose_status_to_met(self):
        manager = CeasefireMilestoneManager()
        mocked_milestone = Mock()
        mocked_milestone.dueDate = datetime.now()
        # set `dateMet` before `dueDate` to acquire `met` status
        dateMet_to_set = mocked_milestone.dueDate - timedelta(days=5)
        manager.choose_status(mocked_milestone, dateMet_to_set)
        assert mocked_milestone.status == 'met', 'Milestone status was not choosed correctly'

    def test_choose_status_to_partially_met(self):
        manager = CeasefireMilestoneManager()
        mocked_milestone = Mock()
        mocked_milestone.dueDate = datetime.now()
        # set `dateMet` after `dueDate` to acquire `partiallyMet` status
        dateMet_to_set = mocked_milestone.dueDate + timedelta(days=2)
        manager.choose_status(mocked_milestone, dateMet_to_set)
        assert mocked_milestone.status == 'partiallyMet', 'Milestone status was not choosed correctly'


class SetContractStatusTest(unittest.TestCase):

    def setUp(self):
        self.manager = CeasefireMilestoneManager()
        self.contract = Mock()

        financing_milestone = MagicMock()
        financing_milestone.type_ = financing_milestone.__getitem__.return_value = 'financing'

        approval_milestone = MagicMock()
        approval_milestone.type_ = approval_milestone.__getitem__.return_value = 'approval'

        reporting_milestone = MagicMock()
        reporting_milestone.type_ = reporting_milestone.__getitem__.return_value = 'reporting'

        self.contract.milestones = [financing_milestone, approval_milestone, reporting_milestone]

    def test_set_by_parameters_table(self):
        statuses_table = (
            (('met', 'processing', 'scheduled'), 'active.approval'),
            (('partiallyMet', 'processing', 'scheduled'), 'active.approval'),
            (('met', 'met', 'processing'), 'active'),
            (('met', 'partiallyMet', 'processing'), 'active'),
            (('met', 'partiallyMet', 'met'), 'pending.terminated'),
            (('met', 'partiallyMet', 'notMet'), 'pending.unsuccessful'),
            (('notMet', 'partiallyMet', 'met'), 'pending.unsuccessful'),
        )
        for row in statuses_table:
            input_statuses = row[0]
            target_contract_status = row[1]

            # init milestone statuses
            for i, milestone in enumerate(self.contract.milestones):
                milestone.status = input_statuses[i]

            self.manager.contract_status_based_on_milestones(self.contract)
            assert self.contract.status == target_contract_status
