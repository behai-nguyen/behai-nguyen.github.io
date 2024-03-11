---
layout: post
title: "Rust: retrofit integration tests to an existing actix-web application."

description: We've previously built an actix-web “application”, which has five (5) public POST and GET routes. We didn't implement any test at all. We're now retrofitting proper integration tests for these existing 5 (five) public routes.

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list:
    - "https://behainguyen.files.wordpress.com/2023/12/093-02.png"
    - "https://behainguyen.files.wordpress.com/2023/12/093-03.png"

tags:
- Rust
- actix-web
- integration test
---

<em>We've previously built an <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> “application”, which has five (5) public <code>POST</code> and <code>GET</code> routes. We didn't implement any test at all. We're now retrofitting proper integration tests for these existing 5 (five) public routes.</em>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rust_web_01" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![093-feature-image.png](https://behainguyen.files.wordpress.com/2023/12/093-feature-image.png) |
|:--:|
| *Rust: retrofit integration tests to an existing actix-web application.* |

🚀 <strong>Please note,</strong> complete code for this post can be downloaded from GitHub with:

```
git clone -b v0.3.0 https://github.com/behai-nguyen/rust_web_01.git
```

The <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> learning application mentioned above has been discussed in the following two (2) previous posts:

<ol>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/10/18/rust-web-application-mysql-server-sqlx-actix-web-and-tera/" title="Rust web application: MySQL server, sqlx, actix-web and tera" target="_blank">Rust web application: MySQL server, sqlx, actix-web and tera</a>.
</li>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/11/26/rust-learning-actix-web-middleware-01/"
title="Rust: learning actix-web middleware 01" target="_blank">Rust: learning actix-web middleware 01</a>.
</li>
</ol>

Detail of the five (5) public routes are:

<ol>
<li style="margin-top:10px;">JSON response route <code>http://0.0.0.0:5000/data/employees</code> -- method: <code>POST</code>; content type: <code>application/json</code>; request body: <code>{"last_name": "%chi", "first_name": "%ak"}</code>.</li>
<li style="margin-top:10px;">JSON response route <code>http://0.0.0.0:5000/data/employees/%chi/%ak</code> -- method <code>GET</code>.</li>
<li style="margin-top:10px;">HTML response route <code>http://0.0.0.0:5000/ui/employees</code> -- method: <code>POST</code>; content type: <code>application/x-www-form-urlencoded; charset=UTF-8</code>; request body: <code>last_name=%chi&first_name=%ak</code>.</li>
<li style="margin-top:10px;">HTML response route <code>http://0.0.0.0:5000/ui/employees/%chi/%ak</code> -- method: <code>GET</code>.</li>
<li style="margin-top:10px;">HTML response route <code>http://0.0.0.0:5000/helloemployee/%chi/%ak</code> -- method: <code>GET</code>.</li>
</ol>

The code we're developing in this post is a continuation of the code from the <a href="https://behainguyen.wordpress.com/2023/11/26/rust-learning-actix-web-middleware-01/" title="Rust: learning actix-web middleware 01" target="_blank">second</a> post above. 🚀 To get the code of this <a href="https://behainguyen.wordpress.com/2023/11/26/rust-learning-actix-web-middleware-01/" title="Rust: learning actix-web middleware 01" target="_blank">second</a>, please use the following command:

```
git clone -b v0.2.0 https://github.com/behai-nguyen/rust_web_01.git
```

<strong>-- Note the tag <code>v0.2.0</code>.</strong>

This post introduces a new module <code>src/lib.rs</code>, and a new directory <code>tests/</code> to the project. The final directory layout's in the screenshot below:

