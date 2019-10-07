import boto3
import os
import tarfile
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pytest
import unittest

SCR_PATH = 'screenshots/'

class ViewTestCase(unittest.TestCase):

    def setUp(self):
        s3_bucket = 'fluidintegrates.resources'
        profile_path = os.path.join(os.getcwd(), 'selenium_profile.default')
        if not os.path.exists(profile_path):
            session = boto3.Session(
                aws_access_key_id = os.environ['FI_AWS_S3_ACCESS_KEY'],
                aws_secret_access_key = os.environ['FI_AWS_S3_SECRET_KEY'])
            s3 = session.resource('s3')
            s3.Bucket(s3_bucket).download_file(
                'selenium/selenium_profile.tar.gz', 'profile.tar.gz')
            with tarfile.open('profile.tar.gz') as tar:
              tar.extractall()
        options = Options()
        profile = FirefoxProfile(profile_path)
        options.headless = True
        self.delay = 20
        self.selenium = webdriver.Firefox(
            firefox_profile=profile,
            options=options)
        self.branch = os.environ['CI_COMMIT_REF_NAME']
        if self.branch == 'master':
            self.url = 'https://fluidattacks.com/integrates'
        else:
            self.url = \
                'https://{}.integrates.env.fluidattacks.com/integrates'.format(self.branch)

        super(ViewTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(ViewTestCase, self).tearDown()

    def __login(self):
        selenium = self.selenium
        selenium.get(self.url)
        selenium.find_element_by_xpath(
            "//*[contains(text(), 'Log in with Google')]").click()
        WebDriverWait(selenium,
                      self.delay).until(
                          EC.presence_of_element_located(
                                (By.XPATH,
                                "//*[contains(text(), 'BWAPP Sample')]")))
        return selenium

    def test_01_init_page(self):
        selenium = self.selenium
        selenium.get(self.url)
        selenium.save_screenshot(SCR_PATH + '01-init_page.png')
        assert 'Log in with Google' in selenium.page_source

    def test_02_dashboard(self):
        selenium = self.__login()
        selenium.save_screenshot(SCR_PATH + '02-dashboard.png')
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
                                "//*[contains(text(), 'Max severity found')]")))
        selenium.save_screenshot(SCR_PATH + '03-indicators.png')
        assert 'Max severity found' in selenium.page_source

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
        selenium.save_screenshot(SCR_PATH + '04-findings.png')
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

        time.sleep(5)
        selenium.save_screenshot(SCR_PATH + '05-finding.png')
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
                            "//*[contains(text(), 'CVSS v3 Temporal')]")))

        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '06-severity.png')
        assert 'Proof of Concept' in selenium.page_source

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
        selenium.save_screenshot(SCR_PATH + '07-evidence.png')
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
        selenium.save_screenshot(SCR_PATH + '08-exploit.png')
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
                            "//*[contains(text(), '2019-01-21')]")))
        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '09-tracking.png')
        assert '2019-01-21' in selenium.page_source

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
                            "//*[contains(text(), 'Validations were run against 5 of the 10 reported fields')]")))
        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '10-comments.png')
        assert 'Validations were run against 5 of the 10 reported fields' in selenium.page_source

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
                                             "//button[contains(text(),'Reports')]")))
        rep_modal.click()
        tech_pdf_report = WebDriverWait(selenium,
                                        self.delay).until(
                                            EC.presence_of_element_located(
                                                (By.XPATH,
                                                 "//div[@id='techReport']//button[contains(text(), 'PDF')]")))

        tech_pdf_report.click()
        WebDriverWait(selenium,
                      self.delay).until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                             "//*[contains(text(), 'Reflected Cross')]")))
        selenium.save_screenshot(SCR_PATH + '11-techpdf.png')
        assert 'Reflected Cross Site' in selenium.page_source

    def test_13_events(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(selenium,
                                  self.delay).until(
                                      EC.presence_of_element_located(
                                          (By.XPATH,
                                           "//*[contains(text(), 'BWAPP Sample')]")))
        proj_elem.click()
        selenium.get(self.url + '/dashboard#!/project/BWAPP/events')

        event_tab = WebDriverWait(selenium,
                                   self.delay).until(
                                        EC.presence_of_element_located(
                                            (By.XPATH,
                                             "//*[contains(text(), 'not possible to access the repo')]")))
        selenium.save_screenshot(SCR_PATH + '131-events.png')
        event_tab.click()
        WebDriverWait(selenium,
                      self.delay).until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                             "//*[contains(text(), 'Affected components')]")))

        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '132-events.png')
        assert 'Test Event' in selenium.page_source

    def test_14_resources(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(selenium,
                                  self.delay).until(
                                      EC.presence_of_element_located(
                                          (By.XPATH,
                                           "//*[contains(text(), 'BWAPP Sample')]")))
        proj_elem.click()
        selenium.get(self.url + '/dashboard#!/project/BWAPP/resources')

        WebDriverWait(selenium, self.delay).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Environments')]")))

        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '14-resources.png')
        assert 'https://fluidattacks.com' in selenium.page_source

    def test_15_project_comments(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(selenium,
                                  self.delay).until(
                                      EC.presence_of_element_located(
                                          (By.XPATH,
                                           "//*[contains(text(), 'BWAPP Sample')]")))
        proj_elem.click()
        selenium.get(self.url + '/dashboard#!/project/BWAPP/comments')

        WebDriverWait(selenium, self.delay).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Now we can post comments on projects')]")))

        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '15-proj_comments.png')
        assert 'Now we can post comments on projects' in selenium.page_source
