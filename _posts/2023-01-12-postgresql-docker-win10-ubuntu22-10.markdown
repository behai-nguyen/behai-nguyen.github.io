---
layout: post
title: "Using PostgreSQL Official Docker image on Windows 10 and Ubuntu 22.10 kinetic."
description: Discussing a basic set up process to use the PostgreSQL Official Docker image on Windows 10 Pro, and Ubuntu 22.10 kinetic running on an older HP laptop. Then backup a PostgreSQL database on Windows 10 Pro machine, and restore this backup database to the newly set up Docker PostgreSQL Server 15.1 on the Ubuntu 22.10 machine.
tags:
- PostgreSQL
- Postgres
- Docker
- Windows
- Ubuntu
---

*Discussing a basic set up process to use the PostgreSQL Official Docker image on Windows 10 Pro, and Ubuntu 22.10 kinetic running on an older HP laptop. Then backup a PostgreSQL database on Windows 10 Pro machine, and restore this backup database to the newly set up Docker PostgreSQL Server 15.1 on the Ubuntu 22.10 machine.*

| ![053-feature-image.png](https://behainguyen.files.wordpress.com/2023/01/053-feature-image.png) |
|:--:|
| *Using PostgreSQL Official Docker image on Windows 10 and Ubuntu 22.10 kinetic.* |

The PostgreSQL Server Docker official images are at this address
<a href="https://hub.docker.com/_/postgres" title="postgres Docker Official Image"
target="_blank">postgres Docker Official Image</a>.

This is the <a href="https://github.com/docker-library/docs/blob/master/postgres/README.md"
title="The full description" target="_blank">full documentation</a> for these images.
Please note, this page has links to Docker official documents on volumes,
etc., which are necessary to run images such as this.

This post also makes use of PostgreSQL Server password file, whose official
documentation is
<a href="https://www.postgresql.org/docs/current/libpq-pgpass.html"
title="34.16. The Password File" target="_blank">34.16. The Password File</a>.

The objectives of this post are rather basic. ❶, getting the Docker
container to store the data in a specific location on the host, of my
own choosing. ❷, implementing the password file on the host and pass
it to the Docker container as per official documentation above.

Of course, the final goal is to connect to a PostgreSQL server
running in a Docker container with whatever clients we need.

<h2>Table of contents</h2>

<ul>
	<li style="margin-top:10px;"><a href="#download-and-store-img">Downloading and Storing the Image Locally</a></li>

	<li style="margin-top:10px;"><a href="#environments">Environments</a></li>

	<li style="margin-top:10px;"><a href="#windows-10">On Windows 10</a></li>

	<li style="margin-top:10px;"><a href="#ubuntu-22-10">On Ubuntu 22.10 kinetic</a></li>

	<li style="margin-top:10px;"><a href="#ubuntu-22-10">Back and Restore a Database</a></li>

	<li style="margin-top:10px;"><a href="#my-other-docker-posts">Other Docker Posts Which I've Written</a></li>
</ul>

<h3 style="color:teal;">
  <a id="download-and-store-img">Downloading and Storing the Image Locally</a>
</h3>

To download:

```
E:\docker-images>docker pull postgres:latest
```

To save the image locally to <code>E:\docker-images\</code>:

```
E:\docker-images>docker save postgres:latest --output postgres-latest.tar
```

<code>postgres-latest.tar</code> is also used in Ubuntu 22.10
later on. This Docker image contains <code>PostreSQL
Server</code> version <code>15.1 (Debian 15.1-1.pgdg110+1)</code>.

<h3 style="color:teal;">
  <a id="environments">Environments</a>
</h3>

<ol>
<li style="margin-top:10px;">
<code>PostreSQL Server Docker</code> official image -- version <code>15.1 (Debian 15.1-1.pgdg110+1)</code>.
</li>

<li style="margin-top:10px;">
<code>Windows 10 Pro</code> -- version <code>10.0.19045 Build 19045</code>.
</li>

<li style="margin-top:10px;">
<code>Ubuntu</code> -- version <code>22.10 kinetic</code>. The machine it runs
on is an older HP Pavilion laptop. The name of this machine is 
<code>HP-Pavilion-15</code>, the rest of this post will use this
name and <code>Ubuntu 22.10</code> interchangeably.
</li>

<li style="margin-top:10px;">
Windows 10 <code>pgAdmin 4</code> -- version <code>6.18</code>. Older
versions might not work: when trying to connect, they fail with different
errors.
</li>

<li style="margin-top:10px;">
On Windows 10, <code>“docker” CLI ( Docker Engine )</code> -- version <code>20.10.17</code>.
</li>

<li style="margin-top:10px;">
On Ubuntu 22.10, <code>“docker” CLI ( Docker Engine )</code> -- <code>version 20.10.22</code>.
</li>
</ol>

<h3 style="color:teal;">
  <a id="windows-10">On Windows 10</a>
</h3>

Since I already have PostgreSQL Server 14 installed on Windows 10 Pro,
I have to turn its service process off, before setting up another server
in Docker container.

❶ I select to store PostgreSQL data in <code>D:\docker_data\postgresql\</code>.
After creating this directory path, on the <code>docker run</code> command,  
it can be mounted as:

```
--mount type=bind,source=//d/docker_data/postgresql,target=/var/lib/postgresql/data
```

My trial and error runs show that <strong>the host directory</strong>,
which is <code>D:\docker_data\postgresql\</code> translated to
<code>//d/docker_data/postgresql</code> in this case, <strong>must be
COMPLETELY empty, otherwise Docker raises an error</strong>.

The image has already been loaded when first pulled. The run command is:

```
docker run -d -it -p 5432:5432 --name postgresql-docker -e POSTGRES_PASSWORD=pcb.2176310315865259 --mount type=bind,source=//d/docker_data/postgresql,target=/var/lib/postgresql/data postgres:latest
```

❷ Now, stop and remove the <code>postgresql-docker</code> container:

```
C:\>docker stop postgresql-docker
C:\>docker rm postgresql-docker
```

Verify that container <code>postgresql-docker</code> has been removed, run:

```
C:\>docker ps -a
```

```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

I have no other containers, your list is likely to be different. We
should be able to confirm that <code>postgresql-docker</code> is not
in the list anymore.

Initial PostreSQL Server files and folders should now be created under
<code>D:\docker_data\postgresql\</code>, around 23 ( twenty three )
items, most are folders.

❸ Now create password file <code>secrets\pgpass.conf</code> under
<code>D:\docker_data\postgresql\</code>:

🐘 Content of <code>D:\docker_data\postgresql\secrets\pgpass.conf</code>:

```
localhost:5432:postgres:postgres:pcb.2176310315865259
```

As per official documentation, the password file is passed to the container as:

```
-e POSTGRES_PASSWORD_FILE=/var/lib/postgresql/data/secrets/pgpass.conf
```

Recall that <code>/var/lib/postgresql/data/</code> is the host
translated directory <code>//d/docker_data/postgresql</code> in the
first mount:

```
--mount type=bind,source=//d/docker_data/postgresql,target=/var/lib/postgresql/data
```

❹ The final command is, then:

```
docker run -d -it -p 5432:5432 --name postgresql-docker --mount type=bind,source=//d/docker_data/postgresql,target=/var/lib/postgresql/data -e POSTGRES_PASSWORD_FILE=/var/lib/postgresql/data/secrets/pgpass.conf postgres:latest
```

<strong>Please note that,</strong><em>I have to do two ( 2 ) commands to
get the password file to work. I did try to run only the final command on
the empty <code>//d/docker_data/postgresql</code>, it did not work.</em>
Please try for yourself.

The obvious question is, can we store the password file in a directory
other than the mounted host data directory <code>D:\docker_data\postgresql\</code>?
I don't know if it is possible, if it is possible, then I don't know how
to do it yet.

To connect <code>pgAdmin 4</code> to the just set up
Docker PostgresSQL Server 15.1, register a new server as:

<ol>
<li style="margin-top:10px;">
Host name/address: <code>localhost</code>
</li>

<li style="margin-top:10px;">
Port: <code>5432</code>.
</li>

<li style="margin-top:10px;">
Username: <code>postgres</code> -- I am using the default as per official document.
</li>

<li style="margin-top:10px;">
Password: <code>pcb.2176310315865259</code>
</li>
</ol>

Please note, the Windows 10 version of <code>pgAdmin 4</code> is <code>6.18</code>.
Older versions might not work: when trying to connect, they fail with different
errors.

Docker PostgresSQL Server 15.1 is now ready in Windows 10.

<h3 style="color:teal;">
  <a id="ubuntu-22-10">On Ubuntu 22.10 kinetic</a>
</h3>

On Ubuntu 22.10, I did not do any of the trial and error runs
as Windows 10. <strong>I assume that, what do not work on Windows 10,
will also not work on Ubuntu 22.10.</strong>

❶ Copy the image to <code>/home/behai/Public/docker-images/</code>,
then load the image with:

```
behai@HP-Pavilion-15:~$ sudo docker load --input /home/behai/Public/docker-images/postgres-latest.tar
```

❷ I want to store data under <code>/home/behai/Public/database/postgresql/</code>,
create the directories <code>database/postgresql/</code> under <code>/home/behai/Public/</code>,
and run the first command:

```
$ sudo docker run -d -it -p 5432:5432 --name postgresql-docker -e POSTGRES_PASSWORD=pcb.2176310315865259 --mount type=bind,source=/home/behai/Public/database/postgresql,target=/var/lib/postgresql/data postgres:latest
```

❸ Then stop and remove the <code>postgresql-docker</code> container:

```
behai@HP-Pavilion-15:~$ sudo docker stop postgresql-docker
behai@HP-Pavilion-15:~$ sudo docker rm postgresql-docker
```

Verify that the Docker container <code>postgresql-docker</code> has been removed:

```
behai@HP-Pavilion-15:~$ sudo docker ps -a
```

```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

Even if the list is not empty, <code>postgresql-docker</code> should not
be in the container list.

Initial PostreSQL Server files and folders should now be created under
<code>/home/behai/Public/database/postgresql/</code>:

![053-01.png](https://behainguyen.files.wordpress.com/2023/01/053-01.png)

❹ Now create <code>secrets/pgpass.conf</code> under <code>/home/behai/Public/database/postgresql/</code>:

🐘 Content of <code>/home/behai/Public/database/postgresql/secrets/pgpass.conf</code>:

```
localhost:5432:postgres:postgres:pcb.2176310315865259
```

The password file is passed to the Docker container as:

```
-e POSTGRES_PASSWORD_FILE=/var/lib/postgresql/data/secrets/pgpass.conf
```

<code>/var/lib/postgresql/data/</code> is the host directory
<code>/home/behai/Public/database/postgresql/</code> in the first mount:

```
--mount type=bind,source=/home/behai/Public/database/postgresql,target=/var/lib/postgresql/data
```

Final command:

```
$ sudo docker run -d -it -p 5432:5432 --name postgresql-docker --mount type=bind,source=/home/behai/Public/database/postgresql,target=/var/lib/postgresql/data -e POSTGRES_PASSWORD_FILE=/var/lib/postgresql/data/secrets/pgpass.conf postgres:latest
```

<a id="pgadmin-4-ubuntu-postgresql-server"></a>From Windows 10, to connect <code>pgAdmin 4</code> 
to Docker PostgresSQL Server 15.1 running on HP-Pavilion-15, register a new server:

<ol>
<li style="margin-top:10px;">
Host name/address: <code>HP-Pavilion-15</code> -- it's better to use 
the machine name, since IP addresses can change.
</li>

<li style="margin-top:10px;">
Port: <code>5432</code>.
</li>

<li style="margin-top:10px;">
Username: <code>postgres</code> -- I am using the default as per official document.
</li>

<li style="margin-top:10px;">
Password: <code>pcb.2176310315865259</code>
</li>
</ol>

Please note, the Windows 10 version of <code>pgAdmin 4</code> is <code>6.18</code>.
Older versions might not work: when trying to connect, they fail with different
errors.

<h3 style="color:teal;">
  <a id="ubuntu-22-10">Backup and Restore a Database</a>
</h3>

I already have PostgreSQL Server 14 installed on Windows 10 Pro.
I back up a development database <code>ompdev</code> from this server,
and restore the backup data to Docker PostgreSQL Server 15.1 running
on Ubuntu 22.10: machine name <code>HP-Pavilion-15</code>.

The database backup command:

```
"C:\Program Files\PostgreSQL\14\bin\pg_dump.exe" postgresql://postgres:top-secret@localhost/ompdev > ompdev_pg_database.sql
```

Please note, the above command will not have the create database statement in 
the dump file, on the target server, we need to manually create a database to 
restore to.

Restoring to HP-Pavilion-15 involves two simple steps.

⓵ Connect <code>pgAdmin 4</code> to Docker PostgreSQL Server on HP-Pavilion-15,
<a href="#pgadmin-4-ubuntu-postgresql-server">as discussed</a>. Then create a new
database with:

```
CREATE DATABASE ompdev;
```

Please note, it does not have to be <code>pgAdmin 4</code>, we can use
any other client tools available.

⓶ Then run the following restore command:

```
"C:\Program Files\PostgreSQL\14\bin\psql.exe" postgresql://postgres:pcb.2176310315865259@HP-Pavilion-15/ompdev &lt; ompdev_pg_database.sql
```

If everything goes well, we should now have the database restored and ready for connection
on Docker PostgreSQL Server 15.1 running on Ubuntu 22.10. The below screen capture showing
the <code>ompdev</code> database restored on HP-Pavilion-15:

![053-02.png](https://behainguyen.files.wordpress.com/2023/01/053-02.png)

<h3 style="color:teal;">
  <a id="my-other-docker-posts">Other Docker Posts Which I've Written</a>
</h3>

<ol>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/11/29/docker-compose-how-to-wait-for-the-mysql-server-container-to-be-ready/"
title="Docker Compose: how to wait for the MySQL server container to be ready?"
target="_blank">Docker Compose: how to wait for the MySQL server container to be ready?</a> --
Waiting for a database server to be ready before starting our own application, such as a middle-tier server, is a familiar issue. Docker Compose is no exception. Our own application container must also wait for their own database server container ready to accept requests before sending requests over. I've tried two ( 2 ) “wait for” tools which are officially recommended by Docker. I'm discussing my attempts in this post, and describing some of the pending issues I still have.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/07/20/synology-ds218-unsupported-docker-installation-and-usage/"
title="Synology DS218: unsupported Docker installation and usage..."
target="_blank">Synology DS218: unsupported Docker installation and usage...</a> --
Synology does not have Docker support for AArch64 NAS models. DS218 is an AArch64 NAS model. In this post, we're looking at how to install Docker for unsupported Synology DS218, and we're also conducting tests to prove that the installation works.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/07/22/python-docker-image-build-install-required-packages-via-requirements-txt-vs-editable-install/"
title="Python: Docker image build -- install required packages via requirements.txt vs editable install."
target="_blank">Python: Docker image build -- install required packages via requirements.txt vs editable install.</a> --
Install via requirements.txt means using this image build step command “RUN pip3 install -r requirements.txt”. Editable install means using the “RUN pip3 install -e .” command. I've experienced that install via requirements.txt resulted in images that do not run, whereas using editable install resulted in images that do work as expected. I'm presenting my findings in this post.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/07/25/python-docker-image-build-the-werkzeug-problem-%f0%9f%a4%96/"
title="Python: Docker image build -- “the Werkzeug” problem 🤖!"
target="_blank">Python: Docker image build -- “the Werkzeug” problem 🤖!</a> --
I've experienced Docker image build installed a different version of the Werkzeug dependency package than the development editable install process. And this caused the Python project in the Docker image failed to run. Development editable install means running the “pip3 install -e .” command within an active virtual environment. I'm describing the problem and how to address it in this post.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/07/27/python-docker-image-build-save-to-and-load-from-tar-files/"
title="Python: Docker image build -- save to and load from *.tar files."
target="_blank">Python: Docker image build -- save to and load from *.tar files.</a> --
We can save Docker images to local *.tar files, and later load and run those Docker images from local *.tar files. I'm documenting my learning experimentations in this post.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/07/29/python-docker-volumes-where-is-my-sqlite-database-file/"
title="Python: Docker volumes -- where is my SQLite database file?"
target="_blank">Python: Docker volumes -- where is my SQLite database file?</a> --
The Python application in a Docker image writes some data to a SQLite database. Stop the container, and re-run again, the data are no longer there! A volume must be specified when running an image to persist the data. But where is the SQLite database file, in both Windows 10 and Linux? We're discussing volumes and where volumes are on disks for both operating systems.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/08/09/docker-on-windows-10-running-mysql8-0-30-debian-with-a-custom-config-file/"
title="Docker on Windows 10: running mysql:8.0.30-debian with a custom config file."
target="_blank">Docker on Windows 10: running mysql:8.0.30-debian with a custom config file.</a> --
Steps required to run the official mysql:8.0.30-debian image on Windows 10 with custom config file E:\mysql-config\mysql-docker.cnf.
</li>

<li style="margin-top:10px;">

<a href="https://behainguyen.wordpress.com/2022/10/21/docker-on-windows-10-mysql8-0-30-debian-log-files/"
title="Docker on Windows 10: mysql:8.0.30-debian log files"
target="_blank">Docker on Windows 10: mysql:8.0.30-debian log files </a> --
Running the Docker Official Image mysql:8.0.30-debian on my Windows 10 Pro host machine, I want to log all queries, slow queries and errors to files on the host machine. In this article, we're discussing how to go about achieving this.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/11/13/pgloader-docker-migrating-from-docker-localhost-mysql-to-localhost-postgresql/"
title="pgloader Docker: migrating from Docker & localhost MySQL to localhost PostgreSQL."
target="_blank">pgloader Docker: migrating from Docker & localhost MySQL to localhost PostgreSQL.</a> --
Using the latest dimitri/pgloader Docker image build, I've migrated a Docker MySQL server 8.0.30 database, and a locally installed MySQL server 5.5 database to a locally installed PostgreSQL server 14.3 databases. I am discussing how I did it in this post.
</li>
</ol>

Thank you for reading and stay safe as always.
