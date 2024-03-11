---
layout: post
title: "Rust: actix-web CORS, Cookies and AJAX calls."

description: Continuing with our actix-web learning application, we will discuss proper AJAX calls to ensure reliable functionality of CORS and session cookies. This also addresses issue ❷ raised in a previous post. 

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.files.wordpress.com/2024/02/098-01-firefox.png"
    - "https://behainguyen.files.wordpress.com/2024/02/098-01-chrome.png"
    - "https://behainguyen.files.wordpress.com/2024/02/098-01-edge.png"
    - "https://behainguyen.files.wordpress.com/2024/02/098-01-opera.png"

gallery-image-list-2:
    - "https://behainguyen.files.wordpress.com/2024/02/098-02.png"

gallery-image-list-3:
    - "https://behainguyen.files.wordpress.com/2024/02/098-03.png"

gallery-image-list-4:
    - "https://behainguyen.files.wordpress.com/2024/02/098-04.png"

gallery-image-list-5:
    - "https://behainguyen.files.wordpress.com/2024/02/098-05.png"

gallery-image-list-6:
    - "https://behainguyen.files.wordpress.com/2024/02/098-06-opera-1.png"
    - "https://behainguyen.files.wordpress.com/2024/02/098-06-opera-2.png"
    - "https://behainguyen.files.wordpress.com/2024/02/098-06-opera-3.png"

gallery-image-list-7:
    - "https://behainguyen.files.wordpress.com/2024/02/098-07-opera-1.png"
    - "https://behainguyen.files.wordpress.com/2024/02/098-07-opera-2.png"
    - "https://behainguyen.files.wordpress.com/2024/02/098-07-opera-3.png"

gallery-image-list-8:
    - "https://behainguyen.files.wordpress.com/2024/02/098-08-chrome-1.png"
    - "https://behainguyen.files.wordpress.com/2024/02/098-08-chrome-2.png"

tags:
- Rust
- actix-web
- CORS
- Cookies
- AJAX
---

<em>Continuing with our <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> learning application, we will discuss proper AJAX calls to ensure reliable functionality of CORS and session cookies. This also addresses <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#some-current-issues" title="issue ❷ raised" target="_blank">issue ❷ raised</a> in a <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/" title="Rust: simple actix-web email-password login and request authentication using middleware." target="_blank">previous post</a>.</em>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rust_web_01" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![098-feature-image.png](https://behainguyen.files.wordpress.com/2024/02/098-feature-image.png) |
|:--:|
| *Rust: actix-web CORS, Cookies and AJAX calls.* |

🚀 <strong>Please note,</strong> complete code for this post
can be downloaded from GitHub with:

```
git clone -b v0.8.0 https://github.com/behai-nguyen/rust_web_01.git
```

The
<a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a>
learning application mentioned above has been discussed 
in the following seven previous posts:

<ol>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/10/18/rust-web-application-mysql-server-sqlx-actix-web-and-tera/" title="Rust web application: MySQL server, sqlx, actix-web and tera" target="_blank">Rust web application: MySQL server, sqlx, actix-web and tera</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/11/26/rust-learning-actix-web-middleware-01/" title="Rust: learning actix-web middleware 01" target="_blank">Rust: learning actix-web middleware 01</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/12/31/rust-retrofit-integration-tests-to-an-existing-actix-web-application/" title="Rust: retrofit integration tests to an existing actix-web application." target="_blank">Rust: retrofit integration tests to an existing actix-web application</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/01/03/rust-adding-actix-session-and-actix-identity-to-an-existing-actix-web-application/" title="Rust: adding actix-session and actix-identity to an existing actix-web application." target="_blank">Rust: adding actix-session and actix-identity to an existing actix-web application</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/01/14/rust-actix-web-endpoints-which-accept-both-application-x-www-form-urlencoded-and-application-json-content-types/" title="Rust: actix-web endpoints which accept both application/x-www-form-urlencoded and application/json content types." target="_blank">Rust: actix-web endpoints which accept both <code>application/x-www-form-urlencoded</code> and <code>application/json</code> content types</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/" title="Rust: simple actix-web email-password login and request authentication using middleware." target="_blank">Rust: simple actix-web email-password login and request authentication using middleware</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/02/10/rust-actix-web-get-ssl-https-for-localhost/" title="Rust: actix-web get SSL/HTTPS for localhost." target="_blank">Rust: actix-web get SSL/HTTPS for localhost</a>.</li>
</ol>

