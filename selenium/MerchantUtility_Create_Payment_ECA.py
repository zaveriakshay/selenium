#!/usr/bin/python
# -*- coding: utf-8 -*-
# from suds.client import Client
# url="http://94.200.29.187:5115/paymentZone/PaymentService/Payment?WSDL"
# client = Client(url)
# print (client)
from MerchantUtility_Create_Payment import *
from PaymentZone_Wallet_Login import *
from localselenium.wrapper.UserControl import *
import xml.etree.ElementTree as ET


def makeECAPayment(browser, rowIndex, readSheet, writeSheet):
    loadURL(browser, "https://www.testepg.ae/merchantUtility/PaymentForm.jsp")
    merchantUtilitySelectMerchant(browser, readSheet.cell(rowIndex, 1).value)
    merchantUtilityPaymentEnterAmount(browser, readSheet.cell(rowIndex, 2).value)
    merchantTxnId = findInputValueById(browser, "txnID")
    writeSheet.write(rowIndex, 3, merchantTxnId)
    merchantUtilityPaymentSubmit(browser)
    paymentZoneWalletLogin_EnterWallet(browser, readSheet.cell(rowIndex, 5).value)
    paymentZoneWalletLogin_EnterPassword(browser, readSheet.cell(rowIndex, 6).value)
    paymentZoneWalletLogin_Submit(browser)
    fillTextFieldById(browser, "paymentForm:dw_payment_details", readSheet.cell(rowIndex, 7).value)
    clickButtonById(browser, "paymentForm:payNow")
    waitForURL(browser, "merchantUtility/NPayResponse.jsp")
    responseXML = findInputValueByClassName(browser, "input-xxlarge")
    root = ET.fromstring(responseXML)
    print(root.tag)
    writeSheet.write(rowIndex, 18, responseXML)


'''browser = createBrowser()
makeECAPayment(browser)'''
