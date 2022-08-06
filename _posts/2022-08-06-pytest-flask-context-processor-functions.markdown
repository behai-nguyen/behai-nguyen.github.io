---
layout: post
title: "Python: pytest and Flask template context processor functions."

---

We have some functional pytest tests, e.g. tests which retrieve HTML contents. The generation of these HTML contents uses some Flask template context_processor functions. These functions are available to the Flask application instance which is created via the Application Factory pattern. How do we make these same context_processor functions available in the pytest application instance which is also created via the same Application Factory pattern? We're discussing this question, and also pytest application fixture and test client fixure.

| ![034-feature-image.png](https://behainguyen.files.wordpress.com/2022/08/034-feature-image.png) |
|:--:|
| *Python: pytest and Flask template context processor functions.* |

<p>
I had to write some 
<span class="keyword">
pytest</span> methods which make requests to routes. Some of these
requests return 
<span class="keyword">
HTML</span> contents. The generation of those contents uses 
<span class="keyword">
Flask template context_processor</span> 
functions. That is, functions which are 
decorated with:
</p>

```python
@app.context_processor
```

<p>
My tests failed since I haven't made these functions available to the
<span class="keyword">
pytest</span>'s 
<span class="keyword">
application fixture</span> yet. I searched for solutions, but
I could not find any... I tested out what I've thought might work, and
it does. 
</p>

<p>
To summarise, the 
<span class="keyword">
application fixture</span> function in the 
<span class="keyword">
pytest</span> module 
<span class="keyword">
conftest.py</span> must decorate the 
<span class="keyword">
pytest</span> application instance with the same 
<span class="keyword">
Flask template context_processor</span> functions. I.e.:
</p>

```
File D:\project_name\tests\conftest.py
```

```python
@pytest.fixture(scope='module')
def app():
    ...
    app = create_app()
    ...	
	
    app.app_context().push()
    """
    Making all custom template functions available 
	to the test application instance.
    """	
    from project_name.utils import context_processor

    return app
```

<p>
Basically, we create the test application instance using the 
Application Factory pattern function as per the real application
instance.
</p>

```python
app.app_context().push()
```

<p>
The above line makes a valid context for the test application instance.
Without a valid context, we'll get a working outside of the application 
context error message. It seems that with 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
app.app_context().push()</span> we have to call only once, then 
the context is available throughout, whereas with
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
app.app_context():</span>, the context is available only 
within the 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
with:</span>'s scope.
</p>

<p>
Then, the <span class="keyword">
import</span> call 
</p>

```python
from project_name.utils import context_processor
```

<p>
decorates the test application instance with all 
<span class="keyword">
Flask template context_processor</span> functions implemented in
module:
</p>

```
D:\project_name\src\project_name\utils\context_processor.py
```

<p>
That is the gist of it... I'm demonstrating this with a proper 
project and tests in the following sections. 
</p>

<p>✿✿✿</p>

<!--------------------------------------------------------------------------------->

<h2>Table of contents</h2>

<ul>
	<li style="margin-top:5px;"><a href="#initial-project-code">Initial project code</a></li>
	
	<li style="margin-top:10px;"><a href="#finished-project-layout">Project layout when completed</a></li>

	<li style="margin-top:10px;"><a href="#install-pytest-packages">Install required packages for pytest</a></li>

	<li style="margin-top:10px;"><a href="#echo-template-and-function">The echo.html template and the context_processor.py module</a>	
		<ul>
			<li style="margin-top:10px;"><a href="#html-echo-template">The echo.html template</a></li>

			<li style="margin-top:10px;"><a href="#context-processor-function">The context_processor.py module</a></li>
		</ul>
	</li>

	<li style="margin-top:10px;"><a href="#application-entry-point">The application entry point module app.py</a></li>

	<li style="margin-top:10px;"><a href="#controller-codes">The controller codes</a>
		<ul>
			<li style="margin-top:10px;"><a href="#controller-codes-package-module">The controller __init__.py module</a></li>

			<li style="margin-top:10px;"><a href="#controller-codes-echo-module">The controller echo.py module</a></li>
		</ul>
	</li>

	<li style="margin-top:10px;"><a href="#urls-factory-modules">The urls.py module and the factory pattern __init__.py module</a></li>

	<li style="margin-top:10px;"><a href="#the-tests">The tests</a>	
		<ul>
			<li style="margin-top:10px;"><a href="#pytest-entry-module">pytest entry module conftest.py</a>
				<ul>
				    <li style="margin-top:10px;"><a href="#pytest-app-fixture">The app() fixture</a></li>

				    <li style="margin-top:10px;"><a href="#pytest-test-client-fixture">The test_client( app ) fixture</a></li>				
				</ul>
			</li>

			<li style="margin-top:10px;"><a href="#The test_routes.py module">The test_routes.py module</a></li>
		</ul>
	</li>

	<li style="margin-top:10px;"><a href="#flask-latest-version-env">Flask latest version and .env file</a></li>

	<li style="margin-top:10px;"><a href="#synology-ds218-test">Synology DS218 tests</a></li>

	<li style="margin-top:10px;"><a href="#codes-download">Codes download</a></li>

	<li style="margin-top:10px;"><a href="#concluding-remarks">Concluding remarks</a></li>
</ul>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="initial-project-code">Initial project code</a>
</h3>

<p>
We'll be using the existing extremely simple 
<span class="keyword">app_demo</span>
project, which has been created for other previous posts. Please get it using:
</p>

```
git clone -b v1.0.0 https://github.com/behai-nguyen/app-demo.git
```

<p>
It has only a single route: 
<a href="http://localhost:5000/" title="http://localhost:5000/" target="_blank">http://localhost:5000/</a>
-- which displays 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
Hello, World!</span>
</p>

<p>
To recap, the layout of the project is:
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
We'll build another 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
/echo</span> route using 
<span class="keyword">
Flask Blueprint</span>, and write tests for all two ( 2 ) routes.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="finished-project-layout">Project layout when completed</a>
</h3>

<p>
The diagram below shows the project layout when completed.
Please note <span style="font-size:1.5em;">★</span> indicates 
new files, and <span style="font-size:1.5em;">☆</span> indicates 
files to be modified: 
</p>

```
D:\app_demo\
|
|-- .env ☆
|-- app.py ☆
|-- setup.py ☆
|-- pytest.ini ★
|
|-- src\
|   |
|   |-- app_demo\
|       |   
|       |-- __init__.py ☆
|       |-- config.py
|       |-- urls.py ★
|       |
|       |-- controllers\ ★
|       |   |
|       |   |-- __init__.py
|       |   |-- echo.py
|       |   
|       |-- utils\ ★
|       |   |
|       |   |-- __init__.py 
|       |   |-- context_processor.py
|       |   |-- functions.py
|       |
|       |-- templates\ ★
|       |   |
|       |   |-- base_template.html
|       |   |-- echo\
|       |   |   |
|       |   |   |--echo.html
|       
|-- tests ★
|   |
|   |-- conftest.py 
|   |-- functional\
|       |
|       |-- test_routes.py
|
|-- venv\
```

<p>
I've tested this project under 
<span class="keyword">
Synology DS218</span>,
<span class="keyword">
DSM 7.1-42661 Update 3</span>, running
<span class="keyword">
Python 3.9 Beta</span>; and 
<span class="keyword">
Windows 10 Pro</span>,
<span class="keyword">
version 10.0.19044 build 19044</span>, running 
<span class="keyword">
Python 3.10.1</span>.
</p>

<p>
The finished codes for this post can be downloaded using:
</p>

```
git clone -b v1.0.4 https://github.com/behai-nguyen/app-demo.git
```

<p>
Please note, the tag is <strong>v1.0.4</strong>. Please ignore all 
<span class="keyword">
Docker</span> related files.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="install-pytest-packages">Install required packages for pytest</a>
</h3>

<p>
We need packages 
<span class="keyword">
pytest</span> and 
<span class="keyword">
coverage</span>. Updated 
<a href="https://github.com/behai-nguyen/app-demo/blob/main/setup.py"
title="setup.py" target="_blank">setup.py</a> to include these two, 
then install the project in edit mode with:
</p>

```
(venv) D:\app_demo>venv\Scripts\pip.exe install -e .
(venv) behai@omphalos-nas-01:/volume1/web/app_demo$ sudo venv/bin/pip install -e .
```


<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="echo-template-and-function">The echo.html template and the context_processor.py module</a>
</h3>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="html-echo-template">The echo.html template</a>
</h4>

<p>
This is 
<a href="https://github.com/behai-nguyen/app-demo/blob/main/src/app_demo/templates/echo/echo.html"
title="echo.html in its entirety"
target="_blank">echo.html in its entirety</a>. It's pretty simple, 
just enough to demonstrate 
<span class="keyword">
Flask template context_processor</span> function 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
print_echo( request )</span>:
</p>

```
{% raw %}{% set echo = print_echo( request ) %}{% endraw %}
```

<p>
We store the value returned from 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
print_echo( request )</span> to template variable 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
echo</span>. Then we just print out the content of this variable.
If it is a 
<span class="keyword">
POST request</span>, then we print out the list of the key, value pairs
that've been submitted. The “Date Time” line is to make the HTML content
looks a bit dynamic.
</p>

<p>
To submit 
<span class="keyword">
POST requests</span> to
<a href="http://localhost:5000/echo"
title="http://localhost:5000/echo"
target="_blank">http://localhost:5000/echo</a> I'm using the 
<a href="https://www.postman.com/downloads/?utm_source=postman-home"
title="The Postman App" target="_blank">The Postman App</a> -- in the
<span class="keyword">
Body</span> tab, select 
<span class="keyword">
x-www-form-urlencoded</span>, and then enter data to be submitted 
into the provided list. Click 
<span class="keyword">
Send</span> -- we should see HTML responses come back in the 
response section below.
</p>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="context-processor-function">The context_processor.py module</a>
</h4>

<p>
This is 
<a href="https://github.com/behai-nguyen/app-demo/blob/main/src/app_demo/utils/context_processor.py"
title=""
target="_blank">context_processor.py in its entirety</a>. It has only
a single simple function. I don't think it would require any explanation. 
<strong>The key issue</strong>, in my understanding:
</p>

```python
...
from flask import current_app as app

@app.context_processor
def print_echo():
    def __print_echo( request ):
        ...
        return data

    return dict( print_echo=__print_echo )
```

<p>
We must use the 
<span class="keyword">
current_app</span> from 
<span class="keyword">
Flask</span>, since we decorate the 
<span class="keyword">
template function</span> with:
</p>

```python
@app.context_processor
def print_echo():
```

<p>
<span class="keyword">
current_app</span> is defined as:
</p>

>A proxy to the application handling the current request.

>https://flask.palletsprojects.com/en/2.1.x/api/#flask.current_app

<p>
It should make sense, since the application instance could be an 
instance of a development web server, or an instance from a 
<span class="keyword">
pytest</span> as we're currently discussing.
</p>

<p>
We understand that this is only a demo method, so we make up the
data for this purpose. For real applications, the data could come
from sources such as a database, computed data, etc. And also we
can have as many methods as we like.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="application-entry-point">The application entry point module app.py</a>
</h3>

<p>
As mentioned previously, context processor functions must be 
made available to the current running application instance. The 
<a href="https://github.com/behai-nguyen/app-demo/blob/main/app.py"
title="updated application entry point module app.py"
target="_blank">updated application entry point module app.py</a>:
</p>

```python
...
with app.app_context():
    from app_demo.utils import context_processor
```

<p>
loads up the context processor function discussed in 
<a href="#context-processor-function">The context_processor.py module</a>
for the current proper application instance just created. Please note:
</p>

```python
...
with app.app_context():
```

<p>
without the above call, it will result in 
<span class="keyword">
<span style="color:red;font-weight:bold;">RuntimeError: Working outside of application context.
</span></span> error.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="controller-codes">The controller codes</a>
</h3>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="controller-codes-package-module">The controller __init__.py module</a>
</h4>

<p>
<a href="https://github.com/behai-nguyen/app-demo/blob/main/src/app_demo/controllers/__init__.py" 
title="controllers\__init__.py" target="_blank">controllers\__init__.py</a>
defines a 
<span class="keyword">
Flask Blueprint</span> instance 
<span class="keyword">echo_blueprint</span>.
</p>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="controller-codes-echo-module">The controller echo.py module</a>
</h4>

<p>
The module 
<a href="https://github.com/behai-nguyen/app-demo/blob/main/src/app_demo/controllers/echo.py"
title="controllers\echo.py" target="_blank">controllers\echo.py</a>, has only a single
one-line function which just renders and returns the
<span class="keyword">
echo.html</span> template discussed in <a href="#html-echo-template">The echo.html template</a>.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="urls-factory-modules">The urls.py module and the factory pattern __init__.py module</a>
</h3>

<p>
<a href="https://github.com/behai-nguyen/app-demo/blob/main/src/app_demo/urls.py" 
title="app_demo\urls.py" target="_blank">app_demo\urls.py</a> defines a URL mapper
list, and a list of available 
<span class="keyword">
Flask Blueprint</span> instances. 
</p>

<p>
The 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
/echo</span> route supports both 
<span class="keyword">
GET</span> and 
<span class="keyword">
POST</span> request methods. And it is mapped to the 
<span class="keyword">echo_blueprint</span>
instance discussed in <a href="#controller-codes-package-module">Controller __init__.py module</a>,
and the response method which serves the HTML content is the 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
do_echo()</span> method discussed in 
<a href="#controller-codes-echo-module">Controller echo.py module</a>.
</p>

<p>
The Application Factory pattern module 
<a href="https://github.com/behai-nguyen/app-demo/blob/main/src/app_demo/__init__.py"
title="app_demo\__init__.py"
target="_blank">app_demo\__init__.py</a> has been updated to support the
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
/echo</span> route. The changes are extracted below:
</p>

```python
...
from app_demo.utils.functions import template_root_path

def create_app():
    app = Flask( 'dsm-python-demo', template_folder=template_root_path() )

    ...

    app.url_map.strict_slashes = False

    ...

    register_blueprints( app )

    ...

def register_blueprints( app ):
    ...
```

<p>
The application instance is now assigned 
<span class="keyword">
template_folder</span>. Turning off 
<span class="keyword">
strict_slashes</span> to make 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
/echo</span> and 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
/echo/</span> the same route. And finally calls to the new function 
<span class="keyword">
register_blueprints</span> to register 
<span class="keyword">
Flask Blueprint</span> instance(s) and URL(s) discussed above.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="the-tests">The tests</a>
</h3>

<p>
This is the main part of this post... It takes awhile go get here 😂.
</p>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="pytest-entry-module">pytest entry module conftest.py</a>
</h4>

<!--------------------------------------------------------------------------------->
<h5 style="color:teal;">
  <a id="pytest-app-fixture">The app() fixture</a>
</h5>

<p>
Let's look at the 
<a href="https://github.com/behai-nguyen/app-demo/blob/main/tests/conftest.py"
title="tests/conftest.py"
target="_blank">tests/conftest.py</a>:
</p>

```python
@pytest.fixture(scope='module')
def app():
    """
    Application fixure.	
    """
    app = create_app()
	
    app.app_context().push()
    """
    Making all custom template functions available 
	to the test application instance.
    """	
    from app_demo.utils import context_processor

    return app
```

<p>
The above method creates the test application instance using the
same Application Factory pattern as per the application proper.
It then creates a valid context for the test application instance
via calling 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
app.app_context().push()</span>. <strong>Next, which is what 
we have been trying to get at</strong> -- it 
loads up the context processor function discussed in 
<a href="#context-processor-function">The context_processor.py module</a>
for the test application instance just created. <strong>
This is exactly the same as for the application proper discussed in 
<a href="#application-entry-point">The application entry point module app.py</a>.
</strong>
</p>

<p>
Please note, for this post, none of the tests use this method directly,
however this will be the test structure that I follow from now on. Anyhow,
it will be used by the 
<span class="keyword">
test_client( app ) fixture</span> -- which we will look at next.
</p>

<!--------------------------------------------------------------------------------->
<h5 style="color:teal;">
  <a id="pytest-test-client-fixture">The test_client( app ) fixture</a>
</h5>

```python
@pytest.fixture(scope='module')
def test_client( app ):
    """
    Creates a test client.
	app.test_client() is able to submit HTTP requests.

    The app argument is the app() fixure above.	
    """
    with app.test_client() as testing_client:
        yield testing_client  # Return to caller.
```

<p>
The argument 
<span class="keyword">
app</span> which is the 
<span class="keyword">
app() fixture</span> who will get called automatically. <strong>
For me, personally, I think of 
</strong>
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
<strong>app.test_client()</strong></span>
<strong>as a web browser, 
a mini-<a href="https://www.postman.com/downloads/?utm_source=postman-home"
title="The Postman App" target="_blank">Postman</a>, etc., which enables
us to make</strong> 
<span class="keyword">
<strong>HTTP requests</strong></span>.
</p>

<p>
Since the <span class="keyword">
app() fixture</span> already comes with a context via calling 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
app.app_context().push()</span> itself, we can call 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
app.test_client()</span> without result in working outside of the 
application context error message.
</p>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="The test_routes.py module">The test_routes.py module</a>
</h4>

<p>
There's only a single test module --
<a href="https://github.com/behai-nguyen/app-demo/blob/main/tests/functional/test_routes.py"
title="functional\test_routes.py" 
target="_blank">functional\test_routes.py</a>:
</p>

```python
...
@pytest.mark.hello_world
def test_hello_world( test_client ):
    ...

@pytest.mark.echo
def test_echo_get_1( test_client ):
    ...

@pytest.mark.echo
def test_echo_get_2( test_client ):
    ...

@pytest.mark.echo
def test_echo_post( test_client ):
    ...
```

<p>
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
@pytest.mark.hello_world</span> and 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
@pytest.mark.echo</span> are optional -- which enable us to 
run specific tests rather than all tests:
</p>

```
(venv) D:\app_demo>venv\Scripts\pytest.exe -m echo
(venv) D:\app_demo>venv\Scripts\pytest.exe -m hello_world
(venv) behai@omphalos-nas-01:/volume1/web/app_demo$ venv/bin/pytest -m echo
(venv) behai@omphalos-nas-01:/volume1/web/app_demo$ venv/bin/pytest -m hello_world
```

<p>
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
hello_world</span> and 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
echo</span> are defined in the 
<a href="https://github.com/behai-nguyen/app-demo/blob/main/pytest.ini" 
title="pytest.ini" target="_blank">pytest.ini</a> config file.
</p>

<p>
The argument 
<span class="keyword">
test_client</span> to all test methods is 
<a href="#pytest-test-client-fixture">The test_client( app ) fixture</a> 
discussed previously. Test methods make use of 
its 
<span class="keyword">
get()</span> and <span class="keyword">
post()</span> methods to make requests, and then look into HTML responses 
for specific texts which we expected to be in the responses.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="flask-latest-version-env">Flask latest version and .env file</a>
</h3>

<p>
I did un-install 
<span class="keyword">
Flask</span> to get the latest version installed. The latest version 
gives this warning:
</p>

```
'FLASK_ENV' is deprecated and will not be used in Flask 2.3. Use 'FLASK_DEBUG' instead.
```

<p>
Environment file 
<a href="https://github.com/behai-nguyen/app-demo/blob/main/.env"
title=".env" target="_blank">.env</a> has been updated with 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
FLASK_DEBUG=True</span> to get rid of the warning.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="synology-ds218-test">Synology DS218 tests</a>
</h3>

<p>
As mentioned before, this project works under 
<span class="keyword">
Linux</span>:
</p>

![034-01-synology-test.png](https://behainguyen.files.wordpress.com/2022/08/034-01-synology-test.png)

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="codes-download">Codes download</a>
</h3>

<p>
To recap, the codes for this post can be downloaded using:
</p>

```
git clone -b v1.0.4 https://github.com/behai-nguyen/app-demo.git
```

<p>
Please note, the tag is <strong>v1.0.4</strong>. Please ignore all 
<span class="keyword">
Docker</span> related files.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="concluding-remarks">Concluding remarks</a>
</h3>

<p>
I have enjoyed working on this project. Particularly explaining
the 
<span class="keyword">
app() fixture</span> and the 
<span class="keyword">
test_client( app ) fixture</span> in my own words. I have found 
these two a bit difficult to understand when I first looked at 
<span class="keyword">
pytest</span>.
</p>

<p>
Successfully applying 
<span class="keyword">
Flask template context_processor</span> functions to the test 
application instance is also satisfied.
</p>

<p>
Most of all, I hope this information can help somebody down the track.
I hope you find this useful... and thank you for reading.
</p>
