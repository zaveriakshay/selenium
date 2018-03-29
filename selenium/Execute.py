from MerchantUtility_Create_Business_Refund import *
from MerchantUtility_Create_Payment_CCD_Saved import *
from MerchantUtility_Create_Payment_CCD_Unregistered import *
from MerchantUtility_Create_Payment_DDB import *
from MerchantUtility_Create_Payment_ECA import *
from Read_Excel import *
from AppConstants import *
from SOAP_Create_Payment_Xpress import *
from SOAP_Create_Refund_Adjustment import makeRefundAdjustment
from SOAP_Create_TopUp import makeTopUp


def executePayment():
    print("Start executePayment")
    paymentOrRefund = excelToExecutable(xlsx, 'Payments')
    execute(paymentOrRefund, xlsx, 'Payments')
    return paymentOrRefund


def executeRefunds():
    print("Start executeRefunds")
    paymentOrRefund = excelToExecutable(xlsx, 'Refunds')
    execute(paymentOrRefund, xlsx, 'Refunds')


def executeFITopUps():
    print("Start executeFITopUps")
    paymentOrRefund = excelToExecutable(xlsx, 'Topup')
    execute(paymentOrRefund, xlsx, 'Topup')


def refundUpdateFlow(payments):
    template_payment_ = payments["templatePayment"]
    executable_list_ = payments["executableList"]
    refunds = excelToExecutable(xlsx, 'Refunds')
    template_refund_ = refunds["templateRefund"]
    templateFIPaymentMessage = refunds["templateFIPaymentMessage"]
    refundDict = createRefundMap(refunds)
    for payment in executable_list_:
        updatePaymentDetailsToAllRefunds(payment, refundDict)
    saveObjectToExcel(xlsx, 'Refunds', refunds["executableList"], template_payment_,
                      template_refund_, templateFIPaymentMessage)


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
                elif executable.Type == "REFUNDADJ" :
                    makeRefundAdjustment(browser, executable)
            elif isinstance(executable, FIPaymentMessage):
                makeTopUp(browser, executable)
        except:
            pass
    saveObjectToExcel(destinationExcelPath, destinationSheetName, executable_list_, template_payment_, template_refund_,
                      templateFIPaymentMessage)
    browser.close();


payments = executePayment()
payments = excelToExecutable(xlsx,'Payments')
refundUpdateFlow(payments)
executeRefunds()

# executeFITopUps()
