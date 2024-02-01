---
layout: post
title: "Rust: simple actix-web email-password login and request authentication using middleware."

description: For our learning actix-web application, we are now adding two new features. ⓵ A simple email-password login with no session expiry. ⓶ A new middleware that manages request authentication using an access token “generated” by the login process. All five existing routes are now protected by this middleware, they can only be accessed if the request has a valid access token. With these two new features added, this application acts as both an application server and an API-like server or a service. 

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.files.wordpress.com/2024/01/096-01-home-01.png"
    - "https://behainguyen.files.wordpress.com/2024/01/096-01-home-02.png"
    - "https://behainguyen.files.wordpress.com/2024/01/096-01-home-03.png"

gallery-image-list-2:
    - "https://behainguyen.files.wordpress.com/2024/01/096-05-auth-header-01.png"
    - "https://behainguyen.files.wordpress.com/2024/01/096-05-auth-header-02.png"

tags:
- Rust
- actix-web
- redirect
- middleware
- request authentication
- authentication
---

<em>For our learning <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> application, we are now adding two new features. ⓵ A simple email-password login with no session expiry. ⓶ A new middleware that manages <a href="#definition-request-auth"><code>request authentication</code></a> using an <a href="#definition-access-token"><code>access token</code></a> “generated” by the login process. All <a href="#issues-covered-existing-routes">five existing routes</a> are now protected by this middleware: they can only be accessed if the request has a valid <a href="#definition-access-token"><code>access token</code></a>. With these two new features added, this application acts as both an <a href="#definition-app-server"><code>application server</code></a> and an <a href="#definition-api-server"><code>API-like server</code> or a <code>service</code></a>.</em>

