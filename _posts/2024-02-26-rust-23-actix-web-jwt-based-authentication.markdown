---
layout: post
title: "Rust: actix-web JSON Web Token authentication."

description: In the sixth post of our actix-web learning application, we implemented a basic email-password login process with a placeholder for a token. In this post, we will implement a comprehensive JSON Web Token (JWT)-based authentication system. We will utilise the jsonwebtoken crate, which we have previously studied.

tags:

- Rust
- actix-web
- JSON Web Token
- JWT
- authentication
---

<em>In the <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/" title="Rust: simple actix-web email-password login and request authentication using middleware." target="_blank">sixth</a> post of our <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> learning application, we implemented a basic email-password login process with a placeholder for a <code>token</code>. In this post, we will implement a comprehensive JSON Web Token (JWT)-based authentication system. We will utilise the <a href="https://docs.rs/jsonwebtoken/latest/jsonwebtoken/index.html" title="jsonwebtoken" target="_blank">jsonwebtoken</a> crate, which we have <a href="https://behainguyen.wordpress.com/2023/11/20/rust-json-web-token-some-investigative-studies-on-crate-jsonwebtoken/" title="Rust: JSON Web Token -- some investigative studies on crate jsonwebtoken" target="_blank">previously studied</a>.</em>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rust_web_01" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![100-feature-image.png](https://behainguyen.files.wordpress.com/2024/02/100-feature-image.png) |
|:--:|
| *Rust: actix-web JSON Web Token authentication.* |

🚀 <strong>Please note,</strong> complete code for this post can be downloaded from GitHub with:

```
git clone -b v0.10.0 https://github.com/behai-nguyen/rust_web_01.git
```

The <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> learning application mentioned above has been discussed in the following nine previous posts:

<ol>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/10/18/rust-web-application-mysql-server-sqlx-actix-web-and-tera/" title="Rust web application: MySQL server, sqlx, actix-web and tera" target="_blank">Rust web application: MySQL server, sqlx, actix-web and tera</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/11/26/rust-learning-actix-web-middleware-01/" title="Rust: learning actix-web middleware 01" target="_blank">Rust: learning actix-web middleware 01</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/12/31/rust-retrofit-integration-tests-to-an-existing-actix-web-application/" title="Rust: retrofit integration tests to an existing actix-web application." target="_blank">Rust: retrofit integration tests to an existing actix-web application</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/01/03/rust-adding-actix-session-and-actix-identity-to-an-existing-actix-web-application/" title="Rust: adding actix-session and actix-identity to an existing actix-web application." target="_blank">Rust: adding actix-session and actix-identity to an existing actix-web application</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/01/14/rust-actix-web-endpoints-which-accept-both-application-x-www-form-urlencoded-and-application-json-content-types/" title="Rust: actix-web endpoints which accept both application/x-www-form-urlencoded and application/json content types." target="_blank">Rust: actix-web endpoints which accept both <code>application/x-www-form-urlencoded</code> and <code>application/json</code> content types</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/" title="Rust: simple actix-web email-password login and request authentication using middleware." target="_blank">Rust: simple actix-web email-password login and request authentication using middleware</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/02/10/rust-actix-web-get-ssl-https-for-localhost/" title="Rust: actix-web get SSL/HTTPS for localhost." target="_blank">Rust: actix-web get SSL/HTTPS for localhost</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/02/13/rust-actix-web-cors-cookies-and-ajax-calls/" title="Rust: actix-web CORS, Cookies and AJAX calls." target="_blank">Rust: actix-web CORS, Cookies and AJAX calls</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/02/16/rust-actix-web-global-extractor-error-handlers/" title="Rust: actix-web global extractor error handlers" target="_blank">Rust: actix-web global extractor error handlers</a>.</li>
</ol>

The code we're developing in this post is a continuation of the code from the <a href="https://behainguyen.wordpress.com/2024/02/16/rust-actix-web-global-extractor-error-handlers/" title="Rust: actix-web global extractor error handlers" target="_blank">ninth</a> post above. 🚀 To get the code of this <a href="https://behainguyen.wordpress.com/2024/02/16/rust-actix-web-global-extractor-error-handlers/" title="Rust: actix-web global extractor error handlers" target="_blank">ninth</a> post, please use the following command:

```
git clone -b v0.9.0 https://github.com/behai-nguyen/rust_web_01.git
```

<strong>-- Note the tag <code>v0.9.0</code>.</strong>

