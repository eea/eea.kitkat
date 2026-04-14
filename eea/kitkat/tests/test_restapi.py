"""Integration tests for eea.kitkat

Tests for view classes and installation.
"""

import unittest
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from transaction import commit
from eea.kitkat.tests.base import FUNCTIONAL_TESTING


class TestKitkatSetup(unittest.TestCase):
    """Test eea.kitkat installation"""

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_product_installed(self):
        """Test that eea.kitkat is installed"""
        from Products.CMFPlone.utils import get_installer

        installer = get_installer(self.portal, self.layer["request"])
        self.assertTrue(installer.is_product_installed("eea.kitkat"))

    def test_portal_exists(self):
        """Test that portal is set up"""
        self.assertIsNotNone(self.portal)


class TestKitkatModuleImport(unittest.TestCase):
    """Test eea.kitkat module imports"""

    def test_captcha_key_class_importable(self):
        """Test that CaptchaKeyGet class can be imported"""
        from eea.kitkat.restapi.get import CaptchaKeyGet

        self.assertIsNotNone(CaptchaKeyGet)

    def test_captcha_verify_class_importable(self):
        """Test that CaptchaVerifyPost class can be imported"""
        from eea.kitkat.restapi.post import CaptchaVerifyPost

        self.assertIsNotNone(CaptchaVerifyPost)

    def test_captcha_settings_importable(self):
        """Test that ICaptchaSettings can be imported"""
        from eea.kitkat.browser.captcha import ICaptchaSettings

        self.assertIsNotNone(ICaptchaSettings)

    def test_captcha_class_importable(self):
        """Test that Captcha browser view can be imported"""
        from eea.kitkat.browser.captcha import Captcha

        self.assertIsNotNone(Captcha)


if __name__ == "__main__":
    unittest.main()
