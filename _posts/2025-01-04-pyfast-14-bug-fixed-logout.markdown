---
layout: post
title: "Python FastAPI: Bug Fixing the Logout Process and Redis Session Cleanup"

description: While experimenting with some CLI clients for the server implemented in this Python FastAPI learning series, I found two similar bugs in the server&#58; both were related to Redis session entries not being cleaned up. The first bug involves some temporary redirection entries that do not get removed after the requests are completed. The second, more significant bug, is that the logout process does not clean up the session entry if the incoming request has only the access token and no session cookies. We address both of these bugs in this post, with most of the focus on the second one. 

tags:
- Python
- FastAPI
- OAuth2
- JSON Web Token
- JWT
---

<em>
While experimenting with some CLI clients for the server implemented in this <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Python FastAPI learning series</a>, I found two similar bugs in the server: both were related to Redis session entries not being cleaned up.
</em>

<em>
The first bug involves some temporary redirection entries that do not get removed after the requests are completed. The second, more significant bug, is that the logout process does not clean up the session entry if the incoming request has only the access token and no session cookies.
</em>

<em>
We address both of these bugs in this post, with most of the focus on the second one.
</em>

<h3>
🐍 <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![131-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/01/131-feature-image.png) |
|:--:|
| *Python FastAPI: Bug Fixing the Logout Process and Redis Session Cleanup* |

The code requires Python 3.12.4. Please refer to the 
<a href="https://github.com/behai-nguyen/fastapi_learning#the-code-after-tag-v040-requires-python-3124" 
title="The Code After Tag v0.4.0 Requires Python 3.12.4" target="_blank">following 
discussion</a> on how to upgrade to Python 3.12.4.

🚀 <strong>Please note,</strong> complete code for this post
can be downloaded from GitHub with:

```
git clone -b v0.14.0 https://github.com/behai-nguyen/fastapi_learning.git
```

<a id="problem-definition"></a>
❶ <strong>Problem Description and Proposed Solution</strong>

The above problems are in the current version, which is <code>v0.13.0</code>, available for cloning with the following command:

```
git clone -b v0.13.0 https://github.com/behai-nguyen/fastapi_learning.git
```

There are two problems:

<a id="problem-def-01"></a>
⓵ Temporary entries that store redirection data between requests do not get removed from Redis storage. This was simple to resolve—just remove the entries after retrieval. We will not go into this any further.

<a id="problem-def-02"></a>
⓶ Logout does not work with the access token, leaving the Redis session entry behind after logging out.

I understood this issue as early as in the 
<a href="https://behainguyen.wordpress.com/2024/05/21/python-fastapi-implementing-persistent-stateful-http-sessions-with-redis-session-middleware-and-extending-oauth2passwordbearer-for-oauth2-security/#session-loading" 
title="Python FastAPI: Implementing Persistent Stateful HTTP Sessions with Redis Session Middleware and Extending OAuth2PasswordBearer for OAuth2 Security" 
target="_blank">third post</a>:

> Subsequent requests from this same <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-authenticated-session" title="authenticated session" target="_blank"><code>authenticated session</code></a> should include the <code>session</code> UUID cookie as <a href="https://behainguyen.wordpress.com/2024/05/21/python-fastapi-implementing-persistent-stateful-http-sessions-with-redis-session-middleware-and-extending-oauth2passwordbearer-for-oauth2-security/#starsessions-lib" title="Python FastAPI: Implementing Persistent Stateful HTTP Sessions with Redis Session Middleware and Extending OAuth2PasswordBearer for OAuth2 Security" target="_blank">discussed</a>. The session middleware then uses this UUID to load the actual session content from the Redis store, making the <code>access_token</code> available in the incoming request's <code>request.session</code> property.

<strong>Logout request must include the <code>session</code> UUID cookie.</strong>

When used as an 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-app-server" 
title="application server" target="_blank"><code>application server</code></a>, 
browsers automatically include this cookie. When used as an 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-api-server" 
title="API-like server or a service" 
target="_blank"><code>API-like server</code> or a <code>service</code></a>, 
we must manually include this cookie in the request. 
<strong>Due to a massive oversight, I forgot this issue until it was too late.</strong> 
Let's illustrate the problem with the following script:

<a id="problem-def-02-script-example"></a>
```python
import urllib3

COOKIE: str = None
ACCESS_TOKEN: str = None

def login(http: urllib3.PoolManager, username: str, password: str):

    global COOKIE
    global ACCESS_TOKEN

    # Assuming always succeeds.
    resp = http.request(
        "POST",
        "https://localhost:5000/api/login",
        fields={"username": username, "password": password}
    )

    status = resp.json()

    """
    An example of server response cookie resp.headers['Set-Cookie']:
        session=4441b57be81e7f8ec37b40652b0a8039; path=/; httponly; samesite=lax

    while resp.info().get_all('Set-Cookie') is a list:
        ['session=4441b57be81e7f8ec37b40652b0a8039; path=/; httponly; samesite=lax']
    """

    COOKIE = resp.headers['Set-Cookie']
    ACCESS_TOKEN = status['data']['access_token']

def logout_01(http: urllib3.PoolManager, response_cookie: str):
    """
    This logout request deletes the Redis session entry.
    """

    http.request(
        "POST",
        "https://localhost:5000/auth/logout",
        headers={
            "Cookie": response_cookie,
            "x-expected-format": "application/json",
        }
    )

def logout_02(http: urllib3.PoolManager, access_token: str):
    """
    This logout request DOES NOT delete the Redis session entry.
    """

    http.request(
        "POST",
        "https://localhost:5000/auth/logout",
        headers={
            "Authorization": f"Bearer {access_token}",
            "x-expected-format": "application/json",
        }
    )

urllib3.disable_warnings()
http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)

login(http, 'behai_nguyen@hotmail.com', 'password')

print(f"COOKIE: {COOKIE}")
print(f"ACCESS_TOKEN: {ACCESS_TOKEN}")

logout_01(http, COOKIE)
# logout_02(http, ACCESS_TOKEN)
```

For more information on 
<a href="https://pypi.org/project/urllib3/" title="The urllib3 library" target="_blank">urllib3</a> and 
SSL/HTTPS, please see the following article: 
<a href="https://behainguyen.wordpress.com/2024/12/17/the-python-urllib3-http-library-and-ssl-https-for-localhost/" 
title="The Python urllib3 HTTP Library and SSL/HTTPS for localhost" 
target="_blank">The Python urllib3 HTTP Library and SSL/HTTPS for localhost</a>.

<a id="problem-def-02-script-example-run"></a>
Let's run the above script as follows:

<ol>
<li style="margin-top:10px;">
Call <code>login(...)</code>, then <code>logout_01(http, COOKIE)</code>: 
<a href="https://redis.io/insight/" title="Redis Insight" target="_blank">Redis Insight</a> 
shows that the session entry gets removed, leaving nothing behind.
<br/><br/>
💥 At the the server-side, <strong><em>the cookie identifies the access token. This makes it unnecessary for the client to remember the access token; they only need to remember the cookie.</em></strong>
</li>

<li style="margin-top:10px;">
Call <code>login(...)</code>, then <code>logout_02(http, ACCESS_TOKEN)</code>: The 
session entry <strong>did not</strong> get removed. In addition, an additional entry 
with a different <code>session</code> UUID was created. This entry stores the redirection data, which also gets fixed in this post: delete the entry when the data gets retrieved.
</li>
</ol>	

<a id="problem-def-02-access-token-proposed-solution"></a>
⓷ <strong>The Proposed Solution for the Access Token Problem</strong>

👉 The proposed solution is to include the session UUID in the access token payload.

All other endpoints that expect the access token will work as they currently do. 
The only endpoint that needs refactoring is the logout endpoint: If the request includes 
the <code>session</code> UUID, then use it to manage the Redis session entry. 
Otherwise, decode the access token, ignoring expiration and any other errors, 
then use the session UUID included in the access token payload to manage the Redis session entry. 
This proposed solution also ensures that, when used as an 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-app-server" 
title="application server" target="_blank"><code>application server</code></a>, 
browser cookies work as they normally do.

💥 Please note ahead that this proposed solution raises some more issues, which I haven't found elegant solutions to. I settled for some workarounds, which are discussed in a 
<a href="#code-refactorings">a later section</a>.

