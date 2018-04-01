#!/usr/bin/python
# -*- coding: utf-8 -*-
# from suds.client import Client
# url="http://94.200.29.187:5115/paymentZone/PaymentService/Payment?WSDL"
# client = Client(url)
# print (client)
from FIServiceClient import paymentMessage
from MerchantUtility_Create_Payment import *
from Read_Excel import Payment, FIPaymentMessage


def handleTopUpResponse(responseXML, payment: FIPaymentMessage):
    try:
        xmlInstance = xmlObject(responseXML)
        payment.ResponseXML = responseXML
        errorCode = xmlInstance.findAllByXPath('Body/SrvRes/ExceptionDetails/ErrorCode')
        payment.ResponseCode = errorCode
        if errorCode == "EPG-PMT-000":
            transactionRef = xmlInstance.findAllByXPath('Body/SrvRes/PaymentMessageRes/Payment/EPGTransactionID')
            payment.noqodiRef = transactionRef
    except:
        pass

def makeTopUp(browser, payment: FIPaymentMessage):
    with open("resources/template/ChargeTopupReq.xml", "r") as xmlTemplateFile:
        xmlString = xmlTemplateFile.read()
    xmlInstance = xmlObject(xmlString)
    requestXML = xmlInstance.pushObjectToTemplate(payment)
    print("Request XML:" + requestXML)
    requestXML = encryption_decyption_util.encrypteAES(requestXML)
    print("Encrypted Request XML:" + requestXML)
    responseXML = paymentMessage(FI_WSDL, requestXML, payment.FICode)
    print("Encrypted Response XML:" + responseXML)
    responseXML = encryption_decyption_util.decryptAES(responseXML)
    print("Response XML:" + responseXML)
    handleTopUpResponse(responseXML, payment)

    if payment.isEOD == "true":
        with open("resources/template/SubmitEODReq_Transaction.xml", "r") as xmlTemplateFile:
            xmlString = xmlTemplateFile.read()
        xmlInstance = xmlObject(xmlString)
        payment.TransactionXML = xmlInstance.pushObjectToTemplate(payment)
