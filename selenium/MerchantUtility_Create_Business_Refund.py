#!/usr/bin/python
# -*- coding: utf-8 -*-
# from suds.client import Client
# url="http://94.200.29.187:5115/paymentZone/PaymentService/Payment?WSDL"
# client = Client(url)
# print (client)
from localselenium.wrapper.UserControl import *

from MerchantUtility_Create_Payment import *
from PaymentZone_Wallet_Login import *
from Read_XML import xmlObject

def merchantUtilityRefundEnterAmount(browser, amount):
    fillTextFieldById(browser, "txnAmount", amount)


def merchantUtilitySelectMerchant(browser, merchant):
    selectDropDownByIdAndOptionValue(browser, "merchantID", merchant)


def merchantUtilityRefundtSubmit(browser):
    clickButtonByXpath(browser, "//input[@type='submit' and @value='Generate Reversal']")
    print("merchant page was submit")

def makeBusinessRefund(browser, rowIndex, readSheet, writeSheet):
    loadURL(browser, "https://www.testepg.ae/merchantUtility/TransactionReversalForm.jsp")
    merchantUtilitySelectMerchant(browser, readSheet.cell(rowIndex, 1).value)
    merchantUtilityRefundEnterAmount(browser, readSheet.cell(rowIndex, 19).value)
    fillTextFieldById(browser, "epgTxnId", readSheet.cell(rowIndex, 17).value)
    fillTextFieldById(browser, "txnId", readSheet.cell(rowIndex, 3).value)
    selectDropDownByIdAndOptionValue(browser,"sourceTypeID", readSheet.cell(rowIndex, 20).value)
    if readSheet.cell(rowIndex, 20).value == "ECA":
        fillTextFieldById(browser, "walletId", readSheet.cell(rowIndex, 21).value)
    elif readSheet.cell(rowIndex, 20).value == "BKT":
        fillTextFieldById(browser, "beneNameId", readSheet.cell(rowIndex, 24).value)
        fillTextFieldById(browser, "beneBankCountryId", readSheet.cell(rowIndex, 23).value)
        fillTextFieldById(browser, "IBANNoId", readSheet.cell(rowIndex, 24).value)

    merchantUtilityRefundtSubmit(browser)
    waitForURL(browser, "merchantUtility/NPayResponse.jsp")
    responseXML = findInputValueByClassName(browser, "input-xxlarge")
    '''xmlInstance = xmlObject(responseXML)
transactionRef = xmlInstance.findAllByXPath('Body/SrvRes/NormalPayRes/Transfer/TransactionRefNo')
writeSheet.write(rowIndex, 17, transactionRef)'''
    writeSheet.write(rowIndex, 26, responseXML)


'''browser = createBrowser()
makeECAPayment(browser)'''