| ![096-feature-image.png](https://behainguyen.files.wordpress.com/2024/01/096-feature-image.png) |
|:--:|
| *Rust: simple actix-web email-password login and request authentication using middleware.* |

<p>
🚀 <strong>Please note,</strong> complete code for this post can be downloaded from GitHub with:
</p>

```
git clone -b v0.6.0 https://github.com/behai-nguyen/rust_web_01.git
```

The
<a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a>
learning application mentioned above has been discussed 
in the following five previous posts:

<ol>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/10/18/rust-web-application-mysql-server-sqlx-actix-web-and-tera/" title="Rust web application: MySQL server, sqlx, actix-web and tera" target="_blank">Rust web application: MySQL server, sqlx, actix-web and tera</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/11/26/rust-learning-actix-web-middleware-01/" title="Rust: learning actix-web middleware 01" target="_blank">Rust: learning actix-web middleware 01</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/12/31/rust-retrofit-integration-tests-to-an-existing-actix-web-application/" title="Rust: retrofit integration tests to an existing actix-web application." target="_blank">Rust: retrofit integration tests to an existing actix-web application</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/01/03/rust-adding-actix-session-and-actix-identity-to-an-existing-actix-web-application/" title="Rust: adding actix-session and actix-identity to an existing actix-web application." target="_blank">Rust: adding actix-session and actix-identity to an existing actix-web application</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/01/14/rust-actix-web-endpoints-which-accept-both-application-x-www-form-urlencoded-and-application-json-content-types/" title="Rust: actix-web endpoints which accept both application/x-www-form-urlencoded and application/json content types." target="_blank">Rust: actix-web endpoints which accept both <code>application/x-www-form-urlencoded</code> and <code>application/json</code> content types</a>.</li>
</ol>

The code we're developing in this post is a continuation 
of the code from the 
<a href="https://behainguyen.wordpress.com/2024/01/14/rust-actix-web-endpoints-which-accept-both-application-x-www-form-urlencoded-and-application-json-content-types/" title="Rust: actix-web endpoints which accept both application/x-www-form-urlencoded and application/json content types." target="_blank">fifth</a>
post above. 🚀 To get the code of this 
<a href="https://behainguyen.wordpress.com/2024/01/14/rust-actix-web-endpoints-which-accept-both-application-x-www-form-urlencoded-and-application-json-content-types/" title="Rust: actix-web endpoints which accept both application/x-www-form-urlencoded and application/json content types." target="_blank">fifth</a>
post, please use the following command:

```
git clone -b v0.5.0 https://github.com/behai-nguyen/rust_web_01.git
```

<strong>-- Note the tag <code>v0.5.0</code>.</strong>

<!--------------------------------------------------------------------------------->
<h2>Table of contents</h2>

<ul>
<li style="margin-top:10px;"><a href="#terms-phrases-definition">Some Terms and Phrases Definition</a></li>
<li style="margin-top:10px;"><a href="#project-layout">Project Layout</a></li>
<li style="margin-top:10px;"><a href="#code-documentation">Code Documentation</a></li>
<li style="margin-top:10px;"><a href="#issues-covered">Issues Covered In This Post</a></li>
<li style="margin-top:10px;"><a href="#hard-coded-employees-password">On the Hard-Coded Value for <code>employees.password</code></a></li>

<li style="margin-top:10px;">
<a href="#notes-on-cookies">Notes On Cookies</a>
<ul>
<li style="margin-top:10px;"><a href="#notes-on-cookies-third-party">The <code>actix-session</code> <code>id</code> cookie</a></li>
<li style="margin-top:10px;"><a href="#notes-on-cookies-our-own">Our cookies: <code>redirect-message</code>, <code>original-content-type</code> and <code>authorization</code></a></li>
</ul>
</li>

<li style="margin-top:10px;"><a href="#response-status-code">HTTP Response Status Code</a></li>

<li style="margin-top:10px;">
<a href="#email-password-login-process">How the Email-Password Login Process Works</a>
<ul>
<li style="margin-top:10px;"><a href="#the-login-process-api-login">The login process, <code>/api/login</code> handler</a></li>
<li style="margin-top:10px;"><a href="#the-login-page-ui-login">The login page, <code>/ui/login</code> handler</a></li>
</ul>
</li>

<li style="margin-top:10px;"><a href="#request-authentication-works">How the Request Authentication Process Works</a></li>
<li style="margin-top:10px;"><a href="#the-home-page-and-logout-routes">The Home Page and the Logout Routes</a></li>

<li style="margin-top:10px;">
<a href="#integration-tests">Integration Tests</a>
<ul>
<li style="margin-top:10px;"><a href="#integration-tests-common">Common test code</a></li>
<li style="margin-top:10px;"><a href="#integration-tests-enble-cookies">Enble cookies in tests</a></li>
<li style="margin-top:10px;"><a href="#integration-tests-existing">Existing tests</a></li>
<li style="margin-top:10px;"><a href="#integration-tests-new">New tests</a></li>			
</ul>
</li>

<li style="margin-top:10px;"><a href="#some-manual-tests">Some Manual Tests</a></li>
<li style="margin-top:10px;"><a href="#rust-users-forum-helps">Rust Users Forum Helps</a></li>
<li style="margin-top:10px;"><a href="#some-current-issues">Some Current Issues</a></li>
<li style="margin-top:10px;"><a href="#concluding-remarks">Concluding Remarks</a></li>
</ul>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;text-transform: none;">
  <a id="terms-phrases-definition">Some Terms and Phrases Definition</a>
</h3>

Let's clarify the meanings of some glossary terms to facilitate the understanding of this post.

<a id="definition-app-server"></a>
● An <code>application server</code> -- the application functions as 
a website server, serving interactive HTML pages and managing 
states associated with client web sessions.

<a id="definition-api-server"></a>
● An <code>API-like server</code> or a <code>service</code> -- the application
operates as a data provider, verifying the validity of client requests. 
Specifically, it checks for a valid <a href="#definition-access-token"><code>access token</code></a>
included in the request <code>authorization</code> header. If the requests are valid, 
it proceeds to serve them.

<a id="definition-access-token"></a>
● An <code>access token</code> -- <strong>in this revision of the code, 
any non-blank string is considered a valid <code>access token</code>!</strong> 
Please note that this is a work in progress, and currently, login emails are 
used as <code>access token</code>s. 

As such, we acknowledge that this so-called 
<code>access token</code> 
is <strong>relatively ineffective as a security measure</strong>. 
The primary focus of this post is on the login and 
<a href="#definition-request-auth"><code>request authentication</code></a> 
processes. Consider it a placeholder, as we plan to refactor it into a 
more formal authentication method.

The response from the login process always includes the <code>access token</code> 
in the <code>authorization</code> header implictly, and explictly in JSON responses. 
Clients should store this <code>access token</code> for future use.

To utilise this application as an <a href="#definition-api-server"><code>API-like 
server</code> or a <code>service</code></a>, client requests must include the 
previously provided <a href="#definition-access-token"><code>access token</code></a> 
in the <code>authorization</code> header.

<a id="definition-authenticated-session"></a>
● An <code>authenticated session</code> -- a client web session who has previously 
<em>logged in</em> or <em>authenticated</em>. That is, having been given an 
<a href="#definition-access-token"><code>access token</code></a> by the login process.

<a id="definition-request-auth"></a>
● <code>Request authentication</code> -- the process of verifying that the 
<a href="#definition-access-token"><code>access token</code></a> is present and valid.
If a request passes the <a href="#definition-request-auth"><code>request authentication</code></a>
process, it indicates that the request comes from an 
<a href="#definition-authenticated-session"><code>authenticated session</code></a>.

<a id="definition-request-auth-middleware"></a>
● <code>Request authentication middleware</code> -- this is the new 
middleware mentioned in the introduction, fully responsible for the 
<a href="#definition-request-auth"><code>request authentication</code></a> process.

<a id="definition-authenticated-request"></a>
● An <code>authenticated request</code> -- a request which has passed the 
<a href="#definition-request-auth"><code>request authentication</code></a> process.

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;text-transform: none;">
  <a id="project-layout">Project Layout</a>
</h3>

This post introduces several new modules and a new HTML home page, with some 
modules receiving updates. The updated directory layout for the project is 
listed below.

<strong>-- Please note,</strong> those marked with <span style="font-size:1.5em;">★</span> 
are updated, and those marked with <span style="font-size:1.5em;">☆</span> are new.

```
.
├── Cargo.toml ★
├── .env
├── migrations
│ ├── mysql
│ │ └── migrations
│ │     ├── 20231128234321_emp_email_pwd.down.sql
│ │     └── 20231128234321_emp_email_pwd.up.sql
│ └── postgres
│     └── migrations
│         ├── 20231130023147_emp_email_pwd.down.sql
│         └── 20231130023147_emp_email_pwd.up.sql
├── README.md ★
├── src
│ ├── auth_handlers.rs ★
│ ├── auth_middleware.rs ☆
│ ├── bh_libs
│ │ └── api_status.rs ★
│ ├── bh_libs.rs ★
│ ├── config.rs
│ ├── database.rs
│ ├── handlers.rs
│ ├── helper
│ │ ├── app_utils.rs ☆
│ │ ├── constants.rs ☆
│ │ ├── endpoint.rs ★
│ │ └── messages.rs ★
│ ├── helper.rs ★
│ ├── lib.rs ★
│ ├── main.rs
│ ├── middleware.rs
│ ├── models.rs ★
│ └── utils.rs
├── templates
│ ├── auth
│ │ ├── home.html ☆
│ │ └── login.html
│ └── employees.html ★
└── tests
    ├── common.rs ★
    ├── test_auth_handlers.rs ☆
    └── test_handlers.rs ★
```

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;text-transform: none;">
  <a id="code-documentation">Code Documentation</a>
</h3>

The code has extensive documentation. It probably has more detail than in 
this post, as documentation is specific to functionalities and implementation. 

To view the code documentation, change to the project directory (where 
<code>Cargo.toml</code> is located) and run the following command:

```
▶️Windows 10: cargo doc --open
▶️Ubuntu 22.10: $ cargo doc --open
```


<!--------------------------------------------------------------------------------->
<h3 style="color:teal;text-transform: none;">
  <a id="issues-covered">Issues Covered In This Post</a>
</h3>

❶ “Complete” the login function.

In the <a href="https://behainguyen.wordpress.com/2024/01/14/rust-actix-web-endpoints-which-accept-both-application-x-www-form-urlencoded-and-application-json-content-types/" title="Rust: actix-web endpoints which accept both application/x-www-form-urlencoded and application/json content types." target="_blank">fifth</a>
post, we introduced two new login-related routes, <code>/ui/login</code> and 
<code>/api/login</code>, used them to demonstrate accepting request data in both
<code>application/x-www-form-urlencoded</code> and <code>application/json</code> formats.

In this post, we'll fully implement a simple email and password login process with 
no session expiry. In other words, if we can identify an employee by email, and the 
submitted password matches the database password, then the session is considered 
<strong>logged in</strong> or <strong>authenticated</strong>. The session remains 
valid indefinitely, until the browser is shut down.

🚀 The handlers for <code>/ui/login</code> and <code>/api/login</code> 
have the capability of conditionally return either HTML or JSON depending  
on the <code>content type</code> of the original request.

❷ Protect all existing and new <code>/data/xxx</code> and <code>/ui/xxx</code> routes 
(except <code>/ui/login</code>) using the new <a href="#definition-request-auth-middleware">
<code>request authentication middleware</code></a> as mentioned in the introduction.

<a id="issues-covered-existing-routes"></a>
This means only <a href="#definition-authenticated-request">
<code>authenticated requests</code></a> can access these routes. 
Recall that we have the following five routes, which query the 
database and return data in some form:

<ol>
<li style="margin-top:10px;">
JSON response route <code>http://0.0.0.0:5000/data/employees</code> -- 
method: <code>POST</code>; 
content type: <code>application/json</code>; 
request body: <code>{"last_name": "%chi", "first_name": "%ak"}</code>.
</li>

<li style="margin-top:10px;">
JSON response route <code>http://0.0.0.0:5000/data/employees/%chi/%ak</code> --
method <code>GET</code>.
</li>

<li style="margin-top:10px;">
HTML response route <code>http://0.0.0.0:5000/ui/employees</code> --
method: <code>POST</code>;
content type: <code>application/x-www-form-urlencoded; charset=UTF-8</code>;
request body: <code>last_name=%chi&first_name=%ak</code>.
</li>

<li style="margin-top:10px;">
HTML response route <code>http://0.0.0.0:5000/ui/employees/%chi/%ak</code> -- 
method: <code>GET</code>.
</li>

<li style="margin-top:10px;">
HTML response route <code>http://0.0.0.0:5000/helloemployee/%chi/%ak</code> -- 
method: <code>GET</code>.
</li>
</ol>

We implement protection, or <a href="#definition-request-auth"><code>request authentication</code></a>, 
around these routes, allowing only <a href="#definition-authenticated-session"><code>
authenticated sessions</code></a> to access them. When a request is not authenticated, 
it gets redirected to the <code>/ui/login</code> route. The handler for this route 
uses the <code>content type</code> of the original request to determine whether it returns 
the HTML login page with a user-friendly error message or an appropriate JSON error response.

The new middleware we're using to manage the <a href="#definition-request-auth"><code>
request authentication</code></a> process is based on the 
<a href="https://github.com/actix/examples/blob/master/middleware/various/src/redirect.rs"
title="the official redirect example" target="_blank">official redirect example</a>.
We rename it to 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/auth_middleware.rs" 
title="src/auth_middleware.rs" target="_blank">src/auth_middleware.rs</a>.

❸ We implement two additional authentication-related routes: <code>/ui/home</code> 
and <code>/api/logout</code>.

The <code>/ui/home</code> route is protected, and if requests 
are successful, its handler always returns the HTML home page.

The <code>/api/logout</code> handler always returns the HTML login
page.

To recap, we have the following four new authentication-related routes: 

<ol>
<li style="margin-top:10px;">
HTML/JSON response route <code>http://0.0.0.0:5000/ui/login</code> -- 
method: <code>GET</code>.
</li>

<li style="margin-top:10px;">
HTML/JSON response route <code>http://0.0.0.0:5000/api/login</code> --
method: <code>POST</code>.
<br/>
content type: <code>application/x-www-form-urlencoded; charset=UTF-8</code>;
request body: <code>email=chirstian.koblick.10004@gmail.com&password=password</code>.
<br/>
content type: <code>application/json</code>;
request body: <code>{"email": "chirstian.koblick.10004@gmail.com", "password": "password"}</code>.
</li>

<li style="margin-top:10px;">
HTML response route <code>http://0.0.0.0:5000/ui/home</code> --
method: <code>GET</code>.
</li>

<li style="margin-top:10px;">
HTML response route <code>http://0.0.0.0:5000/api/logout</code> -- 
method: <code>POST</code>.
</li>
</ol>

❹ Updating existing integration tests and creating new ones for new functionalities.

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;text-transform: none;">
  <a id="hard-coded-employees-password">On the Hard-Coded Value for <code>employees.password</code></a>
</h3>

In the section
<a href="https://behainguyen.wordpress.com/2024/01/14/rust-actix-web-endpoints-which-accept-both-application-x-www-form-urlencoded-and-application-json-content-types/#step-two-update-employees-table" title="Add new fields email and password to the employees table" target="_blank">Add new fields <code>email</code> and <code>password</code> to the <code>employees</code> table</a>
of the 
<a href="https://behainguyen.wordpress.com/2024/01/14/rust-actix-web-endpoints-which-accept-both-application-x-www-form-urlencoded-and-application-json-content-types/" title="Rust: actix-web endpoints which accept both application/x-www-form-urlencoded and application/json content types." target="_blank">fifth</a>
post, in the 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/migrations/mysql/migrations/20231128234321_emp_email_pwd.up.sql#L20" title="migration script" target="_blank">migration script</a>,
we hard-coded the string <code>$argon2id$v=19$m=16,t=2,p=1$cTJhazRqRWRHR3NYbEJ2Zg$z7pMnKzV0eU5eJkdq+hycQ</code> 
for all passwords. It is the hashed version of <code>password</code>.

It was generated using <a href="https://argon2.online/" title="Argon2 Online by Esse.Tools" 
target="_blank">Argon2 Online by Esse.Tools</a>, which is compatible with the 
<a href="https://docs.rs/argon2/latest/argon2/" title="Crate argon2" target="_blank">argon2</a>
crate. Thus, we can use this crate to de-hash a hashed password to compare it to a plain text one.

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;text-transform: none;">
  <a id="notes-on-cookies">Notes On Cookies</a>
</h3>

<a id="notes-on-cookies-third-party"></a>
❶ In the fourth post, <a href="https://behainguyen.wordpress.com/2024/01/03/rust-adding-actix-session-and-actix-identity-to-an-existing-actix-web-application/" title="Rust: adding actix-session and actix-identity to an existing actix-web application." target="_blank">Rust: adding actix-session and actix-identity to an existing actix-web application</a>,
we introduced the crate 
<a href="https://docs.rs/actix-identity/latest/actix_identity/" title="Crate actix_identity" target="_blank">actix-identity</a>, 
which requires the crate <a href="https://docs.rs/actix-session/latest/actix_session/" title="Crate actix_session" target="_blank">actix-session</a>.
However we didn't make use of them. Now, they are used in the code of this post.

The crate <a href="https://docs.rs/actix-session/latest/actix_session/" title="Crate actix_session" target="_blank">actix-session</a> 
will create a <strong>secured cookie</strong> named <code>id</code>.
However, since we're only testing the application with <code>HTTP</code> (not
<code>HTTPS</code>), some browsers reject such secured cookie.

