---
layout: post
title: "pgloader Docker: migrating from Docker & localhost MySQL to localhost PostgreSQL."
description: Using the latest dimitri/pgloader Docker image build, I've migrated a Docker MySQL server 8.0.30 database, and a locally installed MySQL server 5.5 database to a locally installed PostgreSQL server 14.3 databases. I am discussing how I did it in this post.
tags:
- Migrate
- MySQL 
- PostgreSQL
- PGLoader
- Docker
---

*Using the latest dimitri/pgloader Docker image build, I've migrated a Docker MySQL server 8.0.30 database, and a locally installed MySQL server 5.5 database to a locally installed PostgreSQL server 14.3 databases. I am discussing how I did it in this post.*

| ![046-feature-image.png](https://behainguyen.files.wordpress.com/2022/11/046-feature-image.png) |
|:--:|
| *pgloader Docker: migrating from Docker & localhost MySQL to localhost PostgreSQL.* |

<!--------------------------------------------------------------------------------->

<h2>Table of contents</h2>

<ul>
	<li><a href="#environments">Environments</a></li>

	<li><a href="#migrating-commands">Migrating Commands</a></li>

	<li><a href="#migration-observervations">Some Migration Observervations</a></li>	

	<li><a href="#detail-discussions">Detail Discussions</a></li>
</ul>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="environments">Environments</a>
</h3>

<ol>
<li style="margin-top:10px;">
<span class="keyword">Windows 10 Pro</span> -- <span class="keyword"> version 10.0.19045 Build 19045</span>.
</li>

<li style="margin-top:10px;">
<span class="keyword">Windows “docker” CLI ( Docker Engine )</span> -- <span class="keyword"> version 20.10.17, build de40ad0</span>.
</li>

<li style="margin-top:10px;">
<span class="keyword">Windows Docker Desktop</span> -- <span class="keyword"> version 4.11.0</span>.
</li>

<li style="margin-top:10px;">
<span class="keyword">mysql:8.0.30-debian</span> -- this is a 
<a href="https://hub.docker.com/_/mysql" title="MySQL Docker Official Image" target="_blank">MySQL Docker Official Image</a>,
<span class="keyword">version 8.0.30</span>. 
It is running on the Windows 10 machine.
</li>

<li style="margin-top:10px;">
<span class="keyword">MySQL 5.5</span>, 
server installed on the Windows 10 machine. This is an unsupported version of MySQL.
</li>

<li style="margin-top:10px;">
<span class="keyword">PostgreSQL 14.3</span>, server installed on the Windows 10 machine, 
<span class="keyword">version compiled by Visual C++ build 1914, 64-bit</span>.
</li>
</ol>

On <span class="keyword">mysql:8.0.30-debian Docker image build</span>, I've also written two related posts:

<ol>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/08/09/docker-on-windows-10-running-mysql8-0-30-debian-with-a-custom-config-file/"
title="Docker on Windows 10: running mysql:8.0.30-debian with a custom config file"
target="_blank">Docker on Windows 10: running mysql:8.0.30-debian with a custom config file</a>.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/10/21/docker-on-windows-10-mysql8-0-30-debian-log-files/"
title="Docker on Windows 10: mysql:8.0.30-debian log files"
target="_blank">Docker on Windows 10: mysql:8.0.30-debian log files</a>.
</li>
</ol>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="migrating-commands">Migrating Commands</a>
</h3>

Below are two ( 2 ) 
<span class="keyword">
dimitri/pgloader</span> commands I used successfully to migrate the
two ( 2 ) MySQL databases to PostgreSQL. Please note that:

-- PostgreSQL target database must exist before migrating.

❶ Migrate Docker 
<span class="keyword">
mysql:8.0.30-debian</span>'s database
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
ompdev1</span>
to localhost PostgreSQL's 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
test_ompdev1</span> database:

```
F:\>docker run --rm -it dimitri/pgloader:latest pgloader mysql://root:secret-password@172.17.0.2/ompdev1 postgresql://postgres:secret-password@host.docker.internal/test_ompdev1
```

❷ Migrate localhost MySQL 5.5's 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
employees</span> database
to localhost PostgreSQL's 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
employees</span> database:

```
F:\>docker run --rm -it dimitri/pgloader:latest pgloader mysql://root:secret-password@host.docker.internal/employees postgresql://postgres:secret-password@host.docker.internal/employees
```

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="migration-observervations">Some Migration Observervations</a>
</h3>

<p>
Based on the two ( 2 ) migrations' experimentations, I've observed 
the followings:
</p>

<ol>
<li style="margin-top:10px;">
Stored procedures and stored functions are not migrated.
</li>

<li style="margin-top:10px;">
Triggers are not migrated.
</li>

<li style="margin-top:10px;">
Auto increment integer primary keys migrated as integer primary keys;
they lose the auto increment property, I have to fix these manually.
</li>
</ol>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="detail-discussions">Detail Discussions</a>
</h3>

<h4>host.docker.internal and 172.17.0.2 hosts</h4>

Recall the two ( 2 ) commands used in the <a href="#migrating-commands">Migrating Commands</a> section:

```
F:\>docker run --rm -it dimitri/pgloader:latest pgloader mysql://root:secret-password@172.17.0.2/ompdev1 postgresql://postgres:secret-password@host.docker.internal/test_ompdev1
F:\>docker run --rm -it dimitri/pgloader:latest pgloader mysql://root:secret-password@host.docker.internal/employees postgresql://postgres:secret-password@host.docker.internal/employees
```

When I started research MySQL to PostgreSQL migration tool, it seemed to me that 
<a href="https://hub.docker.com/r/dimitri/pgloader/" title="dimitri/pgloader" target="_blank">dimitri/pgloader</a> 
is the tool to use: it is not yet available as a stand-alone version for Windows, 
so the Docker image version is the next best thing. From the official page,
and discussions on the net, this Docker image would just work out of the box. But I was 
not able to get it to work on the first go: I'd forgotten all about Docker networking!

Please note the host addresses, <span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
host.docker.internal</span> and <span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
172.17.0.2</span> in the above commands -- this is where I failed in the first place.

<a href="https://stackoverflow.com/questions/40746453/how-to-connect-to-docker-host-from-container-on-windows-10-docker-for-windows"
title="How to connect to docker host from container on Windows 10 (Docker for Windows)"
target="_blank">How to connect to docker host from container on Windows 10 (Docker for Windows)</a>
cites this official Docker document page 
<a href="https://docs.docker.com/docker-for-windows/networking/"
title="Explore networking features" target="_blank">Explore networking features</a>:

>The host has a changing IP address (or none if you have no network access). We recommend that you connect to the special DNS name host.docker.internal which resolves to the internal IP address used by the host. This is for development purpose and does not work in a production environment outside of Docker Desktop.

So this means 
<span class="keyword">
dimitri/pgloader Docker container</span> sees the host address for
<span class="keyword">
MySQL 5.5</span> and 
<span class="keyword">
PostgreSQL</span> servers installed on the Windows 10 as 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
host.docker.internal</span>.

For Docker 
<span class="keyword">
mysql:8.0.30-debian</span>, I need to use the Docker image container IP address.
Recall from this post 
<a href="https://behainguyen.wordpress.com/2022/08/09/docker-on-windows-10-running-mysql8-0-30-debian-with-a-custom-config-file/"
title="Docker on Windows 10: running mysql:8.0.30-debian with a custom config file"
target="_blank">Docker on Windows 10: running mysql:8.0.30-debian with a custom config file</a>, 
I run it with no network option:

```
E:\>docker run -d -it --rm --name mysql-docker --mount type=bind,source=//e/mysql-config,target=/etc/mysql/conf.d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=pcb.2176310315865259 mysql:8.0.30-debian
```

That means its container uses the default 
<span class="keyword">
bridge</span> network. To list networks:

```
E:\>docker network ls
```

```
NETWORK ID     NAME            DRIVER    SCOPE
4fdfeff4bb4b   bridge          bridge    local
791ebddb8e24   host            host      local
cd3831cd0536   none            null      local
```

To see which containers are in the 
<span class="keyword">
bridge</span> network:

```
E:\>docker inspect bridge
```

I'm extracting out the relevant portion related to container
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
mysql-docker</span>:

```
...
        },
        "ConfigOnly": false,
        "Containers": {
            "02e57f7b22b358a6abaac1848ed0857b2ea9a9c63bc191b40061c15d770cdc2d": {
                "Name": "mysql-docker",
                "EndpointID": "e3cb0ed472f14da240416d828ebd368c4e734ca18f19cc779928106200ca8768",
                "MacAddress": "02:42:ac:11:00:02",
                "IPv4Address": "172.17.0.2/16",
                "IPv6Address": ""
            }
        },
        "Options": {
...
```

<span class="keyword">
IPv4Address</span> is the one we are interested in, which is 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
172.17.0.2</span>.

<h4>The employees database</h4>

The 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
employees</span>
database is a 
<span class="keyword">
MySQL test data</span> database 
released by Oracle Corporation. Downloadable from
<a href="https://github.com/datacharmer/test_db" title="MySQL test data " target="_blank">https://github.com/datacharmer/test_db</a>.
It is a simple database with only a few tables, easy to setup. The main tables have several 
hundreds thousand records, which is very good for testing purposes.

<h4>Saving dimitri/pgloader image to disk</h4>

I like to store Docker images I use to disk. Just in case I lost them, I can just reload, without having to pull them again.

```
D:\>docker images
```

```
REPOSITORY         TAG               IMAGE ID       CREATED        SIZE
...
dimitri/pgloader   latest            d548fdd654a5   2 months ago   194MB
...
```

```
D:\>docker save dimitri/pgloader > E:\docker-images\dimitri_pgloader_01.tar
D:\>docker save d548fdd654a5 --output E:\docker-images\dimitri_pgloader_02.tar
```

I've also done a post on this subject: 
<a href="https://behainguyen.wordpress.com/2022/07/27/python-docker-image-build-save-to-and-load-from-tar-files/"
title="Python: Docker image build — save to and load from *.tar files."
target="_blank">Python: Docker image build — save to and load from *.tar files</a>.

✿✿✿

I have done this for learning purposes. I have not applied this 
in production. I'm sure there are many more issues which I'm not
aware of. During my entire working life so far, I have only done
one production migration: we don't have that many opportunities,
this is an expensive and often not a profitable exercise for
any organisation. I do hope you find this useful. Thank you for
reading and stay safe as always.
