---
layout: post
title: "Docker on Windows 10: mysql:8.0.30-debian log files"
description: Running the Docker Official Image mysql:8.0.30-debian on my Windows 10 Pro host machine, I want to log all queries, slow queries and errors to files on the host machine. In this article, we're discussing how to go about achieving this.
tags:
- Docker 
- MySQL 
- Windows
- Log Files
- Query Log File
---

*Running the Docker Official Image mysql:8.0.30-debian on my Windows 10 Pro host machine, I want to log all queries, slow queries and errors to files on the host machine. In this article, we're discussing how to go about achieving this.*

| ![041-feature-image.png](https://behainguyen.files.wordpress.com/2022/10/041-feature-image.png) |
|:--:|
| *Docker on Windows 10: mysql:8.0.30-debian log files* |

We've previously discussed how to implement a custom config file 
for 
<a href="https://hub.docker.com/_/mysql" 
title="mysql Docker Official Image" target="_blank">MySQL Docker Official Image</a> 
in 
<a href="https://behainguyen.wordpress.com/2022/08/09/docker-on-windows-10-running-mysql8-0-30-debian-with-a-custom-config-file/"
title="Docker on Windows 10: running mysql:8.0.30-debian with a custom config file."
target="_blank">Docker on Windows 10: running mysql:8.0.30-debian with a custom config file</a>.
This post assumes that we are using this custom config file.

What I would like to do is to log all queries, slow queries and errors to files on the host machine. The official references to each of the log types:

<ul>
<li style="margin-top:5px;">
All queries -- 

<a href="https://dev.mysql.com/doc/refman/8.0/en/query-log.html"
title="5.4.3 The General Query Log"
target="_blank">5.4.3 The General Query Log</a>
</li>

<li style="margin-top:10px;">
Slow queries -- 
	<ul>
    <li style="margin-top:5px;">
	<a href="https://dev.mysql.com/doc/refman/5.7/en/slow-query-log.html"
	title="5.4.5 The Slow Query Log"
	target="_blank">5.4.5 The Slow Query Log</a>
    </li>

    <li style="margin-top:10px;">
	<a href="https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_log_queries_not_using_indexes"
	title="5.1.7 Server System Variables | log_queries_not_using_indexes"
	target="_blank">5.1.7 Server System Variables | log_queries_not_using_indexes</a>
    </li>	
	</ul>
</li>

<li style="margin-top:10px;">
Errors -- <a href="https://dev.mysql.com/doc/refman/8.0/en/error-log-destination-configuration.html#error-log-destination-configuration-unix"
title="5.4.2.2 Default Error Log Destination Configuration"
target="_blank">5.4.2.2 Default Error Log Destination Configuration</a>
</li>
</ul>

Accordingly, the custom config file 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
E:\mysql-config\mysql-docker.cnf</span> gets updated as:

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

I updated it directly on Windows, its permissions get changed, and as
discussed in
<a href="https://behainguyen.wordpress.com/2022/08/09/docker-on-windows-10-running-mysql8-0-30-debian-with-a-custom-config-file/"
title="Docker on Windows 10: running mysql:8.0.30-debian with a custom config file."
target="_blank">Docker on Windows 10: running mysql:8.0.30-debian with a custom config file</a>, 
we need to change its permissions to the correct ones.

While 
<span class="keyword">
mysql-docker mysql:8.0.30-debian</span> container is running,
start the interactive mode with 
<span class="keyword">
the Bash process</span> to change config file permissions:

```
E:\>docker exec -it mysql-docker bash
```

```
root@8e6656b15d9a:/# cd /etc/mysql/conf.d/
root@8e6656b15d9a:/# chmod u+rw-x mysql-docker.cnf
root@8e6656b15d9a:/# chmod g+r-wx mysql-docker.cnf
root@8e6656b15d9a:/# chmod o+r-wx mysql-docker.cnf
```

Permissions should now be correct. To verify:

```
root@8e6656b15d9a:/# ls -l
```

```
total 4
-rw-r--r-- 1 root root 380 Oct 20 11:40 mysql-docker.cnf
```

Restart 
<span class="keyword">
mysql-docker</span> container for the new settings to take effect:

```
E:\>docker stop mysql-docker
E:\>docker start mysql-docker
```

<span style="color:blue;font-weight:bold;">Please note, for the above two ( 2 ) commands to work,
<span class="keyword">
mysql-docker</span> must be started without the
<span class="keyword">
--rm</span> flag, that is:
</span>

```
docker run -d -it --name mysql-docker -p 3306:3306 -e MYSQL_ROOT_PASSWORD=pcb.2176310315865259 --mount type=bind,source=//e/mysql-config,target=/etc/mysql/conf.d --mount source=mysqlvol,target=/var/lib/mysql mysql:8.0.30-debian
```

<span style="font-weight:bold;">Please also notice the following option 
in the above 
<span class="keyword">
docker run</span> command:
<span class="keyword">
--mount source=mysqlvol,target=/var/lib/mysql</span>.
</span> We shall come back to this option later on.

Using a client tool such as 
<span class="keyword">
MySQL Workbench</span> to verify that the new settings are effective:

```
show variables like 'general_log';
show variables like 'slow_query_log';
show variables like 'log_queries_not_using_indexes';
```

The above commands should each return 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
ON</span>. Similarly, the below should each return the corresponding values
we set in the config file:

```
show variables like 'general_log_file';
show variables like 'slow_query_log_file';
show variables like 'log_error';
```

➡️ But where 
<span class="keyword">/var/lib/mysql/general_log.log</span>,
<span class="keyword">/var/lib/mysql/slow_query.log</span>
and 
<span class="keyword">/var/lib/mysql/error.err</span>
are?

In 
<a href="https://behainguyen.wordpress.com/2022/07/29/python-docker-volumes-where-is-my-sqlite-database-file/"
title="Python: Docker volumes -- where is my SQLite database file?"
target="_blank">Python: Docker volumes -- where is my SQLite database file?</a>,
I've discussed where 
<span class="keyword">
Docker volumes</span> or
<span class="keyword">
data files</span> are on 
<span class="keyword">
Windows 10 Pro</span> host machine: essentially, due to the installation 
of my <span class="keyword">
Docker Desktop</span> uses <span class="keyword">
Windows Subsystem for Linux ( WSL 2 ) based engine</span>, I can copy 
and paste this directory:

```
\\wsl$\docker-desktop-data\version-pack-data\community\docker
```

to 
<span class="keyword">
Windows File Explorer</span>, and it should go to the top level 
<span class="keyword">
Docker desktop data</span> directory; 
<span class="keyword">
mysql-docker</span>'s files are in:

```
\\wsl$\docker-desktop-data\version-pack-data\community\docker\volumes\mysqlvol\_data
```

We should find our log files:

![041-docker-mysql-log-files.png](https://behainguyen.files.wordpress.com/2022/10/041-docker-mysql-log-files.png)

Why 
<span class="keyword">
\\wsl$\docker-desktop-data\version-pack-data\community\docker\volumes\mysqlvol</span>?

Recall the <span class="keyword">
docker run</span> option previously mentioned 
<span class="keyword">
<strong>--mount source=mysqlvol,target=/var/lib/mysql</strong></span>?
<span class="keyword">
<strong>source=mysqlvol</strong></span> is the host machine volume
or where the container's data files live.

Logging all queries can slow down the server, and the log file can get
very big, it should only be used during development, certainly not in
production. Also, these options can be set and reset on the
flight without needing to use the config file or server restart. For
example, via <span class="keyword">
MySQL Workbench</span>:

```
SET GLOBAL general_log = 'OFF';
SET GLOBAL general_log = 'ON';
```

I've tried, and it works: I can turn off
<span class="keyword">
general_log</span>, then delete the log file, turn on 
<span class="keyword">
general_log</span> again, and a new log file is created. 

I do hope you find this helpful and useful. Thank you for reading and stay safe as always.
