"""events module"""
import logging
import transaction
from datetime import datetime
from eea.kitkat.interfaces import IEEAVersionsFrontend
from plone.registry.interfaces import IRecordModifiedEvent
from zope.component import getUtility
from plone.registry.interfaces import IRegistry


logger = logging.getLogger("eea.kitkat")


def detectVersionChange(settings, event):
    if event.record.fieldName == 'version':
        registry = getUtility(IRegistry)

        registry[settings.__schema__['date'].__str__()] = datetime.now()
        registry[settings.__schema__['old_version'].__str__()] = event.oldValue

        transaction.get().note('eea.kitkat: updating FRONTEND_VERSION')
        transaction.commit()

        logger.info('Frontend version changed from %s to %s'
                    % (event.oldValue, event.newValue))
