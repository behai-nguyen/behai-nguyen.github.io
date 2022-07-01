---
layout: post
title: "Synology DS218: MariaDB 10 enabling remote connection."

---

We discuss how to enable remote connection for MariaDB 10.3.32-1040 on 
Synology DS218, DSM 7.1-42661 Update 1. That is, using a Windows 10 
client tool, we are able to connect to a MariaDB database on Synology DS218.

| ![026-feature-image.png](https://behainguyen.files.wordpress.com/2022/07/026-feature-image.png) |
|:--:|
| *Synology DS218: MariaDB 10 enabling remote connection.* |

<p>
We'll carry out the changes with little explanations. Then we'll go into 
detail. But first, please see the <a href="#disclaimer">Disclaimer</a>
below.
</p>

<!--------------------------------------------------------------------------------->

<h2>Table of contents</h2>

<ul>
	<li><a href="#disclaimer">Disclaimer</a></li>

	<li><a href="#environments">Environments</a></li>

	<li><a href="#steps-in-brief">Steps to enable remote access for MariaDB 10</a></li>

	<li><a href="#elaborate-the-steps">Elaborating of the steps outlined previously</a>
		<ul>
			<li><a href="#references">References</a></li>

			<li><a href="#the-main-issues">What have to be done...</a></li>

			<li><a href="#the-config-files">Working out the config files</a></li>

			<li><a href="#first-try-suggested-cnf">First try with /var/packages/MariaDB10/etc/my.cnf</a></li>
			
			<li><a href="#check-skip-networking">Check loaded “skip networking” option</a></li>			

			<li><a href="#attempts-home-my-cnf">Attempts with /var/services/homes/behai/.my.cnf</a></li>

			<li><a href="#subsequent-tries-suggested-cnf">Subsequent tries with /var/packages/MariaDB10/etc/my.cnf</a></li>
			
			<li><a href="#my-port-cnf">/var/packages/MariaDB10/etc/my_port.cnf</a></li>

			<li><a href="#my-port-cnf">/var/packages/MariaDB10/etc/synology.cnf</a></li>
		</ul>
	</li>
	
	<li><a href="#other-system-commands">Other system commands relating to MariaDB 10</a></li>	

	<li><a href="#concluding-remarks">Concluding remarks</a></li>
</ul>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="disclaimer">Disclaimer</a>
</h3>

<ul>
<li style="top-align:5px;">
The procedures discussed in 
this post are of an experimental nature, they've never been tested
for production usage.
</li>

<li style="margin-top:10px;">
I take no responsibilities for any damages or losses resulting from 
applying the procedures outlined in this post. 
</li>
</ul>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="environments">Environments</a>
</h3>

<ol>
<li style="top-align:5px;">
<span class="keyword">
Synology DS218</span> -- it's accessed via its device name
<span class="keyword">
<strong>omphalos-nas-01</strong></span> instead of its IP address.
</li>

<li style="margin-top:10px;">
<span class="keyword">
Windows 10 PC</span> -- it's accessed via its device name 
<span class="keyword">
<strong>DESKTOP-7BA02KU</strong></span> also. It's 
the client machine which we'll enable to remotely connect to
<span class="keyword">
MariaDB 10</span> on 
<span class="keyword">
<strong>omphalos-nas-01</strong></span>. Client tools 
<span class="keyword">
mysql</span> and 
<span class="keyword">
MySQL Workbench 6.3 CE</span> are installed on this machine.
</li>

<li style="margin-top:10px;">
<span class="keyword">
DSM 7.1-42661 Update 1</span>.
</li>

<li style="margin-top:10px;">
MariaDB 10.3.32-1040 -- I installed it on its own from 
<span class="keyword">
Package Center</span>. I did not change any default settings.
This is a fresh install. There are no 
other prior configurations before this.
</li>

<li style="margin-top:10px;">
<span class="keyword">
Synology DSM</span> user 
<span class="keyword">
“behai”</span> is the user I set up when first installed
<span class="keyword">
DSM</span>. This is not the 
<span class="keyword">
Linux</span>
<span class="keyword">
root</span> user.
</li>

<li style="margin-top:10px;">
<span class="keyword">
MariaDB 10</span> user 
<span class="keyword">
“behai”</span> is the user I set up to allow remote access to
<span class="keyword">
MariaDB 10</span> on the 
<span class="keyword">
Synology DS218</span> box. This is not the 
<span class="keyword">
MariaDB 10</span> 
<span class="keyword">
root</span> user.
</li>
</ol>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="steps-in-brief">Steps to enable remote access for MariaDB 10</a>
</h3>

<p>
❶ Check 
<span class="keyword">
bind-address</span> -- on my installation, the default configuration
file for 
<span class="keyword"> 
MariaDB 10</span> is:
</p>

```
/usr/local/mariadb10/etc/mysql/my.cnf
```

<p>
This file already has 
<span class="keyword">
bind-address</span> under
<span class="keyword">
[mysqld]</span> set to the required value. I didn't have to do anything
to <span class="keyword">
bind-address</span>.
</p>

```
...
[mysqld]
bind-address = 0.0.0.0
...
```

<p>
❷ Turn <span class="keyword">
skip_networking</span> to 
<span class="keyword">
OFF</span> -- modify:
</p>

```
/var/packages/MariaDB10/etc/synology.cnf
```

<p>
Under 
<span class="keyword">
[mysqld]</span>, change 
<span class="keyword">
skip_networking</span> to 
<span class="keyword">
0</span>. The final content of
<span class="keyword">
/var/packages/MariaDB10/etc/synology.cnf</span> is listed below:
</p>

```
# DO NOT EDIT THIS FILE !!!
# You can change the port on user interface of MariaDB10.
# Please add other custom configuration to /var/packages/MariaDB10/etc/my.cnf
[mysqld]
skip_networking=0
```

<p>
❸ Create remote access database and user.
</p>

<p>
From a 
<span class="keyword">
Windows</span> command prompt, run 
<span class="keyword">
SSH</span> to access
<span class="keyword">
DSM</span> command line:
</p>

```
E:\>ssh behai@omphalos-nas-01
```

<p>
Launch 
<span class="keyword">
mysql</span>:
</p>

```
$ mysql -u root -p
```

<p>
Create database:
</p>

```
MariaDB [(none)]> CREATE DATABASE ompdb;
```

<p>
Create <span class="keyword">
MariaDB 10</span> user 
<span class="keyword">
“behai”</span>:
</p>

```
MariaDB [(none)]> CREATE USER 'behai'@'localhost' IDENTIFIED BY '<,U#n*m:5QB3_zbQ';
```

<p>
Grant local and remote access to 
<span class="keyword">
MariaDB 10</span> user 
<span class="keyword">
“behai”</span>:
</p>

```
MariaDB [(none)]> GRANT ALL ON ompdb.* to 'behai'@'localhost' IDENTIFIED BY '<,U#n*m:5QB3_zbQ' WITH GRANT OPTION;
```

```
MariaDB [(none)]> GRANT ALL ON ompdb.* to 'behai'@'DESKTOP-7BA02KU' IDENTIFIED BY '<,U#n*m:5QB3_zbQ' WITH GRANT OPTION;
```

```
MariaDB [(none)]> FLUSH PRIVILEGES;
```

<p>
Verify 
<span class="keyword">
MariaDB 10</span> user 
<span class="keyword">
“behai”</span> has been created, and with allowed access from specified
hosts:
</p>

```
MariaDB [(none)]> SELECT User, Host FROM mysql.user;
```

<p>
There should be two ( 2 ) entries for 
<span class="keyword">
MariaDB 10</span> user 
<span class="keyword">
“behai”</span>:
</p>

```
+-------+-----------------+
| User  | Host            |
+-------+-----------------+
| root  | 127.0.0.1       |
| root  | ::1             |
| behai | desktop-7ba02ku |
| behai | localhost       |
| root  | localhost       |
+-------+-----------------+
5 rows in set (0.001 sec)

MariaDB [(none)]>
```

<p>
❹ Restart 
<span class="keyword"> 
MariaDB 10</span> using the following commands: 
</p>

```
$ sudo synopkg stop MariaDB10
$ sudo synopkg start MariaDB10
$ sudo synopkg status MariaDB10
```

<p>
Remote access should now be enabled.
</p>

<p>
❺ Test remote access
</p>

<p>
⓵ From 
<span class="keyword">
Windows 10 PC</span>, 
<span class="keyword">
<strong>DESKTOP-7BA02KU</strong></span> command prompt, run:
</p>

```
F:\>"C:\Program Files\MySQL\MySQL Server 5.5\bin\mysql" -u behai -p -h omphalos-nas-01
```

<p>
Enter password for <span class="keyword">
“behai”</span>, then run:
</p>

```
mysql> show databases;
```

<p>
We should get the following:
</p>

```
+--------------------+
| Database           |
+--------------------+
| information_schema |
| ompdb              |
+--------------------+
2 rows in set (0.00 sec)

mysql>
```

<p>
⓶ From 
<span class="keyword">
Windows 10 PC</span>, launch 
<span class="keyword">
MySQL Workbench 6.3 CE</span>, create a new connection with:
</p>

<ul>
<li style="margin-top:5px;">Connection Name: 
<span class="keyword">
mariadb-on-nas</span></li>
<li style="margin-top:10px;">Connection Method: 
<span class="keyword">
Standard (TCP/IP)</span></li>
<li style="margin-top:10px;">Hostname: 
<span class="keyword">
omphalos-nas-01</span></li>
<li style="margin-top:10px;">Port: 
<span class="keyword">
3306</span></li>
<li style="margin-top:10px;">Username: 
<span class="keyword">
behai</span></li>
<li style="margin-top:10px;">Password: 
<span class="keyword">
&lt;,U#n*m:5QB3_zbQ</span></li>
<li style="margin-top:10px;">Default Schema: 
<span class="keyword">
ompdb</span></li>
</ul>

<p>
Hit the 
<span class="keyword">
Test Connection</span> button, it should connect. Note that, depending
on your installations, there might be a warning about the client and
the server versions differences, just ignore it.
</p>

<p>
⓷ From 
<span class="keyword">
Synology DS218</span> command line, run:
</p>

```
$ mysql --protocol=tcp --port=3306 --user=behai --password --database ompdb
```

<p>
Enter password. It should connect. Prompt changed to 
<span class="keyword">
MariaDB [ompdb]></span>.
</p>

<p>
⓸ From 
<span class="keyword">
Synology DS218</span> command line, run:
</p>

```
$ mysql --protocol=tcp --host=omphalos-nas-01 --port=3306 --user=behai --password --database ompdb
```

<p>
Enter password. It should connect. Prompt changed to 
<span class="keyword">
MariaDB [ompdb]></span>.
</p>

<p>
This makes sense, since from within, 
<span class="keyword">
<strong>omphalos-nas-01</strong></span> should get translated to 
<span class="keyword">
<strong>127.0.0.1</strong></span> which is 
<span class="keyword">
<strong>localhost</strong></span>.
</p>

<p>
⓹ From 
<span class="keyword">
Synology DS218</span> command line, run:
</p>

```
$ mysql --protocol=tcp --host=127.0.0.1 --port=3306 --user=behai --password --database ompdb
```

<p>
Enter password. It should connect. Prompt changed to 
<span class="keyword">
MariaDB [ompdb]></span>.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="elaborate-the-steps">Elaborating of the steps outlined previously</a>
</h3>

<p>
I've worked with 
<span class="keyword">
MySQL</span> quite in depth before. In 
<span class="keyword">
Windows</span>, I've installed 
<span class="keyword">
MySQL servers</span>, set up replication, automating daily back up
and test restore ( onto different machines ), etc. Some replication
servers were LAN 
<span class="keyword">
Linux</span> 
boxes. I did not set up those 
<span class="keyword">
Linux</span> boxes, 
the extend I've worked on them was modifying configuration files
to make them slave servers: <strong>AND FURTHERMORE, I WAS TOLD 
which configuration files to modify!</strong> I can find my
ways around 
<span class="keyword">
Linux</span>, but it's not my cup of tea. ( During my university 
years, I'd used 
 <span class="keyword">
Unix</span> for six [ 6 ] straight years. ) 
</p>

