---
layout: post
title: "Python FastAPI: Implementing JSON Web Token"

description: Continuing with our Python FastAPI learning series, we will implement proper JSON Web Token (JWT) authentication as discussed in the official tutorial, with a few minor tweaks of our own. 

tags:
- Python 
- FastAPI
- JSON Web Token
- JWT
---

<em>
Continuing with our <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Python FastAPI Complete Series" target="_blank">Python FastAPI learning series</a>, we will implement proper JSON Web Token (JWT) authentication as discussed in <a href="https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/" title="OAuth2 with Password (and hashing), Bearer with JWT tokens" target="_blank">the official tutorial</a>, with a few minor tweaks of our own.
</em>

<h3>
🐍 <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![121-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/09/121-feature-image.png) |
|:--:|
| *Python FastAPI: Implementing JSON Web Token* |

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
git clone -b v0.9.0 https://github.com/behai-nguyen/fastapi_learning.git
```

<a id="prologue"></a>
<p>
❶ Please note 🙏 that the code presented in this post is not my own. 
It is taken from the following official tutorial page, with a few tweaks: 
<a href="https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/" 
title="OAuth2 with Password (and hashing), Bearer with JWT tokens" 
target="_blank">OAuth2 with Password (and hashing), Bearer with JWT tokens</a>.
</p>

<p>
I am working towards implementing some new functionalities that would make 
sense with JSON Web Token (JWT) authentication. It would be easier to read if 
we break them down into individual shorter posts. Hence, this article.
</p>

<p>
Please also note that the JWT authentication implemented by the official example 
is valid for a fixed duration. After this duration, the JWT expires (i.e., becomes invalid), 
and users will need to authenticate again to use the application.
</p>

<p>
I have previously implemented JWT 
<a href="https://behainguyen.wordpress.com/2024/02/26/rust-actix-web-json-web-token-authentication/#jwt-implementations" 
title="Proposed JWT Implementations: Problems and Solutions" target="_blank">whose expiry 
is calculated based on the last access time</a>. It proved complicated. In this post, we 
will stick with the implementation from the official tutorial.
</p>

<a id="project-layout"></a>
<p>
❸ The full updated structure of the project is outlined below. 
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
├── .env ★
├── logger_config.yaml
├── main.py
├── pyproject.toml ★
├── pytest.ini ★
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
│       │   ├── jwt_utils.py ☆
│       │   └── queue_logging.py
│       ├── controllers
│       │   ├── admin.py ★
│       │   ├── auth.py ★
│       │   └── __init__.py
│       ├── __init__.py
│       ├── models
│       │   └── employees.py
│       ├── static
│       │   └── styles.css
│       └── templates
│           ├── admin
│           │   └── me.html
│           ├── auth
│           │   ├── home.html
│           │   └── login.html
│           ├── base.html
│           └── templates
│               ├── admin
│               │   └── me.html
│               ├── auth
│               │   ├── home.html
│               │   └── login.html
│               └── base.html
└── tests
    ├── business
    │   └── test_employees_mgr.py
    ├── conftest.py
    ├── __init__.py
    ├── integration
    │   ├── test_admin_itgt.py ★
    │   ├── test_api_itgt.py ★
    │   ├── test_auth_itgt.py ★
    │   └── test_expired_jwt.py ☆
    ├── README.md
    └── unit
        └── test_employees.py
```

<a id="code-refactorings"></a>
<p>
❸ In this section, we will discuss the code changes.
</p>

<a id="code-refac-env"></a>
<p>
⓵ The <a href="https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/" 
title="OAuth2 with Password (and hashing), Bearer with JWT tokens" 
target="_blank">tutorial example</a> defines three constants 
<code>SECRET_KEY</code>, <code>ALGORITHM</code>, and <code>ACCESS_TOKEN_EXPIRE_MINUTES</code>.
We move them into the environment 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/aa042206d4af5a1b1c2c3ce2c8bedebf50a5727c/.env#L16-L21" 
title="The environment file .env" target="_blank"><code>.env</code> file</a> 
as follows: 
</p>

<figure class="highlight"><pre><code class="language-cfg" data-lang="cfg"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">16
17
18
19
20
21
</pre></td><td class="code"><pre># to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "61973d7ebb87638191435feaed4789a0c0ba173bd102f2c1f940344d9745a8be"
ALGORITHM = "HS256"
# 30 * 60 = 30 minutes.
ACCESS_TOKEN_EXPIRE_SECONDS = 1800
</pre></td></tr></tbody></table></code></pre></figure>

<p>
The unit of <code>ACCESS_TOKEN_EXPIRE_SECONDS</code> is seconds, which provides 
better control over the JWT lifetime, especially in tests, as we 
<a href="#code-refac-new-itgt-test">shall see later</a>.
</p>

<a id="code-refac-pyproj"></a>
<p>
⓶ The 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/aa042206d4af5a1b1c2c3ce2c8bedebf50a5727c/pyproject.toml#L27" 
title="The pyproject.toml file" target="_blank"><code>pyproject.toml</code></a> 
file now includes the required package 
<a href="https://pyjwt.readthedocs.io/en/stable/" title="PyJWT" target="_blank">pyjwt</a>,  
as per the 
<a href="https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/" 
title="OAuth2 with Password (and hashing), Bearer with JWT tokens" 
target="_blank">aforementioned tutorial</a>.
</p>

