---
layout: post
title: "Docker on Ubuntu 22.10: running mysql:8.0.34-debian with custom config, socket, database and log files reside on host machine."

description: We'll look at how to run the official mysql:8.0.34-debian image on Ubuntu 22.10, which we'll store most of the run-time files on our own Ubuntu 22.10 host machine, in locations of our own dictation. These include the custom config file, the database files, the MySQL socket files, and the log files. Finally, we verify that the setup works.

tags:
- Docker
- MySQL
- ERROR 2002 (HY000)
- Ubuntu
---

<em style="color:#111;">We'll look at how to run the official <code>mysql:8.0.34-debian</code> image on Ubuntu 22.10, which we'll store most of the run-time files on our own Ubuntu 22.10 host machine, in locations of our own dictation. These include the custom config file, the database files, the MySQL socket files, and the log files. Finally, we verify that the setup works.</em>

| ![084-feature-image.png](https://behainguyen.files.wordpress.com/2023/09/084-feature-image.png) |
|:--:|
| *Docker on Ubuntu 22.10: running mysql:8.0.34-debian with custom config, socket, database and log files reside on host machine.* |

I've previously written about <code>mysql:8.0.30-debian</code> <a href="https://hub.docker.com/_/mysql" title="mysql Docker Official Image" target="_blank">Docker Official Image</a> on Windows 10 Pro:

<ol>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/08/09/docker-on-windows-10-running-mysql8-0-30-debian-with-a-custom-config-file/" title="Docker on Windows 10: running mysql:8.0.30-debian with a custom config file." target="_blank">Docker on Windows 10: running mysql:8.0.30-debian with a custom config file.</a>
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/10/21/docker-on-windows-10-mysql8-0-30-debian-log-files/" title="Docker on Windows 10: mysql:8.0.30-debian log files" target="_blank">Docker on Windows 10: mysql:8.0.30-debian log files</a>
</li>
</ol>

Afterward, I'd also set it up to run on Ubuntu 22.10, but without log files written to the host machine. I've reinstalled Ubuntu 22.10 a fair while back, but only attempted to set up <code>mysql:8.0.30-debian</code> Docker image container last week. It took me about an hour to consolidate the instructions. I'm writing this post so that in the future, I've something to go back to should the need arise.

<em>In this post, we are using a newer image <strong> <code>mysql:8.0.34-debian</code></strong>.</em>

<strong>Please note:</strong> <code>docker</code> commands in this post are run with the <code>--rm</code> flag, that means <strong><em>when we stop the <code>docker container</code>, we expect it to be removed as well.</em></strong>

<strong><em>Also, the post's longer than I've anticipated, but after the final draft's been completed,</em> I have re-exercised all the steps twice, on average, it takes around 20 (twenty) minutes to complete all the steps.</strong>

<h2>Table of contents</h2>

<ul>
    <li style="margin-top:10px;">
        <a href="#pulling-docker-image">Prepare the <code>mysql:8.0.34-debian</code> Image</a>
	</li>

    <li style="margin-top:10px;">
        <a href="#custom-config-file">The Custom Config File on Ubuntu 22.10</a>

	    <ul>
            <li style="margin-top:10px;">
                <a href="#config-file-location-content">The Location and Content</a>
            </li>

            <li style="margin-top:10px;">
                <a href="#config-permissions-mounting">Permissions and Mounting</a>
            </li>
	    </ul>
	</li>

    <li style="margin-top:10px;">
        <a href="#socket-database-dirs-log-files">The Socket and the Database Directories</a>

	    <ul>
            <li style="margin-top:10px;">
                <a href="#socket-directory">MySQL Socket and Mounting the Socket Directory to Host Machine</a>
            </li>

            <li style="margin-top:10px;">
                <a href="#database-directory">Mounting the Database Directory to Host Machine</a>
            </li>
	    </ul>
	</li>

    <li style="margin-top:10px;">
        <a href="#config-log-files-verification">Verify Custom Config Items, and Log Files Created</a>

	    <ul>
            <li style="margin-top:10px;">
                <a href="#mysql-socket-files">Verify MySQL Socket Files</a>
            </li>

            <li style="margin-top:10px;">
                <a href="#database-and-log-files">Verify Database Files and Log Files</a>
            </li>

            <li style="margin-top:10px;">
                <a href="#config-items-auth-log-bin">Verify <code>default_authentication_plugin</code> and <code>log_bin_trust_function_creators</code></a>
            </li>

            <li style="margin-top:10px;">
                <a href="#check-general-log-file">Checking Out <code>general_log.log</code> File</a>
            </li>
	    </ul>
	</li>

    <li style="margin-top:10px;">
        <a href="#allow-traffic-throu-port-3306">Allow Traffic Through MySQL port <code>3306</code></a>
	</li>

    <li style="margin-top:10px;">
        <a href="#win10-pro-mysql-workbench-connection">Test With a Remote Connection</a>
	</li>

    <li style="margin-top:10px;">
        <a href="#further-test-with-a-complete-database">Further Test Via Setting Up a Complete Database</a>

	    <ul>
            <li style="margin-top:10px;">
                <a href="#database-creation-population">Database Creation and Population</a>
            </li>

            <li style="margin-top:10px;">
                <a href="#remote-stored-procs-creations">Remotely Create Stored Procedures on the Just Setup Database</a>
            </li>
	    </ul>
	</li>

    <li style="margin-top:10px;">
        <a href="#my-other-docker-posts">Other Docker Posts Which I've Written</a>
	</li>
</ul>

<h3 style="color:teal;">
  <a id="pulling-docker-image">Prepare the <code>mysql:8.0.34-debian</code> Image</a>
</h3>

Pulling the Docker image from the registry with:

```
$ sudo docker image pull mysql:8.0.34-debian
```

After finishing pulling, we can verify that the image has been loaded:

```
$ sudo docker images
```

<code>mysql:8.0.34-debian</code> should be in the available image list:

<div class="language-plaintext highlighter-rouge">
<div class="highlight">
<pre class="highlight"><code>REPOSITORY         TAG             IMAGE ID       CREATED        SIZE
<span style="color:blue;"><strong>mysql              8.0.34-debian   beb1bec24656   12 days ago    601MB</strong></span>
bh-aust-postcode   latest          90d2986553e0   2 months ago   980MB
postgres           latest          a26eb6069868   9 months ago   379MB
</code></pre></div></div>

We can save the image to disk with:

```
$ sudo docker save mysql:8.0.34-debian --output /home/behai/Public/mysql-8-0-34-debian.tar
```

Later on, if for some reason, we need the image again, we don't need to download it, we can load it up with:

```
$ sudo docker load --input /home/behai/Public/mysql-8-0-34-debian.tar
```

<h3 style="color:teal;">
  <a id="custom-config-file">The Custom Config File on Ubuntu 22.10</a>
</h3>

<h4 style="color:teal;">
  <a id="config-file-location-content">The Location and Content</a>
</h4>

The <a id="custom-config-file">custom config file</a> is <code>/home/behai/Public/database/mysql-config/mysql-docker.cnf</code>. <code>mysql-docker.cnf</code> is the only file I have under <code>/home/behai/Public/database/mysql-config/</code>.

Please note, the above directory is just my personal preference. Manually create the directories and create <code>mysql-docker.cnf</code> using either <code>nano</code>, <code>vi</code> or <code>vim</code>, etc.

```
Content of /home/behai/Public/database/mysql-config/mysql-docker.cnf:
```

```
[mysqld]
default_authentication_plugin=mysql_native_password
log_bin_trust_function_creators=1

# Below contents are updated contents.

# General and slow logging.
log_output=FILE

general_log=1
general_log_file="/var/lib/mysql/general_log.log"

slow_query_log=1
slow_query_log_file="/var/lib/mysql/slow_query.log"
long_query_time=10
log_queries_not_using_indexes=1

# Error Logging.
log_error="/var/lib/mysql/error.err"
```

Please note that <code>/var/lib/mysql/</code> is the database directory, which later on, we'll mount to the directory <code>/home/behai/Public/database/mysql</code> on the host Ubuntu 22.10 machine. That is, all database files and log files will reside in the directory <code>/home/behai/Public/database/mysql</code> on the host machine.

<ul>
<li style="margin-top:10px;">
For <code>default_authentication_plugin</code>, see
<a href="https://dev.mysql.com/doc/refman/8.0/en/upgrading-from-previous-series.html#upgrade-caching-sha2-password-compatibility-issues" title="caching_sha2_password Compatibility Issues and Solutions" target="_blank">caching_sha2_password Compatibility Issues and Solutions</a>.
For <code>log_bin_trust_function_creators</code>, see
<a href="https://dev.mysql.com/doc/refman/8.0/en/stored-programs-logging.html" title="25.7 Stored Program Binary Logging" target="_blank">25.7 Stored Program Binary Logging</a>.
</li>

<li style="margin-top:10px;">
For log files, see
<a href="https://dev.mysql.com/doc/refman/8.0/en/log-destinations.html" title="5.4.1 Selecting General Query Log and Slow Query Log Output Destinations" target="_blank">5.4.1 Selecting General Query Log and Slow Query Log Output Destinations</a>.
For the purpose of this post, I turn on a lot of logs. This would not be appropriate in
a production environment. I'm aware of that.
</li>
</ul>

<h4 style="color:teal;">
  <a id="config-permissions-mounting">Permissions and Mounting</a>
</h4>

The required permissions are: <strong>owner</strong> has <strong>read</strong> and <strong>write</strong>; <strong>groups</strong> and <strong>others</strong> have only <strong>read</strong>. Our <code>/home/behai/Public/database/mysql-config/mysql-docker.cnf</code> must have the same permissions.

The permissions must be set from a running container. We need to mount it so that <code>docker</code> can recognise this external custom config file. We need only the directory, the mounting option is:

```
--mount type=bind,source=/home/behai/Public/database/mysql-config,target=/etc/mysql/conf.d
```

The command to run:

```
$ sudo docker run -d -it --rm --name mysql-docker --mount type=bind,source=/home/behai/Public/database/mysql-config,target=/etc/mysql/conf.d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=pcb.2176310315865259 mysql:8.0.34-debian
```

Now, run the container in the interactive mode with the Bash process to change config file permissions:

```
$ sudo docker exec -it mysql-docker bash
```

Once in the interactive Bash mode, verify that we’re looking at the Ubuntu 22.10 directory, which has only this config file, also note its permissions:

```
# ls -l /etc/mysql/conf.d
```

Change permissions to match the container's custom config file. That is, <strong>owner</strong> has <strong>read</strong> and <strong>write</strong>; <strong>groups</strong> and <strong>others</strong> have only <strong>read</strong>:

```
# cd /etc/mysql/conf.d/
# chmod u+rw-x mysql-docker.cnf
# chmod g+r-wx mysql-docker.cnf
# chmod o+r-wx mysql-docker.cnf
```

Permissions should now be correct. To verify:

```
# ls -l
```

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>root@1e7273c76a2a:/etc/mysql/conf.d# ls -l
total 4
<span style="color:blue;"><strong>-rw-r--r-- 1 1000 1000 425 Sep 18 12:06 mysql-docker.cnf</strong></span>
root@1e7273c76a2a:/etc/mysql/conf.d#
</code></pre></div></div>

<h3 style="color:teal;">
  <a id="socket-database-dirs-log-files">The Socket and the Database Directories</a>
</h3>

In this section, we'll briefly discuss why we need MySQL socket files on the host machine, how to mount this directory. And then we'll discuss mounting the database directory.

Again, please note that all directories created are my own personal preference. You can create them wherever based on your own liking.

<h4 style="color:teal;">
  <a id="socket-directory">MySQL Socket and Mounting the Socket Directory to Host Machine</a>
</h4>

I've carried out this set up process over several iterations. The second time I set it up with <code>mysql:8.0.30-debian</code> is (yes, <em>present tense</em>, since I'm still writing 😂 this post) smooth sailing. When I try <code>mysql:8.0.34-debian</code>, approximately at this point, I could not connect to the container. The error message I get is:

