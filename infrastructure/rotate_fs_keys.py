#!/usr/bin/env python3

import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def browser_initialize(url):
    browser = webdriver.Firefox()
    browser.get(url)
    return browser

def browser_login(browser, login_id, pass_id, submit_id):
    fs_login = os.environ['FORMSTACK_EMAIL']
    fs_pass = os.environ['FORMSTACK_PASS']
    browser_write_element_by_id(browser, login_id, fs_login)
    browser_write_element_by_id(browser, pass_id, fs_pass)
    browser.find_element_by_id(submit_id).click()

def browser_logout(browser):
    open_formstack_profile_menu(browser)
    browser_navigate_link(browser, 'Logout')
    browser.close()

def browser_navigate_link(browser, link_text):
    browser.find_element_by_link_text(link_text).click()

def browser_write_element_by_id(browser, elem_id, text):
    field = browser.find_element_by_id(elem_id)
    field.clear()
    field.send_keys(text)

def create_token(browser, num):
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

def generate_formstack_tokens(num):
    browser = browser_initialize('https://www.formstack.com/admin/user/login?redirect=/account/dashboard')
    browser_login(browser, 'email', 'password', 'submit')
    open_formstack_profile_menu(browser)
    browser_navigate_link(browser, 'API')
    tokens = [create_token(browser, x) for x in list(range(num))]
    browser_logout(browser)
    return tokens

def get_token(browser, name):
    href = browser.find_element_by_link_text(name).get_attribute('href')
    token_id = href.split('/')[-1]
    return browser.find_element_by_id('app-token-' + token_id).text

def open_formstack_profile_menu(browser):
    xpath = '//a[@aria-label=\"Account Menu\"]'
    WebDriverWait(browser, 10).until(EC.invisibility_of_element_located((By.ID, 'message')))
    browser.find_element_by_xpath(xpath).click()

if __name__ == '__main__':
    NUM_TOKENS = 6
    FORMSTACK_TOKENS = generate_formstack_tokens(NUM_TOKENS)
