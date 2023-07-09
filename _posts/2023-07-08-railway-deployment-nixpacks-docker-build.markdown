---
layout: post
title: "Python, Flask: Railway.app deployment and Railway's Nixpacks Docker image build tool."

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list:
    - "https://behainguyen.files.wordpress.com/2023/07/074-01.png"
    - "https://behainguyen.files.wordpress.com/2023/07/074-02.png"
    - "https://behainguyen.files.wordpress.com/2023/07/074-03.png"

description: I've successfully deployed my Australian postcodes API project to railway.app. I did have some problem during deployment. I'm describing how I've addressed this problem. In the process, we're also covering the following&#58; ⓵ running Railway's own Nixpacks Docker build tool locally on Ubuntu 22.10. ⓶ Override the Nixpacks-built Docker image's CMD&#58; we look at three (3) ways to run the Flask CLI command venv/bin/flask update-postcode, and similarly, we look at how to override the start command gunicorn wsgi&#58;app --preload specified in the Nixpacks required Procfile.
tags:
- Python
- Flask
- Railway
- deployment
- Nixpacks
- Docker
- image
---

<em style="color:#111;">I've successfully deployed my Australian postcodes API project to <a href="https://railway.app" title="https://railway.app" target="_blank">https://railway.app</a>. I did have some problem during deployment. I'm describing how I've addressed this problem. In the process, we're also covering the following: ⓵ running Railway's own Nixpacks Docker build tool locally on Ubuntu 22.10. ⓶ Override the Nixpacks-built Docker image's <code>CMD</code>: we look at three (3) ways to run the Flask CLI command <code>venv/bin/flask update-postcode</code>, and similarly, we look at how to override the start command <code>gunicorn wsgi:app --preload</code> specified in the Nixpacks required <a href="https://github.com/behai-nguyen/bh_aust_postcode/blob/main/Procfile" title="Nixpacks required Procfile" target="_blank">Procfile</a>.</em>