<code><span style="color:red;">
MySQL server is running but I cannot connect : ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/tmp/mysql.sock' (2)
</span></code>

I spend sometimes troubleshoot it, I understand what the problem is, but get nowhere fixing it. I switch back to <code>mysql:8.0.30-debian</code> -- and the same error persists! This does not happen during the second time as mentioned above.

The documentation on the <a href="https://hub.docker.com/_/mysql" title="mysql Docker Official Image" target="_blank">official page</a> does not mention about MySQL socket, but I thought, might be the socket files should be on the host machine also, I try that. It seems to work. <em>I am not at all certain if this is the cause of the problem, or that it is the correct solution.</em> So, please keep that in mind.

<strong>-- I would like to point out that, after completing the final draft of this post, I carry all the steps twice, and everything still works.</strong>

Run the container in the interactive Bash mode, then look in <code>/var/run/mysqld/</code> directory:

```
root@df87897c3326:/etc/mysql/conf.d# ls -l /var/run/mysqld/
```

These are MySQL socket files:

```
total 12
-rw-r----- 1 mysql mysql 2 Sep 20 12:20 mysqld.pid
srwxrwxrwx 1 mysql mysql 0 Sep 20 12:20 mysqld.sock
-rw------- 1 mysql mysql 2 Sep 20 12:20 mysqld.sock.lock
srwxrwxrwx 1 mysql mysql 0 Sep 20 12:20 mysqlx.sock
-rw------- 1 mysql mysql 2 Sep 20 12:20 mysqlx.sock.lock
```

