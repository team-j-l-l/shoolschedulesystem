DROP DATABASE IF EXISTS schoolschedule;

DROP ROLE IF EXISTS manager; 

--创建一个登陆用户，用户名为manager,缺省密码pass

CREATE ROLE manager LOGIN
  ENCRYPTED PASSWORD 'md568cefad35fed037c318b1e44cc3480cf' -- password: pass
  NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE;

--创建一个数据库，用户为manager
CREATE DATABASE schoolschedule WITH OWNER = manager ENCODING = 'UTF8';  