<a id="project-layout"></a>
❷ No new files were added. The current structure of the project is outlined below.

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
├── pyproject.toml
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
│       │   ├── consts.py
│       │   ├── jwt_utils.py ★
│       │   ├── queue_logging.py
│       │   └── scope_utils.py
│       ├── controllers
│       │   ├── admin.py ★
│       │   ├── auth.py ★
│       │   ├── employees_admin.py ★
│       │   ├── __init__.py ★
│       │   └── required_login.py ★
│       ├── __init__.py ★
│       ├── models
│       │   └── employees.py
│       ├── static
│       │   └── js
│       │       └── application.js
│       └── templates
│           ├── admin
│           │   └── me.html
│           ├── auth
│           │   ├── home.html
│           │   └── login.html
│           ├── base.html
│           └── emp
│               ├── insert.html
│               ├── search.html
│               ├── search_result.html
│               └── update.html
└── tests
    ├── business
    │   ├── test_employees_mgr.py
    │   ├── test_employees_validation.py
    │   └── test_scope_utils.py
    ├── conftest.py
    ├── __init__.py
    ├── integration
    │   ├── test_admin_itgt.py
    │   ├── test_api_itgt.py
    │   ├── test_auth_itgt.py
    │   ├── test_employees_itgt.py
    │   ├── test_expired_jwt.py
    │   ├── test_scope_permission_itgt.py
    │   └── test_scope_ui_itgt.py
    ├── README.md
    └── unit
        └── test_employees.py
