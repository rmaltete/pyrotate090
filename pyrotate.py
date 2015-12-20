#!/usr/bin/python
'''
# -*- coding: UTF-8 -*-

pyrotate v0.90
for log files rotation.
Copyright Evgeniy Egorov, 2008-2012
E-mail: anyhow2(at)mail.ru
tested on Python 2.7.3 and 3.2.3

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

'''

import os, sys, time, datetime, string, re, glob
from subprocess import check_call, CalledProcessError
from time import localtime, strftime
from os.path import isfile
from socket import gethostname

global mail_able, mailfrom, mailto , smtp, ourhost, subj

try:
    from sender import sendmsg
    mail_able = True
except Exception as err:
    mail_able = False

ourhost = gethostname()
subj = 'pyrotate error on %s' % (ourhost,)

def prior(file_msk, prdloc, priorloc):
    perc=''
    try:
        perc = re.match(re.compile(".*(%).*"),file_msk).groups()[0]
    except AttributeError as err:
        perc=''

    __first=prdloc[0]
    if __first not in ['m','d','w','M','D','W']:
        # set default rotation period as Monthly
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
        msgerr = 'pyrotate.prior on %s -- file mask "%s" is invalid. %s' % (ourhost, file_msk, err)
        print (msgerr)
        if mail_able:
            sendmsg(mailfrom, mailto, subj, body=msgerr, encoding1='ascii', encoding2='ascii', srvr=smtp)
        __file_msk = file_msk
        return(1)
    return __file_msk

def temp_add(__curr_file):
    __tmp_dir = os.path.dirname(__curr_file)
    __tmp_dir = os.path.normpath(__tmp_dir + '/temp')
    __curr_file_list = glob.glob(__curr_file)
    if len(__curr_file_list) != 0:
        i=0
        while i < len(__curr_file_list):
            try:
                os.renames(__curr_file_list[i], os.path.normpath(os.path.join(__tmp_dir,os.path.basename(__curr_file_list[i]))))
            except Exception as err:
                msgerr = 'pyrotate.temp_add on %s -- file "%s" problem. Unable to move it to temp dir. %s' % (ourhost, __curr_file_list[i], err)
                print (msgerr)
                if mail_able:
                    sendmsg(mailfrom, mailto, subj, body=msgerr, encoding1='ascii', encoding2='ascii', srvr=smtp)
                return(1)
            i += 1
        pass
    return os.path.normpath(os.path.join(__tmp_dir,os.path.basename(__curr_file)))

def rotate(config):
    global mail_able, mailfrom, mailto , smtp, ourhost, subj
    try:
#        from sender import sendmsg
#        mail_able = True
        # mailing parameters
        if  'mailfrom' in config:
            mailfrom = config['mailfrom']
        else:
            mailfrom = ''
            mail_able = False   # if parameter isn't in config - no mailing

        if  'mailto' in config:
            mailto = config['mailto']
        else:
            mailto = ''
            mail_able = False   # if parameter isn't in config - no mailing

        if  'smtp' in config:
            smtp = config['smtp']
        else:
            smtp = 'localhost'  # if parameter isn't in config - set default SMTP server as "localhost"
    except Exception:
        mail_able = False
    if  'logfile' in config:
        logfile = config['logfile']
    else:
        msgerr = "pyrotate on %s -- logfile parameter not found in config file %s" % (ourhost, conf_file)
        print (msgerr)
        if mail_able:
            sendmsg(mailfrom, mailto, subj, body=msgerr, encoding1='ascii', encoding2='ascii', srvr=smtp)
        return(1)

    if  'compress' in config:
        compress = config['compress']
    else:
        compress = 0

    if  'keeps' in config:
        keepFiles = config['keeps']
    else:
        keepFiles = 1

    if  'period' in config:
        period = config['period']
    else:
        period = 'monthly'

    if  'force' in config:
        force = config['force']
    else:
        force = 0

    if  'priorarc' in config:
        priorarc = config['priorarc']
    else:
        priorarc = 0

    if  'priorfile' in config:
        priorfile = config['priorfile']
    else:
        priorfile = 0

    if  'target' in config:
        target = config['target']
        target = prior(target, period, priorarc)
    else:
        target = ''

    if  'sf' in config:
        sf = config['sf']
    else:
        sf = ''

    if  'temp' in config:
        temp = config['temp']
    else:
        temp = 0

    logfile = prior(logfile, period, priorfile)

    sfile = Status(conf_file, sf)
    sfile.read()
    if not force:
        if not sfile.torotate(period):
            return(1)
    if not compress:
        if not isfile(logfile):
            return(1)

    if compress:
        try:
            ext = re.match(re.compile(".*(rar|zip|ace|7z|arj|arc|zoo|lha|paq|sqz|bix).*", re.IGNORECASE),compress).groups()[0]
        except AttributeError:
            ext = ''
    else:
        ext = 0

    i=keepFiles
    if keepFiles > 1:
        while i < 20:
            if target:
                lastfile = "%s.%u" % (target, i)
            else:
                lastfile = "%s.%u" % (logfile, i)
            if compress:
                lastfile = lastfile + '.' + ext

            if os.path.isfile(lastfile):
                try:
                    os.remove(lastfile)
                except OSError as err:
                    #print ("Unable to remove file %s\n%s\n" % (lastfile,err))
                    break
            i += 1
        pass

    i=keepFiles

    while i > 0:
        if keepFiles > 1:
            if target:
                curr_file = "%s.%u" % (target, i)
            else:
                curr_file = "%s.%u" % (logfile, i)
        else:
            if target:
                curr_file = target
            else:
                curr_file = logfile

        if compress:
            curr_file_arc = curr_file + '.' + ext

        if i > 1:
            if target:
                prev_file = "%s.%u" % (target, i-1)
            else:
                prev_file = "%s.%u" % (logfile, i-1)

            if compress:
                prev_file_arc = prev_file + '.' + ext
        else:
            prev_file = logfile

        try:
            if keepFiles > 1:
                if compress:
                    if os.path.isfile(prev_file_arc):
                        os.rename(prev_file_arc, curr_file_arc)
                if os.path.isfile(prev_file):
                    os.rename(prev_file, curr_file)
                sfile.write()
        except OSError as err:
            #print ("Unable to rename file\n%s" % (err))
            pass
        i -= 1

    if compress:
        if keepFiles > 1:
            curr_file = "%s.%u" % (logfile, i)
            curr_file_arc = curr_file + '.' + ext
        else:
            curr_file = logfile
            if target:
                curr_file_1 = target
            else:
                curr_file_1 = logfile
            if temp:
                curr_file = temp_add(curr_file)
            curr_file_arc = curr_file_1 + '.' + ext

        directr = os.path.dirname(curr_file_arc)
        if not os.path.isdir(directr):
            try:
                os.makedirs(directr)
            except Exception as err:
                print (err)
                msgerr = 'pyrotate on %s -- target directory "%s" does not exist and unable to create it'  % (ourhost, directr)
                print (msgerr)
                if mail_able:
                    sendmsg(mailfrom, mailto, subj, body=msgerr, encoding1='ascii', encoding2='ascii', srvr=smtp)
                return(1)

        cmd = "%s \"\"%s\"\" \"\"%s\"\"" % (compress, curr_file_arc, curr_file)
        print (cmd)
        try:
            if os.name == 'posix' :  # Linux (and Mac OS and other Unixes? not tested)
                if os.system(cmd) == 0:
                    sfile.write()
                else:
                    msgerr = 'pyrotate on %s --  error while executing the rotation cmd:\n%s' % (ourhost,cmd)
                    print (msgerr)
                    if mail_able:
                        sendmsg(mailfrom, mailto, subj, body=msgerr, encoding1='ascii', encoding2='ascii', srvr=smtp)
                        return (1)
            else:  # supposed Windows
                if check_call(cmd) == 0:
                    sfile.write()
                else:
                    msgerr = 'pyrotate on %s --  error while executing the rotation cmd:\n%s' % (ourhost,cmd)
                    print (msgerr)
                    if mail_able:
                        sendmsg(mailfrom, mailto, subj, body=msgerr, encoding1='ascii', encoding2='ascii', srvr=smtp)
                        return (1)
        except CalledProcessError as err:  # an error while executing external cmd of archiving (nonzero return code)
            print (err)
#            if mail_able:
#                sendmsg(mailfrom, mailto, subj, body=err, encoding1='ascii', encoding2='ascii', srvr=smtp)
            sendmsg(mailfrom, mailto, subj, body=err, encoding1='ascii', encoding2='ascii', srvr=smtp)
            return (1)
        except Exception as err:  # all other errors
            msgerr = 'pyrotate on %s --  bad rotation cmd' % (ourhost,)
            print (msgerr)
            print (err)
            if mail_able:
                sendmsg(mailfrom, mailto, subj, body=err, encoding1='ascii', encoding2='ascii', srvr=smtp)
            return (1)
    return (0)

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
            # set default rotation period as Monthly
            __first = 'm'
            print ("pyrotate.Status.torotate -- unknown period of rotating. Defaulting Monthly")

        __tdate = datetime.datetime.now()
        if __tdate.year != self.statusdate.year:
            __result=1
            return __result

        if __first == 'd' or __first == 'D':
            if __tdate.day == self.statusdate.day and __tdate.month == self.statusdate.month:
                __result=0
            else:
                __result=1
        elif __first == 'w' or __first == 'W':
            __tdatewd = datetime.datetime.isocalendar(__tdate)[1]
            __statusdatewd = datetime.datetime.isocalendar(self.statusdate)[1]
            if __statusdatewd < __tdatewd:
                __result=1
            else:
                __result=0
        elif __first == 'm' or __first == 'M':
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

if __name__ == "__main__":
    try:
        # get a filename from command line
        conf_file = sys.argv[1]
        # get "config" from configuration file
        exec(open(conf_file).read())
        # do rotation
        if rotate(config):
            msgerr = 'pyrotate.main on %s -- error while rotating by conf_file %s' % (ourhost, conf_file)
#            print (msgerr)
#            if mail_able:
#                sendmsg(mailfrom, mailto, subj, body=msgerr, encoding1='ascii', encoding2='ascii', srvr=smtp)
            sys.exit(1)

    except Exception as err:
        print (err)
        print ("Usage:\npyrotate.py <configFile>\n")
        sys.exit(1)
