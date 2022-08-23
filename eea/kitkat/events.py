# pylint: disable=W1201, C0301
"""events module"""
import logging
from datetime import datetime
import transaction
from plone.api.portal import set_registry_record
from eea.kitkat.interfaces import IEEAVersionsFrontend


logger = logging.getLogger("eea.kitkat")


def detectVersionChange(settings, event):
    """ Frontend vers event subscriber that updates old_version & date record
    """
    if event.record.fieldName == 'version':
        set_registry_record(
            'date', datetime.now(), interface=IEEAVersionsFrontend)
        if event.oldValue:
            set_registry_record(
                'old_version', event.oldValue, interface=IEEAVersionsFrontend)

        transaction.get().note("eea.kitkat: updating FRONTEND_VERSION")
        transaction.commit()

        logger.info(
            "Frontend version changed from %s to %s",
            event.oldValue, event.newValue
        )
