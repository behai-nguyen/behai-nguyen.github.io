---
layout: post
title: "Python FastAPI: Fixing a Bug in the Authentication Process"

description: In the fourth post of our Python FastAPI learning series, we introduced a bug in the authentication process. In this post, we describe the bug and discuss how to fix it. 

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/08/120-01-the-bug.png"

gallery-image-list-2:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/08/120-02-bug-fxed-a.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/08/120-02-bug-fxed-b.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/08/120-02-bug-fxed-c.png"	

tags:
- Python
- FastAPI
- Database
- MySQL
- PostgreSQL
- MariaDB
---

<em>
In the <a href="https://behainguyen.wordpress.com/2024/06/11/python-fastapi-complete-authentication-flow-with-oauth2-security/" title="Python FastAPI: Complete Authentication Flow with OAuth2 Security" target="_blank">fourth post</a> of our <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Python FastAPI Complete Series" target="_blank">Python FastAPI learning series</a>, we introduced a bug in the authentication process. In this post, we describe the bug and discuss how to fix it.
</em>

<h3>
🐍 <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![120-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/08/120-feature-image.png) |
|:--:|
| *Python FastAPI: Fixing a Bug in the Authentication Process* |

The code requires Python 3.12.4. Please refer to the 
<a href="https://github.com/behai-nguyen/fastapi_learning#the-code-after-tag-v040-requires-python-3124" 
title="The Code After Tag v0.4.0 Requires Python 3.12.4" target="_blank">following 
discussion</a> on how to upgrade to Python 3.12.4.

🚀 <strong>Please note,</strong> complete code for this post
can be downloaded from GitHub with:

```
git clone -b v0.8.0 https://github.com/behai-nguyen/fastapi_learning.git
```

<a id="bug-description"></a>
❶ The bug occurs when we log in using the Swagger UI <code>Authorize</code> button. The authentication process is successful, but the following error appears on the Swagger UI screen:

<code>
<span class="danger-text">
auth error SyntaxError: JSON.parse: unexpected character at line 1 column 1 of the JSON data
</span>
</code>

Please see the screenshot illustration below:

{% include image-gallery.html list=page.gallery-image-list-1 %}
<br/>

It is expecting a JSON response, but the response defaults to HTML.

To get this functionality to work correctly, the endpoint handler method for the 
<code>https://0.0.0.0:port/auth/token</code> path should default to return JSON 
as per the original example. It should only return HTML (the home page) when 
explicitly requested.

<a id="the-bug-fix"></a>
❷ After some consideration, I have decided to use an additional hidden field alongside 
the <code>username</code> and <code>password</code> fields. If this hidden field is 
present and its value is <code>text/html</code>, then we return the HTML home page.

Since we have already used the custom header field 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/common/consts.py#L5" 
title="The FORMAT_HEADER constant" target="_blank"><code>x-expected-format</code></a> 
to check for a 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/e419563bcdbf3ca0c384bf2ae2e5b4ad92b82451/src/fastapi_learning/controllers/__init__.py#L30-L35"
title="The json_req(request: Request) method" target="_blank">JSON response</a>, 
we will adopt this custom header field as our new hidden field as well.

<a id="the-bug-fix-const-named-change"></a>
We will change <code>x-expected-format</code>'s constant name to 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/3f365ae78290176fd703a3d739ac8a4e4d2688fd/src/fastapi_learning/common/consts.py#L5" 
title="Renamed to RESPONSE_FORMAT from FORMAT_HEADER" target="_blank"><code>RESPONSE_FORMAT</code></a> 
from <code>FORMAT_HEADER</code> to be more generically appropriate.

<a id="project-layout"></a>
❸ We will make changes to only a few files. There are no new files. Below is the list of the updated files.

<strong>-- Please note,</strong> those marked with <span style="font-size:1.5em;">★</span> 
are updated, and those marked with <span style="font-size:1.5em;">☆</span> are new.

