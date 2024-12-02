---
layout: post
title: "Python FastAPI: Finishing Off the Pending Items, Code Cleanup, and Improvements"

description: In the last post of this Python FastAPI learning series, we concluded with a list of to-do items. In this post, we will address these issues. Additionally, we are performing some code cleanup and improvements. 

tags:
- Python
- FastAPI
- OAuth2
- Scope
- JSON Web Token
- JWT
- UI
---

<em>
In the last post of this <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Python FastAPI learning series</a>, we concluded with a list of <a href="https://behainguyen.wordpress.com/2024/11/22/python-fastapi-oauth2-scopes-part-03-new-crud-endpoints-and-user-assigned-scopes/#concluding-remarks" title="Python FastAPI: OAuth2 Scopes Part 03 - New CRUD Endpoints and User-Assigned Scopes" target="_blank">to-do items</a>. In this post, we will address these issues. Additionally, we are performing some code cleanup and improvements.
</em>

<h3>
🐍 <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![127-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/12/127-feature-image.png) |
|:--:|
| *Python FastAPI: Finishing Off the Pending Items, Code Cleanup, and Improvements* |

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
git clone -b v0.13.0 https://github.com/behai-nguyen/fastapi_learning.git
```

<a id="code-refactoring-summary"></a>
<p>
❶ During and after the 
<a href="https://behainguyen.wordpress.com/2024/11/22/python-fastapi-oauth2-scopes-part-03-new-crud-endpoints-and-user-assigned-scopes/" 
title="Python FastAPI: OAuth2 Scopes Part 03 - New CRUD Endpoints and User-Assigned Scopes" 
target="_blank">last post</a>, I realised that the code could be significantly improved. Some parts have been rewritten. The changes implemented in this post are listed below:
</p>

<ol>
<li style="margin-top:10px;">
A single code path for login redirection.
</li>
<li style="margin-top:10px;">
A single code path for verifying user scopes.
</li>
<li style="margin-top:10px;">
All JSON responses, including 
<a href="https://fastapi.tiangolo.com/reference/exceptions/" 
title="Exceptions - HTTPException and WebSocketException" target="_blank"><code>HTTPException</code></a>, 
now use 
<a href="https://bh-apistatus.readthedocs.io/en/latest/result-status.html#bh_apistatus.result_status.ResultStatus" 
title="bh_apistatus.result_status.ResultStatus class" target="_blank"><code>ResultStatus</code></a>.
</li>
<li style="margin-top:10px;">
Rewrote template code to determine the enabled state of UI elements.
</li>
<li style="margin-top:10px;">
The logged-in user model now includes the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/4703136b6eacc7831e46efc100f1403cb17dc41c/src/fastapi_learning/models/employees.py#L81" 
title="The models/employees.py module" target="_blank">assigned scope list</a> as well. 
The logged-in user's assigned scope list is still in 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/b31421129c5bc75f822a5c2049e764ce1d12dbe9/src/fastapi_learning/__init__.py#L54" 
title="The fastapi_learning/__init__.py module" target="_blank"><code>TokenData</code></a>.
This code change eliminates the need to repeatedly decode the access token to get the logged-in user's assigned scope list.
</li>
<li style="margin-top:10px;">
Temporary data between requests is now stored in the session. 
(For a discussion on persistent stateful HTTP sessions, please refer to the 
<a href="https://behainguyen.wordpress.com/2024/05/21/python-fastapi-implementing-persistent-stateful-http-sessions-with-redis-session-middleware-and-extending-oauth2passwordbearer-for-oauth2-security/" 
title="Python FastAPI: Implementing Persistent Stateful HTTP Sessions with Redis Session Middleware and Extending OAuth2PasswordBearer for OAuth2 Security" 
target="_blank">third post</a>). This simplifies the code and reduces processing.
</li>
</ol>

<a id="project-layout"></a>
<p>
❷ No new files were added. The current structure of the project is outlined below.
</p>

<p>
<strong>-- Please note,</strong> those marked with <span style="font-size:1.5em;">★</span> 
are updated, and those marked with <span style="font-size:1.5em;">☆</span> are new.
</p>

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
├── pytest.ini
├── README.md ★
├── src
│   └── fastapi_learning
│       ├── businesses
│       │   ├── app_business.py
│       │   ├── base_business.py
│       │   ├── base_validation.py
│       │   ├── employees_mgr.py
│       │   └── employees_validation.py
│       ├── common
│       │   ├── consts.py ★
│       │   ├── jwt_utils.py
│       │   ├── queue_logging.py
│       │   └── scope_utils.py
│       ├── controllers
│       │   ├── admin.py ★
│       │   ├── auth.py ★
│       │   ├── employees_admin.py ★
│       │   ├── __init__.py ★
│       │   └── required_login.py ★
│       ├── __init__.py
│       ├── models
│       │   └── employees.py ★
│       ├── static
│       │   └── js
│       │       └── application.js
│       └── templates
│           ├── admin
│           │   └── me.html ★
│           ├── auth
│           │   ├── home.html ★
│           │   └── login.html
│           ├── base.html
│           └── emp
│               ├── insert.html ★
│               ├── search.html ★
│               ├── search_result.html ★
│               └── update.html ★
└── tests
    ├── business
    │   ├── test_employees_mgr.py
    │   ├── test_employees_validation.py
    │   └── test_scope_utils.py
    ├── conftest.py
    ├── __init__.py
    ├── integration
    │   ├── test_admin_itgt.py ★
    │   ├── test_api_itgt.py ★
    │   ├── test_auth_itgt.py ★
    │   ├── test_employees_itgt.py
    │   ├── test_expired_jwt.py ★
    │   ├── test_scope_permission_itgt.py ★
    │   └── test_scope_ui_itgt.py
    ├── README.md
    └── unit
        └── test_employees.py
```

