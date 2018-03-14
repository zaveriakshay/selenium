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


def executePayments():
    print("Start")
    print("XLS Name:" + XLS_Name)
    workbook = xlrd.open_workbook(XLS_Name)
    sheet = workbook.sheet_by_index(0)
    writeWorkBook = copy(workbook)
    w_sheet = writeWorkBook.get_sheet(0)
    print("write sheet 0 was accesed:" + XLS_Name)
    browser = createBrowser()
    for row in range(1, sheet.nrows):
        print(sheet.cell(row, PAYMENT_MODE).value)
        if sheet.cell(row, PAYMENT_MODE).value == "ECA":
            makeECAPayment(browser, row, sheet, w_sheet)
        elif sheet.cell(row, PAYMENT_MODE).value == "CCD":
            makeSavedCCDPayment(browser, row, sheet, w_sheet)
        elif sheet.cell(row, PAYMENT_MODE).value == "CCDUNREG":
            makeUnregisteredCCDPayment(browser, row, sheet, w_sheet)
        elif sheet.cell(row, PAYMENT_MODE).value == "DDB":
            makeDDBPayment(browser, row, sheet, w_sheet)
        elif sheet.cell(row, PAYMENT_MODE).value == "EXIT":
            break
        elif sheet.cell(row, PAYMENT_MODE).value == "NA":
            continue
    writeWorkBook.save(XLS_Name)
    browser.close();


#executePayments();
executeReversal();