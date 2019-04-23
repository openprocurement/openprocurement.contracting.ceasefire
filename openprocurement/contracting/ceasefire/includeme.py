# -*- coding: utf-8 -*-
from logging import getLogger
from pkg_resources import get_distribution
from openprocurement.contracting.core.interfaces import (
    IContractManager,
    IMilestoneManager,
)
from openprocurement.contracting.ceasefire.adapters.contract_manager import (
    CeasefireContractManager,
)
from openprocurement.contracting.ceasefire.adapters.milestone_manager import (
    CeasefireMilestoneManager,
)
from openprocurement.contracting.ceasefire.models import (
    Contract,
    ICeasefireContract,
    ICeasefireMilestone,
)
from openprocurement.contracting.ceasefire.constants import (
    CONTRACT_DEFAULT_TYPE,
    DEFAULT_LEVEL_OF_ACCREDITATION
)


def includeme(config, plugin_config=None):
    PKG = get_distribution(__package__)
    LOGGER = getLogger(PKG.project_name)

    LOGGER.info('Init contracting.ceasefire plugin.')

    contract_types = plugin_config.get('aliases', [])
    manager_registry = config.registry.manager_registry
    if plugin_config.get('use_default', False):
        config.add_contract_contractType(Contract, CONTRACT_DEFAULT_TYPE)
        manager_registry.register_manager(CONTRACT_DEFAULT_TYPE, CeasefireContractManager)
    for ct in contract_types:
        config.add_contract_contractType(Contract, ct)
        manager_registry.register_manager(ct, CeasefireContractManager)

    config.scan("openprocurement.contracting.ceasefire.views")
    config.registry.registerAdapter(
        CeasefireContractManager,
        (ICeasefireContract,),
        IContractManager
    )
    config.registry.registerAdapter(
        CeasefireMilestoneManager,
        (ICeasefireMilestone,),
        IMilestoneManager
    )
    if not plugin_config.get('accreditation'):
        config.registry.accreditation['contract'][Contract._internal_type] = DEFAULT_LEVEL_OF_ACCREDITATION
    else:
        config.registry.accreditation['contract'][Contract._internal_type] = plugin_config['accreditation']
