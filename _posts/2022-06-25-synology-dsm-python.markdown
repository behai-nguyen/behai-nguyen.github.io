---
layout: post
title: "Synology DS218: preparing Python 3.9 Beta compelete devepment environment."

---

We discuss how to set up a Python 3.9 Beta development environment on 
Synology DS218 DiskStation running DSM version 7.1-42661 Update 1. The 
development environment includes: pip, virtualenv, setuptools, wheel 
and the flask development web server.

| ![025-feature-image.jpg](https://behainguyen.files.wordpress.com/2022/06/025-feature-image.jpg) |
|:--:|
| *Synology DS218: preparing Python 3.9 Beta compelete devepment environment.* |

<p>
<a href="https://www.synology.com/en-au/products/DS218"
title="Synology DS218 DiskStation"
target="_blank">Synology DS218 DiskStation -- Versatile 2-bay NAS for small offices and home users</a>
is a <span class="keyword">
Linux</span> device. It runs a
<span class="keyword">
Linux distro</span> named
<span class="keyword">
DSM</span>, and the version on my device is
<span class="keyword">
7.1-42661 Update 1</span>.
</p>

<p>
There're so many different
<span class="keyword">
Linux</span> flavours. During my research on this topic, I realised
I'll have some difficulties. And I did. I have not found a complete
guide on how to do this, the steps that work for me, which I've put
together in this post come from several other existing posts, I'm
listing those referenced posts along the way.
</p>

<p>
I'd like to mention that, following the instructions in this post
<a href="https://linuxhint.com/use-synology-web-station/"
title="How Do I use Synology Web Station?"
target="_blank">How Do I use Synology Web Station?</a>, I've
successfully got a
<span class="keyword">
PHP port-based</span> virtual site hosted by
<span class="keyword">
Apache 2.4</span> to run in under 30 ( thirty ) minutes -- and I can
access it from my
<span class="keyword">
Windows 10</span> machine.
<span class="keyword">
Python</span>, somehow is not that straightforward.
</p>

<!--------------------------------------------------------------------------------->

<h2>Table of contents</h2>

<ul>
	<li><a href="#nas-ip-address">Determining Synology NAS' IP address</a></li>

	<li><a href="#home-service">Enable home service</a></li>

	<li><a href="#enable-ssh">Enable SSH</a></li>

	<li><a href="#using-ssh">SSH to DSM from Windows 10</a></li>

	<li><a href="#pre-installed-python">Existing Python installation</a></li>
	
	<li><a href="#install-webstation-python39-beta">Install Web Station and Python 3.9 Beta</a>
		<ul>
			<li><a href="#install-webstation">Install Web Station</a></li>

			<li><a href="#install-python39-beta">Install Python 3.9 Beta</a></li>
		</ul>
	</li>

	<li><a href="#python-39-beta-location-invoke">Where is Python 3.9 Beta installed, how do I invoke it?</a></li>

	<li><a href="#install-upgrade-verify-pip">Install pip, upgrade pip, and verify pip has been installed</a>
		<ul>
			<li><a href="#install-pip">Install pip</a></li>

			<li><a href="#upgrade-pip">Upgrade pip</a></li>
			
			<li><a href="#verify-pip">Verify pip has been installed</a></li>			
		</ul>
	</li>

	<li><a href="#checking-pip-version">Checking pip version</a></li>

	<li><a href="#update-setuptools-wheel">Update setuptools and wheel packages</a></li>

	<li><a href="#install-virtualenv-verify-installation">Install virtualenv and verify installation</a>
		<ul>
			<li><a href="#install-virtualenv">Install virtualenv</a></li>

			<li><a href="#verify-virtualenv-installed">Verify virtualenv has been installed</a></li>
		</ul>
	</li>
	
	<li><a href="#create-virtualenv-venv">Create virtual environment venv</a></li>	

	<li><a href="#activate-deactivate-venv">Activate and Deactivate the virtual environment venv</a>
		<ul>
			<li><a href="#activate-venv">Activate the virtual environment venv</a></li>

			<li><a href="#deactivate-venv">Deactivate the virtual environment venv</a></li>
		</ul>
	</li>

	<li><a href="#the-test-app">The test app</a>
		<ul>
			<li><a href="#test-app-install-required-packages">Install required packages</a></li>

			<li><a href="#complete-the-test-app">Complete the test application</a></li>

			<li><a href="#run-the-test-app">Run the test application</a></li>
		</ul>
	</li>

	<li><a href="#concluding-remarks">Concluding remarks</a></li>

</ul>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="nas-ip-address">Determining Synology NAS' IP address</a>
</h3>

<p>
Go to <span style="font-weight:bold;">Control Panel > Network > Network Interface tab:</span>
look under <span style="font-weight:bold;">LAN</span>.
</p>

<p>
Mine's <span style="font-weight:bold;">192.168.0.6</span> -- and I'll
reference this throughout this post.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="home-service">Enable home service</a>
</h3>

<p>
Home service means the user home directory.
</p>

<p>
<span class="keyword">
“behai”</span> is the user I set up when first installed
<span class="keyword">
DSM</span>. This is not the root user.
</p>

<p>
Go to <span style="font-weight:bold;">Control Panel > User & Group > select behai > Advanced tab</span>:
</p>

<p>
Check <span style="font-weight:bold;">“Enable user home service”</span>, then click
<span style="font-weight:bold;">“Apply”</span>.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="enable-ssh">Enable SSH</a>
</h3>

<p>
Go to <span style="font-weight:bold;">Control Panel > Terminal & SNMP > Terminal tab</span>:
</p>

<p>
Check <span style="font-weight:bold;">“Enable SSH service”</span>, then click
<span style="font-weight:bold;">“Apply”</span>.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="using-ssh">SSH to DSM from Windows 10</a>
</h3>

<p>
From a 
<span class="keyword">
Windows command prompt</span>, we should now be able to access
<span class="keyword">
DSM</span> command line via
<span class="keyword">
SSH, using:</span>
</p>

```
ssh behai@192.168.0.6
```

<p>
It'll ask for the password, this's the same password we use to log into the device.
</p>

<p>
After logging into
<span class="keyword">
SSH</span> terminal, both commands:
</p>

```
$ echo $HOME
$ pwd
```

<p>
will return the same value, which is the home directory, mine is:
</p>

```
/var/services/homes/behai
```

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="pre-installed-python">Existing Python installation</a>
</h3>

From
<span class="keyword">
Package Center</span> under
<span class="keyword">
Installed</span>, it shows
<span class="keyword">
Python2</span> comes pre-installed ( when we first installed
<span class="keyword">
DSM</span> ).

<p>
But both:
</p>

```
$ python
$ python3
```

<p>
show
<span class="keyword">
Python 3.8.12</span>, please see the screen capture below:
</p>

![025-01.png](https://behainguyen.files.wordpress.com/2022/06/025-01.png)

<!--------------------------------------------------------------------------------->
<h3 style="clear:both;color:teal;">
  <a id="install-webstation-python39-beta">Install Web Station and Python 3.9 Beta</a>
</h3>

<p>
I thought I would need
<span class="keyword">
Web Station</span>, in hindsight, however,
at this stage, I don't think I need
<span class="keyword">
Web Station</span> yet, but I did install it. So I will just go ahead
and include this step in this post.
</p>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="install-webstation">Install Web Station</a>
</h4>

<p>
To start off, I follow the instructions in
<a href="https://linuxhint.com/use-synology-web-station/"
title="How Do I use Synology Web Station?"
target="_blank">How Do I use Synology Web Station?</a>
to install <span class="keyword">
Web Station</span>,
<span class="keyword">
PHP 8.0</span>, set up a
<span class="keyword">
PHP port-based</span> virtual site hosted by
<span class="keyword">
Apache 2.4</span>, and I was able to get this virtual site to run in
under 30 ( thirty ) minutes -- and I can access it from my
<span class="keyword">
Windows 10</span> machine.
</p>

<p>
Basically, use
<span class="keyword">
Package Center</span> to install
<span class="keyword">
Web Station</span>. The installation will create a web root directory:
</p>

```
/volume1/web/
```

<p>
<span class="keyword">
File Station</span> also sees this directory.
</p>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="install-python39-beta">Install Python 3.9 Beta</a>
</h4>

<p>
At this point, I thought, similar to
<span class="keyword">
PHP</span>, I would need to carry out
the same process for
<span class="keyword">
Python</span>:
</p>

<p>
Go to <span style="font-weight:bold;">Main Menu > Web Station > Script Language Settings > Python tab</span> --
please see screen capture below:
</p>

![025-02.png](https://behainguyen.files.wordpress.com/2022/06/025-02.png)

<p style="clear:both;">
<span class="keyword">
Python 3.8.12</span> has been installed, but it still said no
<span class="keyword">
Python 3</span> package. Use 
<span class="keyword">
Package Center</span> to install 
<span class="keyword">
Python 3.9 Beta</span>. Click on
<span class="keyword">
<strong>“Join Beta”</strong></span> to install. 
See screen capture below:
</p>

![25-03.png](https://behainguyen.files.wordpress.com/2022/06/25-03.png)

<p style="clear:both;">
After this a 
<span class="keyword">
User-defined customised profile</span> for  
<span class="keyword">
Python 3.9</span> should appear under 
<span class="keyword">
Web Station</span>'s 
<span class="keyword">
Script Language Settings</span>.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="python-39-beta-location-invoke">Where is Python 3.9 Beta installed, how do I invoke it?</a>
</h3>

<p>
This post 
<a href="https://community.synology.com/enu/forum/10/post/138379"
title="Re-Install pip and virtualenv Site Packages After Package Center Python 3.8.2 Upgrade "
target="_blank">Re-Install pip and virtualenv Site Packages After Package Center Python 3.8.2 Upgrade</a>,
is a bit outdated ( I think ), but it helps me to figure out where 
<span class="keyword">
Python 3.9</span> is installed:
</p>

```
/volume1/\@appstore/Python3.9/usr/bin/python3.9
```

<p>
In fact:
</p>   
   
```
/volume1/\@appstore/Python3.9/usr/bin/ 
```

<p>
is where 
<span class="keyword">
Python 3.9</span> related tools live. This path is recognised by the 
system. Command:
</p>
   
```
$ python3.9
```
   
<p>should just run.</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="install-upgrade-verify-pip">Install pip, upgrade pip, and verify pip has been installed</a>
</h3>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="install-pip">Install pip</a>
</h4>

<p>   
I tried various instructions, they did not work. This 
<a href="https://jackgruber.github.io/2021-06-27-install-pip-on-synology/"
title="Install pip on Synology"
target="_blank">https://jackgruber.github.io/2021-06-27-install-pip-on-synology/</a>
post works. I changed to 
<span class="keyword">
python3.9</span>:
</p>
   
```
$ sudo python3.9 -m ensurepip
```

<p>
   Please see the following screen capture:
</p>

![025-05-installing-pip.png](https://behainguyen.files.wordpress.com/2022/06/025-05-installing-pip.png)
   
<p style="clear:both;">   
   Regarding the warning:
</p>   

<p style="color:red;">
<span class="keyword">
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting 
behaviour with the system package manager. It is recommended to use a virtual environment 
instead: https://pip.pypa.io/warnings/venv
</span>
</p>

<p>   
I don't know what it means yet. As for the warning:
</p>   
   
<p style="color:red;">
<span class="keyword">
WARNING: The scripts pip3 and pip3.9 are installed in 
'/var/packages/Python3.9/target/usr/bin' which is not on PATH.<br/>
Consider adding this directory to PATH or, if you prefer to suppress 
this warning, use --no-warn-script-location.   
</span>
</p>

<p>
I've not taken any action yet... I'll be using the full path initially.
</p>
   
<!--------------------------------------------------------------------------------->   
<h4 style="color:teal;">
  <a id="upgrade-pip">Upgrade pip</a>
</h4>   

<p>
To upgrade pip, I ran the following command:
</p>

```
$ sudo python3.9 -m pip install --upgrade pip
```
   
<p>
I'm also just sleeping on the warnings for the time being, till 
something stops working.
</p>

<!--------------------------------------------------------------------------------->   
<h4 style="color:teal;">
  <a id="verify-pip">Verify pip has been installed</a>
</h4>

<p>   
Using this already mentioned post 
<a href="https://community.synology.com/enu/forum/10/post/138379"
title="Re-Install pip and virtualenv Site Packages After Package Center Python 3.8.2 Upgrade"
target="_blank">Re-Install pip and virtualenv Site Packages After Package Center Python 3.8.2 Upgrade</a>,
the following command verifies that 
<span class="keyword">
pip</span> directory exists:
</p>
   
```
$ ls -l /volume1/\@appstore/Python3.9/usr/lib/python3.9/site-packages
```

<p>
<span class="keyword">
pip</span>, 
<span class="keyword">
pip3</span>, 
<span class="keyword">
pip3.9</span> and 
<span class="keyword">
pip3.10</span> also exist in:
</p>

```
$ ls -l /volume1/\@appstore/Python3.9/usr/bin
```

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="checking-pip-version">Checking pip version</a>
</h3>

<p>
<span style="color:red;">I HAVE TRIED VARIOUS COMMANDS, but none has 
worked. I don't know how to do this presently</span>. I'll post an 
update after I have figured it out.   
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="update-setuptools-wheel">Update setuptools and wheel packages</a>
</h3>

<p>
Run this command:
</p>

```
$ sudo python3.9 -m pip install --upgrade pip setuptools wheel
```
    
<p>
I included 
<span class="keyword">
pip</span>, which was unnecessary as it has already been done.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="install-virtualenv-verify-installation">Install virtualenv and verify installation</a>
</h3>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="install-virtualenv">Install virtualenv</a>
</h4>

<p>
Run this command:
</p>
    
```
$ sudo /volume1/\@appstore/Python3.9/usr/bin/python3.9 -m pip install virtualenv
```

<p>
I included the full path for 
<span class="keyword">
python3.9</span>, which I don't think is necessary.
</p>
	
<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="verify-virtualenv-installed">Verify virtualenv has been installed</a>
</h4>	

<p>
To verify, run this command:
</p>

```
$ ls /volume1/\@appstore/Python3.9/usr/lib/python3.9/site-packages
```

<p>
See the screen capture below, 
<span class="keyword">
virtualenv</span> has been installed:
</p>

![025-07-installing-virtualenv-a.png](https://behainguyen.files.wordpress.com/2022/06/025-07-installing-virtualenv-a.png)

<p style="clear:both;">
The 
<span class="keyword">
bin</span> directory is where related executables live:
</p>

```
$ ls -l /volume1/\@appstore/Python3.9/usr/bin/
```
	
<p>
Please see the output in the screen capture below:
</p>
	
![025-07-installing-virtualenv-b.png](https://behainguyen.files.wordpress.com/2022/06/025-07-installing-virtualenv-b.png)

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="create-virtualenv-venv">Create virtual environment venv</a>
</h3>

<p>
Under  
<span class="keyword">
$HOME</span>, i.e. 
<span class="keyword">
/var/services/homes/behai/</span> 
directory, create directory 
<span class="keyword">
app_demo</span> with command:
</p>	

```
$ mkdir app_demo
```
	
<p>	
Then go to this directory:
</p>

```
$ cd app_demo
```

<p>	
Issue the below command to create virtual environment 
<span class="keyword">
venv</span>:
</p>

```
$ sudo /volume1/\@appstore/Python3.9/usr/bin/virtualenv -p python3.9 venv
```

<p>	
Verify venv created:
</p>
    
```
$ ls -l venv/
```

<p>	
Check 
<span class="keyword">
venv/bin</span> directory:
</p>	
    
```
$ ls -l venv/bin/
```

<p>	
-- We can also see the content of these directories using 
<span class="keyword">
File Station</span>.
</p>

<p>	
The running of these commands is shown in the screen capture below:
</p>

![025-08-creating-virtual-environment-venv.png](https://behainguyen.files.wordpress.com/2022/06/025-08-creating-virtual-environment-venv.png)

<p style="clear:both;">	
Please note, in 
<span class="keyword">
Windows</span>, 
<span class="keyword">
venv\Scripts\</span> is the equivalence of 
<span class="keyword">
venv/bin</span>.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="activate-deactivate-venv">Activate and Deactivate the virtual environment venv</a>
</h3>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="activate-venv">Activate the virtual environment venv</a>
</h4>

<p>
To activate, run:
</p>

```
$ source venv/bin/activate
```

<p>	
The prompt changes as seen in the screen capture below:
</p>

![025-09-activate-virtual-environment-venv.png](https://behainguyen.files.wordpress.com/2022/06/025-09-activate-virtual-environment-venv.png)

<!--------------------------------------------------------------------------------->
<h4 style="clear:both;color:teal;">
  <a id="deactivate-venv">Deactivate the virtual environment venv</a>
</h4>
	
<p>
<span style="color:red;">
I DON'T KNOW HOW TO DEACTIVATE IT YET. I'm not sure what 
<span class="keyword">
venv/bin/deactivate.nu</span> is for. I can't find info on it either
</span>. I just terminate the 
<span class="keyword">
SSH</span> session, get back in, and it still works.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="the-test-app">The test app</a>
</h3>

<p>
This part is similar to 
<a href="https://behainguyen.wordpress.com/2022/06/16/python-application-self-installation-built-distribution-and-test-the-built-distribution/"
title="Python: Application ( Self ) Installation, Built Distribution and Test the Built Distribution."
target="_blank">Python: Application ( Self ) Installation, Built Distribution and Test the Built Distribution.
</a>, which I have written for 
<span class="keyword">
Windows 10</span>.
</p>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="test-app-install-required-packages">Install required packages</a>
</h4>

<p>
Under 
<span class="keyword">
/var/services/homes/behai/app_demo</span>, create 
<span class="keyword">
setup.py</span> file and 
<span class="keyword">
src/</span> directory.
</p>

```
/var/services/homes/behai/app_demo
|
|-- setup.py
|
|-- src/
```

```
File /var/services/homes/behai/app_demo/setup.py
```

```python
"""Installation script for flask_restx demo project."""
from pathlib import Path
from setuptools import setup, find_packages

setup(
    name='dsm-python-demo',
    description='flask dev server on Synology DSM demo.',
    version='1.0.0',
    author='Van Be Hai Nguyen',
    author_email='behai_nguyen@hotmail.com',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires='>=3.9',
    install_requires=[
        'Flask',
        'python-dotenv',
    ],
)
```

<p>
Run the command below to install packages for the test 
application that we are going to write:
</p>

```
$ sudo venv/bin/pip install -e .
```

<p>
This should run with no problems. After finished, use 
<span class="keyword">
File Station</span> to scan through the directories to verify that 
we have the specified packages installed.
</p>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="complete-the-test-app">Complete the test application</a>
</h4>

<p>
Now create the rest of the application:
</p>

```
/var/services/homes/behai/app_demo/
|
|-- .env
|-- app.py
|-- setup.py
|
|-- src/
|   |
|   |-- app_demo/
|       |   
|       |-- __init__.py
|       |-- config.py
|
|-- venv/
```

```
File /var/services/homes/behai/app_demo/.env
```

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=">s3g;?uV^K=`!(3.#ms_cdfy<c4ty%"
```

```
File /var/services/homes/behai/app_demo/app.py
```

```python
"""Flask Application entry point."""

from app_demo import create_app

app = create_app()
```

```
File /var/services/homes/behai/app_demo/src/app_demo/__init__.py
```

```python
"""Flask app initialization via factory pattern."""
from flask import Flask

from app_demo.config import get_config

def create_app():
    app = Flask( 'dsm-python-demo' )

    app.config.from_object( get_config() )

    @app.route( '/' )
    def hello_world():
        return '<p>Hello, World!</p>'

    return app
```

```
File /var/services/homes/behai/app_demo/src/app_demo/config.py
```

```python
"""Flask app config settings."""
import os

class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = os.getenv( 'SECRET_KEY' )
    FLASK_APP = os.getenv( 'FLASK_APP' )
    FLASK_ENV = os.getenv( 'FLASK_ENV' )

def get_config():
    """Retrieve environment configuration settings."""
    return Config
```

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="run-the-test-app">Run the test application</a>
</h4>

<p>
Run it with:
</p>

```
$ sudo venv/bin/flask run --host=0.0.0.0 --port=9090
```

![025-10-run-test-app-a.png](https://behainguyen.files.wordpress.com/2022/06/025-10-run-test-app-a.png)

<p style="clear:both;">
From 
<span class="keyword">
Windows</span>, open this URL 
<span class="keyword">
http://192.168.0.6:9090/</span>:
</p>

<p>
The application responds as expected:
</p>

![025-10-run-test-app-b.png](https://behainguyen.files.wordpress.com/2022/06/025-10-run-test-app-b.png)

<p style="clear:both;">
Recall that 
<span class="keyword">
192.168.0.6</span> is my Synology NAS address.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="concluding-remarks">Concluding remarks</a>
</h3>

<p>
This's been an interesting exercise. I've learned a lot along the way.
What I really want to achieve is to get the
<span class="keyword">
DSM Apache 2.4</span> web server to host
<span class="keyword">
Python</span> web applications in a similar manner as
<span class="keyword">
Internet Information Services (IIS)</span> -- which I've done and described in
<a href="https://behainguyen.wordpress.com/2022/02/22/python-hosting-a-virtualenv-flask-application-in-windows-10-pros-internet-information-services-iis/"
title="Python: hosting a virtualenv Flask application in Windows 10 Pro's Internet Information Services (IIS)."
target="_blank">Python: hosting a virtualenv Flask application in Windows 10 Pro's Internet Information Services (IIS)</a>.
 I'll continue to work towards this objective, I'll do another post after I've learned how to do it, and do it successfully.
</p>

<p>
Thank you for reading, and I hope you find this post useful.
</p>