![093-01.png](https://behainguyen.files.wordpress.com/2023/12/093-01.png)

It takes me several iterations to finally figure how to get the test code to work. In this post, I organise the process into logical steps rather than the steps which I have actually tried out.

It turns out there're quite a bit of refactorings to do, in order to get the existing application code into a state where it makes sense to add integration tests. <strong>This is a consequence of not having tests in the first place.</strong>

<h2>Table of contents</h2>

<ul>
<li style="margin-top:10px;"><a href="#code-refactoring">Code Refactoring in Readiness for Integration Tests</a>
<ul>
<li style="margin-top:10px;"><a href="#code-refactoring-step-one">❶ Fixing application crate name and verifying test module gets recognised</a></li>
<li style="margin-top:10px;"><a href="#code-refactoring-step-two">❷ Referencing (importing) the application crate</a></li>
<li style="margin-top:10px;"><a href="#code-refactoring-step-three">❸ Referencing (importing) an application module</a></li>
<li style="margin-top:10px;"><a href="#code-refactoring-step-four">❹ Fixing the existing three (3) <code>Doc-tests</code> errors</a></li>
<li style="margin-top:10px;"><a href="#code-refactoring-step-five">❺ Enable deserialisation for the <code>struct Employee</code></a></li>
</ul>
</li>
<li style="margin-top:10px;"><a href="#integration-tests">Implementing Integration Tests</a>
<ul>
<li style="margin-top:10px;"><a href="#impl-step-one">❶ Add development crates to <code>Cargo.toml</code>'s <code>[dev-dependencies]</code></a></li>
<li style="margin-top:10px;"><a href="#impl-step-two">❷ Refactor <code>main()</code> into a callable method <code>run()</code></a></li>
<li style="margin-top:10px;"><a href="#impl-step-three">❸ <code>main()</code> calls <code>run()</code></a></li>
<li style="margin-top:10px;"><a href="#impl-step-four">❹ Integration test <code>spawn_app()</code> method</a></li>
<li style="margin-top:10px;"><a href="#impl-step-five">❺ Finish off the first integration test method</a></li>
<li style="margin-top:10px;"><a href="#impl-step-six">❻ Some observations</a></li>
<li style="margin-top:10px;"><a href="#impl-step-seven">❼ Implement server dynamic port</a>
<ul>
<li style="margin-top:10px;"><a href="#impl-step-seven-one">⓵ The <code>run()</code> method</a></li>
<li style="margin-top:10px;"><a href="#impl-step-seven-two">⓶ The <code>main()</code> method</a></li>
<li style="margin-top:10px;"><a href="#impl-step-seven-three">⓷ The <code>spawn_app()</code> method</a></li>
<li style="margin-top:10px;"><a href="#impl-step-seven-four">⓸ Integration test methods</a></li>
</ul>
</li>
</ul>
</li>
</ul>

<h3 style="color:teal;text-transform: none;">
  <a id="code-refactoring">Code Refactoring in Readiness for Integration Tests</a>
</h3>

<a id="code-refactoring-step-one"></a>
❶ Fixing application crate name and verifying test module gets recognised.

<a href="https://doc.rust-lang.org/book/" title="The Rust Programming Language" target="_blank">“The Book”</a>, chapter 10, <a href="https://doc.rust-lang.org/book/ch11-00-testing.html" title="Writing Automated Tests" target="_blank">Writing Automated Tests</a> discusses testing, section <a href="https://doc.rust-lang.org/book/ch11-03-test-organization.html#test-organization" title="Test Organization" target="_blank">Test Organization</a> discusses directory structure for integration tests.

<a id="code-refactoring-step-one-one"></a>
⓵ Before starting this post, I reread this chapter, and realise that the package name in <code>Cargo.toml</code> is not right: it uses hyphens -- where underscores should be used:

```toml
[package]
name = "learn_actix_web"
...
```

<a id="code-refactoring-step-one-two"></a>
⓶ Also, the above chapter illustrates a simple integration test. I'm not certain if it'll work for this project. I have to test it out.

Create a new <code>tests/</code> directory at the same level as <code>src/</code>. And then in this <code>tests/</code> directory create a new file <code>test_handlers.rs</code>, add a dummy test to verify that the new test module gets recognised.

```
Content of tests/test_handlers.rs:
```

```rust
#[actix_web::test]
async fn dummy_test() {
    let b: bool = true;
    assert_eq!(b, true);
}
```

🚀 Run a test with the command <code>cargo test</code>, <code>dummy_test()</code> passes. 👎 But the three (3) existing <code>Doc-tests</code> fail, we'll come back to these <a href="#code-refactoring-step-four">in a later</a> section.

<a id="code-refactoring-step-two"></a>
❷ Referencing (importing) the application crate <code>learn_actix_web</code>.

<a id="code-refactoring-step-two-one"></a>
⓵ Add <code>use learn_actix_web;</code> to <code>tests/test_handlers.rs</code>:

```rust
//...
//...
use learn_actix_web;

#[actix_web::test]
async fn dummy_test() {
...
```

The compiler complains:

```
error[E0432]: unresolved import `learn_actix_web`
 --> tests\test_handlers.rs:3:5
  |
3 | use learn_actix_web;
  |     ^^^^^^^^^^^^^^^ no external crate `learn_actix_web`
```

<a id="code-refactoring-step-two-two"></a>
⓶ ✔️ To fix this error, simply create a new empty file <code>src/lib.rs</code>.

The build command <code>cargo build</code> should now run successfully.

<a id="code-refactoring-step-three"></a>
❸ Referencing (importing) an application module. 

Now, in <code>tests/test_handlers.rs</code>, change <code>use learn_actix_web;</code> to <code>use learn_actix_web::config;</code>, i.e.:

```rust
//...
//...
use learn_actix_web::config;

#[actix_web::test]
async fn dummy_test() {
...
```

The compiler complains:

```
error[E0432]: unresolved import `learn_actix_web::config`
 --> tests\test_handlers.rs:3:5
  |
3 | use learn_actix_web::config;
  |     ^^^^^^^^^^^^^^^^^^^^^^^ no `config` in the root
```

<code>src/main.rs</code> is the binary. <code>src/lib.rs</code> is the library, it's the root for the crate / package <code>learn_actix_web</code>, (I do hope I've this correctly); we need to carry out the following steps to fix this error.

