#!/usr/bin/python
# -*- coding: utf-8 -*-
# from suds.client import Client
# url="http://94.200.29.187:5115/paymentZone/PaymentService/Payment?WSDL"
# client = Client(url)
# print (client)
from MerchantUtility_Create_Payment import *
from PaymentServiceClient import xPressPay
from Read_Excel import Payment


def makeExpressPayment(browser, payment: Payment):
    xmlString = open("resources/template/XPressPay.xml", "r")
    xmlInstance = xmlObject(xmlString.read())
    requestXML = xmlInstance.pushObjectToTemplate(payment)
    print("Request XML:" + requestXML)
    requestXML = encryption_decyption_util.encrypteAES(requestXML)
    print("Encrypted Request XML:" + requestXML)
    responseXML = xPressPay(PAYMENT_WSDL, requestXML)
    print("Encrypted Response XML:" + responseXML)
    responseXML = encryption_decyption_util.decryptAES(responseXML)
    print("Response XML:" + responseXML)
    handleResponse(responseXML, payment)
