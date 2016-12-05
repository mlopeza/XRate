XRate
=====
Small program used to get the exchange rate [MXN/US] from XOOM.

The intended use of this script is to send/print an alert when the exchange rate exceeds certain number.

This is the cronjob to do a request every 30 minutes, this will print it to stdout and we redirect the output to a file:
0,30 * * * * python2.7 main.py >> xoom_exchange_rate 2>&1

If you use python main.py --help you can see the options to send e-mails instead of printing to stdout.
