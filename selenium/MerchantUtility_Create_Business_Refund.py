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
from AppConstants import  *

def merchantUtilityRefundEnterAmount(browser, amount):
    fillTextFieldById(browser, "txnAmount", amount)


def merchantUtilitySelectMerchant(browser, merchant):
    selectDropDownByIdAndOptionValue(browser, "merchantID", merchant)


def merchantUtilityRefundtSubmit(browser):
    clickButtonByXpath(browser, "//input[@type='submit' and @value='General Reversal']")
    print("merchant page was submit")

def handleBusinessRefundResponse(rowIndex, writeSheet, xmlInstance):
    errorCode = xmlInstance.findAllByXPath('Body/SrvRes/ExceptionDetails/ErrorCode')
    writeSheet.write(rowIndex, REVERSAL_ERROR_CODE, errorCode)
    transactionRef = xmlInstance.findAllByXPath('Body/SrvRes/TxnReversalRes/Transfer/NoqodiRevRefNo')
    writeSheet.write(rowIndex, NOQODI_REVERSAL_REF, transactionRef)

def makeBusinessRefund(browser, rowIndex, readSheet, writeSheet):
    loadURL(browser, HOST+"/TransactionReversalForm.jsp")
    merchantUtilitySelectMerchant(browser, readSheet.cell(rowIndex, MERCHANT_CODE).value)
    merchantUtilityRefundEnterAmount(browser, readSheet.cell(rowIndex, REFUND_AMOUNT).value)
    fillTextFieldById(browser, "epgTxnId", readSheet.cell(rowIndex, NOQODI_REF).value)
    fillTextFieldById(browser, "txnId", readSheet.cell(rowIndex, MERCHANT_REF).value)
    selectDropDownByIdAndOptionValue(browser,"sourceTypeID", readSheet.cell(rowIndex, REFUND_TYPE).value)
    if readSheet.cell(rowIndex, REFUND_TYPE).value == "ECA":
        fillTextFieldById(browser, "walletId", readSheet.cell(rowIndex, REFUND_WALLET_ID).value)
    elif readSheet.cell(rowIndex, REFUND_TYPE).value == "BKT":
        fillTextFieldById(browser, "beneNameId", readSheet.cell(rowIndex, REFUND_BENE_NAME).value)
        fillTextFieldById(browser, "beneBankCountryId", readSheet.cell(rowIndex, REFUND_BENE_BANK_COUNTRY).value)
        fillTextFieldById(browser, "IBANNoId", readSheet.cell(rowIndex, REFUND_IBAN).value)

    merchantUtilityRefundtSubmit(browser)
    waitForURL(browser, "merchantUtility/TransactionReversalSubmit.jsp")
    responseXML = findInputValueByClassName(browser, "input-xxlarge")
    writeSheet.write(rowIndex, REVERSAL_RESPONSE_XML, responseXML)
    xmlInstance = xmlObject(responseXML)
    handleBusinessRefundResponse(rowIndex, writeSheet, xmlInstance)

