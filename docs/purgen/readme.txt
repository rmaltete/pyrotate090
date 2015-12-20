purgen v0.90
to purge log (or other) files with given parameters
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
  - fixed some bugs
  - more readable documetation

v0.88 changes:
  - tested for Python v2.7 and v3.2

v0.8 changes:
  - added optional sendings of error messages by SMTP-server, if in the program directory
    (or in the PYTHON path) sender.py is found and in config file are 'mailfrom' and 'mailto'

v0.6 changes:
  - changed and tested to work in Linux
  - deleted some bugs
  - sendmsg changed
  - config examples added

config file:
  logfile - file name or it's mask with special characters to give multiple
      log files for purification. Mask may include symbols like '*'.
      See also section "Python style date formatting" at the end of this doc file.

  keeps - number of file versions to save (default - 9)

  period - daily, weekly or monthly (really use only first letter)

  force - always run to purge files

  priorfile - date for converting to filenames takes from prior period
      (for example for weekly it is today minus 1 week)

  sf - is tne name of the file, which contains purification status for the current config.
      (certains the date and time of the last rotation). If sf not found by program or
      it shows the date of the previous purification period the purification is needed
      and the sf (status file) is re-written with the current date and time.
      If sf parameter not exists in config when status file will be made in
      <userdir>/.pyrotate/<configfilename.sta> (posix) and 
      <configfilenamefullpath.sta> (Windows)

  mailfrom - sender of an error message, for example
      'mailfrom': 'pyrotate_backuper@firma.ru'
      'mailfrom': 'pyrotate_on_%s@firma.ru' % (ourhost,)
      where 'ourhost' variable gets host name in program.
      If not exist, messages will not be sent

  mailto - e-mail of a receiver,
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
