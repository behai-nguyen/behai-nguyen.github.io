---
layout: post
title: "Python: Flask-RESTX and the Swagger UI automatic documentation."

---

Flask-RESTX provides support for building REST APIs. The resulting APIs come automatically with the Swagger UI page as a documentation page and a UI for API testing.


| ![027-feature-image.png](https://behainguyen.files.wordpress.com/2022/07/027-feature-image.png) |
|:--:|
| *Python: Flask-RESTX and the Swagger UI automatic documentation.* |

<p>
I've recently checked out <a href="https://flask-restx.readthedocs.io/en/latest/index.html" title="Flask-RESTX" target="_blank">Flask-RESTX</a>, and along with it <a href="https://swagger.io/resources/open-api/" title="OpenAPI Specification" target="_blank">OpenAPI Specification</a>, and <span class="keyword"> Swagger UI</span>, which:
</p>

> – renders OpenAPI specs as interactive API documentation.

<p>
See <a href="https://swagger.io/docs/specification/about/" title="What Is OpenAPI?" target="_blank">What Is OpenAPI?</a>
</p>

<p>
<span class="keyword"> Flask-RESTX</span> provides support for building <span class="keyword"> REST APIs</span>. The resulting <span class="keyword"> APIs</span> come automatically with the <span class="keyword"> Swagger UI</span> page as documentation and a <span class="keyword"> UI</span> for <span class="keyword"> API</span> testing.
</p>

<p>
Please note, I'm using the term <span class="keyword"> “REST API”</span> out of conformity. It's a complicated topic, and there are a lot of discussions on the net, please see among others:
</p>

<ol>
<li style="margin-top:5px;">
<a href="https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm" title="CHAPTER 5 Representational State Transfer (REST)" target="_blank">https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm</a>
</li>

<li style="margin-top:10px;">
<a href="https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm" title="Architectural Styles and the Design of Network-based Software Architectures" target="_blank">https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm</a>
</li>

<li style="margin-top:10px;">
<a href="https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven" title="REST APIs must be hypertext-driven" target="_blank">https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven</a>
</li>

<li style="margin-top:10px;">
<a href="https://phauer.com/2015/restful-api-design-best-practices/" title="RESTful API Design. Best Practices in a Nutshell." target="_blank">https://phauer.com/2015/restful-api-design-best-practices/</a>
</li>

<li style="margin-top:10px;">
<a href="https://stackoverflow.com/questions/2001773/understanding-rest-verbs-error-codes-and-authentication?noredirect=1&lq=1" title="Understanding REST: Verbs, error codes, and authentication" target="_blank">https://stackoverflow.com/questions/2001773/understanding-rest-verbs-error-codes-and-authentication?noredirect=1&lq=1</a>
</li>

<li style="margin-top:10px;">
<a href="https://stackoverflow.com/questions/7140074/restfully-design-login-or-register-resources" title="RESTfully design /login or /register resources?" target="_blank">https://stackoverflow.com/questions/7140074/restfully-design-login-or-register-resources</a>
</li>

<li style="margin-top:10px;">
<a href="https://stackoverflow.com/questions/15098392/which-http-method-should-login-and-logout-actions-use-in-a-restful-setup?noredirect=1&lq=1" title="Which HTTP method should Login and Logout Actions use in a 'RESTful' setup" target="_blank">https://stackoverflow.com/questions/15098392/which-http-method-should-login-and-logout-actions-use-in-a-restful-setup?noredirect=1&lq=1</a>
</li>

<li style="margin-top:10px;">
<a href="https://stackoverflow.com/questions/51376453/how-to-design-a-restful-url-for-login?noredirect=1&lq=1" title="How to design a restful url for login?" target="_blank">https://stackoverflow.com/questions/51376453/how-to-design-a-restful-url-for-login?noredirect=1&lq=1</a>
</li>

<li style="margin-top:10px;">
<a href="https://stackoverflow.com/questions/6068113/do-sessions-really-violate-restfulness" title="Do sessions really violate RESTfulness?" target="_blank">https://stackoverflow.com/questions/6068113/do-sessions-really-violate-restfulness</a>
</li>

<li style="margin-top:10px;">
<a href="https://stackoverflow.com/questions/319530/restful-authentication?rq=1" title="RESTful Authentication" target="_blank">https://stackoverflow.com/questions/319530/restful-authentication?rq=1</a>
</li>

<li style="margin-top:10px;">
<a href="https://www.google.com/search?q=rfc+rest+api&sxsrf=ALiCzsaPuYDxxY6r8MRV1OllFJ-f7tGs5Q%3A1657516774647&source=hp&ei=5rLLYrHGJauPseMP-ca4uAQ&iflsig=AJiK0e8AAAAAYsvA9j6sdXmU61eth0MeYLOfPaRzoBoV&ved=0ahUKEwix0b2Ui_D4AhWrR2wGHXkjDkcQ4dUDCAg&uact=5&oq=rfc+rest+api&gs_lcp=Cgdnd3Mtd2l6EAMyBQgAEIAEMgYIABAeEBYyBggAEB4QFjIGCAAQHhAWMgYIABAeEBYyBggAEB4QFjoECCMQJzoLCAAQgAQQsQMQgwE6DgguEIAEELEDEMcBEKMCOhEILhCABBCxAxCDARDHARDRAzoLCC4QgAQQsQMQgwE6DgguEIAEELEDEIMBENQCOggIABCABBCxAzoLCC4QgAQQxwEQrwE6CAguEIAEENQCOgUILhCABDoICAAQgAQQyQM6CQgAEB4QyQMQFjoICAAQHhAWEApQAFjtIWD9I2gBcAB4AoAB6gaIAbQikgENMC43LjMuMC4xLjEuMpgBAKABAQ&sclient=gws-wiz" title="Google search 'rfc rest api'" target="_blank">Google search “rfc rest api”</a>
</li>
</ol>

<p>
I'm keen on seeing how this works. My focus was primarily getting out some inbuilt <span class="keyword"> Swagger UI</span> page. I want to understand how it works before focusing on other aspects of <a href="https://flask-restx.readthedocs.io/en/latest/index.html" title="Flask-RESTX" target="_blank">Flask-RESTX</a>.
</p>

<p>
I fancy a website whereby I can keep the information on trees. To start off, I would just have two <span class="keyword"> APIs</span>: one to create a new tree record in the database, the other just returns all records in the table! This is just to keep things simple, nobody in their right mind would return all records in a table in a one go!
</p>

<p>
The screen capture below shows the <span class="keyword"> Swagger UI</span> page for the two <span class="keyword"> tree APIs</span>:
</p>

![027-01.png](https://behainguyen.files.wordpress.com/2022/07/027-01.png)

<p>
<span class="keyword"> POST API create a tree</span> is shown in detail in the following screen capture. This <span class="keyword"> API</span> has three ( 3 ) mandatory form fields, two ( 2 ) are normal string, one ( 1 ) is a <span class="keyword"> URL</span>. And four ( 4 ) possible response codes. Click on <span class="keyword"> “Try it out”</span> button on the top right hand side corner to try this method. To simulate <span class="keyword"> <strong>400	Validation error</strong></span>, enter some digits into either name field.
</p>

![027-02.png](https://behainguyen.files.wordpress.com/2022/07/027-02.png)

<p>
The final <span class="keyword"> API method</span> has no input parameter, and also a few possible response codes and messages.
</p>

![027-03.png](https://behainguyen.files.wordpress.com/2022/07/027-03.png)

<p>
<span style="color:blue;">Please note, the <span class="keyword"> Swagger UI</span> page just happens automatically, we don't have to download and install anything. </span>
</p>

<p>
As we shall see, there're steps we have to follow to get the <span class="keyword"> Swagger UI</span> page correctly, but those steps are also part of the <span class="keyword"> API</span> code... so I do feel we get it for almost free.
</p>

<p>
To start off, we create the <span class="keyword"> API</span> boilerplate code. The initial files and directory structure is as follows:
</p>

```
<pre>
f:\flask_restx_demo
|
|-- .env
|-- app.py
|-- setup.py
|
|-- src\
|   |
|   |-- flask_restx_demo\
|       |
|       |-- __init__.py
|       |-- config.py
```
            
<p>
Let's list the content of each file, since they are very short.
</p>

```
File f:\flask_restx_demo\.env
```

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=">s3g;?uV^K=`!(3.#ms_cdfy<c4ty%"
```

```
File f:\flask_restx_demo\app.py
```

{% highlight python linenos %}
"""Flask Application entry point."""

from flask_restx_demo import create_app

app = create_app()
{% endhighlight %}

```
File f:\flask_restx_demo\setup.py
```

{% highlight python linenos %}
"""Installation script for flask_restx demo project."""
from pathlib import Path
from setuptools import setup, find_packages

setup(
    name='flask-restx-demo',
    description='Flask-RESTX and Swagger UI Demo.',
    version='1.0.0',
    author='Van Be Hai Nguyen',
    author_email='behai_nguyen@hotmail.com',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires='>=3.10',
    install_requires=[
        'Flask',
        'python-dotenv',
        'Flask-RESTX',
        'Flask-SQLAlchemy',
    ],
)
{% endhighlight %}

```
File f:\flask_restx_demo\src\flask_restx_demo\__init__.py
```

{% highlight python linenos %}
"""Flask app initialization via factory pattern."""
from flask import Flask

from flask_restx_demo.config import get_config

def create_app():
    app = Flask( 'flask-restx-demo' )

    app.config.from_object( get_config() )

    return app
{% endhighlight %}

```
File f:\flask_restx_demo\src\flask_restx_demo\config.py
```

{% highlight python linenos %}
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

<p>
Run the following commands to create a virtual environment 
<span class="keyword">
venv</span> and activate it:
</p>

```
F:\flask_restx_demo>C:\PF\Python310\python.exe -m pip install --upgrade pip
```

```
F:\flask_restx_demo>C:\PF\Python310\python.exe -m pip install --user virtualenv
```

```
F:\flask_restx_demo>C:\Users\behai\AppData\Roaming\Python\Python310\Scripts\virtualenv.exe venv
```

```
F:\flask_restx_demo>venv\Scripts\activate.bat
```

<p>
Run the below command to editable install required packages:
</p>

```
(venv) F:\flask_restx_demo>venv\Scripts\pip.exe install -e .
```

<p>
Command:
</p>

```
(venv) F:\flask_restx_demo>venv\Scripts\flask.exe routes
```

<p>
would show the following:
</p>

```
Endpoint  Methods  Rule
--------  -------  -----------------------
static    GET      /static/<path:filename>
```

<p>
Next, we'll need to configure 
<span class="keyword">
flask's Blueprint</span> and 
<span class="keyword">
flask_restx's Api</span>. Our directory structure should now look 
like below, where ★ indicates new files, and ☆ indicates files to
be modified:
</p>

```
f:\flask_restx_demo
|
|-- .env
|-- app.py
|-- setup.py
|
|-- src\
|   |
|   |-- flask_restx_demo\
|       |
|       |-- __init__.py ☆
|       |-- config.py
|       |-- api\
|           |       
|           |-- __init__.py ★
|
|-- venv\
```

```
New file F:\flask_restx_demo\src\flask_restx_demo\api\__init__.py
```

{% highlight python linenos %}
""" Flask-RESTX API blueprint configuration. """
from flask import Blueprint
from flask_restx import Api

api_bp = Blueprint( 'api', __name__, url_prefix='/api/v1' )

api = Api(
    api_bp,
    version='1.0',
    title='Flask-RESTX API Demo',
    description='Welcome to Flask-RESTX API with Swagger UI documentation',
    doc='/ui',
)
{% endhighlight %}

<p>
Following documentations, I'm assigning
<span class="keyword">
version 1.0</span> to the first implementation, also the 
<span class="keyword">
API</span> path starts with 
<span class="keyword">
/api/v1</span>. And 
<span class="keyword">
/api/v1/ui</span> is the 
<span class="keyword">
Swagger UI</span> path.
</p>

```
Modified file f:\flask_restx_demo\src\flask_restx_demo\__init__.py
```

<p>
Please note the lines added are <strong>line 11</strong> and 
<strong>line 13</strong>:
</p>

{% highlight python linenos %}
"""Flask app initialization via factory pattern."""
from flask import Flask

from flask_restx_demo.config import get_config

def create_app():
    app = Flask( 'flask-restx-demo' )

    app.config.from_object( get_config() )

    from flask_restx_demo.api import api_bp

    app.register_blueprint( api_bp )

    return app
{% endhighlight %}

<p>
If everything goes well, and it should go well, the command:
</p>

```
(venv) F:\flask_restx_demo>venv\Scripts\flask.exe routes
```

<p>
now would show the following:
</p>

```
Endpoint          Methods  Rule
----------------  -------  --------------------------
api.doc           GET      /api/v1/ui
api.root          GET      /api/v1/
api.specs         GET      /api/v1/swagger.json
restx_doc.static  GET      /swaggerui/<path:filename>
static            GET      /static/<path:filename>
```

<p>
The skeleton for the 
<span class="keyword">
APIs</span> we're going to write is pretty much in place. We shall
also need a database, and a table to store trees' information. Let's
do the database first.
</p>

<p>
We're using 
<a href="https://docs.sqlalchemy.org/en/14/"
title="SQLAlchemy" target="_blank">SQLAlchemy</a> 
with a <a href="https://www.sqlite.org/index.html"
title="SQLite" target="_blank">SQLite</a> database. The
<span class="keyword">
flask_restx_demo.db</span> database file will be automatically
created under the project directory when we first run the 
application.
</p>

```
File f:\flask_restx_demo\.env -- final version
```

<p>
Added <strong>line 4</strong> and <strong>line 5</strong> which
define database info:
</p>

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=">s3g;?uV^K=`!(3.#ms_cdfy<c4ty%"
SQLALCHEMY_DATABASE_URI="sqlite:///flask_restx_demo.db"
SQLALCHEMY_TRACK_MODIFICATIONS=True
```

<p>
Now, we'll need to update 
<span class="keyword">
config.py</span> to read the two new pieces of database information.
The updated content follows below. New codes added are lines 
<strong>line 11</strong> and <strong>line 12</strong>:
</p>

```
File f:\flask_restx_demo\src\flask_restx_demo\config.py -- final version
```

{% highlight python linenos %}
"""Flask app config settings."""
import os

class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = os.getenv( 'SECRET_KEY' )
    FLASK_APP = os.getenv( 'FLASK_APP' )
    FLASK_ENV = os.getenv( 'FLASK_ENV' )
    SQLALCHEMY_DATABASE_URI = os.getenv( 'SQLALCHEMY_DATABASE_URI' )
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv( 'SQLALCHEMY_TRACK_MODIFICATIONS' )

def get_config():
    """Retrieve environment configuration settings."""
    return Config
{% endhighlight %}

<p>
The application factory must also be updated to manage database
extension object.
</p>

```
File f:\flask_restx_demo\src\flask_restx_demo\__init__.py -- final version
```

<p>
Please note the lines added are <strong>line 3</strong>, 
<strong>line 7</strong> and <strong>lines 18-20</strong>. It's
pretty much run-of-the-mill 
<span class="keyword">
Python</span> code.
</p>

{% highlight python linenos %}
"""Flask app initialization via factory pattern."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_restx_demo.config import get_config

db = SQLAlchemy()

def create_app():
    app = Flask( 'flask-restx-demo' )

    app.config.from_object( get_config() )

    from flask_restx_demo.api import api_bp

    app.register_blueprint( api_bp )

    db.init_app( app )
    with app.app_context():
        db.create_all()

    return app
{% endhighlight %}

<p>
The database codes are out of the way. Next comes the codes for 
the <span class="keyword">
APIs</span>. We'll need several new files as indicated by ★ in the new 
directory layout below:
</p>

```
f:\flask_restx_demo
|
|-- .env
|-- app.py
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
|       |   |-- __init__.py ☆
|       |   |
|       |   |-- trees\
|       |       |
|       |       |-- bro.py ★
|       |       |-- dto.py ★
|       |       |-- routes.py ★ 
|       |       |-- __init__.py ★
|       |
|       |-- models\
|           |       
|           |-- tree.py ★
|
|-- venv\
```

```
File F:\flask_restx_demo\src\flask_restx_demo\models\tree.py
```

<p>
<span class="keyword">
Tree class</span> is a 
<a href="https://docs.sqlalchemy.org/en/14/"
title="SQLAlchemy" target="_blank">SQLAlchemy</a> 
class, which basically represents a table in a database,
in this case the table name is 
<span class="keyword">
“tree”</span>:
</p>

{% highlight python linenos %}
"""Class definition for Tree model."""

from flask_restx_demo import db

class Tree( db.Model ):
    """Tree model for a generic resource for Flask-RESTX API Demo."""

    __tablename__ = "tree"

    id = db.Column( db.Integer, primary_key=True, autoincrement=True )
    scientific_name = db.Column( db.String(128), unique=True, nullable=False )
    common_name = db.Column( db.String(128), nullable=False )
    wiki_url = db.Column( db.String(255), nullable=False )

    def __repr__(self):
        return f"<Tree scientific name={self.scientific_name}, common name={self.common_name}>"

    @classmethod
    def find_by_scientific_name( cls, scientific_name ):
        return cls.query.filter_by( scientific_name=scientific_name ).first()
{% endhighlight %}

<p>
Under directory
</p>

```
F:\flask_restx_demo\src\flask_restx_demo\api\trees
```

<p>
<span class="keyword">
__init__.py</span> is to indicate a regular package. It's empty.
</p>

<p>
<span class="keyword">
DTO</span> is short for
<span class="keyword">
Data Transfer Object</span> -- please see 
<a href="https://www.google.com/search?q=swagger+ui+data+transfer+object&sxsrf=ALiCzsZFPHJOR4_6M85WnrL_CM-fc_s5gQ%3A1657587786906&source=hp&ei=SsjMYtueNdLUjuMP9L23iA4&iflsig=AJiK0e8AAAAAYszWWomqJiLY7q3Ece_waemZEEejNxZ8&ved=0ahUKEwjb6-HZk_L4AhVSqmMGHfTeDeEQ4dUDCAg&uact=5&oq=swagger+ui+data+transfer+object&gs_lcp=Cgdnd3Mtd2l6EAMyBwghEAoQoAE6BwgjEOoCECc6BAgjECc6BwguENQCEEM6BQgAEJECOhEILhCABBCxAxCDARDHARDRAzoLCAAQgAQQsQMQgwE6DQguEMcBENEDENQCEEM6BAgAEEM6EAguELEDEIMBEMcBENEDEEM6CggAELEDEIMBEEM6DQguELEDEMcBENEDEEM6CggAEIAEEIcCEBQ6BQgAEIAEOgYIABAeEBY6BQghEKABOggIIRAeEBYQHToECCEQFVAAWIRhYMJiaAFwAHgAgAHyBIgBhCuSAQowLjI3LjIuNS0xmAEAoAEBsAEK&sclient=gws-wiz"
title="Google search: swagger ui data transfer object"
target="_blank">Google search: “swagger ui data transfer object”</a>.
Basically 
<span class="keyword">
DTO</span> defines API model classes to serialise database
model classes to 
<span class="keyword">
JSON objects </span> before sending them back as HTTP responses.
See 
<a href="https://flask-restx.readthedocs.io/en/latest/marshalling.html"
title="Response marshalling" target="_blank">Response marshalling</a>.
</p>

```
File F:\flask_restx_demo\src\flask_restx_demo\api\trees\dto.py
```

{% highlight python linenos %}
"""Parsers and serializers for /trees API endpoints."""
import re

from flask_restx import Model
from flask_restx.fields import String
from flask_restx.inputs import URL
from flask_restx.reqparse import RequestParser

def tree_name( name ):
    """Validation method for a string containing only letters, '-' and space."""
    if not re.compile(r"^[A-Za-z, ' ', -]+$").match(name):
        raise ValueError(
            f"'{name}' contains one or more invalid characters. Tree name must "
            "contain only letters, hyphen and space characters."
        )
    return name

create_tree_reqparser = RequestParser( bundle_errors=True )
create_tree_reqparser.add_argument(
    'scientific_name',
    type=tree_name,
    location='form',
    required=True,
    nullable=False,
    case_sensitive=True,
)
create_tree_reqparser.add_argument(
    'common_name',
    type=tree_name,
    location='form',
    required=True,
    nullable=False,
    case_sensitive=True,
)
create_tree_reqparser.add_argument(
    'wiki_url',
    type=URL( schemes=[ 'http', 'https' ] ),
    location='form',
    required=True,
    nullable=False,
)

update_tree_reqparser = create_tree_reqparser.copy()
update_tree_reqparser.remove_argument( 'scientific_name' )

tree_model = Model( 'Tree', {
    'scientific_name': String,
    'common_name': String,
    'wiki_url': String,
})
{% endhighlight %}

<p>
<a href="https://flask-restx.readthedocs.io/en/latest/index.html"
title="Flask-RESTX" target="_blank">Flask-RESTX</a>
uses 
<a href="https://flask-restx.readthedocs.io/en/latest/parsing.html"
title="RequestParser" target="_blank">RequestParser</a> to manage
incoming request info.
<strong>Line 18</strong>, we instantiate an instance of
<span class="keyword">
RequestParser</span> to manage creating new trees requests:
</p>

```python
create_tree_reqparser = RequestParser( bundle_errors=True )
```

<p>
Please note, 
<span class="keyword">
bundle_errors=True</span> is explained very clearly in 
<a href="https://flask-restx.readthedocs.io/en/latest/parsing.html"
title="RequestParser" target="_blank">RequestParser | section Error Handling</a>,
basically, setting 
<span class="keyword">
bundle_errors=True</span> to collect and to return all errors at once.
</p>

<p>
A tree requires three ( 3 ) pieces of information.
<strong>Lines 19-41</strong>, we define the properties for
each of the 
<span class="keyword">
create_tree_reqparser</span>'s arguments. As previously mentioned, 
they're mandatory form fields, that would explain 
<span class="keyword">
location='form'</span>, 
<span class="keyword">
required=True</span> and
<span class="keyword">
nullable=False</span>. 
<span class="keyword">
type</span> indicates how an argument ( field ) should be validated.
For 
<span class="keyword">
scientific_name</span> and 
<span class="keyword">
common_name</span>, the validation is based on the custom method:
</p>

```python
def tree_name( name ):
```

<p>
Whereas for 
<span class="keyword">
type</span>, it must a valid URL.
</p>

<p>
<strong>Lines 43-44</strong> are known as 
<span class="keyword">
“parser inheritance”</span>:
</p>

```python
update_tree_reqparser = create_tree_reqparser.copy()
update_tree_reqparser.remove_argument( 'scientific_name' )
```

<p>
We're not implementing an
<span class="keyword">
update API</span>. This is just to show how inheritance works.
<span class="keyword">
update_tree_reqparser</span> is a “clone” of
<span class="keyword">
create_tree_reqparser</span> but without the 
<span class="keyword">
scientific_name</span> argument.
</p>

<p>
Finally, <strong>lines 46-50</strong> defines the serialised API model class:
</p>

```python
tree_model = Model( 'Tree', {
    'scientific_name': String,
    'common_name': String,
    'wiki_url': String,
})
```

<p>
<span class="keyword">
BRO</span> or 
<span class="keyword">
Business Rule Object</span> is a convention used by a company 
I worked for earlier
in my career, during the 
<span class="keyword">
COM/COM+/DCOM</span> days... Since there's 
<span class="keyword">
DTO</span>, so I thought it would be nice to revive this naming
once again. 
</p>

```
File F:\flask_restx_demo\src\flask_restx_demo\api\trees\bro.py
```

{% highlight python linenos %}
"""Business rules ( logic ) for /trees API endpoints."""
from http import HTTPStatus

from flask import jsonify
from flask_restx import abort, marshal

from flask_restx_demo import db
from flask_restx_demo.models.tree import Tree
from flask_restx_demo.api.trees.dto import tree_model

def _create_successful_response( status_code, message ):
    response = jsonify(
        status="success",
        message=message,
    )
    response.status_code = status_code
    response.headers[ 'Cache-Control' ] = 'no-store'
    response.headers[ 'Pragma' ] = 'no-cache'
    return response

def create_tree( tree_dict ):
    if Tree.find_by_scientific_name( tree_dict['scientific_name'] ):
        abort( HTTPStatus.CONFLICT, f"{tree_dict['scientific_name']} is already entered", status="fail" )
    new_tree = Tree( **tree_dict )
    db.session.add( new_tree )
    db.session.commit()
    return _create_successful_response(
        status_code=HTTPStatus.CREATED,
        message='successfully created',
    )

def retrieve_tree_list():
    data = Tree.query.all()
    response_data = marshal( data, tree_model )
    response = jsonify( response_data )
    return response
{% endhighlight %}

<p>
<strong>Line 21</strong> defines an 
<span class="keyword">
API</span> method:
</p>

```python
def create_tree( tree_dict ):
```

<p>
This method first ensures that the new 
<span class="keyword">
scientific_name</span> is not already in the database, then
via the 
<span class="keyword">
** operator</span>, it unpacks the dictionary argument into
keyword arguments, and creates a new record for the new tree.
See also 
<a href="https://reference.codeproject.com/python3/dictionaries/python-dictionary-unpack"
title="The Python Dictionary ** unpack operator"
target="_blank">The Python Dictionary ** unpack operator</a>.
</p>

<p>
Once done, it sends back a 
<span class="keyword">
JSON</span> response consisting of a code and a message.
</p>

<p>
<strong>Line 32</strong> defines another 
<span class="keyword">
API</span> method:
</p>

```python
def retrieve_tree_list():
```

<p>
This method first retrieves data from the database table, then
serialises database data into the API model class defined in module
<span class="keyword">
dto.py</span> earlier. And finally returns this serialised data 
as <span class="keyword">
JSON</span> via 
<span class="keyword">
HTTP</span> response.
</p>

<p>
The final new module implements 
<span class="keyword">
API endpoints</span>:
</p>

```
File F:\flask_restx_demo\src\flask_restx_demo\api\trees\routes.py
```

{% highlight python linenos %}
"""API endpoint definitions for /trees namespace."""
from http import HTTPStatus

from flask_restx import Namespace, Resource

from flask_restx_demo.api.trees.dto import (
    create_tree_reqparser,
    tree_model,
)

from flask_restx_demo.api.trees.bro import (
    create_tree,
    retrieve_tree_list,
)

tree_ns = Namespace( name="trees", validate=True )
# tree_ns.models[ tree_model.name ] = tree_model
# tree_ns.add_model( tree_model.name, tree_model )
tree_ns.model( tree_model.name, tree_model )

@tree_ns.route( "", endpoint='tree_list' )
@tree_ns.response( int(HTTPStatus.BAD_REQUEST), 'Validation error.' )
@tree_ns.response( int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.' )
class TreeList( Resource ):
    """ Handles HTTP requests to URL: /trees. """

    @tree_ns.response( int(HTTPStatus.OK), 'Retrieved tree list.' )
    def get( self ):
        """ Retrieve tree list. """
        return retrieve_tree_list()

    @tree_ns.response(int(HTTPStatus.CREATED), 'Added new tree.' )
    @tree_ns.response(int(HTTPStatus.CONFLICT), 'Tree name already exists.' )
    @tree_ns.expect( create_tree_reqparser )
    def post( self ):
        """ Create a tree. """
        tree_dict = create_tree_reqparser.parse_args()
        return create_tree( tree_dict )
{% endhighlight %}

<p>
For <span class="keyword">
API</span>, 
<a href="https://flask-restx.readthedocs.io/en/latest/api.html#flask_restx.Namespace"
title="class flask_restx.Namespace(name, description=None, path=None, decorators=None, validate=None, authorizations=None, ordered=False, **kwargs)"
target="_blank">class flask_restx.Namespace( ... )</a> is what
<a href="https://flask.palletsprojects.com/en/2.1.x/api/#blueprint-objects"
title="flask.Blueprint" target="_blank">flask.Blueprint</a> is to 
<a href="https://flask.palletsprojects.com/en/2.1.x/api/#flask.Flask"
title="flask.Flask" target="_blank">flask.Flask</a>.
</p>

<p>
<strong>Lines 16-19</strong>
we instantiate an instance of
<span class="keyword">
flask_restx.Namespace</span>, and register our target 
<span class="keyword">
DTO API model class</span> with it: it seems we can do this via
three ( 3 ) different methods, we're using the documented method
( <strong>line 19</strong> ); commented <strong>lines 17, 18</strong>
are also valid codes.
</p>

<p>
In 
<a href="https://flask-restx.readthedocs.io/en/latest/index.html"
title="Flask-RESTX" target="_blank">Flask-RESTX</a> context,
<span class="keyword">
trees</span> are 
<a href="https://flask-restx.readthedocs.io/en/latest/api.html#flask_restx.Resource"
title="class flask_restx.Resource(api=None, *args, **kwargs)"
target="_blank">class flask_restx.Resource( ... )</a>, and so
<span class="keyword">
class TreeList</span> extends from this abstract class as per documentation.
This class has several decorators. The first one:
</p>

```python
@tree_ns.route( "", endpoint='tree_list' )
```

<p>
The value of the first parameter is blank, which indicates that this 
resource doesn't have an endpoint of its own, it'll use the endpoint
provided by the <span class="keyword">
Namespace</span>. That means, both 
<span class="keyword">
API methods</span> are accessible via:
</p>

```
/api/v1/trees
```

<p>
For example:
</p>

```
http://127.0.0.1:5000/api/v1/trees
```

<p>
The requested 
<span class="keyword">
HTTP method</span>, 
<span class="keyword">
GET</span> or
<span class="keyword">
POST</span> differentiates between the two.
</p>

<p>
The next two decorators declare response codes and response messages:
</p>

```python
@tree_ns.response( int(HTTPStatus.BAD_REQUEST), 'Validation error.' )
@tree_ns.response( int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.' )
```

<p>
Did you see that the 
<span class="keyword">
Swagger UI</span> uses info in these decorators in the page?
</p>

<p>
Now go inside 
<span class="keyword">
class TreeList</span> -- we have two main methods:
</p>

```python
def get( self ):
def post( self ):
```

<p>
which're 
<span class="keyword">
API methods</span> -- they call to methods defined in 
<span class="keyword">
bro.py</span>, discussed earlier, to do the work. As can be seen,
these methods can also have decorators which define additional
response codes and associated messages.
</p>

```python
@tree_ns.expect( create_tree_reqparser )
```

<p>
The above decorator is explained under 
<a href="https://flask-restx.readthedocs.io/en/latest/api.html#flask_restx.Namespace"
title="class flask_restx.Namespace(name, description=None, path=None, decorators=None, validate=None, authorizations=None, ordered=False, **kwargs)"
target="_blank">class flask_restx.Namespace( ... )</a>.
</p>

<p>
Finally, we need to make the new codes effective. We need to update
the main 
<span class="keyword">
API</span> module:
</p>

```
File f:\flask_restx_demo\src\flask_restx_demo\api\__init__.py -- final version
```

{% highlight python linenos %}
""" Flask-RESTX API blueprint configuration. """
from flask import Blueprint
from flask_restx import Api

from flask_restx_demo.api.trees.routes import tree_ns

api_bp = Blueprint( 'api', __name__, url_prefix='/api/v1' )

api = Api(
    api_bp,
    version='1.0',
    title='Flask-RESTX API Demo',
    description='Welcome to Flask-RESTX API with Swagger UI documentation',
    doc='/ui',
)

api.add_namespace( tree_ns, path='/trees' )
{% endhighlight %}

There're only two new lines added: <strong>line 5</strong>
and <strong>line 17</strong>.

<p>
That's about it for this post 😆. I wasn't sure if it's worth writing or not... I must
say I wasn't very enthusiastic about writing it: since the codes are mediocre and not
every exciting. I like to learn stuff in incremental steps... This is one of these
steps. So I thought I would write this one for me... I'm sorry it is a bit long, but 
as I'm writing it, more and more stuff seems to need explanations. I hope I did not 
make any mistakes in the codes and in the post. This's merely scratching the surface... 
There're still much more to the subject. Thank you for reading and I hope you find 
this one useful.
</p>