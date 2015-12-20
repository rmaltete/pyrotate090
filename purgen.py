#!/usr/bin/python

'''
purgen v0.90
can purge log (any other too) files with given parameters

and is distributed under the GNU General Public License v2.

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

Copyright Evgeniy Egorov, 2008-2012
E-mail: anyhow2(at)mail.ru

 config file:
   logfile - file name

   keeps - number of file versions to save (default - 9)
   
   period - daily, weekly or monthly (really use only first letter)
   
   force - always rotate files
   
   priorfile - date for converting to filenames takes from prior period
      (for example for weekly it is today minus 1 week)
   
   sf - if exist filename of status file where it is information of
      date and time of last rotation for current config, else status file will
      make in userdir/.pyrotate/<configfilename.sta> (posix) and
      <configfilenamefullpath.sta> (Windows)
   
   mailfrom - sender of error message, for example
    'mailfrom': 'purgen_backuper@firma.ru'
    'mailfrom': 'purgen_on_%s@firma.ru' % (ourhost,)
    where ourhost variable get host name in program.
    if not exist, messages not send
  
   mailto - e-mail of receiver
    if not exist, messages not send
  
   smtp - hostname or ip-address of SMTP-server for sending mail.
    Default: localhost

'''

import os, sys, time, datetime, string, re, glob
from time import localtime, strftime
from os.path import isfile
from socket import gethostname
global ourhost
ourhost = gethostname()
global mail_able
mail_able = False

def prior(file_msk, prdloc, priorloc):
    perc=''
    try:
        perc = re.match(re.compile(".*(%).*"),file_msk).groups()[0]
    except AttributeError as err:
        perc=''

    __first=prdloc[0]
    if __first not in ['m','d','w','M','D','W']:
        __first = 'm'

    __tdate = datetime.datetime.today()

    if priorloc:
        if __first == 'd' or __first == 'D':
            __tdate = __tdate + datetime.timedelta(days=-1)
        elif __first == 'w' or __first == 'W':
            __tdate = __tdate + datetime.timedelta(weeks=-1)
        elif __first == 'm' or __first == 'M':
            if __tdate.month != 1:
                __year = __tdate.year
                __month = __tdate.month - 1
            else:
                __year = __tdate.year - 1
                __month = 12
            __tdate = datetime.date(__year, __month, __tdate.day)

    try:
        if perc:
            __file_msk = __tdate.strftime(file_msk)
        else:
            __file_msk = file_msk
    except Exception as err:
        print ('purgen.prior -- file mask "%s" is invalid' % (file_msk))
        print (err)
        __file_msk = file_msk
        sys.exit()
    return __file_msk


class Status:

    def __init__(self, file, stfl):
        if stfl:
            self.statusfile = stfl
        else:
            if os.name == 'nt' :
                self.statusfile=os.path.normpath(file+".sta")
            else:
                self.statusdir=os.path.normpath(os.path.expanduser("~/.pyrotate"))
                if not os.path.isdir(self.statusdir):
                    os.mkdir(self.statusdir)
                self.statusfile=os.path.normpath(os.path.expanduser("~/.pyrotate/"+os.path.basename(file)+".sta"))


    def read(self):
        if os.path.isfile(self.statusfile):
            __f = open(self.statusfile, "r")
            self.status = __f.readline()
            __f.close()
        else:
            self.status = '1980-01-01 00:00:00'


    def torotate(self, period):
        self.statusdate = datetime.datetime.strptime(self.status, '%Y-%m-%d %H:%M:%S')

        __first=period[0]
        if __first not in ['m','d','w','M','D','W']:
            __first = 'm'
            print ('purgen.Status.torotate -- unknown period of rotating. Defaulting "monthly"')

        __tdate = datetime.datetime.now()
        if __tdate.year != self.statusdate.year:
            __result=1
            return __result

        if __first == 'd' or __first == 'D':
            #if __tdate.day == self.statusdate.day and __tdate.month == self.statusdate.month and __tdate.year == self.statusdate.year:
            if __tdate.day == self.statusdate.day and __tdate.month == self.statusdate.month:
                __result=0
            else:
                __result=1
        elif __first == 'w' or __first == 'W':
            __tdatewd = datetime.datetime.isocalendar(__tdate)[1]
            __statusdatewd = datetime.datetime.isocalendar(self.statusdate)[1]
            #if __statusdatewd < __tdatewd or __tdate.year != self.statusdate.year:
            if __statusdatewd < __tdatewd:
                __result=1
            else:
                __result=0
        elif __first == 'm' or __first == 'M':
            #if  self.statusdate.month < __tdate.month or __tdate.year != self.statusdate.year:
            if  self.statusdate.month < __tdate.month:
                __result=1
            else:
                __result=0
        return __result


    def write(self):
        __dtmt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        __f = open(self.statusfile, "w")
        __f.write(__dtmt)
        __f.close()

try:
    from sender import sendmsg
    mail_able = True

    # mailing parameters
    if  'mailfrom' in config:
        mailfrom = config['mailfrom']
    else:
        mailfrom = ''
        mail_able = False

    if  'mailto' in config:
        mailto = config['mailto']
    else:
        mailto = ''
        mail_able = False

    if  'smtp' in config:
        smtp = config['smtp']
    else:
        smtp = 'localhost'
except Exception:
    mail_able = False

try:
    conf_file = sys.argv[1]
except Exception:
    print ("Usage:\npurgen.py <configFile>\n")
    sys.exit()

exec(open(conf_file).read())

if  'logfile' in config:
    logfile = config['logfile']
else:
    print ("logfile parameter not found in config file %s\n" % (conf_file))
    sys.exit()

if  'keeps' in config:
    keepFiles = config['keeps']
else:
    keepFiles = 9

if  'period' in config:
    period = config['period']
else:
    period = 'monthly'

if  'force' in config:
    force = config['force']
else:
    force = 0

if  'priorfile' in config:
    priorfile = config['priorfile']
else:
    priorfile = 0

if  'sf' in config:
    sf = config['sf']
else:
    sf = ''

logfile = prior(logfile, period, priorfile)

sfile = Status(conf_file, sf)
sfile.read()
if not force:
    if not sfile.torotate(period):
        sys.exit()

dirct = glob.glob(logfile)
dirct.sort(key=str.lower,reverse=1)
dirct_len=len(dirct)

if dirct_len > keepFiles:
    for file_rem in dirct[keepFiles : ]:
        if os.path.isfile(file_rem):
            try:
                os.remove(file_rem)
            except OSError as err:
                body = "%s  purgen -- unable to remove file from %s\n%s\n" % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), ourhost, err)
                print (body)
# this is optional for e-mail error reporting and may removed  -----\
# and must be changed with real parameters (from, to, smtp) if exist
                subj='Purgen trouble on ' + ourhost
                sendmsg(mailfrom, mailto, subj, body, encoding1='ascii', encoding2='ascii', srvr=smtp)
    sfile.write()