The code we're developing in this post is a continuation 
of the code from the 
<a href="https://behainguyen.wordpress.com/2024/02/10/rust-actix-web-get-ssl-https-for-localhost/" title="Rust: actix-web get SSL/HTTPS for localhost." target="_blank">seventh</a>
post above. 🚀 To get the code of this 
<a href="https://behainguyen.wordpress.com/2024/02/10/rust-actix-web-get-ssl-https-for-localhost/" title="Rust: actix-web get SSL/HTTPS for localhost." target="_blank">seventh</a>
post, please use the following command:

```
git clone -b v0.7.0 https://github.com/behai-nguyen/rust_web_01.git
```

<strong>-- Note the tag <code>v0.7.0</code>.</strong>

<a id="project-layout"></a>
❶ We are not adding any new files to the project; it remains the same as in the 
<a href="https://behainguyen.wordpress.com/2024/02/10/rust-actix-web-get-ssl-https-for-localhost/#project-layout" title="Rust: actix-web get SSL/HTTPS for localhost | Project Layout" target="_blank">seventh post</a>.
We are only making changes to a few modules.

<a id="project-layout-chart"></a>
```
.
├── ...
├── README.md ★
├── src
│ ├── auth_handlers.rs ★
│ ├── auth_middleware.rs ★
│ └── lib.rs ★
├── ...
```

<strong>-- Please note,</strong> those marked with <span style="font-size:1.5em;">★</span> 
are updated, and those marked with <span style="font-size:1.5em;">☆</span> are new.

<a id="session-cookies"></a>
❷ Session cookies.

I was working on CORS, session cookies, and AJAX calls when I realised 
that we couldn't get session cookies to work consistently across domains 
for <strong>Firefox</strong> and other <strong>Chromium browsers</strong> 
without <code>HTTPS</code>. 
This realisation prompted the focus on enabling the application 
to run under <code>HTTPS</code>, as discussed in the 
seventh post: <a href="https://behainguyen.wordpress.com/2024/02/10/rust-actix-web-get-ssl-https-for-localhost/" title="Rust: actix-web get SSL/HTTPS for localhost." target="_blank">Rust: actix-web get SSL/HTTPS for localhost</a>.

💥 However, despite running the application under <code>HTTPS</code>, 
we later discovered that it still didn't fully resolve the cookie issue. 
This is because <strong>Chromium browsers</strong> are in the process of 
phasing out third-party cookies.

<a id="cors-allowed-origin"></a>
❸ <a href="https://aws.amazon.com/what-is/cross-origin-resource-sharing/" title="What is Cross-Origin Resource Sharing?" target="_blank">Cross-Origin Resource Sharing (CORS)</a> 
<code>allowed origin</code>.

While studying and experimenting with this issue, I made an observation 
regarding the application's allowed origin. The allowed origin 
is set to <code>http://localhost</code>, as per 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/main/.env#L6"
title=".env" target="_blank">configuration</a>. 

During my experiments, I removed the <strong><code>http://</code></strong> scheme, 
leaving only <code>localhost</code> as the allowed origin:

```
ALLOWED_ORIGIN=localhost
```

<a href="https://aws.amazon.com/what-is/cross-origin-resource-sharing/" title="What is Cross-Origin Resource Sharing?" target="_blank">CORS</a> 
just simply reject the requests:

{% include image-gallery.html list=page.gallery-image-list-1 %}

<br/>

● Please refer to the following Mdm Web Docs for explanations regarding  
<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors/CORSMissingAllowOrigin" title="Mdm Web Docs -- Reason: CORS header 'Access-Control-Allow-Origin' missing" target="_blank">CORS header 'Access-Control-Allow-Origin' missing</a>.

● Additionally, I found the Wikipedia article on 
<a href="https://en.wikipedia.org/wiki/Cross-origin_resource_sharing"
title="Cross-origin resource sharing" target="_blank">Cross-origin resource sharing</a> 
to be informative.

As for why I made that change, I can't recall the exact reason. It may have been due to some confusion while reading the documentation and examining examples from other sources.

