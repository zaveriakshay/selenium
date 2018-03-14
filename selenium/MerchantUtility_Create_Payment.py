#!/usr/bin/python
# -*- coding: utf-8 -*-
# from suds.client import Client
# url="http://94.200.29.187:5115/paymentZone/PaymentService/Payment?WSDL"
# client = Client(url)
# print (client)
from localselenium.wrapper.UserControl import *
from Read_XML import xmlObject
from AppConstants import *


def merchantUtilityPaymentEnterAmount(browser, amount):
    fillTextFieldById(browser, "amount", amount)


def merchantUtilitySelectMerchant(browser, merchant):
    selectDropDownByIdAndOptionValue(browser, "merchantID", merchant)


def merchantUtilityPaymentSubmit(browser):
    clickButtonByXpath(browser, "//input[@type='submit' and @value='Generate Payment']")
    print("merchant page was submit")


def handleResponse(responseXML, rowIndex, writeSheet):
    try:
        xmlInstance = xmlObject(responseXML)
        writeSheet.write(rowIndex, RESPONSE_XML, responseXML)
        errorCode = xmlInstance.findAllByXPath('Body/SrvRes/ExceptionDetails/ErrorCode')
        writeSheet.write(rowIndex, PAYMENT_ERROR_CODE, errorCode)
        transactionRef = xmlInstance.findAllByXPath('Body/SrvRes/NormalPayRes/Transfer/TransactionRefNo')
        writeSheet.write(rowIndex, NOQODI_REF, transactionRef)
    except:
        pass
