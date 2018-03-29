#!/usr/bin/python
# -*- coding: utf-8 -*-
# from suds.client import Client
# url="http://94.200.29.187:5115/paymentZone/PaymentService/Payment?WSDL"
# client = Client(url)
# print (client)
from UserControl import *

from MerchantUtility_Create_Payment import *
from PaymentZone_Wallet_Login import *
from Read_XML import xmlObject
from AppConstants import *


def makeSavedCCDPayment(browser, rowIndex, readSheet, writeSheet):
    loadURL(browser, HOST + "/PaymentForm.jsp")
    merchantUtilitySelectMerchant(browser, readSheet.cell(rowIndex, MERCHANT_CODE).value)
    merchantUtilityPaymentEnterAmount(browser, readSheet.cell(rowIndex, PAYMENT_AMOUNT).value)
    merchantTxnId = findInputValueById(browser, "txnID")
    writeSheet.write(rowIndex, MERCHANT_REF, merchantTxnId)
    merchantUtilityPaymentSubmit(browser)
    paymentZoneWalletLogin_EnterWallet(browser, readSheet.cell(rowIndex, WALLET_ID).value)
    paymentZoneWalletLogin_EnterPassword(browser, readSheet.cell(rowIndex, PASSWORD).value)
    paymentZoneWalletLogin_Submit(browser)
    fillTextFieldById(browser, "paymentForm:dw_payment_details", readSheet.cell(rowIndex, PAYMENT_REMARKS).value)
    clickRadioButtonById(browser, "paymentForm:selectedAccount:1")
    clickButtonById(browser, "paymentForm:payNow")
    waitForURL(browser, "merchantUtility/NPayResponse.jsp")
    responseXML = findInputValueByClassName(browser, "input-xxlarge")
    handleResponse(responseXML, rowIndex, writeSheet)


def makeSavedCCDPayment(browser, payment: Payment):
    loadURL(browser, HOST + "/PaymentForm.jsp")
    merchantUtilitySelectMerchant(browser, payment.merchantCode)
    merchantUtilityPaymentEnterAmount(browser, payment.paymentAmount)
    fillBeneDetails(browser, payment)
    merchantTxnId = findInputValueById(browser, "txnID")
    payment.merchantRef = merchantTxnId
    merchantUtilityPaymentSubmit(browser)
    paymentZoneWalletLogin_EnterWallet(browser, payment.walletId)
    paymentZoneWalletLogin_EnterPassword(browser, payment.password)
    paymentZoneWalletLogin_Submit(browser)
    fillTextFieldById(browser, "paymentForm:dw_payment_details", payment.paymentRemark)
    clickRadioButtonById(browser, "paymentForm:selectedAccount:1")
    clickButtonById(browser, "paymentForm:payNow")
    waitForURL(browser, "merchantUtility/NPayResponse.jsp")
    responseXML = findInputValueByClassName(browser, "input-xxlarge")
    handleResponse(responseXML, payment)
