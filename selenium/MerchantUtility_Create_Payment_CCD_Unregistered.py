#!/usr/bin/python
# -*- coding: utf-8 -*-
# from suds.client import Client
# url="http://94.200.29.187:5115/paymentZone/PaymentService/Payment?WSDL"
# client = Client(url)
# print (client)
from UserControl import *

from MerchantUtility_Create_Payment import *
from Read_XML import xmlObject
from AppConstants import *


def makeUnregisteredCCDPayment(browser, rowIndex, readSheet, writeSheet):
    loadURL(browser, HOST + "/PaymentForm.jsp")
    merchantUtilitySelectMerchant(browser, readSheet.cell(rowIndex, MERCHANT_CODE).value)
    merchantUtilityPaymentEnterAmount(browser, readSheet.cell(rowIndex, PAYMENT_AMOUNT).value)
    merchantTxnId = findInputValueById(browser, "txnID")
    writeSheet.write(rowIndex, MERCHANT_REF, merchantTxnId)
    merchantUtilityPaymentSubmit(browser)
    clickHrefId(browser, "paymentForm:ccdPmtLink");
    fillTextFieldById(browser, "paymentForm:ccdNumber", readSheet.cell(rowIndex, CCD_NUMBER).value)
    fillTextFieldById(browser, "paymentForm:ccdHolderName", readSheet.cell(rowIndex, CCD_HOLDER_NAME).value)
    selectDropDownByIdAndOptionValue(browser, "paymentForm:ccdExpiryDateMM", readSheet.cell(rowIndex, CCD_MONTH).value)
    clickCheckBoxById(browser, "paymentForm:ccdTerms")
    selectDropDownByIdAndOptionValue(browser, "paymentForm:ccdExpiryDateYYYY", readSheet.cell(rowIndex, CCD_YEAR).value)
    fillTextFieldById(browser, "paymentForm:ccdCVV", readSheet.cell(rowIndex, CCD_CVV).value)
    fillTextFieldById(browser, "paymentForm:ccdEmail", readSheet.cell(rowIndex, CCD_EMAIL).value)
    fillTextFieldById(browser, "paymentForm:ccdPaymentDetails", readSheet.cell(rowIndex, PAYMENT_REMARKS).value)
    clickButtonById(browser, "paymentForm:payNow")
    waitForURL(browser, "ap.gateway.mastercard.com/acs/MastercardACS")
    clickButtonByXpath(browser, "//input[@type='submit' and @value='Submit']")
    waitForURL(browser, "merchantUtility/NPayResponse.jsp")
    responseXML = findInputValueByClassName(browser, "input-xxlarge")
    handleResponse(responseXML, rowIndex, writeSheet)


def makeUnregisteredCCDPayment(browser, payment: Payment):
    loadURL(browser, HOST + "/PaymentForm.jsp")
    merchantUtilitySelectMerchant(browser, payment.merchantCode)
    merchantUtilityPaymentEnterAmount(browser, payment.paymentAmount)
    fillBeneDetails(browser, payment)
    merchantTxnId = findInputValueById(browser, "txnID")
    payment.merchantRef = merchantTxnId
    merchantUtilityPaymentSubmit(browser)
    clickHrefId(browser, "paymentForm:ccdPmtLink");
    fillTextFieldById(browser, "paymentForm:ccdNumber", payment.ccdNumber)
    fillTextFieldById(browser, "paymentForm:ccdHolderName", payment.ccdHolderName)
    selectDropDownByIdAndOptionValue(browser, "paymentForm:ccdExpiryDateMM", payment.ccdExpiryMonth)
    clickCheckBoxById(browser, "paymentForm:ccdTerms")
    selectDropDownByIdAndOptionValue(browser, "paymentForm:ccdExpiryDateYYYY", payment.ccdExpiryYear)
    fillTextFieldById(browser, "paymentForm:ccdCVV", payment.ccdCvv)
    fillTextFieldById(browser, "paymentForm:ccdEmail", payment.ccdEmail)
    fillTextFieldById(browser, "paymentForm:ccdPaymentDetails", payment.paymentRemark)
    clickButtonById(browser, "paymentForm:payNow")
    waitForURL(browser, "ap.gateway.mastercard.com/acs/MastercardACS")
    clickButtonByXpath(browser, "//input[@type='submit' and @value='Submit']")
    waitForURL(browser, "merchantUtility/NPayResponse.jsp")
    responseXML = findInputValueByClassName(browser, "input-xxlarge")
    handleResponse(responseXML, payment)