According to the same-origin policy, 
an <code>origin</code> is defined by its <code>scheme</code>, 
<code>host</code>, and <code>port</code>. 
You can find detailed rules for origin determination in the Wikipedia article 
<a href="https://en.wikipedia.org/wiki/Same-origin_policy#Origin_determination_rules"
title="Same-origin policy | Origin determination rules" target="_blank">on the Same-origin policy</a>.

> Two resources are considered to be of the same origin if and only if all these values are exactly the same.
> 
> https://en.wikipedia.org/wiki/Same-origin_policy#Origin_determination_rules

This would likely explain why dropping the scheme resulted in all requests being rejected

<a id="cookies-ajax"></a>
❹ Cookies and AJAX calls.

In the 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/" title="Rust: simple actix-web email-password login and request authentication using middleware." target="_blank">sixth</a> 
post, we 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#some-current-issues" 
title="Issue ❷" target="_blank">raised issue ❷</a>. I further noted in that section:

> It seems logical, but it does not work when we log in using JSON with either an invalid email or password. The client tools simply report that the request could not be completed. I haven’t been able to work out why yet. 

By <code>“...log in using JSON...”</code> I mean AJAX calls. 
I do apologise for not being clear earlier.

-- Recall that in this scenario, the application acts as an 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-api-server"
title="API-like server or a service" target="_blank"><code>API-like server</code> or a <code>service</code></a>.

After some study and experimentation, I have been able to determine the reasons:

<ol>
<li style="margin-top:10px;">
AJAX requests must have both <code>xhrFields.withCredentials</code> 
and <code>crossDomain</code> set to <code>true</code>.
</li>
<li style="margin-top:10px;">
How session cookies are created. We will discuss these in detail in the following sections.
</li>
</ol>

<a id="cookies-ajax-cross-domain-calls"></a>
⓵ AJAX and cross domain. 

I use the HTML page 
<a href="https://github.com/behai-nguyen/behai-nguyen.github.io/blob/eb91f9129dcaefffe9cd541449b98ff8b73803de/tools/ajax_test.html"
title="The HTML page with AJAX call" target="_blank">ajax_test.html</a> 
to test the application with AJAX calls. In the 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/" title="Rust: simple actix-web email-password login and request authentication using middleware." target="_blank">sixth</a> 
post, I used the function 
<a href="https://github.com/behai-nguyen/js/blob/f2a9163e53fcb500850f2a6d2c1417a049163eb4/ajax_funcs.js#L10"
title="function runAjaxEx(...)" target="_blank">runAjaxEx(...)</a>, 
which caused session cookies not to work properly when calls were cross-domain.
Now, I am using the function 
<a href="https://github.com/behai-nguyen/js/blob/f2a9163e53fcb500850f2a6d2c1417a049163eb4/ajax_funcs.js#L88"
title="runAjaxCrossDomain(...)" target="_blank">runAjaxCrossDomain(...)</a>:

```javascript
...
            // https://stackoverflow.com/questions/76956593/how-to-persist-data-across-routes-using-actix-session-and-redisactorsessionstore
            xhrFields: {
                withCredentials: true
            },
            crossDomain: true,
...
```

Refer to the following Mdm Web Docs page on 
<a href="https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/withCredentials" 
title="Mdm Web Docs -- XMLHttpRequest: withCredentials property" target="_blank">
XMLHttpRequest: withCredentials property</a>
for explanations of <code>xhrFields.withCredentials</code>.

💥 Please note that I am still unclear why this is considered a 
cross-domain case. I am accessing 
<a href="https://github.com/behai-nguyen/behai-nguyen.github.io/blob/eb91f9129dcaefffe9cd541449b98ff8b73803de/tools/ajax_test.html"
title="The HTML page with AJAX call" target="_blank">ajax_test.html</a> 
via localhost, while the application is hosted at 
<code>localhost:5000</code>. In the correct response screenshot below, 
without the cross-domain setting, the response would be the login HTML page without the 
<code>Please check login detail.</code> message because cookies are simply rejected:

{% include image-gallery.html list=page.gallery-image-list-2 %}

<br/>

