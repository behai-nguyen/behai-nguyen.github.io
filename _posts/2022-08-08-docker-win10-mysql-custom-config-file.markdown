---
layout: post
title: "Docker on Windows 10: running mysql:8.0.30-debian with a custom config file."
description: Steps required to run the official mysql:8.0.30-debian image on Windows 10 with custom config file E:\mysql-config\mysql-docker.cnf.
tags:
- Docker
- Windows
- MySQL 
- Custom Config File
---

Steps required to run the official mysql:8.0.30-debian image on Windows 10 with custom config file E:\mysql-config\mysql-docker.cnf.

| ![035-feature-image.png](https://behainguyen.files.wordpress.com/2022/08/035-feature-image.png) |
|:--:|
| *Docker on Windows 10: running mysql:8.0.30-debian with a custom config file.* |

<p>
I want to use my custom config file 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
E:\mysql-config\mysql-docker.cnf</span>,
when running the <a href="https://hub.docker.com/_/mysql" 
title="mysql Docker Official Image" target="_blank">Docker Official Image</a> 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
mysql:8.0.30-debian</span>, on my 
<span class="keyword">
Windows 10 Pro</span> machine. I'm describing the
steps to get this working.
</p>

<p>
❶ <span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
mysql-docker.cnf</span> is the only file in 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
E:\mysql-config\</span>. Its content:
</p>

```
[mysqld]
default_authentication_plugin=mysql_native_password
log_bin_trust_function_creators=1
```

<p>
❷ For this 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
mysql:8.0.30-debian</span> image, the custom config file is 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
/etc/mysql/conf.d/mysql.cnf</span>.
</p>

<p>
Its permissions are: <strong>owner</strong> has <strong>read</strong> and <strong>write</strong>;
<strong>groups</strong> and <strong>others</strong> has only <strong>read</strong>. Our own custom
config file must have the same permissions.
</p>

<p>
❸ Mount 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
E:\mysql-config\mysql-docker.cnf</span> to change its permissions, 
we only need the directory.
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
E:\mysql-config\</span> gets translated to 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
//e/mysql-config</span>. The mounting option is thus:
</p>

```
--mount type=bind,source=//e/mysql-config,target=/etc/mysql/conf.d
```

<p>
The command to run:
</p>

```
E:\>docker run -d -it --rm --name mysql-docker --mount type=bind,source=//e/mysql-config,target=/etc/mysql/conf.d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=pcb.2176310315865259 mysql:8.0.30-debian
```

<p>
Run the container in the interactive mode with the bash process to change config file permissions:
</p>

```
E:\>docker exec -it mysql-docker bash
```

<p>
Verify that we're looking at the <span class="keyword">
Windows 10 Pro</span> directory, which has only this config file, also note its permissions:
</p>

```
root@5b671d85c90b:/# ls -l /etc/mysql/conf.d
```

```
total 4
-rwxrwxrwx 1 root root 95 Aug  8 11:41 mysql-docker.cnf
```

<p>
Change permissions to match the corresponding container 
custom config file. That is, 
<strong>owner</strong> has <strong>read</strong> and <strong>write</strong>;
<strong>groups</strong> and <strong>others</strong> has only <strong>read</strong>:
</p>

```
root@5b671d85c90b:/# cd /etc/mysql/conf.d/
root@5b671d85c90b:/# chmod u+rw-x mysql-docker.cnf
root@5b671d85c90b:/# chmod g+r-wx mysql-docker.cnf
root@5b671d85c90b:/# chmod o+r-wx mysql-docker.cnf
```

<p>
Permissions should now be correct. To verify:
</p>

```
root@5b671d85c90b:/# ls -l
```

```
total 4
-rw-r--r-- 1 root root 95 Aug  8 11:41 mysql-docker.cnf
```

<p>
❹ Stop and re-run to verify the custom config file takes effects. 
This time, also run with proper data persistent volume with the option:
</p>

```
--mount source=mysqlvol,target=/var/lib/mysql
```

<p>
The commands to stop the container and to run are:
</p>

```
E:\>docker stop mysql-docker
E:\>docker run -d -it --rm --name mysql-docker -p 3306:3306 -e MYSQL_ROOT_PASSWORD=pcb.2176310315865259 --mount type=bind,source=//e/mysql-config,target=/etc/mysql/conf.d --mount source=mysqlvol,target=/var/lib/mysql mysql:8.0.30-debian
```

<p>
❺ Verify custom config takes effect. Using the 
<span class="keyword">
MySQL command line</span> to query values of the
custom options. Run the interactive bash shell:
</p>

```
E:\>docker exec -it mysql-docker bash
```

<p>
Launch <span class="keyword">
MySQL command line</span>:
</p>

```
root@dfa641fecc0a:/# mysql -uroot -ppcb.2176310315865259
```

<p>
⓵ Verify <span class="keyword">
default_authentication_plugin=mysql_native_password</span>:
</p>

```
mysql> show variables like 'default_authentication_plugin';
```

```
+-------------------------------+-----------------------+
| Variable_name                 | Value                 |
+-------------------------------+-----------------------+
| default_authentication_plugin | mysql_native_password |
+-------------------------------+-----------------------+
1 row in set (0.01 sec)
```

<p>
⓶ Verify <span class="keyword">
log_bin_trust_function_creators=1</span>. Please note, 
<span class="keyword">
1</span> is reported as 
<span class="keyword">
ON</span>:
</p>

```
mysql> show variables like 'log_bin_trust_%';
```

```
+---------------------------------+-------+
| Variable_name                   | Value |
+---------------------------------+-------+
| log_bin_trust_function_creators | ON    |
+---------------------------------+-------+
1 row in set (0.00 sec)
```

<p>
❻ Using a 
<span class="keyword">
Windows MySQL client tool</span>, we should also be able 
to connect to 
<span class="keyword">
MySQL</span> in the 
<span class="keyword">
mysql-docker</span> container. E.g.:
</p>

```
"C:\Program Files\MySQL\MySQL Server 5.5\bin\mysql" --protocol=TCP --host=localhost --port=3306 --user=root --password=pcb.2176310315865259
```

<p>
Since the value of 
<span class="keyword">
default_authentication_plugin</span> is 
<span class="keyword">
mysql_native_password</span> we should login successfully. 
I.e. we should not get the error:
</p>

<span class="keyword">
<span style="color:red;font-weight:bold;">
ERROR 2059 (HY000): Authentication plugin 'caching_sha2_password' cannot be loaded: The specified module could not be found.
</span></span>.

<p>✿✿✿</p>

<p>
It took me a while to work this one out... I document it so that it could possibly be of 
some helps for others. I am actually using 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
mysql:8.0.30-debian</span> as my development server. I'll do 
more documents on it later on. 
I hope you find this helpful and thank you for reading.
</p>