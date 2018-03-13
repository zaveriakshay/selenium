#!/usr/bin/python
# -*- coding: utf-8 -*-
# from suds.client import Client
# url="http://94.200.29.187:5115/paymentZone/PaymentService/Payment?WSDL"
# client = Client(url)
# print (client)
from localselenium.wrapper.UserControl import *

from MerchantUtility_Create_Payment import *
from Read_XML import xmlObject


def makeUnregisteredCCDPayment(browser, rowIndex, readSheet, writeSheet):
    loadURL(browser, "https://www.testepg.ae/merchantUtility/PaymentForm.jsp")
    merchantUtilitySelectMerchant(browser, readSheet.cell(rowIndex, 1).value)
    merchantUtilityPaymentEnterAmount(browser, readSheet.cell(rowIndex, 2).value)
    merchantTxnId = findInputValueById(browser, "txnID")
    writeSheet.write(rowIndex, 3, merchantTxnId)
    merchantUtilityPaymentSubmit(browser)
    clickHrefId(browser, "paymentForm:ccdPmtLink");
    fillTextFieldById(browser, "paymentForm:ccdNumber", readSheet.cell(rowIndex, 8).value)
    fillTextFieldById(browser, "paymentForm:ccdHolderName", readSheet.cell(rowIndex, 11).value)
    selectDropDownByIdAndOptionValue(browser, "paymentForm:ccdExpiryDateMM", readSheet.cell(rowIndex, 9).value)
    clickCheckBoxById(browser, "paymentForm:ccdTerms")
    selectDropDownByIdAndOptionValue(browser, "paymentForm:ccdExpiryDateYYYY", readSheet.cell(rowIndex, 10).value)
    fillTextFieldById(browser, "paymentForm:ccdCVV", readSheet.cell(rowIndex, 12).value)
    fillTextFieldById(browser, "paymentForm:ccdEmail", readSheet.cell(rowIndex, 13).value)
    fillTextFieldById(browser, "paymentForm:ccdPaymentDetails", readSheet.cell(rowIndex, 7).value)
    clickButtonById(browser, "paymentForm:payNow")
    waitForURL(browser, "bne-stripe2.ap.gateway.mastercard.com/acs/MastercardACS")
    clickButtonByXpath(browser, "//input[@type='submit' and @value='Submit']")
    waitForURL(browser, "merchantUtility/NPayResponse.jsp")
    responseXML = findInputValueByClassName(browser, "input-xxlarge")
    xmlInstance = xmlObject(responseXML)
    transactionRef = xmlInstance.findAllByXPath('Body/SrvRes/NormalPayRes/Transfer/TransactionRefNo')
    writeSheet.write(rowIndex, 17, transactionRef)
    writeSheet.write(rowIndex, 18, responseXML)


'''browser = createBrowser()
makeUnregisteredCCDPayment(browser)
'''