<a id="code-new-jwt-utils"></a>
<p>
⓷ In the new module 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/aa042206d4af5a1b1c2c3ce2c8bedebf50a5727c/src/fastapi_learning/common/jwt_utils.py" 
title="JWT management functions common/jwt_utils.py" 
target="_blank"><code>common/jwt_utils.py</code></a>, we house 
the two methods 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/aa042206d4af5a1b1c2c3ce2c8bedebf50a5727c/src/fastapi_learning/common/jwt_utils.py#L16-L27" 
title="def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None)" 
target="_blank"><code>create_access_token(...)</code></a> and
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/aa042206d4af5a1b1c2c3ce2c8bedebf50a5727c/src/fastapi_learning/common/jwt_utils.py#L29-L47" 
title="def decode_access_token(token: str) -> Union[TokenData, HTTPException]" 
target="_blank"><code>decode_access_token(...)</code></a> taken 
from the <a href="https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/" 
title="OAuth2 with Password (and hashing), Bearer with JWT tokens" 
target="_blank">official tutorial</a>.
</p>

<p>
We made a change to the method <code>create_access_token(...)</code>. If the 
value for the <code>expires_delta</code> parameter is <code>None</code>, we 
use the value of <code>ACCESS_TOKEN_EXPIRE_SECONDS</code> from the environment 
file.
</p>

<a id="code-refac-controllers"></a>
<p>
⓸ In the 
<a href="https://github.com/behai-nguyen/fastapi_learning/tree/aa042206d4af5a1b1c2c3ce2c8bedebf50a5727c/src/fastapi_learning/controllers" 
title="fastapi_learning/controllers" 
target="_blank"><code>/controllers</code></a> area, we made the changes discussed below:
</p>

<p>
● In the module 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/aa042206d4af5a1b1c2c3ce2c8bedebf50a5727c/src/fastapi_learning/controllers/auth.py" 
title="controllers/auth.py" target="_blank"><code>auth.py</code></a>, the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/aa042206d4af5a1b1c2c3ce2c8bedebf50a5727c/src/fastapi_learning/controllers/auth.py#L106-L177" 
title="async def login(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Union[Token, None]" 
target="_blank"><code>login(...)</code></a> method now calls the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/aa042206d4af5a1b1c2c3ce2c8bedebf50a5727c/src/fastapi_learning/common/jwt_utils.py#L16-L27" 
title="def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None)" 
target="_blank"><code>create_access_token(...)</code></a> to create 
the JWT access token.
</p>

<p>
● In the module 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/aa042206d4af5a1b1c2c3ce2c8bedebf50a5727c/src/fastapi_learning/controllers/admin.py" 
title="controllers/admin.py" target="_blank"><code>admin.py</code></a>, the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/aa042206d4af5a1b1c2c3ce2c8bedebf50a5727c/src/fastapi_learning/controllers/admin.py#L53-L85" 
title="async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)])" 
target="_blank"><code>get_current_user(...)</code></a> method calls 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/aa042206d4af5a1b1c2c3ce2c8bedebf50a5727c/src/fastapi_learning/common/jwt_utils.py#L29-L47" 
title="def decode_access_token(token: str) -> Union[TokenData, HTTPException]" 
target="_blank"><code>decode_access_token(...)</code></a> to validate 
incoming requests.
</p>

<a id="code-refac-existing-itgt-tests"></a>
<p>
⓹ In the existing 
<a href="https://github.com/behai-nguyen/fastapi_learning/tree/aa042206d4af5a1b1c2c3ce2c8bedebf50a5727c/tests/integration" 
title="tests/integration" target="_blank"><code>tests/integration</code></a> area, 
all tests remain in place with some minor updates to work with the new JWT implementation.
</p>

<a id="code-refac-new-itgt-test"></a>
<p>
⓺ 💥 We added a new integration test module 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/aa042206d4af5a1b1c2c3ce2c8bedebf50a5727c/tests/integration/test_expired_jwt.py" 
title="The integration test_expired_jwt.py module" target="_blank"><code>test_expired_jwt.py</code></a>.
These tests ascertain that when a request comes in with an already expired JWT token, 
the request is denied as expected. 
As <a href="#code-refac-env">mentioned earlier</a>, 
we take advantage of setting the value of the environment variable 
<code>ACCESS_TOKEN_EXPIRE_SECONDS</code> to only a couple of seconds to simulate expiry in these tests. For example:
</p>

```python
        ...
        # Login access token expires in 2 seconds.
        os.environ['ACCESS_TOKEN_EXPIRE_SECONDS'] = '2'

        # Login.
        login_response = login('behai_nguyen@hotmail.com', 'password', test_client)

        # Set session (Id) for next request.
        session_cookie = login_response.cookies.get('session')
        test_client.cookies = {'session': session_cookie}

        # Waits out for the access token to expire.
        time.sleep(3)

        response = test_client.get('/admin/me')
        ...
```

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