I choose to <a href="https://docs.docker.com/storage/bind-mounts/" title="Bind mounts" target="_blank">bind mount</a> container directory <code>/var/run/mysqld/</code> to the same directory on the Ubuntu 22.10 host machine, it does not exist, we need to create it:

```
$ sudo mkdir /var/run/mysqld
```

The mounting option is:

```
--mount type=bind,source=/var/run/mysqld,target=/var/run/mysqld/
```

<h4 style="color:teal;">
  <a id="database-directory">Mounting the Database Directory to Host Machine</a>
</h4>

<strong>For the purpose of this post, I'm assuming that the database directory on the host machine does not yet exist.</strong> Create the database directory: <code>/home/behai/Public/database/mysql</code>.

Based on the official documentation <a href="https://hub.docker.com/_/mysql" title="Where to Store Data" target="_blank">Where to Store Data</a>, the volume mount option for the database directory takes the form:

```
-v /my/own/datadir:/var/lib/mysql
```

That is:

```
-v /home/behai/Public/database/mysql:/var/lib/mysql
```

Please note, as an alternative, we can also use <a href="https://docs.docker.com/storage/bind-mounts/" title="Bind mounts" target="_blank">bind mount</a> for the database directory:

```
--mount type=bind,source=/home/behai/Public/database/mysql,target=/var/lib/mysql
```

