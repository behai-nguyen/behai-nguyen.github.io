---
layout: post
title: "Python FastAPI: Enabling Database Support"

description: Continuing with our Python FastAPI learning series, in this installment, we enable database support for MySQL, PostgreSQL, and MariaDB. We will not add any new functionality; instead, the existing authentication process will check user information from a proper database instead of mock hard-coded data. We will also add a business logic layer responsible for data validation, enforcing business rules, etc. 

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/08/119-02.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/08/119-03.png"

tags:
- Python
- FastAPI
- Database
- MySQL
- PostgreSQL
- MariaDB
---

<em>
Continuing with our <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Python FastAPI Complete Series" target="_blank">Python FastAPI learning series</a>, in this installment, we enable database support for <a href="https://www.mysql.com/" title="MySQL database" target="_blank">MySQL</a>, <a href="https://www.postgresql.org/" title="PostgreSQL database" target="_blank">PostgreSQL</a>, and <a href="https://mariadb.com/" title="MariaDB database" target="_blank">MariaDB</a>. We will not add any new functionality; instead, the existing authentication process will check user information from a proper database instead of mock hard-coded data. We will also add a business logic layer responsible for data validation, enforcing business rules, etc.
</em>

<h3>
🐍 <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![119-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/08/119-feature-image.png) |
|:--:|
| *Python FastAPI: Enabling Database Support* |

<p>
The code requires Python 3.12.4. Please refer to the 
<a href="https://github.com/behai-nguyen/fastapi_learning#the-code-after-tag-v040-requires-python-3124" 
title="The Code After Tag v0.4.0 Requires Python 3.12.4" target="_blank">following 
discussion</a> on how to upgrade to Python 3.12.4.
</p>

<p>
🚀 <strong>Please note,</strong> complete code for this post
can be downloaded from GitHub with:
</p>

```
git clone -b v0.7.0 https://github.com/behai-nguyen/fastapi_learning.git
```

<a id="new-feature"></a>
❶ In this post, we implement database support for the following databases: 
<a href="https://www.mysql.com/" title="MySQL database" target="_blank">MySQL</a>,
<a href="https://www.postgresql.org/" title="PostgreSQL database" target="_blank">PostgreSQL</a>, 
and <a href="https://mariadb.com/" title="MariaDB database" target="_blank">MariaDB</a>. 
In this revision of the code, we limit database operations to only logging in. That is, we are not adding any new functionality; instead, we remove the hard-coded mock data and use proper databases.

<a id="new-feature-crud"></a>
We also make provisional plans for the application to do full CRUD operations later on. 
We have already implemented the 
<a href="https://github.com/behai-nguyen/fastapi_learning/tree/cc6a59a36ea9a21373bb3f69b3bc2ef36811df9e/src/fastapi_learning/controllers" 
title="The controllers layer" target="_blank"><code>controllers</code></a>
layer, and the 
<a href="https://github.com/behai-nguyen/fastapi_learning/tree/cc6a59a36ea9a21373bb3f69b3bc2ef36811df9e/src/fastapi_learning/models"
title="The models or database layer" target="_blank"><code>models</code></a> or 
<code>database</code> layer. 
We are going to have a new business logic layer (<code>./businesses</code>), 
which will sit between the <code>controllers</code> and the <code>models</code> layers. 
Please see the diagram below:

![119-01-app-layers.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/08/119-01-app-layers.png)

<a id="new-feature-ctrlr"></a>
⓵ The <code>controllers</code> layer: As we have already seen, this is where all the endpoint method handlers are implemented, and where all JSON and HTML responses are constructed and returned.

👉 Please note that HTML responses are technically <code>views</code>, 
which is another layer in the 
<a href="https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller" 
title="Model–view–controller software design pattern" 
target="_blank">Model–view–controller</a> software design pattern. The 
<a href="https://github.com/behai-nguyen/fastapi_learning/tree/cc6a59a36ea9a21373bb3f69b3bc2ef36811df9e/src/fastapi_learning/templates" 
title="The templates area" target="_blank">templates</a> area can be thought of as 
the <code>view</code> layer.

<a id="new-feature-ctrlr-data-injection"></a>
The endpoint method handlers might inject some custom data into the incoming request data. 
They call methods in the <code>./businesses</code> area to do all the necessary work.

