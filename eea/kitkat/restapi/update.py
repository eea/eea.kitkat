""" @system POST
"""
import json
import logging

import plone.protect.interfaces
from plone.registry.interfaces import IRegistry
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services import Service
from zope.component import getUtility
from zope.interface import alsoProvides

logger = logging.getLogger("eea.kitkat")
versionRecord = "eea.kitkat.interfaces.IEEAVersionsFrontend.version"


class SystemUpdate(Service):
    """ @system POST
    """
    def reply(self):
        """ Reply """
        records = json.loads(self.request.get("BODY", "{}"))

        # As we can't restrict this endpoint via permissions
        # Thus, restrict access only to internal API
        url = self.context.absolute_url()
        if not (url.startswith('http://localhost') or
                url.startswith('http://backend')):

            logger.warning("DENIED public API PATCH: %s/@system - %s",
                           url, records)
            return self.reply_no_content()

        registry = getUtility(IRegistry)

        if versionRecord not in registry:
            logger.warning("eea.kitkat not installed/upgraded: %s - %s",
                           url, records)
            return self.reply_no_content()

        # Disable CSRF protection
        if "IDisableCSRFProtection" in dir(plone.protect.interfaces):
            alsoProvides(
                self.request,
                plone.protect.interfaces.IDisableCSRFProtection
            )

        for key, value in records.items():
            if key != versionRecord:
                # Skip invalid requests
                continue

            if registry[key] == value:
                continue

            logger.warning("Updating %s - %s", key, value)
            registry[key] = value
            return json_compatible(value)

        return self.reply_no_content()
