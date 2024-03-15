""" Get @system info """
from plone.api.portal import get_registry_record
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services import Service
from eea.kitkat.browser.captcha import ICaptchaSettings


class CaptchaKeyGet(Service):
    """ @captchakey endpoint
    """
    def reply(self):
        """ Reply """
        result = get_registry_record("username", interface=ICaptchaSettings)
        return json_compatible(result)
