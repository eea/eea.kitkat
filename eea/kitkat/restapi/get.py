""" Get @system info """
import pkg_resources
from plone.api.portal import get_registry_record
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services.system.get import SystemGet as PloneSystemGet

from eea.kitkat.interfaces import IEEAVersionsBackend, IEEAVersionsFrontend


class SystemGet(PloneSystemGet):
    """ @system endpoint
    """
    def eggs(self):
        """ Eggs """
        # pylint: disable=not-an-iterable
        for pkg in pkg_resources.working_set:
            yield (pkg.key, pkg.version)

    def frontend(self):
        """ Frontend info """
        return {
            "version": get_registry_record(
                "version", interface=IEEAVersionsFrontend),
            "old_version": get_registry_record(
                "old_version", interface=IEEAVersionsFrontend),
            "date": get_registry_record(
                "date", interface=IEEAVersionsFrontend),
        }

    def backend(self):
        """ Backend info """
        return {
            "version": get_registry_record(
                "version", interface=IEEAVersionsBackend),
            "old_version": get_registry_record(
                "old_version", interface=IEEAVersionsBackend),
            "date": get_registry_record(
                "date", interface=IEEAVersionsBackend),
        }

    def reply(self):
        """ Reply """
        res = super(SystemGet, self).reply()
        if "eggs" not in res:
            res["eggs"] = dict(self.eggs())
        if "frontend" not in res:
            res["frontend"] = self.frontend()
        if "backend" not in res:
            res["backend"] = self.backend()
        return json_compatible(res)
