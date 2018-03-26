import base64
import binascii
import codecs

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from requests import Session
from zeep import Client, Transport

from AppConstants import encryption_decyption_util


def serviceRequest(wsdlUrl, requestXML):
    session = Session()
    session.verify = False
    transport = Transport(session=session)
    client = Client(wsdlUrl,
                    transport=transport)
    print(client)
    responseXML = client.service.serviceRequest(requestXML)
    return responseXML


def paymentDetails(wsdlUrl, requestXML):
    session = Session()
    session.verify = False
    transport = Transport(session=session)
    client = Client(wsdlUrl, transport=transport)
    print(client)
    responseXML = client.service.paymentDetails(requestXML)
    return responseXML


def paymentMessage(wsdlUrl, requestXML):
    session = Session()
    session.verify = False
    transport = Transport(session=session)
    client = Client(wsdlUrl, transport=transport)
    print(client)
    responseXML = client.service.paymentMessage(requestXML)
    return responseXML


def testServiceRequest():
    xmlFile = open("test/data/filename.xml", "r")
    requestXML = xmlFile.read().replace('\n', '')
    replace = encryption_decyption_util.encrypteAES(requestXML)
    result = serviceRequest("https://www.testepg.ae/paymentZone/EPGFIService/EPGFI/EPGFIService.wsdl", replace)
    print(result)
    responseXML = encryption_decyption_util.decryptAES(result)
    print(responseXML)

# testServiceRequest();
