---
layout: post
title: "Rust: actix-web global extractor error handlers."

description: Continuing with our actix-web learning application, we implement global extractor error handlers for both application/json and application/x-www-form-urlencoded data. This enhances the robustness of the code. Subsequently, we refactor the login data extraction process to leverage the global extractor error handlers.

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.files.wordpress.com/2024/02/099-01-chrome-json-1.png"
    - "https://behainguyen.files.wordpress.com/2024/02/099-01-chrome-json-2.png"

gallery-image-list-2:
    - "https://behainguyen.files.wordpress.com/2024/02/099-02-chrome-form-1.png"
    - "https://behainguyen.files.wordpress.com/2024/02/099-02-chrome-form-2.png"

gallery-image-list-3:
    - "https://behainguyen.files.wordpress.com/2024/02/099-03-chrome-json-1.png"
    - "https://behainguyen.files.wordpress.com/2024/02/099-03-chrome-json-2.png"

gallery-image-list-4:
    - "https://behainguyen.files.wordpress.com/2024/02/099-04-chrome-form-1.png"
    - "https://behainguyen.files.wordpress.com/2024/02/099-04-chrome-form-2.png"
    - "https://behainguyen.files.wordpress.com/2024/02/099-04-chrome-form-3.png"

gallery-image-list-5:
    - "https://behainguyen.files.wordpress.com/2024/02/099-05-postman-form-1.png"
    - "https://behainguyen.files.wordpress.com/2024/02/099-05-postman-form-2.png"
    - "https://behainguyen.files.wordpress.com/2024/02/099-05-postman-form-3.png"

gallery-image-list-6:
    - "https://behainguyen.files.wordpress.com/2024/02/099-06-chrome-json-1.png"
    - "https://behainguyen.files.wordpress.com/2024/02/099-06-chrome-json-2.png"
    - "https://behainguyen.files.wordpress.com/2024/02/099-06-chrome-json-3.png"

gallery-image-list-7:
    - "https://behainguyen.files.wordpress.com/2024/02/099-07-edge-form-1.png"
    - "https://behainguyen.files.wordpress.com/2024/02/099-07-edge-form-2.png"
    - "https://behainguyen.files.wordpress.com/2024/02/099-07-edge-form-3.png"

gallery-image-list-8:
    - "https://behainguyen.files.wordpress.com/2024/02/099-08-postman-form-1.png"
    - "https://behainguyen.files.wordpress.com/2024/02/099-08-postman-form-2.png"
    - "https://behainguyen.files.wordpress.com/2024/02/099-08-postman-form-3.png"

gallery-image-list-9:
    - "https://behainguyen.files.wordpress.com/2024/02/099-09-opera-ui-login-1.png"
    - "https://behainguyen.files.wordpress.com/2024/02/099-09-opera-ui-login-2.png"

tags:
- Rust
- actix-web
- extractor configuration
- extractor
- configuration
- JsonConfig
- FormConfig
---

<em>Continuing with our <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> learning application, we implement global extractor error handlers for both <code>application/json</code> and <code>application/x-www-form-urlencoded</code> data. This enhances the robustness of the code. Subsequently, we refactor the login data extraction process to leverage the global extractor error handlers.</em>