<a id="code-refactorings"></a>
<p>
❸ Code changes. For this post, we will not go into a detailed discussion as we did in the previous posts. Blog statistics have shown that these posts aren't frequently read. Instead, I am listing the entire content of the GitHub check-in commands. I believe that, together with this short post, these commands will help in understanding the refactorings done to each code module.
</p>

<p>
Complete GitHub check-in commands:
</p>

```
$ git add pyproject.toml
$ git commit -m "Standardised JSON response via ResultStatus. General refactoring. Improved logic." -m "Removed the deprecated and unused 'aioredis'. The equivalence is 'starsessions[redis]'."
~~~

$ git add main.py
$ git commit -m "Standardised JSON response via ResultStatus. General refactoring. Improved logic." -m "Refactored the requires login custom exception handler,"^

"@app.exception_handler(RequiresLogin) / async def requires_login(request: Request, _: Exception)"^

"    - stores the exception message in session under the key login_redirect_msg."^

"    - conditionally returns JSON or HTML"^

"    - for JSON response, when error, return a JSON similar to ResultStatus"
~~~

$ git add .\src\fastapi_learning\models\employees.py
$ git commit -m "Standardised JSON response via ResultStatus. General refactoring. Improved logic." -m "Added scopes: list[str] = [] to LoggedInEmployee."
~~~

$ git add .\src\fastapi_learning\controllers\required_login.py
$ git commit -m "Standardised JSON response via ResultStatus. General refactoring. Improved logic." -m "Updated async def get_logged_in_user(...):"^

"    - when failed decoded token raises RequiresLogin with token_data.detail."^

"    - copies token payload scopes over to the returned LoggedInEmployee."^

"    - Cache the returned LoggedInEmployee to session as JSON under the key logged_in_user."^

"Added async def get_cached_logged_in_user(request: Request) -> LoggedInEmployee:"^

"Refactored class RequiresLogin(HTTPException): sub-class of HTTPException."
~~~

$ git add .\src\fastapi_learning\controllers\__init__.py
$ git commit -m "Standardised JSON response via ResultStatus. General refactoring. Improved logic." -m "Updates include:"^

"Removed def is_logged_in(...), def has_required_scopes(...)."^

"Refactored async def verify_user_scopes(...):"^

"    - LoggedInEmployee replaced access token param."^

"    - the return tuple is now (bool, permissions checking result)."^

"Improved template codes:"^

"    - added template method: def get_ui_states(...): replaces has_required_scopes(...)."^

"Added the following one-liners session helper methods:"^

"    - def set_access_token(request: Request, token: str):"^

"    - def get_access_token(request: Request) -> Union[str | None]:"^

"    - def delete_access_token(request: Request):"^

"    - def no_access_token(request: Request) -> bool:"^

"    - set_login_redirect_code(request: Request, code: int):"^

"    - get_login_redirect_code(request: Request, delete_also: bool=False) -> int:"^

"    - delete_login_redirect_code(request: Request):"^

"    - def set_login_redirect_message(request: Request, message: str):"^

"    - def get_login_redirect_message(request: Request, delete_also: bool=False) -> str:"^

"    - def delete_login_redirect_message(request: Request):"
~~~

$ git add .\src\fastapi_learning\common\consts.py
$ git commit -m "Standardised JSON response via ResultStatus. General refactoring. Improved logic." -m "Added some new constants."
~~~

$ git add .\src\fastapi_learning\controllers\admin.py
$ git commit -m "Standardised JSON response via ResultStatus. General refactoring. Improved logic." -m "Updates include:"^

"All JSON responses are returned via ResultStatus."^

"async def read_users_me(...):"^

"    - code cleaned up."^

"    - no longer check for authenticated session."^

"    - for JSON response, now returns ResultStatus."^

"async def get_current_user(...):"^

"    - uses [ user = Depends(get_logged_in_user), ]"^

"    - uses verify_user_scopes(...)"
~~~

$ git add .\src\fastapi_learning\controllers\auth.py
$ git commit -m "Standardised JSON response via ResultStatus. General refactoring. Improved logic." -m "Updates include:"^

"All JSON responses are returned via ResultStatus."^

"Removed def __login_page_context(...)."^

"Completely rewrote async def login_page(...)."^

"New def __login_response(...) replaces def __login_page(...)."^

"Refactored async def home_page(...):"^

"    - uses [user = Depends(get_logged_in_user)]"^

"Removed helper method def __home_page(...)."^

"Refactored async def login(...) -- check for access token exists, if it does then call get_logged_in_user(...)."^

"Refactored async def logout(request: Request):"^

"    - stores redirect message in session under the key login_redirect_msg."^

"    - redirects state is now LOGIN_REDIRECT_STATE_CERTAIN."
~~~

$ git add .\src\fastapi_learning\controllers\employees_admin.py
$ git commit -m "Standardised JSON response via ResultStatus. General refactoring. Improved logic." -m "Update as follows:"^

"In all methods where applicable:"^

"    user: Annotated[LoggedInEmployee, Depends(get_cached_logged_in_user)]"^

"replaced ( token: Annotated[str, Depends(oauth2_scheme)] )."
~~~

$ git add .\tests\integration\test_admin_itgt.py
$ git commit -m "Standardised JSON response via ResultStatus. General refactoring. Improved logic." -m "Updates include:"^

"Fixed test_integration_invalid_credentials_admin_own_detail_json(test_client):"^

"    - pass emp_no to token payload."^

"Fixed test_integration_valid_admin_own_detail_json(test_client):"^

"    - calls ( assert PasswordHasher().verify(status['password'], 'password') == True )."^

"Refactored:"^

"    - def test_integration_not_auth_admin_own_detail_json(test_client): JSON via ResultStatus."^

"    - def test_integration_invalid_credentials_admin_own_detail_json(test_client): JSON via ResultStatus."^

"    - def test_integration_not_auth_admin_own_detail_html(test_client): message condition."^

"    - def test_integration_invalid_credentials_admin_own_detail_html(test_client): message condition."^

"    - def test_integration_valid_admin_own_detail_json(test_client): JSON via ResultStatus."
~~~

$ git add .\tests\integration\test_api_itgt.py
$ git commit -m "Standardised JSON response via ResultStatus. General refactoring. Improved logic." -m "Updates include:"^

"Fixed test_integration_valid_admin_own_detail(test_client):"^

"    - calls ( assert PasswordHasher().verify(status['password'], 'password') == True )."^

"Refactored:"^

"    - def test_integration_valid_admin_own_detail(test_client): JSON via ResultStatus."^

"    - def test_integration_valid_login(test_client): JSON via ResultStatus."
~~~

$ git add .\tests\integration\test_expired_jwt.py
$ git commit -m "Standardised JSON response via ResultStatus. General refactoring. Improved logic." -m "Updates include:"^

"Refactored def test_expired_jwt_json_response(test_client): JSON via ResultStatus."^

"Rewrote def test_expired_jwt_html_response(test_client):"^

"    - the returned HTML now is the login page."
~~~

$ git add .\tests\integration\test_scope_permission_itgt.py
$ git commit -m "Standardised JSON response via ResultStatus. General refactoring. Improved logic." -m "Updates include:"^

"def test_scope_permission_invalid_json(test_client): JSON via ResultStatus."^

"def test_scope_permission_api_me(test_client): JSON via ResultStatus."^

"Refactored related to path /auth/token:"^

"    - def test_scope_permission_login_01(test_client): JSON via ResultStatus."^

"    - def test_scope_permission_login_02(test_client): JSON via ResultStatus."^

"    - def test_scope_permission_login_03(test_client): JSON via ResultStatus."
~~~

$ git add .\tests\integration\test_auth_itgt.py
$ git commit -m "Standardised JSON response via ResultStatus. General refactoring. Improved logic." -m "Updates include:"^

" On JSON error responses:"^

"    - def test_integration_login_bad_email_json(test_client)."^

"    - def test_integration_login_bad_password_json(test_client)."^

"    - def test_integration_invalid_username_login_json(test_client)."^

"    - def test_integration_invalid_password_login_json(test_client)."^

"On JSON valid responses:"^

"    - def test_integration_valid_login_json(test_client)."^

"Replaces some literals with already defined constants."
~~~

$ git add .\src\fastapi_learning\templates\admin\me.html
$ git commit -m "Standardised JSON response via ResultStatus. General refactoring. Improved logic." -m "Displaying added new fields employee number and scopes."
~~~

$ git add .\src\fastapi_learning\templates\auth\home.html
$ git add .\src\fastapi_learning\templates\emp\search.html
$ git add .\src\fastapi_learning\templates\emp\search_result.html
$ git add .\src\fastapi_learning\templates\emp\insert.html
$ git add .\src\fastapi_learning\templates\emp\update.html
$ git commit -m "Standardised JSON response via ResultStatus. General refactoring. Improved logic." -m "Use new method def get_ui_states(...). ( Stopped using def has_required_scopes(...) )."

~~~

$ git add README.md
$ git commit -m "Standardised JSON response via ResultStatus. General refactoring. Improved logic." -m "Updates include:"^

"    - added [ Implemented routes ] section."^

"    - added post [ Python FastAPI: Finishing Off the Pending Items, Code Cleanup, and Improvements ]"
~~~

$ git branch -M main
$ git push -u origin main
~~~

$ git tag -a v0.13.0 -m "Added post [ Python FastAPI: Finishing Off the Pending Items, Code Cleanup, and Improvements ]"
$ git push origin --tags

$ git tag
```

