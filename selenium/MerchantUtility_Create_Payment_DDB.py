#!/usr/bin/python
# -*- coding: utf-8 -*-
# from suds.client import Client
# url="http://94.200.29.187:5115/paymentZone/PaymentService/Payment?WSDL"
# client = Client(url)
# print (client)
from localselenium.wrapper.UserControl import *

from MerchantUtility_Create_Payment import *
from Read_XML import xmlObject
from AppConstants import  *


def makeDDBPayment(browser, rowIndex, readSheet, writeSheet):
    loadURL(browser, HOST+"/PaymentForm.jsp")
    merchantUtilitySelectMerchant(browser, readSheet.cell(rowIndex, MERCHANT_CODE).value)
    merchantUtilityPaymentEnterAmount(browser, readSheet.cell(rowIndex, PAYMENT_AMOUNT).value)
    merchantTxnId = findInputValueById(browser, "txnID")
    writeSheet.write(rowIndex, MERCHANT_REF, merchantTxnId)
    merchantUtilityPaymentSubmit(browser)
    clickHrefId(browser, "paymentForm:netBankPmtLink");
    selectDropDownByIdAndOptionValue(browser, "paymentForm:ddbBank", readSheet.cell(rowIndex, DDB_BANK).value)
    clickCheckBoxById(browser, "paymentForm:ddbTerms")
    fillTextFieldById(browser, "paymentForm:ddbName", readSheet.cell(rowIndex, DDB_NAME).value)
    fillTextFieldById(browser, "paymentForm:ddbEmail", readSheet.cell(rowIndex, DDB_EMAIL).value)
    fillTextFieldById(browser, "paymentForm:ddbPaymentDetails", readSheet.cell(rowIndex, PAYMENT_REMARKS).value)
    clickButtonById(browser, "paymentForm:payNow")
    '''waitForURL(browser, "bne-stripe2.ap.gateway.mastercard.com/acs/MastercardACS")
    clickButtonByXpath(browser, "//input[@type='submit' and @value='Submit']")
    waitForURL(browser, "merchantUtility/NPayResponse.jsp")'''
    responseXML = findInputValueByClassName(browser, "input-xxlarge")
    handleResponse(responseXML, rowIndex, writeSheet)


'''browser = createBrowser()
makeECAPayment(browser)'''
