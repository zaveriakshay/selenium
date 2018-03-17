from MerchantUtility_Create_Business_Refund import *
from MerchantUtility_Create_Payment_CCD_Saved import *
from MerchantUtility_Create_Payment_CCD_Unregistered import *
from MerchantUtility_Create_Payment_DDB import *
from MerchantUtility_Create_Payment_ECA import *
from Read_Excel import *


def executePayment():
    print("Start executePayment")
    paymentOrRefund = excelToExecutable('test/data/Payments.xlsx','Payments')
    execute(paymentOrRefund,'test/data/Payments.xlsx', 'Payments')
    return paymentOrRefund

def executeRefunds():
    print("Start executeRefunds")
    paymentOrRefund = excelToExecutable('test/data/Payments.xlsx','Refunds')
    execute(paymentOrRefund,'test/data/Payments.xlsx', 'Refunds')

def refundUpdateFlow(payments):
    template_payment_ = payments["templatePayment"]
    executable_list_ = payments["executableList"]
    refunds = excelToExecutable('test/data/Payments.xlsx', 'Refunds')
    template_refund_ = refunds["templateRefund"]
    refundDict = createRefundMap(refunds)
    for payment in executable_list_ :
        updatePaymentDetailsToAllRefunds(payment,refundDict)
    saveObjectToExcel('test/data/Payments.xlsx', 'Refunds', refunds["executableList"], template_payment_, template_refund_)

def createRefundMap(paymentOrRefund):
    print("Start createRefundMap")
    executable_list_ = paymentOrRefund["executableList"]
    dict = {}
    for executable in executable_list_:
        if isinstance(executable, Refund):
            dict.setdefault(str(executable.paymentSequence), []).append(executable)
    return dict

def updatePaymentDetailsToAllRefunds(payment :Payment,refundDict):
    print("start updatePaymentDetailsToAllRefunds")
    try:
        executables = refundDict[payment.sequence]
        if isinstance(executables,list):
            for executable in executables :
                executable.noqodiRef = payment.noqodiRef
                executable.merchantRef = payment.merchantRef
                executable.merchantCode = payment.merchantCode
        else:
            executables.noqodiRef = payment.noqodiRef
            executables.merchantRef = payment.merchantRef
            executables.merchantCode = payment.merchantCode
    except:
        pass



def execute(paymentOrRefund,destinationExcelPath,destinationSheetName):
    browser = createBrowser()
    template_refund_ = paymentOrRefund["templateRefund"]
    template_payment_ = paymentOrRefund["templatePayment"]
    executable_list_ = paymentOrRefund["executableList"]
    for executable in executable_list_:
        if isinstance(executable, Payment):
            if executable.paymentMode == "ECA":
                makeECAPayment(browser, executable)
            elif executable.paymentMode == "CCD":
                makeSavedCCDPayment(browser, executable)
            elif executable.paymentMode == "CCDUNREG":
                makeUnregisteredCCDPayment(browser, executable)
            elif executable.paymentMode == "DDB":
                makeDDBPayment(browser, executable)
            elif executable.paymentMode == "EXIT":
                break
            elif executable.paymentMode == "NA":
                continue
        elif isinstance(executable, Refund):
            makeBusinessRefund(browser, executable)
    saveObjectToExcel(destinationExcelPath, destinationSheetName, executable_list_, template_payment_, template_refund_)
    browser.close();


payments = executePayment()
#payments = excelToExecutable('test/data/Payments.xlsx','Payments')
refundUpdateFlow(payments)
executeRefunds()