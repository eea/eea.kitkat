"""Captcha verify"""

import json
import logging
from contextlib import closing
from urllib.parse import urlencode
from six.moves import urllib
from plone import api
from plone.app.registry.browser import controlpanel
from Products.Five.browser import BrowserView
from zope import schema
from zope.interface import Interface
from eea.kitkat import EEAMessageFactory as _

logger = logging.getLogger("eea.kitkat")


class ICaptchaSettings(Interface):
    """Client settings for friendly captcha"""

    server = schema.TextLine(
        title=_("Captcha URL"),
        description=_("Captcha siteverify URL"),
        default="https://api.friendlycaptcha.com/api/v1/siteverify",
    )

    username = schema.TextLine(
        title=_("Captcha API KEY"), description=("Captcha API KEY"), default=""
    )

    password = schema.TextLine(
        title=_("Captcha API SECRET"), description=("Captcha API SECRET"), default=""
    )

    timeout = schema.Int(
        title=_("Timeout"), description=_("Request timeout"), default=15
    )


class ControlPanelForm(controlpanel.RegistryEditForm):
    """Friendly Captcha control panel"""

    id = "captcha"
    label = _("Captcha settings")
    schema = ICaptchaSettings


class ControlPanelView(controlpanel.ControlPanelFormWrapper):
    """Friendly Captcha Control Panel"""

    form = ControlPanelForm


class Captcha(BrowserView):
    """Friendly Captcha verify"""

    @property
    def password(self):
        """Captcha secret"""
        return api.portal.get_registry_record(
            "password", interface=ICaptchaSettings, default=""
        )

    @property
    def username(self):
        """Captcha key"""
        return api.portal.get_registry_record(
            "username", interface=ICaptchaSettings, default=""
        )

    @property
    def server(self):
        """Captcha serververify link"""
        return api.portal.get_registry_record(
            "server", interface=ICaptchaSettings, default=""
        )

    @property
    def timeout(self):
        """Timeout"""
        return api.portal.get_registry_record(
            "timeout", interface=ICaptchaSettings, default=15
        )

    def __call__(self):
        try:
            req = urllib.request.Request(
                self.server,
                headers={"Accept": "application/json"},
                data=urlencode(
                    {
                        "sitekey": self.username,
                        "secret": self.password,
                        "solution": self.request.get("solution"),
                    }
                ).encode("utf-8"),
            )
            with closing(urllib.request.urlopen(req, timeout=self.timeout)) as conn:
                return conn.read()
        except Exception as err:
            logger.exception(err)
            return json.dumps({"success": False, "errors": repr(err)})
