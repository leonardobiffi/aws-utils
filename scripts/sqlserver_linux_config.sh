#!/bin/bash
#
# Ubuntu 16.04 - SQL Server Web 2017
#
# Feito por: Leonardo Biffi

mkdir /SQL
mkdir /SQL/data
mkdir /SQL/log
mkdir /SQL/dump
mkdir /SQL/backup

chown -R mssql /SQL
chgrp -R mssql /SQL

export PATH="$PATH:/opt/mssql-tools/bin"

/opt/mssql/bin/mssql-conf set filelocation.defaultdatadir /SQL/data
/opt/mssql/bin/mssql-conf set filelocation.defaultlogdir /SQL/log
/opt/mssql/bin/mssql-conf set filelocation.defaultdumpdir /SQL/dump
/opt/mssql/bin/mssql-conf set filelocation.errorlogfile /SQL/log/errorlog
/opt/mssql/bin/mssql-conf set filelocation.defaultbackupdir /SQL/backup

systemctl stop mssql-server

/opt/mssql/bin/mssql-conf set-sa-password

systemctl start mssql-server

systemctl enable mssql-server


sqlcmd -S localhost -U sa



Boa tarde,
Segue o acesso ao SQL Server
IP: 52.44.255.110
user: sa
password: VQPKnY7W