| ![074-feature-image.png](https://behainguyen.files.wordpress.com/2023/07/074-feature-image.png) |
|:--:|
| *Python, Flask: Railway.app deployment and Railway's Nixpacks Docker image build tool.* |

These are the two (2) API endpoints hosted on Railway:

<ol dir="auto">
<li>
<p dir="auto">Swagger UI Documentation: <a href="https://web-production-ed7a.up.railway.app/api/v0/ui" rel="nofollow" target="_blank"> https://web-production-ed7a.up.railway.app/api/v0/ui </a>.</p>
</li>
<li>
<p dir="auto">Endpoint API: <code>web-production-ed7a.up.railway.app/api/v0/aust-postcode/</code>.<br>E.g. To search for localities which contain <code>spring</code>: <a href="https://web-production-ed7a.up.railway.app/api/v0/aust-postcode/spring" rel="nofollow" target="_blank"> https://web-production-ed7a.up.railway.app/api/v0/aust-postcode/spring </a>.</p>
</li>
</ol>

🚀 Full source code and documentation: <a href="https://github.com/behai-nguyen/bh_aust_postcode" title="https://github.com/behai-nguyen/bh_aust_postcode" target="_blank">https://github.com/behai-nguyen/bh_aust_postcode</a>. This repo is now Railway-deployment ready. It includes Railway's required files <code>requirements.txt</code>, <code>Procfile</code> and <code>runtime.txt</code>.

As noted in the <a href="https://github.com/behai-nguyen/bh_aust_postcode/blob/main/README.md" title="README" target="_blank">README.md</a> file, the current version supports PostgreSQL, instead of SQLite as it did originally, since <a href="https://railway.app" title="https://railway.app" target="_blank">https://railway.app</a> does not support SQLite.

Related posts on this Australian postcodes API project. Please note, except for changing to support PostgreSQL, there was no change to functionalities:

<ol>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/05/18/python-a-simple-web-api-to-search-for-australian-postcodes-based-on-locality-aka-suburb/" title="Python: A simple web API to search for Australian postcodes based on locality aka suburb." target="_blank">Python: A simple web API to search for Australian postcodes based on locality aka suburb.</a>
</li>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/05/25/ubuntu-22-10-hosting-a-python-flask-web-api-with-gunicorn-and-nginx/" title="Ubuntu 22.10: hosting a Python Flask web API with Gunicorn and Nginx." target="_blank">Ubuntu 22.10: hosting a Python Flask web API with Gunicorn and Nginx.</a>
</li>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/06/05/jquery-plugin-bhaustpostcode-to-work-with-the-search-australian-postcodes-web-api/" title="jQuery plugin: bhAustPostcode to work with the search Australian postcodes web API." target="_blank">jQuery plugin: bhAustPostcode to work with the search Australian postcodes web API.</a>
</li>
</ol>

❶ <a href="https://railway.app/" title="Railway" target="_blank">Railway</a> deployment problem.

On a side note, I stumbled upon the <a href="https://railway.app/" title="Railway" target="_blank">Railway</a> website. I was able to set up a PostgreSQL database fairly quickly, I can connect to it using <code>pgAdmin 4</code> version <code>6.18</code>, Windows 10. The documentation is easy to understand, I like it. I played around with it for awhile. I was on a free plan. But the next day, they stated that they can't verify who I am using my GitHub account, so I joined the Hobby Plan. It is only fair, we need to pay for the services.

Before deployment, I was actually thinking that I already have it in the bag 😂, since the database is my biggest concern, and I am pretty sure I have no problem with it. But before talking to the database, the project needs to be successfully deployed.

Railway reported error, these are the last lines of my second deployment log:

```
...
File "/app/wsgi.py", line 1, in &lt;module>
from app import app
File "/app/app.py", line 3, in &lt;module>
from bh_aust_postcode import create_app
ModuleNotFoundError: No module named 'bh_aust_postcode'
[2023-07-05 10:36:48 +0000] [9] [INFO] Worker exiting (pid: 9)
[2023-07-05 10:36:48 +0000] [1] [INFO] Shutting down: Master
[2023-07-05 10:36:48 +0000] [1] [INFO] Reason: Worker failed to boot.
```

To recap, the directory structure of the project is as follows:

```
/home/behai/webwork/bh_aust_postcode
├── app.py
├── Hosting.md
├── instance
├── LICENSE
├── omphalos-logging.yml
├── Procfile
├── pyproject.toml
├── pytest.ini
├── README.md
├── requirements.txt
├── runtime.txt
├── src
│     ├── bh_aust_postcode
│     │     ├── api
│     │     │     ├── bro.py
│     │     │     ├── __init__.py
│     │     │     ├── postcode_pool.py
│     │     │     └── routes.py
│     │     ├── commands
│     │     │     ├── schema.sql
│     │     │     └── update_postcode.py
│     │     ├── config.py
│     │     ├── __init__.py
│     │     └── utils
│     │         ├── __init__.py
├── tests
│     ├── conftest.py
│     ├── __init__.py
│     ├── test_api_endpoints.py
│     ├── test_bro.py
│     └── test_postcode_pool.py
└── wsgi.py
```

Seeing the error, I did verify that the name of the project root directory <code>bh_aust_postcode</code> is not important, it can be anything. Looking at Railway's build log, I understand that the root <code>/app</code> directory is the value of the Docker image environment variable <code>WORKDIR</code> -- and that should not be a problem!

What I did next was installing Railway's own build tool <a href="https://nixpacks.com/docs" title="Nixpacks" target="_blank">Nixpacks</a> to my Ubuntu 22.10 machine and did my own build: I did not supply my own <code>Dockerfile</code>, I want to use the default to closely match the Railway's image.

-- My own built image using <a href="https://nixpacks.com/docs" title="Nixpacks" target="_blank">Nixpacks</a> produced the same error! Which is somehow... a good thing!

I started to fully qualify all <code>import</code>s across the entire project. I.e. changing from:

```python
from bh_aust_postcode.config import get_database_connection
```

to:

```python
from src.bh_aust_postcode.config import get_database_connection
```

And it finally deployed! 

-- Only then I remember addressing this very issue in <a href="https://behainguyen.wordpress.com/2022/07/22/python-docker-image-build-install-required-packages-via-requirements-txt-vs-editable-install/" title="Python: Docker image build — install required packages via requirements.txt vs editable install." target="_blank">Python: Docker image build — install required packages via requirements.txt vs editable install</a>! And that was nearly one (1) year ago! But not all wasted, I learn about <a href="https://nixpacks.com/docs" title="Nixpacks" target="_blank">Nixpacks</a> and a bit more about Docker.

<strong>I did not want to use absolute import, but I did in this case. Perhaps if I supply my own <code>Dockerfile</code>, then I can use editable install and do not have to use absolute import?</strong>

❷ Installing and running Railway’s own <a href="https://nixpacks.com/docs" title="Nixpacks" target="_blank">Nixpacks</a> Docker build tool locally on Ubuntu 22.10.

<a href="https://nixpacks.com/docs/install" title="Nixpacks Installation" target="_blank">Nixpacks installation</a> is simple. Download the appropriate installation file from <a href="https://github.com/railwayapp/nixpacks/releases" title="Nixpacks Releases" target="_blank">Nixpacks Releases</a>.

For <em>HP Pavilion 15 Notebook PC</em>, <code>Born On Date</code> of <code>04/October/2014</code>, it is <code>nixpacks-v1.9.2-amd64.deb</code>, and I copied to it <code>/home/behai/Public/</code>. Then run the following command to install:

```
$ sudo dpkg -i /home/behai/Public/nixpacks-v1.9.2-amd64.deb
```

We need to set the values of the environment variables in the <code>.env</code> file appropriate for the Docker image. 

```
Content of /home/behai/webwork/bh_aust_postcode/.env:
```

```
SECRET_KEY="&gt;s3g;?uV^K=`!(3.#ms_cdfy&lt;c4ty%"
FLASK_APP=app.py
FLASK_DEBUG=True
SOURCE_POSTCODE_URL="http://192.168.0.17/australian_postcodes.json"
KEEP_DOWNLOADED_POSTCODES=False
DB_CREATE_SCRIPT="schema.sql"
SCHEMA_NAME='bh_aust_postcode'
POSTCODE_TABLE_NAME='postcode'
PGHOST=192.168.0.17
PGDATABASE=ompdev
PGUSER=postgres
PGPASSWORD=pcb.2176310315865259
PGPORT=5432
```

Just to save a bit of data usage, I don't want to download the postcodes from <a href="https://www.matthewproctor.com/Content/postcodes/australian_postcodes.json" title="https://www.matthewproctor.com/Content/postcodes/australian_postcodes.json" target="_blank">https://www.matthewproctor.com/Content/postcodes/australian_postcodes.json</a> every time I do a test run, I store a copy in the default Nginx site, it can be accessed as <code>http://192.168.0.17/australian_postcodes.json</code>. Where <code>192.168.0.17</code> is the IP address of the Ubuntu 22.10 machine.

The PostgreSQL database server used is the Official Docker image running on Ubuntu 22.10, <a href="https://behainguyen.wordpress.com/2023/01/13/using-postgresql-official-docker-image-on-windows-10-and-ubuntu-22-10-kinetic/#ubuntu-22-10" title="Using PostgreSQL Official Docker image on Windows 10 and Ubuntu 22.10 kinetic." target="_blank">please see this post for how to set it up</a>. Environment variables <code>PGHOST</code>, <code>PGDATABASE</code>, <code>PGUSER</code>, <code>PGPASSWORD</code> and <code>PGPORT</code> specify database connection information. 

To build, run the below command. Please note, ⓵ the present working directory is <code>/home/behai/</code>, ⓶ the name of the resultant Docker image is <code>bh-aust-postcode</code>:

```
$ sudo nixpacks build webwork/bh_aust_postcode --name bh-aust-postcode
```

The partial build log is shown in the first two (2) screenshots, the resultant Docker image listing is in the last one:

{% include image-gallery.html list=page.gallery-image-list %}

<!-- WordPress gallery, align right 
https://behainguyen.files.wordpress.com/2023/07/074-01.png
https://behainguyen.files.wordpress.com/2023/07/074-02.png
https://behainguyen.files.wordpress.com/2023/07/074-03.png
-->

❸ Override the Docker image's <code>CMD</code>.

⓵ Three (3) ways to run the Flask CLI command <code>venv/bin/flask update-postcode</code> for the Docker image.

As noted in the <a href="https://github.com/behai-nguyen/bh_aust_postcode/blob/main/README.md" title="README" target="_blank">README.MD</a> file, we need to run the following command to download postcodes and populate the database:

```
$ venv/bin/flask update-postcode
```

The Railway's equivalence, using its own CLI is:

```
$ railway run flask update-postcode
```

I can verify that it works, because I've successfully run it to populate the database hosted by Railway. I've never thought about this before, till now: how do we run commands such as this from a Docker image?

The obvious answer is to run the target Docker image in <code>bash</code> mode, then run application's commands inside it. Command to get to <code>bash</code> interactive mode:

```
$ sudo docker run -it --rm bh-aust-postcode bash 
```

The below screenshot shows <code>bh-aust-postcode</code> in <code>bash</code> mode:

![074-04.png](https://behainguyen.files.wordpress.com/2023/07/074-04.png)

Note: it does not show the Python virtual environment directory <code>venv</code>, I did supply a local <code>.gitignore</code> file, and <a href="https://nixpacks.com/docs" title="Nixpacks" target="_blank">Nixpacks</a> uses it for the build.

And running the <code>venv/bin/flask update-postcode</code> equivalent command:

```
root@598d49469064:/app# flask update-postcode
```

Output:

![074-05.png](https://behainguyen.files.wordpress.com/2023/07/074-05.png)

The second approach is to override Docker <code>CMD</code>. I.e.:

```
$ sudo docker run -it bh-aust-postcode "flask update-postcode"
```

Output:

![074-06.png](https://behainguyen.files.wordpress.com/2023/07/074-06.png)

The third method is to override <code>ENTRYPOINT</code>. I found the command a little nonintuitive:

```
$ sudo docker run -it --entrypoint /opt/venv/bin/flask bh-aust-postcode update-postcode
```

On <code>/opt/venv/bin/flask</code>, just <code>flask</code> it would not work, the error is about executable not found. And its output is identical to the previous two (2):

![074-07.png](https://behainguyen.files.wordpress.com/2023/07/074-07.png)

⓶ Override the start command <code>gunicorn wsgi:app --preload</code> specified in the Nixpacks required <a href="https://github.com/behai-nguyen/bh_aust_postcode/blob/main/Procfile" title="Nixpacks required Procfile" target="_blank">Procfile</a>.

In a similar manner to the previous section, we can run <code>bh-aust-postcode</code> image with a specific port and non-routable <code>0.0.0.0</code> IP address:

```
$ sudo docker run -it bh-aust-postcode "gunicorn --bind 0.0.0.0:5000 wsgi:app"
$ sudo docker run -it --entrypoint /opt/venv/bin/gunicorn bh-aust-postcode --bind 0.0.0.0:5000 wsgi:app
```

While the container is running, both of the following endpoints API will work locally:

```
$ curl http://172.17.0.3:5000/api/v0/ui
$ curl http://172.17.0.3:5000/api/v0/aust-postcode/spring
```

Please note, <code>172.17.0.3</code> is the <code>IPv4Address</code> of the container. We run the image without specifying the container name. To find the container IP address we need to know the container name.

The following command shows all available containers, and whether or not they've stopped or still are running:

```
$ sudo docker ps -a
```

Since we're using the default network <code>bridge</code>:

```
$ sudo docker network inspect bridge
```

Look for the container name in the output, the value of <code>IPv4Address</code> is the IP address which we should use.

It has been an interesting exercise for me. The deployment process in itself is not that complicated. Involving a database, we'll need to carry a few steps, but that's to be expected. I would like to write about it in a later post. I hope you find the information in this post useful. Thank you for reading and stay safe as always.

✿✿✿

Feature image sources:

<ul>
<li>
<a href="https://in.pinterest.com/pin/337277459600111737/" target="_blank">https://in.pinterest.com/pin/337277459600111737/</a>
</li>
<li>
<a href="https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper" target="_blank">https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper</a>
</li>
<li>
<a href="https://railway.app/design" target="_blank">https://railway.app/design</a>
</li>
<li>
<a href="https://icon-icons.com/download/170045/PNG/512/" target="_blank">https://icon-icons.com/download/170045/PNG/512/</a>
</li>
<li>
<a href="https://seeklogo.com/vector-logo/332789/python" target="_blank">https://seeklogo.com/vector-logo/332789/python</a>
</li>
<li>
<a href="https://flask-restx.readthedocs.io/en/latest/" target="_blank">https://flask-restx.readthedocs.io/en/latest/</a>
</li>
<li>
<a href="https://www.vectorstock.com/royalty-free-vector/australia-map-with-flag-blue-red-background-vector-25323215" target="_blank">https://www.vectorstock.com/royalty-free-vector/australia-map-with-flag-blue-red-background-vector-25323215</a>
</li>
<li>
<a href="https://logos-world.net/australia-post-logo/" target="_blank">https://logos-world.net/australia-post-logo/</a>
</li>
</ul>