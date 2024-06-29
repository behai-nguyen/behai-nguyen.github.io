---
layout: post
title: "Python FastAPI: Complete Authentication Flow with OAuth2 Security"

description: In the third post, we implemented persistent stateful HTTP sessions. In this post, we will complete the application’s authentication UI flow. For the existing /auth/token and /admin/me routes, we will add functionality to conditionally return either HTML or JSON. Based on this new functionality, we will implement two new routes&#58; /api/login and /api/me. These routes will only return JSON, and their endpoint handlers will be the same as those of the aforementioned routes respectively. 

tags:
- Python 
- FastAPI
- OAuth2
- Authentication
- Flow
---

<em>In the <a href="https://behainguyen.wordpress.com/2024/05/21/python-fastapi-implementing-persistent-stateful-http-sessions-with-redis-session-middleware-and-extending-oauth2passwordbearer-for-oauth2-security/" title="Python FastAPI: Implementing Persistent Stateful HTTP Sessions with Redis Session Middleware and Extending OAuth2PasswordBearer for OAuth2 Security" target="_blank">third post</a>, we implemented persistent stateful HTTP sessions. In this post, we will complete the application’s authentication UI flow. For the existing <code>/auth/token</code> and <code>/admin/me</code> routes, we will add functionality to conditionally return either HTML or JSON. Based on this new functionality, we will implement two new routes: <code>/api/login</code> and <code>/api/me</code>. These routes will only return JSON, and their endpoint handlers will be the same as those of the aforementioned routes respectively.</em>

<h3>
🐍 <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![110-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/06/110-feature-image.png) |
|:--:|
| *Python FastAPI: Complete Authentication Flow with OAuth2 Security* |

🚀 <strong>Please note,</strong> complete code for this post can be downloaded from GitHub with:

```
git clone -b v0.4.0 https://github.com/behai-nguyen/fastapi_learning.git
```

<h2>Table of Contents</h2>

<ul style="list-style: none;">
<li style="margin-top:10px;">
<a href="#new-functionality">❶ New Functionality and Routes Summary</a>
</li>
<li style="margin-top:10px;">
<a href="#project-layout">❷ Project Layout</a>
</li>
<li style="margin-top:10px;">
<a href="#impl-html-json-response">❸ Implementation of Conditional HTML and JSON Response</a>
</li>
<li style="margin-top:10px;">
<a href="#app-auth-ui-flow">❹ Completion of the Application Authentication UI Flow</a>
</li>
<li style="margin-top:10px;">
<a href="#refactor-password-matching">❺ Implementation of a Production-Grade Password Hashing and Matching</a>
</li>
<li style="margin-top:10px;">
<a href="#integration-tests">❻ Integration Tests</a>
</li>
<li style="margin-top:10px;">
<a href="#running-the-app">❼ Preparation to Run the Example Application and UI Discussion</a>
</li>
<li style="margin-top:10px;">
<a href="#concluding-remarks">❽ Concluding Remarks</a>
</li>
</ul>

<a id="new-functionality"></a>
❶ Continuing from the introduction above, after the completion of this post, 
our <a href="https://fastapi.tiangolo.com/learn/" title="FastAPI" target="_blank">FastAPI</a> 
learning application will be capable of functioning as both an 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-app-server" 
title="application server" target="_blank"><code>application server</code></a> 
and an 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-api-server" 
title="API-like server or a service" target="_blank"><code>API-like server</code> 
or a <code>service</code></a>. Here is a summary of the available routes after 
the completion of this post.

<a id="existing-routes"></a>
Existing routes, some with added functionality to conditionally return either HTML or JSON:

<ol>
<li style="margin-top:10px;">
<code>GET</code>, <code>http://0.0.0.0:port/admin/me</code>: 
Returns the currently logged-in user’s information in either JSON or HTML format. 
This route is accessible only to
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-authenticated-session"
title="Authenticated sessions" target="_blank"><code>authenticated sessions</code></a>.
</li>

<li style="margin-top:10px;">	
<code>GET</code>, <code>http://0.0.0.0:port/auth/login</code>: 
Returns the application login page in HTML format.
</li>

<li style="margin-top:10px;">
<code>POST</code>, <code>http://0.0.0.0:port/auth/token</code>: 
Authenticates users. The response can be in either JSON or HTML format.
</li>

