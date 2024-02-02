---
layout: post
title: "Rust: actix-web endpoints which accept both application/x-www-form-urlencoded and application/json content types."

description: We're implementing a login process for our actix-web learning application. We undertake some general updates to get ready to support login. We then implement a new /api/login route, which supports both application/x-www-form-urlencoded and application/json content types. In this post, we only implement deserialising the submitted request data, then echo some response. We also add a login page via route /ui/login.

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.files.wordpress.com/2024/01/095-02.png"
    - "https://behainguyen.files.wordpress.com/2024/01/095-03.png"

gallery-image-list-2:
    - "https://behainguyen.files.wordpress.com/2024/01/095-04.png"
    - "https://behainguyen.files.wordpress.com/2024/01/095-05.png"

gallery-image-list-3:
    - "https://behainguyen.files.wordpress.com/2024/01/095-06.png"
    - "https://behainguyen.files.wordpress.com/2024/01/095-07.png"

tags:
- Rust
- actix-web
- application/x-www-form-urlencoded
- application/json
- content type
---

<em>We're implementing a login process for our <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> learning application. We undertake some general updates to get ready to support login. We then implement a new <code>/api/login</code> route, which supports both <code>application/x-www-form-urlencoded</code> and <code>application/json</code> content types. In this post, we only implement deserialising the submitted request data, then echo some response. We also add a login page via route <code>/ui/login</code>.</em>

