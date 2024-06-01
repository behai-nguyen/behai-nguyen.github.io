---
layout: post
title: "Python FastAPI: Implementing Persistent Stateful HTTP Sessions with Redis Session Middleware and Extending OAuth2PasswordBearer for OAuth2 Security"

description: In the second post of our FastAPI learning series, we implemented a placeholder for the application's own authentication process. In this post, we will complete this process by implementing persistent server-side HTTP sessions using the starsessions library and its Redis store store, as well as extending the OAuth2PasswordBearer class. 

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/05/107-02-a.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/05/107-02-b.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/05/107-02-c.png"

gallery-image-list-2:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/05/107-03-a.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/05/107-03-b.png"

gallery-image-list-3:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/05/107-04-a.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/05/107-04-b.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/05/107-04-c.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/05/107-04-d.png"

gallery-image-list-4:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/05/107-05-a.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/05/107-05-b.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/05/107-05-c.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/05/107-05-d.png"

tags:
- Python
- FastAPI
- OAuth2
- Security
- persistent
- server-side 
- session
---

<em>In the <a href="https://behainguyen.wordpress.com/2024/05/13/python-fastapi-integrating-oauth2-security-with-the-applications-own-authentication-process/" title="Python FastAPI: Integrating OAuth2 Security with the Application’s Own Authentication Process" target="_blank">second post</a> of our <a href="https://fastapi.tiangolo.com/learn/" title="FastAPI" target="_blank">FastAPI</a> learning series, we implemented a placeholder for the application's own authentication process. In this post, we will complete this process by implementing persistent server-side HTTP sessions using the <a href="https://pypi.org/project/starsessions/" title="starsessions" target="_blank">starsessions</a> library and its <a href="https://redis.io/" title="Redis store" target="_blank">Redis store</a> store, as well as extending the <a href="https://fastapi.tiangolo.com/tutorial/security/first-steps/?h=oauth2passwordbearer#fastapis-oauth2passwordbearer" title="OAuth2PasswordBearer" target="_blank">OAuth2PasswordBearer</a> class.</em>

<h3>
🐍 <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![107-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/05/107-feature-image.png) |
|:--:|
| *Python FastAPI: Implementing Persistent Stateful HTTP Sessions with Redis Session Middleware and Extending OAuth2PasswordBearer for OAuth2 Security* |

<p>
🚀 <strong>Please note,</strong> complete code for this post
can be downloaded from GitHub with:
</p>

```
git clone -b v0.3.0 https://github.com/behai-nguyen/fastapi_learning.git
```

<a id="starsessions-lib"></a>
<p>
❶ We use the <a href="https://pypi.org/project/starsessions/" title="starsessions" target="_blank">starsessions</a> library and its <a href="https://redis.io/" title="Redis store" target="_blank">Redis store</a> to implement persistent server-side HTTP sessions.
</p>

<p>
The <code>starsessions</code> library stores UUID session IDs in browsers under a cookie named <code>session</code>. In Redis, these session IDs are prefixed with <code>starsessions.</code>, for example, <code>starsessions.4d6982465cb604f0fc8523c925957e56</code>.
</p>

<p>
Requests must include the <code>session</code> cookie to be recognised as originating from <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-authenticated-session" title="authenticated sessions" target="_blank"><code>authenticated sessions</code></a>. Cookies can be problematic; we will discuss this in the relevant sections of the post.
</p>

<p>
Note that the <a href="https://github.com/alex-oleshkevich/starsessions/blob/master/examples/redis_.py" title="starsessions Redis store example" target="_blank">starsessions Redis store example</a> has been written for the <a href="https://www.starlette.io/" title="Starlette framework" target="_blank">Starlette framework</a>. For <a href="https://fastapi.tiangolo.com/learn/"title="FastAPI" target="_blank">FastAPI</a>, we register middleware with <code>FastAPI().add_middleware(...)</code>.
</p>