<li style="margin-top:10px;">
<code>POST</code>, <code>http://0.0.0.0:port/auth/logout</code>: 
Logs out the currently logged-in or authenticated user. Currently, 
this redirects to the application’s HTML login page.
</li>
	
<li style="margin-top:10px;">
<code>GET</code>, <code>http://0.0.0.0:port/</code>: This is the same as <code>http://0.0.0.0:port/auth/login</code>.
</li>
</ol>

<a id="new-routes"></a>
New routes: 

<ol>
<li style="margin-top:10px;">
<code>GET</code>, <code>http://0.0.0.0:port/auth/home</code>: Returns the application 
home page in HTML format after a user has successfully logged in. This route is 
accessible only to 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-authenticated-session" 
title="Authenticated sessions" target="_blank"><code>authenticated sessions</code></a>.
</li>

<li style="margin-top:10px;">
<code>GET</code>, <code>http://0.0.0.0:port/api/me</code>: 
This is a duplicate of <code>http://0.0.0.0:port/admin/me</code>, 
but this route returns the currently logged-in user’s information in JSON only.
</li>

<li style="margin-top:10px;">
<code>POST</code>, <code>http://0.0.0.0:port/api/login</code>: 
This is a duplicate of <code>http://0.0.0.0:port/auth/token</code>,
but the response is in JSON only.
</li>
</ol>

<a id="project-layout"></a>
❷ The layout of the project is listed below.

<strong>-- Please note,</strong> those marked with <span style="font-size:1.5em;">★</span> are updated, and those marked with <span style="font-size:1.5em;">☆</span> are new.

```
/home/behai/fastapi_learning/
.
├── main.py ★
├── pyproject.toml ★
├── pytest.ini ★
├── README.md ★
├── src
│ └── fastapi_learning
│     ├── common
│     │ └── consts.py ★
│     ├── controllers
│     │ ├── admin.py ★
│     │ ├── auth.py ★
│     │ └── __init__.py ★
│     ├── __init__.py ★
│     ├── models
│     │ └── employees.py ★
│     ├── static
│     │ └── styles.css
│     └── templates
│         ├── admin ☆
│         │ └── me.html 
│         ├── auth
│         │ ├── home.html ☆
│         │ └── login.html ★
│         └── base.html ★
└── tests
    ├── conftest.py
    ├── __init__.py
    ├── integration
    │ ├── test_admin_itgt.py ★
    │ ├── test_api_itgt.py ☆
    │ └── test_auth_itgt.py ★
    └── README.md ☆
```

<a id="impl-html-json-response"></a>
❸ We are implementing functionality to conditionally return either HTML or JSON.
In the 
<a href="https://behainguyen.wordpress.com/2024/05/21/python-fastapi-implementing-persistent-stateful-http-sessions-with-redis-session-middleware-and-extending-oauth2passwordbearer-for-oauth2-security/" 
title="Python FastAPI: Implementing Persistent Stateful HTTP Sessions with Redis Session Middleware and Extending OAuth2PasswordBearer for OAuth2 Security" 
target="_blank">third post</a>, the only UI we had was the HTML login page. 
All the responses were in JSON. Without a complete UI, it’s not very efficient 
to observe a complete authentication process.

We will refactor this behavior as follows: the default response will be HTML. 
The response will be JSON only when the incoming request contains the header 
<code>x-expected-format</code>, and its value is set to <code>application/json</code>.

The public helper function 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/d01c61372c63b3609ee6ad01eb4c00fccdae26cc/src/fastapi_learning/controllers/__init__.py#L17-L22" 
title="def json_req(request: Request):" 
target="_blank"><code>json_req(...)</code></a> in the 
<a href="https://github.com/behai-nguyen/fastapi_learning/tree/d01c61372c63b3609ee6ad01eb4c00fccdae26cc/src/fastapi_learning/controllers" 
title="fastapi_learning/controllers" 
target="_blank"><code>/controllers</code></a> 
layer checks for a requested JSON response. 

