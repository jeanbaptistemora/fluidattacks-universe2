import os
import pytest
import shutil
import tarfile
import time
import unittest
import contextlib

import boto3
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException
)
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
            self.url = 'https://integrates.fluidattacks.com/new'
        elif self.in_ci:
            self.url = \
                f'https://{self.branch}.integrates.fluidattacks.com/new'
        else:
            self.url = 'https://localhost:8080/new'

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
        with contextlib.suppress(TimeoutException):  # User does not have existing session
            selenium = self.selenium
            continue_btn = WebDriverWait(selenium, self.delay/10).until(
                expected.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Continue')]")))
            self.__click(continue_btn)

    def __check_legal_notice(self):
        with contextlib.suppress(TimeoutException):  # User has already checked the legal notice
            selenium = self.selenium
            WebDriverWait(selenium, self.delay/10).until(
                expected.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Legal notice')]")))
            checkbox = selenium.find_element_by_xpath("//*[@name='remember']")
            self.__click(checkbox)
            accept_btn = selenium.find_element_by_xpath(
                "//*[contains(text(), 'Accept and continue')]")
            self.__click(accept_btn)

    def __click(self, element):
        self.selenium.execute_script('arguments[0].click()', element)
        time.sleep(6)

    def __login_aux(self):
        with contextlib.suppress(TimeoutException):
            selenium = self.selenium
            WebDriverWait(selenium, self.delay/10).until(
                expected.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Elegir una cuenta')]")))
            mail_suffix = [1, 2, 2][self.ci_node_index - 1]
            btn_user = selenium.find_element_by_xpath(
                f"//*[contains(text(), 'continuoushack{mail_suffix}@gmail.com')]")
            self.__click(btn_user)

    def __accept_cookies(self):
        with contextlib.suppress(TimeoutException):
            selenium = self.selenium
            WebDriverWait(selenium, self.delay/10).until(
                expected.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Allow all cookies')]")))
            accept_cookies = selenium.find_element_by_xpath(
                "//*[contains(text(), 'Allow all cookies')]")
            self.__click(accept_cookies)

    def __login(self):
        selenium = self.selenium
        selenium.get(self.url)
        if 'Allow all cookies' in selenium.page_source:
            self.__accept_cookies()
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Sign in with Microsoft')]")))
        selenium.save_screenshot(f'{SCR_PATH}00.00-init-page.png')

        # Pending to see why Azure does not work on CI
        # It works locally and manually
        text = "//*[contains(text(), 'Sign in with Google')]"
        btn_login = selenium.find_element_by_xpath(text)
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
        selenium.get(self.url + f'/orgs/okada/groups/unittesting/')
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
               (By.XPATH,
                "//*[contains(text(), 'Vulnerabilities over time')]")))
        selenium.save_screenshot(SCR_PATH + '03-01-analytics.png')
        assert 'Vulnerabilities over time' in selenium.page_source

    def test_04_findings(self):
        selenium = self.selenium
        selenium.get(self.url + f'/orgs/okada/groups/unittesting/vulns')
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'FIN.H.060. Insecure exceptions')]")))
        selenium.save_screenshot(SCR_PATH + '04-01-findings.png')
        assert 'FIN.H.060. Insecure exceptions' in selenium.page_source

    def test_05_finding(self):
        selenium = self.selenium
        selenium.get(self.url + f'/orgs/okada/groups/unittesting/vulns')
        finding_elem = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'FIN.H.060. Insecure exceptions')]")))
        selenium.save_screenshot(SCR_PATH + '05-01-finding.png')

        self.__click(finding_elem)
        description_elem = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//a[text()[contains(., 'Description')]]")))

        self.__click(description_elem)
        selenium.save_screenshot(SCR_PATH + '05-02-finding.png')
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'R359. Avoid using generic exceptions.')]")))
        selenium.save_screenshot(SCR_PATH + '05-03-finding.png')
        assert 'The source code uses generic exceptions to handle unexpected errors' in selenium.page_source

    def test_06_severity(self):
        selenium = self.selenium
        selenium.get(self.url + f'/orgs/okada/groups/unittesting/vulns')
        finding_elem = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'FIN.H.060. Insecure exceptions')]")))
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
        selenium.save_screenshot(SCR_PATH + '06-03-severity.png')
        assert 'Confidentiality Impact' in selenium.page_source

    def test_07_evidence(self):
        selenium = self.selenium
        selenium.get(self.url + f'/orgs/okada/groups/unittesting/vulns')
        finding_elem = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'FIN.H.060. Insecure exceptions')]")))
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
                (By.XPATH, "//*[contains(text(), 'exception')]")))
        selenium.save_screenshot(SCR_PATH + '07-04-evidence.png')
        assert 'exception' in selenium.page_source

    @pytest.mark.no_prod  # temporary mark
    def test_08_exploit(self):
        selenium = self.selenium
        selenium.get(self.url + f'/orgs/okada/groups/unittesting/vulns')
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
        selenium.save_screenshot(SCR_PATH + '08-03-exploit.png')
        assert 'It works' in selenium.page_source

    def test_09_tracking(self):
        selenium = self.selenium
        selenium.get(self.url + f'/orgs/okada/groups/unittesting/vulns')
        finding_elem = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'FIN.H.060. Insecure exceptions')]")))
        selenium.save_screenshot(SCR_PATH + '09-01-tracking.png')

        self.__click(finding_elem)
        tracking_elem = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//a[text()[contains(., 'Tracking')]]")))

        self.__click(tracking_elem)
        selenium.save_screenshot(SCR_PATH + '09-02-tracking.png')

        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), '2020-09-09')]")))
        selenium.save_screenshot(SCR_PATH + '09-03-tracking.png')
        assert '2020-09-09' in selenium.page_source

    def test_10_comments(self):
        selenium = self.selenium
        selenium.get(self.url + f'/orgs/okada/groups/unittesting/vulns')
        finding_elem = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'FIN.H.060. Insecure exceptions')]")))
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
        selenium.save_screenshot(SCR_PATH + '10-03-comments.png')
        assert 'oldest' in selenium.page_source

    def test_11_techpdf(self):
        selenium = self.selenium
        selenium.get(self.url + f'/orgs/okada/groups/unittesting/vulns')
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'FIN.H.060. Insecure exceptions')]")))
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
                    "//*[contains(text(), 'FIN.H.060. Insecure exceptions')]")))
        selenium.save_screenshot(SCR_PATH + '11-03-techpdf.png')
        assert 'FIN.H.060. Insecure exceptions' in selenium.page_source

    def test_13_events(self):
        selenium = self.selenium
        selenium.get(self.url + f'/orgs/okada/groups/unittesting/events')
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
        selenium.save_screenshot(SCR_PATH + '13-02-events.png')
        assert 'This is an eventuality with evidence' in selenium.page_source

    def test_14_resources(self):
        selenium = self.selenium
        selenium.get(self.url + f'/orgs/okada/groups/unittesting/scope')
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
        selenium.save_screenshot(SCR_PATH + '14-02-resources.png')
        self.__cancel_modal()

        add_envs = selenium.find_element_by_xpath(
            '//*[@id="resources"]/div[3]/div[2]/div/button')
        self.__click(add_envs)
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Add environment')]")))
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
        selenium.save_screenshot(SCR_PATH + '14-05-resources.png')
        self.__cancel_modal()

        add_tags = selenium.find_element_by_xpath(
            '//*[@id="resources"]/div[7]/div[2]/div/button[1]')
        self.__click(add_tags)
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Add tags')]")))
        selenium.save_screenshot(SCR_PATH + '14-06-resources.png')
        self.__cancel_modal()

        selenium.execute_script('window.scrollTo(680, 980);')
        selenium.save_screenshot(SCR_PATH + '14-07-resources.png')

        total_tables = len(selenium.find_elements_by_tag_name("table"))
        assert total_tables == 5
        assert 'https://fluidattacks.com' in selenium.page_source

    def test_15_project_comments(self):
        selenium = self.selenium
        selenium.get(self.url + f'/orgs/okada/groups/unittesting/consulting')
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                 "//*[contains(text(), 'Now we can post comments on projects')]")))
        selenium.save_screenshot(SCR_PATH + '15-01-proj_comments.png')
        assert 'Now we can post comments on projects' in selenium.page_source

    def test_16_forces(self):
        selenium = self.selenium
        selenium.get(
            self.url + f'/orgs/okada/groups/unittesting/devsecops')
        time.sleep(3.0)
        selenium.save_screenshot(SCR_PATH + '16.01-forces-executions.png')

        if self.branch == 'master':
            assert 'There is no data to display' in selenium.page_source
        else:
            forces_elem = WebDriverWait(selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH, "//td[contains(text(),'08c1e735a73243f2ab1ee0757041f80e')]")))
            selenium.save_screenshot(SCR_PATH + '16.02-forces-executions.png')

            forces_elem.click()
            WebDriverWait(selenium, self.delay).until(
                expected.presence_of_element_located(
                    (By.XPATH, "//p[contains(text(),'Vulnerable')]")))
            selenium.save_screenshot(SCR_PATH + '16.03-forces-execution-modal.png')

            log_element = selenium.find_element_by_xpath(
                '//*[@id="forcesExecutionLogTab"]/a')
            self.__click(log_element)
            assert 'findings' in selenium.page_source

    # Temporarily disabled while we grant a user access to this project
    def _test_17_pending_to_delete(self):
        selenium = self.selenium

        selenium.get(self.url + f'/orgs/okada/groups/pendingproject')
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Cancel group deletion')]")))
        selenium.save_screenshot(SCR_PATH + '17-02-pending_to_delete.png')
        assert 'Group pending to delete' in selenium.page_source

        selenium.get(self.url + f'/orgs/okada/groups/pendingproject/vulns')
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Cancel group deletion')]")))
        selenium.save_screenshot(SCR_PATH + '17-03-pending_to_delete.png')
        assert 'Group pending to delete' in selenium.page_source


    def test_18_tag_indicators(self):
        selenium = self.selenium

        selenium.get(
            self.url + f'/orgs/okada/portfolios/test-projects/indicators')
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Severity')]")))
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

        assert 'Open vulnerabilities by group' in selenium.page_source
        assert 'Findings by group' in selenium.page_source
        assert 'Open findings by group' in selenium.page_source
        assert 'Mean time to remediate' in selenium.page_source
        assert 'remediated' in selenium.page_source
        assert 'Status' in selenium.page_source
        assert 'Treatment' in selenium.page_source
        assert 'Treatmentless by group' in selenium.page_source

        selenium.get(
            self.url + f'/orgs/okada/portfolios/test-projects/groups')
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Description')]")))
        selenium.save_screenshot(SCR_PATH + '18-08-tag_groups.png')
        total_tables = len(selenium.find_elements_by_tag_name("table"))
        assert total_tables == 1

        selenium.get(
            self.url + f'/orgs/okada/portfolios/doesnotexists/groups')
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Vulnerabilities over time')]")))
        selenium.save_screenshot(SCR_PATH + '18-09-tag_indicators.png')

    def test_19_finding_reattack_vulns(self):
        selenium = self.selenium
        selenium.get(self.url + f'/orgs/okada/groups/unittesting/vulns')
        finding_elem = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'FIN.H.060. Insecure exceptions')]")))
        selenium.save_screenshot(SCR_PATH + '19-01-finding_vuln.png')

        self.__click(finding_elem)
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'test/data/lib_path/f060/csharp.cs')]")))
        selenium.save_screenshot(SCR_PATH + '19-02-finding_vuln.png')

        verify_btn = selenium.find_element_by_xpath(
            '//*/button[text()[contains(., "Reattack")]]')
        self.__click(verify_btn)
        selenium.save_screenshot(SCR_PATH + '19-03-finding_vuln.png')

        checkboxes = selenium.find_elements_by_css_selector("#linesVulns input[type='checkbox']")
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                self.__click(checkbox)
        time.sleep(2)
        selenium.save_screenshot(SCR_PATH + '19-04-finding_vuln.png')

        reattack_vulns = selenium.find_element_by_xpath(
            '//*/button[text()[contains(., "Reattack")]]')
        self.__click(reattack_vulns)
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Justification')]")))
        selenium.save_screenshot(SCR_PATH + '19-05-finding_vuln.png')

        modal_btn = selenium.find_element_by_xpath(
            '//*/button[text()[contains(., "Cancel")]]')
        self.__click(modal_btn)
        time.sleep(1)
        selenium.execute_script('window.scrollTo(0, 0);')

        assert 'test/data/lib_path/f060/csharp.cs' in selenium.page_source

    def test_20_finding_edit_vulns(self):
        selenium = self.selenium
        selenium.get(self.url + f'/orgs/okada/groups/unittesting/vulns')
        finding_elem = WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'FIN.H.060. Insecure exceptions')]")))

        selenium.save_screenshot(SCR_PATH + '20-01-finding_vuln.png')

        self.__click(finding_elem)
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH,
                    "//*[contains(text(), 'test/data/lib_path/f060/csharp.cs')]")))

        selenium.save_screenshot(SCR_PATH + '20-02-finding_vuln.png')

        edit_btn = selenium.find_element_by_xpath(
            '//*/button[text()[contains(., "Edit")]]')
        self.__click(edit_btn)
        selenium.save_screenshot(SCR_PATH + '20-03-finding_vuln.png')

        checkboxes = selenium.find_elements_by_css_selector("#linesVulns input[type='checkbox']")
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                self.__click(checkbox)
        time.sleep(2)
        selenium.save_screenshot(SCR_PATH + '20-04-finding_vuln.png')

        selenium.execute_script('window.scrollTo(0, 580);')
        edit_vulns = selenium.find_element_by_xpath(
            '//*/button[text()[contains(., "Edit vulnerabilities")]]')
        self.__click(edit_vulns)
        WebDriverWait(selenium, self.delay).until(
            expected.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'External BTS')]")))
        selenium.save_screenshot(SCR_PATH + '20-05-finding_vuln.png')

        modal_btn = selenium.find_element_by_xpath(
            '//*/button[text()[contains(., "Close")]]')
        self.__click(modal_btn)
        time.sleep(1)
        selenium.execute_script('window.scrollTo(0, 0);')

        assert 'test/data/lib_path/f060/csharp.cs' in selenium.page_source
