import xlrd
from localselenium.wrapper.UserControl import *
from xlutils.copy import copy

from MerchantUtility_Create_Payment_CCD_Saved import *
from MerchantUtility_Create_Payment_CCD_Unregistered import *
from MerchantUtility_Create_Payment_DDB import *
from MerchantUtility_Create_Payment_ECA import *
from MerchantUtility_Create_Business_Refund import *
from AppConstants import *
from ExecuteReversal import *
from Read_Excel import *


def execute():
    print("Start")
    paymentOrRefund = excelToPayment()
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
            break;

    saveObjectToExccel(executable_list_, template_payment_, template_refund_)
    browser.close();


# executePayments();
execute();
