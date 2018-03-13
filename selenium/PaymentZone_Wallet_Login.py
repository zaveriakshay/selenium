#!/usr/bin/python
# -*- coding: utf-8 -*-
# from suds.client import Client
# url="http://94.200.29.187:5115/paymentZone/PaymentService/Payment?WSDL"
# client = Client(url)
# print (client)


def paymentZoneWalletLogin_EnterWallet(driver, wallet):
    elem = driver.find_element_by_id("paymentForm:wallet_id")
    elem.clear()
    elem.send_keys(wallet)
    print("wallet id was entered")


def paymentZoneWalletLogin_EnterPassword(driver, password):
    elem = driver.find_element_by_id("paymentForm:password")
    elem.clear()
    elem.send_keys(password)
    print("password was entered")


def paymentZoneWalletLogin_Submit(driver):
    driver.find_element_by_id("paymentForm:loginButton").click()
    print("payment login hapenned")
