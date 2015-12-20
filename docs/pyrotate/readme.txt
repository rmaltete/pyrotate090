pyrotate v0.90
for files rotation
Copyright Evgeniy Egorov (aka Eugene Egorow), 2008-2012
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
  - changed and tested to work in Windows (XP)
  - fixed some bugs
  - more readable documetation

v0.88 changes:
  - tested for Python v2.7 and v3.2
  - in case of an error control returns with nonzero code instead of a program exit
  - added double "" in command lines for filenames with spaces
    (resulting cmd is for example now:
    /usr/bin/zip  ""/rota/txt_120620.zip"" ""/rota/lis*.txt"")

v0.8 changes:
  - added optional sendings of error messages by SMTP-server, if in the program directory
    (or in the PYTHON path) sender.py is found and in config file are 'mailfrom' and 'mailto'
  - if target archive directory does not exist it will be created

v0.6 changes:
  - changed and tested to work in GNU/Linux
  - after compressing rotated files will not be deleted now.
    If you want to delete rotated files - use command
    like "m" (move) in archiver's command strings.
  - config examples added

Dependences:
  - Python v2.6 or better v2.7 (v2.5 for pyrotate v0.8 or earlier)
  - an external archiver as specified in 'compress' parameter

config file:
  logfile - file name or it's mask with special characters
      to give multiple log files for rotation. Mask may include symbols like '*'.
      See also section "Python style date formatting" at the end of this doc file.

  keeps - number of file versions to save (0 - no renaming)

  compress (0 - don't compress files or command line to archive)

  target - file name of target archive (if not present - an archive
      name will be the same as logfile and keeps > 1)
 
  period - daily, weekly or monthly (only first letter used really). 
      Default is 'monthly'

  force - if is not 0, always rotate files. Default is 0.

  priorfile - if is not 0, date for converting to filenames takes from prior period
      (for example for weekly it is today minus 1 week)

  priorarc - if is not 0, date for converting to archive names takes from prior period

  sf - is tne name of the file, which contains rotation status for the current config.
      (certains the date and time of the last rotation). If sf not found by program or
      it shows the date of the previous rotation period the rotation is needed and the
      sf (status file) is re-written with the current date and time.
      If sf parameter not exists in config when status file will be made in
      <userdir>/.pyrotate/<configfilename.sta> (posix) and 
      <configfilenamefullpath.sta> (Windows)

  temp - if = 1, then subdir temp is made in log files directory and all logs are moved
      there before archiving and after rotation all temp directory and its content will
      be deleted. Default is 0.

  mailfrom - sender of an error message, for example
     'mailfrom': 'pyrotate_backuper@firma.ru'
     'mailfrom': 'pyrotate_on_%s@firma.ru' % (ourhost,)
     where 'ourhost' variable gets host name in program.
     If not exist, messages will not be sent

  mailto - e-mail of a receiver
    if not exist, messages will not be sent

  smtp - hostname or ip-address of SMTP-server for sending mail.
    Default: localhost

   The following directives can be embedded in the logfile and target
     (Python style date formatting).
     if keeps > 1, directives in filenames are not allowed

   Directive | Meaning | Notes
   %a  Locale's abbreviated weekday name.
   %A  Locale's full weekday name.
   %b  Locale's abbreviated month name.
   %B  Locale's full month name.
   %c  Locale's appropriate date and time representation.
   %d  Day of the month as a decimal number [01,31].
   %H  Hour (24-hour clock) as a decimal number [00,23].
   %I  Hour (12-hour clock) as a decimal number [01,12].
   %j  Day of the year as a decimal number [001,366].
   %m  Month as a decimal number [01,12].
   %M  Minute as a decimal number [00,59].
   %p  Locale's equivalent of either AM or PM. (1)
   %S  Second as a decimal number [00,61]. (2)
   %U  Week number of the year (Sunday as the first day of the week) 
       as a decimal number [00,53]. All days in a new year preceding 
       the first Sunday are considered to be in week 0.    (3)
   %w  Weekday as a decimal number [0(Sunday),6].
   %W  Week number of the year (Monday as the first day of the week)
       as a decimal number [00,53]. All days in a new year preceding
       the first Monday are considered to be in week 0.    (3)
   %x  Locale's appropriate date representation.
   %X  Locale's appropriate time representation.
   %y  Year without century as a decimal number [00,99].
   %Y  Year with century as a decimal number.
   %Z  Time zone name (no characters if no time zone exists).
   %%  A literal "%" character.
