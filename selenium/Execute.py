from MerchantUtility_Create_Business_Refund import *
from MerchantUtility_Create_Payment_CCD_Saved import *
from MerchantUtility_Create_Payment_CCD_Unregistered import *
from MerchantUtility_Create_Payment_DDB import *
from MerchantUtility_Create_Payment_ECA import *
from Read_Excel import *
from AppConstants import *
from SOAP_Create_Payment_Xpress import *
from SOAP_Create_Refund_Adjustment import makeRefundAdjustment
from SOAP_Create_TopUp import makeTopUp, callEOD
import pandas as pd


def executePayment():
    print("Start executePayment")
    paymentOrRefund = excelToExecutable(xlsx, SHEET_NAME_PAYMENT)
    execute(paymentOrRefund, xlsx, SHEET_NAME_PAYMENT)
    return paymentOrRefund


def executeRefunds():
    print("Start executeRefunds")
    paymentOrRefund = excelToExecutable(xlsx, SHEET_NAME_REFUND)
    execute(paymentOrRefund, xlsx, SHEET_NAME_REFUND)


def refundUpdateFlow(payments):
    template_payment_ = payments["templatePayment"]
    executable_list_ = payments["executableList"]
    refunds = excelToExecutable(xlsx, SHEET_NAME_REFUND)
    template_refund_ = refunds["templateRefund"]
    templateFIPaymentMessage = refunds["templateFIPaymentMessage"]
    refundDict = createRefundMap(refunds)
    for payment in executable_list_:
        updatePaymentDetailsToAllRefunds(payment, refundDict)
    saveObjectToExcel(xlsx, SHEET_NAME_REFUND, refunds["executableList"], template_payment_,
                      template_refund_, templateFIPaymentMessage,None)


def createRefundMap(paymentOrRefund):
    print("Start createRefundMap")
    executable_list_ = paymentOrRefund["executableList"]
    dict = {}
    for executable in executable_list_:
        if isinstance(executable, Refund):
            dict.setdefault(str(executable.paymentSequence), []).append(executable)
    return dict


def updatePaymentDetailsToAllRefunds(payment: Payment, refundDict):
    print("start updatePaymentDetailsToAllRefunds")
    try:
        executables = refundDict[payment.sequence]
        if isinstance(executables, list):
            for executable in executables:
                executable.noqodiRef = payment.noqodiRef
                executable.merchantRef = payment.merchantRef
                executable.merchantCode = payment.merchantCode
        else:
            executables.noqodiRef = payment.noqodiRef
            executables.merchantRef = payment.merchantRef
            executables.merchantCode = payment.merchantCode
    except:
        pass


def executeFITopUps():
    print("Start executeFITopUps")
    paymentOrRefund = excelToExecutable(xlsx, SHEET_NAME_FI_TOPUP)
    execute(paymentOrRefund, xlsx, SHEET_NAME_FI_TOPUP)

def executeFIEOD():
    print("Start executeFIEOD")
    paymentOrRefund = excelToExecutable(xlsx, SHEET_NAME_FI_EOD)
    execute(paymentOrRefund, xlsx, SHEET_NAME_FI_EOD)

def EODFIUpdateFlow():
    topups = excelToExecutable(xlsx, SHEET_NAME_FI_EOD)
    list_ = []
    templateFIEOD = topups["templateFIEOD"]

    df = pd.read_excel(xlsx,SHEET_NAME_FI_TOPUP)
    grouped = df.groupby('FICode')

    for index, groupObj in enumerate(grouped):
        name = groupObj[0]
        group = groupObj[1]
        print(name)
        print(group)
        print(str(group["FICode"].count()) + ":" + str(group["Amount"].sum()) + ":" + str(group["TransactionXML"].sum()))
        fiEOD = FIEOD()
        list_.append(fiEOD)
        fiEOD.FICode = name
        fiEOD.TransactionXML = str(group["TransactionXML"].sum())
        fiEOD.sequence = str(index +1)
        fiEOD.FITransactionID = str(group["FITransactionID"].max())
        fiEOD.TotalAmount = str(group["Amount"].sum())
        fiEOD.TotalTransactions = str(group["FICode"].count())
        fiEOD.Type = SHEET_NAME_FI_EOD

    saveObjectToExcel(xlsx, SHEET_NAME_FI_EOD, list_, None,None,None,templateFIEOD)


def execute(paymentOrRefund, destinationExcelPath, destinationSheetName):
    browser = createBrowser()
    template_refund_ = paymentOrRefund["templateRefund"]
    template_payment_ = paymentOrRefund["templatePayment"]
    templateFIPaymentMessage = paymentOrRefund["templateFIPaymentMessage"]
    executable_list_ = paymentOrRefund["executableList"]
    for executable in executable_list_:
        try:
            if isinstance(executable, Payment):
                if executable.paymentMode == "ECA":
                    makeECAPayment(browser, executable)
                elif executable.paymentMode == "CCD":
                    makeSavedCCDPayment(browser, executable)
                elif executable.paymentMode == "CCDUNREG":
                    makeUnregisteredCCDPayment(browser, executable)
                elif executable.paymentMode == "DDB":
                    makeDDBPayment(browser, executable)
                elif executable.paymentMode == "XPR":
                    makeExpressPayment(browser, executable)
                elif executable.paymentMode == "EXIT":
                    break
                elif executable.paymentMode == "NA":
                    continue
            elif isinstance(executable, Refund):
                if executable.Type == "REFUND":
                    makeBusinessRefund(browser, executable)
                elif executable.Type == "REFUNDADJ":
                    makeRefundAdjustment(browser, executable)
            elif isinstance(executable, FIPaymentMessage):
                makeTopUp(browser, executable)
            elif isinstance(executable, FIEOD):
                callEOD(browser, executable)
        except Exception as exception:
            print(exception)
            pass
    saveObjectToExcel(destinationExcelPath, destinationSheetName, executable_list_, template_payment_, template_refund_,
                      templateFIPaymentMessage,None)
    browser.close();
    browser.quit();

'''
payments = executePayment()
payments = excelToExecutable(xlsx, SHEET_NAME_PAYMENT)
refundUpdateFlow(payments)
executeRefunds()
'''

#executeFITopUps()
#EODFIUpdateFlow()
executeFIEOD()