# -*- coding: utf-8 -*-
import iso8601

from datetime import datetime, date
from zope.interface import implementer

from openprocurement.api.utils import (
    get_now,
)
from openprocurement.api.utils import (
    calculate_business_date,
    search_list_with_dicts,
)
from openprocurement.api.utils.data_engine import DataEngine
from openprocurement.api.exceptions import CorniceErrors
from openprocurement.contracting.core.utils import (
    LOGGER,
)
from openprocurement.contracting.core.interfaces import (
    IMilestoneManager,
)
from openprocurement.contracting.ceasefire.utils import (
    view_milestones_by_type,
)
from openprocurement.contracting.ceasefire.models import Milestone
from openprocurement.contracting.ceasefire.constants import (
    MILESTONE_APPROVAL_DUEDATE_OFFSET,
    MILESTONE_FINANCING_DUEDATE_OFFSET,
    MILESTONE_REPORTING_DUEDATE_OFFSET_YEARS,
    MILESTONE_TERMINAL_STATUSES,
    MILESTONE_TYPES,
    MILESTONE_TYPES_REQUIRE_DOCUMENT_TO_PATCH,
)


@implementer(IMilestoneManager)
class CeasefireMilestoneManager(object):

    data_engine_cls = DataEngine

    def __init__(self):
        self.de = self.data_engine_cls()

    def create_milestones(self, contract):
        contract.milestones = self.populate_milestones(contract)

    def change_milestone(self, event):
        milestone = event.ctx.low
        new_status = event.data.get('status')
        contract = event.ctx.high

        milestone_upd = self.de.apply_data_on_context(event)
        # validation 1
        new_status = event.data.get('status')
        new_dateMet = milestone_upd.get('dateMet')
        current_status = milestone.status
        current_dateMet = milestone.dateMet
        milestone_type = milestone.type_

        is_status_change = (new_status != current_status) or (new_dateMet != current_dateMet)
        milestone_requires_document = milestone_type in MILESTONE_TYPES_REQUIRE_DOCUMENT_TO_PATCH

        contract_documents = event.ctx.high.documents
        related_document = None
        for document in contract_documents:
            if (
                document.relatedItem == milestone.id
                and document.documentOf == 'milestone'
            ):
                related_document = document
                break

        if is_status_change and not related_document and milestone_requires_document:
            raise CorniceErrors(
                403,
                (
                    'body',
                    'status',
                    'Status change could not be completed. Add a document to this milestone'
                )
            )

        # validation 2
        if milestone.status in MILESTONE_TERMINAL_STATUSES:
            raise CorniceErrors(
                403,
                (
                    'body',
                    'status',
                    "Can\'t update milestone in current ({0}) status".format(milestone.status)
                )
            )
        # validation end

        # `notMet` handling
        if new_status == 'notMet' and milestone.status == 'processing':
            milestone.status = new_status
            milestone.__parent__.status = 'pending.unsuccessful'

        # handle patching `dueDate` of reporting milestone in `scheduled` status
        patched_dueDate = event.data.get('dueDate')
        if (
            patched_dueDate and
            milestone.status == 'scheduled' and
            milestone.type_ == 'reporting'
        ):
            new_dueDate = iso8601.parse_date(patched_dueDate)
            self.validate_dueDate(event.ctx.high, new_dueDate)
            milestone.dueDate = new_dueDate

        # `dateMet` handling
        patched_date_met_str = milestone_upd.get('dateMet')
        if patched_date_met_str:
            new_dateMet = milestone_upd.dateMet
            self.validate_dateMet(event.ctx.low, event.ctx.high, new_dateMet)
            self.choose_status(milestone, new_dateMet)
            milestone.dateMet = new_dateMet
            next_milestone = self.get_next_milestone(milestone)
            if next_milestone:
                next_milestone.status = 'processing'
                self.set_dueDate(next_milestone, contract)
                self.contract_status_based_on_milestones(contract)
            else:
                self.contract_status_based_on_milestones(contract)

        milestone.dateModified = get_now()
        self.de.update(event)
        return {'data': milestone.serialize()}

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
                working_days=False,
                specific_hour=18,
                result_is_working_day=True)
        elif milestone.type_ == 'approval':
            financing_milestone = search_list_with_dicts(contract.milestones, 'type_', 'financing')
            milestone.dueDate = calculate_business_date(
                financing_milestone.dateMet,
                MILESTONE_APPROVAL_DUEDATE_OFFSET,
                context=contract,
                working_days=False,
                specific_hour=18,
                result_is_working_day=True)
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

    def validate_dateMet(self, milestone, contract, dateMet):
        previous_milestone = self.get_previous_milestone(milestone)
        if (
            (previous_milestone and (previous_milestone.dateMet >= dateMet)) or
            (contract.dateSigned >= dateMet)
        ):
            raise CorniceErrors(
                422,
                (
                    'body',
                    'dateMet',
                    'dateMet must be greater than dateMet of previous milestone and dateSigned of related contract'
                )
            )

    def validate_dueDate(self, contract, dueDate):
        approval_milestone = search_list_with_dicts(contract.milestones, 'type_', 'approval')
        if approval_milestone.dueDate >= dueDate:
            raise CorniceErrors(
                422,
                (
                    'body',
                    'dueDate',
                    'dueDate must be greater than dueDate of approval milestone'
                )
            )
