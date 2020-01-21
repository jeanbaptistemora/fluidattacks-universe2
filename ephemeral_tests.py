import os
import shutil
import tarfile
import time
import unittest

import boto3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.ui import WebDriverWait

SCR_PATH = 'screenshots/'


class ViewTestCase(unittest.TestCase):

    def setUp(self):
        s3_bucket = 'fluidintegrates.resources'
        profile_path = '/root/.config/google-chrome/Default'
        if not os.path.exists(profile_path):
            session = boto3.Session(
                aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
            s3_sess = session.resource('s3')
            s3_sess.Bucket(s3_bucket).download_file(
                'selenium/chrome-selenium-profile.tar.gz', 'profile.tar.gz')
            with tarfile.open('profile.tar.gz') as tar:
                tar.extractall()
            profile_src = os.getcwd() + '/Default'
            profile_dest = '/root/.config/google-chrome/Default'
            shutil.move(profile_src, profile_dest)
        options = Options()
        options.add_argument('--user-data-dir=/root/.config/google-chrome')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.headless = True
        self.delay = 20
        self.selenium = webdriver.Chrome('/usr/bin/chromedriver',
                                         options=options)
        self.branch = os.environ['CI_COMMIT_REF_NAME']
        if self.branch == 'master':
            self.url = 'https://fluidattacks.com/integrates'
        else:
            self.url = \
                f'https://{self.branch}.integrates.env.fluidattacks.com/integrates'

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

    def test_02_dashboard(self):
        selenium = self.__login()
        selenium.save_screenshot(SCR_PATH + '02-dashboard.png')
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
                     "//*[contains(text(), 'FIN.H.0037. Fuga de información técnica')]")))
        selenium.save_screenshot(SCR_PATH + '05-02-finding.png')
        find_ele.click()
        WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'Eliminar el banner de los servicios')]")))

        time.sleep(5)
        selenium.save_screenshot(SCR_PATH + '05-03-finding.png')
        assert 'Descripción de fuga de información técnica' in selenium.page_source
        assert 'REQ.0077. La aplicación no debe revelar detalles' in selenium.page_source

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
        sev_elem.click()
        WebDriverWait(
            selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(text(), 'Comentario')]")))
        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '07-04-evidence.png')
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
        selenium.save_screenshot(SCR_PATH + '09-03-tracking.png')
        sev_elem.click()
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
                (By.XPATH, "//*[contains(text(), 'Environments')]")))

        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '14-02-resources.png')
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