⓵ Move all existing <code>mod</code> imports and <code>struct AppState</code> in <code>src/main.rs</code> to <code>src/lib.rs</code> and make them all public.

```
Content of src/lib.rs:
```

```rust
use sqlx::{Pool, MySql};

pub mod config;
pub mod database;
pub mod utils;
pub mod models;
pub mod handlers;

pub mod middleware;

pub struct AppState {
    db: Pool<MySql>,
}
```

⓶ Update <code>src/main.rs</code>:

● remove <code>use sqlx::{Pool, MySql};</code>

● add <code>use learn_actix_web::{config, database, AppState, middleware, handlers};</code>

The compiler should now accept <code>use learn_actix_web::config;</code> import in <code>tests/test_handlers.rs</code>.

<a id="code-refactoring-step-four"></a>
❹ Fixing the existing three (3) <code>Doc-tests</code> errors mentioned in <a href="#code-refactoring-step-one-two">step ❶.⓶</a> above.

<a id="code-refactoring-step-four-one"></a>
⓵ In <code>src/config.rs</code>, update <code>/// mod config;</code> to <code>/// use learn_actix_web::config;</code>.

<a id="code-refactoring-step-four-two"></a>
⓶ In <code>src/database.rs</code>, update <code>/// mod database;</code> to <code>/// use learn_actix_web::database;</code>.

<a id="code-refactoring-step-four-three"></a>
⓷ In <code>src/models.rs</code>, there're several updates:

● Replace <code>/// mod models;</code> and <code>/// use models::get_employees;</code> with <code>/// use learn_actix_web::models::get_employees;</code>.

● Bug fix. Change <code>/// let query_result = task::block_on(get_employees(pool, "nguy%", "be%"));</code> to <code>/// let query_result = task::block_on(get_employees(&pool, "nguy%", "be%"));</code>; i.e. update parameter <code>pool</code> to <code>&pool</code>.

● Update <code>/// mod database;</code> to <code>/// use learn_actix_web::database;</code>.

All tests should now pass.

<a id="code-refactoring-step-five"></a>
❺ In <code>src/models.rs</code>, enable deserialisation for the <code>struct Employee</code>.

Some of the routes return employee data in JSON format. Some of the tests would require deserialising JSON data into <code>struct Employee</code>, which does not yet implement the <a href="https://docs.rs/serde/latest/serde/de/trait.Deserialize.html" title="serde::de::Deserialize trait" target="_blank">serde::de::Deserialize</a> trait.