<p>
In 
<span class="keyword">
Windows</span>, we've set up 
<span class="keyword">
MySQL servers</span> for remote access both in-house ( LAN ) and
as dedicated private database servers ( i.e. also LAN ) within data 
centres -- I do not recall we'd any major problems.
</p>

<p>
This's the first time I've attempted this on a 
<span class="keyword">
Linux</span> box. 
There's just no answer from Synology... But there're plenty of
posts on the subject, related to different flavours of 
<span class="keyword">
Linux</span>. I'm listing below the main posts that I've used. 
</p>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="references">References</a>
</h4>

<ol>
<li style="top-align:5px;">
<a href="https://mariadb.com/kb/en/configuring-mariadb-for-remote-client-access/"
title="Configuring MariaDB for Remote Client Access"
target="_blank">Configuring MariaDB for Remote Client Access</a>
</li>

<li style="top-align:10px;">
<a href="https://stackoverflow.com/questions/580331/determine-which-mysql-configuration-file-is-being-used"
title="Determine which MySQL configuration file is being used"
target="_blank">Determine which MySQL configuration file is being used</a>
</li>

<li style="top-align:10px;">
<a href="https://mariadb.com/kb/en/configuring-mariadb-with-option-files/"
title="Configuring MariaDB with Option Files"
target="_blank">Configuring MariaDB with Option Files</a>
</li>