<a id="new-feature-bus"></a>
⓶ The business (<code>./businesses</code>) logic layer: Methods in this layer will first carry out basic data validation on the submitted data. If there is any error, it will send back an error response, and that will be the end of the request. Otherwise, it will next carry out business rules validation and any required calculations on the submitted data. If a failure occurs, it will respond with an error as in the first step.

Finally, it will call methods in the <code>models</code></a> or <code>database</code> layer to perform CRUD operations on the final data. CRUD operations could also result in either a successful response or a failure one.

<a id="new-feature-models"></a>
⓷ The <code>models</code> or <code>database</code> layer: A model is a database table, and it includes all CRUD methods necessary to operate this table. This layer does not have any logic or intelligence; it receives some data and communicates with the target database to carry out CRUD operations on the given data.

👉 Please note, this pattern is also used in the two 
<a href="https://github.com/behai-nguyen/bh_database/tree/main/examples" 
title="bh-database examples" target="_blank">examples</a> provided for the 
<a href="https://pypi.org/project/bh-database/" title="bh-database" 
target="_blank">bh-database</a> wrapper classes for SQLAlchemy. The code for the business layer is, in fact, taken from these two examples.

<a id="the-databases"></a>
❷ The source database is the <code>MySQL test data</code> released by Oracle Corporation, 
downloadable from this <a href="https://github.com/datacharmer/test_db" 
title="MySQL test data " target="_blank">GitHub repository</a>. The <code>employees</code> 
table does not have the <code>email</code> and <code>password</code> columns, so we 
have to create and populate them ourselves. Let’s start with the source database.

<a id="the-db-mysql"></a>
● MySQL <span style="font-size:1.2em;">🐬</span> is the source or starting 
database. There are two ways to create and populate the <code>email</code> 
and <code>password</code> columns:

<ol>
<li style="margin-top:10px;">
A more involved and proper method is discussed in the section 
<a href="https://behainguyen.wordpress.com/2024/01/14/rust-actix-web-endpoints-which-accept-both-application-x-www-form-urlencoded-and-application-json-content-types/#step-two-update-employees-table" 
title="Add new fields email and password to the employees table" 
target="_blank">Add new fields <code>email</code> and <code>password</code> to the 
<code>employees</code> table</a> of a Rust post. It does not involve coding in Rust, 
but uses a Rust-related tool.
</li>

<li style="margin-top:10px;">
A shortcut method is to run the following script
<a href="https://github.com/behai-nguyen/rust_web_01/blob/41734efbfe31ada987d9e19694e487d532230691/migrations/mysql/migrations/20231128234321_emp_email_pwd.up.sql" 
title="Add new fields email and password to the employees table" 
target="_blank">20231128234321_emp_email_pwd.up.sql</a> on the source database.
</li>
</ol>

<a id="the-db-postgresql"></a>
● To create an equivalent PostgreSQL <span style="font-size:1.2em;">🐘</span> 
database from a MySQL database, my preferred method is discussed in the post 
<a href="https://behai-nguyen.github.io/2022/11/12/mysql-to-postgresql-using-pgloader-docker.html" 
title="pgloader Docker: migrating from Docker & localhost MySQL to localhost PostgreSQL" 
target="_blank">pgloader Docker: migrating from Docker & localhost MySQL to localhost PostgreSQL</a>.
You can use whatever method you feel comfortable with.

<a id="the-db-mariadb"></a>
● To create an equivalent MariaDB <span style="font-size:1.6em;">🦭</span> database 
from a MySQL database, use MySQL tools. I backed up a MySQL database and restored 
the backup content to a MariaDB database. We have discussed this in a 
<a href="https://behainguyen.wordpress.com/2024/07/28/python-mariadb-which-driver-an-example-of-executing-a-stored-procedure-that-returns-multiple-result-sets/" 
title="Python & MariaDB: Which Driver? An Example of Executing a Stored Procedure That Returns Multiple Result Sets" 
target="_blank">previous post</a>.

<a id="project-layout"></a>
❸ The full updated structure of the project is outlined below. 

<strong>-- Please note,</strong> those marked with <span style="font-size:1.5em;">★</span> 
are updated, and those marked with <span style="font-size:1.5em;">☆</span> are new.

