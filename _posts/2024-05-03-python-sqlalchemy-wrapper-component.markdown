---
layout: post
title: "Python: A SQLAlchemy Wrapper Component That Works With Both Flask and FastAPI Frameworks"

description: In late 2022, I developed a database wrapper component for SQLAlchemy. Initially designed for use with the Flask framework, it was discovered that this component also seamlessly integrates with the FastAPI framework. In this post, I will describe this component and provide examples of how it is used within both frameworks. 

tags:
- SQLAlchemy
- Flask
- FastAPI
- MySQL
- PostgreSQL
- database wrapper
---

<em>In late 2022, I developed a <a href="https://pypi.org/project/bh-database/" title="bh-database" target="_blank">database wrapper component</a> for <a href="https://www.sqlalchemy.org/" title="SQLAlchemy" target="_blank">SQLAlchemy</a>. Initially designed for use with the <a href="https://flask.palletsprojects.com/en/3.0.x/" title="Flask" target="_blank">Flask</a> framework, it was discovered that this component also seamlessly integrates with the <a href="https://fastapi.tiangolo.com/" title="FastAPI" target="_blank">FastAPI</a> framework. In this post, I will describe this component and provide examples of how it is used within both frameworks.</em>

| ![104-feature-image.png](https://behainguyen.files.wordpress.com/2024/05/104-feature-image.png) |
|:--:|
| *Python: A SQLAlchemy Wrapper Component That Works With Both Flask and FastAPI Frameworks* |

This component is based on a concept I previously implemented using Delphi and later PHP. Essentially, it consists of base classes representing database tables, equipped with the ability to interact with databases and implement generic functionalities for CRUD operations.

While learning the <a href="https://flask.palletsprojects.com/en/3.0.x/" title="Flask" target="_blank">Flask</a> framework, I found the conventional approach of accessing the database layer through the Flask application instance uncomfortable. In my previous projects, the database layer has always remained independent of other layers. The business layer ensures data validity and then delegates CRUD operations to the database layer. The UI layer, whether a desktop application or web client, communicates solely with the business layer, never directly accessing the database layer.

In <a href="https://www.sqlalchemy.org/" title="SQLAlchemy" target="_blank">SQLAlchemy</a>, <code>model</code>s representing database tables typically subclass <a href="https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase" title="sqlalchemy.orm.DeclarativeBase" target="_blank">sqlalchemy.orm.DeclarativeBase</a> (this class supersedes the <a href="https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declarative_base" title="sqlalchemy.orm.declarative_base" target="_blank">sqlalchemy.orm.declarative_base</a> function). Accordingly, the abstract base class in this <a href="https://pypi.org/project/bh-database/" title="bh-database" target="_blank">database wrapper component</a> is a <code>sqlalchemy.orm.DeclarativeBase</code> subclass, accompanied by another custom base class providing additional dunder methods.

Further subclasses of this abstract base class implement additional functionalities. Application models inherit from either the <a href="https://bh-database.readthedocs.io/en/latest/base_table.html#bh_database.base_table.ReadOnlyTable" title="ReadOnlyTable" target="_blank">ReadOnlyTable</a> or the <a href="https://bh-database.readthedocs.io/en/latest/base_table.html#bh_database.base_table.WriteCapableTable" title="WriteCapableTable" target="_blank">WriteCapableTable</a> base classes.

Application <code>model</code>s are required to implement their own specific database reading methods. For example, selecting all customers with the surname <code>Nguyễn</code>.

The <a href="https://bh-database.readthedocs.io/en/latest/core.html#bh_database.core.Database" title="Database" target="_blank">Database</a> class is responsible for establishing connections to the target database. Once the database connection is established, application models can interact with the target database.

🚀 The full documentation can be found at <a href="https://bh-database.readthedocs.io/en/latest/" title="bh-database API documentation" target="_blank">https://bh-database.readthedocs.io/en/latest/</a>.

Next, we will explore some examples. <strong><em>💥 The first two are simple, single-module web server applications where the web layer directly accesses the database layer.</em> Although not ideal, it simplifies usage illustration.</strong>

The latter two examples include complete business layers, where submitted data is validated before being passed to the database layer for CRUD operations.

❶ <code>example.py</code>: A Simple Single-Module <a href="https://flask.palletsprojects.com/en/3.0.x/" title="Flask" target="_blank">Flask</a> Application.

● Windows 10: <code>F:\bh_database\examples\flaskr\example.py</code><br/>
● Ubuntu 22.10: <code>/home/behai/bh_database/examples/flaskr/example.py</code>

```python
from sqlalchemy import (
    Column,
    Integer,
    Date,
    String,
)

import flask

from bh_database.core import Database
from bh_database.base_table import WriteCapableTable

from bh_apistatus.result_status import ResultStatus

SQLALCHEMY_DATABASE_SCHEMA = 'employees'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:pcb.2176310315865259@localhost:3306/employees'
# Enable this for PostgreSQL.
# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:pcb.2176310315865259@localhost/employees'

class Employees(WriteCapableTable):
    __tablename__ = 'employees'

    emp_no = Column(Integer, primary_key=True)
    birth_date = Column(Date, nullable=False)
    first_name = Column(String(14), nullable=False)
    last_name = Column(String(16), nullable=False)
    gender = Column(String(1), nullable=False)
    hire_date = Column(Date, nullable=False)

    def select_by_partial_last_name_and_first_name(self, 
            last_name: str, first_name: str) -> ResultStatus:
        
        return self.run_stored_proc('get_employees', [last_name, first_name], True)

def create_app(config=None):
    """Construct the core application."""

    app = flask.Flask(__name__, instance_relative_config=False)

    init_extensions(app)
    
    init_app_database(app)

    return app
    
def init_extensions(app):
    app.url_map.strict_slashes = False

def init_app_database(app):    
    Database.disconnect()
    Database.connect(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_DATABASE_SCHEMA)

app = create_app()

@app.get('/employees/search/<last_name>/<first_name>')
def search_employees(last_name: str, first_name: str) -> dict:
    """ last_name and first_name are partial using %.

    An example of a valid route: http://localhost:5000/employees/search/%nas%/%An
    """

    return Employees() \
        .select_by_partial_last_name_and_first_name(last_name, first_name) \
        .as_dict()

if __name__ == '__main__':  
   app.run()
```

To execute the <code>example.py</code> application:

```
▶️<code>Windows 10:</code> (venv) F:\bh_database\examples\flaskr>venv\Scripts\flask.exe --app example run --host 0.0.0.0 --port 5000
▶️<code>Ubuntu 22.10:</code> (venv) behai@hp-pavilion-15:~/bh_database/examples/flaskr$ venv/bin/flask --app example run --host 0.0.0.0 --port 5000
```

Accessing the <code>example.py</code> application running locally from Windows 10:

```
http://localhost:5000/employees/search/%nas%/%An
```

Accessing the <code>example.py</code> application running on Ubuntu 22.10 from Windows 10:

```
http://192.168.0.16:5000/employees/search/%nas%/%An
```

❷ <code>example.py</code>: A Simple Single-Module <a href="https://fastapi.tiangolo.com/" title="FastAPI" target="_blank">FastAPI</a> Application.

● Windows 10: <code>F:\bh_database\examples\fastapir\example.py</code><br/>
● Ubuntu 22.10: <code>/home/behai/bh_database/examples/fastapir/example.py</code>

```python
from sqlalchemy import (
    Column,
    Integer,
    Date,
    String,
)

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from bh_database.core import Database
from bh_database.base_table import WriteCapableTable

from bh_apistatus.result_status import ResultStatus

SQLALCHEMY_DATABASE_SCHEMA = 'employees'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:pcb.2176310315865259@localhost:3306/employees'
# Enable this for PostgreSQL.
# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:pcb.2176310315865259@localhost/employees'

class Employees(WriteCapableTable):
    __tablename__ = 'employees'

    emp_no = Column(Integer, primary_key=True)
    birth_date = Column(Date, nullable=False)
    first_name = Column(String(14), nullable=False)
    last_name = Column(String(16), nullable=False)
    gender = Column(String(1), nullable=False)
    hire_date = Column(Date, nullable=False)

    def select_by_partial_last_name_and_first_name(self, 
            last_name: str, first_name: str) -> ResultStatus:
        
        return self.run_stored_proc('get_employees', [last_name, first_name], True)

app = FastAPI()

Database.disconnect()
Database.connect(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_DATABASE_SCHEMA)

@app.get("/employees/search/{last_name}/{first_name}", response_class=JSONResponse)
async def search_employees(last_name: str, first_name: str):
    """ last_name and first_name are partial using %.

    An example of a valid route: http://localhost:5000/employees/search/%nas%/%An
    """

    return Employees() \
        .select_by_partial_last_name_and_first_name(last_name, first_name) \
        .as_dict()
```

To execute the <code>example.py</code> application:

```
▶️<code>Windows 10:</code> (venv) F:\bh_database\examples\fastapir>venv\Scripts\uvicorn.exe example:app --host 0.0.0.0 --port 5000
▶️<code>Ubuntu 22.10:</code> (venv) behai@hp-pavilion-15:~/bh_database/examples/fastapir$ venv/bin/uvicorn example:app --host 0.0.0.0 --port 5000
```

Accessing the <code>example.py</code> application running locally from Windows 10:

```
http://localhost:5000/employees/search/%nas%/%An
```

Accessing the <code>example.py</code> application running on Ubuntu 22.10 from Windows 10:

```
http://192.168.0.16:5000/employees/search/%nas%/%An
```

❸ A more comprehensive <a href="https://flask.palletsprojects.com/en/3.0.x/" title="Flask" target="_blank">Flask</a> application: a fully documented web server example with CRUD operations.

Please refer to <a href="https://github.com/behai-nguyen/bh_database/tree/main/examples/flaskr" title="Flask web server example with CRUD operations." target="_blank">https://github.com/behai-nguyen/bh_database/tree/main/examples/flaskr</a> for the full source code, instructions on setting up the environment, installing packages, running tests, and finally running the application.

The layout of the example project is as follows:

```
/home/behai/bh_database/examples/flaskr
├── app.py
├── .env
├── pyproject.toml
├── pytest.ini
├── README.md
├── src
│ └── flaskr
│     ├── business
│     │ ├── app_business.py
│     │ ├── base_business.py
│     │ ├── base_validation.py
│     │ ├── employees_mgr.py
│     │ └── employees_validation.py
│     ├── config.py
│     ├── controllers
│     │ └── employees_admin.py
│     ├── __init__.py
│     ├── models
│     │ └── employees.py
│     ├── static
│     │ └── styles.css
│     └── templates
│         ├── admin
│         │ ├── emp_edit.html
│         │ ├── emp_search.html
│         │ └── emp_search_result.html
│         └── base.html
└── tests
    ├── business
    │ └── test_employees_mgr.py
    ├── conftest.py
    ├── __init__.py
    ├── integration
    │ └── test_employees_itgt.py
    └── unit
        └── test_employees.py
```

❹ A more comprehensive <a href="https://fastapi.tiangolo.com/" title="FastAPI" target="_blank">FastAPI</a> application: a fully documented web server example with CRUD operations.

Please refer to <a href="https://github.com/behai-nguyen/bh_database/tree/main/examples/fastapir" title="FastAPI web server example with CRUD operations." target="_blank">https://github.com/behai-nguyen/bh_database/tree/main/examples/fastapir</a> for the full source code, instructions on setting up the environment, installing packages, running tests, and finally running the application.

The layout of the example project is as follows:

```
/home/behai/bh_database/examples/fastapir
├── .env
├── main.py
├── pyproject.toml
├── pytest.ini
├── README.md
├── src
│ └── fastapir
│     ├── business
│     │ ├── app_business.py
│     │ ├── base_business.py
│     │ ├── base_validation.py
│     │ ├── employees_mgr.py
│     │ └── employees_validation.py
│     ├── config.py
│     ├── controllers
│     │ ├── employees_admin.py
│     │ └── __init__.py
│     ├── __init__.py
│     ├── models
│     │ └── employees.py
│     ├── static
│     │ └── styles.css
│     └── templates
│         ├── admin
│         │ ├── emp_edit.html
│         │ ├── emp_search.html
│         │ └── emp_search_result.html
│         └── base.html
└── tests
    ├── business
    │ └── test_employees_mgr.py
    ├── conftest.py
    ├── __init__.py
    ├── integration
    │ └── test_employees_itgt.py
    └── unit
        └── test_employees.py
```

💥 Except for the framework-specific layer code, the remaining code in these two examples is very similar.

Let's briefly discuss their similarities:

<ul>
<li style="margin-top:10px;">
<code>/models</code> and <code>/business</code> code are identical. They could be shared across both examples, but I prefer to keep each example self-contained.
</li>
<li style="margin-top:10px;">
<code>/tests/unit</code> and <code>/tests/business</code> code are identical.
</li>
</ul>

<p>
And there are differences in the following areas:
</p>

<ul>
<li style="margin-top:10px;">
<code>/controllers</code>: This is the web layer, which is framework-specific, so understandably they are different.
</li>

<li style="margin-top:10px;">
<code>/tests/integration</code>: The sole difference is framework-specific: how the HTTP response value is extracted:

<ul>
<li style="margin-top:10px;">
<code>Flask</code>: <code>response.get_data(as_text=True)</code>
</li>

<li style="margin-top:10px;">
<code>FastAPI</code>: <code>response.text</code>
</li>			
</ul>
</li>

<li style="margin-top:10px;">
<code>/tests/conftest.py</code>: This file is framework-dependent. Both modules return the same fixtures, but the code has nothing in common.
</li>

<li style="margin-top:10px;">
<code>/templates/base.html</code>: There is one difference:

<ul>
<li style="margin-top:10px;">
<code>Flask</code>: <code>&lt;link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}"></code>
</li>

