import base64
import binascii
import codecs

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from requests import Session
from zeep import Client, Transport

keyFilePath = "Key.kf"
keyFile = open(keyFilePath, "rb")
ivLength = int.from_bytes(bytes(keyFile.read(1)), byteorder='big')
print(ivLength)
iv = bytes(keyFile.read(int(ivLength)))
print(iv)

passPhraseLength = int.from_bytes(bytes(keyFile.read(1)), byteorder='big')
print(passPhraseLength)
passPhrase = bytes(keyFile.read(int(passPhraseLength))).decode()
print(passPhrase)

saltLength = int.from_bytes(bytes(keyFile.read(1)), byteorder='big')
print(saltLength)
salt = bytes(keyFile.read(int(saltLength)))
saltString = binascii.hexlify(salt)
saltHexArray = binascii.unhexlify(saltString)
print(salt)

iterationsLength = int.from_bytes(bytes(keyFile.read(1)), byteorder='big')
print(iterationsLength)
iterations = bytes(keyFile.read(int(iterationsLength)))
print(iterations)

kdf = PBKDF2(passPhrase.encode(), saltHexArray, int(128 / 8), int(iterations.decode()))
key = kdf[:32]


def encrypteAES(plainText):
    encryptCipher = AES.new(key, AES.MODE_CBC, iv)
    encodedPlainText = plainText.encode()
    length = 16 - (len(encodedPlainText) % 16)
    encodedPlainText += bytes([length]) * length
    return base64.b64encode(encryptCipher.encrypt(encodedPlainText)).decode()


def decryptAES(cipherText):
    decryptCipher = AES.new(key, AES.MODE_CBC, iv)
    decryptedBytes = decryptCipher.decrypt(base64.b64decode(cipherText))
    decryptedText = (decryptedBytes[:-decryptedBytes[-1]]).decode()
    return decryptedText


def serviceRequest(wsdlUrl, requestXML):
    session = Session()
    session.verify = False
    transport = Transport(session=session)
    client = Client(wsdlUrl,
                    transport=transport)
    print(client)
    responseXML = client.service.serviceRequest(requestXML)
    return responseXML


def xPressPay(wsdlUrl, requestXML):
    session = Session()
    session.verify = False
    transport = Transport(session=session)
    client = Client(wsdlUrl,
                    transport=transport)
    print(client)
    responseXML = client.service.xPressPay(requestXML)
    return responseXML


def testAES():
    plainText = "Hello Akshay"
    cipherText = encrypteAES(plainText)
    print("Encrypted Text" + cipherText)
    print("Plain Text" + plainText)
    plainTextBytes = decryptAES(cipherText)
    print("Decrypted Text" + plainTextBytes)


def testServiceRequest():
    xmlFile = open("test/data/filename.xml", "r")
    requestXML = xmlFile.read().replace('\n', '')
    replace = encrypteAES(requestXML)
    result = serviceRequest("https://www.testepg.ae/paymentZone/PaymentService/Payment/PaymentService.wsdl", replace)
    print(result)
    responseXML = decryptAES(result)
    print(responseXML)