If we just add the <code>Deserialize</code> macro to <code>struct Employee</code>, the compiler will complain:

```
error[E0425]: cannot find function `deserialize` in module `utils::australian_date_format`
  --> src\models.rs:17:26
   |
17 |   #[derive(FromRow, Debug, Deserialize, Serialize)]
   |                            ^^^^^^^^^^^ help: a function with a similar name exists: `serialize`
   |
  ::: src\utils.rs:17:5
   |
17 | /     pub fn serialize<S>(
18 | |         date: &Date,
19 | |         serializer: S,
20 | |     ) -> Result<S::Ok, S::Error>
...  |
26 | |         serializer.serialize_str(&s)
27 | |     }
   | |_____- similarly named function `serialize` defined here
   |
   = note: this error originates in the derive macro `Deserialize` (in Nightly builds, run with -Z macro-backtrace for more info)
```

✔️ To address this, update <code>src/utils.rs</code>. Implement <code>pub fn deserialize&lt;'de, D>(deserializer: D,) -> Result&lt;Date, D::Error></code> for <code>mod australian_date_format</code>.

<code>Employee</code> can now implement both <code>Deserialize</code> and <code>Serialize</code>, we also throw in <code>Debug</code>:

```rust
#[derive(FromRow, Debug, Deserialize, Serialize)]
pub struct Employee {
...
```

Please note also, in <code>src/models.rs</code>, two (2) unit tests have also been added <code>fn test_employee_serde()</code> and <code>fn test_employee_serde_failure()</code>.

We are now ready to implement actual integration tests. All test methods will be in <code>tests/test_handlers.rs</code>.

<h3 style="color:teal;text-transform: none;">
  <a id="integration-tests">Implementing Integration Tests</a>
</h3>

My original plan is to follow <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a>'s instructions in section <a href="https://actix.rs/docs/testing/#integration-testing-for-applications" title="Integration Testing For Applications" target="_blank">Integration Testing For Applications</a>.

<a id="impl-first-attempt"></a>
I start off implementing the first test method <code>async fn get_helloemployee_has_data()</code>, which tests the route <code>http://0.0.0.0:5000//helloemployee/{last_name}/{first_name}</code>.

Eventually, it becomes clear that we need to have the <a href="https://docs.rs/actix-web/latest/actix_web/struct.App.html" title="actix-web App object" target="_blank">App</a> object in the test code to run tests!

I don't want to create the <a href="https://docs.rs/actix-web/latest/actix_web/struct.App.html" title="actix-web App object" target="_blank">App</a> object in every test! <strong>For me personally, this might introduce bugs in the tests, and this would defeat the purpose of testing.</strong>

I attempt to refactor the code so that both the application and the test code could just call some method and have the <a href="https://docs.rs/actix-web/latest/actix_web/struct.App.html" title="actix-web App object" target="_blank">App</a> object ready: <strong>this would guarantee the same App object code is in the application proper and the tests.</strong>

-- But this proves to be difficult! On Jun 13, 2022, someone has tried this and has also given up, please see this StackOverflow post <a href="https://stackoverflow.com/questions/72415245/actix-web-integration-tests-reusing-the-main-thread-application" title="Actix-web integration tests: reusing the main thread application" target="_blank">Actix-web integration tests: reusing the main thread application</a>. This <a href="https://stackoverflow.com/questions/72415245/actix-web-integration-tests-reusing-the-main-thread-application#comment128248572_72415245" title="first answer" target="_blank">first answer</a> basically suggests that in the tests, we just run the application proper as is, then use <a href="https://docs.rs/reqwest/latest/reqwest/" title="reqwest" target="_blank">reqwest</a> crate to send requests and receiving responses from the application.

This approach has been discussed in detail by Luca Palmieri in the sample 59-page extract of his book <a href="https://www.zero2prod.com/assets/sample_zero2prod.pdf" title="ZERO TO PRODUCTION IN RUST by Luca Palmieri" target="_blank">ZERO TO PRODUCTION IN RUST</a>. I abandon <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a>'s integration test framework, and use the just mentioned approach.

