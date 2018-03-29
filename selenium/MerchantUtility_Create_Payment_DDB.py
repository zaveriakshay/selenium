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


def makeDDBPayment(browser, rowIndex, readSheet, writeSheet):
    loadURL(browser, HOST + "/PaymentForm.jsp")
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
    responseXML = findInputValueByClassName(browser, "input-xxlarge")
    handleResponse(responseXML, rowIndex, writeSheet)


def makeDDBPayment(browser, payment: Payment):
    loadURL(browser, HOST + "/PaymentForm.jsp")
    merchantUtilitySelectMerchant(browser, payment.merchantCode)
    merchantUtilityPaymentEnterAmount(browser, payment.paymentAmount)
    fillBeneDetails(browser, payment)
    merchantTxnId = findInputValueById(browser, "txnID")
    payment.merchantRef = merchantTxnId
    merchantUtilityPaymentSubmit(browser)
    clickHrefId(browser, "paymentForm:netBankPmtLink");
    selectDropDownByIdAndOptionValue(browser, "paymentForm:ddbBank", payment.ddbBank)
    clickCheckBoxById(browser, "paymentForm:ddbTerms")
    fillTextFieldById(browser, "paymentForm:ddbName", payment.ddbName)
    fillTextFieldById(browser, "paymentForm:ddbEmail", payment.ddbEmail)
    fillTextFieldById(browser, "paymentForm:ddbPaymentDetails", payment.paymentRemark)
    clickButtonById(browser, "paymentForm:payNow")
    responseXML = findInputValueByClassName(browser, "input-xxlarge")
    handleResponse(responseXML, payment)
