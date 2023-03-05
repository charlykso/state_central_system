CREATE DATABASE IF NOT EXISTS central_system_db;
CREATE USER IF NOT EXISTS 'GSC_MYSQL_USER'@'localhost' IDENTIFIED BY = 'GSC_MYSQL_PWD';
-- SET PASSWORD FOR 'GSC_MYSQL_USER'@'localhost' = 'GSC_MYSQL_pwd';
GRANT USAGE ON *.* TO 'GSC_MYSQL_USER'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'GSC_MYSQL_USER'@'localhost';
GRANT ALL PRIVILEGES ON `central_system_db`.* TO 'GSC_MYSQL_USER'@'localhost';
FLUSH PRIVILEGES;

-- to export db
mysqldump -u [username] -p [database name] > [database name].sql
-- to import db
mysql -u [username] -p newdatabase < [database name].sql

GSC_MYSQL_USER=GSC_MYSQL_USER GSC_MYSQL_PWD=GSC_MYSQL_PWD GSC_MYSQL_HOST=localhost GSC_MYSQL_DB=central_system_db python3 -m web_dynamic.app

-- to auto create the tables
GSC_MYSQL_USER=GSC_MYSQL_USER GSC_MYSQL_PWD=GSC_MYSQL_PWD GSC_MYSQL_HOST=localhost GSC_MYSQL_DB=central_system_db python3
from models import storage
storage.reload()