<a id="impl-step-one"></a>
❶ We'd need <a href="https://docs.rs/tokio/latest/tokio/" title="crate tokio" target="_blank">tokio</a> and <a href="https://docs.rs/reqwest/latest/reqwest/" title="reqwest" target="_blank">reqwest</a> crates, but only for testing. It makes sense to add them to the <code>[dev-dependencies]</code> section of <code>Cargo.toml</code>:

```toml
...
[dev-dependencies]
tokio = {version = "1", features = ["full"]}
reqwest = {version = "0.11", features = ["json"]}
...
```

<a id="impl-step-two"></a>
❷ The next step is refactoring <code>async fn main() -> std::io::Result&lt;()></code> into a callable method which both the application and test code can call. This method should return an <a href="https://docs.rs/actix-web/latest/actix_web/dev/struct.Server.html" title="actix_web::dev::Server" target="_blank">actix_web::dev::Server</a> instance. Function <code>src/main.rs</code>'s <code>main()</code> moved to <code>src/lib.rs</code>, and renamed to <code>run()</code>:

```
src/lib.rs with run() method added:
```

```rust
...
pub fn run() -> Result<Server, std::io::Error> {
    ...
    let server = HttpServer::new(move || {
            // Everything remains the same.
    })
    .bind(("0.0.0.0", 5000))?
    .run();

    Ok(server)
}
...
```

Note the following about the <code>run()</code> method:

<ul>
<li style="margin-top:10px;">the return value has been changed to <code>Result<Server, std::io::Error></code>.</li>
<li style="margin-top:10px;">it isn't <code>async</code>, therefore no <code>.await</code> call.</li>
<li style="margin-top:10px;">if no error occurs, it returns <code>Ok(server)</code> (of course!)</li>
</ul>

<a id="impl-step-three"></a>
❸ Now <code>main()</code> should now call <code>run()</code>.

```
Content of src/main.rs:
```

```rust
use learn_actix_web::run;

#[actix_web::main]
async fn main() -> Result<(), std::io::Error> {
    run()?.await
}
```

<a id="impl-step-four"></a>
❹ The next step is the <code>spawn_app()</code> method which evokes the application server during tests. I anticipate having more integration test modules in the future, so I have <code>spawn_app()</code> in <code>tests/common.rs</code>, among other smaller helper methods.

```
tests/common.rs with spawn_app() method:
```

```rust
use learn_actix_web::run;

pub fn spawn_app() {
    let server = run().expect("Failed to create server");
    let _ = tokio::spawn(server);
}
...
```

<a id="impl-step-five"></a>
❺ Now, we can finish off the first integration test method <code>async fn get_helloemployee_has_data()</code>, which has been <a href="#impl-first-attempt">attempted previously</a>:

```
tests/test_handlers.rs with get_helloemployee_has_data() method:
```

