---
layout: post
title: "Python FastAPI: Integrating OAuth2 Security with the Application's Own Authentication Process"

description: In the first post, we explore some aspects of OAuth2 authentication, focusing on the /token path as illustrated in an example from the Simple OAuth2 with Password and Bearer section of the Tutorial - User Guide Security. In this subsequent post, we implement our own custom preliminary login process, leveraging the /token path. This means that both the Swagger UI Authorize button and our application's login button utilise the same server code.

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list:
    - "https://behainguyen.files.wordpress.com/2024/05/106-04a.png"
    - "https://behainguyen.files.wordpress.com/2024/05/106-04b.png"
    - "https://behainguyen.files.wordpress.com/2024/05/106-04c.png"

tags:
- Python 
- FastAPI
- OAuth2
- Security
---

<em>In the <a href="https://behainguyen.wordpress.com/2024/05/11/python-fastapi-some-further-studies-on-oauth2-security/" title="First post" target="_blank">first post</a>, we explore some aspects of <code>OAuth2</code> authentication, focusing on the <code>/token</code> path as illustrated in an example from the <a href="https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/" title="Simple OAuth2 with Password and Bearer" target="_blank">Simple OAuth2 with Password and Bearer</a> section of the <a href="https://fastapi.tiangolo.com/tutorial/security/" title="Tutorial - User Guide Security" target="_blank">Tutorial - User Guide Security</a>. In this subsequent post, we implement our own custom preliminary login process, leveraging the <code>/token</code> path. This means that both the Swagger UI <code>Authorize</code> button and our application's login button utilise the same server code.</em>

<h3>
🐍 <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![106-feature-image.png](https://behainguyen.files.wordpress.com/2024/05/106-feature-image.png) |
|:--:|
| *Python FastAPI: Integrating OAuth2 Security with the Application's Own Authentication Process* |

🚀 <strong>Please note,</strong> complete code for this post can be downloaded from GitHub with:

```
git clone -b v0.2.0 https://github.com/behai-nguyen/fastapi_learning.git
```

During my research on <code>“FastAPI application custom login process”</code>, I've encountered implementations where there are two endpoints for handling authentication: the <code>/token</code> endpoint, as discussed in the <a href="https://fastapi.tiangolo.com/tutorial/security/" title="Tutorial - User Guide Security" target="_blank">Tutorial - User Guide Security</a> section, and the application's own login endpoint. 

<strong>💥 This approach doesn't seem right to me. In my view, the <code>/token</code> endpoint should serve as the application's login endpoint as well.</strong> In this post, we introduce a preliminary custom login process with the endpoint being the <code>/token</code> endpoint.

The code developed in this post maintains the one-module application structure from the original example. However, we've added a login HTML page and organised the project directory structure to prepare for further code changes as we progress. The updated project layout is listed below.

<strong>-- Please note,</strong> those marked with <span style="font-size:1.5em;">★</span> are updated, and those marked with <span style="font-size:1.5em;">☆</span> are new.

<a id="project-layout-chart"></a>
```
/home/behai/fastapi_learning/
├── main.py ★
├── pyproject.toml
├── README.md ★
└── src ☆
    └── fastapi_learning
        ├── static
        │ └── styles.css
        └── templates
            ├── auth
            │ └── login.html
            └── base.html
```

Changes to <a href="https://github.com/behai-nguyen/fastapi_learning/blob/3fd102080ba8bef48b3eee1d14f4a066e89909f7/main.py" title="Application module main.py" target="_blank"><code>main.py</code></a> include the following:

⓵ <a href="https://github.com/behai-nguyen/fastapi_learning/blob/3fd102080ba8bef48b3eee1d14f4a066e89909f7/main.py#L21-L23" title="Lines 21 to 23" target="_blank">Lines 21 to 23</a>: Added required imports to support HTML output.

⓶ <a href="https://github.com/behai-nguyen/fastapi_learning/blob/3fd102080ba8bef48b3eee1d14f4a066e89909f7/main.py#L25-L45" title="Lines 25 to 45" target="_blank">Lines 25 to 45</a>: Completely refactored the <code>fake_users_db</code> database to slowly match the <a href="https://github.com/datacharmer/test_db" title="test employees MySQL database by the Oracle Corporation" target="_blank">test <code>employees</code> MySQL database by Oracle Corporation</a>, as utilised in the <a href="https://github.com/behai-nguyen/bh_database/tree/main/examples/fastapir" title="SQLAlchemy database wrapper component FastAPI example" target="_blank">SQLAlchemy database wrapper component FastAPI example</a>, and <a href="https://behainguyen.wordpress.com/2024/01/14/rust-actix-web-endpoints-which-accept-both-application-x-www-form-urlencoded-and-application-json-content-types/#step-two-update-employees-table" title="Update the employees table, adding new fields email and password" target="_blank">Update the <code>employees</code> table, adding new fields <code>email</code> and <code>password</code></a>.

⓷ <a href="https://github.com/behai-nguyen/fastapi_learning/blob/3fd102080ba8bef48b3eee1d14f4a066e89909f7/main.py#L49-L50" title="Lines 49 to 50" target="_blank">Lines 49 to 50</a>: Added initialisation code to prepare support for HTML template processing.

⓸ <a href="https://github.com/behai-nguyen/fastapi_learning/blob/3fd102080ba8bef48b3eee1d14f4a066e89909f7/main.py#L66-L72" title="Lines 66 to 72" target="_blank">Lines 66 to 72</a>: Refactored models to align with the changes in <code>fake_users_db</code>.

⓹ <a href="https://github.com/behai-nguyen/fastapi_learning/blob/3fd102080ba8bef48b3eee1d14f4a066e89909f7/main.py#L95-L100" title="Lines 95 to 100" target="_blank">Lines 95 to 100</a>: Refactored the <code>get_current_active_user(...)</code> method to cease checking the <code>disabled</code> attribute of the <a href="https://github.com/behai-nguyen/fastapi_learning/blob/3fd102080ba8bef48b3eee1d14f4a066e89909f7/main.py#L66" title="The User model" target="_blank"><code>User</code> model</a>, as this attribute has been removed from the model.

⓺ <a href="https://github.com/behai-nguyen/fastapi_learning/blob/3fd102080ba8bef48b3eee1d14f4a066e89909f7/main.py#L120-L123" title="Lines 120 to 123" target="_blank">Lines 120 to 123</a>: Implemented the new <code>/login</code> endpoint, which simply returns the login HTML page.

<strong>🚀 Note that</strong> the endpoint code for the <code>/token</code> path, specifically the method <code>async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):</code>, <strong>remains unchanged.</strong>

