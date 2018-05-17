# -*- coding: utf-8 -*-
from logging import getLogger
from pkg_resources import get_distribution




def includeme(config, plugin_config=None):
    PKG = get_distribution(__package__)
    LOGGER = getLogger(PKG.project_name)

    LOGGER.info('Init contracting.ceasefire plugin.')
    # config.add_contract_contractType(Contract)
    # config.scan("openprocurement.contracting.ceasefire.views")
