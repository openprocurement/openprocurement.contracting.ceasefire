# -*- coding: utf-8 -*-
from logging import getLogger
from pkg_resources import get_distribution

from openprocurement.contracting.core.interfaces import (
    IContractManager,
    IMilestoneManager,
)
from openprocurement.contracting.ceasefire.adapters import (
    CeasefireContractManager,
    CeasefireMilestoneManager,
)
from openprocurement.contracting.ceasefire.models import (
    Contract,
    ICeasefireContract,
    ICeasefireMilestone,
)
from openprocurement.contracting.ceasefire.constants import (
    CONTRACT_DEFAULT_TYPE,
)




def includeme(config, plugin_config=None):
    PKG = get_distribution(__package__)
    LOGGER = getLogger(PKG.project_name)

    LOGGER.info('Init contracting.ceasefire plugin.')

    contract_types = plugin_config.get('aliases', [])
    if plugin_config.get('use_default', False):
        config.add_contract_contractType(Contract, CONTRACT_DEFAULT_TYPE)
    for ct in contract_types:
        config.add_contract_contractType(Contract, ct)

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
