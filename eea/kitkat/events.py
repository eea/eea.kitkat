# pylint: disable=W1201, C0301
"""events module"""
import logging
from datetime import datetime
import transaction
from plone.api.portal import set_registry_record


logger = logging.getLogger("eea.kitkat")


def detectVersionChange(settings, event):
    """ Frontend vers event subscriber that updates old_version & date record
    """
    if event.record.fieldName == 'version':
        set_registry_record('eea.kitkat.interfaces.IEEAVersionsFrontend.date', datetime.now())  # noqa
        set_registry_record('eea.kitkat.interfaces.IEEAVersionsFrontend.old_version', event.oldValue)  # noqa

        transaction.get().note("eea.kitkat: updating FRONTEND_VERSION")
        transaction.commit()

        logger.info("Frontend version changed from %s to %s"
                    % (event.oldValue, event.newValue))