<li style="top-align:10px;">
<a href="https://stackoverflow.com/questions/22283422/set-mysql-skip-networking-to-off"
title="Set mysql skip-networking to off"
target="_blank">Set mysql skip-networking to off</a>
</li>

<li style="top-align:10px;">
<a href="https://stackoverflow.com/questions/64320136/error-2002-hy000-cant-connect-to-mysql-server-on-192-168-1-15-115"
title="ERROR 2002 (HY000): Can't connect to MySQL server on '192.168.1.15' (115)"
target="_blank">ERROR 2002 (HY000): Can't connect to MySQL server on '192.168.1.15' (115)</a>
</li>

<li style="top-align:10px;">
<a href="https://askubuntu.com/questions/1009175/mariadb-10-0-33-configuring-mariadb-for-remote-client-access"
title="MariaDB 10.0.33 Configuring MariaDB for Remote Client Access"
target="_blank">MariaDB 10.0.33 Configuring MariaDB for Remote Client Access</a>
</li>

<li style="top-align:10px;">
<a href="https://websiteforstudents.com/allow-remote-access-to-mariadb-database-server-on-ubuntu-18-04/"
title="Allow Remote Access to MariaDB Database Server on Ubuntu 18.04"
target="_blank">Allow Remote Access to MariaDB Database Server on Ubuntu 18.04</a>
</li>
</ol>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="the-main-issues">What have to be done...</a>
</h4>

