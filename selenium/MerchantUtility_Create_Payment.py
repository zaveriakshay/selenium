#!/usr/bin/python
# -*- coding: utf-8 -*-
# from suds.client import Client
# url="http://94.200.29.187:5115/paymentZone/PaymentService/Payment?WSDL"
# client = Client(url)
# print (client)
from AppConstants import *
from Read_Excel import Payment
from Read_XML import xmlObject
from localselenium.wrapper.UserControl import *


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


def handleResponse(responseXML, payment: Payment):
    try:
        xmlInstance = xmlObject(responseXML)
        payment.paymentResponseXML = responseXML
        errorCode = xmlInstance.findAllByXPath('Body/SrvRes/ExceptionDetails/ErrorCode')
        payment.paymentErrorCode = errorCode
        transactionRef = xmlInstance.findAllByXPath('Body/SrvRes/NormalPayRes/Transfer/TransactionRefNo')
        payment.noqodiRef = transactionRef
    except:
        pass
