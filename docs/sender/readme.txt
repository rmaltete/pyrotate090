sender v0.90
send a message by the smtp server
Copyright Evgeniy Egorov, 2008-2012
E-mail anyhow2(at)mail.ru

License - GNU General Public License v2

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

v0.90 changes:
  - fixed some bugs
  - more readable documetation

v0.88 changes:
  - tested for Python v2.7
  - added parameter "sleeping"
  - SMTP server may be as "server:port" now
  - default for both encodings is "ascii" now

v0.8 changes:
  - some fixes

v0.4 changes:
  - tested and changed to work in Linux too (as in Windows)
  - full compliance to SMTP's RFCs for best antispam pass through

parameter's list:

from_adr, to_adr, subj='', body='', encoding1='ascii', encoding2='ascii', srvr='localhost', name='', password='', debug=0, sleeping=0):

  from_adr - sender e-mail (no defaults)
  to_adr - receiver e-mail (no defaults)
  subj - message subject (default '')
  body - message text (default '')
  encoding1 - initial (input) encoding of subject and body (default ascii)
  encoding2 - result (output) encoding of subject and body (default ascii)
    You may change default encodings as yuo wish. For example to 'ascii'
    If encoding1 == encoding2 == ascii module work and in Python 3.x
  srvr - SMTP server (default localhost) as "server" or "server:port"
  name - user login for SMTP-authentication, default '' 
  password - for SMTP-authentication, default ''
  debug - if != 0, will print all SMTP session on console
  sleeping - number of seconds for sleep after message
    sending, default 0 - for possible time based antispam systems (by several
    messages in given time interval)

running in command line arguments are in this seq:
    from_adr
    to_adr
    subject
    text
    encoding1
    encoding2
    srvr