<h2>Table of contents</h2>
<ul>
<li style="margin-top:10px;">
<a href="#previous-studies-jwt">Previous Studies on JSON Web Token (JWT)</a>
</li>
<li style="margin-top:10px;">
<a href="#jwt-implementations">Proposed JWT Implementations: Problems and Solutions</a>
<ul>
<li style="margin-top:10px;">
<a href="#proposed-jwt-impl">Proposed JWT Implementations</a>
</li>
<li style="margin-top:10px;">
<a href="#proposed-jwt-impl-problems">Problems with the Proposed Implementations</a>
<ul>
<li style="margin-top:10px;">
<a href="#proposed-jwt-impl-problems-api-server">Problems when Used as an API-Server or Service</a>					
</li>
<li style="margin-top:10px;">
<a href="#proposed-jwt-impl-problems-app-server">Problems when Used as an Application Server</a>					
</li>
</ul>				
</li>
<li style="margin-top:10px;">
<a href="#proposed-jwt-impl-solutions">Proposed Solutions</a>
</li>			
</ul>
</li>
<li style="margin-top:10px;">
<a href="#bearer-token">The “Bearer” Token Scheme</a>
</li>
<li style="margin-top:10px;">
<a href="#project-layout">Project Layout</a>
</li>
<li style="margin-top:10px;">
<a href="#token-utility-and-test">The Token Utility jwt_utils.rs and Test test_jsonwebtoken.rs Modules</a>
<ul>
<li style="margin-top:10px;">
<a href="#token-utility-and-test-module">The Token Utility src/helper/jwt_utils.rs Module</a>
</li>
<li style="margin-top:10px;">
<a href="#token-utility-and-test-test">The Test tests/test_jsonwebtoken.rs Module</a>
</li>
</ul>
</li>
<li style="margin-top:10px;">
<a href="#updated-login-process">The Updated Login Process</a>
</li>
<li style="margin-top:10px;">
<a href="#updated-request-auth-process">The Updated Request Authentication Process</a>
<ul>
<li style="margin-top:10px;">
<a href="#updated-request-auth-process-mw">Code Updated in the src/auth_middleware.rs Module</a>
</li>
<li style="margin-top:10px;">
<a href="#updated-request-auth-process-lib">Code Updated in the src/lib.rs Module</a>
</li>
</ul>
</li>
<li style="margin-top:10px;">
<a href="#jwt-and-logout">JWT and Logout</a>
</li>
<li style="margin-top:10px;">
<a href="#updated-integration-tests">Updating Integration Tests</a>
</li>	
<li style="margin-top:10px;">
<a href="#concluding-remarks">Concluding Remarks</a>
</li>
</ul>

<h3 style="color:teal;text-transform: none;">
  <a id="previous-studies-jwt">Previous Studies on JSON Web Token (JWT)</a>
</h3>

As mentioned earlier, we conducted studies on the <a href="https://docs.rs/jsonwebtoken/latest/jsonwebtoken/index.html" title="jsonwebtoken" target="_blank">jsonwebtoken</a> crate, as detailed in the post titled <a href="https://behainguyen.wordpress.com/2023/11/20/rust-json-web-token-some-investigative-studies-on-crate-jsonwebtoken/" title="Rust: JSON Web Token -- some investigative studies on crate jsonwebtoken" target="_blank">Rust: JSON Web Token -- some investigative studies on crate jsonwebtoken</a>. The JWT implementation in this post is based on the specifications discussed in the <a href="https://behainguyen.wordpress.com/2023/11/20/rust-json-web-token-some-investigative-studies-on-crate-jsonwebtoken/#the-second-example" title="Rust: JSON Web Token -- some investigative studies on crate jsonwebtoken" target="_blank">second example</a> of the aforementioned post, particularly focusing on this specification:

> 🚀 <strong>It should be obvious that: <em>this implementation implies <code>SECONDS_VALID_FOR</code> is the duration the token stays valid since last active</em></strong>. It does not mean that after this duration, the token becomes invalid or expired. So long as the client keeps sending requests while the token is valid, it will never expire!

We will provide further details on this specification later in the post. Additionally, before <a href="https://behainguyen.wordpress.com/2023/11/20/rust-json-web-token-some-investigative-studies-on-crate-jsonwebtoken/" title="Rust: JSON Web Token -- some investigative studies on crate jsonwebtoken" target="_blank">studying the jsonwebtoken crate</a>, we conducted research on the <a href="https://docs.rs/jwt-simple/latest/jwt_simple/" title="jwt-simple" target="_blank">jwt-simple</a> crate, as discussed in the post titled <a href="https://behainguyen.wordpress.com/2023/11/17/rust-json-web-token-some-investigative-studies-on-crate-jwt-simple/" title="Rust: JSON Web Token -- some investigative studies on crate jwt-simple" target="_blank">Rust: JSON Web Token -- some investigative studies on crate jwt-simple</a>. It would be beneficial to review this post as well, as it covers background information on JWT.

<h3 style="color:teal;text-transform: none;">
  <a id="jwt-implementations">Proposed JWT Implementations: Problems and Solutions</a>
</h3>

<h4 style="color:teal;text-transform: none;">
  <a id="proposed-jwt-impl">Proposed JWT Implementations</a>
</h4>

Let's revisit the specifications outlined in the previous section:

> 🚀 <strong>It should be obvious that: <em>this implementation implies <code>SECONDS_VALID_FOR</code> is the duration the token stays valid since last active</em></strong>. It does not mean that after this duration, the token becomes invalid or expired. So long as the client keeps sending requests while the token is valid, it will never expire!

This concept involves extending the expiry time of a valid token every time a request is made. This functionality was demonstrated in the original discussion, specifically in the <a href="https://behainguyen.wordpress.com/2023/11/20/rust-json-web-token-some-investigative-studies-on-crate-jsonwebtoken/#the-second-example" title="Rust: JSON Web Token -- some investigative studies on crate jsonwebtoken" target="_blank">second example</a> section mentioned earlier.

🦀 <strong><em>Since the expiry time is updated, we generate a new <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-access-token" title="access token" target="_blank"><code>access token</code></a>. </em></strong> Here's what we do with the new token:

<ol>
<li style="margin-top:10px;">
Replace the current <a href="https://docs.rs/actix-identity/0.7.0/actix_identity/struct.Identity.html" title="actix-identity Identity" target="_blank">actix-identity::Identity</a> login with the new <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-access-token" title="access token" target="_blank"><code>access token</code></a>.
</li>
<li style="margin-top:10px;">
<strong>Always</strong> send the new <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-access-token" title="access token" target="_blank"><code>access token</code></a> to clients via both the response header and the response cookie <code>authorization</code>, as in the <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#the-login-process-api-login" title="login process" target="_blank">login process</a>.
</li>
</ol>

We generate a new <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-access-token" title="access token" target="_blank"><code>access token</code></a> based on logic, but it doesn't necessarily mean the previous ones have expired."

<h4 style="color:teal;text-transform: none;">
  <a id="proposed-jwt-impl-problems">Problems with the Proposed Implementations</a>
</h4>

The proposed implementations outlined above present some practical challenges, which we will discuss next. 

<span style="color:blue;font-weight:bold;">However, for the sake of learning in this project, we will proceed with the proposed implementations despite the identified issues.</span>

<h5 style="color:teal;text-transform: none;">
  <a id="proposed-jwt-impl-problems-api-server">Problems when Used as an API-Server or Service</a>
</h5>

In an <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-api-server" title="API-like server or a service" target="_blank"><code>API-like server</code> or a <code>service</code></a>, users are required to include a valid <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-access-token" title="access token" target="_blank"><code>access token</code></a> in the request <code>authorization</code> header. Therefore, if a new token is generated, users should have access to this latest token.

<a id="proposed-jwt-impl-problems-api-server-problems"></a>
What happens if users simply ignore the new tokens and continue using a previous one that has not yet expired? In such a scenario, <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-request-auth" title="request authentication" target="_blank"><code>request authentication</code></a> would still be successful, and the requests would potentially succeed until the old token expires. However, a more serious concern arises if we implement blacklisting. In that case, we would need to blacklist all previous tokens. This would necessitate writing the current access token to a blacklist table for every request, which is impractical.

<h5 style="color:teal;text-transform: none;">
  <a id="proposed-jwt-impl-problems-app-server">Problems when Used as an Application Server</a>
</h5>

When used as an <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-app-server" title="application server" target="_blank"><code>application server</code></a>, we simply replace the current <a href="https://docs.rs/actix-identity/0.7.0/actix_identity/struct.Identity.html" title="actix-identity Identity" target="_blank">actix-identity::Identity</a> login with the new <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-access-token" title="access token" target="_blank"><code>access token</code></a>. If we implement blacklisting, we only need to blacklist the last token

🚀 This process makes sense, as we cannot expire a session while a user is still actively using it.

<a id="proposed-jwt-impl-problems-app-server-problems"></a> However, we still encounter similar problems <a href="#proposed-jwt-impl-problems-api-server-problems">as described</a> in the previous section for <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-api-server" title="API-like server or a service" target="_blank"><code>API-like servers</code> or <code>services</code></a>. Since clients always have access to the <code>authorization</code> response header and cookie, they can use this token with different client tools to send requests, effectively treating the application as an <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-api-server" title="API-like server or a service" target="_blank"><code>API-like server</code> or a <code>service</code></a>.

<h4 style="color:teal;text-transform: none;">
  <a id="proposed-jwt-impl-solutions">Proposed Solutions</a>
</h4>

The above problems would disappear, and the actual implementations would be simpler if we adjust the logic slightly:

<ol>
<li style="margin-top:10px;">
<strong>Only</strong> send the <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-access-token" title="access token" target="_blank"><code>access token</code></a> to clients <strong>once if the content type of the login request is <code>application/json</code></strong>.
</li>
<li style="margin-top:10px;">
Then users of an <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-api-server" title="API-like server or a service" target="_blank"><code>API-like server</code> or a <code>service</code></a> will only have one <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-access-token" title="access token" target="_blank"><code>access token</code></a> until it expires. They will need to log in again to obtain a new token.
</li>
<li style="margin-top:10px;">
Still replace the current <a href="https://docs.rs/actix-identity/0.7.0/actix_identity/struct.Identity.html" title="actix-identity Identity" target="_blank">actix-identity::Identity</a> login with the new <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-access-token" title="access token" target="_blank"><code>access token</code></a>. The <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-app-server" title="application server" target="_blank"><code>application server</code></a> continues to function as usual. However, since users no longer have access to the token, we only need to manage the one stored in the <a href="https://docs.rs/actix-identity/0.7.0/actix_identity/struct.Identity.html" title="actix-identity Identity" target="_blank">actix-identity::Identity</a> login.
</li>
</ol>

<span style="color:blue;font-weight:bold;">
But as mentioned at the start of this section, we will ignore the problems and, therefore, the solutions for this revision of the code.
</span>

<h3 style="color:teal;text-transform: none;">
  <a id="bearer-token">The “Bearer” Token Scheme</a>
</h3>

We adhere to the “Bearer” token scheme as specified in <a href="https://datatracker.ietf.org/doc/html/rfc6750" title="The OAuth 2.0 Authorization Framework: Bearer Token Usage" target="_blank">RFC 6750</a>, section <a href="https://datatracker.ietf.org/doc/html/rfc6750#page-5" title="2.1. Authorization Request Header Field" target="_blank">2.1. Authorization Request Header Field</a>:

```
    For example:
        GET /resource HTTP/1.1
        Host: server.example.com
        Authorization: Bearer mF_9.B5f-4.1JqM
```

That is, the <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-access-token" title="access token" target="_blank"><code>access token</code></a> used during <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-request-auth" title="request authentication" target="_blank"><code>request authentication</code></a> is in the format:

```
Bearer. + the proper JSON Web Token
```

For example:

```
Bearer.eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImNoaXJzdGlhbi5rb2JsaWNrLjEwMDA0QGdtYWlsLmNvbSIsImlhdCI6MTcwODU1OTcwNywiZXhwIjoxNzA4NTYxNTA3LCJsYXN0X2FjdGl2ZSI6MTcwODU1OTcwN30.CN-whQ0rWW8IuLPVTF7qprk4-GgtK1JSJqp3C8X-ytE
```

❶ The <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-access-token" title="access token" target="_blank"><code>access token</code></a> included in the request <code>authorization</code> header must adhere to the "Bearer" token format.

❷ Similarly, the <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-access-token" title="access token" target="_blank"><code>access token</code></a> set for the <a href="https://docs.rs/actix-identity/0.7.0/actix_identity/struct.Identity.html" title="actix-identity Identity" target="_blank">actix-identity::Identity</a> login is also a "Bearer" token.

🦀 However, the <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-access-token" title="access token" target="_blank"><code>access token</code></a> sent to clients via the response header and the response cookie <code>authorization</code> is always a pure JSON Web Token.

<h3 style="color:teal;text-transform: none;">
  <a id="project-layout">Project Layout</a>
</h3>

Below is the complete project layout.

<strong>-- Please note,</strong> those marked with <span style="font-size:1.5em;">★</span> are updated, and those marked with <span style="font-size:1.5em;">☆</span> are new.

<a id="project-layout-chart"></a>
```
.
├── .env ★
├── Cargo.toml ★
├── cert
│ ├── cert-pass.pem
│ ├── key-pass-decrypted.pem
│ └── key-pass.pem
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
│ ├── auth_middleware.rs ★
│ ├── bh_libs
│ │ ├── api_status.rs
│ │ └── australian_date.rs
│ ├── bh_libs.rs
│ ├── config.rs ★
│ ├── database.rs
│ ├── handlers.rs
│ ├── helper
│ │ ├── app_utils.rs ★
│ │ ├── constants.rs ★
│ │ ├── endpoint.rs ★
│ │ ├── jwt_utils.rs ☆
│ │ └── messages.rs ★
│ ├── helper.rs ★
│ ├── lib.rs ★
│ ├── main.rs
│ ├── middleware.rs
│ └── models.rs ★
├── templates
│ ├── auth
│ │ ├── home.html
│ │ └── login.html
│ └── employees.html
└── tests
    ├── common.rs ★
    ├── test_auth_handlers.rs ★
    ├── test_handlers.rs ★
    └── test_jsonwebtoken.rs ☆
```

<h3 style="color:teal;text-transform: none;">
  <a id="token-utility-and-test">The Token Utility jwt_utils.rs and Test test_jsonwebtoken.rs Modules</a>
</h3>

<h4 style="color:teal;text-transform: none;">
  <a id="token-utility-and-test-module">The Token Utility src/helper/jwt_utils.rs Module</a>
</h4>

In the module <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/helper/jwt_utils.rs" title="src/helper/app_utils.rs" target="_blank">src/helper/jwt_utils.rs</a>, we implement all the JWT management code, which includes the core essential code that somewhat repeats the code already mentioned in the <a href="https://behainguyen.wordpress.com/2023/11/20/rust-json-web-token-some-investigative-studies-on-crate-jsonwebtoken/#the-second-example" title="Rust: JSON Web Token -- some investigative studies on crate jsonwebtoken" target="_blank">second example</a>:

<ul>
<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/helper/jwt_utils.rs#L25" title="src/helper/app_utils.rs JWTPayload" target="_blank"> <code>struct JWTPayload</code></a> -- represents the JWT payload, where the <code>email</code> field uniquely identifies the logged-in user.
</li>

<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/helper/jwt_utils.rs#L64" title="src/helper/app_utils.rs impl JWTPayload" target="_blank"><code>JWTPayload implementation</code></a> -- implements some of the required functions and methods:
<ul>
<li style="margin-top:10px;">
A function to create a new instance.
</li>
<li style="margin-top:10px;">
Methods to update the expiry field (<code>exp</code>) and the <code>last_active</code> field using seconds, minutes, and hours.
</li>
<li style="margin-top:10px;">
Four getter methods which return the values of the <code>iat</code>, <code>email</code>, <code>exp</code>, and <code>last_active</code> fields.
</li>
</ul>
</li>
</ul>

Additionally, there are two main functions:

<ol>
<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/helper/jwt_utils.rs#L187" title="src/helper/app_utils.rs pub fn make_token" target="_blank"><code>pub fn make_token</code></a> -- creates a new JWT from an <code>email</code>. The parameter <code>secs_valid_for</code> indicates how many seconds the token is valid for, and the parameter <code>secret_key</code> is used by the <a href="https://docs.rs/jsonwebtoken/latest/jsonwebtoken/index.html" title="jsonwebtoken" target="_blank">jsonwebtoken</a> crate to encode the token. It creates an instance of <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/helper/jwt_utils.rs#L25" title="src/helper/app_utils.rs JWTPayload" target="_blank"><code>struct JWTPayload</code></a>, and then creates a token using this instance.
</li>
<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/helper/jwt_utils.rs#L262" title="src/helper/app_utils.rs pub fn decode_token" target="_blank"><code>pub fn decode_token</code></a> -- decodes a given token. If the token is valid and successfully decoded, it returns the token's <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/helper/jwt_utils.rs#L25" title="src/helper/app_utils.rs JWTPayload" target="_blank"><code>struct JWTPayload</code></a>. Otherwise, it returns an <a href="https://github.com/behai-nguyen/rust_web_01/blob/e5fa751f1454bf3ffe3ad72a7c70c6169402bfcb/src/bh_libs/api_status.rs#L18" title="src/bh_libs/api_status.rs ApiStatus" target="_blank"><code>ApiStatus</code></a> which describes the error.
</li>
</ol>

<p>
Other functions are “convenient” functions or wrapper functions:
</p>

<ol>
<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/helper/jwt_utils.rs#L217" title="src/helper/app_utils.rs pub fn make_token_from_payload" target="_blank"><code>pub fn make_token_from_payload</code></a> -- creates a JWT from an instance of struct <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/helper/jwt_utils.rs#L25" title="src/helper/app_utils.rs JWTPayload" target="_blank"><code>struct JWTPayload</code></a>. It is a "convenient" function. We decode the current token, update the extracted payload, then call this function to create an updated token.
</li>
<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rust_web_01/blob/main/src/helper/jwt_utils.rs#L242" title="src/helper/app_utils.rs pub fn make_bearer_token" target="_blank"><code>pub fn make_bearer_token</code></a> -- a wrapper function that creates a <a href="#bearer-token">“Bearer” token</a> from a given token.
</li>
<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/helper/jwt_utils.rs#L309" title="src/helper/app_utils.rs pub fn decode_bearer_token" target="_blank"><code>pub fn decode_bearer_token</code></a> -- a wrapper function that decodes a <a href="#bearer-token">“Bearer” token</a>.
</li>
</ol>

Please note also the unit test section in this module. There are sufficient tests to cover all functions and methods.

The documentation in the source code should be sufficient to aid in the reading of the code.

<h4 style="color:teal;text-transform: none;">
  <a id="token-utility-and-test-test">The Test tests/test_jsonwebtoken.rs Module</a>
</h4>

We implement some integration tests for JWT management code. These tests are self-explanatory.

<h3 style="color:teal;text-transform: none;">
  <a id="updated-login-process">The Updated Login Process</a>
</h3>

In the current <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#the-login-process-api-login" title="login process" target="_blank">login process</a>, at <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#the-login-process-api-login-step-four" title="login process step 4" target="_blank">step 4</a>, we note: 

```rust
...
    // TO_DO: Work in progress -- future implementations will formalise access token.
    let access_token = &selected_login.email;

    // https://docs.rs/actix-identity/latest/actix_identity/
    // Attach a verified user identity to the active session
    Identity::login(&request.extensions(), String::from(access_token)).unwrap();
...	
```

This part of the login process handler <a href="https://github.com/behai-nguyen/rust_web_01/blob/main/src/auth_handlers.rs#L388" title="The login process handler" target="_blank"><code>pub async fn login(request: HttpRequest, app_state: web::Data&lt;super::AppState>, body: Bytes) -> Either&lt;impl Responder, HttpResponse></code></a> is updated to:

```rust
...
    let access_token = make_token(&selected_login.email, 
        app_state.cfg.jwt_secret_key.as_ref(), app_state.cfg.jwt_mins_valid_for * 60);

    // https://docs.rs/actix-identity/latest/actix_identity/
    // Attach a verified user identity to the active session
    Identity::login(&request.extensions(), String::from( make_bearer_token(&access_token) )).unwrap();
...	
```

Please note the call to <code>make_bearer_token</code>, which adheres to <a href="#bearer-token">The “Bearer” Token Scheme</a>.

This update would take care of the <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-app-server" title="application server" target="_blank"><code>application server</code></a> case. In the case of an <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-api-server" title="API-like server or a service" target="_blank"><code>API-like server</code> or a <code>service</code></a>, users are required to include a valid <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-access-token" title="access token" target="_blank"><code>access token</code></a> in the request <code>authorization</code> header, <a href="#proposed-jwt-impl-problems-api-server">as mentioned</a>, so we don't need to do anything.

The next task is to update the <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-request-auth" title="request authentication" target="_blank"><code>request authentication</code></a> process. This update occurs in the <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/auth_middleware.rs" title="src/auth_middleware.rs" target="_blank">src/auth_middleware.rs</a> and the <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/lib.rs" title="src/lib.rs" target="_blank">src/lib.rs</a> modules.

<h3 style="color:teal;text-transform: none;">
  <a id="updated-request-auth-process">The Updated Request Authentication Process</a>
</h3>

The updated request <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-request-auth" title="request authentication" target="_blank"><code>request authentication</code></a> involves changes to both the <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/auth_middleware.rs" title="src/auth_middleware.rs" target="_blank">src/auth_middleware.rs</a> and <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/lib.rs" title="src/lib.rs" target="_blank">src/lib.rs</a> modules.

This section, <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#request-authentication-works" title="How the Request Authentication Process Works" target="_blank">How the Request Authentication Process Works</a>, describes the current process.