```
/home/behai/fastapi_learning/
.
├── cert
│   ├── cert.pem
│   └── key.pem
├── .env
├── logger_config.yaml
├── main.py ★
├── pyproject.toml ★
├── pytest.ini ★
├── README.md ★
├── src
│   └── fastapi_learning
│       ├── businesses ☆
│       │   ├── app_business.py
│       │   ├── base_business.py
│       │   ├── base_validation.py
│       │   ├── employees_mgr.py
│       │   └── employees_validation.py
│       ├── common
│       │   ├── consts.py ★
│       │   └── queue_logging.py
│       ├── controllers
│       │   ├── admin.py ★
│       │   ├── auth.py ★
│       │   └── __init__.py ★
│       ├── __init__.py
│       ├── models
│       │   └── employees.py ★
│       ├── static
│       │   └── styles.css
│       └── templates
│           ├── admin
│           │   └── me.html ★
│           ├── auth
│           │   ├── home.html
│           │   └── login.html
│           └── base.html
└── tests
    ├── business ☆
    │   └── test_employees_mgr.py
    ├── conftest.py
    ├── __init__.py
    ├── integration
    │   ├── test_admin_itgt.py ★
    │   ├── test_api_itgt.py ★
    │   └── test_auth_itgt.py ★
    ├── README.md
    └── unit ☆
        └── test_employees.py
```

<a id="code-refactorings"></a>
❹ In this section, we will discuss the code changes.

<a id="code-refac-env"></a>
⓵ In the last check-in of the environment 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/main/.env#L9-L12" 
title="The environment file .env" target="_blank"><code>.env</code> file</a>, 
we have already included the database connection information:

<figure class="highlight"><pre><code class="language-cfg" data-lang="cfg"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">9
10
11
12
</pre></td><td class="code"><pre>SQLALCHEMY_DATABASE_SCHEMA = employees
SQLALCHEMY_DATABASE_URI = mysql+mysqlconnector://root:pcb.2176310315865259@localhost:3306/employees
# Enable this for PostgreSQL.
# SQLALCHEMY_DATABASE_URI = postgresql+psycopg2://postgres:pcb.2176310315865259@localhost/employees
</pre></td></tr></tbody></table></code></pre></figure>

As discussed in <a href="https://behainguyen.wordpress.com/2024/07/28/python-mariadb-which-driver-an-example-of-executing-a-stored-procedure-that-returns-multiple-result-sets/" 
title="Python & MariaDB: Which Driver? An Example of Executing a Stored Procedure That Returns Multiple Result Sets" 
target="_blank">this post</a>, the MariaDB database connection string is identical to MySQL. Just substitute the connection information. I added the MariaDB entry locally, and I did not check it in.

<a id="code-refac-pyproj"></a>
⓶ The 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/pyproject.toml#L27-L32" 
title="The pyproject.toml file" target="_blank"><code>pyproject.toml</code></a> 
file now includes the following required packages:

● <a href="https://werkzeug.palletsprojects.com/en/3.0.x/" title="werkzeug" target="_blank">werkzeug</a>: We need the <code>datastructures.MultiDict</code> class.

● <a href="https://pypi.org/project/python-dotenv/" title="python-dotenv" target="_blank">python-dotenv</a>: To load the environment file <code>.env</code> into environment variables.

● <a href="https://wtforms.readthedocs.io/en/3.1.x/" title="wtforms" target="_blank">wtforms</a>: We use the data validation feature to validate the HTTP submitted data.

● <a href="https://bh-database.readthedocs.io/en/latest/" title="bh-database" target="_blank">bh-database</a>: Provides some convenient classes to perform CRUD operations on database tables. As mentioned <a href="#new-feature">previously</a>, we support MySQL, PostgreSQL, and MariaDB. That is the reason why we include both <code>mysql-connector-python</code> and <code>psycopg2-binary</code>.

● <a href="https://pypi.org/project/bh-apistatus/" title="bh_apistatus" target="_blank">bh_apistatus</a>: Provides some convenient classes to wrap returned results from method calls.

<a id="code-refac-main"></a>
⓷ Within the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/main.py#L48-L59" 
title="The main.py module" target="_blank"><code>main.py</code></a> module, 
in <code>async def lifespan(app: FastAPI)</code>, 
we establish a connection to the database. If the connection fails, we raise a 
<a href="https://docs.python.org/3/library/exceptions.html#RuntimeError" 
title="exception RuntimeError" target="_blank">RuntimeError</a> exception 
and terminate the application:

<figure class="highlight"><pre><code class="language-python" data-lang="python"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">48
49
50
51
52
53
54
55
56
57
58
59
</pre></td><td class="code"><pre>    <span class="n">Database</span><span class="p">.</span><span class="n">disconnect</span><span class="p">()</span>

    <span class="c1"># It is the responsibility of the caller to handle this exception.
</span>    <span class="k">try</span><span class="p">:</span>
        <span class="n">Database</span><span class="p">.</span><span class="n">connect</span><span class="p">(</span><span class="n">os</span><span class="p">.</span><span class="n">environ</span><span class="p">.</span><span class="n">get</span><span class="p">(</span><span class="s">'SQLALCHEMY_DATABASE_URI'</span><span class="p">),</span> 
                         <span class="n">os</span><span class="p">.</span><span class="n">environ</span><span class="p">.</span><span class="n">get</span><span class="p">(</span><span class="s">'SQLALCHEMY_DATABASE_SCHEMA'</span><span class="p">))</span>
    <span class="k">except</span> <span class="nb">Exception</span> <span class="k">as</span> <span class="n">e</span><span class="p">:</span>
        <span class="n">logger_fn</span><span class="p">.</span><span class="n">exception</span><span class="p">(</span><span class="nb">str</span><span class="p">(</span><span class="n">e</span><span class="p">))</span>
        <span class="n">logger_fn</span><span class="p">.</span><span class="n">error</span><span class="p">(</span><span class="s">'Attempt to terminate the application now.'</span><span class="p">)</span>
        <span class="c1"># raise RuntimeError(...) flushes any pending loggings and 
</span>        <span class="c1"># also terminates the application.        
</span>        <span class="k">raise</span> <span class="nb">RuntimeError</span><span class="p">(</span><span class="s">'Failed to connect to the target database.'</span><span class="p">)</span>
</pre></td></tr></tbody></table></code></pre></figure>

Please note that, prior to establishing the database connection, the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/main.py#L74" 
title="The main.py module" target="_blank"><code>main.py</code></a> 
module has already loaded the environment <code>.env</code> file:

<figure class="highlight"><pre><code class="language-python" data-lang="python"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">74
</pre></td><td class="code"><pre><span class="n">load_dotenv</span><span class="p">(</span> <span class="n">os</span><span class="p">.</span><span class="n">path</span><span class="p">.</span><span class="n">join</span><span class="p">(</span><span class="n">os</span><span class="p">.</span><span class="n">getcwd</span><span class="p">(),</span> <span class="s">'.env'</span><span class="p">)</span> <span class="p">)</span>
</pre></td></tr></tbody></table></code></pre></figure>

<a id="code-refac-emp-mod"></a>
⓸ The 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/models/employees.py" 
title="The employees.py module" target="_blank"><code>employees.py</code></a> 
module has been completely rewritten. All mock data and existing models were removed. It now has the following new classes:

● <a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/models/employees.py#L26-L48" 
title="The Employees class" target="_blank"><code>class Employees(WriteCapableTable)</code></a>: 
Represents the <code>employees</code> database table. 

● <a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/models/employees.py#L50-L62" 
title="The LoggedInEmployee class" target="_blank"><code>class LoggedInEmployee(BaseModel)</code></a>: 
The equivalent of the removed class 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/cc6a59a36ea9a21373bb3f69b3bc2ef36811df9e/src/fastapi_learning/models/employees.py#L24-25" 
title="The UserInDB class" target="_blank"><code>class UserInDB(User)</code></a> 
in the tutorial’s original example.

Please note that having both a 
<a href="https://www.sqlalchemy.org/" title="SQLAlchemy" target="_blank">SQLAlchemy</a> 
model and a Pydantic “logical” model is also demonstrated in the official documentation page 
<a href="https://docs.pydantic.dev/1.10/usage/models/" 
title="Pydantic Models" target="_blank">Pydantic Models</a>.

<a id="code-refac-bus"></a>
⓹ We now describe each module within the business logic 
(<a href="https://github.com/behai-nguyen/fastapi_learning/tree/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/businesses" 
title="The businesses layer" target="_blank"><code>./businesses</code></a>) layer: 