We have successfully refactored the 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/d2bde5020867d89860aa017944b40d70763adb64/src/auth_handlers.rs#L62"
title="Login error, no match on employee email"
target="_blank">fn first_stage_login_error_response(request: &HttpRequest, message: &str) -> HttpResponse</a> 
function, as discussed in the aforementioned 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#some-current-issues" 
title="Issue ❷" target="_blank">issue ❷</a>. 
Additionally, we've included a call to create the 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#notes-on-cookies-our-own"
title="The server-side per-request cookies" target="_blank">server-side per-request</a>
<code>original-content-type</code> cookie:

```rust
...
        .cookie(build_original_content_type_cookie(&request, request.content_type()))
...
```

<a id="cookies-ajax-cookies-management"></a>
⓶ How session cookies are created. 

<a href="#session-cookies">As mentioned</a> earlier, without <code>HTTPS</code>, 
cookies do not function properly; they are rejected by <strong>Chromium browsers</strong> 
and <strong>Firefox</strong>.

In this post, the cookie implementations are as follows:

<ol>
<li style="margin-top:10px;">
<code>Scheme</code>: <code>HTTPS://</code>
</li>
<li style="margin-top:10px;">
<code>Secure</code>: <code>true</code>
</li>
<li style="margin-top:10px;">
<code>SameSite</code>: <code>None</code>
</li>
</ol>

Let's examine some examples where cookies are rejected.

<a id="cookies-ajax-cookies-mgnt-example-1"></a>
１. 
<code>Scheme</code>: <code>HTTP://</code>, <code>Secure</code>: <code>false</code>, 
and <code>SameSite</code>: <code>Strict</code>.

When accessing 
<a href="https://github.com/behai-nguyen/behai-nguyen.github.io/blob/eb91f9129dcaefffe9cd541449b98ff8b73803de/tools/ajax_test.html" 
title="The HTML page with AJAX call" target="_blank">ajax_test.html</a> 
on <code>localhost</code>, and the application is hosted on the Ubuntu 22.10 machine at 
<code>192.168.0.16:5000</code>, the 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#notes-on-cookies-our-own"
title="The server-side per-request cookies" target="_blank">server-side per-request</a>
cookies are rejected:

{% include image-gallery.html list=page.gallery-image-list-3 %}

<br/>

The expected output is:

```javascript
{
	"code": 401,
	"message": "Please check login detail.",
	"session_id": null
}
```

The warnings in the above screenshot are:

```
Some cookies are misusing the recommended “SameSite“ attribute

Cookie “original-content-type” has been rejected because it is in a cross-site context and its “SameSite” is “Lax” or “Strict”.

Cookie “redirect-message” has been rejected because it is in a cross-site context and its “SameSite” is “Lax” or “Strict”.

Cookie “redirect-message” has been rejected because it is in a cross-site context and its “SameSite” is “Lax” or “Strict”.

Cookie “original-content-type” has been rejected because it is in a cross-site context and its “SameSite” is “Lax” or “Strict”.

Cookie “redirect-message” has been rejected because it is in a cross-site context and its “SameSite” is “Lax” or “Strict”.

Cookie “original-content-type” has been rejected because it is in a cross-site context and its “SameSite” is “Lax” or “Strict”.
```

The warnings indicate that both <code>Lax</code> and <code>Strict</code>
would result in these cookies being rejected. The only remaining option left 
is <code>None</code>.
For more information, 
please refer to the following Mdm Web Docs article on 
<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#samesitesamesite-value" title="Mdm Web Docs Set-Cookie SameSite" target="_blank">Set-Cookie SameSite</a>.

<a id="cookies-ajax-cookies-mgnt-example-2"></a>
２. 
<code>Scheme</code>: <code>HTTP://</code>, <code>Secure</code>: <code>false</code>, 
and <code>SameSite</code>: <code>None</code>.

The cookies are accepted, but there are still warnings regarding the 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#notes-on-cookies-our-own"
title="The server-side per-request cookies" target="_blank">server-side per-request</a> 
cookies:

{% include image-gallery.html list=page.gallery-image-list-4 %}

<br/>

The warnings are:

