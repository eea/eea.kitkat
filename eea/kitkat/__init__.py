""" Main product initializer
"""
import os
import logging
import transaction
from datetime import datetime
import Zope2
from BTrees.OOBTree import OOBTree
from zope.component import queryAdapter
from zope.annotation.interfaces import IAnnotations
from zope.i18nmessageid.message import MessageFactory


logger = logging.getLogger("eea.design")
EEAMessageFactory = MessageFactory('eea')
EEANOTRANSLATIONMessageFactory = MessageFactory('eea.notranslation')


def initialize(context):
    """Initializer called when used as a Zope 2 product.
    """
    root = Zope2.app()
    sites = root.objectValues("Plone Site")
    version = os.environ.get("EEA_KGS_VERSION", "")
    if not version:
        return

    changed = False
    for site in sites:
        anno = queryAdapter(site, IAnnotations)
        if not anno:
            continue

        if not anno.get("EEA_KGS_VERSION", None):
            anno["EEA_KGS_VERSION"] = OOBTree()
            changed = True

        if not anno["EEA_KGS_VERSION"].get(version, None):
            anno["EEA_KGS_VERSION"][version] = datetime.now()
            changed = True

    if changed:
        transaction.get().note('eea.kitkat: updating EEA_KGS_VERSION')
        try:
            transaction.commit()
        except Exception as err:
            logger.warn("EEA_KGS_VERSION already updated elsewhere: %s", err)
            transaction.abort()
        else:
            logger.info("EEA_KGS_VERSION updated to: %s", version)
