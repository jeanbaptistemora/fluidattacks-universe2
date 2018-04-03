from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

driver = webdriver.Remote(command_executor='http://192.168.200.101:4444/wd/hub',\
desired_capabilities=DesiredCapabilities.CHROME)
driver.get("https://192.168.200.100.xip.io:8000/")
driver.find_element_by_link_text("Log in with Google").click()
driver.find_element_by_id("identifierId").clear()
driver.find_element_by_id("identifierId").send_keys("continuoushacking@gmail.com")
driver.find_element_by_css_selector("#identifierNext > content.CwaK9").click()
time.sleep(20)
driver.find_element_by_name("password").click()
driver.find_element_by_name("password").send_keys("integratesbyfluidattacks")
driver.find_element_by_css_selector("#passwordNext > content.CwaK9").click()
time.sleep(40)
driver.find_element_by_xpath("//table[@id='myProjectsTbl']/tbody/tr/td[2]").click()
time.sleep(40)
driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
driver.find_element_by_css_selector("button.btn.btn-danger").click()
all_windows = driver.window_handles
time.sleep(10)

driver.switch_to.window(all_windows[-1])

driver.quit()
