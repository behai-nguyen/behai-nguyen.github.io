---
layout: post
title: "Python: Application ( Self ) Installation, Built Distribution and Test the Built Distribution."

---

In this post, we discuss how to make an application self-installable 
in editable or development mode; and then prepare it for distribution. 
Finally, test the distribution in another virtual environment.

| ![023-feature-image.png](https://behainguyen.files.wordpress.com/2022/06/023-feature-image.png) |
|:--:|
| *Python: Application ( Self ) Installation, Built Distribution and Test the Built Distribution.* |

For a 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
Python</span> application, 
we can install required packages individually or via the
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
requirements.txt</span> text file. We can also use the
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
setuptools</span> package to make applications install packages in 
editable or development mode; and later use 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
wheel</span> to prepare the application built distribution.

In this post, we demonstrate how to do this with a simple
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
Flask</span> web application that has only a single route
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
/hello</span>. We will then install the application built distribution
onto another virtual environment and run the application with
<a href="https://docs.pylonsproject.org/projects/waitress/en/latest/" 
title="Waitress web server" 
target="_blank">Waitress web server -- https://docs.pylonsproject.org/projects/waitress/en/latest/</a>.

<h3><a id="environments">Environments</a></h3>

<ol>
<li style="margin-top:10px;">
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
Python 3.10.1</span>.
</li>
</ol>

<h3><a id="app-structure">Application Directories and Files</a></h3>

These are the directories and files that we will create manually:

```
F:\self_install\
|
|-- .env
|-- app.py
|-- setup.py
|
|-- src\
|   |
|   |-- self_install\
|       |   
|       |-- __init__.py
|       |-- config.py
```

Please note, this is my environment only, you can name it whatever 
you like and where ever suit you most.

<h3><a id="app-create">Create The Application</a></h3>

<h4>Setting up the virtual environment</h4>

Change directory to 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
F:\self_install\</span>, and run the following three ( 3 ) commands 
to set up the virtual environment:

```
C:\PF\Python310\python.exe -m pip install --upgrade pip

C:\PF\Python310\python.exe -m pip install --user virtualenv 

C:\Users\behai\AppData\Roaming\Python\Python310\Scripts\virtualenv.exe venv
```

Then activate the virtual environment:

```
.\venv\Scripts\activate.bat
```

For creating virtual environment, please see 
<a href="https://behainguyen.wordpress.com/2022/02/15/python-virtual-environment-virtualenv-for-multiple-python-versions/" 
title="Python: Virtual Environment virtualenv for multiple Python versions." 
target="_blank">Python: Virtual Environment virtualenv for multiple Python versions.</a>

The screen should now look similar to the image below:

![023-01.png](https://behainguyen.files.wordpress.com/2022/06/023-01.png)

<h4>setuptools and wheel</h4>

After activating
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
venv</span>, install and upgrade 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
setuptools</span> and 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
wheel</span>, run the following command:

```
.\venv\Scripts\pip.exe install --upgrade setuptools wheel
```

The output should look similar to the image below:

![023-02.png](https://behainguyen.files.wordpress.com/2022/06/023-02.png)

We should take a glance inside     
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
F:\self_install\venv\Lib\site-packages\</span>,
and make mental notes of what are in there.

<h4>F:\self_install\setup.py</h4>

Below are the relevant documentations:

<ul>
<li style="margin-top:10px;">
<a href="https://setuptools.pypa.io/en/latest/references/keywords.html" 
title="Setuptools Keywords" 
target="_blank">Setuptools Keywords -- https://setuptools.pypa.io/en/latest/references/keywords.html</a>
</li>

<li style="margin-top:10px;">
<a href="https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#using-find-or-find-packages" 
title="Package Discovery and Namespace Packages" 
target="_blank">
Package Discovery and Namespace Packages -- https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#using-find-or-find-packages
</a>
</li>
</ul>

The file
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
setup.py</span> is used to install the application, and via 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
wheel</span> prepare the built distribution.

```
File F:\self_install\setup.py:
```

{% highlight python %}
"""Installation script for self_install demo project."""
from pathlib import Path
from setuptools import setup, find_packages

setup(
    name='self-install',
    description='Demonstrate project self installation through pip.',
    version='1.0.0',
    author='Van Be Hai Nguyen',
    author_email='behai_nguyen@hotmail.com',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires='>=3.10',
    install_requires=[
        'Flask',
        'python-dotenv',
    ],
)
{% endhighlight %}

<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
python-dotenv</span> is required to read 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
.env</span> enviroment file. <span style="color:blue;">
A further note, this setup requires sub-directory 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
src\</span> exists under
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
F:\self_install\</span> before we can run the installation.
</span>

<h4>Install the Application</h4>

To install the application in editable mode, run the below command:

```
.\venv\Scripts\pip.exe install -e .
```

The output should look similar to the image below:

![023-03.png](https://behainguyen.files.wordpress.com/2022/06/023-03.png)

Please take a look in:

<ul>
<li style="margin-top:10px;">
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
F:\self_install\venv\Lib\site-packages\</span>
</li>

<li style="margin-top:10px;">
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
F:\self_install\src\self_install.egg-info\</span>
</li>
</ul>

<h4>Create And Run The Application</h4>

We are now ready to create the application. It is so simple, so I will 
just list the content of the files one after another, and will not discuss 
the content.

```
File F:\self_install\.env:
```

{% highlight python %}
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=">s3g;?uV^K=`!(3.#ms_cdfy<c4ty%"
{% endhighlight %}

```
File F:\self_install\src\self_install\__init__.py:
```

{% highlight python %}
"""Flask app initialization via factory pattern."""
from flask import Flask

from self_install.config import get_config

def create_app():
    app = Flask( 'self_install' )

    app.config.from_object( get_config() )

    # A simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
{% endhighlight %}

```
File F:\self_install\src\self_install\config.py:
```

{% highlight python %}
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
{% endhighlight %}


```
File F:\self_install\app.py:
```

{% highlight python %}
"""Flask Application entry point."""

from self_install import create_app

app = create_app()
{% endhighlight %}

If everything is working correctly, we should be able to 
query the application routes with the following command:

```
.\venv\Scripts\flask.exe routes
```

The output should look similar to the image below:

![023-04.png](https://behainguyen.files.wordpress.com/2022/06/023-04.png)

We can now run the application with:

```
.\venv\Scripts\flask.exe run
```

Paste the following 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
http://127.0.0.1:5000/hello</span> into a browser, and we should 
get <span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
Hello, World!</span> response. The application is now complete.
We can now prepare the built distribution.

<h4>Prepare and Test the Built Distribution</h4>

The following command will do the built distribution:

```
.\venv\Scripts\python.exe setup.py bdist_wheel
```

The output should look similar to the image below:

<!-- WordPress gallery, align right -->
![023-05.png](https://behainguyen.files.wordpress.com/2022/06/023-05.png)

Please note the following two directories created by the 
above command:

<ul>
<li style="margin-top:10px;">
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
F:\self_install\build\</span>
</li>

<li style="margin-top:10px;">
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
F:\self_install\dist\</span>
</li>
</ul>

The output file is 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
F:\self_install\dist\self_install-1.0.0-py3-none-any.whl</span>. The 
components of this file name are:

```
{project name}-{version}-{python tag}-{abi tag}-{platform tag}
```
		
Please see 
<a href="https://peps.python.org/pep-0427/#file-format" 
title="PEP 427 – The Wheel Binary Package Format 1.0" 
target="_blank">
PEP 427 – The Wheel Binary Package Format 1.0 -- https://peps.python.org/pep-0427/#file-format</a>

This file can be copied to another machine, another 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
virtualenv</span>, then install with
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
pip</span>. For this post, I am creating another virtual environment 
under <span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
D:\test\</span>, copy 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
self_install-1.0.0-py3-none-any.whl</span> to 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
D:\test\</span>, and run the below command:

```
.\venv\Scripts\pip.exe install self_install-1.0.0-py3-none-any.whl
```

If everything goes well, the output should look like the image below:

![023-01.png](https://behainguyen.files.wordpress.com/2022/06/023-06.png)

Next, we install the 
<a href="https://docs.pylonsproject.org/projects/waitress/en/latest/" 
title="Waitress web server" 
target="_blank">Waitress web server -- https://docs.pylonsproject.org/projects/waitress/en/latest/</a> with:

```
.\venv\Scripts\pip.exe install waitress
```

Then we can launch the application with:

```
.\venv\Scripts\waitress-serve.exe --call self_install:create_app
```

The output of those two commands above shown below:

![023-07.png](https://behainguyen.files.wordpress.com/2022/06/023-07.png)

Despite 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
http://0.0.0.0</span> stated by
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
waitress-serve.exe</span>, the correct address is 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
localhost</span> -- copy and paste 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
http://localhost:8080/hello </span> into a browser address, we should
get <span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
Hello, World!</span> response as before.

This concludes this post... I had fun writing this. For me, I found it 
useful. I hope you get something out of this post, and thank you for reading.