Since this is only a learning application, we'll make all cookies 
<strong>non-secured</strong>. Module 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/lib.rs#L70" title="src/lib.rs" target="_blank">src/lib.rs</a> 
gets updated as follows:

```rust
...
            .wrap(SessionMiddleware::builder(
                    redis_store.clone(),
                    secret_key.clone()
                )
                .cookie_secure(false)
                .build(),
            )
...
```

We call the 
<a href="https://docs.rs/actix-session/latest/actix_session/struct.SessionMiddleware.html#method.builder"
title="builder(...)" target="_blank">builder(...)</a> method 
to access the 
<a href="https://docs.rs/actix-session/latest/actix_session/config/struct.SessionMiddlewareBuilder.html#method.cookie_secure"
title="cookie_secure(...)" target="_blank">cookie_secure(...)</a> method 
and set the cookie <code>id</code> to non-secured.

<a id="notes-on-cookies-our-own"><!--our own cookies--></a>
❷ To handle potential request redirections during the login and 
the 
<a href="#definition-request-auth"><code>request authentication</code></a>
processes, the application utilises the following <em><strong>server-side
per-request</strong></em> cookies: <code>redirect-message</code> 
and <code>original-content-type</code>. 

💥 <strong><code>Request redirection</code> occurs when a request is redirected 
to <code>/ui/login</code> due to some failure condition. </strong> When a request 
gets redirected elsewhere, <code>request redirection</code> does not apply.