| ![095-feature-image.png](https://behainguyen.files.wordpress.com/2024/01/095-feature-image.png) |
|:--:|
| *Rust: actix-web endpoints which accept both <code>application/x-www-form-urlencoded</code> and <code>application/json</code> content types.* |

🚀 <strong>Please note,</strong> complete code for this post can be downloaded from GitHub with:

```
git clone -b v0.5.0 https://github.com/behai-nguyen/rust_web_01.git
```

The <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> learning application mentioned above has been discussed in the following four (4) previous posts:

<ol>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/10/18/rust-web-application-mysql-server-sqlx-actix-web-and-tera/" title="Rust web application: MySQL server, sqlx, actix-web and tera" target="_blank">Rust web application: MySQL server, sqlx, actix-web and tera</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/11/26/rust-learning-actix-web-middleware-01/" title="Rust: learning actix-web middleware 01" target="_blank">Rust: learning actix-web middleware 01</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/12/31/rust-retrofit-integration-tests-to-an-existing-actix-web-application/" title="Rust: retrofit integration tests to an existing actix-web application." target="_blank">Rust: retrofit integration tests to an existing actix-web application</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/01/03/rust-adding-actix-session-and-actix-identity-to-an-existing-actix-web-application/" title="Rust: adding actix-session and actix-identity to an existing actix-web application." target="_blank">Rust: adding actix-session and actix-identity to an existing actix-web application</a>.</li>
</ol>

The code we're developing in this post is a continuation of the code from the <a href="https://behainguyen.wordpress.com/2024/01/03/rust-adding-actix-session-and-actix-identity-to-an-existing-actix-web-application/" title="Rust: adding actix-session and actix-identity to an existing actix-web application." target="_blank">fourth</a> post above. 🚀 To get the code of this <a href="https://behainguyen.wordpress.com/2024/01/03/rust-adding-actix-session-and-actix-identity-to-an-existing-actix-web-application/" title="Rust: adding actix-session and actix-identity to an existing actix-web application." target="_blank">fourth</a> post, please use the following command:

```
git clone -b v0.4.0 https://github.com/behai-nguyen/rust_web_01.git
```

<strong>-- Note the tag <code>v0.4.0</code>.</strong>

<em>As already mentioned in the introduction above, in this post, our main focus of the login process is deserialising both <code>application/x-www-form-urlencoded</code> and <code>application/json</code> into a <code>struct</code> ready to support login. I struggle with this issue a little, I document it as part of my Rust learning journey.</em>

<a id="new-directory-layout"></a>
This post introduces a few new modules, some MySQL migration scripts, and a new login HTML page. The updated directory layout for the project is in the screenshot below:

![095-01.png](https://behainguyen.files.wordpress.com/2024/01/095-01.png)

<h2>Table of contents</h2>

<ul>
<li style="margin-top:10px;"><a href="#step-one-update-rust">❶ Update Rust to use latest actix-cors</a></li>
<li style="margin-top:10px;"><a href="#step-two-update-employees-table">❷ Add new fields <code>email</code> and <code>password</code> to the <code>employees</code> table</a></li>
<li style="margin-top:10px;"><a href="#step-three-update-models">❸ Update <code>src/models.rs</code></a></li>
<li style="margin-top:10px;"><a href="#step-four-login-routes">❹ New module <code>src/auth_handlers.rs</code> which implements routes <code>/ui/login</code> and <code>/api/login</code></a></li>
<li style="margin-top:10px;"><a href="#step-five-update-lib">❺ Update <code>src/lib.rs</code></a></li>
<li style="margin-top:10px;"><a href="#step-six-new-login-page">❻ The new <code>templates/auth/login.html</code></a></li>
<li style="margin-top:10px;"><a href="#step-seven-some-testing">❼ Testing</a>
<ul>
<li style="margin-top:10px;"><a href="#step-seven-some-testing-notes-on-cargo-test">⓵ <code>cargo test</code></a></li>
<li style="margin-top:10px;"><a href="#step-seven-some-testing-manual-tests">⓶ Manual tests</a></li>
</ul>
</li>
</ul>

<a id="step-one-update-rust"></a>
❶ Update Rust to the latest version. At the time of this post, the latest version is <code>1.75.0</code>. The command to update:

```
▶️<code>Windows 10:</code> rustup update
▶️<code>Ubuntu 22.10:</code> $ rustup update
```

We've taken <a href="https://aws.amazon.com/what-is/cross-origin-resource-sharing/" title="CORS" target="_blank">CORS</a> into account when we started out this project in this <a href="https://behainguyen.wordpress.com/2023/10/18/rust-web-application-mysql-server-sqlx-actix-web-and-tera/" title="Rust web application: MySQL server, sqlx, actix-web and tera" target="_blank">first</a> post. 

I'm not quite certain what'd happened, but all of a sudden, it just rejects requests with message <code><span style="font-weight:bold;color:red;">Origin is not allowed to make this request</span></code>.

-- Browsers have been updated, perhaps?

Failing to troubleshoot the problem, and seeing that <a href="https://docs.rs/actix-cors/latest/actix_cors/index.html" title="actix-cors" target="_blank">actix-cors</a> is at version <code>0.7.0</code>. I update it. 

-- It does not work with Rust version <code>1.74.0</code>. This new version of <a href="https://docs.rs/actix-cors/latest/actix_cors/index.html" title="actix-cors" target="_blank">actix-cors</a> seems to fix the above request rejection issue.

<a id="step-two-update-employees-table"></a>
❷ Update the <code>employees</code> table, adding new fields <code>email</code> and <code>password</code>.

Using the migration tool <a href="https://github.com/launchbadge/sqlx/tree/main/sqlx-cli" title="SQLx CLI" target="_blank">SQLx CLI</a>, which we've covered in <a href="https://behainguyen.wordpress.com/2023/10/10/rust-sqlx-cli-database-migration-with-mysql-and-postgresql/" title="Rust SQLx CLI: database migration with MySQL and PostgreSQL." target="_blank">Rust SQLx CLI: database migration with MySQL and PostgreSQL</a>, to update the <code>employees</code> table.

While inside the new directory <code>migrations/mysql/</code>, see <a href="#new-directory-layout">project directory layout</a> above, create empty migration files <code>99999999999999_emp_email_pwd.up.sql</code> and <code>99999999999999_emp_email_pwd.down.sql</code> using the command:

```
▶️<code>Windows 10:</code> sqlx migrate add -r emp_email_pwd
▶️<code>Ubuntu 22.10:</code> $ sqlx migrate add -r emp_email_pwd
```

Populate the two script files with what we would like to do. Please see their contents <a href="https://github.com/behai-nguyen/rust_web_01/tree/6082e2df7f4f073c001f1707ebd418a33a08a6b3main/migrations/mysql/migrations" title="on GitHub" target="_blank">on GitHub</a>. To apply, run the below command, it'll take a little while to complete:

```
▶️<code>Windows 10:</code> sqlx migrate add -r emp_email_pwd
▶️<code>Ubuntu 22.10:</code> $ sqlx migrate add -r emp_email_pwd
```

<a id="step-three-update-models"></a>
❸ Update <a href="https://github.com/behai-nguyen/rust_web_01/blob/6082e2df7f4f073c001f1707ebd418a33a08a6b3/src/models.rs" title="updated src/models.rs" target="_blank"><code>src/models.rs</code></a> to manage new fields <code>employees.email</code> and <code>employees.password</code>.

If we run <code>cargo test</code> now, all integration tests should fail. All integration tests eventually call to <code>get_employees(...)</code>, which does a <code>select * from employees...</code>. Since the two new fields've been added to a specific order, field indexes in <code>get_employees(...)</code> are out of order.

Module <a href="https://github.com/behai-nguyen/rust_web_01/blob/6082e2df7f4f073c001f1707ebd418a33a08a6b3/src/models.rs" title="updated src/models.rs" target="_blank"><code>src/models.rs</code></a> gets the following updates:

<ol>
<li style="margin-top:10px;"><code>pub email: String</code> field added to <code>struct Employee</code>.</li>
<li style="margin-top:10px;"><code>pub async fn get_employees(...)</code> updated to read <code>Employee.email</code> field. Other fields' indexes also get updated.</li>
<li style="margin-top:10px;">New <code>pub struct EmployeeLogin</code>.</li>
<li style="margin-top:10px;">New <code>pub async fn select_employee(...)</code>, which optionally selects an employee base on exact email match.</li>
<li style="margin-top:10px;">New <code>pub struct LoginSuccess</code>.</li>
<li style="margin-top:10px;">Add <code>"email": "siamak.bernardeschi.67115@gmail.com"</code> to existing tests.</li>
</ol>

Please see the <a href="https://github.com/behai-nguyen/rust_web_01/blob/6082e2df7f4f073c001f1707ebd418a33a08a6b3/src/models.rs" title="updated src/models.rs" target="_blank">updated <code>src/models.rs</code></a> on GitHub. The documentation should be sufficient to help reading the code.

<a id="step-four-login-routes"></a>
❹ New module <a href="https://github.com/behai-nguyen/rust_web_01/blob/6082e2df7f4f073c001f1707ebd418a33a08a6b3/src/auth_handlers.rs" title="src/auth_handlers.rs" target="_blank"><code>src/auth_handlers.rs</code></a>, where new login routes <code>/ui/login</code> and <code>/api/login</code> are implemented.

● <code>http://0.0.0.0:5000/ui/login</code> is a <code>GET</code> route, which just returns the <code>login.html</code> page as HTML.

● <code>http://0.0.0.0:5000/api/login</code> is a <code>POST</code> route. This is effectively the application login handler.

💥 This <code>http://0.0.0.0:5000/api/login</code> route is the main focus of this post:

-- Its handler method accepts both <code>application/x-www-form-urlencoded</code> and <code>application/json</code> content types, and deserialises the byte stream to <code>struct EmployeeLogin</code> <a href="#step-three-update-models">mentioned above</a>.

💥 <strong><em>Please also note that, as already mentioned, in this post, the login process does not do login, if successfully deserialised the submitted data, it'd just echo a confirmation response in the format of the request content type. If failed to deserialise, it'd send back a JSON response which has an error code and a text message. </em></strong>

Examples of valid submitted data for each content type:

✔️ Content type: <code>application/x-www-form-urlencoded</code>; data: <code>email=chirstian.koblick.10004@gmail.com&password=password</code>.

✔️ Content type: <code>application/json</code>; data: <code>{"email": "chirstian.koblick.10004@gmail.com", "password": "password"}</code>.

<div style="background-color:rgb(209, 209, 209);padding:10px;">
Content of <a href="https://github.com/behai-nguyen/rust_web_01/blob/6082e2df7f4f073c001f1707ebd418a33a08a6b3/src/auth_handlers.rs" 
title="src/auth_handlers.rs" target="_blank">src/auth_handlers.rs</a>
</div>

```rust
#[post("/login")]
pub async fn login(
    request: HttpRequest,
    body: Bytes
) -> HttpResponse {
...
    // Attempts to extract -- deserialising -- request body into EmployeeLogin.
    let api_status = extract_employee_login(&body, request.content_type());
    // Failed to deserialise request body. Returns the error as is.
    if api_status.is_err() {
        return HttpResponse::Ok()
            .content_type(ContentType::json())
            .body(serde_json::to_string(&api_status.err().unwrap()).unwrap());
    }

    // Succeeded to deserialise request body.
    let emp_login: EmployeeLogin = api_status.unwrap();
...	
```

Note the second parameter <code>body</code>, which is <a href="https://docs.rs/actix-web/4.4.1/actix_web/web/struct.Bytes.html" title="actix_web::web::Bytes" target="_blank">actix_web::web::Bytes</a>, this is the byte stream presentation of the request body. 

As an extractor, <a href="https://docs.rs/actix-web/4.4.1/actix_web/web/struct.Bytes.html" title="actix_web::web::Bytes" target="_blank">actix_web::web::Bytes</a> has been mentioned in section <a href="https://actix.rs/docs/extractors#other" title="Other" target="_blank">Type-safe information extraction | Other</a>. We're providing our own implementation to do the deserialisation, method <code>extract_employee_login(...)</code> in new module <a href="https://github.com/behai-nguyen/rust_web_01/blob/6082e2df7f4f073c001f1707ebd418a33a08a6b3/src/helper/endpoint.rs" title="src/helper/endpoint.rs" target="_blank"><code>src/helper/endpoint.rs</code></a>.

<div style="background-color:rgb(209, 209, 209);padding:10px;">
Content of <a href="https://github.com/behai-nguyen/rust_web_01/blob/6082e2df7f4f073c001f1707ebd418a33a08a6b3/src/helper/endpoint.rs" 
title="src/helper/endpoint.rs" target="_blank">src/helper/endpoint.rs</a>
</div>

```rust
pub fn extract_employee_login(
    body: &Bytes, 
    content_type: &str
) -> Result<EmployeeLogin, ApiStatus> {
...
    extractors.push(Extractor { 
        content_type: mime::APPLICATION_WWW_FORM_URLENCODED.to_string(), 
        handler: |body: &Bytes| -> Result<EmployeeLogin, ApiStatus> {
            match from_bytes::<EmployeeLogin>(&body.to_owned().to_vec()) {
                Ok(e) => Ok(e),
                Err(e) => Err(ApiStatus::new(err_code_500()).set_text(&e.to_string()))
            }
        }
    });
...
    extractors.push(Extractor {
        content_type: mime::APPLICATION_JSON.to_string(),
        handler: |body: &Bytes| -> Result<EmployeeLogin, ApiStatus> {
            // From https://stackoverflow.com/a/67340858
            match serde_json::from_slice(&body.to_owned()) {
                Ok(e) => Ok(e),
                Err(e) => Err(ApiStatus::new(err_code_500()).set_text(&e.to_string()))
            }
        }
    });
```

For <code>application/x-www-form-urlencoded</code> content type, we call method <a href="https://docs.rs/serde_html_form/0.2.3/serde_html_form/fn.from_bytes.html" title="serde_html_form::from_bytes(...)" target="_blank">serde_html_form::from_bytes(...)</a> from (new) crate <a href="https://docs.rs/serde_html_form/0.2.3/serde_html_form/" title="serde_html_form" target="_blank">serde_html_form</a> to deserialise the byte stream to <code>EmployeeLogin</code>.

-- <a href="https://github.com/behai-nguyen/rust_web_01/blob/6082e2df7f4f073c001f1707ebd418a33a08a6b3/Cargo.toml" title="Cargo.toml" target="_blank"><code>Cargo.toml</code></a> has been updated to include crate <a href="https://docs.rs/serde_html_form/0.2.3/serde_html_form/" title="serde_html_form" target="_blank">serde_html_form</a>.

And for <code>application/json</code> content type, we call to <a href="https://docs.rs/serde_json/latest/serde_json/fn.from_slice.html" title="serde_json::from_slice(...)" target="_blank">serde_json::from_slice(...)</a> from the already included <a href="https://docs.rs/serde_json/latest/serde_json/" title="serde_json" target="_blank">serde_json</a> crate to do the work.

These're the essential details of the code. The rest is fairly straightforward, and there's also sufficient documentation to aid the reading of the code.

💥 Please also note that there're also some more new modules, such as <a href="https://github.com/behai-nguyen/rust_web_01/blob/6082e2df7f4f073c001f1707ebd418a33a08a6b3/src/bh_libs/api_status.rs" title="src/bh_libs/api_status.rs" target="_blank"><code>src/bh_libs/api_status.rs</code></a> and <a href="https://github.com/behai-nguyen/rust_web_01/blob/6082e2df7f4f073c001f1707ebd418a33a08a6b3/src/helper/messages.rs" title="src/helper/messages.rs" target="_blank"><code>src/helper/messages.rs</code></a>, they're very small, self-explanatory and have sufficient documentation where appropriate.

<a id="step-five-update-lib"></a>
❺ Register new login routes <code>/ui/login</code> and <code>/api/login</code>.

<div style="background-color:rgb(209, 209, 209);padding:10px;">
Updated <a href="https://github.com/behai-nguyen/rust_web_01/blob/6082e2df7f4f073c001f1707ebd418a33a08a6b3/src/lib.rs"
title="src/lib.rs" target="_blank">src/lib.rs</a>:
</div>

```rust
pub async fn run(listener: TcpListener) -> Result<Server, std::io::Error> {
...
            .service(
                web::scope("/ui")
                    .service(handlers::employees_html1)
                    .service(handlers::employees_html2)
                    .service(auth_handlers::login_page)
                    // .service(auth_handlers::home_page),
            )
            .service(
                web::scope("/api")
                    .service(auth_handlers::login)
            )
            .service(
                web::resource("/helloemployee/{last_name}/{first_name}")
                    .wrap(middleware::SayHi)
                    .route(web::get().to(handlers::hi_first_employee_found))
            )
...			
```

<a id="step-six-new-login-page"></a>
❻ The last addition, the new <a href="https://github.com/behai-nguyen/rust_web_01/blob/6082e2df7f4f073c001f1707ebd418a33a08a6b3/templates/auth/login.html" title="templates/auth/login.html" target="_blank"><code>templates/auth/login.html</code></a>.

Please note, this login page has only HTML. There is no CSS at all. It looks like a dog's breakfast, but it does work. There is no client-side validations either. 

The <code>Login</code> button <code>POST</code>s login requests to <code>http://0.0.0.0:5000/api/login</code>, the content type then is <code>application/x-www-form-urlencoded</code>.

For <code>application/json</code> content type, we can use <a href="https://testfully.io/" title="Testfully" target="_blank">Testfully</a>. (We could also write our own AJAX requests to test.)

<a id="step-seven-some-testing"></a>
❼ As this is not yet the final version of the login process, we're not writing any integration tests for it yet. We'll do so in due course...

<a id="step-seven-some-testing-notes-on-cargo-test"></a>
⓵ For the time being, we've written some new code and their associated unit tests. We have also written some documentation examples. The full test with the command <code>cargo test</code> should have all tests pass.

<a id="step-seven-some-testing-manual-tests"></a>
⓶ Manual tests of the new routes. 

In the following two successful tests, I run the application server on an Ubuntu 22.10 machine, and run both the login page and <a href="https://testfully.io/" title="Testfully" target="_blank">Testfully</a> on Windows 10.

Test <code>application/x-www-form-urlencoded</code> submission via login page:

{% include image-gallery.html list=page.gallery-image-list-1 %}

Test <code>application/json</code> submission using <a href="https://testfully.io/" title="Testfully" target="_blank">Testfully</a>:

{% include image-gallery.html list=page.gallery-image-list-2 %}

In this failure test, I run the application server and <a href="https://testfully.io/" title="Testfully" target="_blank">Testfully</a> on Windows 10. The submitted <code>application/json</code> data does not have an <code>email</code> field:

{% include image-gallery.html list=page.gallery-image-list-3 %}

It's been an interesting exercise for me. My understanding of Rust's improved a little. I hope you find the information in this post useful. Thank you for reading and stay safe as always.

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