<p>
From the existing posts, it seems to be a straightforward configuration 
process, albeit commands' differences across 
<span class="keyword">
Linux</span> flavours. For me, the main issues were: 
</p>

<ol>
<li style="top-align:5px;">Identify the right config file to update. 
They're different across 
<span class="keyword">
Linux</span> distros. And unlike in 
<span class="keyword">
Windows</span>, there's only a single 
<span class="keyword">
.ini file</span> used. In 
<span class="keyword">
Linux</span>, there can several different config files loaded 
by the running instance.
</li>

<li style="top-align:10px;">
Change 
<span class="keyword">
bind-address</span> to
<span class="keyword">
0.0.0.0</span>; add entry 
<span class="keyword">
skip-bind-address</span>; change 
<span class="keyword">
skip_networking</span> and / or 
<span class="keyword">
skip-networking</span> to 
<span class="keyword">
0</span>.
</li>

<li style="top-align:10px;">
Possibly adding a firewall rule to allow access to 
<span class="keyword">
MariaDB 10</span>'s port of
<span class="keyword">
3306</span>.
</li>
</ol>

<p>
Also, there're some inconsistencies among the existing posts, notably 
for me:
</p>

<ol>
<li style="top-align:5px;">
<span class="keyword">
skip_networking</span> and 
<span class="keyword">
skip-networking</span> -- underscore ( _ ) and hyphen ( - ).
</li>

