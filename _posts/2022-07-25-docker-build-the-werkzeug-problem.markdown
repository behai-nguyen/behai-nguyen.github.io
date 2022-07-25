---
layout: post
title: "Python: Docker image build -- “the Werkzeug” problem 🤖!"

---

I've experienced Docker image build installed a different version of the Werkzeug dependency package than the development editable install process. And this caused the Python project in the Docker image failed to run. Development editable install means running the “pip3 install -e .” command within an active virtual environment. I'm describing the problem and how to address it in this post.

| ![031-feature-image.png](https://behainguyen.files.wordpress.com/2022/07/031-feature-image.png) |
|:--:|
| *Python: Docker image build -- “the Werkzeug” problem 🤖!* |

<p>
The environments in this post: 
⓵ <span class="keyword">
Windows 10 Pro version 10.0.19044 Build 19044</span>. ⓶ 
<span class="keyword">
docker CLI version 20.10.12, build e91ed57.</span>
</p>

<p>
Please note, the 
<span class="keyword">
Python</span> code in this post is a continuation of the code used in the post 
<a href="https://behainguyen.wordpress.com/2022/07/16/python-interactive-shell-and-shell_context_processor-decorator/"
title="Python: interactive shell and shell_context_processor() decorator."
target="_blank">Python: interactive shell and shell_context_processor() decorator.</a>,
whom code can be cloned with:
</p>

```
git clone -b v1.0.1 https://github.com/behai-nguyen/flask-restx-demo.git
```

<p>✿✿✿</p>

<p>
On around the 20/July/2022, I did a 
<span class="keyword">
Docker build</span> for this 
<span class="keyword">
Python</span> project using editable install image build step:
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
RUN pip3 install -e .</span>. I was able to run this image successfully. In fact, I 
did use it to learn 
<span class="keyword">
Docker volumes</span>: I started and stopped the runs several times. 
I'm 100% certain that it worked. I removed all containers, 
images and volumes afterward.
</p>

<p>
I've manually recorded all essential commands and their results in a text 
file -- I still am doing that. On the 24/July/2022, I repeated what 
I've done previously: the build worked, but running the image resulted 
in import error!
</p>

<p>
Command to build:
</p>

```
F:\flask_restx_demo\>docker build --tag flask-restx-demo .
```

<p>
Command to run:
</p>

```
F:\flask_restx_demo>docker run --publish 8000:8000 --rm flask-restx-demo
```

<p>
<span class="keyword">
<span style="color:red;font-weight:bold;">ImportError: cannot import name 'parse_rule' from 
'werkzeug.routing' (/usr/local/lib/python3.10/site-packages/werkzeug/routing/__init__.py)</span></span>.
</p>

<p>
Please see the screen capture below for the full log:
</p>

![031-01-restx-demo-run-image-failed.png](https://behainguyen.files.wordpress.com/2022/07/031-01-restx-demo-run-image-failed.png)

<p>
Following the error, I was able to figure out what the problem was.
Inside the 
<span class="keyword">
Docker image</span>, the version of the 
<span class="keyword">
Werkzeug</span> <strong>was</strong>
<span class="keyword">
<strong>2.2.0</strong></span>, while in the development environment, 
it <strong>is</strong> 
<span class="keyword">
<strong>2.1.2</strong></span>. I describe how I did this in the later 
section 
<a href="#look-inside-Docker-image">How to look inside a Docker image</a>.
</p>

<p>
The 
<span class="keyword">
Werkzeug</span> package, in my understanding, is a dependency package. 
It gets installed automatically when required by the packages that we 
specify. We don't usually have to explicitly specify the 
<span class="keyword">
Werkzeug</span> package as a required package.
</p>

<p>
Between those nearly four ( 4 ) days, the only significant change was in 
<span class="keyword">
Python</span> codes, where I enable cross-origin
<span class="keyword">
AJAX</span> with package 
<span class="keyword">
Flask-Cors</span>. In my understanding, this package should not cause 
a different version of the 
<span class="keyword">
Werkzeug</span> package to be installed?
</p>

<p>
I should also mention that on my 
<span class="keyword">
Windows 10 Pro</span> the 
<span class="keyword">
Python</span> version is 
<span class="keyword">
3.10.1</span>; while for image build, it is
<span class="keyword">
3.10.5</span>: 
<span class="keyword">
FROM python:3.10.5-slim-buster</span>. 
</p>

<p>
-- But this configuration has not been changed between those nearly 
four ( 4 ) days.
</p>

<p>
Google searches would show that others had problems with 
<span class="keyword">
Werkzeug</span> dependency versions too, and they have to explicitly
force the correct version in their required packages list. So I thought
if I force the development environment to explicitly install version 
<span class="keyword">
2.2.0</span>, then it will fail with the import error like the 
<span class="keyword">
Docker image</span> does.
</p>

<p>
I updated 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
setup.py</span>'s
<span class="keyword">
install_requires</span> section to include as its last entry 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
'werkzeug==2.2.0'</span>:
</p>

```python
    install_requires=[
        'Flask',
        'python-dotenv',
        'Flask-RESTX',
        'Flask-SQLAlchemy',
        'Flask-Cors',		
        'werkzeug==2.2.0',
    ],
```

<p>
Re-run editable install:
</p>

```
(venv) F:\flask_restx_demo>pip3 install -e .
```

<p>
Then run the project:
</p>

```
(venv) F:\flask_restx_demo>venv\Scripts\flask.exe run
```

<p>
I did get the expected error. Please see the screen capture below:
</p>

![031-02-restx-demo-flask-run-failed.png](https://behainguyen.files.wordpress.com/2022/07/031-02-restx-demo-flask-run-failed.png)

<p>
<span class="keyword">
<span style="color:red;font-weight:bold;">
ImportError: cannot import name 'parse_rule' from 'werkzeug.routing' (F:\flask_restx_demo\venv\lib\site-packages\werkzeug\routing\__init__.py)
</span></span>.
</p>

<p>
Based on this, I expected that if I change 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
Werkzeug</span> to version 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
2.1.2</span> then the 
<span class="keyword">
Docker image</span> should work. The development environment already works 
as we've seen before.
</p>

<p>
<a href="https://github.com/behai-nguyen/flask-restx-demo/blob/main/setup.py"
title="setup.py"target="_blank">setup.py</a>'s
<span class="keyword">
install_requires</span> is now:
</p>

```python
    install_requires=[
        ...
        'werkzeug==2.1.2',
    ],
```

<p>
❶ Re-install required packages in editable mode, the project 
run with the
<span class="keyword">
Flask development server</span> as before. ❷ Re-build and re-run 
<span class="keyword">
Docker image</span> -- it works.
</p>

<p>
Please note, if run with:
</p>

```
F:\flask_restx_demo>docker run --publish 8000:8000 --rm flask-restx-demo
```

<p>
Then the URLs to container are:
</p>

```
http://0.0.0.0:8000/api/v1/ui -- Swagger UI URL
http://0.0.0.0:8000/api/v1/trees -- API URL
```

<p>
The latest code for this post can be cloned with:
</p>

```
git clone -b v1.0.2 https://github.com/behai-nguyen/flask-restx-demo.git
```

<p>
<strong>Please note</strong>, I have now included two ( 2 ) test clients  
under 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
test_client_app\</span>. ⓵ 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
test_client_app\delphi</span> is a simple 
<span class="keyword">
Delphi 10.4 Community</span> project, you will have to compile it yourself. ⓶ 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
test_client_app\jquery-ajax\TreeAPIClient.html</span> is a 
<span class="keyword">
JQuery</span> page, just copy it to a web site or a virtual web 
directory, and run it from there.
</p>

<!--------------------------------------------------------------------------------->
<h3>
  <a id="look-inside-Docker-image">How to look inside a Docker image</a>
</h3>

<p>
Run the container in the interactive mode with the 
<span class="keyword">
bash</span> process:
</p>

```
F:\flask_restx_demo>docker run -it --rm flask-restx-demo bash
```

<p>
The prompt will change to something like this:
</p>

```
root@64be4aeb190a:/flask_restx_demo#
```

<p>
We would need an editor to look at the files. 
<span class="keyword">
vi</span> is not installed. We can install it, but we need to know 
what kind of 
<span class="keyword">
Linux distro</span> it is, run:
</p>

```
root@64be4aeb190a:/flask_restx_demo# cat /etc/os-release
```

<p>
We get:
</p>

```
PRETTY_NAME="Debian GNU/Linux 10 (buster)"
NAME="Debian GNU/Linux"
VERSION_ID="10"
VERSION="10 (buster)"
VERSION_CODENAME=buster
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"
root@64be4aeb190a:/flask_restx_demo#
```

<p>
I searched for “install vi debian”, and found this 
<a href="https://vitux.com/how-to-install-vim-editor-on-debian/"
title="How to Install vim editor on Debian 11"
target="_blank">How to Install vim editor on Debian 11</a> -- 
basically, run these two ( 2 ) commands:
</p>

```
root@64be4aeb190a:/flask_restx_demo# apt update
root@64be4aeb190a:/flask_restx_demo# apt install vim
```

<p>
Now that we have 
<span class="keyword">
vim</span>, we can look at files now. With 
<span class="keyword">
Werkzeug <strong>2.2.0</strong></span> installed:
</p>

```
root@64be4aeb190a:/flask_restx_demo# vi /usr/local/lib/python3.10/site-packages/werkzeug/routing/__init__.py
```

<p>
There is no 
<span class="keyword">
parse_rule</span> defined!
</p>

```
root@64be4aeb190a:/flask_restx_demo# vi /usr/local/lib/python3.10/site-packages/werkzeug/__init__.py
```

<p>
The last line should tell us the version:
</p>

```python
__version__ = "2.2.0"
```

<p>
When finished:
</p>

```
root@64be4aeb190a:/flask_restx_demo# exit
```

<p>✿✿✿</p>

<p>
Although 
<strong>I still couldn't figure out why the different versions of 
<span class="keyword">
Werkzeug</span> get installed...</strong> I'm happy to have figured 
out that the versions caused the import error. I hope you find this 
post useful, thank you for reading and happy Dockering 🙀!
</p>
