---
layout: post
title: "Python: interactive shell and shell_context_processor() decorator."

---

Python Flask interactive shell enables us to explore our application data. shell_context_processor decorator makes application objects available in the Python Flask interactive shell. In this post, we focus on shell_context_processor decorator and how to use Python Flask interactive shell.

| ![028-feature-image.png](https://behainguyen.files.wordpress.com/2022/07/028-feature-image.png) |
|:--:|
| *Python: interactive shell and shell_context_processor() decorator.* |

<p>
The 
</p>

```
$ flask shell
```

<p>
command starts a <span class="keyword"> Python</span> interactive command prompt where we can explore our application data. To quote from the link <a href="https://flask.palletsprojects.com/en/2.1.x/cli/" title="Command Line Interface" target="_blank">Command Line Interface</a>:
</p>

> To explore the data in your application, you can start an interactive Python shell with the <a href="https://flask.palletsprojects.com/en/2.1.x/api/#flask.cli.shell_command" title="shell" target="_blank">shell</a> command. An application context will be active, and the app instance will be imported.<br/>
> ...<br/>
> Use <a href="https://flask.palletsprojects.com/en/2.1.x/api/#flask.Flask.shell_context_processor" title="shell_context_processor()" target="_blank">shell_context_processor()</a> to add other automatic imports.

<p>
In this short post, we're focusing on the <a href="https://flask.palletsprojects.com/en/2.1.x/api/#flask.Flask.shell_context_processor" title="shell_context_processor()" target="_blank">shell_context_processor()</a> decorator and how it works with the <span class="keyword"> “flash shell”</span> command.
</p>

<p>
The code for this post is built upon the code created for this post <a href="https://behai-nguyen.github.io/2022/07/12/flask-restx-swagger-ui.html" title="Python: Flask-RESTX and the Swagger UI automatic documentation." target="_blank">Python: Flask-RESTX and the Swagger UI automatic documentation.</a> This code can be cloned from <span class="keyword"> GitHub</span> using:
</p>

```
E:\>git clone -b v1.0.0 https://github.com/behai-nguyen/flask-restx-demo.git
```

<p>
To recap, the layout of the project from the above <span class="keyword"> git clone</span> is as below -- ☆ marks the file we're going to update for this post:
</p>

```
f:\flask_restx_demo
|
|-- .env
|-- app.py ☆
|-- setup.py
|
|-- src\
|   |
|   |-- flask_restx_demo\
|       |
|       |-- __init__.py 
|       |-- config.py
|       |
|       |-- api\
|       |   |       
|       |   |-- __init__.py
|       |   |
|       |   |-- trees\
|       |       |
|       |       |-- bro.py
|       |       |-- dto.py
|       |       |-- routes.py 
|       |       |-- __init__.py
|       |
|       |-- models\
|           |       
|           |-- tree.py
|
|-- venv\
```

```
Updated file f:\flask_restx_demo\app.py
```

```python
"""Flask Application entry point."""

from flask_restx_demo import (
    create_app,
    db,
)	

app = create_app()

@app.shell_context_processor
def shell():
    return {
        "db": db,
    }
```

<p>
<span style="color:blue;"> The complete code for this post can be downloaded from <span class="keyword"> GitHub</span> using: </span>
</p>

```
E:\>git clone -b v1.0.1 https://github.com/behai-nguyen/flask-restx-demo.git
```

<p>
Basically, we import the <span class="keyword"> db</span> object, and making it available to the <span class="keyword"> Python</span> interactive shell via the <span class="keyword"> @app.shell_context_processor</span> decorator. We list all objects we want to make available to the shell one after another, separated by comma ( , ). Please note that the method does not have to be:
</p>

```python
def shell():
```

<p>
We could name it whatever we like, for so long it makes sense. What's important is the <span class="keyword"> @app.shell_context_processor</span> decorator.
</p>

<p>
❶ Now we can try opening a <span class="keyword"> Python</span> interactive shell with:
</p>

```
(venv) F:\flask_restx_demo>venv\Scripts\flask.exe shell
```

<p>
We'll get the following:
</p>

```
Python 3.10.1 (tags/v3.10.1:2cd268a, Dec  6 2021, 19:10:37) [MSC v.1929 64 bit (AMD64)] on win32
App: flask-restx-demo [development]
Instance: F:\flask_restx_demo\instance
>>>
```

<p>
❷ Remember an earlier quote from <a href="https://flask.palletsprojects.com/en/2.1.x/cli/" title="Command Line Interface" target="_blank">Command Line Interface</a>?
</p>

> An application context will be active, and the app instance will be imported.

<p>
We'd expect the <span class="keyword"> app</span> object to be available:
</p>

```
>>> print( app )
```

<p>
We should get:
</p>

```
<Flask 'flask-restx-demo'>
>>>
```

<p>
❸ Let's look at the <span class="keyword"> db</span> object:
</p>

```
>>> print( db )
```

<p>
This is the output on my configuration:
</p>

```
<SQLAlchemy engine=sqlite:///F:\flask_restx_demo\flask_restx_demo.db>
>>>
```

<p>
❹ Similar to other <span class="keyword"> Python</span> interactive shells, we can also use the <span class="keyword"> db</span> object in an interactive manner:
</p>

```
>>> conn = db.engine.connect()
>>> res = conn.execute( 'select * from tree' )
>>> for r in res:
...    print( r )
... press Enter key
```

<p>
It'll print out the... entire <span class="keyword"> tree</span> table:
</p>

```
(1, 'Acer palmatum', 'Japanese maple', 'https://en.wikipedia.org/wiki/Acer_palmatum')
(2, 'Liquidambar', 'Sweetgums', 'https://en.wikipedia.org/wiki/Liquidambar')
(3, 'Lagerstroemia', 'Crepe myrtle', 'https://en.wikipedia.org/wiki/Lagerstroemia')
(4, 'Pinus Thunbergii', 'Black Pine', 'https://en.wikipedia.org/wiki/Pinus_thunbergii')
(5, 'Pinus parviflora', 'Japanese White Pine', 'https://en.wikipedia.org/wiki/Pinus_parviflora')
>>>
```


<p>
❺ I did run the same application on my  <span class="keyword"> Synology DS218</span> box. It's not different to the <span class="keyword"> Windows 10 Pro</span> environment:
</p>

```
(venv) behai@omphalos-nas-01:/var/services/web/flask_restx_demo$ sudo venv/bin/flask shell
```

```
Python 3.9.6 (default, Jan  5 2022, 15:50:31)
[GCC 8.5.0] on linux
App: flask-restx-demo [development]
Instance: /volume1/web/flask_restx_demo/instance
```

<p>
Then:
</p>

```
>>> conn = db.engine.connect()
>>> res = conn.execute( 'select * from tree' )
>>> for r in res:
...     print( r )
... press Enter key
```

<p>
I've only one record in the <span class="keyword"> tree</span> table on this environment:
</p>

```
(1, 'Acer Buergerianum', 'Trident Maple', 'https://en.wikipedia.org/wiki/Acer_buergerianum')
>>>
```

<p>
❻ To exit the interactive shell:
</p>

```
>>> exit()
```

<p>
We'll be returned to the <span class="keyword"> Python virtualenv</span> prompt.
</p>

<p>
<span style="color:blue;"> The complete code for this post can be downloaded from <span class="keyword"> GitHub</span> using: </span>
</p>

```
E:\>git clone -b v1.0.1 https://github.com/behai-nguyen/flask-restx-demo.git
```

<p>
For such small addition, we've such rich functionalities... I find this feature very enticing. I hope you find this post helpful in some manner. And thank you for reading.
</p>

