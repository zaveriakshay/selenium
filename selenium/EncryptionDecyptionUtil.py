import base64
import binascii

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2


class EncryptionDecyptionUtil:

    def __init__(self):
        keyFilePath = "Key.kf"
        keyFile = open(keyFilePath, "rb")
        ivLength = int.from_bytes(bytes(keyFile.read(1)), byteorder='big')
        print(ivLength)
        self.iv = bytes(keyFile.read(int(ivLength)))
        print(self.iv)

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
        self.key = kdf[:32]

    def encrypteAES(self, plainText):
        encryptCipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encodedPlainText = plainText.encode()
        length = 16 - (len(encodedPlainText) % 16)
        encodedPlainText += bytes([length]) * length
        return base64.b64encode(encryptCipher.encrypt(encodedPlainText)).decode()

    def decryptAES(self, cipherText):
        decryptCipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decryptedBytes = decryptCipher.decrypt(base64.b64decode(cipherText))
        decryptedText = (decryptedBytes[:-decryptedBytes[-1]]).decode()
        return decryptedText


def testAES(self):
    plainText = "Hello Akshay"
    util = EncryptionDecyptionUtil()
    cipherText = util.encrypteAES(plainText)
    print("Encrypted Text" + cipherText)
    print("Plain Text" + plainText)
    plainTextBytes = util.decryptAES(cipherText)
    print("Decrypted Text" + plainTextBytes)
