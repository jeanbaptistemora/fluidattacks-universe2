import os
import shutil
import tarfile
import time
import unittest

import boto3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.ui import WebDriverWait

SCR_PATH = './test/functional/screenshots/'


class ViewTestCase(unittest.TestCase):

    def setUp(self):
        self.geckodriver = os.environ['pkgGeckoDriver']
        self.geckodriver = f'{self.geckodriver}/bin/geckodriver'

        self.firefox = os.environ['pkgFirefox']
        self.firefox = f'{self.firefox}/bin/firefox'

        s3_bucket = 'fluidintegrates.resources'
        profile_path = './test/functional/profile'
        if not os.path.exists(profile_path):
            session = boto3.Session(
                aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
            resource = session.resource('s3')
            resource.Bucket(s3_bucket).download_file(
                'selenium/firefox-selenium-profile.tar.gz',
                './test/functional/profile.tar.gz')
            with tarfile.open('./test/functional/profile.tar.gz') as tar:
                tar.extractall('./test/functional')
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--window-size=1366,768')
        options.binary_location = self.firefox
        options.headless = True
        self.delay = 60
        self.selenium = webdriver.Firefox(
          executable_path=self.geckodriver,
          firefox_binary=self.firefox,
          firefox_profile=profile_path,
          options=options)
        self.branch = os.environ['CI_COMMIT_REF_NAME']
        self.in_ci = bool(os.environ['CI'])
        if self.branch == 'master':
            self.url = 'https://fluidattacks.com/integrates'
        elif self.in_ci:
            self.url = \
                f'https://{self.branch}.integrates.env.fluidattacks.com/integrates'
            self.url_async = \
                f'https://{self.branch}-async.integrates.env.fluidattacks.com/integrates'
        else:
            self.url = 'https://localhost:8080/integrates'

        super(ViewTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(ViewTestCase, self).tearDown()

    def __login(self):
        selenium = self.selenium
        selenium.get(self.url)
        time.sleep(5)
        selenium.find_element_by_xpath(
            "//*[contains(text(), 'Log in with Google')]").click()
        WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'Integrates unit test project')]")))
        return selenium

    def __login_async(self):
        selenium = self.selenium
        selenium.get(self.url_async)
        time.sleep(5)
        selenium.find_element_by_xpath(
            "//*[contains(text(), 'Log in with Google')]").click()
        WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'Integrates unit test project')]")))
        return selenium

    def test_01_init_page(self):
        selenium = self.selenium
        selenium.get(self.url)
        WebDriverWait(selenium,
                      self.delay).until(
                          expected.presence_of_element_located(
                              (By.XPATH,
                               "//*[contains(text(), 'Log in with Google')]")))
        selenium.save_screenshot(SCR_PATH + '01-init_page.png')
        assert 'Log in with Google' in selenium.page_source

    def test_01_init_page_async(self):
        selenium = self.selenium
        selenium.get(self.url_async)
        WebDriverWait(selenium,
                      self.delay).until(
                          expected.presence_of_element_located(
                              (By.XPATH,
                               "//*[contains(text(), 'Log in with Google')]")))
        selenium.save_screenshot(SCR_PATH + '01-init_page_async.png')
        assert 'Log in with Google' in selenium.page_source

    def test_02_dashboard(self):
        selenium = self.__login()
        selenium.save_screenshot(SCR_PATH + '02-dashboard.png')
        assert 'Integrates unit test project' in selenium.page_source

    def test_02_dashboard_async(self):
        selenium = self.__login_async()
        selenium.save_screenshot(SCR_PATH + '02-dashboard-async.png')
        assert 'Integrates unit test project' in selenium.page_source

    def test_03_indicators(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'Integrates unit test project')]")))
        selenium.save_screenshot(SCR_PATH + '03-01-indicators.png')
        proj_elem.click()
        WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'Max severity found')]")))
        selenium.save_screenshot(SCR_PATH + '03-02-indicators.png')
        assert 'Max severity found' in selenium.page_source

    def test_04_findings(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'Integrates unit test project')]")))
        selenium.save_screenshot(SCR_PATH + '04-01-findings.png')
        proj_elem.click()

        selenium.get(self.url + '/dashboard#!/project/UNITTESTING/findings')
        WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'FIN.H.0037. Fuga de información técnica')]")))
        selenium.save_screenshot(SCR_PATH + '04-02-findings.png')
        assert 'FIN.H.0037. Fuga de información técnica' in selenium.page_source

    def test_05_finding(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'Integrates unit test project')]")))
        selenium.save_screenshot(SCR_PATH + '05-01-finding.png')
        proj_elem.click()

        selenium.get(self.url + '/dashboard#!/project/UNITTESTING/findings')
        find_ele = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'FIN.S.0051. Weak passwords reversed')]")))
        selenium.save_screenshot(SCR_PATH + '05-02-finding.png')

        find_ele.click()
        WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'REQ.0132. Passwords (phrase type) must be at least 3 words long')]")))

        time.sleep(5)
        selenium.save_screenshot(SCR_PATH + '05-03-finding.png')
        selenium.find_element_by_xpath(
            '//*/button[contains(text(), "Request verification")]').click()
        selenium.save_screenshot(SCR_PATH + '05-04-finding.png')
        checkboxes = selenium.find_elements_by_css_selector("#inputsVulns input[type='checkbox']")
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                checkbox.click()
        time.sleep(2)
        selenium.save_screenshot(SCR_PATH + '05-05-finding.png')
        selenium.find_element_by_id(
            'request_verification_vulns').click()

        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Justification')]")))
        time.sleep(2)
        selenium.save_screenshot(SCR_PATH + '05-06-finding.png')
        selenium.find_element_by_xpath(
            '//*[@class="modal-body"]/form/div[2]/button[1]').click()
        time.sleep(1)

        selenium.find_element_by_xpath(
            '//*/button[contains(text(), "Cancel Request")]').click()
        assert 'possible reverse the users credentials due that password' in selenium.page_source

    def test_06_severity(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'Integrates unit test project')]")))
        selenium.save_screenshot(SCR_PATH + '06-01-severity.png')
        proj_elem.click()

        selenium.get(self.url + '/dashboard#!/project/UNITTESTING/findings')
        find_ele = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'FIN.H.0037. Fuga de información técnica')]")))
        selenium.save_screenshot(SCR_PATH + '06-02-severity.png')
        find_ele.click()
        sev_elem = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.ID, 'cssv2Item')))
        selenium.save_screenshot(SCR_PATH + '06-03-severity.png')
        sev_elem.click()

        WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'Confidentiality Impact')]")))

        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '06-04-severity.png')
        assert 'Proof of Concept' in selenium.page_source

    def test_07_evidence(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'Integrates unit test project')]")))
        selenium.save_screenshot(SCR_PATH + '07-01-evidence.png')
        proj_elem.click()

        selenium.get(self.url + '/dashboard#!/project/UNITTESTING/findings')
        find_ele = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'FIN.H.0037. Fuga de información técnica')]")))
        selenium.save_screenshot(SCR_PATH + '07-02-evidence.png')
        find_ele.click()
        sev_elem = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.ID, 'evidenceItem')))
        selenium.save_screenshot(SCR_PATH + '07-03-evidence.png')
        evidences = sev_elem.find_element_by_link_text('Evidence')
        evidences.click()
        selenium.save_screenshot(SCR_PATH + '07-04-evidence.png')
        WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'Comentario')]")))
        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '07-05-evidence.png')
        assert 'Comentario' in selenium.page_source

    def test_08_exploit(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'Integrates unit test project')]")))
        selenium.save_screenshot(SCR_PATH + '08-01-exploit.png')
        proj_elem.click()

        selenium.get(self.url + '/dashboard#!/project/UNITTESTING/findings')
        find_ele = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'FIN.H.0037. Fuga de información técnica')]")))
        selenium.save_screenshot(SCR_PATH + '08-02-exploit.png')
        find_ele.click()
        sev_elem = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.ID, 'exploitItem')))
        selenium.save_screenshot(SCR_PATH + '08-03-exploit.png')
        sev_elem.click()
        WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'It works')]")))
        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '08-04-exploit.png')
        assert 'It works' in selenium.page_source

    def test_09_tracking(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'Integrates unit test project')]")))
        selenium.save_screenshot(SCR_PATH + '09-01-tracking.png')
        proj_elem.click()

        selenium.get(self.url + '/dashboard#!/project/UNITTESTING/findings')
        find_ele = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'FIN.H.0037. Fuga de información técnica')]")))
        selenium.save_screenshot(SCR_PATH + '09-02-tracking.png')
        find_ele.click()
        sev_elem = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.ID, 'trackingItem')))
        tracking = sev_elem.find_element_by_link_text('Tracking')
        tracking.click()
        selenium.save_screenshot(SCR_PATH + '09-03-tracking.png')
        WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), '2019-09-16')]")))
        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '09-04-tracking.png')
        assert '2019-09-16' in selenium.page_source

    def test_10_comments(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'Integrates unit test project')]")))
        selenium.save_screenshot(SCR_PATH + '10-01-comments.png')
        proj_elem.click()

        selenium.get(self.url + '/dashboard#!/project/UNITTESTING/findings')
        find_ele = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'FIN.H.0037. Fuga de información técnica')]")))
        selenium.save_screenshot(SCR_PATH + '10-02-comments.png')
        find_ele.click()
        sev_elem = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.ID, 'commentItem')))
        selenium.save_screenshot(SCR_PATH + '10-03-comments.png')
        sev_elem.click()
        WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'Oldest')]")))
        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '10-04-comments.png')
        assert 'oldest' in selenium.page_source

    def test_11_techpdf(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'Integrates unit test project')]")))
        selenium.save_screenshot(SCR_PATH + '11-01-techpdf.png')
        proj_elem.click()

        selenium.get(self.url + '/dashboard#!/project/UNITTESTING/findings')
        WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'FIN.H.0037. Fuga de información técnica')]")))

        rep_modal = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//button[contains(text(),'Reports')]")))
        selenium.save_screenshot(SCR_PATH + '11-02-techpdf.png')
        rep_modal.click()
        tech_pdf_report = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//div[@id='techReport']//button[contains(text(), 'PDF')]")))

        selenium.save_screenshot(SCR_PATH + '11-03-techpdf.png')
        tech_pdf_report.click()
        WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'FIN.H.0037. Fuga de información')]")))
        selenium.save_screenshot(SCR_PATH + '11-04-techpdf.png')
        assert 'FIN.H.0037. Fuga de información técnica' in selenium.page_source

    def test_13_events(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'Integrates unit test project')]")))
        selenium.save_screenshot(SCR_PATH + '13-01-events.png')
        proj_elem.click()
        selenium.get(self.url + '/dashboard#!/project/UNITTESTING/events')

        event_tab = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'This is an eventuality with evidence')]")))
        selenium.save_screenshot(SCR_PATH + '13-02-events.png')
        event_tab.click()
        WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'This is an eventuality with evidence')]")))

        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '13-03-events.png')
        assert 'This is an eventuality with evidence' in selenium.page_source

    def test_14_resources(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'Integrates unit test project')]")))
        selenium.save_screenshot(SCR_PATH + '14-01-resources.png')
        proj_elem.click()
        selenium.get(self.url + '/dashboard#!/project/UNITTESTING/resources')

        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Repositories')]")))

        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Environments')]")))

        selenium.save_screenshot(SCR_PATH + '14-02-resources.png')

        selenium.find_element_by_xpath(
            '//*[@id="resources"]/div[1]/div[2]/div/button').click()

        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Add repository')]")))
        time.sleep(1)
        selenium.save_screenshot(SCR_PATH + '14-03-resources.png')
        selenium.find_element_by_xpath(
            '//*/button[contains(text(), "Cancel")]').click()
        time.sleep(2)

        selenium.find_element_by_xpath(
            '//*[@id="resources"]/div[3]/div[2]/div/button').click()
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Add environment')]")))
        time.sleep(1)
        selenium.save_screenshot(SCR_PATH + '14-04-resources.png')
        selenium.find_element_by_xpath(
            '//*/button[contains(text(), "Cancel")]').click()
        time.sleep(2)

        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Files')]")))

        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Portfolio')]")))

        selenium.execute_script(
            'window.scrollTo(0, 680);')
        selenium.save_screenshot(SCR_PATH + '14-05-resources.png')

        selenium.find_element_by_xpath(
            '//*[@id="resources"]/div[5]/div[2]/div/button').click()
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Add file')]")))
        time.sleep(1)
        selenium.save_screenshot(SCR_PATH + '14-06-resources.png')
        selenium.find_element_by_xpath(
            '//*/button[contains(text(), "Cancel")]').click()
        time.sleep(2)

        selenium.find_element_by_xpath(
            '//*[@id="resources"]/div[7]/div[2]/div/button[1]').click()
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Add tags')]")))
        time.sleep(1)
        selenium.save_screenshot(SCR_PATH + '14-07-resources.png')
        selenium.find_element_by_xpath(
            '//*/button[contains(text(), "Cancel")]').click()

        selenium.execute_script(
            'window.scrollTo(680, 980);')
        selenium.save_screenshot(SCR_PATH + '14-08-resources.png')
        selenium.find_element_by_xpath(
            '//*[@id="resources"]/div[10]/div/div/button ').click()
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Delete Project')]")))
        time.sleep(1)
        selenium.save_screenshot(SCR_PATH + '14-09-resources.png')
        selenium.find_element_by_xpath(
            '//*/button[contains(text(), "Cancel")]').click()

        total_tables = len(selenium.find_elements_by_tag_name("table"))
        assert total_tables == 4
        assert 'https://fluidattacks.com' in selenium.page_source

    def test_15_project_comments(self):
        selenium = self.__login()
        proj_elem = WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'Integrates unit test project')]")))
        selenium.save_screenshot(SCR_PATH + '15-01-proj_comments.png')
        proj_elem.click()
        selenium.get(self.url + '/dashboard#!/project/UNITTESTING/comments')

        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                 "//*[contains(text(), 'Now we can post comments on projects')]")))

        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '15-02-proj_comments.png')
        assert 'Now we can post comments on projects' in selenium.page_source
