#!/usr/bin/python
'''
sender v0.90
for sending E-mail messages
tested on Python 2.7
(3.x may be later)
now work on v3.x if encodings are only ascii and compatible and texts are in English
Copyright Evgeniy Egorov, 2008-2012
E-mail: anyhow2(at)mail.ru

Distributed under the GNU General Public License v2.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


inputs:
  from_adr - sender e-mail (no defaults)
  to_adr - receiver e-mail (no defaults)
  subj - message subject (default '')
  body - message text (default '')
  encoding1 - initial (input) encoding of subject and body (default 'ascii' for 7-bit English texts)
    For example 'UTF-8' in modern Linuxes
  encoding2 - result (output) encoding of subject and body (default 'ascii')
    For example 'Windows-1251'
  srvr - SMTP server as "server" or "server:port" (default 'localhost')
  name - user login for SMTP-authentication, default '' 
  password - for SMTP-authentication, default ''
  debug - if != 0, will print all SMTP session on console
  sleeping - number of seconds for sleep after message sending, default 0
    for possible time based antispam systems (by several messages in given time interval)
'''

import smtplib, sys, re
from email.mime.text import MIMEText
from base64 import standard_b64encode
def sendmsg(from_adr, to_adr, subj='', body='', encoding1='ascii', encoding2='ascii', srvr='localhost', name='', password='', debug=0, sleeping=0):

    if encoding1 != encoding2:
        __subj = unicode(subj, encoding1).encode(encoding2)
        __body = unicode(body, encoding1).encode(encoding2)
    else:
        __subj = subj
        __body = body
    if encoding2.lower() not in ['ascii','us','us-ascii','iso-8859-1','lat1','latin1','latin-1']:
        __subj = '=?' + encoding2 + '?B?' + standard_b64encode(__subj) + '?='

    port=25
    server=srvr
    try:
        port = int(re.match(re.compile(".*\:(\d+)"),srvr).groups()[0])
        server = re.match(re.compile("(.*)\:.*"),srvr).groups()[0]
    except:
        port = 25
        server=srvr

    # create message
    msg = MIMEText(__body, "", encoding2)
    msg['Subject'] = __subj
    msg['From'] = from_adr
    msg['To'] = to_adr

    # and send it
    err=''
    try:
        s = smtplib.SMTP(server, port)
        # if you want to see SMTP session, then set debug != 0
        if debug:
            s.set_debuglevel(1)
        # if name not empty, then login in SMTP-server
        if name:
            s.starttls()
            s.login(name, password)
        s.sendmail(from_adr, to_adr, msg.as_string())
        s.quit()
#       sleep 3 seconds for possible time based antispam systems (by several messages in given time interval)
        from time import sleep
        sleep(sleeping)
    except smtplib.SMTPResponseException as err:
        pass
    return(err)
#
#test and usage example
#
if __name__ == "__main__":
    try:
        from_adr = sys.argv[1]
        to_adr = sys.argv[2]
        subject = sys.argv[3]
        text = sys.argv[4]
        encoding1 = sys.argv[5]
        encoding2 = sys.argv[6]
        srvr = sys.argv[7]
    except:
        from_adr = 'anyhow5@mail.com'
        to_adr = 'anyhow5@mail.com'
        subject = 'statistics error'
        text = 'awstats or other statisics problem'
        encoding1='ascii'
        encoding2='ascii'
        srvr='localhost'

    result=sendmsg(from_adr, to_adr, subject, text, encoding1, encoding2, srvr, sleeping=1)
    if result:
        print ('Error:')
        print (result)
