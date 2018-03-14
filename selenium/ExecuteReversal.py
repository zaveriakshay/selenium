import xlrd
from localselenium.wrapper.UserControl import *
from xlutils.copy import copy

from AppConstants import *
from MerchantUtility_Create_Business_Refund import *


def executeReversal():
    print("Start")
    print("Reversal is starting here")
    refundworkbook = xlrd.open_workbook(XLS_Name)
    ref_sheet = refundworkbook.sheet_by_index(0)
    refundWriteWorkBook = copy(refundworkbook)
    w_ref_sheet = refundWriteWorkBook.get_sheet(0)
    browser = createBrowser()
    print("write sheet 0 was accesed:" + XLS_Name)
    for row in range(1, ref_sheet.nrows):
        print("Payment error code:" + ref_sheet.cell(row, PAYMENT_ERROR_CODE).value)
        if "REVERSAL" in ref_sheet.cell(row, MODULE).value and "EPG-PMT-000" in ref_sheet.cell(row,
                                                                                               PAYMENT_ERROR_CODE).value:
            makeBusinessRefund(browser, row, ref_sheet, w_ref_sheet)
    refundWriteWorkBook.save(XLS_Name)
    browser.close();

