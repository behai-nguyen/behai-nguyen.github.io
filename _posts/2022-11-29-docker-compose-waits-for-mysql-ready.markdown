---
layout: post
title: "Docker Compose: how to wait for the MySQL server container to be ready?"
description: Waiting for a database server to be ready before starting our own application, such as a middle-tier server, is a familiar issue. Docker Compose is no exception. Our own application container must also wait for their own database server container ready to accept requests before sending requests over. I've tried two ( 2 ) “wait for” tools which are officially recommended by Docker. I'm discussing my attempts in this post, and describing some of the pending issues I still have.
tags:
- Docker
- docker-compose
- wait for
- database server
- MySQL server
---

*Waiting for a database server to be ready before starting our own application, such as a middle-tier server, is a familiar issue. Docker Compose is no exception. Our own application container must also wait for their own database server container ready to accept requests before sending requests over. I've tried two ( 2 ) “wait for” tools which are officially recommended by Docker. I'm discussing my attempts in this post, and describing some of the pending issues I still have.*

| ![049-feature-image.png](https://behainguyen.files.wordpress.com/2022/11/049-feature-image.png) |
|:--:|
| *Docker Compose: how to wait for the MySQL server container to be ready?* |

<h2>Table of contents</h2>

<ul>
	<li style="margin-top:10px;"><a href="#environments">Environments</a></li>

	<li style="margin-top:10px;"><a href="#reference-docs-tuts-posts">Reference Documents, Tutorials and Posts</a></li>

	<li style="margin-top:10px;"><a href="#wait-for-it">wait-for-it</a>
	    <ul>
		   <li style="margin-top:10px;"><a href="#wait-for-it-dockerfile">Dockerfile</a></li>
		   <li style="margin-top:10px;"><a href="#env-file-env-docker">The Python environment file .env-docker</a></li>
		   <li style="margin-top:10px;"><a href="#wait-for-it-docker-compose">docker-compose.yml</a></li>
	    </ul>
	</li>

	<li style="margin-top:10px;"><a href="#atkrad-wait4x">atkrad/wait4x</a>
	    <ul>
		   <li style="margin-top:10px;"><a href="#atkrad-wait4x-dockerfile">Dockerfile</a></li>
		   <li style="margin-top:10px;"><a href="#atkrad-wait4x-docker-compose">docker-compose.yml</a></li>
	    </ul>	
	</li>
	
	<li style="margin-top:10px;"><a href="#my-other-docker-posts">Other Docker Posts Which I've Written</a></li>	
</ul>

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
<span class="keyword">Windows “docker-compose” CLI </span> -- <span class="keyword"> version 1.29.2, build 5becea4c</span>.
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
<span class="keyword">python:3.10.5-slim-buster</span> 
-- this WAS a 
<a href="https://hub.docker.com/_/python" title="Python Docker Official Image" target="_blank">
Python Docker Official Image</a>, I downloaded it a few months back. I checked just now, it is not 
listed there anymore, but I am <strong>guessing</strong> a closer version would still do for this post.
</li>
</ol>

<h3 style="color:teal;">
  <a id="reference-docs-tuts-posts">Reference Documents, Tutorials and Posts</a>
</h3>

I have used official Docker images in my development environment.
I've also attempted to build images for my own understanding. Before
starting Compose, I've checked out official documentations
and some tutorials. 

I've worked with a multi-tier application before.
Sitting between the web front-end and the database server is our own
application data server written as a 
<span class="keyword">
Windows service</span>: if a server machine 
must restart, our application data server must wait for the target
database server to be ready before starting itself.

At the outset, none of the visible tutorials on 
Compose which I've come across address the waiting issue, 
even though an application container and a database container are present;
and official Docker documents, on the hand, sporadically mentions
that this is an issue, but they don't immediately point to the 
actual document that addresses this issue! 

<ol>
<li style="margin-top:5px;">

<a href="https://docs.docker.com/compose/"
title="Docker Compose Overview" target="_blank">https://docs.docker.com/compose/</a> 
-- an overview of Compose.
</li>
<li style="margin-top:10px;">
This is the tutorial which jumps start me on Compose: 
<a href="https://geshan.com.np/blog/2022/02/mysql-docker-compose/"
title="How to use MySQL with Docker and Docker compose a beginners guide"
target="_blank">How to use MySQL with Docker and Docker compose a beginners guide</a>.
It does not address the waiting issue, I write a simple Python script which
runs only a query and prints out the rows. I expected it <strong>not to work</strong> 
consistently all the times, and it did not. I repeatedly run it, and there're times 
when the MySQL server container does not start on time.
</li>
<li style="margin-top:10px;">
Further Googling, I found this Docker document 
<a href="https://docs.docker.com/compose/startup-order/"
title="Control startup and shutdown order in Compose" target="_blank">Control startup and shutdown order in Compose</a>,
whereby several tools are recommended to implement the waiting, among them are
<a href="https://github.com/vishnubob/wait-for-it" title="wait-for-it" target="_blank">wait-for-it</a> and
<a href="https://github.com/atkrad/wait4x" title="Wait4X" target="_blank">Wait4X</a>.
</li>
<li style="margin-top:10px;">
I don't remember exactly how, but I found this Stack Overflow post 
<a href="https://stackoverflow.com/questions/42567475/docker-compose-check-if-mysql-connection-is-ready"
title="Docker-compose check if mysql connection is ready"
target="_blank">Docker-compose check if mysql connection is ready</a>, where:
<ul style="margin-bottom:20px;">
<li style="margin-top:10px;">
<a href="https://stackoverflow.com/users/13053425/erg"
title="user Erg" target="_blank">user Erg</a> discussed
<span class="keyword">
wait-for-it</span>.
</li>
<li style="margin-top:10px;">
<a href="https://stackoverflow.com/users/1906108/d%c3%a1vid-szab%c3%b3"
title="user Dávid Szabó" target="_blank">user Dávid Szabó</a> discussed
<span class="keyword">
<a id="atkrad-wait4x-dávid-szabó">atkrad/wait4x</a></span>.
</li>
</ul>
<strong>-- This post is a reproduction of their discussions and implementations.</strong>
</li>
<li style="margin-top:10px;">
Not directly related to this post, but the first 
<span class="keyword">
Docker</span> tutorial I took was 
<a href="https://docker-curriculum.com/"
title="Learn to build and deploy your distributed applications easily to the cloud with Docker "
target="_blank">Learn to build and deploy your distributed applications easily to the cloud with Docker</a>,
it's an excellent tutorial and does also cover Compose.
</li>
</ol>

On <span class="keyword">mysql:8.0.30-debian Docker image build</span>, I've also written two related posts:

<ol>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/08/09/docker-on-windows-10-running-mysql8-0-30-debian-with-a-custom-config-file/"
title="Docker on Windows 10: running mysql:8.0.30-debian with a custom config file"
target="_blank">Docker on Windows 10: running mysql:8.0.30-debian with a custom config file</a> -- 
the <span class="keyword">
--mounts</span> configuration are re-used in this post:
<ul>
<li style="margin-top:10px;">
<span class="keyword">
--mount type=bind,source=//e/mysql-config,target=/etc/mysql/conf.d</span>
</li>

<li style="margin-top:10px;">
<span class="keyword">
--mount source=mysqlvol,target=/var/lib/mysql</span>
</li>
</ul>
</li>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/10/21/docker-on-windows-10-mysql8-0-30-debian-log-files/"
title="Docker on Windows 10: mysql:8.0.30-debian log files"
target="_blank">Docker on Windows 10: mysql:8.0.30-debian log files</a>.
</li>
</ol>

<h3 style="color:teal;">
  <a id="wait-for-it">wait-for-it</a>
</h3>

<span class="keyword">python:3.10.5-slim-buster</span> 
is a <span class="keyword">
Debian GNU/Linux 10 (buster)</span>. Follow the 
<a href="https://tracker.debian.org/pkg/wait-for-it"
title="Debian package"
target="_blank">Debian package</a> link given by 
<a href="https://github.com/vishnubob/wait-for-it" title="wait-for-it" target="_blank">wait-for-it</a>,
we'll eventually find this link 
<a href="https://packages.debian.org/source/oldoldstable/wait-for-it"
title="Source Package: wait-for-it (0.0~git20160501-1)"
target="_blank">https://packages.debian.org/source/oldoldstable/wait-for-it</a>,
I downloaded the 
<strong>wait-for-it_0.0~git20160501.orig.tar.gz</strong> file and extracted 
<strong>wait-for-it.sh</strong> out to the project root directory where
<em>setup.py</em>, <em>app.py</em>, <strong>.dockerignore</strong>, <strong>Dockerfile</strong>
and <strong>docker-compose.yml</strong> are.

I will not list the content of <strong>.dockerignore</strong> as it is application specific.
<strong>Dockerfile</strong> is somewhat irrelevant is the context of this discussion,
except for the Python environment file <strong>.env-docker</strong>.

<h4 style="color:teal;">
  <a id="wait-for-it-dockerfile">Dockerfile</a>
</h4>

```
# syntax=docker/dockerfile:1

FROM python:3.10.5-slim-buster

WORKDIR /book_keeping

COPY . .

EXPOSE 8000

RUN /usr/local/bin/python -m pip install --upgrade pip \
    && pip3 install -e . \
	&& pip3 install bh_utils-1.0.0-py3-none-any.whl \
	&& pip3 install bh_validator-1.0.0-py3-none-any.whl

RUN chmod +x wait-for-it.sh

RUN rm bh_utils-1.0.0-py3-none-any.whl \
    && rm bh_validator-1.0.0-py3-none-any.whl \
    && mv .env-docker .env	
	
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0" ]
```

Please note:

```
RUN chmod +x wait-for-it.sh
```

We are going to run 
<span class="keyword">
wait-for-it.sh</span> later in Compose, I'm giving it 
<span class="keyword">
execute</span> permission in readiness.

<h4 style="color:teal;">
  <a id="env-file-env-docker">The Python environment file .env-docker</a>
</h4>

The Python environment file <strong>.env-docker</strong> is the same as 
my local development one, except:

```
SQLALCHEMY_DATABASE_URI = mysql+mysqlconnector://behai1:password@mysql_db/ompdev1
```

where the database host is 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
mysql_db</span> -- this is the service name of the MySQL container in the 
<strong>docker-compose.yml</strong> file. And according to 
<a href="https://docs.docker.com/compose/networking/"
title="Networking in Compose" target="_blank">Networking in Compose</a>:

> Each container can now look up the hostname web or db and get back the appropriate container’s IP address. For example, web’s application code could connect to the URL postgres://db:5432 and start using the Postgres database.

<h4 style="color:teal;">
  <a id="wait-for-it-docker-compose">docker-compose.yml</a>
</h4>

```yaml
version: "3.9"
services:
  mysql_db:
    image: mysql:8.0.30-debian
    cap_add:
      - SYS_NICE    
    restart: always
    environment:
      - MYSQL_DATABASE=ompdev1
      - MYSQL_ROOT_PASSWORD=pcb.2176310315865259
    ports:
      - '3306:3306'
    volumes:
      - type: bind
        source: //e/mysql-config
        target: /etc/mysql/conf.d 
        
      - type: volume 
        source: mysqlvol
        target: /var/lib/mysql

  app:
    container_name: book-keeping
    restart: always    
    build: .
    image: book-keeping
    depends_on:
      - mysql_db
    ports:
      - '8000:8000'
    command: ./wait-for-it.sh -t 40 mysql_db:3306 -- python ./app.py
    #command: python -m flask run --host=0.0.0.0:8000
    #command: python3 -m flask run
    command: flask run -h 0.0.0.0 -p 8000
    
volumes:
  mysqlvol:
    external: true
```

In the above Compose file, 
<span class="keyword">
wait-for-it.sh</span> is called in pretty much the same manner as it is
documented. 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
mysql_db</span> is the MySQL database server address as discussed previously;
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
3306</span> is the default port:

```
command: ./wait-for-it.sh -t 40 mysql_db:3306 -- python ./app.py
```

We will go through some of the configuration items which are 
not so apparent, for others, such as 
<span class="keyword">
restart</span>,
<span class="keyword">
depends_on</span> etc., please find out for yourself.

<ul>
<li style="margin-top:10px;">
<span class="keyword">
services:mysql_db:volumes:</span>; 
recall this post which I mention earlier 
<a href="https://behainguyen.wordpress.com/2022/08/09/docker-on-windows-10-running-mysql8-0-30-debian-with-a-custom-config-file/"
title="Docker on Windows 10: running mysql:8.0.30-debian with a custom config file"
target="_blank">Docker on Windows 10: running mysql:8.0.30-debian with a custom config file</a>.
The same 
<span class="keyword">
bind --mount</span> is used in Compose, syntax translated according to this Docker document 
<a href="https://docs.docker.com/storage/bind-mounts/#use-a-bind-mount-with-compose"
title="Use a bind mount with compose" target="_blank">Use a bind mount with compose</a>.
This enables my Compose to use the existing database / volumes, and
the existing MySQL custom configuration file.
</li>

<li style="margin-top:10px;">
 <span class="keyword">
volumes:mysqlvol:external:true</span>; recall 
<span class="keyword">
--mount source=mysqlvol,target=/var/lib/mysql</span>? 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
mysqlvol</span> is the directory on the host machine, Windows 10 Pro using WSL2 
in my case, where Docker container data is stored: I've written about this in
<a href="https://behainguyen.wordpress.com/2022/07/29/python-docker-volumes-where-is-my-sqlite-database-file/#docker-volumes-on-disk"
title="Docker volumes on disk" target="_blank">Docker volumes on disk</a>. 
Referencing it and setting 
<span class="keyword">
external</span> to
<span class="keyword">
true</span> in this case to signify that this volume has been created 
outside of Compose, please see the official document 
<a href="https://docs.docker.com/compose/compose-file/compose-file-v3/#external"
title="Compose reference on volumes | external" 
target="_blank">Compose reference on volumes | external</a>.
</li>
<li style="margin-top:10px;">
<span class="keyword">
app:ports:'8000:8000' ( i.e. host port:container port )</span>; 
-- this enables accessing the Dockerised site as 
<a href="http://localhost:8000" title="http://localhost:8000" target="_blank">http://localhost:8000</a>,
without it, the next command would not work:
</li>
<li style="margin-top:10px;">
<span class="keyword">
app:command:flask run -h 0.0.0.0 -p 8000</span>; 
<span style="font-weight:bold;color:red;">placing this command here is my own guess works, 
I've not yet found any documentation on this, I am not sure if this will always work.</span>
I'm facing two ( 2 ) problems at this point:
<ol style="margin-bottom:10px;">
<li style="margin-top:10px;">
If I don't have this command here, the application container will 
not be able to start properly, it will just sit on the last command:
<span class="keyword">
./wait-for-it.sh -t 40 mysql_db:3306 -- python ./app.py</span> -- 
and keeps on restarting endlessly.
</li>
<li style="margin-top:10px;">
Before this command, I've tried several others as seen in the 
commented out ones, none of them allows connecting to the 
application container as 
<a href="http://localhost:8000" title="http://localhost:8000" target="_blank">http://localhost:8000</a>,
even though the container was running. It seems that this is a popular 
“problem”, and I have yet come across a concrete answer for it, different
solutions seem to work for different situations...
</li>
</ol>
This also means, the last command in the <strong>Dockerfile</strong>
<span class="keyword">
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0" ]</span> 
is not needed: I've tried, and found this is to be the case.
</li>
</ul>

<h3 style="color:teal;">
  <a id="atkrad-wait4x">atkrad/wait4x</a>
</h3>

The same <a href="#env-file-env-docker">Python environment file .env-docker</a>
is used. Except for the “wait for” implementation, everything else is identical
to the <a href="#wait-for-it">wait-for-it</a>'s implementation.

<span style="color:blue;">
And please note again, the “wait for” implementation of this section is not
mine -- I am merely reproducing the implementation quoted in the 
<a href="#atkrad-wait4x-dávid-szabó">Reference Documents, Tutorials and Posts</a>
above.
</span>

I did pull the 
<span class="keyword">
atkrad/wait4x</span> Docker image manually before running 
<span class="keyword">
docker-compose</span>, but I don't think that is necessary:

```
docker pull atkrad/wait4x
```

<h4 style="color:teal;">
  <a id="atkrad-wait4x-dockerfile">Dockerfile</a>
</h4>

```
# syntax=docker/dockerfile:1

FROM python:3.10.5-slim-buster

WORKDIR /book_keeping

COPY . .

EXPOSE 8000

RUN /usr/local/bin/python -m pip install --upgrade pip \
    && pip3 install -e . \
	&& pip3 install bh_utils-1.0.0-py3-none-any.whl \
	&& pip3 install bh_validator-1.0.0-py3-none-any.whl

RUN rm bh_utils-1.0.0-py3-none-any.whl \
    && rm bh_validator-1.0.0-py3-none-any.whl \
    && mv .env-docker .env	
	
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0" ]
```

<h4 style="color:teal;">
  <a id="atkrad-wait4x-docker-compose">docker-compose.yml</a>
</h4>

```yaml
version: "3.9"
services:
  mysql_db:
    image: mysql:8.0.30-debian
    cap_add:
      - SYS_NICE    
    restart: always
    environment:
      - MYSQL_DATABASE=ompdev1
      - MYSQL_ROOT_PASSWORD=pcb.2176310315865259
    ports:
      - '3306:3306'
    volumes:
      - type: bind
        source: //e/mysql-config
        target: /etc/mysql/conf.d 
        
      - type: volume 
        source: mysqlvol
        target: /var/lib/mysql

  app:
    container_name: book-keeping
    restart: always    
    build: .
    image: book-keeping
    depends_on:
      wait-for-db:
        condition: service_completed_successfully      
    ports:
      - '8000:8000'
    command: flask run -h 0.0.0.0 -p 8000

  wait-for-db:
    image: atkrad/wait4x
    depends_on:
      - mysql_db
    command: tcp mysql_db:3306 -t 30s -i 250ms
    
volumes:
  mysqlvol:
    external: true
```

The “wait for” command is:

```
command: tcp mysql_db:3306 -t 30s -i 250ms
```

I would prefer this method rather than the other one, this tool seems to be
actively maintained, more than half a million downloads. And most importantly,
I don't have to carry around another additional script. I don't think it adds
much to the final image size either.

<h3 style="color:teal;">
  <a id="my-other-docker-posts">Other Docker Posts Which I've Written</a>
</h3>

<ol>
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

✿✿✿

Thank you for reading... And I hope you found this post useful. Stay safe as always.
