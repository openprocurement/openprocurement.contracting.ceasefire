# -*- coding: utf-8 -*-
import iso8601

from datetime import datetime, date
from zope.interface import implementer

from openprocurement.api.utils import (
    error_handler,
    validate_with,
)
from openprocurement.api.utils import (
    calculate_business_date,
)
from openprocurement.contracting.core.utils import (
    LOGGER,
)
from openprocurement.contracting.core.interfaces import (
    IMilestoneManager,
)
from openprocurement.contracting.ceasefire.utils import (
    search_list_with_dicts,
    view_milestones_by_type,
)
from openprocurement.contracting.ceasefire.models import Milestone
from openprocurement.contracting.ceasefire.validators import (
    validate_document_is_present_on_milestone_status_change,
    validate_milestone_is_not_in_terminal_status,
)
from openprocurement.contracting.ceasefire.constants import (
    MILESTONE_APPROVAL_DUEDATE_OFFSET,
    MILESTONE_FINANCING_DUEDATE_OFFSET,
    MILESTONE_REPORTING_DUEDATE_OFFSET_YEARS,
    MILESTONE_TYPES,
)


@implementer(IMilestoneManager)
class CeasefireMilestoneManager(object):

    change_validators = (
        validate_document_is_present_on_milestone_status_change,
        validate_milestone_is_not_in_terminal_status,
    )

    def __init__(self, context):
        self.context = context

    def create_milestones(self, request):
        contract = request.validated['contract']
        contract.milestones = self.populate_milestones(contract)

    @validate_with(change_validators)
    def change_milestone(self, request):
        milestone = request.context
        new_status = request.json.get('data', {}).get('status')
        contract = milestone.__parent__

        # `notMet` handling
        if new_status == 'notMet' and milestone.status == 'processing':
            milestone.status = new_status
            milestone.__parent__.status = 'pending.unsuccessful'

        # handle patching `dueDate` of reporting milestone in `scheduled` status
        patched_dueDate = request.json.get('data', {}).get('dueDate')
        if (
            patched_dueDate and
            milestone.status == 'scheduled' and
            milestone.type_ == 'reporting'
        ):
            new_dueDate = iso8601.parse_date(patched_dueDate)
            self.validate_dueDate(request, new_dueDate)
            milestone.dueDate = new_dueDate

        # `dateMet` handling
        patched_date_met_str = request.validated['data'].get('dateMet')
        if patched_date_met_str:
            new_dateMet = iso8601.parse_date(patched_date_met_str)
            self.validate_dateMet(request, new_dateMet)
            self.choose_status(milestone, new_dateMet)
            milestone.dateMet = new_dateMet
            next_milestone = self.get_next_milestone(milestone)
            if next_milestone:
                next_milestone.status = 'processing'
                self.set_dueDate(next_milestone, contract)
                self.contract_status_based_on_milestones(contract)
            else:
                self.contract_status_based_on_milestones(contract)

    def set_dueDate(self, milestone, contract):
        """Sets dueDate of the Milestone

        Also takes into account milestone's type, so this method can be used on
        any milestone of Ceasefire contracting.

        :param milestone: milestone to work with
        :param contract: contract, related to milestone

        :type milestone: openprocurement.contracting.ceasefire.models.Milestone
        :type start_date: openprocurement.contracting.ceasefire.models.Contract

        :return: dueDate of milestone
        :rtype: datetime.datetime
        """
        if milestone.type_ == 'financing':
            milestone.dueDate = calculate_business_date(
                contract.dateSigned,
                MILESTONE_FINANCING_DUEDATE_OFFSET,
                context=contract,
                working_days=True,
                specific_hour=18)
        elif milestone.type_ == 'approval':
            financing_milestone = search_list_with_dicts(contract.milestones, 'type_', 'financing')
            milestone.dueDate = calculate_business_date(
                financing_milestone.dateMet,
                MILESTONE_APPROVAL_DUEDATE_OFFSET,
                context=contract,
                working_days=True,
                specific_hour=18)
        elif milestone.type_ == 'reporting' and milestone.dueDate is None:
            approval_milestone = search_list_with_dicts(contract.milestones, 'type_', 'approval')
            milestone.dueDate = datetime.combine(
                date(
                    approval_milestone.dateMet.year + MILESTONE_REPORTING_DUEDATE_OFFSET_YEARS,
                    approval_milestone.dateMet.month,
                    approval_milestone.dateMet.day
                ),
                approval_milestone.dateMet.time()
            )

    def populate_milestones(self, contract):
        """Create group of ceasefire milestones

        :param contract: contract, related to milestone
        :type contract: openprocurement.contracting.ceasefire.models.Contract
        """
        financing = Milestone({
            'type': 'financing',
            'status': 'processing',
        })
        approval = Milestone({
            'type': 'approval',
            'status': 'scheduled',
        })
        reporting = Milestone({
            'type': 'reporting',
            'status': 'scheduled',
        })
        self.set_dueDate(financing, contract)
        return [financing, approval, reporting]

    def choose_status(self, milestone, dateMet):
        if dateMet <= milestone.dueDate:
            milestone.status = 'met'
        elif dateMet > milestone.dueDate:
            milestone.status = 'partiallyMet'

    def get_next_milestone(self, milestone):
        current_milestone_type_index = MILESTONE_TYPES.index(milestone.type_)
        if current_milestone_type_index + 1 < len(MILESTONE_TYPES):
            next_milestone = search_list_with_dicts(
                milestone.__parent__.milestones,
                'type_',
                MILESTONE_TYPES[current_milestone_type_index + 1]
            )
            return next_milestone

    def get_previous_milestone(self, milestone):
        current_milestone_type_index = MILESTONE_TYPES.index(milestone.type_)
        if current_milestone_type_index > 0:
            previous_milestone = search_list_with_dicts(
                milestone.__parent__.milestones,
                'type_',
                MILESTONE_TYPES[current_milestone_type_index - 1]
            )
            return previous_milestone

    def contract_status_based_on_milestones(self, contract):
        """Sets status of related contract based on it's milestones statuses"""
        milestones = view_milestones_by_type(contract.milestones)
        statuses = (
            milestones['financing'].status,
            milestones['approval'].status,
            milestones['reporting'].status
        )
        contract_status = contract.status
        successful_statuses = ('met', 'partiallyMet')

        if 'notMet' in statuses:
            contract_status = 'pending.unsuccessful'

        if (
            statuses[0] in successful_statuses and
            statuses[1] == 'processing' and
            statuses[2] == 'scheduled'
        ):
            contract_status = 'active.approval'
        elif (
            statuses[0] in successful_statuses and
            statuses[1] in successful_statuses and
            statuses[2] == 'processing'
        ):
            contract_status = 'active'
        elif (
            statuses[0] in successful_statuses and
            statuses[1] in successful_statuses and
            statuses[2] in successful_statuses
        ):
            contract_status = 'pending.terminated'

        contract.status = contract_status
        LOGGER.info(
            "Evaluated and updated ceasefire contract status from it's milestones. Status: {0}, id: {1}".format(
                contract_status,
                contract.id
            )
        )

    def validate_dateMet(self, request, dateMet):
        previous_milestone = self.get_previous_milestone(request.context)
        if (
            (previous_milestone and (previous_milestone.dateMet >= dateMet)) or
            (request.context.__parent__.dateSigned >= dateMet)
        ):
            request.errors.add(
                'body',
                'dateMet',
                'dateMet must be greater than dateMet of previous milestone and dateSigned of related contract'
            )
            request.errors.status = 422
            raise error_handler(request)

    def validate_dueDate(self, request, dueDate):
        approval_milestone = search_list_with_dicts(request.context.__parent__.milestones, 'type_', 'approval')
        if approval_milestone.dueDate >= dueDate:
            request.errors.add(
                'body',
                'dueDate',
                'dueDate must be greater than dueDate of approval milestone'
            )
            request.errors.status = 422
            raise error_handler(request)
