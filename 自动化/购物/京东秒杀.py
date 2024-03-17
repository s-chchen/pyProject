import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

import win32com.client
speaker = win32com.client.Dispatch("SAPI.SpVoice")


# 打开浏览器
browser = webdriver.Chrome()

# 进入京东首页
browser.get("https://www.jd.com/")
time.sleep(3)

if browser.find_element(By.LINK_TEXT, "你好，请登录"):
    browser.find_element(By.LINK_TEXT, "你好，请登录").click()
    print(f"请扫码")
    time.sleep(9)

# 购物车
browser.get("https://cart.jd.com/cart_index")
time.sleep(6)


while True:
    if browser.find_element(By.CLASS_NAME, 'jdcheckbox'):
        speaker.Speak(f"选择购物车首个商品")
        jdcheckboxs = browser.find_element(By.CLASS_NAME, 'jdcheckbox')
        tck = jdcheckboxs[1]
        tck.click()
        break

# while True:
#     now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
#     print(now)
#
#     if now >= '2024-03-17 13:55:00':
#         while 1 == 1:
#             try:
#                 if browser.find_element(By.LINK_TEXT, '去结算'):
#                     print("提交订单了")
#                     browser.find_element(By.LINK_TEXT, '去结算').click()
#                     speaker.Speak(f"已经提交订单了，请支付")
#                     break
#             except:
#                 pass
#
#         while True:
#             try:
#                 if browser.find_element(By.LINK_TEXT, '提交订单'):
#                     browser.find_element(By.LINK_TEXT, '提交订单').click()
#             except:
#                 print(f"请支付")
#                 break
#
#         time.sleep(0.01)