<li style="top-align:10px;">
<span class="keyword">
skip-bind-address</span> -- some posts mention this, some don't.
</li>
</ol>

<p>
These're not major problems. We can progressively eliminate them 
via trial and error. The main problem's identifying the right 
config file. 
</p>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="the-config-files">Working out the config files</a>
</h4>

<p>
The below command lists files where default options are loaded from:
</p>

```
$ mysql --verbose --help | grep -A 1 "Default options"
```

<p>
It gives the following output:
</p>

```
Default options are read from the following files in the given order:
/usr/local/mariadb10/etc/mysql/my.cnf ~/.my.cnf
behai@omphalos-nas-01:~$
```

<ul>
<li style="top-margin:5px;">
<span class="keyword">
/usr/local/mariadb10/etc/mysql/my.cnf</span> is the default installation file.
</li>

<li style="top-margin:10px;">
<span class="keyword">
~/.my.cnf</span> -- in my understanding, its full path is $HOME, which
is 
<span class="keyword">
/var/services/homes/behai/.my.cnf</span>. It does not exist.
</li>
</ul>

```
First lines and last lines of /usr/local/mariadb10/etc/mysql/my.cnf:
```

```
# DO NOT EDIT THIS FILE !!!
# You can change the port on user interface of MariaDB10.
# Please add other custom configuration to /var/packages/MariaDB10/etc/my.cnf
#
[client]
socket = /run/mysqld/mysqld10.sock

[mysqld]
bind-address = 0.0.0.0
socket = /run/mysqld/mysqld10.sock
...
!include /var/packages/MariaDB10/etc/my.cnf
!include /var/packages/MariaDB10/etc/my_port.cnf
!include /var/packages/MariaDB10/etc/synology.cnf
```

<p>
The instructions on the first three ( 3 ) lines are very clear. 
The target config file is 
<span class="keyword">
/var/packages/MariaDB10/etc/my.cnf</span>.
</p>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="first-try-suggested-cnf">First try with /var/packages/MariaDB10/etc/my.cnf</a>
</h4>

<p>
<span class="keyword">
/var/packages/MariaDB10/etc/my.cnf</span> did not exist. I created
it with the following content:
</p>

```
[mysqld]
skip-networking=0
skip-bind-address
```

<p>
Then restarted 
<span class="keyword"> 
MariaDB 10</span> for the change to take effect. From here onwards,
whenever we mention a config file changed or created, it's implicit
that we restarted 
<span class="keyword"> 
MariaDB 10</span> immediately.
</p>

<p>
Please note 
<span class="keyword">
<strong>skip-networking</strong></span> -- it was a 
<strong>- ( hyphen )</strong> in between. I restarted 
<span class="keyword">
MariaDB 10</span> -- needless to say, it did not work. Not realising
my mistake, I went ahead and set up Firewall rule: 
under <span style="font-weight:bold;">Control Panel > Security > Firewall tab</span>.
Still did not work. I played around with this Firewall rule a few times, still 
did not work! I am confident that I've got the Firewall rule right, 
since this was a simple rule.
</p>