<p>
Please refer to the post <a href="https://behainguyen.wordpress.com/2023/12/23/using-the-redis-official-docker-image-on-windows-10-and-ubuntu-22-10-kinetic/" title="Using the Redis Official Docker Image on Windows 10 and Ubuntu 22.10 kinetic" target="_blank">Using the Redis Official Docker Image on Windows 10 and Ubuntu 22.10 kinetic</a> for instructions on setting up the Redis server on both Windows 10 and Ubuntu 22.10 Kinetic.
</p>

<p>
On Windows 10, we use the <a href="https://redis.io/insight/" title="Redis Insight desktop application" target="_blank">Redis Insight desktop application</a> to view the Docker container Redis databases on both Windows 10 and Ubuntu 22.10. Start the application; the local database should be listed under <code>127.0.0.1:6379</code>. To connect to a Docker container Redis database on another machine, click the <code>+ Add Redis database</code> button on the top left-hand corner, then specify the IP address and the Redis database port. I did not need to specify the username and password. The screenshot below shows both Docker container Redis databases on Windows 10 and Ubuntu 22.10:
</p>

![107-01.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/05/107-01.png)

<p style="clear:both;">
In this post, we refactor the application significantly. We make changes to the routes and reorganise the project layout more logically.
</p>

<a id="app-routes"></a>
<p>
❷ We group the implemented routes under two prefixes: <code>/auth</code> and <code>/admin</code>. We also add some new routes. Please refer to the list below: 
</p>

<ol>
<li style="margin-top:10px;">
<code>GET</code>, <code>http://0.0.0.0:port/admin/me</code>: Originally <code>/users/me</code>.
</li>
<li style="margin-top:10px;">	
<code>GET</code>, <code>http://0.0.0.0:port/auth/login</code>: Originally <code>/login</code>.
</li>
<li style="margin-top:10px;">
<code>POST</code>, <code>http://0.0.0.0:port/auth/token</code>: Originally <code>/token</code>.
</li>
<li style="margin-top:10px;">
<code>POST</code>, <code>http://0.0.0.0:port/auth/logout</code>: This is a new route.
</li>
	
<li style="margin-top:10px;">
<code>GET</code>, <code>http://0.0.0.0:port/</code>: This is a new route. It is the same as <code>http://0.0.0.0:port/auth/login</code>.
</li>
</ol>

<a id="project-restructure"></a>

<p>
❸ We refactor the single-module application into appropriate layers: <code>/models</code> and <code>/controllers</code>. We also add integration tests for all routes. The layout of the project is listed below.
</p>

<a id="project-layout-chart"></a>

<p>
<strong>-- Please note,</strong> those marked with <span style="font-size:1.5em;">★</span> are updated, and those marked with <span style="font-size:1.5em;">☆</span> are new.
</p>

```
/home/behai/fastapi_learning/
.
├── main.py ★
├── pyproject.toml ★
├── pytest.ini ☆
├── README.md ★
├── src
│ └── fastapi_learning
│     ├── common ☆
│     │ └── consts.py
│     ├── controllers ☆
│     │ ├── admin.py
│     │ ├── auth.py
│     │ └── __init__.py
│     ├── __init__.py ☆
│     ├── models ☆
│     │ └── employees.py
│     ├── static
│     │ └── styles.css
│     └── templates
│         ├── auth
│         │ └── login.html ★
│         └── base.html
└── tests ☆
    ├── conftest.py
    ├── __init__.py
    └── integration
        ├── test_admin_itgt.py
        └── test_auth_itgt.py
```

<p>
Despite appearing complicated, there is not a lot of new code. 
The code under 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/cb2a77e45475a360515c7d08c36ff59ab34f0cd1/src/fastapi_learning/models" 
title="/models" target="_blank"><code>/models</code></a> is 
copied as-is from <a href="https://github.com/behai-nguyen/fastapi_learning/blob/3fd102080ba8bef48b3eee1d14f4a066e89909f7/main.py" title="main.py" target="_blank"><code>main.py</code></a>. 
Most of the <a href="https://github.com/behai-nguyen/fastapi_learning/blob/cb2a77e45475a360515c7d08c36ff59ab34f0cd1/src/fastapi_learning/controllers" 
title="/controllers" target="_blank"><code>/controllers</code></a> code 
is also copied from <a href="https://github.com/behai-nguyen/fastapi_learning/blob/3fd102080ba8bef48b3eee1d14f4a066e89909f7/main.py" title="main.py" target="_blank"><code>main.py</code></a>; 
the endpoint method for <code>/auth/logout</code> and some minor private 
helper methods are new. These should be self-explanatory. We will discuss 
some of the key code refactorings in the following sections.
</p>

