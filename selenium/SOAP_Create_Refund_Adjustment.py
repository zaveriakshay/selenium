#!/usr/bin/python
# -*- coding: utf-8 -*-
# from suds.client import Client
# url="http://94.200.29.187:5115/paymentZone/PaymentService/Payment?WSDL"
# client = Client(url)
# print (client)
from MerchantUtility_Create_Business_Refund import handleBusinessRefundResponse
from MerchantUtility_Create_Payment import *
from PaymentServiceClient import serviceRequest


def makeRefundAdjustment(browser, refund: Refund):
    with open("resources/template/ReversalAdjustment"+refund.refundSourceType+".xml", "r") as xmlTemplateFile:
        xmlString = xmlTemplateFile.read()
    xmlInstance = xmlObject(xmlString)
    requestXML = xmlInstance.pushObjectToTemplate(refund)
    print("Request XML:" + requestXML)
    requestXML = encryption_decyption_util.encrypteAES(requestXML)
    print("Encrypted Request XML:" + requestXML)
    responseXML = serviceRequest(PAYMENT_WSDL, requestXML)
    print("Encrypted Response XML:" + responseXML)
    responseXML = encryption_decyption_util.decryptAES(responseXML)
    print("Response XML:" + responseXML)
    refund.reversalResponseXML = responseXML
    xmlInstance = xmlObject(responseXML)
    handleBusinessRefundResponse(refund,xmlInstance)