These cookies help persisting necessary information between requests. <em>Between 
requests</em> refers to the original request that gets redirected, resulting in 
the second and final independent request. Hence, <strong><em>per-request</em></strong> 
pertains to the original request.

We implement a helper function to create these cookies in the module 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/helper/app_utils.rs#L18" title="src/helper/app_utils.rs" target="_blank">src/helper/app_utils.rs</a>: 

```rust
pub fn build_cookie<'a>(
...
    let mut cookie = Cookie::build(name, value)
        .domain(String::from(parts.collect::<Vec<&str>>()[0]))
        .path("/")
        .secure(false)
        .http_only(server_only)
        .same_site(SameSite::Strict)
        .finish();

    if removal {
        cookie.make_removal();
    }
...		
```

Refer to the following Mdm Web Docs 
<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie" title="Mdm Web Docs" target="_blank">Set-Cookie</a>
for explanations of the settings used in the above function.

Take note of the call to the method 
<a href="https://docs.rs/actix-web/latest/actix_web/cookie/struct.Cookie.html#method.make_removal"
title="Method make_removal(...)" target="_blank">make_removal(...)</a> -- 
it's necessary to remove the <em>server-side per-request</em> cookies when 
the request completes.

In addition to the aforementioned temporary cookies, the application 
also maintains an application-wide publicly available cookie named 
<code>authorization</code>. This cookie stores the 
<a href="#definition-access-token"><code>access token</code></a>
after a successful login.

To recap, the application maintains three cookies. In the module 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/helper/app_utils.rs" title="src/helper/app_utils.rs" target="_blank">src/helper/app_utils.rs</a>, 
we also implement three pairs of helper methods, 
<code>build_xxx_cookie(...)</code> and <code>remove_xxx_cookie(...)</code>, 
to help manage the lifetime of these cookies.

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;text-transform: none;">
  <a id="response-status-code">HTTP Response Status Code</a>
</h3>

All HTTP responses -- successful and failure, HTML and JSON --
have their HTTP response status code set to an appropriate 
code. In addition, if a response is in JSON format, the
field 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/bh_libs/api_status.rs#L20"
title="ApiStatus.code" target="_blank"><code>ApiStatus.code</code></a> 
also has its value sets to the value of the HTTP response status 
code.

-- We've introduced 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/bh_libs/api_status.rs#L20"
title="ApiStatus" target="_blank"><code>ApiStatus</code></a> in the 
<a href="https://behainguyen.wordpress.com/2024/01/14/rust-actix-web-endpoints-which-accept-both-application-x-www-form-urlencoded-and-application-json-content-types/" title="Rust: actix-web endpoints which accept both application/x-www-form-urlencoded and application/json content types." target="_blank">fifth</a>
post. Basically, it's a generic API status response that gets 
included in all JSON responses.

We set the HTTP response status code base on
“The OAuth 2.0 Authorization Framework”:
<a href="https://datatracker.ietf.org/doc/html/rfc6749"
title="The OAuth 2.0 Authorization Framework"
target="_blank">https://datatracker.ietf.org/doc/html/rfc6749</a>;
sections 
<a href="https://datatracker.ietf.org/doc/html/rfc6749#section-5.1"
title="Successful Response" target="_blank">Successful Response</a>
and
<a href="https://datatracker.ietf.org/doc/html/rfc6749#section-5.2"
title="Error Response" target="_blank">Error Response</a>.

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;text-transform: none;">
  <a id="email-password-login-process">How the Email-Password Login Process Works</a>
</h3>

👎 This is the area where I encountered the most difficulties while learning
<a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> 
and <a href="https://docs.rs/actix-web/latest/actix_web/middleware/index.html"
title="actix-web middleware" target="_blank">actix-web middleware</a>. Initially, 
I thought both the login and the <a href="#definition-request-auth"><code>request authentication</code></a>
processes should be in the same middleware. I attempted that approach, but it was unsuccessful. 
Eventually, I realised that login should be handled by an endpoint handler function. And 
<a href="#definition-request-auth"><code>request authentication</code></a> should be managed 
by the middleware. In this context, the middleware is much like a Python decorator.

The email-password login process exclusively occurs in module  
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/auth_handlers.rs"
title="src/auth_handlers.rs" target="_blank">src/auth_handlers.rs</a>.
In broad terms, this process involves two routes <code>/api/login</code> and <code>/ui/login</code>.

<a id="the-login-process-api-login"></a>
<p>
❶ The login process, <code>/api/login</code> handler.
</p>

The login process handler is 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/auth_handlers.rs#L284"
title="The login process handler"
target="_blank"><code>pub async fn login(request: HttpRequest, app_state: web::Data&lt;super::AppState>, <br/>body: Bytes) -> Either&lt;impl Responder, HttpResponse></code></a>.
It works as follows:

<a id="the-login-process-api-login-step-one"></a>
⓵ Attempt to extract the submitted log in information, a step discussed the 
<a href="https://behainguyen.wordpress.com/2024/01/14/rust-actix-web-endpoints-which-accept-both-application-x-www-form-urlencoded-and-application-json-content-types/" title="Rust: actix-web endpoints which accept both application/x-www-form-urlencoded and application/json content types." target="_blank">fifth</a> 
post above. If the extraction fails, it <strong>always returns a JSON response</strong>
of <a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/bh_libs/api_status.rs#L20"
title="ApiStatus" target="_blank"><code>ApiStatus</code></a> with a <code>code</code>
of <code>400</code> for <code>BAD REQUEST</code>. And that's the end of the request. 

<a id="the-login-process-api-login-step-two"></a>
⓶ Next, we use the submitted email to retrieve the target employee
from the database. If there is no match, we call the helper function 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/auth_handlers.rs#L63"
title="Login error, no match on employee email"
target="_blank"><code>fn first_stage_login_error_response(request: &HttpRequest, message: &str) -> HttpResponse</code></a>
to handle the failure: 