So we have two possible full final commands:

🚀 ❶ The first full, final command:

```
$ sudo docker run -d -it --rm --name mysql-docker
    --mount type=bind,source=/home/behai/Public/database/mysql-config,target=/etc/mysql/conf.d
    -v /home/behai/Public/database/mysql:/var/lib/mysql
    --mount type=bind,source=/var/run/mysqld,target=/var/run/mysqld/
    -p 3306:3306 -e MYSQL_ROOT_PASSWORD=pcb.2176310315865259 mysql:8.0.34-debian
```

🚀 ❷ The second full, final command:

```
$ sudo docker run -d -it --rm --name mysql-docker
    --mount type=bind,source=/home/behai/Public/database/mysql-config,target=/etc/mysql/conf.d
    --mount type=bind,source=/home/behai/Public/database/mysql,target=/var/lib/mysql
    --mount type=bind,source=/var/run/mysqld,target=/var/run/mysqld/
    -p 3306:3306 -e MYSQL_ROOT_PASSWORD=pcb.2176310315865259 mysql:8.0.34-debian
```

<h3 style="color:teal;">
  <a id="config-log-files-verification">Verify Custom Config Items, and Log Files Created</a>
</h3>

We run the <code>mysql:8.0.34-debian</code> image with one of the final commands above and verify that the items specified in the <a href="#custom-config-file">custom config file</a> have taken effect: ⓵ <code>default_authentication_plugin</code> and <code>log_bin_trust_function_creators</code> have been set; ⓶ MySQL socket files, as well as ⓷ all database files and log files get created in the respective directories on the host machine.

To recap, at this point, both <code>/var/run/mysqld</code> and <code>/home/behai/Public/database/mysql</code> on the host machine are empty.

Stop the container with (note, <code>mysql-docker</code> container also gets removed):

```
$ sudo docker stop mysql-docker
```

Re-run the image with either one of the above final commands:

