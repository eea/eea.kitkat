from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import adapter
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.interface import Interface
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class EEAVersionsGet(Service):
    def __init__(self, context, request):
        super().__init__(context, request)
        self.backend_record_name = "EEA_KGS_VERSION"
        self.frontend_record_name = "EEA_VOLTO_VERSION"

    def reply(self):
        registry = getUtility(IRegistry)
        backend_value = registry[self.backend_record_name]
        frontend_value = registry[self.frontend_record_name]

        result = {"eeaversions": {"@id": f"{self.context.absolute_url()}/@eeaversions"}}

        result["eeaversions"]["backend_version"] = backend_value
        result["eeaversions"]["frontend_version"] = frontend_value


        self.request.response.setStatus(201)
        self.request.__annotations__.pop("plone.memoize")

        return result
