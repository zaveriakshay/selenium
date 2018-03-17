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

def executeRefunds():
    print("Start executeRefunds")
    paymentOrRefund = excelToExecutable('test/data/Payments.xlsx','Refunds')
    execute(paymentOrRefund,'test/data/Payments.xlsx', 'Refunds')

def refundUpdateFlow():
    loadPayment = excelToExecutable('test/data/Payments.xlsx','Payments')
    template_refund_ = loadPayment["templateRefund"]
    template_payment_ = loadPayment["templatePayment"]
    executable_list_ = loadPayment["executableList"]
    paymentOrRefund = excelToExecutable('test/data/Payments.xlsx', 'Refunds')
    refundDict = createRefundMap(paymentOrRefund)
    for payment in executable_list_ :
        updatePaymentDetailsToAllRefunds(payment,refundDict)
    saveObjectToExcel('test/data/Payments.xlsx', 'Refunds', paymentOrRefund["executableList"], template_payment_, template_refund_)

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
    executables = refundDict[payment.sequence]
    if isinstance(executables,list):
        for executable in executables :
            executable.noqodiRef = payment.noqodiRef
            executable.merchantRef = payment.merchantRef
    else:
        executables.noqodiRef = payment.noqodiRef
        executables.merchantRef = payment.merchantRef



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


#executePayment();
refundUpdateFlow()
