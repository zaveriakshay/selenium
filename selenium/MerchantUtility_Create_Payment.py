#!/usr/bin/python
# -*- coding: utf-8 -*-
# from suds.client import Client
# url="http://94.200.29.187:5115/paymentZone/PaymentService/Payment?WSDL"
# client = Client(url)
# print (client)
from AppConstants import *
from Read_Excel import Payment
from Read_Excel import Refund
from Read_XML import xmlObject
from UserControl import *


def merchantUtilityPaymentEnterAmount(browser, amount):
    fillTextFieldById(browser, "amount", amount)


def merchantUtilitySelectMerchant(browser, merchant):
    selectDropDownByIdAndOptionValue(browser, "merchantID", merchant)


def merchantUtilityPaymentSubmit(browser):
    clickButtonByXpath(browser, "//input[@type='submit' and @value='Generate Payment']")
    print("merchant page was submit")


def fillBeneDetails(browser, payment: Payment):
    if payment.isBene == "true":
        clickCheckBoxById(browser, "beneEnable")
        count = 1;
        buttonCount = 0;
        for key in payment.beneficiaryList:
            if count % 2 == 0:
                buttonCount = buttonCount + 1
                clickButtonById(browser, "btnAddBen" + str(buttonCount))
            count = count + 1
        count = 1;
        for key in payment.beneficiaryList:
            fillTextFieldById(browser, key, payment.beneficiaryList[key])
            count = count + 1

def fillBeneDetails(browser, refund: Refund):
    if refund.isBene == "true":
        clickCheckBoxById(browser, "beneEnable")
        count = 1;
        buttonCount = 0;
        for key in refund.beneficiaryList:
            if count % 2 == 0:
                buttonCount = buttonCount + 1
                clickButtonById(browser, "btnAddBen" + str(buttonCount))
            count = count + 1
        count = 1;
        for key in refund.beneficiaryList:
            fillTextFieldById(browser, key, refund.beneficiaryList[key])
            count = count + 1

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
        if errorCode == "EPG-PMT-000":
            transactionRef = xmlInstance.findAllByXPath('Body/SrvRes/NormalPayRes/Transfer/TransactionRefNo')
            payment.noqodiRef = transactionRef
    except:
        pass