<h4 style="color:teal;text-transform: none;">
  <a id="updated-request-auth-process-mw">Code Updated in the src/auth_middleware.rs Module</a>
</h4>

Please recall that the <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/auth_middleware.rs" title="src/auth_middleware.rs" target="_blank">src/auth_middleware.rs</a> module serves as the <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-request-auth-middleware" title="Request authentication middleware" target="_blank"><code>request authentication middleware</code></a>. We will make some substantial updates within this module.

Although the code has sufficient documentation, we will discuss the updates in the following sections.

<a id="updated-request-auth-process-mw-module-doc"></a>
⓵ The module documentation has been updated to describe how the <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-request-auth" title="request authentication" target="_blank"><code>request authentication</code></a> process works with JWT. Please refer to the documentation section <a href="https://github.com/behai-nguyen/rust_web_01/blob/main/src/auth_middleware.rs#L21" title="How This Middleware Works" target="_blank">How This Middleware Works</a> for more details.

<a id="updated-request-auth-process-mw-tokenstatus"></a>
⓶ New <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/auth_middleware.rs#L84" title="src/auth_middleware.rs struct TokenStatus" target="_blank"><code>struct TokenStatus</code></a>:

```rust
struct TokenStatus {
    is_logged_in: bool,
    payload: Option<JWTPayload>,
    api_status: Option<ApiStatus>
}
```

The <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/auth_middleware.rs#L84" title="src/auth_middleware.rs struct TokenStatus" target="_blank"><code>struct TokenStatus</code></a> represents the status of the <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-access-token" title="access token" target="_blank"><code>access token</code></a> for the current request:

<ul>
<li style="margin-top:10px;">
When there is no token, <code>is_logged_in</code> is set to <code>false</code> to indicate that the request comes from an <strong>un</strong><a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-authenticated-session" title="authenticated session" target="_blank"><code>authenticated session</code></a>. The other two fields are set to <code>None</code>, indicating that there is no error.
</li>
<li style="margin-top:10px;">
When there is a token, we call the <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/helper/jwt_utils.rs#L262" title="pub fn decode_token(token: &str, secret_key: &[u8]) -&gt; Result&lt;JWTPayload, ApiStatus&gt;" target="_blank"><code>pub fn decode_token(token: &str, secret_key: &[u8]) -> Result&lt;JWTPayload, ApiStatus></code></a> function:
<ul>
<li style="margin-top:10px;">
If token decoding fails or the token has already expired, <code>is_logged_in</code> is set to <code>false</code>, and <code>api_status</code> is set to the returned <a href="https://github.com/behai-nguyen/rust_web_01/blob/e5fa751f1454bf3ffe3ad72a7c70c6169402bfcb/src/bh_libs/api_status.rs#L18" title="src/bh_libs/api_status.rs ApiStatus" target="_blank"><code>ApiStatus</code></a>. This indicates an error.
</li>
<li style="margin-top:10px;">
If token decoding succeeds, <code>is_logged_in</code> is set to to <code>true</code>, and <code>payload</code> is set to the returned <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/helper/jwt_utils.rs#L25" title="src/helper/app_utils.rs JWTPayload" target="_blank"><code>JWTPayload</code></a>.
</li>
</ul>
</li>
</ul>

<a id="updated-request-auth-process-mw-token-verify-fn"></a>
⓷ The function <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/auth_middleware.rs#L167" title="fn verify_valid_access_token(request: &ServiceRequest) -&gt; TokenStatus" target="_blank"><code>fn verify_valid_access_token(request: &ServiceRequest) -> TokenStatus</code></a> has been completely rewritten, although its purpose remains the same. It checks if the token is present and, if so, decodes it.

The return value of this function is <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/auth_middleware.rs#L84" title="src/auth_middleware.rs struct TokenStatus" target="_blank"><code>struct TokenStatus</code></a>, whose fields are set based on the rules <a href="#updated-request-auth-process-mw-tokenstatus">discussed previously</a>.

<a id="updated-request-auth-process-mw-token-updated-set"></a>
⓸ The new helper function <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/auth_middleware.rs#L206" title="fn update_and_set_updated_token(request: &ServiceRequest, token_status: TokenStatus)" target="_blank"><code>fn update_and_set_updated_token(request: &ServiceRequest, token_status: TokenStatus)</code></a> is called when there is a token and the token is successfully decoded.

It uses the <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/helper/jwt_utils.rs#L25" title="src/helper/app_utils.rs JWTPayload" target="_blank"><code>JWTPayload</code></a> instance in the <code>token_status</code> parameter to create the updated <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-access-token" title="access token" target="_blank"><code>access token</code></a>. Then, it:

<ol>
<li style="margin-top:10px;">
Replaces the current <a href="https://docs.rs/actix-identity/0.7.0/actix_identity/struct.Identity.html" title="actix-identity Identity" target="_blank">actix-identity::Identity</a> login with the new updated token, as <a href="#proposed-jwt-impl-problems-app-server">discussed earlier</a>.
</li>
<a id="updated-request-auth-process-mw-token-updated-set-next-adhoc-mw"></a>
<li style="margin-top:10px;">
Attaches the updated token to <a href="https://docs.rs/actix-web/latest/actix_web/dev/struct.ServiceRequest.html" title="dev::ServiceRequest" target="_blank">dev::ServiceRequest</a>'s <a href="https://docs.rs/actix-web/latest/actix_web/dev/struct.Extensions.html" title="dev::Extensions" target="_blank">dev::Extensions</a> by calling <a href="https://docs.rs/actix-web/latest/actix_web/dev/struct.ServiceRequest.html#method.extensions_mut" title="fn extensions_mut(&self) -&gt; RefMut&lt;'_, Extensions&gt;" target="_blank">fn extensions_mut(&self) -> RefMut&lt;'_, Extensions></a>.
<br/><br/>
The next adhoc middleware, <a href="#updated-request-auth-process-lib">discussed in the next section</a>, consumes this extension.
</li>
</ol>

