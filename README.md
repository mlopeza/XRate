XRate
=====
Small program used to get the exchange rate [MXN/US] from XOOM.

The intended use of this program is to send an alert when the 
Exchange Rate is high enough that you consider good and then 
the same program will use your email to send you an alert.

This is the cronjob to do a request every 30 minutes:
0,30 * * * * DISPLAY=:1 xvfb-run python2.7 main.py >> xoom_exchange_rate 2>&1

The Display option and xvfb-run where used for Uniteller, because you need to login
in order to check the Exchange rate, but you also need to change your password every 
30 days, so it is difficult to mantain the script working correctly
