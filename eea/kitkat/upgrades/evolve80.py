"""Upgrade to version 8.0"""

import logging
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

logger = logging.getLogger("eea.kitkat")

kitkatBackendRecord = "eea.kitkat.interfaces.IEEAVersionsBackend"
kitkatFrontendRecord = "eea.kitkat.interfaces.IEEAVersionsFrontend"
newBackendRecord = "eea.api.controlpanel.interfaces.IEEAVersionsBackend"
newFrontendRecord = "eea.api.controlpanel.interfaces.IEEAVersionsFrontend"


def cleanup(*args, **kwargs):
    """Cleanup old records"""
    registry = getUtility(IRegistry)

    backend_date = registry.get(kitkatBackendRecord + ".date", None)
    registry[newBackendRecord + ".date"] = backend_date

    backend_old_version = registry.get(kitkatBackendRecord + ".old_version", None)
    registry[newBackendRecord + ".old_version"] = backend_old_version

    backend_version = registry.get(kitkatBackendRecord + ".version", None)
    registry[newBackendRecord + ".version"] = backend_version

    frontend_date = registry.get(kitkatFrontendRecord + ".date", None)
    registry[newFrontendRecord + ".date"] = frontend_date

    frontend_old_version = registry.get(kitkatFrontendRecord + ".old_version", None)
    registry[newFrontendRecord + ".old_version"] = frontend_old_version

    frontend_version = registry.get(kitkatFrontendRecord + ".version", None)
    registry[newFrontendRecord + ".version"] = frontend_version
