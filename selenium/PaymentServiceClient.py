import base64

import binascii
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from requests import Session
from zeep import Client, Transport
import codecs

keyFilePath = "Key.kf"
keyFile = open(keyFilePath, "rb")
ivLength = int.from_bytes(bytes(keyFile.read(1)), byteorder='big')
print(ivLength)
iv = bytes(keyFile.read(int(ivLength)))
print(iv)

passPhraseLength = int.from_bytes(bytes(keyFile.read(1)), byteorder='big')
print(passPhraseLength)
passPhrase = bytes(keyFile.read(int(passPhraseLength)))
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

kdf = PBKDF2(passPhrase, saltHexArray, 16, iterationsLength)
key = kdf[:32]


def encrypteAES(plainText):
    encryptCipher = AES.new(key, AES.MODE_CFB, iv)
    encodedPlainText = plainText.encode()
    return encryptCipher.encrypt(encodedPlainText)


def decryptAES(cipherText):
    decryptCipher = AES.new(key, AES.MODE_CFB, iv)
    return decryptCipher.decrypt(cipherText)


plainText = "Hello Akshay"
cipherText = encrypteAES(plainText)
print("Encrypted Text" + str(cipherText))
print("Plain Text" + plainText)
plainTextBytes = decryptAES(cipherText)
print("Decrypted Text" + plainTextBytes.decode('utf-8'))

session = Session()
session.verify = False
transport = Transport(session=session)
client = Client('https://www.testepg.ae/paymentZone/PaymentService/Payment/PaymentService.wsdl', transport=transport)
print(client)
xmlFile = open("test/data/filename.xml", "r")
requestXML = xmlFile.read().replace('\n','')
encryptedRequestXML = codecs.encode(encrypteAES(requestXML), 'base64')
base64EncodedRequestXML = base64.b64encode(encrypteAES(requestXML))
replace = str(base64EncodedRequestXML)
result = client.service.serviceRequest(replace)
print(result)