```
Some cookies are misusing the recommended “SameSite“ attribute

Cookie “original-content-type” will be soon rejected because it has the “SameSite” attribute set to “None” without the “secure” attribute. To know more about the “SameSite“ attribute, read https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie/SameSite

Cookie “redirect-message” will be soon rejected because it has the “SameSite” attribute set to “None” without the “secure” attribute. To know more about the “SameSite“ attribute, read https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie/SameSite

Cookie “redirect-message” will be soon rejected because it has the “SameSite” attribute set to “None” without the “secure” attribute. To know more about the “SameSite“ attribute, read https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie/SameSite

Cookie “original-content-type” will be soon rejected because it has the “SameSite” attribute set to “None” without the “secure” attribute. To know more about the “SameSite“ attribute, read https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie/SameSite

Cookie “redirect-message” will be soon rejected because it has the “SameSite” attribute set to “None” without the “secure” attribute. To know more about the “SameSite“ attribute, read https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie/SameSite login

Cookie “original-content-type” will be soon rejected because it has the “SameSite” attribute set to “None” without the “secure” attribute. To know more about the “SameSite“ attribute, read https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie/SameSite
```

The application also maintains an application-wide publicly available cookie named 
<code>authorization</code> cookie, discussed 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#notes-on-cookies-our-own"
title="The authorization cookie" target="_blank"> 
toward the end of this section</a>. This cookie stores the 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-access-token"
title="The access token" target="_blank"><code>access token</code></a>
after a successful login. Based on the warnings above, 
we would expect to receive the same warning for this cookie. And indeed, we do: 

{% include image-gallery.html list=page.gallery-image-list-5 %}

<br/>

Generally, this is not a problem, as this 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-access-token"
title="The access token" target="_blank"><code>access token</code></a> 
is also included in the response's 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#the-login-process-api-login-step-four-authorization-header" 
title="The authorization header" target="_blank"><code>authorization</code></a> header, 
clients can get it from this header instead.

<a id="cookies-ajax-cookies-mgnt-example-3"></a>
３.
<code>Scheme</code>: <code>HTTP://</code>, <code>Secure</code>: <code>false</code>, 
and <code>SameSite</code>: <code>None</code> -- as per in ２.

<strong>Chromium browsers</strong>, including <strong>Opera</strong>, 
appear to reject cookies even when not accessed cross-domain. 
For instance, when logging in with an invalid email, the login page 
is displayed without the <code>Please check login detail.</code> message.

{% include image-gallery.html list=page.gallery-image-list-6 %}

<br/>

Now that the application can run under <code>HTTPS://</code>, let's set 
<code>Secure</code> to <code>true</code> and <code>SameSite</code> to 
<code>None</code> and observe how browsers handle cookies.

<a id="cookies-ajax-https"></a>
❺ <code>Scheme</code>: <code>HTTPS://</code>, <code>Secure</code>: 
<code>true</code>, and <code>SameSite</code>: <code>None</code>.
We need to make two changes to the cookie creation code.

First, for 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#notes-on-cookies-our-own"
title="The server-side per-request cookies" target="_blank">server-side per-request</a> cookies, 
we've already made changes since the 
<a href="https://behainguyen.wordpress.com/2024/02/10/rust-actix-web-get-ssl-https-for-localhost/" title="Rust: actix-web get SSL/HTTPS for localhost." target="_blank">seventh</a> 
post. Please refer to 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/1738173addc7c4db0832ed7678358e0bae2a2a2d/src/helper/app_utils.rs#L18"
title="src/helper/app_utils.rs" target="_blank">src/helper/app_utils.rs</a>:

```rust
...
pub fn build_cookie<'a>(
    _request: &'a HttpRequest,
    name: &'a str,
    value: &'a str,
    server_only: bool,
    removal: bool
) -> Cookie<'a> {
    ...

    let mut cookie = Cookie::build(name, value)
        // .domain(String::from(parts.collect::<Vec<&str>>()[0]))
        .path("/")
        .secure(true)
        .http_only(server_only)
        .same_site(SameSite::None)
        .finish();
...
```

I've also removed the <code>domain</code> setting, as it doesn't seem 
to make any difference; we just let it use the default value.

These changes will also apply to the 
<code>authorization</code> cookie, discussed 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#notes-on-cookies-our-own"
title="The authorization cookie" target="_blank">toward the end of this section</a>.

