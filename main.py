#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import requests
import smtplib
import sys

from datetime import datetime


def _connect(func):
    """
    Decorator to ensure that we always connect just before trying to send an e-mail.
    """
    def wrapper(self, *args, **kwargs):
        if not self._server:
            self._server = smtplib.SMTP(self.server)
            self._server.starttls()
            self._server.login(self.username, self.password)
        return func(self, *args, **kwargs)
    return wrapper

class Mailer(object):
    """
    Create a connection to an SMTP server to be able to send e-mails.
    """
    def __init__(self, username, password, server):
        self.username = username
        self.password = password
        self.server = server
        self._server = None


    @_connect
    def send_mail(self, subject, message, to_address, date=None):
        """
        Send an e-mail using the current connection.
        """
        if not date:
            date = datetime.now()
        senddate = datetime.strftime(date, '%Y-%m-%d')

        formatted_message = "Date: {0}\r\nFrom: {1}\r\nTo: {2}\r\nSubject: {3}\r\nX-Mailer: My-Mail\r\n\r\n{4}".format(
            senddate, self.username, to_address, subject, message)
        self._server.sendmail(self.username, to_address, formatted_message)

    def close(self):
        # There's no standard way of checking for an open connection, so we use a
        # common attribute in the class to verify if there's an open connection.
        if self._server and self._server.file:
            self._server.close()


class XOOM(object):
    """
    Retrieve Exchange Rate from the XOOM site
    """
    SITE = "https://xoom.com"

    def __init__(self):
        self.name = "XOOM"
        self._rate = None

    @property
    def rate(self):
        if self._rate:
            return self._rate
        url = os.path.join(self.SITE,
                           "ajax",
                           "options-xfer-amount-ajax?receiveCountryCode=MX&sendAmount=25&_=1400631011779")
        self._rate = float(requests.get(url).json()['result']['fxRate'])
        return self._rate

    def __str__(self):
        return "{0}: {1}".format(self.name, self.rate)

def main():
    parser = argparse.ArgumentParser(description="Send e-mail with current exchange rates for MXN/USD")
    parser.add_argument('--to', help='Where to send exchange rates, if not provided they will be printed out.',
                        default=None)
    parser.add_argument('--from-email',
                        help='From which e-mail will the results be sent out from.', default=None)
    parser.add_argument('--password',
                        help='Password for the e-mail that will be used to send the exchange rates.',
                        default=None)
    parser.add_argument('--smtp-server',
                        help='SMTP server to connect to.', default=None)
    parser.add_argument('--subject', default="Exchange Rates.")
    parser.add_argument('--minimum', type=float, help="Minimum amount you want in the exchange rate to consider it to be "
                                                 "sent out. As an example, you might want to receive notificatiosn only"
                                                 " if the exchange rate is higher than 20 MXN",
                        default=0)
    args = parser.parse_args()

    # If all the conditions are met to send an e-mail we can use the Mailer object to send it, otherwise we will just
    # print the result to stdout.
    mailer = None
    if args.to and args.from_email and args.password:
        mailer = Mailer(args.from_email, args.password, args.smtp_server)

    # For now we only have XOOM, so concatenations is not an issue
    xoom = XOOM()
    message = ""
    if xoom.rate > args.minimum:
        message = message + "\n" + str(xoom)

    # Remove extra newlines
    message = message.lstrip()

    if mailer:
        mailer.send_mail(args.subject, message, args.to)
        mailer.close()
    else:
        # We weren't able to create a mailer object so we print to stdout.
        print(message)

if __name__ == "__main__":
    sys.exit(main())
