sender v0.88
send message by smtp server
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

v0.88 changes:
  - протестировано в Python v2.7
  - добавлен параметр "sleeping"
  - SMTP сервер можно указывать теперь в виде "server:port" 
  - умолчания для обеих кодировок теперь стало "ascii"

v0.8 changes:
  - пофиксены некоторые ошибки

v0.4 changes:
  - протестировано для работы в Linux тоже (как и в Windows)
  - полное соответствие SMTPёвым RFCшках для лучшего прохождения сквозь антиспамные филтры

parameter's list:

from_adr, to_adr, subj='', body='', encoding1='ascii', encoding2='ascii', srvr='localhost', name='', password='', debug=0, sleeping=0):

  from_adr - адрес отправителя
  to_adr - адрес получателя
  тема сообщения
  текст сообщения
  encoding1 - входная кодировка темы и текста письма (умолчание ascii)
  encoding2 - кодировка темы и текста письма, в которой посылается сообщение (умолчание ascii)
  srvr - SMTP сервер (умолчание localhost) в виде "server" или "server:port"
  name - логин для SMTP-аутентификации, умолчание '' (пусто)
  password - пароль SMTP-аутентификации, умолчание '' (пусто)
  debug - if != 0, will print all SMTP session on console
  sleeping - количество секунд для задержки после отправки сообщения,
    умолчание 0 - для возможных тупых почтовиков и их админов, которые 
    устраивают антиспам по ограничению числа полученных с адреса сообщений
    в определенный интервал времени

При запуске из командной строки аргументы должны быть в таком порядке:
    from_adr
    to_adr
    subject
    text
    encoding1
    encoding2
    srvr