🙏 Please note the following important change in the logic of the code. In the 
<a href="https://behainguyen.wordpress.com/2024/05/21/python-fastapi-implementing-persistent-stateful-http-sessions-with-redis-session-middleware-and-extending-oauth2passwordbearer-for-oauth2-security/" 
title="Python FastAPI: Implementing Persistent Stateful HTTP Sessions with Redis Session Middleware and Extending OAuth2PasswordBearer for OAuth2 Security" 
target="_blank">third post</a>, the default behavior of the 
<a href="https://fastapi.tiangolo.com/tutorial/security/first-steps/?h=oauth2passwordbearer#fastapis-oauth2passwordbearer" 
title="OAuth2PasswordBearer" target="_blank">OAuth2PasswordBearer</a> class was 
to raise an <code>HTTPException</code> on error, which resulted in a JSON response 
being sent to the client. Similarly, the helper methods of the endpoint handlers 
also raised <code>HTTPException</code>. This is no longer appropriate, 
<strong>as only the endpoint handlers can determine the correct response format.</strong> 
To accommodate this, all helper methods of the endpoint handlers now return the 
<code>HTTPException</code>. Furthermore, the <code>auto_error</code> of 
<a href="https://fastapi.tiangolo.com/tutorial/security/first-steps/?h=oauth2passwordbearer#fastapis-oauth2passwordbearer" 
title="OAuth2PasswordBearer" target="_blank">OAuth2PasswordBearer</a> 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/d01c61372c63b3609ee6ad01eb4c00fccdae26cc/src/fastapi_learning/__init__.py#L29" 
title="fastapi_learning/__init__.py" target="_blank">is turned off</a> 
to prevent it from raising the <code>HTTPException</code> exceptions. 
As a result, we need to 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/main/src/fastapi_learning/controllers/admin.py#L45-55" 
title="controllers/admin.py" target="_blank">detect and handle its errors</a> ourselves. 
<strong>In this iteration of the code, to return an error JSON response, 
the endpoint handlers also raise the returned <code>HTTPException</code></strong>. 
This implementation might change in the future. 

💥 To request a JSON response from the existing <code>/auth/token</code> 
and <code>/admin/me</code> routes, users must explicitly set the value of 
the <code>x-expected-format</code> header to <code>application/json</code>. 
However, with the new routes <code>/api/login</code> and <code>/api/me</code>, 
users do not have to set the <code>x-expected-format</code> header.

