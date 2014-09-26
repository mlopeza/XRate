#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import sys
import smtplib
import json
from datetime import datetime
import time



def noticeEMail(rate, usr, psw, fromaddr, toaddr):

    # Initialize SMTP server
    server=smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(usr,psw)

    # Send email
    senddate=datetime.strftime(datetime.now(), '%Y-%m-%d')
    subject="Great Rate right now"
    m="Date: %s\r\nFrom: %s\r\nTo: %s\r\nSubject: %s\r\nX-Mailer: My-Mail\r\n\r\n" % (senddate, fromaddr, toaddr, subject)
    msg='Rate:\n'+str(rate)

    server.sendmail(fromaddr, toaddr, m+msg)
    server.quit()

def get_info():
    result = requests.get('https://www.xoom.com/ajax/options-xfer-amount-ajax?receiveCountryCode=MX&sendAmount=25&_=1400631011779')
    return result.json()['result']


def get_uniteller():
    from pyvirtualdisplay import Display
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    display = Display(visible=1, size=(1024, 768))
    display.start()
    profile = webdriver.FirefoxProfile("/home/mario/.mozilla/firefox/b0l6x1qu.default")
    browser = webdriver.Firefox(profile)

    browser.get('https://send.uniteller.com/jsps/LoginPage.action?request_locale=es&wlp_name=Uniteller')
    elem = browser.find_element_by_name('email')
    #TODO: Don't hardcode user
    elem.send_keys('user@mail.com')
    time.sleep(5)
    browser.find_element_by_id('proceed').click()
    #TODO: Don't use a hardcoded password
    browser.find_element_by_id('password').send_keys("HARDCODED_PASSWORD")
    time.sleep(5)
    browser.find_element_by_id('proceed').click()
    answer = browser.find_element_by_id("firstAnswer")
    #TODO: Make this configurable (Questions)
    if answer is not None:
        question = browser.find_element_by_class_name('email_box')
        question = question.text
        if question[9:] == u"¿Cuál era tu apodo de la infancia?":
            response = ""
        elif question[9:] == u"¿Cuál es el nombre de tu mejor amigo de la infancia?":
            response = ""
        else:
            response = "Windsor"
    browser.find_element_by_id('firstAnswer').send_keys(response)
    browser.find_element_by_id('registerComputerCheck').click()
    time.sleep(5)
    browser.find_element_by_id('proceed').click()

    exchange_rate = browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div[1]/ul/li[8]/strong').text
    exchange_rate = exchange_rate.split('=')[1].split(' ')[0]
    browser.get("https://send.uniteller.com/jsps/LogoutAction.action")
    time.sleep(5)
    browser.quit()
    display.stop()
    return exchange_rate


def get_rate():
    result = get_info()
    return result['fxRate']

def main():
    date_now = str(datetime.now())
    rate_xoom = get_rate()
    #rate_uniteller = get_uniteller()
    rate_string = date_now+ " XOOM       " + str(rate_xoom) + "\n"
    print rate_string
    #TODO: Make The desired rate configurable
    if float(rate_xoom) < 12.95:
        return 0
    #TODO: Send user and password as parameters
    usr=None
    psw=None
    fromaddr=usr
    toaddr=usr
    if usr and psw:
        # Send notification email
        noticeEMail(rate_string, usr, psw, fromaddr, toaddr)

if __name__ == "__main__":
    sys.exit(main())