<a id="updated-request-auth-process-mw-unauth-closure"></a>
⓹ The new closure, <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/auth_middleware.rs#L329" title="let unauthorised_token = |req: ServiceRequest, api_status: ApiStatus| -&gt; Self::Future" target="_blank"> <code>let unauthorised_token = |req: ServiceRequest, api_status: ApiStatus| -> Self::Future</code></a>, calls the <a href="https://docs.rs/actix-web/latest/actix_web/struct.HttpResponse.html#method.Unauthorized" title="the Unauthorized() method" target="_blank">Unauthorized()</a> method on <a href="https://docs.rs/actix-web/latest/actix_web/struct.HttpResponse.html" title="HttpResponse" target="_blank">HttpResponse</a> to return a JSON serialisation of <a href="https://github.com/behai-nguyen/rust_web_01/blob/e5fa751f1454bf3ffe3ad72a7c70c6169402bfcb/src/bh_libs/api_status.rs#L18" title="src/bh_libs/api_status.rs ApiStatus" target="_blank"><code>ApiStatus</code></a>.

Note the calls to remove the <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#notes-on-cookies-our-own" title="server-side per-request cookies" target="_blank">server-side per-request</a> cookies <code>redirect-message</code> and <code>original-content-type</code>.

<a id="updated-request-auth-process-mw-call-method"></a>
⓺ Update the <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/auth_middleware.rs#L329" title="fn call(&self, request: ServiceRequest) -&gt; Self::Future" target="_blank"><code>fn call(&self, request: ServiceRequest) -> Self::Future</code></a> function. All groundwork has been completed. The updates to this method are fairly straightforward:

<ol>
<li style="margin-top:10px;">
Update the call to <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/auth_middleware.rs#L167" title="fn verify_valid_access_token(request: &ServiceRequest) -&gt; TokenStatus" target="_blank"><code>fn verify_valid_access_token(request: &ServiceRequest) -> TokenStatus</code></a>; the return value is now <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/auth_middleware.rs#L84" title="src/auth_middleware.rs struct TokenStatus" target="_blank"><code>struct TokenStatus</code></a>.
</li>
<li style="margin-top:10px;">
If the token is in error, call the closure <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/auth_middleware.rs#L329" title="let unauthorised_token = |req: ServiceRequest, api_status: ApiStatus| -&gt; Self::Future" target="_blank"><code>unauthorised_token()</code></a> to return the error response. The request is then completed.
</li>
<li style="margin-top:10px;">
If the request is from an <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-authenticated-session" title="authenticated session" target="_blank"><code>authenticated session</code></a>, meaning we have a token, and the token has been decoded successfully, we make an additional call to the new helper function <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/auth_middleware.rs#L206" title="fn update_and_set_updated_token(request: &ServiceRequest, token_status: TokenStatus)" target="_blank"><code>fn update_and_set_updated_token(request: &ServiceRequest, token_status: TokenStatus)</code></a>, which has been described in the <a href="#updated-request-auth-process-mw-token-updated-set">previous</a> section.
</li>
</ol>

The core logic of this method remains unchanged.

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;text-transform: none;">
  <a id="updated-request-auth-process-lib">Code Updated in the src/lib.rs Module</a>
</h4>

<a href="#jwt-implementations">As mentioned previously</a>, if a valid token is present, an updated token is generated from the current token's payload every time a request occurs. This updated <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-access-token" title="access token" target="_blank"><code>access token</code></a> <a href="#proposed-jwt-impl">is then sent</a> to the client via both the response header and the response cookie <code>authorization</code>.

<a href="#updated-request-auth-process-mw-token-updated-set-next-adhoc-mw">This section</a> describes how the updated token is attached to the request extension so that the next adhoc middleware can pick it up and send it to the clients.

This is the updated <code>src/lib.rs</code> <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/lib.rs#L156" title="src/lib.rs token forwarding adhoc middleware" target="_blank">next adhoc middleware</a>. Its functionality is straightforward. It queries the current <a href="https://docs.rs/actix-web/latest/actix_web/dev/struct.ServiceRequest.html" title="dev::ServiceRequest" target="_blank">dev::ServiceRequest</a>'s <a href="https://docs.rs/actix-web/latest/actix_web/dev/struct.Extensions.html" title="dev::Extensions" target="_blank">dev::Extensions</a> for a <a href="https://doc.rust-lang.org/std/string/struct.String.html" title="Struct std::string::String" target="_blank">String</a>, which represents the updated token. If found, it sets the <a href="https://docs.rs/actix-web/latest/actix_web/dev/struct.ServiceResponse.html" title="ServiceResponse" target="_blank">ServiceResponse</a> <code>authorization</code> header and cookie with this updated token.

