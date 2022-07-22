---
layout: post
title: "Python: Docker image build -- install required packages via requirements.txt vs editable install."

---

Install via requirements.txt means using this image build step command “RUN pip3 install -r requirements.txt”. Editable install means using the “RUN pip3 install -e .” command. I've experienced that install via requirements.txt resulted in images that do not run, whereas using editable install resulted in images that do work as expected. I'm presenting my findings in this post.

| ![030-feature-image.png](https://behainguyen.files.wordpress.com/2022/07/030-feature-image.png) |
|:--:|
| *Python: Docker image build -- install required packages via requirements.txt vs editable install.* |

<p>
The first 
<span class="keyword">
Docker</span> tutorial I took was 
<a href="https://docker-curriculum.com/"
title="Learn to build and deploy your distributed applications easily to the cloud with Docker "
target="_blank">Learn to build and deploy your distributed applications easily to the cloud with Docker</a>,
it's an excellent tutorial and I did successfully complete all of it. Then I did this 
<a href="https://docs.docker.com/language/python/build-images/" 
title="Build your Python image" target="_blank">Build your Python image</a> -- only 
this first part.
</p>

<p>
What's common between them are -- in my observations:
</p>

<ol>
<li style="margin-top:5px;">
The <span class="keyword">
Python</span> projects have only a single 
<span class="keyword">
Python file</span>. I did scan through some other tutorials, the projects
also have a 
single <span class="keyword">
Python file</span>.
</li>

<li style="margin-top:10px;">
In the 
<span class="keyword">
Dockerfile</span> file, they both use 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
RUN pip3 install -r requirements.txt</span> to install required packages.
</li>
</ol>

<p>
I would like to try building an image for a project which has 
more than a single module: most real projects would have more 
than one module. The code for 
<a href="https://behainguyen.wordpress.com/2022/06/25/synology-ds218-preparing-python-3-9-beta-compelete-devepment-environment/"
title="Synology DS218: preparing Python 3.9 Beta compelete devepment environment."
target="_blank">Synology DS218: preparing Python 3.9 Beta compelete devepment environment.</a>
is fairly simple, and would be a good first try.
</p>

<p>
This is the repository 
<a href="https://github.com/behai-nguyen/app-demo"
title="GitHub behai-nguyen/app-demo" 
target="_blank">https://github.com/behai-nguyen/app-demo</a>
for the code. For the above post, the 
<span class="keyword">
tag</span> is 
<span class="keyword">
<strong>v1.0.0</strong></span>. It can be cloned with:
</p>

```
git clone -b v1.0.0 https://github.com/behai-nguyen/app-demo.git
```

<p>
Please note, all 
<span class="keyword">
Docker builds</span> discussed in this post've been out carried on 
<span class="keyword">
Windows 10 Pro</span>, using 
<span class="keyword">
docker CLI version 20.10.12, build e91ed57</span>.
</p>

<p>
To recap, the project layout for 
<span class="keyword">
app-demo</span> at 
<span class="keyword">
tag <strong>v1.0.0</strong></span> is:
</p>

```
D:\app_demo\
|
|-- .env
|-- app.py
|-- setup.py
|
|-- src\
|   |
|   |-- app_demo\
|       |   
|       |-- __init__.py
|       |-- config.py
|
|-- venv\
```

<p>
I did create 
<span class="keyword">
virtualenv</span> 
<span class="keyword">
venv</span> for this project in 
<span class="keyword">
Windows 10</span>.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="build-with-requirements">Building using “RUN pip3 install -r requirements.txt” command</a>
</h3>

<p>
Please note, 
<span style="color:blue;font-weight:bold;">
this image build step command renders 
<span class="keyword">
setup.py</span> not in use.
</span>
</p>

<p>
Generate the 
<span class="keyword">
requirements.txt</span> file with:
</p>

```
D:\app_demo>venv\Scripts\pip.exe freeze > requirements.txt
```

<p>
Then manually removed everything except for those packages specified 
in the section 
<span class="keyword">
install_requires</span> in the 
<span class="keyword">
setup.py</span> file.
</p>

```
File D:\app_demo\requirements.txt
```

```
Flask==2.1.2
python-dotenv==0.20.0
```

```
File D:\app_demo\Dockerfile
```

```
# syntax=docker/dockerfile:1

FROM python:3.10.5-slim-buster

WORKDIR /app_demo

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0" ]
```

```
File D:\app_demo\.dockerignore
```

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
venv
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis
FlaskApp.wsgi
Working
```

<p>
The root level of the project layout is now:
</p>

```
D:\app_demo\
|
|-- .env
|-- app.py
|-- setup.py
|-- requirements.txt 
|-- Dockerfile
|-- .dockerignore
|
...
```

<p>
The command to build:
</p>

```
D:\app_demo>docker build --tag app-demo .
```

<p>
The build runs successfully. To run the newly built image:
</p>

```
D:\app_demo>docker run --publish 8000:5000 --rm app-demo
```

<p>
It does not work, as can be seen in the screen capture below:
</p>

![030-01-run-failed.png](https://behainguyen.files.wordpress.com/2022/07/030-01-run-failed.png)

<p style="clear:both;">
<span class="keyword">
The error is 
<span style="color:red;font-weight:bold;">ModuleNotFoundError: No module named 'app_demo'</span></span>.
</p>

<p>
These changes for this not-working-built can be cloned using:
</p>

```
git clone -b v1.0.1 https://github.com/behai-nguyen/app-demo.git
```

<p>✿✿✿</p>

<p>
Google search suggests that others also have experienced similar error. 
The suggestion is to use absolute import -- for example, please see  
<a href="https://stackoverflow.com/questions/70329984/module-not-found-error-with-python-in-docker"
title="Module not found error with Python in Docker"
target="_blank">Module not found error with Python in Docker</a>.
</p>

<p>
I did try out absolute import, since the project is small, the changes 
are minuscule, and the resultant image does run. However, that does not 
seem right... I should not have to do that...
</p>

<p>
The changes to use absolute import can be cloned using:
</p>

```
git clone -b v1.0.2 https://github.com/behai-nguyen/app-demo.git
```

<p>
Basically, relevant 
<span class="keyword">
import</span> statements in:
</p>

```
File D:\app_demo\app.py
File D:\app_demo\src\app_demo\__init__.py
```

<p>
were prefixed with 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
src.</span> to become respectively:
</p>

```python
from src.app_demo import create_app
from src.app_demo.config import get_config
```

<p>
Build and run, respectively, with:
</p>

```
D:\app_demo>docker build --tag app-demo .
D:\app_demo>docker run --publish 8000:5000 --rm app-demo
```

<p>
It runs successfully. 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
http://localhost:8000</span> displays the expect output of
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
Hello, World!</span>
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="build-with-edit-install">Building using “RUN pip3 install -e .” command</a>
</h3>

<p>
<span style="color:blue;font-weight:bold;">
Please note for this image build step:
</span>
</p>

<p>
❶ Both:
</p>

```
File D:\app_demo\app.py
File D:\app_demo\src\app_demo\__init__.py
```
<p>
have their 
<span class="keyword">
import</span> statements reversed back to 
<span class="keyword">
relative import</span>:
</p>

```python
from app_demo import create_app
from app_demo.config import get_config
```

<p>
That is, prefix 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
src.</span> added in the last build was removed.
</p>

<p> 
❷ This image build step command renders 
<span class="keyword">
requirements.txt</span> obsolete.
</p>

<p>✿✿✿</p>

<p>
I was doing another 
<span class="keyword">
Docker image</span> for another 
<span class="keyword">
Python</span> project, I thought I would just try editable install 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
RUN pip3 install -e .</span> instead. I did think that I would have to 
change the source codes to absolute import anyway, so why not just 
use <span class="keyword">
setup.py</span> that's already in place. The build just went through with no
problem. I ran it to get the first import failure... It does not fail!
</p>

<p>
It works! <strong>I still don't know why it works!</strong>
</p>

<p>
So I go back to this project, and hence this post. Changes are:
</p>

```
File D:\app_demo\Dockerfile
```

```
# syntax=docker/dockerfile:1

FROM python:3.10.5-slim-buster

WORKDIR /app_demo

COPY . .

RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip3 install -e .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0" ]
```

<p>
<span class="keyword">
requirements.txt</span> is obsolete; it's added to 
<span class="keyword">
D:\app_demo\.dockerignore</span>.
</p>

```
File D:\app_demo\.dockerignore
```

```
... 
requirements.txt
```

<p>
Clone the new changes with the below command, please discard 
<span class="keyword">
requirements.txt</span>:
</p>

```
git clone -b v1.0.3 https://github.com/behai-nguyen/app-demo.git
```

<p>
Build and run, respectively, with:
</p>

```
D:\app_demo>docker build --tag app-demo .
D:\app_demo>docker run --publish 8000:5000 --rm app-demo
```

<p>
It runs successfully:
</p>

![030-02-run-worked.png](https://behainguyen.files.wordpress.com/2022/07/030-02-run-worked.png)

<p style="clear:both;">
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
http://localhost:8000</span> displays the expect output of
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
Hello, World!</span>
</p>

<p>✿✿✿</p>

<p>
I don't know why 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
RUN pip3 install -e .</span> works... Please tell me if you know, I would appreciate that very much.
</p>

<p>
Since I've made my decision to use 
<span class="keyword">
setup.py</span>, this 
<span class="keyword">
Docker</span> image build step just works out great. I'm happy with it.
Thank you for reading and I hope you find this post useful somehow.
</p>