● If the request content type is <code>application/json</code>, 
we return a JSON response of 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/bh_libs/api_status.rs#L20"
title="ApiStatus" target="_blank"><code>ApiStatus</code></a> with a <code>code</code>
of <code>401</code> for <code>UNAUTHORIZED</code>. The value for the 
<code>message</code> field is set to the value of the parameter <code>message</code>.

● For the <code>application/x-www-form-urlencoded</code> content type, 
we set the <em>server-side per-request</em> cookie <code>redirect-message</code> 
and redirect to route <code>/ui/login</code>:

```rust
...
        HttpResponse::Ok()
            .status(StatusCode::SEE_OTHER)
            .append_header((header::LOCATION, "/ui/login"))
            // Note this per-request server-side only cookie.
            .cookie(build_login_redirect_cookie(&request, message))
            .finish()
...			
```

We've <a href="#notes-on-cookies-our-own">previously</a> described 
<code>redirect-message</code>. In the <a href="#the-login-page-ui-login">following section</a>, 
we'll cover the <code>/ui/login</code> handler.

● An appropriate failure response has been provided, and the request is completed.

<a id="the-login-process-api-login-step-three"></a>
⓷ An employee's been found using an exact email match. The next step is to compare password. 

The function 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/auth_handlers.rs#L97"
title="Login process, attempt to match password"
target="_blank"><code>fn match_password_response(request: &HttpRequest, <br/>submitted_login: &EmployeeLogin, selected_login: &EmployeeLogin) -> Result&lt;(), HttpResponse></code></a>
handles password comparison. It uses the 
<a href="https://docs.rs/argon2/latest/argon2/" title="Crate argon2" target="_blank">argon2</a> 
crate to de-hash the database password and compare it to the submitted password.
We've briefly discussed this process in the section <a href="#hard-coded-employees-password">On the Hard-Coded Value for <code>employees.password</code></a>.

● If the passwords don't match, similar to 
<a href="#the-login-process-api-login-step-two">step ⓶ above</a>, 
we call the function 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/auth_handlers.rs#L63"
title="Login error, no match on employee email"
target="_blank"><code>fn first_stage_login_error_response(request: &HttpRequest, message: &str) -> HttpResponse</code></a> 
to return an appropriate HTTP response.

● The passwords don't match. An appropriate failure response has been provided, and the request is completed. 

<a id="the-login-process-api-login-step-four"></a>
⓸ Email-password login has been successful. Now, we're back in the endpoint 
handler for <code>/api/login</code>, <a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/auth_handlers.rs#L402"
title="The login process handler" target="_blank"><code>pub async fn login(request: HttpRequest, app_state: web::Data&lt;super::AppState>, <br/>body: Bytes) -> Either&lt;impl Responder, HttpResponse></code></a>.

```rust
...
    // TO_DO: Work in progress -- future implementations will formalise access token.
    let access_token = &selected_login.email;

    // https://docs.rs/actix-identity/latest/actix_identity/
    // Attach a verified user identity to the active session
    Identity::login(&request.extensions(), String::from(access_token)).unwrap();

    // The request content type is "application/x-www-form-urlencoded", returns the home page.
    if request.content_type() == ContentType::form_url_encoded().to_string() {
        Either::Right( HttpResponse::Ok()
            // Note this header.
            .append_header((header::AUTHORIZATION, String::from(access_token)))
            // Note this client-side cookie.
            .cookie(build_authorization_cookie(&request, access_token))
            .content_type(ContentType::html())
            .body(render_home_page(&request))
        )
    }
    else {
        // The request content type is "application/json", returns a JSON content of
        // LoginSuccessResponse.
        // 
        // Token field is the access token which the users need to include in the future 
        // requests to get authenticated and hence access to protected resources.		
        Either::Right( HttpResponse::Ok()
            // Note this header.
            .append_header((header::AUTHORIZATION, String::from(access_token)))
            // Note this client-side cookie.
            .cookie(build_authorization_cookie(&request, access_token))
            .content_type(ContentType::json())
            .body(login_success_json_response(&selected_login.email, &access_token))
        )
    }
...	
```

<a id="the-login-process-api-login-step-four-refactor-authentication"></a>
● The <a href="#definition-access-token"><code>access_token</code></a> 
is a work in progress. The main focus of this post is on the login and the 
<a href="#definition-request-auth"><code>request authentication</code></a>
processes. Setting the <a href="#definition-access-token"><code>access_token</code></a> 
to just the email is sufficient to get the entire process working, helping us understand 
how everything comes together better. We'll refactor this to a more formal type of 
authentication later.

● The line <code>Identity::login(&request.extensions(), String::from(access_token)).unwrap();</code>
is taken directly from the <a href="https://docs.rs/actix-identity/latest/actix_identity/" 
title="Crate actix_identity" target="_blank">actix-identity</a> crate. I believe this 
allows the application to operate as an <a href="#definition-app-server"><code>application server</code></a>.

<a id="the-login-process-api-login-step-four-authorization-header"></a>
● 🚀 Note that for all responses, the 
<a href="#definition-access-token"><code>access_token</code></a>  
is set in both the <code>authorization</code> header and the 
<code>authorization</code> cookie. This is intended for clients usage,
for example, in JavaScript. Clients have the option to extract and store this 
<a href="#definition-access-token"><code>access_token</code></a> 
for later use.

● 💥 Take note of this <code>authorization</code> header. <strong>It is
only available to clients, for example, in JavaScript.</strong> The 
<a href="#definition-request-auth-middleware"><code>request authentication middleware</code></a> 
also attempts to extract the 
<a href="#definition-access-token"><code>access_token</code></a> 
from this header, 
<a href="#request-authentication-works-extract-access-token">as explained earlier</a>. 
<strong>This header is set explicitly by clients
when making requests.</strong> While, at this point, it is a response header, 
and therefore, it will not be available again in later requests unless explicitly set.

And, finally:

● If the content type is <code>application/x-www-form-urlencoded</code>,
we return the HTML home page as is.

● If the content type is <code>application/json</code>,
we return a JSON serialisation of 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/models.rs#L61"
title="Login success, JSON response" target="_blank"><code>LoginSuccessResponse</code></a>.

<a id="the-login-page-ui-login"></a>
❷ The login page, <code>/ui/login</code> handler.

The login page handler is 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/auth_handlers.rs#L135"
title="The login page handler"
target="_blank"><code>pub async fn login_page(request: HttpRequest) -> Either&lt;impl Responder, HttpResponse></code></a>.

This route can be accessed in the following three ways: 

<a id="the-login-page-ui-login-direct-access"></a>
⓵ Direct access from the browser address bar, the login page HTML gets served 
as is. This is a common use case. The request content type is blank. 

