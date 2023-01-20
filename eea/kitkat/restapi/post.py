# pylint: disable=C0301
""" Get @system info """
import logging
import plone.protect.interfaces

from plone.restapi.deserializer import json_body
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services import Service
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from eea.kitkat.browser.captcha import Captcha


logger = logging.getLogger("eea.kitkat")


@implementer(IPublishTraverse)
class CaptchaVerifyPost(Service):
    """Creates new aliases"""

    def reply(self):
        """ check if captcha solution is valid
        """
        data = json_body(self.request)

        #  Disable CSRF protection
        if "IDisableCSRFProtection" in dir(plone.protect.interfaces):
            alsoProvides(self.request, plone.protect.interfaces.IDisableCSRFProtection)  # noqa

        self.request.form = data
        captcha = Captcha(self.context, self.request)
        return json_compatible(captcha())