<p>
<strong>
I removed 
<span class="keyword">
/var/packages/MariaDB10/etc/my.cnf</span>.
</strong>
</p>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="check-skip-networking">Check loaded “skip networking” option</a>
</h4>

<p>
Based on one of the posts that I've come across, we can use
<span class="keyword">
mysql command line</span> tool to query 
<strong>skip_networking</strong> value</span>: 
<strong>_ ( underscore )</strong> in between. Run:
</p>

```
$ mysql -u root -p
```

<p>Then, run:</p>

```
MariaDB [(none)]> SHOW VARIABLES LIKE 'skip_networking';
```

<p>
The output was:
</p>

```
+-----------------+-------+
| Variable_name   | Value |
+-----------------+-------+
| skip_networking | ON    |
+-----------------+-------+
1 row in set (0.003 sec)

MariaDB [(none)]>
```

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="attempts-home-my-cnf">Attempts with /var/services/homes/behai/.my.cnf</a>
</h4>

<p>
At this point, the Firewall rule was still in place.
</p>

<p>
I created 
<span class="keyword">
/var/packages/MariaDB10/etc/my.cnf</span>, and tried different contents:
</p>

```
[mysqld]
bind-address=0.0.0.0
skip_networking=0
skip-bind-address
```

<p>
I couldn't remember why I did include 
<span class="keyword">
bind-address</span>! Then:
</p>

```
[mysqld]
skip_networking=0
skip-bind-address
```

<p>
Finally:
</p>

```
[mysqld]
skip_networking=0
```

<p>
None worked. 
<span class="keyword">
skip_networking</span> was still
<span class="keyword">
ON</span>.
</p>

<p>
<strong>
I removed 
<span class="keyword">
/var/services/homes/behai/.my.cnf</span>.
</strong>
</p>


<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="subsequent-tries-suggested-cnf">Subsequent tries with /var/packages/MariaDB10/etc/my.cnf</a>
</h4>

<p>
At this point, the Firewall rule was still in place.
</p>

<p>
I recreated
<span class="keyword">
/var/packages/MariaDB10/etc/my.cnf</span>, and tried with same contents
as in previous section <a href="#attempts-home-my-cnf">
Attempts with /var/services/homes/behai/.my.cnf</a>.
</p>

<p>
It did not work.
</p>

<p>
<strong>
I removed 
<span class="keyword">
/var/packages/MariaDB10/etc/my.cnf</span>.
</strong>
</p>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="my-port-cnf">/var/packages/MariaDB10/etc/my_port.cnf</a>
</h4>

<p>
Recall from section 
<a href="#the-config-files">Working out the config files</a>, the 
last three ( 3 ) lines of the default config file are:
</p>

```
Last three lines of /usr/local/mariadb10/etc/mysql/my.cnf:
```

```
...
!include /var/packages/MariaDB10/etc/my.cnf
!include /var/packages/MariaDB10/etc/my_port.cnf
!include /var/packages/MariaDB10/etc/synology.cnf
```

<p>
Up to this point, I've not looked at either
<span class="keyword">
/var/packages/MariaDB10/etc/my_port.cnf</span> or
<span class="keyword">
/var/packages/MariaDB10/etc/synology.cnf</span>.
</p>

```
Content of /var/packages/MariaDB10/etc/my_port.cnf
```

```
# DO NOT EDIT THIS FILE !!!
# You can change the port on user interface of MariaDB10.
# Please add other custom configuration to /var/packages/MariaDB10/etc/my.cnf
[mysqld]
port=3306
[client]
port=3306
```

<p>
It's easy enough to understand... Let's look at
<span class="keyword">
/var/packages/MariaDB10/etc/synology.cnf</span> next.
</p>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="my-port-cnf">/var/packages/MariaDB10/etc/synology.cnf</a>
</h4>

<p>
At this point, the Firewall rule was still in place.
</p>

```
Content of /var/packages/MariaDB10/etc/synology.cnf
```

