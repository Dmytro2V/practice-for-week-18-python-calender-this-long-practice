#postgres setup 
sudo service postgresql status /start/stop/restart
psql:

Creating user

```
$ sudo -u postgres createuser <username>
```


Creating Database
```
$ sudo -u postgres createdb <dbname>
```


Giving the user a password
```
$ sudo -u postgres psql
psql=# alter user <username> with encrypted password '<password>';
```


Granting privileges on database
```
psql=# grant all privileges on database <dbname> to <username> ; 
```
- not working...
instead - ALTER DATABASE name OWNER TO user