import json
import os
from collections import OrderedDict

from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from .api.formstack import FormstackAPI
from .entity import schema


class ViewTestCase(TestCase):

    def setUp(self):
        options = Options()
        options.headless = True
        self.selenium = webdriver.Firefox(options=options)
        self.branch = os.environ['CI_COMMIT_REF_NAME']

        super(ViewTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(ViewTestCase, self).tearDown()

    def test_init_page(self):
        selenium = self.selenium
        selenium.get('https://{}.integrates.env.fluidattacks.com'.
                     format(self.branch))
        assert 'Log in with Google' in selenium.page_source