<a id="the-login-page-ui-login-redirected-by-login-handler"></a>
⓶ Redirected to by the login process handler as 
<a href="#the-login-process-api-login-step-two">already discussed</a>.
It should be apparent that when this handler is called, 
the <em>server-side per-request</em> cookie <code>redirect-message</code> 
has already been set. The presence of this cookie signifies that
this handler is called after a fail login attempt. The value
of the <code>redirect-message</code> cookie is included in the
final response, and the HTTP response code is set to <code>401</code> 
for <code>UNAUTHORIZED</code>.

In this scenario, the request content type is available throughout the call stack.

<a id="the-login-page-ui-login-redirected-by-middleware"></a>
⓷ Redirected to by 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/auth_middleware.rs" 
title="src/auth_middleware.rs" target="_blank">src/auth_middleware.rs</a>. This
middleware is discussed in its own section titled 
<a href="#request-authentication-works">How the Request Authentication Process Works</a>.

At this point, we need to understand that, within the middleware, the closure 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/auth_middleware.rs#L208" 
title="src/auth_middleware.rs" target="_blank"><code>redirect_to_route = |req: ServiceRequest, route: &str| -> Self::Future</code></a>:

<ul>
<li style="margin-top:10px;">
Always creates the <em>server-side per-request</em> <code>original-content-type</code> 
cookie, with its value being the original request content type.
</li>
<li style="margin-top:10px;">
If it redirects to <code>/ui/login</code>, then creates the 
<em>server-side per-request</em> <code>redirect-message</code> 
cookie with a value set to the constant 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/helper/messages.rs#L8" 
title="Message constant UNAUTHORISED_ACCESS_MSG" target="_blank"><code>UNAUTHORISED_ACCESS_MSG</code></a>.
</li>
</ul>

<a id="the-login-page-handler"></a>
⓸ Back to the login page handler
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/auth_handlers.rs#L236"
title="The login page handler"
target="_blank"><code>pub async fn login_page(request: HttpRequest) -> Either&lt;impl Responder, HttpResponse></code></a>:

```rust
...
    let mut content_type: String = String::from(request.content_type());
    let mut status_code = StatusCode::OK;
    let mut message = String::from("");

    // Always checks for cookie REDIRECT_MESSAGE.
    if let Some(cookie) = request.cookie(REDIRECT_MESSAGE) {
        message = String::from(cookie.value());
        status_code = StatusCode::UNAUTHORIZED;

        if let Some(cookie) = request.cookie(ORIGINAL_CONTENT_TYPE) {
            if content_type.len() == 0 {
                content_type = String::from(cookie.value());
            }
        }
    }
...
```

From 
<a href="#the-login-page-ui-login-redirected-by-login-handler">section ⓶</a>
and 
<a href="#the-login-page-ui-login-redirected-by-middleware">section ⓷</a>,
it should be clear that the presence of the 
<em>server-side per-request</em> <code>redirect-message</code> cookie 
indicates a redirect access. If the request content type is not
available, we attempt to retrieve it from the <em>server-side per-request</em> 
<code>original-content-type</code> cookie.

Finally, it delivers the response based on the content type and removes 
both the <code>redirect-message</code> and <code>original-content-type</code> 
cookies. Note on the following code:

```rust
...
    else {
        Either::Left( 
            ApiStatus::new(http_status_code(status_code)).set_message(&message) 
        )
    }
...	
```

We implement 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/helper/app_utils.rs#L260" 
title="Implement Responder for ApiStatus" target="_blank">
<code>Responder trait</code> for <code>ApiStatus</code></a> as described in the
<a href="https://actix.rs/docs/handlers#response-with-custom-type" title="Response with custom type" target="_blank">Response with custom type</a>
section of the official documentation.

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;text-transform: none;">
  <a id="request-authentication-works">How the Request Authentication Process Works</a>
</h3>

Now, let's delve into the discussion of the 
<a href="#definition-request-auth-middleware"><code>request authentication middleware</code></a>.
Recall the definition of 
<a href="#definition-request-auth"><code>request authentication</code></a>

The essential logic of this new middleware is to determine if a request is from an
<a href="#definition-authenticated-session"><code>authenticated session</code></a>, 
and then either pass the request through or redirect to an appropriate route.

This logic can be described by the following pseudocode:

```
When Logged In
--------------

1. Requests to the routes “/ui/login” and “/api/login”
   are redirected to the route “/ui/home”.
   
2. Requests to any other routes should proceed.

When Not Logged In
------------------

1. Requests to the routes “/ui/login” and “/api/login” 
   should proceed.
   
2. Requests to any other route are redirected to 
   the route “/ui/login”.
```

This logic should cover all future routes. Since this middleware is registered last, 
it means that all <a href="#issues-covered-existing-routes">existing routes</a>
and potential future routes are protected by this middleware. 

A pair of helper functions discribed below is responsible for managing the 
<a href="#definition-request-auth"><code>request authentication</code></a> process.

<a id="request-authentication-works-extract-access-token"></a>
The helper function 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/auth_middleware.rs#L57" 
title="Helper function to extract access token" target="_blank"><code>fn extract_access_token(request: &ServiceRequest) -> Option&lt;String></code></a> 
looks for the <a href="#definition-access-token"><code>access token</code></a> in:

<ul>
<li style="margin-top:10px;">
The <code>authorization</code> header, 
<strong>which is set explicitly by clients when making requests.</strong>
</li>
<li style="margin-top:10px;">
If it isn't in the header, we look for it in the identity managed by the 
<a href="https://docs.rs/actix-identity/latest/actix_identity/" title="Crate actix_identity" target="_blank">actix-identity</a> 
crate as described 
<a href="#the-login-process-api-login-step-four">previously</a>.
</li>
<li style="margin-top:10px;">
Note: we could also look in the <code>authorization</code> cookie, but this code has been commented out to focus on testing the identity functionality.
</li>
</ul>

Function 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/auth_middleware.rs#L113" 
title="Helper function to verify access token" target="_blank"><code>fn verify_valid_access_token(request: &ServiceRequest) -> bool</code></a>
is a work in progress. It calls the <code>extract_access_token(...)</code> 
function to extract the <a href="#definition-access-token"><code>access token</code></a>. 
If none is found, the request is not authenticated. <strong>If something is found,
and it has a non-zero length, the 
<a href="#definition-authenticated-request"><code>request is considered authenticated</code></a>.</strong> 
<em>For the time being, this suffices to demonstrate the login and the
<a href="#definition-request-auth"><code>request authentication</code></a> processes.</em> 
<a id="the-login-process-api-login-step-four-refactor-authentication">
As mentioned previously</a>, this will be refactored later on.

