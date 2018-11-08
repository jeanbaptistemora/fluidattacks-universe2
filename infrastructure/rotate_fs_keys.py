#!/usr/bin/env python3

"""
Script that uses Selenium to automate the generation and deletion
of Formstack Tokens necessary to communicate with the API
"""

import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

NUM_TOKENS = 12

def browser_initialize(url):
    """
    Starts a Firefox browser in the defined URL in headless mode

    :param url: URL to load once the browser starts
    """
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    browser = webdriver.Firefox(firefox_options=options)
    browser.get(url)
    return browser

def browser_get_api_page():
    """
    Navigates to the Formstack API page
    """
    browser = browser_initialize('https://www.formstack.com/admin/user/login?redirect=/account/dashboard')
    browser_login(browser, 'email', 'password', 'submit')
    open_formstack_profile_menu(browser)
    browser_navigate_link(browser, 'API')
    return browser

def browser_login(browser, login_id, pass_id, submit_id):
    """
    Performs a login by filling the respective form with credentials
    taken from the environment

    :param browser: Selenium object that contains the session information
    :param login_id: ID of the HTML input element for the login
    :param pass_id: ID of the HTML input element for the password
    :param submit_id: ID of the HTML input element used to submit the form
    """
    fs_login = os.environ['FORMSTACK_EMAIL']
    fs_pass = os.environ['FORMSTACK_PASS']
    browser_write_element_by_id(browser, login_id, fs_login)
    browser_write_element_by_id(browser, pass_id, fs_pass)
    browser.find_element_by_id(submit_id).click()

def browser_formstack_logout(browser):
    """
    Finish the browser session with Formstack

    :param browser: Selenium object that contains the session information
    """
    open_formstack_profile_menu(browser)
    browser_navigate_link(browser, 'Logout')
    browser.close()

def browser_navigate_link(browser, link_text):
    """
    Allows the browser to navigate the website by finding and clicking
    links

    :param browser: Selenium object that contains the session information
    :param link_text: Text of an HTML link element
    """
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.LINK_TEXT, link_text)))
    browser.find_element_by_link_text(link_text).click()

def browser_write_element_by_id(browser, elem_id, text):
    """
    Enter text in an HTML element located by its ID

    :param browser: Selenium object that contains the session information
    :param elem_id: ID of the HTML element where the text is going to be input
    :param text: Text to the be input in the HTML element
    """
    field = browser.find_element_by_id(elem_id)
    field.clear()
    field.send_keys(text)

def create_token(browser, num):
    """
    Creates a Formstack token based on the current date

    :param browser: Selenium object that contains the session information
    :param num: Queue number of the token to be created
    """
    date = datetime.now().strftime('%Y%m%d')
    token_name = 'Integrates' + str(num) + '.' + date
    redirect_uri = 'https://fluidattacks.com'
    description = 'Integrates Formstack Token'
    browser_navigate_link(browser, 'New Application')
    browser_write_element_by_id(browser, 'name', token_name)
    browser_write_element_by_id(browser, 'redirect_uri', redirect_uri)
    browser_write_element_by_id(browser, 'description', description)
    browser.find_element_by_xpath('//input[@value=\"Create Application\"]').click()
    return get_token(browser, token_name)

def delete_formstack_tokens():
    """
    Schedules the deletion of Formstack tokens
    """
    browser = browser_get_api_page()
    [delete_token(browser, x) for x in list(range(NUM_TOKENS))]
    browser_formstack_logout(browser)
    print('Tokens erased successfully!')

def delete_token(browser, num):
    """
    Deletes a Formstack token based on the date of the previous day

    :param browser: Selenium object that contains the session information
    :param num: Queue number of the token to be deleted
    """
    yesterday_date = (datetime.now() - timedelta(1)).strftime('%Y%m%d')
    token_name = 'Integrates' + str(num) + '.' + yesterday_date
    browser_navigate_link(browser, token_name)
    browser_navigate_link(browser, 'Delete')
    WebDriverWait(browser, 10).until(EC.alert_is_present())
    Alert(browser).accept()

def generate_formstack_tokens():
    """
    Schedules the creation of Formstack tokens
    """
    browser = browser_get_api_page()
    tokens = [create_token(browser, x) for x in list(range(NUM_TOKENS))]
    browser_formstack_logout(browser)
    return ','.join(map(str, tokens))

def get_token(browser, name):
    """
    Gets the value of a Formstack token by its name

    :param browser: Selenium object that contains the session information
    :param name: Token name
    """
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.LINK_TEXT, name)))
    href = browser.find_element_by_link_text(name).get_attribute('href')
    token_id = href.split('/')[-1]
    return browser.find_element_by_id('app-token-' + token_id).text

def open_formstack_profile_menu(browser):
    """
    Opens the dropdown menu in Formstack to view the Account Information

    :param browser: Selenium object that contains the session information
    """
    xpath = '//a[@aria-label=\"Account Menu\"]'
    WebDriverWait(browser, 10).until(EC.invisibility_of_element_located((By.ID, 'message')))
    browser.find_element_by_xpath(xpath).click()

if __name__ == '__main__':
    FORMSTACK_TOKENS = generate_formstack_tokens()
    print(FORMSTACK_TOKENS)