| ![099-feature-image.jpg](https://behainguyen.files.wordpress.com/2024/02/099-feature-image.jpg) |
|:--:|
| *Rust: actix-web global extractor error handlers.* |

🚀 <strong>Please note,</strong> complete code for this post
can be downloaded from GitHub with:

```
git clone -b v0.9.0 https://github.com/behai-nguyen/rust_web_01.git
```

The
<a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a>
learning application mentioned above has been discussed 
in the following eight previous posts:

<ol>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/10/18/rust-web-application-mysql-server-sqlx-actix-web-and-tera/" title="Rust web application: MySQL server, sqlx, actix-web and tera" target="_blank">Rust web application: MySQL server, sqlx, actix-web and tera</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/11/26/rust-learning-actix-web-middleware-01/" title="Rust: learning actix-web middleware 01" target="_blank">Rust: learning actix-web middleware 01</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/12/31/rust-retrofit-integration-tests-to-an-existing-actix-web-application/" title="Rust: retrofit integration tests to an existing actix-web application." target="_blank">Rust: retrofit integration tests to an existing actix-web application</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/01/03/rust-adding-actix-session-and-actix-identity-to-an-existing-actix-web-application/" title="Rust: adding actix-session and actix-identity to an existing actix-web application." target="_blank">Rust: adding actix-session and actix-identity to an existing actix-web application</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/01/14/rust-actix-web-endpoints-which-accept-both-application-x-www-form-urlencoded-and-application-json-content-types/" title="Rust: actix-web endpoints which accept both application/x-www-form-urlencoded and application/json content types." target="_blank">Rust: actix-web endpoints which accept both <code>application/x-www-form-urlencoded</code> and <code>application/json</code> content types</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/" title="Rust: simple actix-web email-password login and request authentication using middleware." target="_blank">Rust: simple actix-web email-password login and request authentication using middleware</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/02/10/rust-actix-web-get-ssl-https-for-localhost/" title="Rust: actix-web get SSL/HTTPS for localhost." target="_blank">Rust: actix-web get SSL/HTTPS for localhost</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/02/13/rust-actix-web-cors-cookies-and-ajax-calls/" title="Rust: actix-web CORS, Cookies and AJAX calls." target="_blank">Rust: actix-web CORS, Cookies and AJAX calls</a>.</li>
</ol>

The code we're developing in this post is a continuation 
of the code from the 
<a href="https://behainguyen.wordpress.com/2024/02/13/rust-actix-web-cors-cookies-and-ajax-calls/" title="Rust: actix-web CORS, Cookies and AJAX calls." target="_blank">eighth</a>
post above. 🚀 To get the code of this 
<a href="https://behainguyen.wordpress.com/2024/02/13/rust-actix-web-cors-cookies-and-ajax-calls/" title="Rust: actix-web CORS, Cookies and AJAX calls." target="_blank">eighth</a>
post, please use the following command:

```
git clone -b v0.8.0 https://github.com/behai-nguyen/rust_web_01.git
```

<strong>-- Note the tag <code>v0.8.0</code>.</strong>

<a id="project-layout"></a>
❶ We are not adding any new files to the project; it remains the same as in the 
<a href="https://behainguyen.wordpress.com/2024/02/10/rust-actix-web-get-ssl-https-for-localhost/#project-layout" title="Rust: actix-web get SSL/HTTPS for localhost | Project Layout" target="_blank">seventh post</a>.
We are only making changes to some modules.

<a id="project-layout-chart"></a>
```
.
├── Cargo.toml ★
├── README.md ★
├── src
│ ├── auth_handlers.rs ★
│ ├── handlers.rs ★
│ ├── helper
│ │ ├── app_utils.rs ★
│ │ ├── endpoint.rs ★
│ │ └── messages.rs ★
│ ├── helper.rs ★
│ └── lib.rs ★
└── tests
    ├── test_auth_handlers.rs ★
    └── test_handlers.rs ★
```

<strong>-- Please note,</strong> those marked with <span style="font-size:1.5em;">★</span> 
are updated, and those marked with <span style="font-size:1.5em;">☆</span> are new.

<a id="current-extractor-problems"></a>
❷ Currently, the application does not handle extraction errors for both 
<code>application/json</code> and <code>application/x-www-form-urlencoded</code>
data in data-related routes.

🚀 As a reminder, we have the following existing 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#issues-covered-existing-routes" 
title="Existing data related routes" target="_blank">data-related routes</a>. 
Briefly:

<ul>
<li style="margin-top:10px;">
Route <code>https://0.0.0.0:5000/data/employees</code> 
accepts <code>application/json</code>. For example <code>
{"last_name": "%chi", "first_name": "%ak"}</code>.
</li>
<li style="margin-top:10px;">
Route <code>https://0.0.0.0:5000/ui/employees</code> 
accepts <code>application/x-www-form-urlencoded</code>. For 
example <code>last_name=%chi&first_name=%ak</code>.
</li>
</ul>

<a id="refactor-login-custom-extractors"></a>
Unlike the data-related routes, the login route <code>https://0.0.0.0:5000/api/login</code> 
currently implements a custom extractor that also handles extraction errors. Please refer 
to the sections 
<a href="https://behainguyen.wordpress.com/2024/01/14/rust-actix-web-endpoints-which-accept-both-application-x-www-form-urlencoded-and-application-json-content-types/#step-four-login-routes"
title="Implementations of Routes /ui/login and /api/login" target="_blank">Implementations of Routes <code>/ui/login</code> and <code>/api/login</code></a>
and 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#email-password-login-process"
title="How the Email-Password Login Process Works" target="_blank">How the Email-Password Login Process Works</a> 
in previous posts for more details. <em>💥 We will refactor this implementation 
to eliminate the custom extractor and fully leverage the global extractor error 
handlers that we are going to implement.</em>

Let's demonstrate some unhandled extraction errors for both content types.

🚀 Please note that the 
<a href="https://github.com/behai-nguyen/behai-nguyen.github.io/blob/0238b02b77787818fb1e0fc737e38ac522412c2d/tools/ajax_test.html"
title="The HTML page with AJAX call" target="_blank">ajax_test.html</a> 
page is used in the examples below.

<a id="current-extractor-problems-example-1"></a>
⓵ <code>application/json</code> content type. First, we make an invalid 
submission with empty data. Then, we submit data with an invalid field 
name:

{% include image-gallery.html list=page.gallery-image-list-1 %}
<br/>

The above screenshots indicate that there is some implicit default extraction 
error handling in place: the response status code is <code>400</code> for 
<code>BAD REQUEST</code>, and the response text contains the actual extraction 
error message.

<a id="how-extraction-error-handler-should-be"></a>
💥 However, this behavior <strong>is not consistent</strong> with the existing 
implementation for the <code>https://0.0.0.0:5000/api/login</code> route, where 
an extraction error always results in a JSON serialisation of 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/d2bde5020867d89860aa017944b40d70763adb64/src/bh_libs/api_status.rs#L20" 
title="ApiStatus" target="_blank">ApiStatus</a> with a code of <code>400</code> 
for <code>BAD REQUEST</code>, and the message containing the exact extraction error. 
For more details, refer to the current implementation of 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/d2bde5020867d89860aa017944b40d70763adb64/src/helper/endpoint.rs#L25" 
title="pub fn extract_employee_login(body: &Bytes, content_type: &str) -&gt; Result&lt;EmployeeLogin, ApiStatus&gt;" 
target="_blank"><code>pub fn extract_employee_login(body: &Bytes, content_type: &str) -> Result&lt;EmployeeLogin, ApiStatus></code></a>
It's worth noting that, <a href="#refactor-login-custom-extractors">as mentioned earlier</a>, 
we are also refactoring this custom extractor while retaining its current handling 
of extraction errors.

<a id="current-extractor-problems-example-2"></a>
⓶ <code>application/x-www-form-urlencoded</code> content type. 
Similar to the previous example, we also submit two invalid 
requests: one with empty data and another with data containing 
an invalid field name:

{% include image-gallery.html list=page.gallery-image-list-2 %}
<br/>

<a id="global-extractor-error-handlers"></a>
❸ Implementing “global extractor error handlers” for <code>application/json</code> 
and <code>application/x-www-form-urlencoded</code> data.

This involves configuring extractor configurations provided by the 
<a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" 
target="_blank">actix-web</a> crate, namely 
<a href="https://docs.rs/actix-web/latest/actix_web/web/struct.JsonConfig.html"
title="JsonConfig" target="_blank">JsonConfig</a> and 
<a href="https://docs.rs/actix-web/latest/actix_web/web/struct.FormConfig.html"
title="FormConfig" target="_blank">FormConfig</a>, respectively. 
We can define custom error handlers for each content type using their 
<code>error_handler(...)</code> method.

In our context, we refer to these custom error handlers as 
“global extractor error handlers”.

Based on the documentation, we implement the functions 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/e5fa751f1454bf3ffe3ad72a7c70c6169402bfcb/src/lib.rs#L65"
title="fn json_config() -&gt; web::JsonConfig"
target="_blank">fn json_config() -> web::JsonConfig</a>
and 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/e5fa751f1454bf3ffe3ad72a7c70c6169402bfcb/src/lib.rs#L88"
title="fn form_config() -&gt; web::FormConfig"
target="_blank">fn form_config() -> web::FormConfig</a>,
and then 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/e5fa751f1454bf3ffe3ad72a7c70c6169402bfcb/src/lib.rs#L142"
title="Register extractor configurations" target="_blank">register them</a> 
according to the official example.

The key part is the <code>error_handler(...)</code> function within 
both extractor configurations:

```rust
...
        .error_handler(|err, _req| {
            let err_str: String = String::from(err.to_string());
            error::InternalError::from_response(err, 
                make_api_status_response(StatusCode::BAD_REQUEST, &err_str, None)).into()
        })
...
```

Here, <code>err_str</code> represents the actual extraction error message. 

We utilise the function  
<a href="https://github.com/behai-nguyen/rust_web_01/blob/e5fa751f1454bf3ffe3ad72a7c70c6169402bfcb/src/helper/app_utils.rs#L278" 
title="pub fn make_api_status_response(status_code: StatusCode, message: &str, session_id: Option&lt;String&gt;) -&gt; HttpResponse" 
target="_blank"><code>pub fn make_api_status_response( status_code: StatusCode, message: &str, session_id: Option&lt;String>) -> HttpResponse</code></a> 
to construct a response, which is a JSON serialisation of
<a href="https://github.com/behai-nguyen/rust_web_01/blob/d2bde5020867d89860aa017944b40d70763adb64/src/bh_libs/api_status.rs#L20" 
title="ApiStatus" target="_blank">ApiStatus</a>.

We can verify the effectiveness of the global extractor error 
handlers by repeating the previous two examples.

<a id="global-extractor-error-handlers-example-1"></a>
⓵ <code>application/json</code> content type:

{% include image-gallery.html list=page.gallery-image-list-3 %}
<br/>

The screenshots confirm that we receive the expected response, which 
contrasts the <a href="#current-extractor-problems-example-1">example</a> 
prior to refactoring.

<a id="global-extractor-error-handlers-example-2"></a>
⓶ <code>application/x-www-form-urlencoded</code> content type:

{% include image-gallery.html list=page.gallery-image-list-4 %}
<br/>

We get the expected response. This is the 
<a href="#current-extractor-problems-example-2"> example</a> before refactoring.

<a id="global-extractor-error-handlers-example-3"></a>
⓷ Let's try another example via 
<a href="https://www.postman.com/" title="Postman" target="_blank">Postman</a>:

{% include image-gallery.html list=page.gallery-image-list-5 %}
<br/>

When an extraction error occurs, the response is a JSON serialisation of 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/d2bde5020867d89860aa017944b40d70763adb64/src/bh_libs/api_status.rs#L20" 
title="ApiStatus" target="_blank">ApiStatus</a>. When a request to
route <code>https://0.0.0.0:5000/ui/employees</code> is successful, 
the response is HTML. (As a reminder, we need to set
the request <code>authorization</code> header to something, for example,
<code>chirstian.koblick.10004@gmail.com</code>.)

<a id="extractor-error-new-integration-tests"></a>
❹ Integration tests for data-related routes. 

To ensure that the global extractor error handlers function correctly, we need tests to verify their behavior.

In
<a href="https://github.com/behai-nguyen/rust_web_01/blob/e5fa751f1454bf3ffe3ad72a7c70c6169402bfcb/tests/test_handlers.rs"
title="tests/test_handlers.rs" target="_blank">tests/test_handlers.rs</a>, we've
implemented four failed extraction tests, each ending with <code>_error_empty</code> 
and <code>_error_missing_field</code>.

These tests closely resemble the examples shown previously. The code for the 
new tests is similar to existing ones, so we won't walk through it as they 
are self-explanatory.

💥 In the new tests, take note of the error messages: <code>"Content type error"</code>
and <code>"Content type error."</code>!

<a id="refactor-login-data-extractor"></a>
❺ Refactoring the login data extraction process.

In the fifth post, <a href="https://behainguyen.wordpress.com/2024/01/14/rust-actix-web-endpoints-which-accept-both-application-x-www-form-urlencoded-and-application-json-content-types/" title="Rust: actix-web endpoints which accept both application/x-www-form-urlencoded and application/json content types." target="_blank">Rust: actix-web endpoints which accept both <code>application/x-www-form-urlencoded</code> and <code>application/json</code> content types</a>, 
we implemented the custom extractor function 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/6082e2df7f4f073c001f1707ebd418a33a08a6b3/src/helper/endpoint.rs#L19"
title="pub fn extract_employee_login(body: &Bytes, content_type: &str) -&gt; Result&lt;EmployeeLogin, ApiStatus&gt;"
target="_blank"><code>pub fn extract_employee_login(body: &Bytes, content_type: &str) -> Result&lt;EmployeeLogin, ApiStatus></code></a> 
which accepts both <code>application/x-www-form-urlencoded</code> and 
<code>application/json</code> content types, and deserialises the byte 
stream to the 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/d2bde5020867d89860aa017944b40d70763adb64/src/models.rs#L41"
title="src/models.rs Employee struct" target="_blank"><code>EmployeeLogin struct</code></a>.

This function is currently functional. 
<a href="#refactor-login-custom-extractors">As mentioned</a>  previously,
we intend to refactor the code while retaining its extraction error handling behaviors, 
which are now available automatically due to the introduction of 
<a href="#global-extractor-error-handlers">global extractor error handlers</a>.

We are eliminating this helper function and instead using the 
<a href="https://docs.rs/actix-web/latest/actix_web/enum.Either.html" 
title="enum Either" target="_blank">enum Either</a>, which provides a mechanism 
for <a href="https://docs.rs/actix-web/latest/actix_web/enum.Either.html#extractor" 
title="Either combination extractors" target="_blank">trying two extractors</a>: 
a primary and a fallback.

In 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/e5fa751f1454bf3ffe3ad72a7c70c6169402bfcb/src/auth_handlers.rs"
title="src/auth_handlers.rs" target="_blank">src/auth_handlers.rs</a>, the 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/e5fa751f1454bf3ffe3ad72a7c70c6169402bfcb/src/auth_handlers.rs#L274"
title="The login function" target="_blank">login function</a>, the endpoint
handler for route <code>/api/login</code>, is updated as follows:

```rust
#[post("/login")]
pub async fn login(
    request: HttpRequest,
    app_state: web::Data<super::AppState>,
    body: Either<web::Json<EmployeeLogin>, web::Form<EmployeeLogin>>
) -> HttpResponse {
    let submitted_login  = match body {
        Either::Left(json) => json.into_inner(),
        Either::Right(form) => form.into_inner(),
    };
...	
```

The last parameter and the return type have changed. The parameter 
<code>body</code> is now an 
<a href="https://docs.rs/actix-web/latest/actix_web/enum.Either.html" 
title="enum Either" target="_blank">enum Either</a>, which is the focal 
point of this refactoring. The extraction process is more elegant, and 
we are taking advantage of a built-in feature, which should be well-tested.

The <a href="#global-extractor-error-handlers">global extractor error handlers</a>
enforce the same validations on the submitted data as the previous custom extractor 
helper function.

Please note the previous return type of this function:

```rust
#[post("/login")]
pub async fn login(
    request: HttpRequest,
    app_state: web::Data<super::AppState>,
    body: Bytes
) -> Either<impl Responder, HttpResponse> {
...
```

There are other minor changes throughout the function, but they are self-explanatory.

Let's observe the refactored login code in action.

<a id="refactor-login-data-extractor-example-1"></a>
⓵ <code>application/json</code> content type. Two invalid requests and one valid request:

{% include image-gallery.html list=page.gallery-image-list-6 %}
<br/>

<a id="refactor-login-data-extractor-example-2"></a>
⓶ <code>application/x-www-form-urlencoded</code> content type.
Two invalid requests and one valid request:

{% include image-gallery.html list=page.gallery-image-list-7 %}
<br/>

<a id="refactor-login-data-extractor-example-3"></a>
⓷ <code>application/x-www-form-urlencoded</code> content type. 
Using <a href="https://www.postman.com/" title="Postman" target="_blank">Postman</a>.
Two invalid requests and one valid request:

{% include image-gallery.html list=page.gallery-image-list-8 %}
<br/>

<a id="refactor-login-data-extractor-example-4"></a>
⓸ <code>application/x-www-form-urlencoded</code> content type.
Using the application's login page, first log in with an invalid email, 
then log in again with a valid email and password.

{% include image-gallery.html list=page.gallery-image-list-9 %}
<br/>

<a id="refactor-login-data-extractor-integration-tests"></a>
❻ Integration tests for invalid login data.

These tests should have been written earlier, immediately after 
completing the login functionalities.

In the test module, 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/e5fa751f1454bf3ffe3ad72a7c70c6169402bfcb/tests/test_auth_handlers.rs" 
title="tests/test_auth_handlers.rs" 
target="_blank">tests/test_auth_handlers.rs</a>, we've added four failed extraction 
tests, denoted by functions ending with <code>_error_empty</code> and 
<code>_error_missing_field</code>.

❼ We have reached the conclusion of this post. <em>I don't feel that implementing the 
function <code>extract_employee_login</code> was a waste of time. Through this process, 
I've gained valuable insights into Rust.</em>

As for the next post for this project, I'm not yet sure what it will entail 😂... There 
are still several functionalities I would like to implement. I'll let my intuition guide 
me in deciding the topic for the next post.

Thank you for reading, and I hope you find the information in this post useful. Stay safe, 
as always.

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