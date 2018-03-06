#!/usr/bin/python
# -*- coding: utf-8 -*-
# from suds.client import Client
# url="http://94.200.29.187:5115/paymentZone/PaymentService/Payment?WSDL"
# client = Client(url)
# print (client)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from localselenium.wrapper.UserControl import *


def merchantUtilityPaymentEnterAmount(browser, amount):
    fillTextFieldById(browser, "amount", amount)


def merchantUtilitySelectMerchant(browser, merchant):
    selectDropDownByIdAndOptionValue(browser, "merchantID", merchant)


def merchantUtilityPaymentSubmit(browser):
    clickButtonByXpath(browser, "//input[@type='submit' and @value='Generate Payment']")
    print("merchant page was submit")