<a id="get-helloemployee-has-data"></a>
```rust
#[actix_web::test]
async fn get_helloemployee_has_data() {
    let root_url = "http://localhost:5000";

    spawn_app();

    let client = reqwest::Client::new();

    let response = client
        .get(make_full_url(root_url, "/helloemployee/%chi/%ak"))
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

Crate <a href="https://docs.rs/reqwest/latest/reqwest/" title="reqwest" target="_blank">reqwest</a> is feature rich. It seems to handle all HTTP methods, all request content types as well as all response content types. To finish off the other integration test methods, I have to spend times reading the documentation, but they follow pretty much the same pattern. I won't list out the rest of the code, please see them for yourself.

<a id="impl-step-six"></a>
❻ 💥 I would like to point out the following.

<ul>
<li style="margin-top:10px;"><code>spawn_app()</code> behaves like having the actual application server running. That is, if we remove <code>spawn_app()</code> from the test code, and run the application server instead, the tests would still run. (This should be apparent also from how <a href="https://docs.rs/reqwest/latest/reqwest/" title="reqwest" target="_blank">reqwest</a> is used.)</li>
<li style="margin-top:10px;">In total, there are six (6) integration tests. During a test run, <code>spawn_app()</code> gets called 6 (six) times. On Windows 10, this does not appear to be an issue. On Ubuntu 22.10, test methods fail at random with error messages such as <code><span style="color:red;">thread 'post_employees_html1' panicked at 'Failed to create server: Os { code: 98, <br/> kind: AddrInUse, message: "Address already in use" }', tests/common.rs:8:24</span></code>. This error has been discussed in <a href="https://www.zero2prod.com/assets/sample_zero2prod.pdf" title="ZERO TO PRODUCTION IN RUST by Luca Palmieri" target="_blank">ZERO TO PRODUCTION IN RUST</a> -- we need to implement dynamic port to address this problem.</li>
</ul>

<a id="impl-step-seven"></a>
❼ Implement dynamic port using <a href="https://doc.rust-lang.org/std/net/struct.TcpListener.html" title="std::net::TcpListener" target="_blank">std::net::TcpListener</a>.

<a id="impl-step-seven-one"></a>
⓵ The <code>run()</code> method should receive a ready to use instance of <a href="https://doc.rust-lang.org/std/net/struct.TcpListener.html" title="std::net::TcpListener" target="_blank">std::net::TcpListener</a>:

```
src/lib.rs with run() method updated:
```

```rust
use std::net::TcpListener;
...
pub fn run(listener: TcpListener) -> Result<Server, std::io::Error> {
    ...
    let server = HttpServer::new(move || {
            // Everything remains the same.
    })
    .listen(listener)?
    .run();

    Ok(server)
}
...
```

Not a significant change, apart from the additional parameter, the <code>listen(...)</code> method is used instead of the <code>bind(...)</code> method.

<a id="impl-step-seven-two"></a>
⓶ The <code>main()</code> method must then instantiate an instance of <a href="https://doc.rust-lang.org/std/net/struct.TcpListener.html" title="std::net::TcpListener" target="_blank">std::net::TcpListener</a>:

```
Content of src/main.rs:
```

```rust
use std::net::TcpListener;
use learn_actix_web::run;

#[actix_web::main]
async fn main() -> Result<(), std::io::Error> {
    let listener = TcpListener::bind("0.0.0.0:5000").expect("Failed to bind port 5000");
    // We retrieve the port assigned to us by the OS
    let port = listener.local_addr().unwrap().port();
    println!("Server is listening on port {}", port);

    run(listener)?.await
}
```

For the application, we want a fixed port, we use the current <code>port 5000</code>, as before.

<a id="impl-step-seven-three"></a>
⓷ Similar to <code>main()</code>, <code>spawn_app()</code> must also instantiate an instance of <a href="https://doc.rust-lang.org/std/net/struct.TcpListener.html" title="std::net::TcpListener" target="_blank">std::net::TcpListener</a>.

-- But we want the system to dynamically allocate port on the run, so we bind to <code>port 0</code>.

In addition, it should also formulate the root URL using the dynamically assigned port so that test methods can use this root URL to talk to the test application server.

```
tests/common.rs with spawn_app() updated:
```

```rust
use std::net::TcpListener;
use learn_actix_web::run;

pub fn spawn_app() -> String {
    let listener = TcpListener::bind("0.0.0.0:0")
        .expect("Failed to bind random port");
    
    // We retrieve the port assigned to us by the OS
    let port = listener.local_addr().unwrap().port();

    let server = run(listener).expect("Failed to create server");
    let _ = tokio::spawn(server);

    format!("http://127.0.0.1:{}", port)
}
```

<a id="impl-step-seven-four"></a>
⓸ Next, all integration test methods must be updated to use the root URL returned by <code>spawn_app()</code>. For example, <a href="#get-helloemployee-has-data"><code>async fn get_helloemployee_has_data()</code></a> above gets a single update:

```rust
#[actix_web::test]
async fn get_helloemployee_has_data() {
    let root_url = &spawn_app();

    ...
}
```

That is, instead of <code>let root_url = "http://localhost:5000";</code>, the root URL is now the returned value of the <code>spawn_app()</code> method.

All tests now pass on both Windows 10 and Ubuntu 22.10:

{% include image-gallery.html list=page.gallery-image-list %}

<br/>
From this point onwards, new functionalities and their integration tests can be developed and tested at the same.

I've learned a lot during this process. I hope you find the information in this post helpful. Thank you for reading and stay safe as always.

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