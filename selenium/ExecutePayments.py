import xlrd
from localselenium.wrapper.UserControl import *
from xlutils.copy import copy

from MerchantUtility_Create_Payment_CCD_Saved import *
from MerchantUtility_Create_Payment_CCD_Unregistered import *
from MerchantUtility_Create_Payment_DDB import *
from MerchantUtility_Create_Payment_ECA import *
from MerchantUtility_Create_Business_Refund import *

workbook = xlrd.open_workbook(r"test\data\Payments.xls")
sheet = workbook.sheet_by_index(0)
writeWorkBook = copy(workbook)
w_sheet = writeWorkBook.get_sheet(0)

browser = createBrowser()
for row in range(1, sheet.nrows):
    print(sheet.cell(row, 4).value)
    if sheet.cell(row, 4).value == "ECA":
        makeECAPayment(browser, row, sheet, w_sheet)
    elif sheet.cell(row, 4).value == "CCD":
        makeSavedCCDPayment(browser, row, sheet, w_sheet)
    elif sheet.cell(row, 4).value == "CCDUNREG":
        makeUnregisteredCCDPayment(browser, row, sheet, w_sheet)
    elif sheet.cell(row, 4).value == "DDB":
        makeDDBPayment(browser, row, sheet, w_sheet)
    elif sheet.cell(row, 4).value == "EXIT":
        break
    elif sheet.cell(row, 4).value == "NA":
        continue

    if "REVERSAL" in sheet.cell(row, 0).value:
        writeWorkBook.save(r"test\data\Payments.xls")
        makeBusinessRefund(browser, row, sheet, w_sheet)

writeWorkBook.save(r"test\data\Payments.xls")
#browser.close();
