---
layout: post
title: "Ubuntu: Changing MySQL Default Data Directory."

---

I have just installed MySQL on Ubuntu virtual machine, and I wanted 
to change MySQL default data directory ( datadir ). The first time, 
I failed, causing MySQL not enable to start at all. I had to reverse 
it back, getting MySQL to work again. And this is my documentation 
of my second attempt.

The new data directory is **/home/behai/database/**.

What I have found during second and successful attempt are:

* I do not have to disable AppArmor.
   
* I do not have to change permissions for the new data directory.

| ![015-01.png](https://behainguyen.files.wordpress.com/2022/04/015-01.png) | 
|:--:| 
| *MySQL showing new datadir.* |

### The Environment

**Ubuntu**
: Ubuntu 20.04.4 LTS. Release: 20.04. Codename: focal

**MySQL**
: mysql  Ver 8.0.28-0ubuntu0.20.04.3 for Linux on x86_64 ((Ubuntu))

**Oracle VM VirtualBox**
: Version 6.1.32 r149290 (Qt5.6.2)

### Backing Up Config Files

The following config files are to be modified. Their original copies
should be back up elsewhere first:

1. /etc/mysql/mysql.conf.d/mysqld.cnf

2. /etc/apparmor.d/tunables/alias

3. /etc/apparmor.d/usr.sbin.mysqld

### References

I have done this in production environments before, but only for Windows. 
This was the first time I tried on Linux. I did study the process beforehand,
and looking for info to troubleshoot problems as they came about.

* [https://www.digitalocean.com/community/tutorials/how-to-move-a-mysql-data-directory-to-a-new-location-on-ubuntu-16-04](https://www.digitalocean.com/community/tutorials/how-to-move-a-mysql-data-directory-to-a-new-location-on-ubuntu-16-04){:target="_blank"}.

  This is my primary reference. But it appears to have some outdated info 
  ( in Step 3 ), and it also seems to miss a step too: updating AppArmor 
  profile for MySQL.

* [https://developpaper.com/ubuntu-16-04-changing-mysql-default-data-storage-directory/](https://developpaper.com/ubuntu-16-04-changing-mysql-default-data-storage-directory/){:target="_blank"}.

  This is a copy of the above DigitalOcean post, it updates Step 3 -- 
  confirming the error I had when trying it the first time.
  
* [https://stackoverflow.com/questions/63075272/mysql-8-0-ubuntu-server-failed-to-start-after-moving-datadir](https://stackoverflow.com/questions/63075272/mysql-8-0-ubuntu-server-failed-to-start-after-moving-datadir){:target="_blank"}.

  This post brings about the awareness of the *AppArmor profile for MySQL* in 
  the discussion of *Mandatory Access Control (MAC)* -- apart from that, it 
  does not help me any further. They also mention disable AppArmor -- which 
  **I do not have to do to get MySQL working with the changed data directory**.

* [https://askubuntu.com/questions/1249792/ubuntu-20-04-mysql-datadir-permissions-errno-13](https://askubuntu.com/questions/1249792/ubuntu-20-04-mysql-datadir-permissions-errno-13){:target="_blank"}.

  This post describes the problem I had almost identically. The author also mentions
  *AppArmor profile for MySQL* and lists his modifications in the post: 
  **I use this info in this post**. They also discuss changing files and directories 
  permissions, which **I do not have to do.**

* [https://severalnines.com/database-blog/how-configure-apparmor-mysql-based-systems-mysqlmariadb-replication-galera](https://severalnines.com/database-blog/how-configure-apparmor-mysql-based-systems-mysqlmariadb-replication-galera){:target="_blank"}.

  This post discusses the *AppArmor profile for MySQL* and how to reload it after updating
  the config file. **Reloading this config requires root user logging in.**  

### Step by Step Procedure

Please note, except for the reload command in *Step 8*, which runs under Ubuntu 
**root** user; all others should run under the user created during Ubuntu 
installation.

#### 1. Verify datadir:

Run the following command:

```
$ mysql -u root -p
```

After logging to MySQL, run:

```
mysql> select @@datadir;
```

My default installation of MySQL shows **/var/lib/mysql/**.

#### 2. Shut MySQL down and verify:

To shut down:

```
$ sudo systemctl stop mysql
```

To verify that it has been shut down:

```
$ systemctl status mysql
```

#### 3. Synch data: 

**Note /database/ DOES NOT exist under /home/behai/** yet.

This command synch data from **/var/lib/mysql** to new directory
**/home/behai/database/**:

```
$ sudo rsync -av /var/lib/mysql /home/behai/database
```

Note the actual **datadir** is **/home/behai/database/mysql/**.

#### 4. Verify **/home/behai/database/mysql/** exists:

Use Unix command:

```
ls -l
```

to verify that:

* **/database/mysql/** exists under **/home/behai/**.

* **/database/mysql/** owner is user **mysql**.

#### 5. Rename original datadir for backup purpose:

Run this command:

```
$ sudo mv /var/lib/mysql /var/lib/mysql.bak
```

#### 6. Update MySQL config file:

Update MySQL config file with new data directory. To edit, 
run this command:

```
$ sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

Add the below line under **[mysqld]** section:

```
datadir=/home/behai/database/mysql
```

**Note: no ending '/'!**

#### 7. Configuring AppArmor Access Control Rules:

Edit the following config file:

```
$ sudo nano /etc/apparmor.d/tunables/alias
```

Add the following line at the end of the file:

```
alias /var/lib/mysql/ -> /home/behai/database/mysql/,
```

Do **note the last ending comma ( , )**. Ensure getting it 
correctly, do not miss the comma &#128517;!


Then restart AppArmor with command:

```
$ sudo systemctl restart apparmor
```

#### 8. Update AppArmor Profile: 

**Note the reload command will need to be run with root user.**

Update config file:

```
$ sudo nano /etc/apparmor.d/usr.sbin.mysqld
```

Find the comment line **# Allow data dir access**, and add lines
*/home/behai/database/mysql/ r,* and */home/behai/database/mysql/** rwk,*. 
This whole section should look like:

```
# Allow data dir access
/var/lib/mysql/ r,
/home/behai/database/mysql/ r,
/var/lib/mysql/** rwk,
/home/behai/database/mysql/** rwk,
```

**Note the ending '/'** in **/home/behai/database/mysql/** and the comma ( , ) 
after each line! Don't miss them.

Log in with user **root** and run the reload command:

```
$ apparmor_parser -r -T /etc/apparmor.d/usr.sbin.mysqld
```

#### 9. To by pass: /usr/share/mysql/mysql-systemd-start

See the aforementioned [DigitalOcean post](https://www.digitalocean.com/community/tutorials/how-to-move-a-mysql-data-directory-to-a-new-location-on-ubuntu-16-04){:target="_blank"} 
for detail explanation. Run the below command:

```
$ sudo mkdir /var/lib/mysql/mysql -p
```

#### 10. Start MySQL:

Start MySQL with the command:

```
$ sudo systemctl start mysql
```

If there are no errors reported, go ahead and verify that MySQL 
has actually started:

```
$ sudo systemctl status mysql
```

#### 11. Verify new datadir takes effect:

Run the following command:

```
$ mysql -u root -p
```

After logging to MySQL, run:

```
mysql> select @@datadir;
```

It should now show **/home/behai/database/mysql/**.

### Some Notes on Error Checking

During my first failed attempt, Ubuntu routinely gives the following
two error checking commands:

```
$ systemctl status mysql.service
```

```
$ journalctl -xe
```

I find them relevant in getting the sense of actual problems.

And also there is the actual MySQL error log file, which can be viewed
via different methods. **vi** is time-honoured &#128512;:

```
$ vi /var/log/mysql/error.log
```

And there is this very informative command:

```
$ sudo -u mysql /usr/sbin/mysqld
```

The first time I ran it, while having problem during my first attempt,
it gave the following info:

```
behai@GUI-Ubuntu:~$ sudo -u mysql /usr/sbin/mysqld
2022-04-09T15:14:42.358229Z 0 [Warning] [MY-010091] [Server] Can't create test file /home/behai/database/mysqld_tmp_file_case_insensitive_test.lower-test
2022-04-09T15:14:42.358292Z 0 [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.0.28-0ubuntu0.20.04.3) starting as process 7758
2022-04-09T15:14:42.360325Z 0 [Warning] [MY-010091] [Server] Can't create test file /home/behai/database/mysqld_tmp_file_case_insensitive_test.lower-test
2022-04-09T15:14:42.360334Z 0 [Warning] [MY-010159] [Server] Setting lower_case_table_names=2 because file system for /home/behai/database/ is case insensitive
2022-04-09T15:14:42.360557Z 0 [ERROR] [MY-013276] [Server] Failed to set datadir to '/home/behai/database/' (OS errno: 13 - Permission denied)
2022-04-09T15:14:42.360674Z 0 [ERROR] [MY-010119] [Server] Aborting
2022-04-09T15:14:42.360767Z 0 [System] [MY-010910] [Server] /usr/sbin/mysqld: Shutdown complete (mysqld 8.0.28-0ubuntu0.20.04.3)  (Ubuntu).
behai@GUI-Ubuntu:~$
```

But when I tried it subsequently, there was no output! I have not figured it out yet.

That is about it. I hope you find this useful somehow and thank you for visiting.