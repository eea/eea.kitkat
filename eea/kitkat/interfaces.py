"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IEeaKitkatLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IEEAVersionsBackend(Interface):
    """Old Registry record for the backend versions"""


class IEEAVersionsFrontend(Interface):
    """Old Registry record for the frontend versions"""


__all__ = [
    "IEeaKitkatLayer",
    "IEEAVersionsBackend",
    "IEEAVersionsFrontend",
]
