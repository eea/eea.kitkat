""" Main product initializer
"""
import os
import logging
from datetime import datetime
import transaction
import Zope2
from zope.i18nmessageid.message import MessageFactory


logger = logging.getLogger("eea.kitkat")
EEAMessageFactory = MessageFactory('eea')

version_record = "eea.kitkat.interfaces.IEEAVersionsBackend.version"
old_version_record = "eea.kitkat.interfaces.IEEAVersionsBackend.old_version"
date_record = "eea.kitkat.interfaces.IEEAVersionsBackend.date"
version_env = "BACKEND_VERSION"


def initialize(context):
    """Initializer called when used as a Zope 2 product.
    """
    root = Zope2.app()
    sites = root.objectValues("Plone Site")
    version = os.environ.get(version_env, "")

    if not version:
        return

    changed = False
    for site in sites:
        if not hasattr(site, "portal_registry"):
            continue

        registry = site.portal_registry

        if version_record not in registry:
            continue

        if not isinstance(version, str):
            version = str(version)

        if registry[version_record] != version:
            registry[old_version_record] = registry[version_record]
            registry[version_record] = version
            registry[date_record] = datetime.now()
            changed = True

    if changed:
        transaction.get().note('eea.kitkat: updating BACKEND_VERSION')
        try:
            transaction.commit()
        except Exception as err:
            logger.warning(
                "BACKEND_VERSION already updated elsewhere: %s", err)
            transaction.abort()
        else:
            logger.info("BACKEND_VERSION updated to: %s", version)