The next essential piece of functionality is the closure 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/auth_middleware.rs#L208" 
title="src/auth_middleware.rs" target="_blank"><code>redirect_to_route = |req: ServiceRequest, route: &str| -> Self::Future</code></a>,
which must be <a href="#the-login-page-ui-login-redirected-by-middleware">
described in an earlier section</a>.

<a href="#the-login-page-ui-login-redirected-by-middleware">As discussed earlier</a>, 
this closure also creates the <em>server-side per-request</em> 
<code>original-content-type</code> cookie. This cookie is so obscured. 
To help addressing the obscurities, 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/helper/app_utils.rs#L154" 
title="Helper method which creates original-content-type cookie" 
target="_blank">the helper method</a> that creates this cookie comes
with extensive documentation explaining all scenarios where this cookie is
required.

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;text-transform: none;">
  <a id="the-home-page-and-logout-routes">The Home Page and the Logout Routes</a>
</h3>

❶ The home page handler 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/auth_handlers.rs#L437"
title="The home page handler" target="_blank"><code>pub async fn home_page(request: 
HttpRequest) -> impl Responder</code></a> is simple; it just delivers the HTML home page as is.

The 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/templates/auth/home.html"
title="The home page HTML" target="_blank"><code>home page HTML</code></a>
itself is also simple,  
without any CSS. It features a Logout button and other buttons 
whose event handler methods simply call the <a href="#issues-covered-existing-routes">existing routes</a>
using AJAX, displaying responses in plain JavaScript dialogs.

The AJAX function, <code>runAjaxEx(...)</code>, used by the home page, is also available 
<a href="https://github.com/behai-nguyen/js/blob/main/ajax_funcs.js" title="Function 
runAjaxEx(...)" target="_blank">on GitHub</a>. It makes references to some 
<a href="https://getbootstrap.com/" title="Bootstrap CSS classes" target="_blank">Bootstrap 
CSS classes</a>, but that should not be a problem for this example.

❷ There is also not much in the logout process handler, 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/auth_handlers.rs#L461"
title="The logout process handler"
target="_blank"><code>async fn logout(request: HttpRequest, user: Identity) -> impl Responder</code></a>.

The code, especially <code>user.logout(),</code> is taken directly from the
<a href="https://docs.rs/actix-identity/latest/actix_identity/" title="Crate actix_identity" target="_blank">actix-identity</a> 
crate.

The handler removes the application wide <code>authorization</code> cookie 
and redirects to the login page, delivering the HTML login page as is.

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;text-transform: none;">
  <a id="integration-tests">Integration Tests</a>
</h3>

<code>Test</code> and <code>tests</code> in this section 
mean <code>integration test</code> and <code>integration tests</code>,
respectively.

Code has changed. Existing tests and some common test code must be 
updated. New tests are added to test new functionalities.

The application now uses cookies, all tests must enable cookie 
usage. We'll also cover this in a <a href="#integration-tests-enble-cookies">later section</a>.

<a id="integration-tests-common"></a>
❶ Common test code.

Now that an <a href="#definition-access-token"><code>access_token</code></a>
is required to access protected routes. To log in every time to test is not 
always appropriate. We want to ensure that the code can extract the 
<a href="#definition-access-token"><code>access_token</code></a>
from the <code>authorization</code> header.

I did look into the <code>setup</code> and <code>tear down</code>
test setup in Rust. The intention is, in <code>setup</code>
we'll do a login, remember the 
<a href="#definition-access-token"><code>access_token</code></a>
and use it in proper tests. In <code>tear down</code>, we  
log out. But this seems troublesome in Rust. I gave up
on this idea.

Recall from 
<a href="#request-authentication-works-extract-access-token">
this discussion</a> that <em>currently, anything that is non-blank
is considered a valid 
<a href="#definition-access-token"><code>access_token</code></a>!</em> 

💥 We've settled on a compromise for this code revision: we will 
implement a method that returns a hard-coded 
<a href="#definition-access-token"><code>access_token</code></a>. 
As we proceed with the authentication refactoring, we'll also update 
this method accordingly.

In the 
<a href="https://behainguyen.wordpress.com/2023/12/31/rust-retrofit-integration-tests-to-an-existing-actix-web-application/" title="Rust: retrofit integration tests to an existing actix-web application." target="_blank">third post</a>, 
we've incorporated tests following the approach outlined by Luca Palmieri 
in the 59-page sample extract of his book 
<a href="https://www.zero2prod.com/assets/sample_zero2prod.pdf"
title="ZERO TO PRODUCTION IN RUST by Luca Palmieri"
target="_blank">ZERO TO PRODUCTION IN RUST</a>.
Continuing with this approach, we'll define a simple <code>TestApp</code> in 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/tests/common.rs#L15"
title="tests/common.rs" target="_blank">tests/common.rs</a>:

```rust
pub struct TestApp {
    pub app_url: String,
}

impl TestApp {
    pub fn mock_access_token(&self) -> String {
        String::from("chirstian.koblick.10004@gmail.com")
    }    
}
```

And <code>spawn_app()</code> now returns an instance of <code>TestApp</code>.
We can then call the method <code>mock_access_token()</code> on this instance 
to use the hard-coded <a href="#definition-access-token"><code>access_token</code></a>.

<a id="integration-tests-enble-cookies"></a>
❷ Enble cookies in tests.

We use the
<a href="https://docs.rs/reqwest/latest/reqwest/" title="reqwest" target="_blank">reqwest</a>
crate to send requests to the application. To enable cookies, 
we create a client using the 
<a href="https://docs.rs/reqwest/latest/reqwest/struct.Client.html#method.builder"
title="The builder() method" target="_blank">builder method</a> 
and chain to 
<a href="https://docs.rs/reqwest/latest/reqwest/struct.ClientBuilder.html#method.cookie_store"
title="The cookie_store(...) method" target="_blank">cookie_store(true)</a>:

```rust
    let client = reqwest::Client::builder()
        .cookie_store(true)
        .build()
        .unwrap();
```

<a id="integration-tests-existing"></a>
❸ Existing tests.

All existing tests in 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/tests/test_handlers.rs"
title="tests/test_handlers.rs" target="_blank">tests/test_handlers.rs</a> 
must be updated as outlined above, for example:

```rust
async fn get_helloemployee_has_data() {
    let test_app = &spawn_app().await;

    let client = reqwest::Client::builder()
        .cookie_store(true)
        .build()
        .unwrap();

    let response = client
        .get(make_full_url(&test_app.app_url, "/helloemployee/%chi/%ak"))
        .header(header::AUTHORIZATION, &test_app.mock_access_token())
        .send()
        .await
        .expect("Failed to execute request.");    

    assert_eq!(response.status(), StatusCode::OK);

    let res = response.text().await;
    assert!(res.is_ok(), "Should have a HTML response.");

    // This should now always succeed.
    if let Ok(html) = res {
        assert!(html.contains("Hi first employee found"), "HTML response error.");
    }
}
```