```

<a id="code-refactorings"></a>
❸ <strong>Code Refactorings</strong>

<a id="code-reftr-session-id"></a>
⓵ <strong>Accessing the <code>session</code> UUID to Include in the Access Token Payload</strong>

I have looked through the 
<a href="https://pypi.org/project/starsessions/" 
title="starsessions" target="_blank">starsessions</a> library documentation and code, 
and I could not find a way to generate the <code>session</code> UUID 
in advance of access token creation. 
In the current version (<code>v0.13.0</code>), after calling 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/436c732e248d84876cfa11863c639f0e3d5abab4/src/fastapi_learning/controllers/auth.py#L208" 
title="The login(...) endpoint handler method" 
target="_blank"><code>set_access_token(request, access_token)</code></a>,
the <code>session</code> UUID is still not accessible, at least from my understanding.
It is first available after redirecting to 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/436c732e248d84876cfa11863c639f0e3d5abab4/src/fastapi_learning/controllers/auth.py#L210-L214" 
title="The login(...) endpoint handler method" target="_blank"><code>/auth/token</code></a>, 
i.e., the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/436c732e248d84876cfa11863c639f0e3d5abab4/src/fastapi_learning/controllers/auth.py#L126-L138" 
title="The home_page(...) endpoint handler method" target="_blank"><code>home_page(...)</code></a> 
endpoint handler method.

As we also redirect to the <code>home_page(...)</code> under different scenarios, 
we cannot create the access token there. Instead, we redirect to a “private” endpoint, 
create and set the access token in this endpoint handler method, and then redirect to the 
<code>/auth/token</code> endpoint as before.

<a id="code-reftr-login-process"></a>
⓶ <strong>Refactoring the login process</strong>

Within the <code>login(...)</code> endpoint handler method, 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/b2caf207cfea2bd92565eaa981479993996c799b/src/fastapi_learning/controllers/auth.py#L303-L327" 
title="The login(...) endpoint handler method" target="_blank">these lines are the refactored code</a>.
The <code>FIXME</code> markers indicate workaround code for which I hope to find a better solution later on. Please note the following:

<figure class="highlight"><pre><code class="language-python" data-lang="python"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">303
304
305
306
307
</pre></td><td class="code"><pre>    <span class="c1"># 
</span>    <span class="c1"># FIXME: HACK! This causes the 'session' cookie created, so that 
</span>    <span class="c1">#     async def __internal(request: Request): can access the session Id.
</span>    <span class="c1">#
</span>    <span class="n">request</span><span class="p">.</span><span class="n">session</span><span class="p">[</span><span class="s">'x-email'</span><span class="p">]</span> <span class="o">=</span> <span class="n">op_status</span><span class="p">.</span><span class="n">data</span><span class="p">[</span><span class="mi">0</span><span class="p">][</span><span class="s">'email'</span><span class="p">]</span>
</pre></td></tr></tbody></table></code></pre></figure>

Without setting an entry in <code>request.session</code>, the <code>session</code> UUID 
cookie would not be created.

<figure class="highlight"><pre><code class="language-python" data-lang="python"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">322
323
324
325
326
327
</pre></td><td class="code"><pre>    <span class="n">response</span><span class="p">.</span><span class="n">set_cookie</span><span class="p">(</span><span class="n">key</span><span class="o">=</span><span class="n">RESPONSE_FORMAT</span><span class="p">,</span> <span class="n">value</span><span class="o">=</span><span class="n">response_format</span><span class="p">,</span> <span class="n">httponly</span><span class="o">=</span><span class="bp">True</span><span class="p">)</span>
    <span class="n">response</span><span class="p">.</span><span class="n">set_cookie</span><span class="p">(</span><span class="n">key</span><span class="o">=</span><span class="s">'x-email'</span><span class="p">,</span> <span class="n">value</span><span class="o">=</span><span class="n">op_status</span><span class="p">.</span><span class="n">data</span><span class="p">[</span><span class="mi">0</span><span class="p">][</span><span class="s">'email'</span><span class="p">],</span> <span class="n">httponly</span><span class="o">=</span><span class="bp">True</span><span class="p">)</span>
    <span class="n">response</span><span class="p">.</span><span class="n">set_cookie</span><span class="p">(</span><span class="n">key</span><span class="o">=</span><span class="s">'x-emp-no'</span><span class="p">,</span> <span class="n">value</span><span class="o">=</span><span class="nb">str</span><span class="p">(</span><span class="n">op_status</span><span class="p">.</span><span class="n">data</span><span class="p">[</span><span class="mi">0</span><span class="p">][</span><span class="s">'emp_no'</span><span class="p">]),</span> <span class="n">httponly</span><span class="o">=</span><span class="bp">True</span><span class="p">)</span>
    <span class="n">response</span><span class="p">.</span><span class="n">set_cookie</span><span class="p">(</span><span class="n">key</span><span class="o">=</span><span class="s">'x-scopes'</span><span class="p">,</span> <span class="n">value</span><span class="o">=</span><span class="s">'^'</span><span class="p">.</span><span class="n">join</span><span class="p">(</span><span class="n">op_status</span><span class="p">.</span><span class="n">data</span><span class="p">.</span><span class="n">scopes</span><span class="p">),</span> <span class="n">httponly</span><span class="o">=</span><span class="bp">True</span><span class="p">)</span>

    <span class="k">return</span> <span class="n">response</span>
</pre></td></tr></tbody></table></code></pre></figure>

<a id="code-reftr-login-process-internal-route"></a>
We need these pieces of information in the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/b2caf207cfea2bd92565eaa981479993996c799b/src/fastapi_learning/controllers/auth.py#L154-L229" 
title="The __internal(...) endpoint handler method" target="_blank"><code>__internal(...)</code></a> 
endpoint handler method. 
In this method, we extract the information from the cookies to create the access token and set it to the session storage. We remove all temporary entries set in cookies and session storage. Then, finally, we redirect to the home page endpoint handler method as before.

I don't particularly like this workaround, but for the time being, this is the best I could do. I have tried several other approaches and have not succeeded in getting them to work.

<a id="code-reftr-logout-process"></a>
⓷ <strong>Rewrote and Bug-Fixed the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/b2caf207cfea2bd92565eaa981479993996c799b/src/fastapi_learning/controllers/auth.py#L329-L375" 
title="The logout(...) endpoint handler method" target="_blank"><code>logout(...)</code></a> 
Endpoint Handler Method</strong>

Again, please note the <code>FIXME</code> markers. Please note the following:

● Added the parameter <code>token: Annotated[str, Depends(oauth2_scheme)]</code>: This 
ensures that this endpoint method gets the access token.

● First, it looks into the request cookies to extract the <code>session</code> UUID. 
If there are no cookies, it extracts the <code>session</code> UUID from the access token.

● Then it uses Redis directly to remove the session entry:

<figure class="highlight"><pre><code class="language-python" data-lang="python"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">366
367
368
</pre></td><td class="code"><pre>    <span class="n">response</span><span class="p">.</span><span class="n">set_cookie</span><span class="p">(</span><span class="n">key</span><span class="o">=</span><span class="n">RESPONSE_FORMAT</span><span class="p">,</span> <span class="n">value</span><span class="o">=</span><span class="n">res</span>        <span class="c1"># Does this session Id exist, currently?
</span>        <span class="n">auth_session</span> <span class="o">=</span> <span class="n">session_id</span> <span class="ow">in</span> <span class="n">redis_server</span><span class="p">.</span><span class="n">scan_iter</span><span class="p">(</span><span class="n">session_id</span><span class="p">)</span>
        <span class="n">redis_server</span><span class="p">.</span><span class="n">delete</span><span class="p">(</span><span class="n">session_id</span><span class="p">)</span>
</pre></td></tr></tbody></table></code></pre></figure>

The 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/b2caf207cfea2bd92565eaa981479993996c799b/src/fastapi_learning/controllers/__init__.py#L41-L42" 
title="The controllers/__init__.py module" 
target="_blank"><code>redis_server</code></a> instance is:

<figure class="highlight"><pre><code class="language-python" data-lang="python"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">41
42
</pre></td><td class="code"><pre><span class="n">redis_server</span> <span class="o">=</span> <span class="n">redis</span><span class="p">.</span><span class="n">Redis</span><span class="p">(</span><span class="n">host</span><span class="o">=</span><span class="n">os</span><span class="p">.</span><span class="n">environ</span><span class="p">.</span><span class="n">get</span><span class="p">(</span><span class="s">"REDIS_URL"</span><span class="p">,</span> <span class="s">"redis://localhost"</span><span class="p">).</span><span class="n">split</span><span class="p">(</span><span class="s">'//'</span><span class="p">)[</span><span class="mi">1</span><span class="p">],</span> 
                           <span class="n">decode_responses</span><span class="o">=</span><span class="bp">True</span><span class="p">)</span>
</pre></td></tr></tbody></table></code></pre></figure>

This is a bit drastic. I do not like it. But I do not know of another alternative. 

I have written middleware to inject <code>starsessions</code>'s 
<a href="https://github.com/alex-oleshkevich/starsessions/blob/0b32a2393f8291ec8bb8ab239e8bd8f7c1d8cae3/starsessions/stores/redis.py#L15" 
title="The starsessions/stores/redis.py module" target="_blank"><code>RedisStore</code></a> 
into the request and use the <code>RedisStore</code> instance to access Redis. 
However, in the latest version, they removed the <code>exists(...)</code> method, which I need.

These changes take care of cleaning up the Redis session storage when logging out using access tokens.

<a id="code-reftr-decoration"></a>
⓸ <strong>Redecorate Endpoint Methods</strong>

I have just learned that endpoint methods can be decorated with multiple different path decorators. 😂

In the <code>admin.py</code> module, we removed the method 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/436c732e248d84876cfa11863c639f0e3d5abab4/src/fastapi_learning/controllers/admin.py#L119-L132" 
title="The controllers/admin.py module" target="_blank"><code>read_users_me_api(...)</code></a>, 
and decorated the method 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/b2caf207cfea2bd92565eaa981479993996c799b/src/fastapi_learning/controllers/admin.py#L72-L131" 
title="The controllers/admin.py module" target="_blank"><code>read_users_me(...)</code></a> with 
<code>@api_router.get("/me")</code>.

Similarly, in the <code>auth.py</code> module, we removed the method 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/436c732e248d84876cfa11863c639f0e3d5abab4/src/fastapi_learning/controllers/auth.py#L237-L248" 
title="The controllers/auth.py module" target="_blank"><code>login_api(...)</code></a>, 
and moved the decorator <code>@api_router.post("/login")</code> to the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/b2caf207cfea2bd92565eaa981479993996c799b/src/fastapi_learning/controllers/auth.py#L231-L327" 
title="The controllers/auth.py module" target="_blank"><code>login(...)</code></a> method.

Finally, we created a new <code>/api/logout</code> route with the following decorator 
<code>@api_router.post("/logout", response_class=HTMLResponse)</code> 
on the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/b2caf207cfea2bd92565eaa981479993996c799b/src/fastapi_learning/controllers/auth.py#L329-L375" 
title="The logout(...) endpoint handler method" target="_blank"><code>logout(...)</code></a> 
endpoint handler method.

<a id="on-test-modules"></a>
❹ <strong>On Tests</strong>

All of the 84 tests remain unchanged, and they all pass with this new implementation. I intentionally did not write any new tests; I just ensured the existing tests work as they are. I might write some more later. Importantly, after running all tests, the Redis server should show no entries.

<a id="refatored-code-cli-test-script"></a>
❺ <strong>Test the Refactored Code with a CLI Test Script</strong>

Let's see how the illustrative script <a href="#problem-def-02-script-example">
previously demonstrated</a> would work with the refactored code. But first, recall
from the <a href="#code-reftr-login-process">login process</a> code refactoring that 
we redirect with some cookies set. The 
<a href="https://pypi.org/project/urllib3/" title="The urllib3 library" target="_blank">urllib3</a> 
library does not have cookies enabled, and the server will not handle cookies correctly. 
We need to enable cookies ourselves, which I have not been able to figure out how to do. 
The 
<a href="https://pypi.org/project/requests/" title="The Requests library" target="_blank">Requests</a> 
library, which uses <code>urllib3</code>, handles cookies out of the box.

So we need to modify the <a href="#problem-def-02-script-example">original script</a> 
a little: The two logout methods remain unchanged, and the <code>login(...)</code> method 
uses the <code>Requests</code> library. Please note the header setting 
<code>headers={'x-referer': 'desktopclient'}</code>, which is used in the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/b2caf207cfea2bd92565eaa981479993996c799b/src/fastapi_learning/controllers/auth.py#L154-L229" 
title="The __internal(...) endpoint handler method" target="_blank"><code>__internal(...)</code></a> 
endpoint handler method 
<a href="#code-reftr-login-process-internal-route">as discussed</a>.

```
import urllib3
import requests

