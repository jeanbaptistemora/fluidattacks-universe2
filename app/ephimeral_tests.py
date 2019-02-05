import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pytest
import unittest


class ViewTestCase(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.headless = True
        self.delay = 20
        self.selenium = webdriver.Firefox(options=options)
        self.branch = os.environ['CI_COMMIT_REF_NAME']
        self.url = \
            'https://{}.integrates.env.fluidattacks.com'.format(self.branch)
        self.username = os.environ['FI_INTEGRATES_USER']
        self.password = os.environ['FI_INTEGRATES_USERPASS']

        super(ViewTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(ViewTestCase, self).tearDown()

    def __login(self):
        selenium = self.selenium
        selenium.get(self.url)
        selenium.find_element_by_xpath(
            "//*[contains(text(), 'Log in with Google')]").click()
        email_id = \
            WebDriverWait(selenium,
                          self.delay).until(
                              EC.presence_of_element_located(
                                  (By.NAME, 'identifier')))

        email_id.send_keys(self.username)
        selenium.find_elements_by_xpath(
            "//*[contains(text(), 'Next')]")[1].click()
        time.sleep(3)
        pass_id = \
            WebDriverWait(selenium,
                          self.delay).until(
                              EC.presence_of_element_located(
                                  (By.XPATH,
                                   "//*[contains(@type, 'password')]")))

        pass_id.send_keys(self.password)
        selenium.find_elements_by_xpath(
            "//*[contains(text(), 'Next')]")[1].click()
        WebDriverWait(selenium,
                      self.delay).until(
                          EC.presence_of_element_located(
                                (By.XPATH,
                                "//*[contains(text(), 'BWAPP Sample')]")))
        return selenium

    def test_01_init_page(self):
        selenium = self.selenium
        selenium.get(self.url)
        assert 'Log in with Google' in selenium.page_source

    def test_02_dashboard(self):
        selenium = self.__login()

        assert 'BWAPP Sample' in selenium.page_source

    def test_03_indicators(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(selenium,
                                  self.delay).until(
                                      EC.presence_of_element_located(
                                          (By.XPATH,
                                           "//*[contains(text(), 'BWAPP Sample')]")))
        proj_elem.click()
        WebDriverWait(selenium,
                      self.delay).until(
                            EC.presence_of_element_located(
                                (By.XPATH,
                                "//*[contains(text(), 'Maximum Severity Found')]")))

        assert 'Maximum Severity Found' in selenium.page_source

    def test_04_findings(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(selenium,
                                  self.delay).until(
                                      EC.presence_of_element_located(
                                          (By.XPATH,
                                           "//*[contains(text(), 'BWAPP Sample')]")))
        proj_elem.click()

        selenium.get(self.url + '/dashboard#!/project/BWAPP/findings')
        WebDriverWait(selenium,
                      self.delay).until(
                            EC.presence_of_element_located(
                                (By.XPATH,
                                "//*[contains(text(), 'Reflected Cross Site')]")))
        assert 'Reflected Cross Site' in selenium.page_source

    def test_05_finding(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(selenium,
                                  self.delay).until(
                                      EC.presence_of_element_located(
                                          (By.XPATH,
                                           "//*[contains(text(), 'BWAPP Sample')]")))
        proj_elem.click()

        selenium.get(self.url + '/dashboard#!/project/BWAPP/findings')
        find_ele = WebDriverWait(selenium,
                                self.delay).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH,
                                         "//*[contains(text(), 'Reflected Cross Site')]")))
        find_ele.click()
        WebDriverWait(selenium,
                      self.delay).until(
                            EC.presence_of_element_located(
                                (By.XPATH,
                                "//*[contains(text(), 'http://localhost/bWAPP/htmli_post.php')]")))

        time.sleep(3)
        assert 'The forms in the application allow the injection of code' in selenium.page_source
        assert 'REQ.0173. The system must discard all' in selenium.page_source
        assert 'http://localhost/bWAPP/htmli_post.php' in selenium.page_source

    def test_06_severity(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(selenium,
                                  self.delay).until(
                                      EC.presence_of_element_located(
                                          (By.XPATH,
                                           "//*[contains(text(), 'BWAPP Sample')]")))
        proj_elem.click()

        selenium.get(self.url + '/dashboard#!/project/BWAPP/findings')
        find_ele = WebDriverWait(selenium,
                                self.delay).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH,
                                         "//*[contains(text(), 'Reflected Cross Site')]")))
        find_ele.click()
        sev_elem = WebDriverWait(selenium,
                                self.delay).until(
                                    EC.presence_of_element_located(
                                        (By.ID, 'cssv2Item')))
        sev_elem.click()

        WebDriverWait(selenium,
                      self.delay).until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                            "//*[contains(text(), 'CVSS v2 Temporal')]")))

        time.sleep(3)
        assert 'The vulnerability is recognized' in selenium.page_source

    def test_07_evidence(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(selenium,
                                  self.delay).until(
                                      EC.presence_of_element_located(
                                          (By.XPATH,
                                           "//*[contains(text(), 'BWAPP Sample')]")))
        proj_elem.click()

        selenium.get(self.url + '/dashboard#!/project/BWAPP/findings')
        find_ele = WebDriverWait(selenium,
                                self.delay).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH,
                                         "//*[contains(text(), 'Reflected Cross Site')]")))
        find_ele.click()
        sev_elem = WebDriverWait(selenium,
                                self.delay).until(
                                    EC.presence_of_element_located(
                                        (By.ID, 'evidenceItem')))
        sev_elem.click()
        WebDriverWait(selenium,
                      self.delay).until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                            "//*[contains(text(), 'Pop-up message')]")))
        time.sleep(3)
        assert 'Pop-up message' in selenium.page_source

    def test_08_exploit(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(selenium,
                                  self.delay).until(
                                      EC.presence_of_element_located(
                                          (By.XPATH,
                                           "//*[contains(text(), 'BWAPP Sample')]")))
        proj_elem.click()

        selenium.get(self.url + '/dashboard#!/project/BWAPP/findings')
        find_ele = WebDriverWait(selenium,
                                self.delay).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH,
                                         "//*[contains(text(), 'Reflected Cross Site')]")))
        find_ele.click()
        sev_elem = WebDriverWait(selenium,
                                self.delay).until(
                                    EC.presence_of_element_located(
                                        (By.ID, 'exploitItem')))
        sev_elem.click()
        WebDriverWait(selenium,
                      self.delay).until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                            "//*[contains(text(), 'http.has_xss')]")))
        time.sleep(3)
        assert 'http.has_xss' in selenium.page_source

    def test_09_tracking(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(selenium,
                                  self.delay).until(
                                      EC.presence_of_element_located(
                                          (By.XPATH,
                                           "//*[contains(text(), 'BWAPP Sample')]")))
        proj_elem.click()

        selenium.get(self.url + '/dashboard#!/project/BWAPP/findings')
        find_ele = WebDriverWait(selenium,
                                self.delay).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH,
                                         "//*[contains(text(), 'Reflected Cross Site')]")))
        find_ele.click()
        sev_elem = WebDriverWait(selenium,
                                self.delay).until(
                                    EC.presence_of_element_located(
                                        (By.ID, 'trackingItem')))
        sev_elem.click()
        WebDriverWait(selenium,
                      self.delay).until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                            "//*[contains(text(), '2019-01-28')]")))
        time.sleep(3)
        assert '2019-01-28' in selenium.page_source

    def test_10_comments(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(selenium,
                                  self.delay).until(
                                      EC.presence_of_element_located(
                                          (By.XPATH,
                                           "//*[contains(text(), 'BWAPP Sample')]")))
        proj_elem.click()

        selenium.get(self.url + '/dashboard#!/project/BWAPP/findings')
        find_ele = WebDriverWait(selenium,
                                self.delay).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH,
                                         "//*[contains(text(), 'Reflected Cross Site')]")))
        find_ele.click()
        sev_elem = WebDriverWait(selenium,
                                self.delay).until(
                                    EC.presence_of_element_located(
                                        (By.ID, 'commentItem')))
        sev_elem.click()
        WebDriverWait(selenium,
                      self.delay).until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                            "//*[contains(text(), 'Se realizaron validaciones en 5/10 campos reportados')]")))
        time.sleep(3)
        assert 'Se realizaron validaciones en 5/10 campos reportados' in selenium.page_source

    def test_11_techpdf(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(selenium,
                                  self.delay).until(
                                      EC.presence_of_element_located(
                                          (By.XPATH,
                                           "//*[contains(text(), 'BWAPP Sample')]")))
        proj_elem.click()

        selenium.get(self.url + '/dashboard#!/project/BWAPP/findings')
        WebDriverWait(selenium,
                      self.delay).until(
                            EC.presence_of_element_located(
                                (By.XPATH,
                                "//*[contains(text(), 'Reflected Cross Site')]")))

        rep_modal = WebDriverWait(selenium,
                                  self.delay).until(
                                        EC.presence_of_element_located(
                                            (By.XPATH,
                                             "//*[contains(@data-original-title, 'Documentation')]")))
        rep_modal.click()
        tech_pdf_report = WebDriverWait(selenium,
                                        self.delay).until(
                                            EC.presence_of_element_located(
                                                (By.XPATH,
                                                 "//*[contains(@ng-click, 'findingMatrizTechnicalPDFReport')]")))

        tech_pdf_report.click()
        WebDriverWait(selenium,
                      self.delay).until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                             "//*[contains(text(), 'Reflected Cross')]")))
        assert 'Reflected Cross Site' in selenium.page_source

    def test_12_execpdf(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(selenium,
                                  self.delay).until(
                                      EC.presence_of_element_located(
                                          (By.XPATH,
                                           "//*[contains(text(), 'BWAPP Sample')]")))
        proj_elem.click()

        selenium.get(self.url + '/dashboard#!/project/BWAPP/findings')
        WebDriverWait(selenium,
                      self.delay).until(
                            EC.presence_of_element_located(
                                (By.XPATH,
                                "//*[contains(text(), 'Reflected Cross Site')]")))

        rep_modal = WebDriverWait(selenium,
                                  self.delay).until(
                                        EC.presence_of_element_located(
                                            (By.XPATH,
                                             "//*[contains(@data-original-title, 'Documentation')]")))
        rep_modal.click()
        exec_pdf_report = WebDriverWait(selenium,
                                        self.delay).until(
                                            EC.presence_of_element_located(
                                                (By.XPATH,
                                                 "//*[contains(@ng-click, 'findingMatrizExecutivePDFPresentation')]")))

        exec_pdf_report.click()
        WebDriverWait(selenium,
                      self.delay).until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                             "//*[contains(text(), 'Reflected Cross')]")))
        assert 'Reflected Cross Site' in selenium.page_source
