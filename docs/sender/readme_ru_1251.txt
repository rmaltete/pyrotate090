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
  - �������������� � Python v2.7
  - �������� �������� "sleeping"
  - SMTP ������ ����� ��������� ������ � ���� "server:port" 
  - ��������� ��� ����� ��������� ������ ����� "ascii"

v0.8 changes:
  - ��������� ��������� ������

v0.4 changes:
  - �������������� ��� ������ � Linux ���� (��� � � Windows)
  - ������ ������������ SMTP���� RFC���� ��� ������� ����������� ������ ����������� ������

parameter's list:

from_adr, to_adr, subj='', body='', encoding1='ascii', encoding2='ascii', srvr='localhost', name='', password='', debug=0, sleeping=0):

  from_adr - ����� �����������
  to_adr - ����� ����������
  ���� ���������
  ����� ���������
  encoding1 - ������� ��������� ���� � ������ ������ (��������� ascii)
  encoding2 - ��������� ���� � ������ ������, � ������� ���������� ��������� (��������� ascii)
  srvr - SMTP ������ (��������� localhost) � ���� "server" ��� "server:port"
  name - ����� ��� SMTP-��������������, ��������� '' (�����)
  password - ������ SMTP-��������������, ��������� '' (�����)
  debug - if != 0, will print all SMTP session on console
  sleeping - ���������� ������ ��� �������� ����� �������� ���������,
    ��������� 0 - ��� ��������� ����� ���������� � �� �������, ������� 
    ���������� �������� �� ����������� ����� ���������� � ������ ���������
    � ������������ �������� �������

��� ������� �� ��������� ������ ��������� ������ ���� � ����� �������:
    from_adr
    to_adr
    subject
    text
    encoding1
    encoding2
    srvr
