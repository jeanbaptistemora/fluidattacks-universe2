import os
import shutil
import tarfile
import time
import unittest

import boto3
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException, TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.ui import WebDriverWait

from __init__ import BASE_URL


SCR_PATH = './test/functional/screenshots/'


class ViewTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.geckodriver = os.environ['pkgGeckoDriver']
        self.geckodriver = f'{self.geckodriver}/bin/geckodriver'

        self.firefox = os.environ['pkgFirefox']
        self.firefox = f'{self.firefox}/bin/firefox'

        s3_bucket = 'fluidintegrates.build'
        profile_path = './test/functional/profile.selenium'
        if not os.path.exists(profile_path):
            session = boto3.Session(
                aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                aws_session_token=os.environ.get('AWS_SESSION_TOKEN'))
            resource = session.resource('s3')
            resource.Bucket(s3_bucket).download_file(
                'selenium/firefox-selenium-three-accounts-profile.tar.gz',
                './test/functional/profile.tar.gz')
            with tarfile.open('./test/functional/profile.tar.gz') as tar:
                tar.extractall('./test/functional')
        options = Options()
        options.add_argument('--width=1366')
        options.add_argument('--height=768')
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
        self.ci_node_index = int(os.environ.get('CI_NODE_INDEX', 1))
        self.ci_node_total = int(os.environ.get('CI_NODE_TOTAL', 1))
        if self.branch == 'master':
            self.url = BASE_URL
        elif self.in_ci:
            self.url = \
                f'https://{self.branch}.integrates.fluidattacks.com/integrates'
        else:
            self.url = 'https://localhost:8080/integrates'

        self.selenium = ViewTestCase().__login()

    def tearDown(self):
        if self.selenium.current_url == f'{self.url}/':  # check if should log in again
            self.selenium = self.__login()
        super(ViewTestCase, self).tearDown()

    @classmethod
    def tearDownClass(self):
        if 'pe-7s-power' in self.selenium.page_source:  # logout icon
            logout_btn = self.selenium.find_element_by_xpath(
                '//*[@class="bm-item-list"]/div/ul/li/a')
            ViewTestCase().__click(logout_btn)
            proceed_btn = self.selenium.find_element_by_xpath(
                '//*/button[contains(text(), "Proceed")]')
            ViewTestCase().__click(proceed_btn)
        self.selenium.quit()

    def __cancel_modal(self):
        cancel_btn = self.selenium.find_element_by_xpath(
            '//*/button[contains(text(), "Cancel")]')
        self.__click(cancel_btn)
        time.sleep(2)

    def __check_existing_session(self):
        try:
            selenium = self.selenium
            continue_btn = WebDriverWait(selenium, self.delay/10).until(
                expected.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Continue')]")))
            self.__click(continue_btn)
        except TimeoutException:
            # User does not have existing session
            pass

    def __check_legal_notice(self):
        try:
            selenium = self.selenium
            WebDriverWait(selenium, self.delay/10).until(
                expected.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Legal notice')]")))
            checkbox = selenium.find_element_by_xpath("//*[@name='remember']")
            self.__click(checkbox)
            accept_btn = selenium.find_element_by_xpath(
                "//*[contains(text(), 'Accept and continue')]")
            self.__click(accept_btn)
        except TimeoutException:
            # User has already checked the legal notice
            pass

    def __click(self, element):
        self.selenium.execute_script('arguments[0].click()', element)
        time.sleep(6)

    def __login_aux(self):
        try:
            selenium = self.selenium
            WebDriverWait(selenium, self.delay/10).until(
                expected.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Elegir una cuenta')]")))
            user_to_login = self.ci_node_index % self.ci_node_total
            btn_user = selenium.find_element_by_xpath(
                f"//*[contains(text(), 'continuoushack{user_to_login}@gmail.com')]")
            self.__click(btn_user)
        except TimeoutException:
            pass

    def __login(self):
        selenium = self.selenium
        selenium.get(self.url)
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Sign in with Microsoft')]")))
        selenium.save_screenshot(f'{SCR_PATH}00.00-init-page.png')
        if self.ci_node_index % self.ci_node_total != 0 and self.ci_node_total > 1:
            btn_login = selenium.find_element_by_xpath(
                "//*[contains(text(), 'Sign in with Google')]")
        else:
            btn_login = selenium.find_element_by_xpath(
                "//*[contains(text(), 'Sign in with Microsoft')]")
        self.__click(btn_login)
        self.__login_aux()
        self.__check_existing_session()
        self.__check_legal_notice()

        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'Vulnerabilities over time')]")))
        selenium.save_screenshot(f'{SCR_PATH}00.01-after-login.png')
        return selenium

    def test_02_dashboard(self):
        selenium = self.selenium
        selenium.save_screenshot(SCR_PATH + '01-dashboard.png')
        assert 'Analytics' in selenium.page_source
        assert 'Vulnerabilities over time' in selenium.page_source

    def test_03_analytics(self):
        selenium = self.selenium
        org = 'okada' if self.branch == 'master' else 'imamura'
        selenium.get(self.url + f'/orgs/{org}/groups/unittesting/')
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
               (By.XPATH,
                "//*[contains(text(), 'Vulnerabilities over time')]")))
        selenium.save_screenshot(SCR_PATH + '03-01-analytics.png')
        assert 'Vulnerabilities over time' in selenium.page_source

    def test_04_findings(self):
        selenium = self.selenium
        org = 'okada' if self.branch == 'master' else 'imamura'
        selenium.get(self.url + f'/orgs/{org}/groups/unittesting/vulns')
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'FIN.H.0037. Fuga de información técnica')]")))
        selenium.save_screenshot(SCR_PATH + '04-01-findings.png')
        assert 'FIN.H.0037. Fuga de información técnica' in selenium.page_source

    def test_05_finding(self):
        selenium = self.selenium
        org = 'okada' if self.branch == 'master' else 'imamura'
        selenium.get(self.url + f'/orgs/{org}/groups/unittesting/vulns')
        finding_elem = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'FIN.S.0051. Weak passwords reversed')]")))
        selenium.save_screenshot(SCR_PATH + '05-01-finding.png')

        self.__click(finding_elem)
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'REQ.0132. Passwords (phrase type) must be at least 3 words long')]")))
        time.sleep(5)
        selenium.save_screenshot(SCR_PATH + '05-02-finding.png')

        verify_btn = selenium.find_element_by_xpath(
            '//*/button[text()[contains(., "Reattack")]]')
        self.__click(verify_btn)
        selenium.save_screenshot(SCR_PATH + '05-03-finding.png')

        checkboxes = selenium.find_elements_by_css_selector("#inputsVulns input[type='checkbox']")
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                self.__click(checkbox)
        time.sleep(2)
        selenium.save_screenshot(SCR_PATH + '05-04-finding.png')

        verify_vulns = selenium.find_element_by_id('request_verification_vulns')
        self.__click(verify_vulns)
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Justification')]")))
        time.sleep(2)
        selenium.save_screenshot(SCR_PATH + '05-05-finding.png')

        modal_btn = selenium.find_element_by_xpath(
            '//*[@class="modal-body"]/form/div[2]/button[1]')
        self.__click(modal_btn)
        time.sleep(1)
        selenium.execute_script('window.scrollTo(0, 0);')
        assert 'possible reverse the users credentials due that password' in selenium.page_source

    def test_06_severity(self):
        selenium = self.selenium
        org = 'okada' if self.branch == 'master' else 'imamura'
        selenium.get(self.url + f'/orgs/{org}/groups/unittesting/vulns')
        finding_elem = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'FIN.H.0037. Fuga de información técnica')]")))
        selenium.save_screenshot(SCR_PATH + '06-01-severity.png')

        self.__click(finding_elem)
        sev_elem = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//a[text()[contains(., 'Severity')]]")))
        selenium.save_screenshot(SCR_PATH + '06-02-severity.png')

        self.__click(sev_elem)
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'Confidentiality Impact')]")))
        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '06-03-severity.png')
        assert 'Proof of Concept' in selenium.page_source

    def test_07_evidence(self):
        selenium = self.selenium
        org = 'okada' if self.branch == 'master' else 'imamura'
        selenium.get(self.url + f'/orgs/{org}/groups/unittesting/vulns')
        finding_elem = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'FIN.H.0037. Fuga de información técnica')]")))
        selenium.save_screenshot(SCR_PATH + '07-01-evidence.png')

        self.__click(finding_elem)
        evidence_elem = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//a[text()[contains(., 'Evidence')]]")))
        selenium.save_screenshot(SCR_PATH + '07-02-evidence.png')

        self.__click(evidence_elem)
        selenium.save_screenshot(SCR_PATH + '07-03-evidence.png')

        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Comentario')]")))
        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '07-04-evidence.png')
        assert 'Comentario' in selenium.page_source

    def test_08_exploit(self):
        selenium = self.selenium
        org = 'okada' if self.branch == 'master' else 'imamura'
        selenium.get(self.url + f'/orgs/{org}/groups/unittesting/vulns')
        finding_elem = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'FIN.H.0037. Fuga de información técnica')]")))
        selenium.save_screenshot(SCR_PATH + '08-01-exploit.png')

        self.__click(finding_elem)
        exploit_elem = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//a[text()[contains(., 'Exploit')]]")))
        selenium.save_screenshot(SCR_PATH + '08-02-exploit.png')

        self.__click(exploit_elem)
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'It works')]")))
        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '08-03-exploit.png')
        assert 'It works' in selenium.page_source

    def test_09_tracking(self):
        selenium = self.selenium
        org = 'okada' if self.branch == 'master' else 'imamura'
        selenium.get(self.url + f'/orgs/{org}/groups/unittesting/vulns')
        finding_elem = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'FIN.H.0037. Fuga de información técnica')]")))
        selenium.save_screenshot(SCR_PATH + '09-01-tracking.png')

        self.__click(finding_elem)
        tracking_elem = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//a[text()[contains(., 'Tracking')]]")))

        self.__click(tracking_elem)
        selenium.save_screenshot(SCR_PATH + '09-02-tracking.png')

        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), '2019-09-16')]")))
        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '09-03-tracking.png')
        assert '2019-09-16' in selenium.page_source

    def test_10_comments(self):
        selenium = self.selenium
        org = 'okada' if self.branch == 'master' else 'imamura'
        selenium.get(self.url + f'/orgs/{org}/groups/unittesting/vulns')
        finding_elem = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'FIN.H.0037. Fuga de información técnica')]")))
        selenium.save_screenshot(SCR_PATH + '10-01-comments.png')

        self.__click(finding_elem)
        comments_elem = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//a[text()[contains(., 'Consulting')]]")))
        selenium.save_screenshot(SCR_PATH + '10-02-comments.png')

        self.__click(comments_elem)
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Oldest')]")))
        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '10-03-comments.png')
        assert 'oldest' in selenium.page_source

    def test_11_techpdf(self):
        selenium = self.selenium
        org = 'okada' if self.branch == 'master' else 'imamura'
        selenium.get(self.url + f'/orgs/{org}/groups/unittesting/vulns')
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'FIN.H.0037. Fuga de información técnica')]")))
        rep_modal = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//button[contains(text(),'Reports')]")))
        selenium.save_screenshot(SCR_PATH + '11-01-techpdf.png')

        self.__click(rep_modal)
        tech_pdf_report = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//div[@id='techReport']//button[contains(text(), 'Executive')]")))
        selenium.save_screenshot(SCR_PATH + '11-02-techpdf.png')

        self.__click(tech_pdf_report)
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'FIN.H.0037. Fuga de información')]")))
        selenium.save_screenshot(SCR_PATH + '11-03-techpdf.png')
        assert 'FIN.H.0037. Fuga de información técnica' in selenium.page_source

    def test_13_events(self):
        selenium = self.selenium
        org = 'okada' if self.branch == 'master' else 'imamura'
        selenium.get(self.url + f'/orgs/{org}/groups/unittesting/events')
        event_tab = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'This is an eventuality with evidence')]")))
        selenium.save_screenshot(SCR_PATH + '13-01-events.png')

        self.__click(event_tab)
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'This is an eventuality with evidence')]")))
        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '13-02-events.png')
        assert 'This is an eventuality with evidence' in selenium.page_source

    def test_14_resources(self):
        selenium = self.selenium
        org = 'okada' if self.branch == 'master' else 'imamura'
        selenium.get(self.url + f'/orgs/{org}/groups/unittesting/scope')
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Repositories')]")))
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Environments')]")))
        selenium.save_screenshot(SCR_PATH + '14-01-resources.png')

        add_repos = selenium.find_element_by_xpath(
            '//*[@id="resources"]/div[1]/div[2]/div/button')
        self.__click(add_repos)
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Add repository')]")))
        time.sleep(1)
        selenium.save_screenshot(SCR_PATH + '14-02-resources.png')
        self.__cancel_modal()

        add_envs = selenium.find_element_by_xpath(
            '//*[@id="resources"]/div[3]/div[2]/div/button')
        self.__click(add_envs)
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Add environment')]")))
        time.sleep(1)
        selenium.save_screenshot(SCR_PATH + '14-03-resources.png')
        self.__cancel_modal()

        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Files')]")))
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Portfolio')]")))
        selenium.execute_script(
            'window.scrollTo(0, 680);')
        selenium.save_screenshot(SCR_PATH + '14-04-resources.png')

        add_files = selenium.find_element_by_xpath(
            '//*[@id="resources"]/div[5]/div[2]/div/button')
        self.__click(add_files)
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Add file')]")))
        time.sleep(1)
        selenium.save_screenshot(SCR_PATH + '14-05-resources.png')
        self.__cancel_modal()

        add_tags = selenium.find_element_by_xpath(
            '//*[@id="resources"]/div[7]/div[2]/div/button[1]')
        self.__click(add_tags)
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Add tags')]")))
        time.sleep(1)
        selenium.save_screenshot(SCR_PATH + '14-06-resources.png')
        self.__cancel_modal()

        selenium.execute_script('window.scrollTo(680, 980);')
        selenium.save_screenshot(SCR_PATH + '14-07-resources.png')

        total_tables = len(selenium.find_elements_by_tag_name("table"))
        assert total_tables == 5
        assert 'https://fluidattacks.com' in selenium.page_source

    def test_15_project_comments(self):
        selenium = self.selenium
        org = 'okada' if self.branch == 'master' else 'imamura'
        selenium.get(self.url + f'/orgs/{org}/groups/unittesting/consulting')
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                 "//*[contains(text(), 'Now we can post comments on projects')]")))
        time.sleep(3)
        selenium.save_screenshot(SCR_PATH + '15-01-proj_comments.png')
        assert 'Now we can post comments on projects' in selenium.page_source

    def test_16_forces(self):
        selenium = self.selenium
        project_name = 'bwapp' if self.branch == 'master' else 'unittesting'
        selenium.get(
            self.url + f'/orgs/imamura/groups/{project_name}/devsecops')
        time.sleep(3.0)
        selenium.save_screenshot(SCR_PATH + '16.01-forces-executions.png')

        if self.branch == 'master':
            assert 'There is no data to display' in selenium.page_source
        else:
            forces_elem = WebDriverWait(selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Source Code')]")))
            selenium.save_screenshot(SCR_PATH + '16.02-forces-executions.png')

            forces_elem.click()
            WebDriverWait(selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Exploitable')]")))
            time.sleep(1)
            selenium.save_screenshot(SCR_PATH + '16.03-forces-execution-modal.png')
            assert 'Running Fluid Asserts' in selenium.page_source

    def test_17_pending_to_delete(self):
        selenium = self.selenium

        org = 'okada' if self.branch == 'master' else 'testorg'
        selenium.get(self.url + f'/orgs/{org}/groups/pendingproject')
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Cancel group deletion')]")))
        time.sleep(2)
        selenium.save_screenshot(SCR_PATH + '17-02-pending_to_delete.png')
        assert 'Group pending to delete' in selenium.page_source

        selenium.get(self.url + f'/orgs/{org}/groups/pendingproject/vulns')
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Cancel group deletion')]")))
        selenium.save_screenshot(SCR_PATH + '17-03-pending_to_delete.png')
        assert 'Group pending to delete' in selenium.page_source


    def test_18_tag_indicators(self):
        selenium = self.selenium

        org = 'okada' if self.branch == 'master' else 'imamura'
        selenium.get(
            self.url + f'/orgs/{org}/portfolios/test-projects/indicators')
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Max open severity')]")))
        selenium.save_screenshot(SCR_PATH + '18-01-tag_indicators.png')

        selenium.execute_script('window.scrollTo(0, 380);')
        selenium.save_screenshot(SCR_PATH + '18-02-tag_indicators.png')

        selenium.execute_script('window.scrollTo(380, 800);')
        selenium.save_screenshot(SCR_PATH + '18-03-tag_indicators.png')

        selenium.execute_script('window.scrollTo(800, 1200);')
        selenium.save_screenshot(SCR_PATH + '18-04-tag_indicators.png')

        selenium.execute_script('window.scrollTo(1300, 1700);')
        selenium.save_screenshot(SCR_PATH + '18-05-tag_indicators.png')

        selenium.execute_script('window.scrollTo(1900, 2300);')
        selenium.save_screenshot(SCR_PATH + '18-06-tag_indicators.png')

        selenium.execute_script('window.scrollTo(2300, 2700);')
        selenium.save_screenshot(SCR_PATH + '18-07-tag_indicators.png')

        total_tables = len(selenium.find_elements_by_tag_name("table"))
        assert total_tables == 1
        assert 'Open vulnerabilities by group' in selenium.page_source
        assert 'Findings by group' in selenium.page_source
        assert 'Open findings by group' in selenium.page_source
        assert 'Mean time to remediate' in selenium.page_source
        assert 'remediated' in selenium.page_source
        assert 'Status' in selenium.page_source
        assert 'Treatment' in selenium.page_source
        assert 'Treatmentless by group' in selenium.page_source

        selenium.get(
            self.url + f'/orgs/{org}/portfolios/doesnotexists/indicators')
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Vulnerabilities over time')]")))
        selenium.save_screenshot(SCR_PATH + '18-09-tag_indicators.png')
