#!/usr/bin/env python3

# apt-get install xvfb # frame buffer stores the screen's pixel vals in arrays
# pip3 install pyvirtualdisplay # python wrapper for xvfb


from datetime import datetime
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
import os

now = datetime.now().strftime("%d%b%Y-%T")
out_file = "tmp/SS-"+now+".png"

display = Display(visible=0, size = [1000,1000])
display.start()

chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("disable-extensions")
chrome_options.add_argument("test-type")
chrome_options.add_argument("ignore-certificate-errors")
browser = webdriver.Chrome('/home/guest/bin/chromedriver',chrome_options=chrome_options)
# YMMV this is the chromedriver I use and the location

url = "https://gps-coordinates.org/my-location.php"
browser.get(url)
browser.save_screenshot(out_file)


browser.close()
browser.quit()

display.stop()