<a id="on-test-modules"></a>
<p>
❹ Please take note of the following regarding the test modules: 
A majority of the refactoring centers around JSON responses returned via 
<a href="https://bh-apistatus.readthedocs.io/en/latest/result-status.html#bh_apistatus.result_status.ResultStatus" 
title="bh_apistatus.result_status.ResultStatus class" target="_blank"><code>ResultStatus</code></a>. 
Therefore, we have to check <code>['status']['code']</code> to get the actual returned HTTP code, 
as <code>status_code</code> is always <code>HTTP_200_OK</code>. For example:
</p>

```python
        ...
        login_response = test_client.post('/auth/token', data=login_data)

        assert login_response != None
        # assert login_response.status_code == http_status.HTTP_400_BAD_REQUEST
        assert login_response.status_code == http_status.HTTP_200_OK

        status = login_response.json()

        # Should always check for this.
        assert status['status']['code'] == http_status.HTTP_500_INTERNAL_SERVER_ERROR
        assert status['status']['text'] == BAD_LOGIN_MSG
		...
```

<a id="concluding-remarks"></a>
<p>
❺ I believe this is the final post of this series. We have explored some essential features 
of the <a href="https://fastapi.tiangolo.com/" title="FastAPI" target="_blank">FastAPI</a> 
framework. If I find something else interesting about it in the future, we might revisit 
this series once again.
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
<a href="https://www.omgubuntu.co.uk/2024/03/ubuntu-24-04-wallpaper" target="_blank">https://www.omgubuntu.co.uk/2024/03/ubuntu-24-04-wallpaper</a>
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