<a id="code-refac-bus-base-bus"></a>
● <a href="https://github.com/behai-nguyen/fastapi_learning/tree/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/businesses/base_business.py" 
title="The base_business.py module" target="_blank"><code>base_business.py</code></a>: 
Implements an abstract class. The core functionality is the template 
<a href="https://github.com/behai-nguyen/fastapi_learning/tree/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/businesses/base_business.py#L313-L365" 
title="The template write_to_database(...) method" target="_blank"><code>def write_to_database(self, data)</code></a>, 
which implements a consistent approach to data validation, data calculation, and finally 
writing the data to the database. This template method calls other abstract methods to 
perform each of the mentioned tasks. 
Descendant classes must implement all these abstract methods. If a method is not required, 
it should just return a 
<a href="https://bh-apistatus.readthedocs.io/en/latest/result-status.html#bh_apistatus.result_status.make_status" 
title="make_status() result" target="_blank">make_status()</a> result.

<a id="code-refac-bus-app-bus"></a>
● <a href="https://github.com/behai-nguyen/fastapi_learning/tree/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/businesses/app_business.py" 
title="The app_business.py module" target="_blank"><code>app_business.py</code></a>: 
Provides a common parent business class for all application business logic classes. 
This module implements the <code>AppBusiness</code> class, which is a direct descendant 
of the above <a href="#code-refac-bus-base-bus"><code>BaseBusiness</code></a> class. 
<code>AppBusiness</code> implements all abstract methods mentioned above to simply return 
a <a href="https://bh-apistatus.readthedocs.io/en/latest/result-status.html#bh_apistatus.result_status.make_status" 
title="make_status() result" target="_blank">make_status()</a> result.

<a id="code-refac-bus-base-val"></a>
● <a href="https://github.com/behai-nguyen/fastapi_learning/tree/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/businesses/base_validation.py" 
title="The base_validation.py module" target="_blank"><code>base_validation.py</code></a>: 
Implements the following:

<ol>
<li style="margin-top:10px;">
The application common 
<a href="https://github.com/behai-nguyen/fastapi_learning/tree/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/businesses/base_validation.py#L40-L113" 
title="The BaseValidationForm class" target="_blank"><code>BaseValidationForm</code></a>
class: Wraps the <a href="https://wtforms.readthedocs.io/en/3.1.x/forms/#the-form-class" 
title="The wtforms Form class" target="_blank">wtforms' <code>Form</code></a> class and 
provides additional capabilities such as label substitution and field re-ordering.
</li>

<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/fastapi_learning/tree/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/businesses/base_validation.py#L116-L147" 
title="The base_validation.py module" target="_blank"><code>def validate(data: dict, forms: list) -> ResultStatus</code></a>: 
Validates the data coming from the <code>controllers</code> layer as 
<a href="#new-feature-ctrlr-data-injection">described previously</a>.
</li>
</ol>

<a id="code-refac-bus-emp-val"></a>
● <a href="https://github.com/behai-nguyen/fastapi_learning/tree/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/businesses/employees_validation.py" 
title="The employees_validation.py module" target="_blank"><code>employees_validation.py</code></a>: It should be self-explanatory.

<a id="code-refac-bus-emp-mgr"></a>
● <a href="https://github.com/behai-nguyen/fastapi_learning/tree/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/businesses/employees_mgr.py" 
title="The employees_mgr.py module" target="_blank"><code>employees_mgr.py</code></a>: 
Responsible for managing data and business logic associated with the <code>employees</code> table. 

In this revision of the code, it has only two public methods: a method 
<a href="https://github.com/behai-nguyen/fastapi_learning/tree/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/businesses/employees_mgr.py#L55-L91" 
title="The employees_mgr.py select_by_email method" target="_blank">to retrieve</a> 
a specific employee by email, and a method 
<a href="https://github.com/behai-nguyen/fastapi_learning/tree/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/businesses/employees_mgr.py#L93-L141" 
title="The employees_mgr.py login method" target="_blank">to log in</a> 
an employee using an email and a password. These methods implement all basic data validations; presently, there are no business logics.

We are not yet writing new records into the <code>employees</code> table. However, we 
implement the abstract methods provided by the <a href="#code-refac-bus-app-bus"><code>AppBusiness</code></a> 
class, even though they are not in use yet. This is part of the CRUD provisional plans 
<a href="#new-feature-crud">previously mentioned</a>.

<a id="code-refac-ctrlr"></a>
⓺ The changes in each of the existing 
<a href="https://github.com/behai-nguyen/fastapi_learning/tree/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/controllers" 
title="The controllers layer" target="_blank"><code>controllers</code></a> 
modules are discussed in the sections below: 