Secondly, for the third-party
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#notes-on-cookies-third-party"
title="The third-party id cookie" target="_blank"><strong>secured cookie</strong> 
<code>id</code></a>, we update the 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/d2bde5020867d89860aa017944b40d70763adb64/src/lib.rs#L96" title="src/lib.rs" target="_blank">src/lib.rs</a> 
module as follows:

```rust
...
            .wrap(SessionMiddleware::builder(
                    redis_store.clone(),
                    secret_key.clone()
                )
                .cookie_secure(true)
                .cookie_same_site(SameSite::None)
                .build(),
            )
...
```

To recap, all cookies now have <code>Secure</code> set to <code>true</code>, 
and <code>SameSite</code> set to <code>None</code>. 💥 <span style="color:red;">
<em>While this currently satisfies <strong>Chromium browsers</strong>, it comes 
with a new warning. There's no assurance that these cookies will continue to be 
accepted in the future, </em></span> as illustrated by the 
<a href="#cookies-ajax-https-example-3">Chrome example</a> below.

<a id="cookies-ajax-https-example-1"></a>
⓵ <strong>Firefox</strong> does not show any cookie warnings, we 
will not show any screenshots.

<a id="cookies-ajax-https-example-2"></a>
⓶ <strong>Opera</strong> accepts the 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#notes-on-cookies-our-own"
title="The server-side per-request cookies" target="_blank">server-side per-request</a> cookies.
Log in using an invalid email, we get the expected response:

{% include image-gallery.html list=page.gallery-image-list-7 %}

<br/>

<a id="cookies-ajax-https-example-3"></a>
⓷ <strong>Chrome</strong> also accepts the cookies, but shows a new warning:

{% include image-gallery.html list=page.gallery-image-list-8 %}

<br/>

The warning is:

```
Setting cookie in cross-site context will be blocked in future Chrome versions

Cookies with the SameSite=None; Secure and not Partitioned attributes that operate in cross-site contexts are third-party cookies. In future Chrome versions, setting third-party cookies will be blocked. This behavior protects user data from cross-site tracking.

Please refer to the article linked to learn more about preparing your site to avoid potential breakage.
```

We will briefly discuss this warning in the next section.

<a id="chromium-cookies-partitioned-warning"></a>
❻ <strong>Chromium</strong> is in the process of phasing out 
of third-party cookies! 

The <code>article linked</code> Chrome mentions in the warning is:

🚀 <a href="https://developers.google.com/privacy-sandbox/3pcd#report-issues" 
title="Prepare for third-party cookie restrictions" 
target="_blank">Prepare for third-party cookie restrictions</a>

I have not read everything yet, but it does look very comprehensive, 
listing a lot of alternatives to third-party cookies.

I can't remember how, but I came across this Mdm Web Docs article titled 
<a href="https://developer.mozilla.org/en-US/docs/Web/Privacy/Partitioned_cookies" 
title="Cookies Having Independent Partitioned State (CHIPS)" 
target="_blank">Cookies Having Independent Partitioned State (CHIPS)</a>  
before encountering the <strong>Chrome</strong> article mentioned above. 
It explains <code>Partitioned cookie</code>. Subsequently, I reached out 
to the authors of the relevant crates to inquire about this topic:

<ul>
<li style="margin-top:10px;">
<a href="https://github.com/actix/actix-web/discussions/3284"
title="Does actix-web support cookie &quot;Partitioned&quot; yet, please? #3284"
target="_blank">Does actix-web support cookie &quot;Partitioned&quot; yet, please? #3284</a>
</li>
<li style="margin-top:10px;">
<a href="https://github.com/SergioBenitez/cookie-rs/issues/224"
title="Does cookie-rs support cookie &quot;Partitioned&quot; yet, please? #224"
target="_blank">Does cookie-rs support cookie &quot;Partitioned&quot; yet, please? #224</a>
</li>
</ul>

It appears that they are going to support this <code>Partitioned cookie</code>.
We'll just have to wait and see how it pans out.

I haven't delved into cookies for a while, and there have been changes. I feel 
up-to-date with cookies now! 😂 It has been an interesting issue to study. I 
hope you find the information in this post useful. Thank you for reading. 
And stay safe, as always.
 
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
