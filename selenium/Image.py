import datetime

import imageio
import selenium
from selenium import webdriver

from AppConstants import *

VALID_EXTENSIONS = ('png', 'jpg')


def create_gif(filenames, duration):
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    output_file = 'Gif-%s.gif' % datetime.datetime.now().strftime('%Y-%M-%d-%H-%M-%S')
    imageio.mimsave(output_file, images, duration=duration)


class GifCreator:

    def __init__(self, duration, outputFileName,inputFileName):
        self.imageCollection = []
        self.duration = duration
        self.outputFileName = outputFileName
        self.nowPng = inputFileName

    def appendToGif(self):
        self.imageCollection.append(imageio.imread(self.nowPng))

    def saveGIFToDisk(self):
        imageio.mimsave(self.outputFileName, self.imageCollection, duration=self.duration)

    def takeScreenShot(self, browser):
        browser.save_screenshot(self.nowPng)


class GifCreatorDecorator(object):

    def __init__(self, arg1: GifCreator):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        print("Inside __init__()")
        self.gifCreator = arg1

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        print("Inside __call__()")

        def wrapped_f(*args):
            print("Inside wrapped_f()")
            # print("Decorator arguments:", self.arg1)
            if isinstance(args[0], selenium.webdriver.chrome.webdriver.WebDriver):
                print("arg[0] is instance of web driver, now we can take screen shot call gif creator")
                self.gifCreator.takeScreenShot(args[0])
                self.gifCreator.appendToGif()
                self.gifCreator.saveGIFToDisk()

            return f(*args)
            print("After f(*args)")

        return wrapped_f