```
$ sudo docker run -d -it --rm --name mysql-docker --mount type=bind,source=/home/behai/Public/database/mysql-config,target=/etc/mysql/conf.d -v /home/behai/Public/database/mysql:/var/lib/mysql --mount type=bind,source=/var/run/mysqld,target=/var/run/mysqld/ -p 3306:3306 -e MYSQL_ROOT_PASSWORD=pcb.2176310315865259 mysql:8.0.34-debian
```

```
$ sudo docker run -d -it --rm --name mysql-docker --mount type=bind,source=/home/behai/Public/database/mysql-config,target=/etc/mysql/conf.d --mount type=bind,source=/home/behai/Public/database/mysql,target=/var/lib/mysql --mount type=bind,source=/var/run/mysqld,target=/var/run/mysqld/ -p 3306:3306 -e MYSQL_ROOT_PASSWORD=pcb.2176310315865259 mysql:8.0.34-debian
```

<h4 style="color:teal;">
  <a id="mysql-socket-files">Verify MySQL Socket Files</a>
</h4>

After running one of the final commands above, <strong>after a little while</strong>, MySQL socket files should be created in <code>/var/run/mysqld</code>. Please see the screenshot below:

![084-01-1.png](https://behainguyen.files.wordpress.com/2023/09/084-01-1.png)

<h4 style="color:teal;">
  <a id="database-and-log-files">Verify Database Files and Log Files</a>
</h4>

Similar to MySQL socket files, after running one of the final commands above, initial database and log files are created in <code>/home/behai/Public/database/mysql</code>. Please see the screenshot below:

![084-02.png](https://behainguyen.files.wordpress.com/2023/09/084-02.png)

<h4 style="color:teal;">
  <a id="config-items-auth-log-bin">Verify <code>default_authentication_plugin</code> and <code>log_bin_trust_function_creators</code></a>
</h4>

Run the container in the interactive mode with the Bash process, with:

```
$ sudo docker exec -it mysql-docker bash
```

Once in the Bash shell, run <code>mysql</code> command line with:

```
# mysql -uroot -ppcb.2176310315865259
```

We can query <code>default_authentication_plugin</code>'s value with:

```
mysql> show variables like 'default_authentication_plugin';
```

We should get:

```
+-------------------------------+-----------------------+
| Variable_name                 | Value                 |
+-------------------------------+-----------------------+
| default_authentication_plugin | mysql_native_password |
+-------------------------------+-----------------------+
1 row in set (0.02 sec)
```

Then <code>log_bin_trust_function_creators</code>:

```
mysql> show variables like 'log_bin_trust_function_creators';
```

```
+---------------------------------+-------+
| Variable_name                   | Value |
+---------------------------------+-------+
| log_bin_trust_function_creators | ON    |
+---------------------------------+-------+
1 row in set (0.01 sec)
```

<h4 style="color:teal;">
  <a id="check-general-log-file">Checking Out <code>general_log.log</code> File</a>
</h4>

Up to this point, we've run two (queries), they should be in the <code>general_log.log</code> file:

```
$ sudo cat /home/behai/Public/database/mysql/general_log.log
```

And they are:

```
...
2023-09-21T03:12:01.424052Z         8 Connect   root@localhost on  using Socket
2023-09-21T03:12:01.424277Z         8 Query     select @@version_comment limit 1
2023-09-21T03:12:10.402121Z         8 Query     show variables like 'default_authentication_plugin'
2023-09-21T03:12:27.396645Z         8 Query     show variables like 'log_bin_trust_function_creators'
2023-09-21T03:12:48.420061Z         8 Quit
behai@hp-pavilion-15:~/Public/database$
```

<h3 style="color:teal;">
  <a id="allow-traffic-throu-port-3306">Allow Traffic Through MySQL port <code>3306</code></a>
</h3>

We're using the default MySQL port <code>3306</code>. Allow traffic through this port with:

```
$ sudo ufw allow from any to any port 3306 proto tcp
```

The set up is basically complete, <code>mysql:8.0.34-debian</code> Docker container is ready for connection. Let's test it.

<h3 style="color:teal;">
  <a id="win10-pro-mysql-workbench-connection">Test With a Remote Connection</a>
</h3>

Remotely connect to the container from Windows 10 Pro using MySQL Workbench 8.0. The connection information is as follow:

```
Host: 192.168.0.16 -- Ubuntu 22.10 IP address on local network.
Port: 3306
Username: root
Password: pcb.2176310315865259
```

MySQL Workbench version is <code>8.0.30 build 2054668 C4 (64 bits) Community</code>, older versions might not work.

I'm able to connect with no problem. It's an empty server, the only item appears under <code>SCHEMAS</code> is <code>sys</code>. Let's set up a database.

<h3 style="color:teal;">
  <a id="further-test-with-a-complete-database">Further Test Via Setting Up a Complete Database</a>
</h3>

We will use the <code>employees</code> <a href="https://github.com/datacharmer/test_db" title="Oracle Corporation MySQL test data" target="_blank">Oracle Corporation MySQL test data</a> database.

<h4 style="color:teal;">
  <a id="database-creation-population">Database Creation and Population</a>
</h4>

On Windows 10 Pro, back up the <code>employees</code> database with:

```
docker exec mysql-docker /usr/bin/mysqldump -u root --password=pcb.2176310315865259 employees > E:\employees.sql
```

<code>E:\employees.sql</code> is around 170 MB, and it <strong>does not have</strong> the <code>use employees</code> statement in the content. Copy <code>E:\employees.sql</code> to Ubuntu's <code>/home/behai/Public/</code> directory. I.e. <code>/home/behai/Public/employees.sql</code>.

Next, restore <code>/home/behai/Public/employees.sql</code> on Ubuntu 22.10 using the newly set up container for <code>mysql:8.0.34-debian</code> image.

The following commands issue warning about password being insecure. For the purpose of this post, we can ignore this warning.

First, drop any existing <code>employees</code> database. We know there is not any, but this is a step I always follow:

```
$ sudo docker exec mysql-docker /usr/bin/mysql -u root --password=pcb.2176310315865259 -e "drop database if exists employees"
```

Next, create the <code>employees</code> database:

```
$ sudo docker exec mysql-docker /usr/bin/mysql -u root --password=pcb.2176310315865259 -e "create database employees default CHARSET=utf8mb4 collate=utf8mb4_unicode_ci"
```

We can then list available databases with:

```
$ sudo docker exec mysql-docker /usr/bin/mysql -u root --password=pcb.2176310315865259 -e "show databases"
```

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>mysql: [Warning] Using a password on the command line interface can be insecure.
Database
<span style="color:blue;"><strong>employees</strong></span>
information_schema
mysql
performance_schema
sys
</code></pre></div></div>

We are now ready to load up the <code>/home/behai/Public/employees.sql</code> dump file with:

```
$ sudo docker exec -i mysql-docker /usr/bin/mysql -u root --password=pcb.2176310315865259 --database employees < /home/behai/Public/employees.sql
```

-- This can take a while, depending on the machine.

We can query the <code>employees</code> database with:

```
$ sudo docker exec mysql-docker /usr/bin/mysql -u root --password=pcb.2176310315865259 --database employees -e "select * from departments"
```

-- The <code>departments</code> table should have data.

The log files should now have gotten bigger. We can verify with:

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>behai@hp-pavilion-15:~/Public/database$ cd mysql
behai@hp-pavilion-15:~/Public/database/mysql$ pwd
/home/behai/Public/database/mysql
behai@hp-pavilion-15:~/Public/database/mysql$ ls -l general_log.log slow_query.log error.err
<span style="color:blue;"><strong>-rw-r----- 1 999 gamemode      6606 Sep 21 22:17 error.err</strong></span>
<span style="color:blue;"><strong>-rw-r----- 1 999 gamemode 181679518 Sep 21 22:17 general_log.log</strong></span>
<span style="color:blue;"><strong>-rw-r----- 1 999 gamemode       537 Sep 21 22:04 slow_query.log</strong></span>
behai@hp-pavilion-15:~/Public/database/mysql$
</code></pre></div></div>

<code>general_log.log</code> is 181,679,518 bytes. This is to be expected, considering that <code>/home/behai/Public/employees.sql</code> is around 170 MB. To delete these log files, first stop the container, delete the log file(s), then re-run the image again.

<h4 style="color:teal;">
  <a id="remote-stored-procs-creations">Remotely Create Stored Procedures on the Just Setup Database</a>
</h4>

Connect to the container from Windows 10 Pro using MySQL Workbench (<a href="#win10-pro-mysql-workbench-connection">as above</a>). The <code>employees</code> database should be there. Select it, and create the following two (2) stored procedures:

● Stored procedure <code>get_employees</code>:

```sql
DELIMITER $$
CREATE DEFINER=`root`@`%` PROCEDURE `get_employees`( pmLastName varchar(16), pmFirstName varchar(14) )
    READS SQL DATA
begin
  select * from employees e where (e.last_name like pmLastName)
    and (e.first_name like pmFirstName) order by e.emp_no;
end$$
DELIMITER ;
```

● Stored procedure <code>DemoStoredProc1</code>:

```sql
DELIMITER $$
CREATE DEFINER=`root`@`%` PROCEDURE `DemoStoredProc1`( pm_dept_no varchar(4) )
    READS SQL DATA
begin
  select * from departments where dept_no = pm_dept_no;
  select * from dept_manager where dept_no = pm_dept_no;
end$$
DELIMITER ;
```

My naming convention is not consistent. I'm aware of this. I wrote these two (2) stored procedures times apart for different posts, so I just kept the original names.

Since we connect using user <code>root</code>, they should be created successfully.

With that, we conclude this post. I do apologise that this post is a bit long. I did not expect it to be this long, the case of <em>the devil is in the details</em>, I think. I do hope you find it useful. Thank you for reading and stay safe as always.

✿✿✿

Feature image source:

<ul>
<li>
<a href="https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper" target="_blank">https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper</a>
</li>
<li>
<a href="https://www.stickpng.com/img/icons-logos-emojis/tech-companies/jenkins-logo-landscape" target="_blank">https://www.stickpng.com/img/icons-logos-emojis/tech-companies/jenkins-logo-landscape</a>
</li>
<li>
<a href="https://www.freepnglogos.com/uploads/logo-mysql-png/logo-mysql-mysql-logo-png-images-are-download-crazypng-21.png" target="_blank">https://www.freepnglogos.com/uploads/logo-mysql-png/logo-mysql-mysql-logo-png-images-are-download-crazypng-21.png</a>
</li>
</ul>

<h3 style="color:teal;">
  <a id="my-other-docker-posts">Other Docker Posts Which I've Written</a>
</h3>

<ol>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/07/24/synology-ds218-sudo-password-and-unsupported-docker-problems-update/"
title="Synology DS218: sudo password and unsupported Docker problems update..."
target="_blank">Synology DS218: sudo password and unsupported Docker problems update...</a> --
I have been updating the DSM without running <code>sudo</code> or <code>docker</code>. I have just tried both recently, both failed. I'm describing how I've managed to fix these two problems.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/07/09/python-flask-railway-app-deployment-and-railways-nixpacks-docker-image-build-tool/"
title="Python, Flask: Railway.app deployment and Railway's Nixpacks Docker image build tool." target="_blank">Python, Flask: Railway.app deployment and Railway's Nixpacks Docker image build tool.</a> --
I've successfully deployed my Australian postcodes API project to <a href="https://railway.app" title="https://railway.app" target="_blank">https://railway.app</a>. I did have some problem during deployment. I'm describing how I've addressed this problem. In the process, we're also covering the following: ⓵ running Railway's own Nixpacks Docker build tool locally on Ubuntu 22.10. ⓶ Override the Nixpacks-built Docker image's <code>CMD</code>: we look at three (3) ways to run the Flask CLI command <code>venv/bin/flask update-postcode</code>, and similarly, we look at how to override the start command <code>gunicorn wsgi:app --preload</code> specified in the Nixpacks required <a href="https://github.com/behai-nguyen/bh_aust_postcode/blob/main/Procfile" title="Nixpacks required Procfile" target="_blank">Procfile</a>.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/01/13/using-postgresql-official-docker-image-on-windows-10-and-ubuntu-22-10-kinetic/"
title="Using PostgreSQL Official Docker image on Windows 10 and Ubuntu 22.10 kinetic."
target="_blank">Using PostgreSQL Official Docker image on Windows 10 and Ubuntu 22.10 kinetic.</a> --
Discussing a basic set up process to use the PostgreSQL Official Docker image on Windows 10 Pro, and Ubuntu 22.10 kinetic running on an older HP laptop. Then backup a PostgreSQL database on Windows 10 Pro machine, and restore this backup database to the newly set up Docker PostgreSQL Server 15.1 on the Ubuntu 22.10 machine.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/11/29/docker-compose-how-to-wait-for-the-mysql-server-container-to-be-ready/"
title="Docker Compose: how to wait for the MySQL server container to be ready?"
target="_blank">Docker Compose: how to wait for the MySQL server container to be ready?</a> --
Waiting for a database server to be ready before starting our own application, such as a middle-tier server, is a familiar issue. Docker Compose is no exception. Our own application container must also wait for their own database server container ready to accept requests before sending requests over. I've tried two ( 2 ) “wait for” tools which are officially recommended by Docker. I'm discussing my attempts in this post, and describing some of the pending issues I still have.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/11/13/pgloader-docker-migrating-from-docker-localhost-mysql-to-localhost-postgresql/"
title="pgloader Docker: migrating from Docker & localhost MySQL to localhost PostgreSQL."
target="_blank">pgloader Docker: migrating from Docker & localhost MySQL to localhost PostgreSQL.</a> --
Using the latest dimitri/pgloader Docker image build, I've migrated a Docker MySQL server 8.0.30 database, and a locally installed MySQL server 5.5 database to a locally installed PostgreSQL server 14.3 databases. I am discussing how I did it in this post.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/10/21/docker-on-windows-10-mysql8-0-30-debian-log-files/"
title="Docker on Windows 10: mysql:8.0.30-debian log files"
target="_blank">Docker on Windows 10: mysql:8.0.30-debian log files </a> --
Running the Docker Official Image mysql:8.0.30-debian on my Windows 10 Pro host machine, I want to log all queries, slow queries and errors to files on the host machine. In this article, we're discussing how to go about achieving this.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/08/09/docker-on-windows-10-running-mysql8-0-30-debian-with-a-custom-config-file/"
title="Docker on Windows 10: running mysql:8.0.30-debian with a custom config file."
target="_blank">Docker on Windows 10: running mysql:8.0.30-debian with a custom config file.</a> --
Steps required to run the official mysql:8.0.30-debian image on Windows 10 with custom config file E:\mysql-config\mysql-docker.cnf.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/07/29/python-docker-volumes-where-is-my-sqlite-database-file/"
title="Python: Docker volumes -- where is my SQLite database file?"
target="_blank">Python: Docker volumes -- where is my SQLite database file?</a> --
The Python application in a Docker image writes some data to a SQLite database. Stop the container, and re-run again, the data are no longer there! A volume must be specified when running an image to persist the data. But where is the SQLite database file, in both Windows 10 and Linux? We're discussing volumes and where volumes are on disks for both operating systems.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/07/27/python-docker-image-build-save-to-and-load-from-tar-files/"
title="Python: Docker image build -- save to and load from *.tar files."
target="_blank">Python: Docker image build -- save to and load from *.tar files.</a> --
We can save Docker images to local *.tar files, and later load and run those Docker images from local *.tar files. I'm documenting my learning experimentations in this post.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/07/25/python-docker-image-build-the-werkzeug-problem-%f0%9f%a4%96/"
title="Python: Docker image build -- “the Werkzeug” problem 🤖!"
target="_blank">Python: Docker image build -- “the Werkzeug” problem 🤖!</a> --
I've experienced Docker image build installed a different version of the Werkzeug dependency package than the development editable install process. And this caused the Python project in the Docker image failed to run. Development editable install means running the “pip3 install -e .” command within an active virtual environment. I'm describing the problem and how to address it in this post.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/07/22/python-docker-image-build-install-required-packages-via-requirements-txt-vs-editable-install/"
title="Python: Docker image build -- install required packages via requirements.txt vs editable install."
target="_blank">Python: Docker image build -- install required packages via requirements.txt vs editable install.</a> --
Install via requirements.txt means using this image build step command “RUN pip3 install -r requirements.txt”. Editable install means using the “RUN pip3 install -e .” command. I've experienced that install via requirements.txt resulted in images that do not run, whereas using editable install resulted in images that do work as expected. I'm presenting my findings in this post.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/07/20/synology-ds218-unsupported-docker-installation-and-usage/"
title="Synology DS218: unsupported Docker installation and usage..."
target="_blank">Synology DS218: unsupported Docker installation and usage...</a> --
Synology does not have Docker support for AArch64 NAS models. DS218 is an AArch64 NAS model. In this post, we're looking at how to install Docker for unsupported Synology DS218, and we're also conducting tests to prove that the installation works.
</li>
</ol>
