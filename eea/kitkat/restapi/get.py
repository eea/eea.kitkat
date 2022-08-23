""" Get @system info """
from plone.restapi.services.system.get import SystemGet as PloneSystemGet
import pkg_resources
from eea.kitkat.interfaces import IEEAVersionsFrontend
from eea.kitkat.interfaces import IEEAVersionsBackend
from plone.api.portal import get_registry_record
from plone.restapi.serializer.converters import json_compatible


class SystemGet(PloneSystemGet):
    def reply(self):
        res = super(SystemGet, self).reply()
        if 'eggs' not in res:
            res['eggs'] = {}
            for pkg in pkg_resources.working_set:
                res['eggs'][pkg.key] = pkg.version
        if 'frontend' not in res:
            res['frontend'] = {
                'version': get_registry_record(
                    'version', interface=IEEAVersionsFrontend),
                'old_version': get_registry_record(
                    'old_version', interface=IEEAVersionsFrontend),
                'date': get_registry_record(
                    'date', interface=IEEAVersionsFrontend),
            }
        if 'backend' not in res:
            res['backend'] = {
                'version': get_registry_record(
                    'version', interface=IEEAVersionsBackend),
                'old_version': get_registry_record(
                    'old_version', interface=IEEAVersionsBackend),
                'date': get_registry_record(
                    'date', interface=IEEAVersionsBackend),
            }
        return json_compatible(res)