Afterward, it forwards the response. Since it is currently the last middleware in the call stack, the response will be sent directly to the client, completing the request.

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;text-transform: none;">
  <a id="jwt-and-logout">JWT and Logout</a>
</h3>

Due to the issues outlined in <a href="#proposed-jwt-impl-problems-api-server-problems">this section</a> and <a href="#proposed-jwt-impl-problems-app-server-problems">this section</a>, we were unable to effectively implement the logout functionality in the application. This will remain unresolved until we implement the <a href="#proposed-jwt-impl-solutions">proposed solutions</a> and integrate blacklisting.

-- For the time being, we will retain the current logout process unchanged.

Once blacklisting is implemented, the <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-request-auth" title="request authentication" target="_blank"><code>request authentication</code></a> process will need to validate the <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-access-token" title="access token" target="_blank"><code>access token</code></a> against the blacklist table. If the token is found in the blacklist, it will be considered invalid.

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;text-transform: none;">
  <a id="updated-integration-tests">Updating Integration Tests</a>
</h3>

There is a new integration test module as already discussed in section <a href="#token-utility-and-test-test">The Test tests/test_jsonwebtoken.rs Module</a>. There is no new integration test added to existing modules.

Some common test code has been updated as a result of implementing JSON Web Token.

⓵ There are several updates in module <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/tests/common.rs" title="tests/common.rs" target="_blank">tests/common.rs</a>:

<ol>
<li style="margin-top:10px;">
Function <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/tests/common.rs#L43" title="pub fn mock_access_token(&self, secs_valid_for: u64) -&gt; String" target="_blank"> <code>pub fn mock_access_token(&self, secs_valid_for: u64) -> String</code></a> now returns a correctly formatted <a href="#bearer-token">“Bearer” token</a>. Please note the new parameter <code>secs_valid_for</code>.
</li>
<li style="margin-top:10px;">
New function <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/tests/common.rs#L29" title="pub fn jwt_secret_key() -&gt; String" target="_blank"><code>pub fn jwt_secret_key() -> String</code></a> 
</li>
<li style="margin-top:10px;">
New function <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/tests/common.rs#L180" title="pub fn assert_token_email(token: &str, email: &str)" target="_blank"><code>pub fn assert_token_email(token: &str, email: &str)</code></a>. It decodes the parameter <code>token</code>, which is expected to always succeed, then tests that the token <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/helper/jwt_utils.rs#L25" title="src/helper/app_utils.rs JWTPayload" target="_blank"><code>JWTPayload</code></a>'s <code>email</code> value equal to parameter <code>email</code>.
</li>
<li style="margin-top:10px;">
Rewrote <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/tests/common.rs#L188" title="pub fn assert_access_token_in_header(response: &reqwest::Response, email: &str)" target="_blank"><code>pub fn assert_access_token_in_header(response: &reqwest::Response, email: &str)</code></a> and <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/tests/common.rs#L198" title="pub fn assert_access_token_in_cookie(response: &reqwest::Response, email: &str)" target="_blank"><code>pub fn assert_access_token_in_cookie(response: &reqwest::Response, email: &str)</code></a>.
</li>
<li style="margin-top:10px;">
Updated <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/tests/common.rs#L188" title="pub async fn assert_json_successful_login(response: reqwest::Response, email: &str)" target="_blank"><code>pub async fn assert_json_successful_login(response: reqwest::Response, email: &str)</code></a>.
</li>
</ol>

⓶ Some minor changes in both the <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/tests/test_handlers.rs" title="tests/test_handlers.rs" target="_blank">tests/test_handlers.rs</a> and the <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/tests/test_auth_handlers.rs" title="tests/test_auth_handlers.rs" target="_blank">tests/test_auth_handlers.rs</a> modules:

<ol>
<li style="margin-top:10px;">
Call the function <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/tests/common.rs#L43" title="pub fn mock_access_token(&self, secs_valid_for: u64) -&gt; String" target="_blank"><code>pub fn mock_access_token(&self, secs_valid_for: u64) -> String</code></a> with the new parameter <code>secs_valid_for</code>.
</li>
<li style="margin-top:10px;">
Other updates as a result of the updates in the <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/tests/common.rs" title="tests/common.rs" target="_blank">tests/common.rs</a> module.
</li>
</ol>

<h3 style="color:teal;text-transform: none;">
  <a id="concluding-remarks">Concluding Remarks</a>
</h3>

It has been an interesting process for me as I delved into the world of <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> adhoc middleware. While the code may seem simple at first glance, I encountered some problems along the way and <a href="https://users.rust-lang.org/t/actix-web-an-application-wide-adhoc-middleware-to-set-a-response-header-for-all-routes/107207" title="sought assistance" target="_blank">sought assistance</a> to overcome them.

I anticipated the problems, as described in <a href="#proposed-jwt-impl-problems-api-server-problems">this section</a> and <a href="#proposed-jwt-impl-problems-app-server-problems">this section</a>, before diving into the actual coding process. Despite the hurdles, I proceeded with the implementation because I wanted to learn how to set a custom header for all routes before their final response is sent to clients – that's the essence of adhoc middleware.

In a future post, I plan to implement the <a href="#proposed-jwt-impl-solutions">proposed solutions</a> and explore the concept of blacklisting.

I hope you find this post informative and helpful. Thank you for reading. And stay safe, as always.

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

<h3>
🦀 <a href="https://github.com/behai-nguyen/rust_web_01" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>
