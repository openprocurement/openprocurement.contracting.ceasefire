# -*- coding: utf-8 -*-
from openprocurement.contracting.ceasefire.constants import (
    CONTRACT_ALLOW_TERMINAL_STATUS_SET_USERIDS,
    CONTRACT_PRE_TERMINAL_STATUSES,
    CONTRACT_TERMINAL_STATUSES,
)


def allowed_contract_status_changes_for_broker(current_status, new_status):
    return (
        current_status == 'active.confirmation'
        and (
            new_status == 'active.payment'
            or new_status == 'active.confirmation'
        )
    )


def allowed_contract_status_changes_for_bot(current_status, new_status, authenticated_userid):
    return (
        (authenticated_userid in CONTRACT_ALLOW_TERMINAL_STATUS_SET_USERIDS) and  # check bot's role
        (new_status in CONTRACT_TERMINAL_STATUSES) and  # allow bot to set only terminal statuses
        (current_status in CONTRACT_PRE_TERMINAL_STATUSES)  # prove that contract is in pre-terminated status
    )


def allowed_contract_status_changes(current_status, new_status, authenticated_userid):
    return (
        # forbid all those status changes, that must be done through milestones
        allowed_contract_status_changes_for_broker(current_status, new_status) or
        # allow bot to terminate contract
        allowed_contract_status_changes_for_bot(current_status, new_status, authenticated_userid)
    )
