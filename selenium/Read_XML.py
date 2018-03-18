#!/usr/bin/python
# -*- coding: utf-8 -*-
# from suds.client import Client
# url="http://94.200.29.187:5115/paymentZone/PaymentService/Payment?WSDL"
# client = Client(url)
# print (client)
import xml.etree.ElementTree as ET
from UserControl import *


class xmlObject:
    def __init__(self,xmlString):
        print("__init__:in:" + xmlString)
        self.xmlString = xmlString;
        self.elementTree = ET.fromstring(self.xmlString)

    def getXmlString(self):
        print("getXmlString:in:" )
        return self.xmlString;

    def getElementTree(self):
        print("getElementTree:in:" )
        return self.elementTree;

    def printAllTags(self):
        print("printAllTags:in:" )
        for child in self.elementTree:
            print(child.tag)

    def findByXpath(self,xPath):
        print("findByXpath:in:" +xPath)
        print("findByXpath:self.elementTree:" +self.elementTree.tag)
        self.elementTree.find(xPath)

    def iterateSearch(self,tagName):
        print("iterateSearch:in:" +tagName)
        print("iterateSearch:self.elementTree:" +self.elementTree.tag)
        tag = self.elementTree.iter(tagName)
        print(tag)

    def findAllByXPath(self,xPath):
        print("findAllByXPath:in:" +xPath)
        tag = self.elementTree.findall(xPath)
        print("findAllByXPath:tag:" +str(tag))
        for i in tag:
            text = i.text
            break
        print("findAllByXPath:out:" +text)
        return text

def readXML(xmlString):
    print("readXML:in:" + xmlString)
    xmlInstance = xmlObject(xmlString)
    xmlInstance.findAllByXPath('Body/SrvRes/NormalPayRes/Transfer/TransactionRefNo')

def createXML():
    root = ET.Element("root")
    doc = ET.SubElement(root, "doc")
    ET.SubElement(doc, "field1").text = "some value1"
    ET.SubElement(doc, "field2").text = "some vlaue2"
    tree = ET.ElementTree(root)
    xmlAsString = ET.tostring(tree)
    print(xmlAsString)
    tree.write("test/data/filename.xml")


#createXML()