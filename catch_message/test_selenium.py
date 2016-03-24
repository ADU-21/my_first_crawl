#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time
from selenium import webdriver

browser = webdriver.Firefox()
browser.set_window_size(1055, 800)
browser.get("https://www.hack-cn.com/url.php?id=76232469049e5e3916fc03f1f3070ee1")
#browser.find_element_by_id("idClose").click()
#time.sleep(5)

browser.save_screenshot("shot.png")
browser.quit()