```
/home/behai/fastapi_learning/
.
├── README.md ★
├── src
│   └── fastapi_learning
│       ├── common
│       │   └── consts.py ★
│       ├── controllers
│       │   ├── auth.py ★
│       │   └── __init__.py ★
│       ├── __init__.py ★
│       └── templates
│           └── auth
│               └── login.html ★
└── tests
    └── integration
        ├── test_admin_itgt.py ★
        └── test_auth_itgt.py ★
```

<a id="code-refactorings"></a>
❹ In this section, we will discuss the code changes.

⓵ <a href="https://github.com/behai-nguyen/fastapi_learning/blob/3f365ae78290176fd703a3d739ac8a4e4d2688fd/src/fastapi_learning/common/consts.py" 
title="The common/consts.py module" target="_blank"><code>common/consts.py</code></a>: 
We just renamed a constant as <a href="#the-bug-fix-const-named-change">previously described</a>.

⓶ <a href="https://github.com/behai-nguyen/fastapi_learning/blob/3f365ae78290176fd703a3d739ac8a4e4d2688fd/src/fastapi_learning/__init__.py" 
title="The fastapi_learning/__init__.py module" 
target="_blank"><code>fastapi_learning/__init__.py</code></a>: We added the classes 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/3f365ae78290176fd703a3d739ac8a4e4d2688fd/src/fastapi_learning/__init__.py#L23-L26" 
title="class Token" target="_blank"><code>Token</code></a>
and 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/3f365ae78290176fd703a3d739ac8a4e4d2688fd/src/fastapi_learning/__init__.py#L28-L30" 
title="class TokenData" target="_blank"><code>TokenData</code></a> 
as per the later official tutorials, starting with  
<a href="https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/" 
title="OAuth2 with Password (and hashing), Bearer with JWT tokens" 
target="_blank">OAuth2 with Password (and hashing), Bearer with JWT tokens</a>. 
In the <code>Token</code> class, we have an additional <code>detail</code> 
string field for informational purposes. We added them to this package file so 
that they are accessible by all other modules in the application.

⓷ <a href="https://github.com/behai-nguyen/fastapi_learning/blob/3f365ae78290176fd703a3d739ac8a4e4d2688fd/src/fastapi_learning/controllers/__init__.py" 
title="The controllers/__init__.py module" 
target="_blank"><code>controllers/__init__.py</code></a>: We added a new method 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/3f365ae78290176fd703a3d739ac8a4e4d2688fd/src/fastapi_learning/controllers/__init__.py#L37-L48" 
title="async def html_req(request: Request)" 
target="_blank"><code>async def html_req(request: Request)</code></a> as 
discussed <a href="#the-bug-fix">previously</a>. Note that we check both the 
request headers and the field list for <code>x-expected-format</code>, with request headers having higher precedence.

⓸ <a href="https://github.com/behai-nguyen/fastapi_learning/blob/3f365ae78290176fd703a3d739ac8a4e4d2688fd/src/fastapi_learning/controllers/auth.py" 
title="The controllers/auth.py module" 
target="_blank"><code>controllers/auth.py</code></a>: We made the following 
refactorings to 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/3f365ae78290176fd703a3d739ac8a4e4d2688fd/src/fastapi_learning/controllers/auth.py#L105-L175" 
title="The async def login(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) method" 
target="_blank"><code>async def login(...)</code></a>: 

<span style="font-size:1.5em;font-weight:bold;">⑴</span> Annotated the return value as <code>Union[Token, None]</code>. 

<span style="font-size:1.5em;font-weight:bold;">⑵</span> The sub-method 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/3f365ae78290176fd703a3d739ac8a4e4d2688fd/src/fastapi_learning/controllers/auth.py#L143-L156" 
title="The async def bad_login(op_status: ResultStatus) sub-method" 
target="_blank"><code>async def bad_login(...)</code></a> refactored to:

```python
    async def bad_login(op_status: ResultStatus):
        ...

        if await html_req(request):
            return RedirectResponse(url=f"{router.url_path_for('login_page')}?state={op_status.code}", 
                                    status_code=status.HTTP_303_SEE_OTHER)        
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail=message)
```

Previously, it was:

```python
    def bad_login(op_status: ResultStatus):
        ...

        if json_req(request):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail=message)
        else:
            return RedirectResponse(url=f"{router.url_path_for('login_page')}?state={op_status.code}", 
                                    status_code=status.HTTP_303_SEE_OTHER)
```

<span style="font-size:1.5em;font-weight:bold;">⑶</span> Fixed the two return statements to: 

```python
        return RedirectResponse(url=router.url_path_for('home_page'), status_code=status.HTTP_303_SEE_OTHER) \
            if await html_req(request) else \
                Token(access_token=request.session["access_token"], token_type="bearer", detail=LOGGED_IN_SESSION_MSG)
...				
    return RedirectResponse(url=router.url_path_for('home_page'), status_code=status.HTTP_303_SEE_OTHER) \
        if await html_req(request) else Token(access_token=user_username, token_type="bearer", detail="")
```

The default response is always JSON. It will only return the HTML home page if explicitly 
requested. In the previous revisions, they were:

```python
        return {"detail": LOGGED_IN_SESSION_MSG} if json_req(request) \
            else RedirectResponse(url=router.url_path_for('home_page'), status_code=status.HTTP_303_SEE_OTHER)
...
    return {"access_token": user_username, "token_type": "bearer"} \
        if json_req(request) \
        else RedirectResponse(url=router.url_path_for('home_page'), status_code=status.HTTP_303_SEE_OTHER)
```

⓹ <a href="https://github.com/behai-nguyen/fastapi_learning/blob/3f365ae78290176fd703a3d739ac8a4e4d2688fd/src/fastapi_learning/templates/auth/login.html#L29" 
title="templates/auth/login.html page" 
target="_blank"><code>templates/auth/login.html</code></a>: 
We added the hidden field as <a href="#the-bug-fix">previously described</a>.

⓺ <a href="https://github.com/behai-nguyen/fastapi_learning/blob/3f365ae78290176fd703a3d739ac8a4e4d2688fd/tests/integration/test_auth_itgt.py" 
title="The tests/integration/test_auth_itgt.py module" 
target="_blank"><code>tests/integration/test_auth_itgt.py</code></a></a>: We 
added the hidden field to the login data in the following methods:

<ul>
<li style="margin-top:10px;">
<code>test_integration_valid_login_html</code>
</li>
<li style="margin-top:10px;">
<code>test_integration_valid_login_twice</code>
</li>
<li style="margin-top:10px;">
<code>test_integration_login_bad_email_html</code>
</li>
<li style="margin-top:10px;">
<code>test_integration_invalid_username_login_html</code>
</li>
<li style="margin-top:10px;">
<code>test_integration_invalid_password_login_html</code>
</li>
</ul>

<a href="https://github.com/behai-nguyen/fastapi_learning/blob/3f365ae78290176fd703a3d739ac8a4e4d2688fd/tests/integration/test_admin_itgt.py" 
title="The tests/integration/test_admin_itgt.py" 
target="_blank"><code>tests/integration/test_admin_itgt.py</code></a></a>: 
We updated the constant name to 
<a href="#the-bug-fix-const-named-change"><code>RESPONSE_FORMAT</code></a>. No other changes.

<a id="the-bug-fixed"></a>
❺ The screenshots below show that the bug has been fixed:

{% include image-gallery.html list=page.gallery-image-list-2 %}
<br/>

<a id="concluding-remarks"></a>
❻ Thank you for reading. Stay safe, as always.

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
<li>
<a href="https://www.flaticon.com/free-icon/bug-fixing_15511" target="_blank">https://www.flaticon.com/free-icon/bug-fixing_15511</a>
</li>
</ul>

<h3>
🐍 <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>
