""" Main product initializer
"""
import os
import logging
import transaction
from datetime import datetime
import Zope2
from BTrees.OOBTree import OOBTree
from zope.i18nmessageid.message import MessageFactory


logger = logging.getLogger("eea.kitkat")
EEAMessageFactory = MessageFactory('eea')

backend_record_name = "eea.kitkat.BACKEND_VERSION"
frontend_record_name = "eea.kitkat.FRONTEND_VERSION"


def initialize(context):
    """Initializer called when used as a Zope 2 product.
    """
    root = Zope2.app()
    sites = root.objectValues("Plone Site")
    version = os.environ.get(backend_record_name, "")
    # for testing purposes
    version = 2

    if not version:
        return

    changed = False
    for site in sites:
        if not hasattr(site, "portal_registry"):
            continue

        registry = site.portal_registry

        if not isinstance(version, str):
            version = str(version)

        if registry[backend_record_name].get('version', None) != version:
            date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
            entry = {'version': version, 'date': date}
            registry[backend_record_name] = entry
            changed = True

    if changed:
        transaction.get().note('eea.kitkat: updating BACKEND_VERSION')
        try:
            transaction.commit()
        except Exception as err:
            logger.warn("BACKEND_VERSION already updated elsewhere: %s", err)
            transaction.abort()
        else:
            logger.info("BACKEND_VERSION updated to: %s", version)
