"""Module where all interfaces, events and exceptions live."""

from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from eea.kitkat import EEAMessageFactory as _


class IEeaKitkatLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IEEAVersionsBackend(Interface):
    """ Registry record for the backend versions
    """
    date = schema.Datetime(
        title=_(u"Date of last version update"),
        description=(u"The date when the version was last updated"),
        required=True
    )

    version = schema.Text(
        title=_(u"Current version"),
        description=(u"The latest version that exists"),
        required=True
    )

    old_version = schema.Text(
        title=_(u"Previous version"),
        description=(u"The version that was previously"),
        required=False
    )


class IEEAVersionsFrontend(Interface):
    """ Registry record for the frontend versions
    """
    date = schema.Datetime(
        title=_(u"Date of last version update"),
        description=(u"The date when the version was last updated"),
        required=True
    )

    version = schema.Text(
        title=_(u"Current version"),
        description=(u"The latest version that exists"),
        required=True
    )

    old_version = schema.Text(
        title=_(u"Previous version"),
        description=(u"The version that was previously"),
        required=False
    )
