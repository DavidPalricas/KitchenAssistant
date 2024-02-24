@echo off

set SQL_FILE=setup_database.sql
set DB_USER=admin
set DB_PASSWORD=admin

mysql -u %DB_USER% -p%DB_PASSWORD% < %SQL_FILE%

echo Base de dados configurada.
pause
