##This file will contain all constanta
from EncryptionDecyptionUtil import EncryptionDecyptionUtil
from Image import GifCreator

#HOST = "http://94.200.29.187:5115/merchantUtility"
#PAYMENT_WSDL = "http://94.200.29.187:5115/paymentZone/PaymentService/Payment/PaymentService.wsdl"
#FI_WSDL = "http://94.200.29.187:5115/paymentZone/EPGFIService/EPGFI/EPGFIService.wsdl"
HOST="https://www.testepg.ae/merchantUtility"
PAYMENT_WSDL = "https://www.testepg.ae/paymentZone/PaymentService/Payment/PaymentService.wsdl"
FI_WSDL = "https://www.testepg.ae/paymentZone/EPGFIService/EPGFI/EPGFIService.wsdl"

XLS_Name = r"test\data\TNOQ-5173\Round1\Reversal_API_Single Bene_No Charges_No Adjustment_Multi_Refund.xls"
testCaseFolder = "test/data/DataCreation/Round4/"
xlsx = testCaseFolder+'Day6_data_Preparation_refund_MR100599.xlsx'

MODULE = 0
MERCHANT_CODE = MODULE + 1
PAYMENT_AMOUNT = MERCHANT_CODE + 1
MERCHANT_REF = PAYMENT_AMOUNT + 1
PAYMENT_MODE = MERCHANT_REF + 1
WALLET_ID = PAYMENT_MODE + 1
PASSWORD = WALLET_ID + 1
PAYMENT_REMARKS = PASSWORD + 1
CCD_NUMBER = PAYMENT_REMARKS + 1
CCD_MONTH = CCD_NUMBER + 1
CCD_YEAR = CCD_MONTH + 1
CCD_HOLDER_NAME = CCD_YEAR + 1
CCD_CVV = CCD_HOLDER_NAME + 1
CCD_EMAIL = CCD_CVV + 1
DDB_BANK = CCD_EMAIL + 1
DDB_NAME = DDB_BANK + 1
DDB_EMAIL = DDB_NAME + 1
NOQODI_REF = DDB_EMAIL + 1
RESPONSE_XML = NOQODI_REF + 1
PAYMENT_ERROR_CODE = RESPONSE_XML + 1
REFUND_AMOUNT = PAYMENT_ERROR_CODE + 1
REFUND_TYPE = REFUND_AMOUNT + 1
REFUND_WALLET_ID = REFUND_TYPE + 1
REFUND_BENE_NAME = REFUND_WALLET_ID + 1
REFUND_BENE_BANK_COUNTRY = REFUND_BENE_NAME + 1
REFUND_IBAN = REFUND_BENE_BANK_COUNTRY + 1
NOQODI_REVERSAL_REF = REFUND_IBAN + 1
REVERSAL_RESPONSE_XML = NOQODI_REVERSAL_REF + 1
REVERSAL_ERROR_CODE = REVERSAL_RESPONSE_XML + 1

nowPng = testCaseFolder+r"Images/now.png"
gifGlobalCreator = GifCreator(1, testCaseFolder+"Images/now.gif",nowPng)
encryption_decyption_util = EncryptionDecyptionUtil()

print(REVERSAL_RESPONSE_XML)