<p>
⓵ <a href="https://github.com/behai-nguyen/fastapi_learning/blob/cb2a77e45475a360515c7d08c36ff59ab34f0cd1/main.py" 
title="Application module main.py" target="_blank"><code>main.py</code></a>:
Most of the code has been moved out, as mentioned above.
</p>

<p>
● The key addition includes 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/cb2a77e45475a360515c7d08c36ff59ab34f0cd1/main.py#L28-L30" 
title="Lines 28 to 30" target="_blank">lines 28 to 30</a>: 
</p>

```python
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost")
app.add_middleware(SessionAutoloadMiddleware)
app.add_middleware(SessionMiddleware, store=RedisStore(REDIS_URL), cookie_https_only=False)
```

<p>
We use the <a href="https://pypi.org/project/starsessions/" 
title="starsessions" target="_blank">starsessions</a> 
library and its 
<a href="https://redis.io/" title="Redis store" target="_blank">Redis store</a> 
to implement persistent server-side HTTP sessions, as mentioned 
<a href="#starsessions-lib">previously</a>.
</p>

<p>
<strong>💥 Please note:</strong> <code>cookie_https_only=False</code> — since we are not using the <code>HTTPS</code> scheme, it is necessary to set <code>cookie_https_only</code> to <code>False</code>. This setting is unrelated to integration tests.
</p>

<p>
Cookies are a complex issue. We have discussed cookies in greater detail elsewhere. Please refer to this <a href="https://behainguyen.wordpress.com/2024/02/13/rust-actix-web-cors-cookies-and-ajax-calls/#cookies-ajax-cookies-management" title="Rust: actix-web CORS, Cookies and AJAX calls | How session cookies are created" target="_blank">detailed discussion</a>.
</p>

<p>
● Other refactorings in this module should be self-explanatory.
</p>

<p>
⓶ The next key refactoring is the endpoint handler method 
for the <code>POST</code> login path <code>/auth/token</code>, located in 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/cb2a77e45475a360515c7d08c36ff59ab34f0cd1/src/fastapi_learning/controllers/auth.py#L56-L73" 
title="controllers/auth.py login(...) method" 
target="_blank"><code>controllers/auth.py</code></a>,
please note lines <strong>5</strong>, <strong>6</strong> and <strong>10</strong>:
</p>