Even though their respective endpoint handlers are the same, we register 
the <code>/api/*</code> routes with a 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/d01c61372c63b3609ee6ad01eb4c00fccdae26cc/src/fastapi_learning/controllers/__init__.py#L24-L46" 
title="class JsonAPIRoute(APIRoute):" 
target="_blank">custom <code>JsonAPIRoute</code> routing class</a>. 
Within this custom class, we intercept the incoming HTTP requests and add 
our own custom header <code>x-expected-format</code>:

<figure class="highlight"><pre><code class="language-python" data-lang="python"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">41
42
</pre></td><td class="code"><pre>            <span class="n">json_header</span><span class="p">:</span> <span class="n">Tuple</span><span class="p">[</span><span class="nb">bytes</span><span class="p">]</span> <span class="o">=</span> <span class="n">FORMAT_HEADER</span><span class="p">.</span><span class="n">encode</span><span class="p">(),</span> <span class="n">types_map</span><span class="p">[</span><span class="s">'.json'</span><span class="p">].</span><span class="n">encode</span><span class="p">()</span>
            <span class="n">request</span><span class="p">.</span><span class="n">headers</span><span class="p">.</span><span class="n">__dict__</span><span class="p">[</span><span class="s">"_list"</span><span class="p">].</span><span class="n">append</span><span class="p">(</span><span class="n">json_header</span><span class="p">)</span>
</pre></td></tr></tbody></table></code></pre></figure>

In the 
<a href="https://github.com/behai-nguyen/fastapi_learning/tree/d01c61372c63b3609ee6ad01eb4c00fccdae26cc/src/fastapi_learning/controllers" 
title="fastapi_learning/controllers" 
target="_blank"><code>/controllers</code></a> modules 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/d01c61372c63b3609ee6ad01eb4c00fccdae26cc/src/fastapi_learning/controllers/auth.py#L40-L43" 
title="controllers/auth.py" target="_blank"><code>auth.py</code></a>
and 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/d01c61372c63b3609ee6ad01eb4c00fccdae26cc/src/fastapi_learning/controllers/admin.py#L40-L43" 
title="controllers/admin.py" target="_blank"><code>admin.py</code></a>,  
we create new router instances using 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/d01c61372c63b3609ee6ad01eb4c00fccdae26cc/src/fastapi_learning/controllers/__init__.py#L24-L46" 
title="class JsonAPIRoute(APIRoute):" 
target="_blank"><code>JsonAPIRoute</code></a> as follows:

```python
api_router = APIRouter(route_class=JsonAPIRoute,
    prefix="/api",
    tags=["API"],
)
```

We decorate the new <code>/api/*</code> routes using the new <code>api_router</code> 
instances, respectively in each of the above two modules as follows:

```python
@api_router.post("/login")
async def login_api(request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):

    return await login(request, form_data)
```

```python
@api_router.get("/me")
async def read_users_me_api(
    request: Request,
    current_user: Annotated[User, Depends(get_current_active_user)]
):    
    return await read_users_me(request, current_user)
```

Finally, the application instance 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/main/main.py#L34-L37" 
title="main.py routers registration" target="_blank">incorporates the two new router 
instances</a> to activate the two new routes <code>/api/login</code> and <code>/api/me</code>.

<a id="app-auth-ui-flow"></a>
❹ We are completing the application authentication UI flow. 
Before being served, a request must undergo 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-request-auth"
title="request authentication" target="_blank"><code>request authentication</code></a>.
The outcome of the authentication determines if the request gets served, redirected, or results in an error response.

The term <em>“Authentication UI flow”</em> refers to when the application is being used as an 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-app-server" 
title="application server" target="_blank"><code>application server</code></a>, 
i.e., serving HTML pages, and how the application redirects requests to 
appropriate HTML pages depending on the outcome of the 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-request-auth" 
title="request authentication" target="_blank"><code>request authentication</code></a> 
process. Consider the following examples:

<a id="app-auth-ui-flow-example-01"></a>
⓵ A request to the route <code>/auth/home</code> while not logged in gets redirected 
to the login page <code>/auth/login?state=2</code>. The value of the query parameter 
<code>state</code> triggers an appropriate message to be displayed on the login page. 

<strong>Please note</strong>, in this 
<a href="https://github.com/behai-nguyen/rust_web_01" title="Index of the Complete Rust actix-web Series" target="_blank">Rust series</a>, 
I implement redirection using 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#notes-on-cookies-our-own" 
title="server-side per-request cookies" target="_blank">server-side per-request cookies</a>.
Cookies can be complicated, 
<a href="https://behai-nguyen.github.io/2024/02/13/rust-21-actix-web-cors-cookies-ajax-calls.html" 
title="Rust: actix-web CORS, Cookies and AJAX calls" 
target="_blank">as discussed in this post</a>. 
While a query parameter is not as elegant as cookies, it is simple to implement, and in this case, it is not a security-critical piece of information.

<a id="app-auth-ui-flow-example-02"></a>
⓶ A request to the route <code>/auth/login</code> while already logged in 
redirects to  <code>/auth/home</code>.

⓷ While already logged in, a request to the route <code>/admin/me</code> 
returns the logged-in user’s new information HTML page.

In the future, if we add new routes, they should follow the behaviour just described.

<a id="refactor-password-matching"></a>
❺ We have updated the password hashing and matching. In the last 
revision of the <code>models/employees.py</code> module, the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/cb2a77e45475a360515c7d08c36ff59ab34f0cd1/src/fastapi_learning/models/employees.py#L25-L45" 
title="models/employees.py" target="_blank"><code>fake_users_db</code></a> 
constant had a bug: the value of the <code>hashed_password</code> 
field was incorrect. This bug 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/d01c61372c63b3609ee6ad01eb4c00fccdae26cc/src/fastapi_learning/models/employees.py#L27-L47" 
title="models/employees.py" target="_blank">has now been fixed</a>.

In this post, we removed the existing 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/cb2a77e45475a360515c7d08c36ff59ab34f0cd1/src/fastapi_learning/models/employees.py#L47-L48" 
title="models/employees.py" target="_blank"><code>fake_hash_password(...)</code> method</a>  
and added a new production-grade 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/d01c61372c63b3609ee6ad01eb4c00fccdae26cc/src/fastapi_learning/models/employees.py#L49-L53" 
title="models/employees.py" target="_blank"><code>password_match(...)</code> method</a>. 
This new method uses the 
<a href="https://pypi.org/project/argon2-cffi/" 
title="argon2-cffi: Argon2 for Python" target="_blank">argon2-cffi</a> 
library to dehash the database password and compare it to the plain submitted password. 
This <code>password_match(...)</code> method will work with the test database, as 
mentioned toward the end of the 
<a href="https://behainguyen.wordpress.com/2024/05/21/python-fastapi-implementing-persistent-stateful-http-sessions-with-redis-session-middleware-and-extending-oauth2passwordbearer-for-oauth2-security/" 
title="Python FastAPI: Implementing Persistent Stateful HTTP Sessions with Redis Session Middleware and Extending OAuth2PasswordBearer for OAuth2 Security" 
target="_blank">third post</a>: 

> Also, we will use a proper database, the <a href="https://github.com/datacharmer/test_db" title="Oracle Corporation MySQL test database" target="_blank">Oracle Corporation MySQL test database</a>. And our database access layer will be the <a href="https://github.com/behai-nguyen/bh_database" title="Database wrapper classes for SQLAlchemy" target="_blank">Database wrapper classes for SQLAlchemy</a>. The main table in the above database is the <code>employees</code> table, which does not have the email and the password fields, we will have to manually add them as discussed in the following section of another post <a href="https://behainguyen.wordpress.com/2024/01/14/rust-actix-web-endpoints-which-accept-both-application-x-www-form-urlencoded-and-application-json-content-types/#step-two-update-employees-table" title="Update the employees table, adding new fields email and password" target="_blank">Update the <code>employees</code> table, adding new fields <code>email</code> and <code>password</code></a>.

Please note, 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/d01c61372c63b3609ee6ad01eb4c00fccdae26cc/src/fastapi_learning/models/employees.py#L27-L47" 
title="models/employees.py" target="_blank"><code>fake_users_db</code></a> 
has two test users listed below. Please use them to test the example: 

<ol>
<li style="margin-top:10px;">
<code>Username</code>: <code>behai_nguyen@hotmail.com</code>; <code>password</code>: <code>password</code>
</li>

<li style="margin-top:10px;">
<code>Username</code>: <code>pranav.furedi.10198@gmail.com</code>; <code>password</code>: <code>password</code>
</li>
</ol>

<a id="integration-tests"></a>
❻ We still only have 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/d01c61372c63b3609ee6ad01eb4c00fccdae26cc/tests" 
title="Integration Tests" target="_blank"><code>Integration Tests</code></a>,
which have been significantly upgraded: 

⓵ Please refer to
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/d01c61372c63b3609ee6ad01eb4c00fccdae26cc/tests/README.md" 
title="README.md" target="_blank">README.md</a> 
for explanations on some implementation details.

⓶ For the two existing modules, 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/d01c61372c63b3609ee6ad01eb4c00fccdae26cc/tests/integration/test_auth_itgt.py" 
title="integration/test_auth_itgt.py" 
target="_blank"><code>integration/test_auth_itgt.py</code></a> 
and 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/d01c61372c63b3609ee6ad01eb4c00fccdae26cc/tests/integration/test_admin_itgt.py" 
title="integration/test_admin_itgt.py"
target="_blank"><code>integration/test_admin_itgt.py</code></a>,
new tests were created to test new functionalities.

⓷ The new test module, 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/d01c61372c63b3609ee6ad01eb4c00fccdae26cc/tests/integration/test_api_itgt.py" 
title="integration/test_api_itgt.py" 
target="_blank"><code>integration/test_api_itgt.py</code></a>,  
contains some tests for the <code>/api/*</code> routes. 
This module is not very comprehensive, as it is just a duplicate of some of 
the tests already covered in the previous two existing modules.

<a id="running-the-app"></a>
❼ Let’s get the example application running and briefly describe how the UI works. 
Please note that our application UI and Swagger UI share the same persistent 
stateful HTTP session state. Regardless of which route we use to log in, once 
logged in, it should be recognised as such in both UIs.

<a id="running-the-app-install-pkg"></a>
⓵ We need to install the 
<a href="https://pypi.org/project/argon2-cffi/" 
title="argon2-cffi: Argon2 for Python" target="_blank">argon2-cffi</a> 
package. Please run the below project editable install command: 

```
▶️Windows 10:</code> (venv) F:\fastapi_learning>venv\Scripts\pip.exe install -e .
▶️Ubuntu 22.10:</code> (venv) behai@hp-pavilion-15:~/fastapi_learning$ ./venv/bin/pip install -e .
```

<a id="running-the-app-command"></a>
⓶ The command to run the application:

```
▶️Windows 10:</code> (venv) F:\fastapi_learning>venv\Scripts\uvicorn.exe main:app --host 0.0.0.0 --port 5000 
▶️Ubuntu 22.10:</code>  (venv) behai@hp-pavilion-15:~/fastapi_learning$ ./venv/bin/uvicorn main:app --host 0.0.0.0 --port 5000
```

<a id="running-the-app-own-ui"></a>
⓷ The application UI. Open a web browser and navigate to the example URL 
<a href="http://192.168.0.16:5000/" 
title="The example application URL on Ubuntu 22.10" target="_blank">http://192.168.0.16:5000/</a>
or <a href="http://localhost:5000/"
title="The example application URL on localhost" target="_blank">http://localhost:5000/</a>. 
We should get the application login page as illustrated in 
<a href="https://behainguyen.wordpress.com/2024/05/21/python-fastapi-implementing-persistent-stateful-http-sessions-with-redis-session-middleware-and-extending-oauth2passwordbearer-for-oauth2-security/#ui-01" 
title="Python FastAPI: Implementing Persistent Stateful HTTP Sessions with Redis Session Middleware and Extending OAuth2PasswordBearer for OAuth2 Security" 
target="_blank">these screenshots in the third post</a>. 
Then use one of these test credentials to log in:

<ol>
<li style="margin-top:10px;">
<code>Username</code>: <code>behai_nguyen@hotmail.com</code>; <code>password</code>: <code>password</code>
</li>

<li style="margin-top:10px;">
<code>Username</code>: <code>pranav.furedi.10198@gmail.com</code>; <code>password</code>: <code>password</code>
</li>
</ol>

<a id="running-the-app-swagger-ui"></a>
⓸ The Swagger UI URL is 
<a href="http://192.168.0.16:5000/docs" 
title="The example application Swagger UI URL on Ubuntu 22.10" target="_blank">http://192.168.0.16:5000/docs</a>
or <a href="http://localhost:5000/docs"
title="The example application Swagger UI URL on localhost" target="_blank">http://localhost:5000/docs</a>.
And it still shares the same persistent stateful HTTP session state as the application UI.

Log in using either UI, then accessing a route on the other UI that requires an 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-authenticated-session"
title="authenticated session" target="_blank"><code>authenticated session</code></a>, 
it should result in a successful response. We have discussed this behaviour in 
<a href="https://behainguyen.wordpress.com/2024/05/21/python-fastapi-implementing-persistent-stateful-http-sessions-with-redis-session-middleware-and-extending-oauth2passwordbearer-for-oauth2-security/#ui-02" 
title="Python FastAPI: Implementing Persistent Stateful HTTP Sessions with Redis Session Middleware and Extending OAuth2PasswordBearer for OAuth2 Security" 
target="_blank">this illustration in the third post</a>. 

<a id="running-the-app-api-route"></a>
⓹ Accessing the <code>/api/*</code> routes. 
The following screenshots illustrate accessing the <code>/api/*</code> 
routes using 
<a href="https://www.postman.com/" title="Postman" target="_blank">Postman</a>.

● Accessing the login route <code>/api/login</code>: 
Submits the credentials using <code>application/x-www-form-urlencoded</code>:

![110-01.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/06/110-01.png)

● Accessing the logged-in user information route <code>/api/me</code>: We need to 
set the <code>Authorization</code> header with <code>Bearer &lt;access_token&gt;</code>, 
currently the <code>access_token</code> is still just the username: 

![110-02.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/06/110-02.png)

<a id="concluding-remarks"></a>
❽ During the development of the code for this post, I have learned some more useful 
features of 
<a href="https://fastapi.tiangolo.com/learn/" title="FastAPI" target="_blank">FastAPI</a> 
I hope you would enjoy these features as well. We still have more to explore in this series, 
though I am not certain what we will cover in the next post yet.

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
<a href="https://fastapi.tiangolo.com/" target="_blank">https://fastapi.tiangolo.com/</a>
</li>
<li>
<a href="https://1000logos.net/download-image/" target="_blank">https://1000logos.net/download-image/</a>
</li>
</ul>

<h3>
🐍 <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>