COOKIE: str = None
ACCESS_TOKEN: str = None

def login(http: requests.Session, username: str, password: str):

    global COOKIE
    global ACCESS_TOKEN

    # Assuming always succeeds.
    resp = http.post(
        "https://localhost:5000/api/login",
        headers={'x-referer': 'desktopclient'},
        data={"username": username, "password": password},
        verify=False
    )

    status = resp.json()

    COOKIE = f"session={resp.cookies.get('session')}; path=/; httponly; samesite=lax"
    ACCESS_TOKEN = status['data']['access_token']

def logout_01(http: urllib3.PoolManager, response_cookie: str):
    """
    This logout request deletes the Redis session entry.
    """

    http.request(
        "POST",
        "https://localhost:5000/auth/logout",
        headers={
            "Cookie": response_cookie,
            "x-expected-format": "application/json",
        }
    )

def logout_02(http: urllib3.PoolManager, access_token: str):
    """
    This logout request DOES NOT delete the Redis session entry.
    """

    http.request(
        "POST",
        "https://localhost:5000/auth/logout",
        headers={
            "Authorization": f"Bearer {access_token}",
            "x-expected-format": "application/json",
        }
    )

# Suppress only the single warning from urllib3.
urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)
session = requests.Session()

urllib3.disable_warnings()
http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)

login(session, 'behai_nguyen@hotmail.com', 'password')

print(f"COOKIE: {COOKIE}")
print(f"ACCESS_TOKEN: {ACCESS_TOKEN}")

logout_01(http, COOKIE)
# logout_02(http, ACCESS_TOKEN)
```

Please run it as 
<a href="#problem-def-02-script-example-run">previously described</a>, but this time, both of the logout methods should remove all entries from the Redis server storage.

<a id="concluding-remarks"></a>
❻ I am not sure how much I have understood 
<a href="https://pypi.org/project/starsessions/" title="starsessions" target="_blank">starsessions</a>,  
even though I have spent time looking at its code. Ideally, users should be able to dictate when to create the <code>session</code> UUID and thus the session entry. So far, this does not seem to be the case with this library.

Thank you for reading. I hope you find the information in this post useful. Stay safe, as always.

✿✿✿

Feature image source:

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