<!-- highlight python linenos hl_lines="5 6 10" -->
{% highlight python linenos %}
@router.post("/token")
async def login(request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    
    if __is_logged_in(request): 
        return {"message": LOGGED_IN_SESSION_MSG}

    ...
    
    request.session["access_token"] = user.username

    return {"access_token": user.username, "token_type": "bearer"}
{% endhighlight %}

<a id="session-loading"></a>
<p>
● After a valid login, we store the <code>access_token</code> in the persistent server-side HTTP session Redis store.
</p>

<p>
Subsequent requests from this same 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-authenticated-session" 
title="authenticated session" target="_blank"><code>authenticated session</code></a> 
should include the <code>session</code> UUID cookie as 
<a href="#starsessions-lib">discussed</a>. 
The session middleware then uses this UUID to load the actual session 
content from the Redis store, making the <code>access_token</code> 
available in the incoming request's <code>request.session</code> property.
</p>

<p>
● As long as we have a valid <code>access_token</code> in the persistent 
server-side HTTP session Redis store, any subsequent login request will simply 
return a JSON response <code>{"message": "Already logged in"}</code>. 
This same behavior applies to the <code>GET</code> login page path 
<code>/auth/login</code>, whose endpoint handler method is the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/cb2a77e45475a360515c7d08c36ff59ab34f0cd1/src/fastapi_learning/controllers/auth.py#L49-L54" 
title="login_form(...) method" 
target="_blank"><code>login_form(...)</code></a> 
method in 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/cb2a77e45475a360515c7d08c36ff59ab34f0cd1/src/fastapi_learning/controllers/auth.py" 
title="controllers/auth.py" target="_blank"><code>controllers/auth.py</code></a>.
</p>

<p>
This simple returned JSON serves as a placeholder in this revision of the code. It will be refactored further as we progress.
</p>

<p>
⓷ The final key refactoring is in the module 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/cb2a77e45475a360515c7d08c36ff59ab34f0cd1/src/fastapi_learning/__init__.py" 
title="fastapi_learning/__init__.py" target="_blank"><code>fastapi_learning/__init__.py</code></a>, 
with the following content:
</p>

```python
class OAuth2PasswordBearerRedis(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:

        ret_value = request.session.get("access_token")

        if ret_value != None:
            return ret_value
    
        return await super().__call__(request)
    
oauth2_scheme = OAuth2PasswordBearerRedis(tokenUrl="/auth/token")
```

<p>
Recall that in the <a href="https://github.com/behai-nguyen/fastapi_learning/blob/3fd102080ba8bef48b3eee1d14f4a066e89909f7/main.py#L64" title="main.py line 64" target="_blank">previous version</a>, it was a one-liner: 
</p>

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

<p>
We effectively extend <a href="https://fastapi.tiangolo.com/tutorial/security/first-steps/?h=oauth2passwordbearer#fastapis-oauth2passwordbearer" title="OAuth2PasswordBearer" target="_blank">OAuth2PasswordBearer</a> to first look for the <code>access_token</code> in the incoming <code>request.session</code>. If it is not there, we fall back to the default behavior, which checks the request <code>Authorization</code> header.
</p>

<p>
We understand that at this point, the appropriate session content in the Redis database has been loaded <a href="#session-loading">as described</a>. Otherwise, the call to <code>request.session.get("access_token")</code> would not work as expected.
</p>

<p>
❹ <a href="https://github.com/behai-nguyen/fastapi_learning/blob/cb2a77e45475a360515c7d08c36ff59ab34f0cd1/tests" 
title="Integration Tests" target="_blank"><code>Integration Tests</code></a>. 
</p>

<p>
We are using <a href="https://docs.pytest.org/en/8.2.x/" title="pytest" target="_blank">pytest</a> and <a href="https://fastapi.tiangolo.com/reference/testclient/" title="FastAPI TestClient" target="_blank">FastAPI TestClient</a>. To install the development dependencies onto the active virtual environment, please use the command: 
</p>

```
pip install -e .[dev]
```

<p>
<strong>💥 Key point to remember:</strong> It is our responsibility to pass the <a href="#starsessions-lib"><code>session</code> cookie</a> from a successful login response to the subsequent requests; otherwise, the tests will not have access to the Redis session store. Here is what the code looks like. 
Please note lines <strong>4</strong> and <strong>5</strong>:
</p>

<!-- highlight python mark_lines="4 5" -->
{% highlight python linenos %}
login_response = test_client.post('/auth/token', ...)

# Set session (Id) for next request.
session_cookie = login_response.cookies.get('session')
test_client.cookies = {'session': session_cookie}

response = test_client.post('/auth/logout')
{% endhighlight %}

<p>
I struggled with setting the cookie correctly and sought help from various posts, please refer to <a href="https://github.com/tiangolo/fastapi/discussions/11510" title="this post" target="_blank">this post</a> and <a href="https://github.com/alex-oleshkevich/starsessions/discussions/72" title="this post" target="_blank">this post</a>, but they were not very helpful. Finally, ChatGPT came <a href="https://chatgpt.com/share/ce977733-60a4-4b6b-8f08-4b567b603706" title="FastAPI Pytest Testing Session" target="_blank">to the rescue</a>. Interestingly, ChatGPT did not get it right the first time on cookie setting, but after giving feedback, the second revision of the test code was correct.
</p>

<p>
We will not discuss the actual integration tests in detail; they should be self-explanatory. The tests simply check the responses from each route based on whether the HTTP session is <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-authenticated-session" title="authenticated session" target="_blank"><code>authenticated</code></a> or not.
</p>

<p>
❺ Let's take a look at how the UI works. We want to verify that regardless of which route we use to log in, once logged in, it should be recognised as such in both our application UI and Swagger UI.
</p>

<a id="ui-01"></a>
<p>
⓵ Login using the application login page: 
</p>

{% include image-gallery.html list=page.gallery-image-list-1 %}

<p style="clear:both;">
Note in the screenshots that the <code>session</code> cookie is created and stored in the browser, and in Redis, the <code>session</code> UUID is prefixed with <code>starsessions.</code>, as discussed <a href="#starsessions-lib">previously</a>. The <code>access_token</code> is stored in the Redis database.
</p>

<a id="ui-02"></a>
<p>
⓶ Using the same browser as in <a href="#ui-01">illustration ⓵</a>, go to Swagger UI and submit a <code>GET</code> request to <code>/admin/me</code>: 
</p>

{% include image-gallery.html list=page.gallery-image-list-2 %}

<p style="clear:both;">
We get the expected response. Please recall that this did not work in the <a href="https://behainguyen.wordpress.com/2024/05/13/python-fastapi-integrating-oauth2-security-with-the-applications-own-authentication-process/" title="Python FastAPI: Integrating OAuth2 Security with the Application’s Own Authentication Process" target="_blank">previous post</a>.
</p>

<a id="ui-03"></a>
<p>
⓷ Using the same browser as in <a href="#ui-01">illustration ⓵</a>, 
logout from Swagger UI:
</p>

{% include image-gallery.html list=page.gallery-image-list-3 %}

<p style="clear:both;">
Please note that the browser cookie is removed from the browser, and the session UUID is removed from Redis. In the last Redis screenshot, the data on the right-hand pane is residual data from <a href="#ui-01">illustration ⓵</a>.
</p>

<a id="ui-04"></a>
<p>
⓸ From Swagger UI, login using the <code>POST</code> request to path <code>/auth/token</code>: 
</p>

{% include image-gallery.html list=page.gallery-image-list-4 %}

<p style="clear:both;">
We can see that it functions the same as when we login via the application login page, it should be so, since the endpoint method for both routes is the same.
</p>

<p>
The above UI illustrations are not all possible UI combinations.
We can try, for example, login using the Swagger UI 
<code>Authorize</code> button, then accessing other routes. They 
should all work the same for both the Swagger UI and the application UI.
</p>

<p>
We conclude this post here. In the next iterations, we will possibly 
complete the UI, having a home page, etc. Also, we will use a proper database, 
the <a href="https://github.com/datacharmer/test_db" 
title="Oracle Corporation MySQL test database" 
target="_blank">Oracle Corporation MySQL test database</a>. And 
our database access layer will be the 
<a href="https://github.com/behai-nguyen/bh_database" 
title="Database wrapper classes for SQLAlchemy" 
target="_blank">Database wrapper classes for SQLAlchemy</a>. 
The main table in the above database is the <code>employees</code> table,
which does not have the email and the password fields, we will have to
manually add them as discussed in the following section of another post 
<a href="https://behainguyen.wordpress.com/2024/01/14/rust-actix-web-endpoints-which-accept-both-application-x-www-form-urlencoded-and-application-json-content-types/#step-two-update-employees-table" 
title="Update the employees table, adding new fields email and password" 
target="_blank">Update the <code>employees</code> table, adding new fields <code>email</code> and <code>password</code></a>.
</p>

<p>
We will also have a PostgreSQL version of the above MySQL database. 
And our future example application will work with both databases, all 
we have to do is setting the database connection string appropriately 
in an external <code>.env</code> file.
</p>

<p>
Thank you for reading. I hope you find the information in this post useful. Stay safe, as always.
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
<a href="https://fastapi.tiangolo.com/" target="_blank">https://fastapi.tiangolo.com/</a>
</li>
<li>
<a href="https://1000logos.net/download-image/" target="_blank">https://1000logos.net/download-image/</a>
</li>
</ul>

<h3>
🐍 <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>