<li style="margin-top:10px;">
<code>FastAPI</code>: <code>&lt;link rel="stylesheet" href="{{ url_for('static', path='/styles.css') }}"></code>
</li>			
</ul>

<p>
That is, <code>Flask</code> uses <code>filename</code>, while 
<code>FastAPI</code> uses <code>path</code>.
</p>
</li>
</ul>

<p>
The <code>/controllers</code> layer is thin in the sense that the code is fairly short; it simply takes the client-submitted data and passes it to the business layer to handle the work. The business layer then forwards the validated data to the database layer, and so on. The differences between the two implementations are minor.
</p>

<p>
It has been an interesting exercise developing this wrapper component. The fact that it seamlessly integrates with the <a href="https://fastapi.tiangolo.com/" title="FastAPI" target="_blank">FastAPI</a> framework is just a bonus for me; I didn't plan for it since I hadn't learned <code>FastAPI</code> at the time. I hope you find this post useful. Thank you for reading, and stay safe as always.
</p>

<p>✿✿✿</p>

<p>
Feature image source:
</p>

<ul>
<li>
<a href="https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper" target="_blank">https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper</a>
</li>
<li>
<a href="https://in.pinterest.com/pin/337277459600111737/" target="_blank">https://in.pinterest.com/pin/337277459600111737/</a>
</li>
<li>
<a href="https://quintagroup.com/cms/python/images/sqlalchemy-logo.png/view" target="_blank">https://quintagroup.com/cms/python/images/sqlalchemy-logo.png/view</a>
</li>
<li>
<a href="https://www.logo.wine/logo/MySQL" target="_blank">https://www.logo.wine/logo/MySQL</a>
</li>
<li>
<a href="https://icon-icons.com/download/170836/PNG/512/" target="_blank">https://icon-icons.com/download/170836/PNG/512/</a>
</li>
<li>
<a href="https://flask.palletsprojects.com/en/3.0.x/" target="_blank">https://flask.palletsprojects.com/en/3.0.x/</a>
</li>
</ul>