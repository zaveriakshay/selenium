from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select

def pauseForSeconds(seconds):
    time.sleep(seconds)

def fillTextFieldById(browser, id, value):
    print("fillTextFieldById:in:" + id + ":" + value)
    global elem
    elem = browser.find_element_by_id(id)
    elem.clear()
    elem.send_keys(value)
    print("fillTextFieldById:out")


def selectDropDownByIdAndOptionValue(browser, id, value):
    print("selectDropDownByIdAndOptionValue:in:" + id + ":" + value)
    global select
    select = Select(browser.find_element_by_id(id))
    select.select_by_value(value)
    print("selectDropDownByIdAndOptionValue:out")


def clickCheckBoxById(browser, id):
    print("selectCheckBoxById:in:" + id)
    pauseForSeconds(2)
    browser.find_element_by_id(id).click()
    print("selectCheckBoxById:out:")


def clickRadioButtonById(browser, id):
    print("clickRadioButtonById:in:" + id)
    browser.find_element_by_id(id).click()
    print("clickRadioButtonById:out:")


def clickButtonById(browser, id):
    print("clickButtonById:in:" + id)
    browser.find_element_by_id(id).click()
    print("clickButtonById:out:")


def clickButtonByXpath(browser, xPath):
    print("clickButtonByXpath:in:" + xPath)
    browser.find_element_by_xpath(xPath).click()
    print("clickButtonByXpath:out:")


def waitForURL(browser, waitOnThisURL):
    print("waitForURL:in:" + waitOnThisURL)
    while True:
        pauseForSeconds(3)
        if waitOnThisURL not in browser.current_url:
            print(browser.current_url)
        elif waitOnThisURL in browser.current_url:
            print(browser.current_url)
            break


def createBrowser():
    browser = webdriver.Chrome(
        r"resources\selenium\webdriver\chrome\x86\chromedriver.exe")
    return browser


def loadURL(browser, url):
    browser.get(url)


def clickHrefId(browser, id):
    print("clickHrefId:in:" + id)
    pauseForSeconds(2)
    browser.find_element_by_id(id).click()
    print("clickHrefId:out:")


def findInputValueById(browser, id):
    print("findInputValueByXPath:in:" + ":" + id)
    inputElement = browser.find_element_by_id(id)
    value = inputElement.get_attribute('value')
    print("findInputValueByXPath:out:" + ":" + value)
    return value


def findInputValueByXPath(browser, xPath):
    print("findInputValueByXPath:in:" + ":" + xPath)
    inputElement = browser.find_element_by_xpath(xPath)
    value = inputElement.get_attribute('value')
    print("findInputValueByXPath:out:" + ":" + value)
    return value


def findInputValueByCssSelector(browser, cssSelector):
    print("findInputValueByCssSelector:in:" + ":" + cssSelector)
    inputElement = browser.find_element_by_css_selector(cssSelector)
    value = inputElement.get_attribute('value')
    print("findInputValueByCssSelector:out:" + ":" + value)
    return value


def findInputValueByClassName(browser, className):
    print("findInputValueByClassName:in:" + ":" + className)
    inputElement = browser.find_element_by_class_name(className)
    value = inputElement.get_attribute('value')
    print("findInputValueByClassName:out:" + ":" + value)
    return value