<strong>💥 Regarding the <a href="https://github.com/behai-nguyen/fastapi_learning/blob/3fd102080ba8bef48b3eee1d14f4a066e89909f7/src/fastapi_learning/templates/auth/login.html" title="Login HTML page" target="_blank"><code>HTML login page</code></a>, please take note of the following points:</strong>

```html
...
    <form method="POST" action="/token" id="loginForm">
        <h1 class="h3 mb-3 fw-normal">Please login</h1>

        <!-- 
		Please note: there are no backslash \ in live code.
		Percentage and curly braces characters are not recognised in Markdown HTML code block.
		-->
        {\% if message is defined \%}
            <h2>\{\{ message \}\}</h2>
        {\% endif \%}

        <div>
            <label for="username">Email address:</label>
            <input type="email" class="form-control" id="username" name="username" placeholder="name@example.com" required value="">
        </div>

        <div>
            <label for="password">Password:</label>
            <input type="password" class="form-control" id="password" name="password" placeholder="Password" required value="">
        </div>
        <button type="submit">Login</button>
    </form>
...	
```

⓵ The action of the login form is directed to the <code>/token</code> path. In other words, when the login form is submitted, it sends a <code>POST</code> login request to the same endpoint used by the <code>Authorize</code> button on the Swagger UI page.

⓶ The names of the two login fields are <code>username</code> and <code>password</code>. This requirement is specified in the tutorial in the section titled <a href="https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/" title="Simple OAuth2 with Password and Bearer" target="_blank">Simple OAuth2 with Password and Bearer</a>:

>
> OAuth2 specifies that when using the "password flow" (that we are using) the client/user must send a <code>username</code> and <code>password</code> fields as form data.
>

<strong>🚀 Our application's login process now shares the same server code as the Swagger UI login process.</strong> We have two separate “clients”:

<ol>
<li style="margin-top:10px;"><code>http://0.0.0.0:port/docs</code>: The Swagger UI client page.</li>
<li style="margin-top:10px;"><code>http://0.0.0.0:port/login</code>: Our own custom login page.</li>
</ol>

On Ubuntu 22.10, run the application with the command:

```
(venv) ...:~/fastapi_learning$ venv/bin/uvicorn main:app --host 0.0.0.0 --port 5000
```

When accessing the Swagger UI page on Windows 10 at <a href="http://192.168.0.16:5000/docs" title="The Swagger UI client" target="_blank">http://192.168.0.16:5000/docs</a>, we encounter a familiar page:

![106-01.png](https://behainguyen.files.wordpress.com/2024/05/106-01.png)

The <code>GET</code> <code>/login</code> path should simply return the login HTML page, while the remaining paths should function as discussed in the <a href="https://behainguyen.wordpress.com/2024/05/11/python-fastapi-some-further-studies-on-oauth2-security/" title="First post" target="_blank">first post</a>.

When accessing the application's login page on Windows 10 at <a href="http://192.168.0.16:5000/login" title="The application login page" target="_blank">http://192.168.0.16:5000/login</a>, we are presented with our custom login page:

![106-02.png](https://behainguyen.files.wordpress.com/2024/05/106-02.png)

Upon logging in using one of the following credentials: <code>behai_nguyen@hotmail.com</code>/<code>password</code> or <code>pranav.furedi.10198@gmail.com</code>/<code>password</code>, we should receive a successful JSON response, as depicted in the screenshot below:

![106-03.png](https://behainguyen.files.wordpress.com/2024/05/106-03.png)

When attempting to log in using an invalid credential, we should receive an HTTP <code>400</code> response, which indeed occurs, as seen in the screenshots below:

{% include image-gallery.html list=page.gallery-image-list %}
<br/>

<!--
https://behainguyen.files.wordpress.com/2024/05/106-04a.png
https://behainguyen.files.wordpress.com/2024/05/106-04b.png
https://behainguyen.files.wordpress.com/2024/05/106-04c.png
-->

In the current implementation, the login process is incomplete, but it serves as an appropriate preliminary step nonetheless. We will conclude this post here as I don't want to make it too long... In the next post or so, we will implement stateful sessions and extend <code>OAuth2PasswordBearer</code> to maintain <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-authenticated-session" title="authenticated sessions" target="_blank"><code>authenticated sessions</code></a>. This means that after a successful login, users can access protected application routes until they choose to log out.

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
</ul>

<h3>
🐍 <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>