```
# DO NOT EDIT THIS FILE !!!
# You can change the port on user interface of MariaDB10.
# Please add other custom configuration to /var/packages/MariaDB10/etc/my.cnf
[mysqld]
skip_networking=1
```

<p>
So I made the change as discussed previously in 
<a href="#steps-in-brief">Steps to enable remote access for MariaDB 10 | 
❷ Turn <span class="keyword">
skip_networking</span> to 
<span class="keyword">
OFF</span></a>; then restarted the server.
</p>

<p>
<a href="#check-skip-networking">Check loaded “skip networking” option</a>
now shows 
<span class="keyword">
skip_networking</span> is 
<span class="keyword">
OFF</span>.
</p>

<p>
Next, I tried to connect to it from my 
<span class="keyword">
Windows</span> machine. It works. <strong>Next, I proceeded to 
remove the Firewall rule. I have no Firewall rule at all</strong>. 
Finally, I carried out all the tests as discussed in 

<a href="#steps-in-brief">Steps to enable remote access for 
MariaDB 10 | ❺ Test remote access</a>.
</p>

<p>
In summary, there is only a single change needed! It took me a lot of hours
to get it -- not all wasted: I've learned some other stuff along with the 
hours spending on it.
</p>

<p>
Another point, I can't help but feel that <strong>SYNOLOGY'S INLINE DOCUMENTATIONS
IN THOSE CONFIGURE FILES ARE POSSIBLY MISLEADING</strong>?
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="other-system-commands">Other system commands relating to MariaDB 10</a>
</h3>

<p>
❶ The below command shows the starting arguments:
</p>

```
$ sudo mysql --print-defaults
```

<p>Output:</p>

```
mysql would have been started with the following arguments:
--socket=/run/mysqld/mysqld10.sock --no-auto-rehash --port=3306
behai@omphalos-nas-01:~$
```

<p>
❷ Query 
<span class="keyword">
MariaDB 10</span> services and port numbers:
</p>

```
$ cat /etc/services | grep mysql*
```

<p>Output:</p>

```
mysql           3306/tcp
mysql           3306/udp
mysql-proxy     6446/tcp                        # MySQL Proxy
mysql-proxy     6446/udp
behai@omphalos-nas-01:~$
```

<p>
❸ Query 
<span class="keyword">
MariaDB 10</span> processes info:
</p>

```
$ ps xa | grep mysqld
```

<p>Output:</p>

```
  347 ?        S      0:00 /bin/sh /usr/local/mariadb10/bin/mysqld_safe --datadir=/var/packages/MariaDB10/target/mysql --pid-file=/run/mysqld/mysqld10.pid
  502 ?        Sl     0:05 /usr/local/mariadb10/bin/mysqld --basedir=/usr/local/mariadb10 --datadir=/var/packages/MariaDB10/target/mysql --plugin-dir=/usr/local/mariadb10/lib/mysql/plugin --user=mysql --log-error=/var/packages/MariaDB10/target/mysql/omphalos-nas-01.err --pid-file=/run/mysqld/mysqld10.pid --socket=/run/mysqld/mysqld10.sock --port=3306
10131 pts/0    S+     0:00 grep --color=auto mysqld
behai@omphalos-nas-01:~$
```

<p>
❹ Some other <span class="keyword">
netstat</span> commands:
</p>

```
$ sudo netstat -anp | grep 3306
$ netstat -na | grep mysql*
$ netstat -ln | grep mysql
```

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="concluding-remarks">Concluding remarks</a>
</h3>

<p>
This process is an experiment to satisfy my own curiosities.
Also, there've been a lot of questions on this topic, it's satisfying 
to figure out the answer. Also, it's always good to have a separate 
development database server. Please note, I've ignored all security
considerations. I'll think about it later.
</p>

<p>
I'm not at all sure if I've got everything correctly... I've included
the detail description of my working progress with the hope that it 
might help with similar problems on some other 
<span class="keyword">
Linux</span> distros.
</p>

<p>
Thank you for reading... and I hope you find this post helpful somehow.
</p>