<a id="code-refac-ctrlr-auth"></a>
● <a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/controllers/auth.py" 
title="The auth.py module" target="_blank"><code>auth.py</code></a>: All mock code 
has been removed. Most importantly, in the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/controllers/auth.py#L96-L167" 
title="The login endpoint handler method" target="_blank"><code>login(...)</code></a> 
endpoint handler method, we call the 
<a href="https://github.com/behai-nguyen/fastapi_learning/tree/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/businesses/employees_mgr.py#L93-L141" 
title="The employees_mgr.py login method" target="_blank"><code>EmployeesManager.login(...)</code></a> 
method to serve the login request as <a href="#code-refac-bus-emp-mgr">described previously</a>.

<a id="code-refac-ctrlr-admin"></a>
● <a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/controllers/admin.py" 
title="The admin.py module" 
target="_blank"><code>admin.py</code></a>: All mock code has been removed. There are two important refactorings:

<ol>
<li style="margin-top:10px;">
In the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/controllers/admin.py#L51-L77" 
title="The admin.py get_current_user method" 
target="_blank"><code>get_current_user(...)</code></a> method, we call the 
<a href="https://github.com/behai-nguyen/fastapi_learning/tree/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/businesses/employees_mgr.py#L55-L91" 
title="The employees_mgr.py select_by_email method" 
target="_blank"><code>EmployeesManager.select_by_email(...)</code></a> 
method to retrieve the currently logged-in user (employee) information. We could have cached this information in the web session and retrieved it from there. However, the logged-in user can update their information after logging in. Reading the information from the database will always provide the most up-to-date information. 
<br><br>
<a id="code-refac-ctrlr-admin-username-issue"></a>
💥 We need to consider whether or not to allow the logged-in user to change their email. Right now, the email is the <code>username</code>. If they are able to change their email after logging in, then this call will fail. This would be the most embarrassing failure.
</li>

<li style="margin-top:10px;">
<a id="code-refac-ctrlr-admin-username-issue-handled"></a>
In the
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/controllers/admin.py#L84-L141" 
title="The admin.py read_users_me endpoint handler method" 
target="_blank"><code>read_users_me(...)</code></a> endpoint handler method, 
we handle the error where the logged-in user
<a href="#code-refac-ctrlr-admin-username-issue">could not retrieve</a> their information.
In this case, instead of passing a dictionary that represents the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/models/employees.py#L50-L62" 
title="The LoggedInEmployee class" target="_blank"><code>class LoggedInEmployee(BaseModel)</code></a> 
class to the template, we pass an error dictionary instead.
</li>
</ol>

<a id="code-refac-ctrlr-init"></a>
● <a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/controllers/__init__.py" 
title="The __init__.py module" target="_blank"><code>__init__.py</code></a>: 
We made the following additions:

<ol>
<a id="code-refac-ctrlr-init-tmpl"></a>
<li style="margin-top:10px;">
Added the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/controllers/__init__.py#L16-L28" 
title="The __init__.py valid_logged_in_employee template" 
target="_blank"><code>valid_logged_in_employee(...)</code></a> template method.
Please refer to the discussions on the potential issue with enabling the logged-in user 
<a href="#code-refac-ctrlr-admin-username-issue">to update their email</a>, and how 
we <a href="#code-refac-ctrlr-admin-username-issue-handled">pre-emptively handle</a> 
this potential issue. This new method is called by the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/templates/admin/me.html" 
title="The admin/me.html template" target="_blank"><code>admin/me.html</code></a> 
template to check if the context dictionary represents a logged-in employee or an error condition.
</li>

<a id="code-refac-ctrlr-init-hlpr"></a>
<li style="margin-top:10px;">
Added the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/controllers/__init__.py#L37-L41" 
title="The __init__.py is_logged_in helper method" 
target="_blank"><code>is_logged_in(...)</code></a> helper method. 
This is the previous 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/cc6a59a36ea9a21373bb3f69b3bc2ef36811df9e/src/fastapi_learning/controllers/auth.py#L64-L65"
title="The auth.py module __is_logged_in method" 
target="_blank"><code>__is_logged_in(...)</code></a> method.
</li>
</ol>

