#!/usr/bin/env python3

"""
Script that uses Selenium to automate the generation of
of Formstack backups
"""
from __future__ import absolute_import
import os
import requests
import boto3
import rotate_fs_keys as fs_func
from datetime import datetime
from botocore.exceptions import ClientError
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

CLIENT_S3 = boto3.client('s3',
                         aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                         aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
BUCKET_S3 = os.environ['FS_S3_BUCKET_NAME']


def get_auth_cookie(browser):
    """
    Gets the value of Formstack auth cookie

    :param browser: Selenium object that contains the session information
    """
    cookies = browser.get_cookies()
    auth_cookie = {}
    for cookie in cookies:
        cookie_form = cookie.get('name')
        if cookie_form == 'FormSpringAuth':
            auth_cookie = {'FormSpringAuth': cookie.get('value')}
            break
        else:
            pass
    return auth_cookie

def browser_navigate_href(browser, xpath):
    """
    Allows the browser to navigate the website by finding href attributes

    :param browser: Selenium object that contains the session information
    :param xpath: Path of a HTML link element
    """
    success = False
    attempts = 0
    file_url = ''
    while not success and attempts < 120:
        try:
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            file_url = browser.find_element_by_xpath(xpath).get_attribute('href')
            success = True
        except TimeoutException:
            attempts += 10
            browser.implicitly_wait(10)
    if not success:
        raise TimeoutException
    else:
        return file_url

def download_file(browser, file_name):
    """
    Allows the browser to download a a file
    :param browser: Selenium object that contains the session information
    :param file_name: Name of the file to download
    """
    auth_cookie = get_auth_cookie(browser)
    file_url = browser_navigate_href(browser, '//fs-btn/a[contains(@href,\"download\")]')
    response = requests.get(file_url, cookies=auth_cookie)
    file_route = '/tmp/' + file_name
    try:
        with open(file_route, 'wb') as f:
            f.write(response.content)
            return True
    except (OSError, IOError):
        return False

def upload_file(browser, form_name, file_name):
    """
    Upload a file to s3 bucket
    :param browser: Selenium object that contains the session information
    :param file_name: Name of the file to upload
    """
    file_route = '/tmp/' + file_name
    file_folder = 'formsbackup/{form_name}/{file_name}'\
        .format(form_name=form_name, file_name=file_name)
    with open(file_route, 'rb') as file_obj:
        try:
            CLIENT_S3.upload_fileobj(file_obj, BUCKET_S3, file_folder)
            return True
        except ClientError:
            return False

def delete_old_exports(browser, xpath):
    """
    Delete old exports of a form

    :param browser: Selenium object that contains the session information
    :param xpath: Path of a HTML link element
    """
    try:
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
        try:
            browser.find_element_by_xpath('//fs-container/div[contains(@class, \"fs-container2--collapsed\")]')
            fs_func.browser_navigate_xpath(browser, xpath)
            old_exports = browser.find_elements_by_xpath('//fs-btn/a[contains(@href,\"download\")]')
            for i in old_exports:
                fs_func.browser_navigate_xpath(browser, '//div/fs-icon[contains(@class, \"fs-icon-trash\")]')
        except NoSuchElementException:
            pass
    except TimeoutException:
        pass

def browser_popup_navigate(browser, xpath):
    """
    Navigate thought popup menu in Formstack to click a button

    :param browser: Selenium object that contains the session information
    :param xpath: Path of a HTML link element
    """
    WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    browser.find_element_by_xpath(xpath).click()

def formstack_backup(form_name):
    """
    Navigates to the Formstack API page
    """
    browser = fs_func.browser_initialize('https://www.formstack.com/admin/user/login?redirect=/account/dashboard')
    fs_func.browser_login(browser, 'email', 'password', 'submit')
    fs_func.browser_navigate_link(browser, form_name)
    fs_func.browser_navigate_xpath(browser, '//a/span[text()=\"Submissions\"]')
    delete_old_exports(browser, '//div/span[contains(text(), \"Exporting Submissions\")]')
    fs_func.browser_navigate_xpath(browser, '//submissions-export-all')
    fs_func.browser_navigate_xpath(browser, '//ul/li/span[contains(text(), \"to CSV\")]')
    browser_popup_navigate(browser, '//a/div/p[contains(text(), \"Export All Submissions in Filter\")]')
    date = datetime.now().strftime('%Y%m%d')
    form_name = form_name.replace(' ', '')
    file_name = '{file_name}_{date}.csv'.format(file_name=form_name, date=date)
    file_downloaded = download_file(browser, file_name)
    if file_downloaded:
        fs_func.browser_navigate_xpath(browser, '//div/fs-icon[contains(@class, \"fs-icon-trash\")]')
        uploaded_file = upload_file(browser, form_name, file_name)
    else:
        uploaded_file = False
    fs_func.browser_formstack_logout(browser)
    return uploaded_file

if __name__ == '__main__':
    form = 'Hallazgos'
    backup_uploaded = formstack_backup(form)
    if backup_uploaded:
        print('Backup of {form} form was generated'.format(form=form))
    else:
        print('Backup of {form} form failed'.format(form=form))
