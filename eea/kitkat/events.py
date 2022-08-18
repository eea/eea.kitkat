"""events module"""
import logging
from datetime import datetime
import transaction
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


logger = logging.getLogger("eea.kitkat")


def detectVersionChange(settings, event):
    """ Frontend vers event subscriber that updates old_version & date record
    """
    if event.record.fieldName == 'version':
        registry = getUtility(IRegistry)

        registry[settings.__schema__['date'].__str__()] = datetime.now()
        registry[settings.__schema__['old_version'].__str__()] = event.oldValue

        transaction.get().note("eea.kitkat: updating FRONTEND_VERSION")
        transaction.commit()

        logger.info("Frontend version changed from %s to %s"
                    % (event.oldValue, event.newValue))