<a id="code-refac-tmplt"></a>
⓻ In the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/templates" 
title="The templates layer" target="_blank"><code>templates</code></a> layer, 
we made changes only to the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/templates/admin/me.html" 
title="The admin/me.html template" target="_blank"><code>admin/me.html</code></a> template.
Please refer to the 
<a href="#code-refac-ctrlr-init-tmpl">previous discussion</a> for details on what the changes were.

<a id="code-refac-test-unit"></a>
⓼ The new 
<a href="https://github.com/behai-nguyen/fastapi_learning/tree/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/tests/unit" 
title="tests/unit" target="_blank"><code>tests/unit</code></a> directory: 
Tests the <code>models</code></a> or <code>database</code> layer modules. Presently 
there is only a single 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/models/employees.py" 
title="The employees.py module" target="_blank"><code>employees.py</code></a> module.
The two test methods should be self-explanatory.

<a id="code-refac-test-bus"></a>
⓽ The new 
<a href="https://github.com/behai-nguyen/fastapi_learning/tree/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/tests/business" 
title="tests/business" 
target="_blank"><code>tests/business</code></a> directory: Contains tests for the 
business logic layer (<code>./businesses</code>). There are only tests for the 
<a href="https://github.com/behai-nguyen/fastapi_learning/tree/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/businesses/employees_mgr.py" 
title="The employees_mgr.py module" target="_blank"><code>employees_mgr.py</code></a>
module. Since this module utilises every other module under this layer, its tests effectively cover every other module as well.

The tests are long because we test all possible code paths. However, the tests are independent and should be easy to read.

<a id="code-refac-test-itgt"></a>
⓾ The existing 
<a href="https://github.com/behai-nguyen/fastapi_learning/tree/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/tests/integration" 
title="tests/integration" 
target="_blank"><code>tests/integration</code></a> directory: All existing tests remain in place with minor updates to the test conditions, field names renamed, and new fields added.

We added the following new tests to the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/tests/integration/test_auth_itgt.py" 
title="The integration test_auth_itgt.py module" target="_blank"><code>test_auth_itgt.py</code></a> 
module <code>test_integration_login_bad_email_html(...)</code>, 
<code>test_integration_login_bad_email_json(...)</code>, and 
<code>test_integration_login_bad_password_json(...)</code>.

🚀 It should be noted that tests under the <code>tests/business</code> layer 
and <code>tests/integration</code> can overlap since the <code>controllers</code> 
layer just calls the business logic layer (<code>./businesses</code>).
<strong>If we want to exclude overlapping tests, we should exclude tests from the 
<code>tests/integration</code> directory, never from the <code>tests/business</code> 
directory.</strong>

❺ The Swagger UI and our existing custom UIs are still functioning as they did in previous revisions. Please see the two illustrated screenshots below:

{% include image-gallery.html list=page.gallery-image-list %}
<br/>

<a id="concluding-remarks"></a>
❻ We conclude our discussions. We now have the database support in place. We will implement database writing in a future revision. I am not sure what we will discuss next in this series, but there are certainly a few more topics that I would like to explore.

Thank you for reading. I hope you find the information in this post useful. Stay safe, as always.

✿✿✿

Feature image source:

<ul>
<li>
<a href="https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper" target="_blank">https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper</a>
</li>
<li>
<a href="https://in.pinterest.com/pin/337277459600111737/" target="_blank">https://in.pinterest.com/pin/337277459600111737/</a>
</li>
<li>
<a href="https://www.python.org/downloads/release/python-3124/" target="_blank">https://www.python.org/downloads/release/python-3124/</a>
</li>
<li>
<a href="https://fastapi.tiangolo.com/" target="_blank">https://fastapi.tiangolo.com/</a>
</li>
<li>
<a href="https://1000logos.net/download-image/" target="_blank">https://1000logos.net/download-image/</a>
</li>
<li>
<a href="https://www.logo.wine/logo/MySQL" target="_blank">https://www.logo.wine/logo/MySQL</a>
</li>
<li>
<a href="https://icon-icons.com/download/170836/PNG/512/" target="_blank">https://icon-icons.com/download/170836/PNG/512/</a>
</li>
<li>
<a href="https://www.stickpng.com/img/icons-logos-emojis/tech-companies/mariadb-full-logo" target="_blank">https://www.stickpng.com/img/icons-logos-emojis/tech-companies/mariadb-full-logo</a>
</li>
</ul>

<h3>
🐍 <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>