<a id="integration-tests-new"></a>
❹ New tests.

⓵ We have a new test module, 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/tests/test_auth_handlers.rs"
title="tests/test_auth_handlers.rs" target="_blank">tests/test_auth_handlers.rs</a>,
exclusively for testing the newly added authentication routes. There are a total of 
eleven tests, with eight dedicated to login and six focused on accessing 
existing protected routes without the <code>authorization</code> header set.

⓶ In the existing test module, 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/tests/test_handlers.rs"
title="tests/test_handlers.rs" target="_blank">tests/test_handlers.rs</a>, we've added 
six more tests. These tests focused on accessing existing protected routes without 
the <code>authorization</code> header set. These test functions ended with 
<code>_no_access_token</code>.

These new tests should be self-explanatory. We will not go into detail.

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;text-transform: none;">
  <a id="some-manual-tests">Some Manual Tests</a>
</h3>

❶ Home page: demonstrating the project as an <a href="#definition-app-server"><code>application server</code></a>.

The gallery below shows the home page, and responses from some of the routes:

{% include image-gallery.html list=page.gallery-image-list-1 %}

❷ While logged in, enter <code>http://192.168.0.16:5000/data/employees/%chi/%ak</code> 
in the browser address bar, we get the JSON response as expected:

![096-02.png](https://behainguyen.files.wordpress.com/2024/01/096-02.png)

Next, enter <code>http://192.168.0.16:5000/ui/login</code> directly 
in the browser address bar. This should bring us back to the home page.

❸ While not logged in, 
enter <code>http://192.168.0.16:5000/data/employees/%chi/%ak</code> 
directly in the browser address bar. This redirects us to the login 
page with an appropriate message:

![096-03.png](https://behainguyen.files.wordpress.com/2024/01/096-03.png)

❹ Attempt to log in with an incorrect email and/or password:

![096-04.png](https://behainguyen.files.wordpress.com/2024/01/096-04.png)

❺ Access the JSON response route <code>http://192.168.0.16:5000/data/employees</code>
with the <code>authorization</code> header. This usage demonstrate the application 
as an <a href="#definition-api-server"><code>API-like server</code> or a 
<code>service</code></a>:

{% include image-gallery.html list=page.gallery-image-list-2 %}

❻ Access <code>http://192.168.0.16:5000/data/employees/%chi/%ak</code>
without the <code>authorization</code> header. 
While the successful response is in JSON, the request lacks a content type. 
<a href="#definition-request-auth"><code>Request authentication</code></a>
fails, the response is the HTML login page

![096-06-no-auth-header-get.png](https://behainguyen.files.wordpress.com/2024/01/096-06-no-auth-header-get.png)

❼ Access the same <code>http://192.168.0.16:5000/data/employees/%chi/%ak</code>
with the <code>authorization</code> header. This should result in a successful 
JSON response as expected:

![096-07-auth-header-get.png](https://behainguyen.files.wordpress.com/2024/01/096-07-auth-header-get.png)

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;text-transform: none;">
  <a id="rust-users-forum-helps">Rust Users Forum Helps</a>
</h3>

I received a lot of help from the 
<a href="https://users.rust-lang.org/" title="Rust Users Forum" target="_blank">Rust Users Forum</a>
while learning <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a>
and Rust:

<ul>
<li style="margin-top:10px;">
<a href="https://users.rust-lang.org/t/actix-web-middleware-redirect-with-extension-data-please-help/103431"
title="actix-web middleware redirect with extension data, please help."
target="_blank">actix-web middleware redirect with extension data, please help</a>;
particularly, this 
<a href="https://users.rust-lang.org/t/actix-web-middleware-redirect-with-extension-data-please-help/103431/5?u=behai"
title="reply by user jofas" target="_blank">reply by user jofas</a> helped me 
enormously in understanding how
<a href="https://docs.rs/actix-web/latest/actix_web/middleware/index.html"
title="actix-web middleware" target="_blank">actix-web middleware</a> works.
</li>

<li style="margin-top:10px;">
<a href="https://users.rust-lang.org/t/actix-web-how-to-determine-if-a-called-route-was-a-redirect/105013"
title="actix-web: how to determine if a called route was a redirect?"
target="_blank">actix-web: how to determine if a called route was a redirect?</a>
Based on the answers provided by other users, I decided to use the <code>redirect-message</code> 
cookie.
</li>
</ul>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;text-transform: none;">
  <a id="some-current-issues">Some Current Issues</a>
</h3>

❶ <code>println!</code> should be replaced with proper logging. I plan to implement logging to files later on.

❷ The 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/45274f0797101bb4001a29cc572684d70b6bf6fb/src/auth_handlers.rs#L63"
title="Login error, no match on employee email"
target="_blank"><code>fn first_stage_login_error_response(request: &HttpRequest, message: &str) -> HttpResponse</code></a> 
helper function, 
<a href="#the-login-process-api-login-step-two">discussed in this section</a>,
redirects requests to the route <code>/ui/login</code>; 
<a href="#the-login-page-ui-login">whose handler</a> is capable 
of handling both <code>application/x-www-form-urlencoded</code> 
and <code>application/json</code>. 
And for that reason, this helper function could be refactored to:

```rust
fn first_stage_login_error_response(
    request: &HttpRequest,
    message: &str
) -> HttpResponse {
	HttpResponse::Ok()
		.status(StatusCode::SEE_OTHER)
		.append_header((header::LOCATION, "/ui/login"))
		// Note this per-request server-side only cookie.
		.cookie(build_login_redirect_cookie(&request, message))
		.finish()
}
```

It seems logical, but it does not work when we log in using JSON 
with either an invalid email or password. The client tools simply 
report that the request could not be completed. I haven't been able 
to work out why yet.

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;text-transform: none;">
  <a id="concluding-remarks">Concluding Remarks</a>
</h3>

I do apologise that this post is a bit too long. I can't help 
it. I include all the details which I think are relevant. It has taken 
nearly two months for me to arrive at this point in the code. It is a 
significant learning progress for me.

We haven't completed this project yet. I have several other objectives in 
mind. While I'm unsure about the content of the next post for this project, 
there will be one.

Thank you for reading. I hope you find this post useful. Stay safe, as always.

<!--------------------------------------------------------------------------------->

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
<a href="https://www.rust-lang.org/" target="_blank">https://www.rust-lang.org/</a>
</li>
<li>
<a href="https://www.pngitem.com/download/ibmJoR_rust-language-hd-png-download/" target="_blank">https://www.pngitem.com/download/ibmJoR_rust-language-hd-png-download/</a>
</li>
</ul>