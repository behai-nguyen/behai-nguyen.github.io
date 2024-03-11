---
layout: post
title: "Rust: adding actix-session and actix-identity to an existing actix-web application."

description: I've been studying user authentication with the actix-web framework. It seems that a popular choice is to use crate actix-identity, which requires crate actix-session. To add these two (2) crates, the code of the existing application must be refactored a little. We first look at code refactoring and integration. Then we briefly discuss the official examples given in the documentation of the 2 (two) mentioned crates.

tags:
- Rust
- actix-web
- actix-session
- actix-identity
---

<em>I've been studying user authentication with the <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> framework. It seems that a popular choice is to use crate <a href="https://docs.rs/actix-identity/latest/actix_identity/" title="Crate actix_identity" target="_blank">actix-identity</a>, which requires crate <a href="https://docs.rs/actix-session/latest/actix_session/" title="Crate actix_session" target="_blank">actix-session</a>. To add these two (2) crates, the code of the existing application must be refactored a little. We first look at code refactoring and integration. Then we briefly discuss the official examples given in the documentation of the 2 (two) mentioned crates.</em>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rust_web_01" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![094-feature-image.png](https://behainguyen.files.wordpress.com/2024/01/094-feature-image.png) |
|:--:|
| *Rust: adding actix-session and actix-identity to an existing actix-web application.* |

🚀 <strong>Please note,</strong> complete code for this post can be downloaded from GitHub with:

```
git clone -b v0.4.0 https://github.com/behai-nguyen/rust_web_01.git
```

The <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> learning application mentioned above has been discussed in the following three (3) previous posts:

<ol>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/10/18/rust-web-application-mysql-server-sqlx-actix-web-and-tera/" title="Rust web application: MySQL server, sqlx, actix-web and tera" target="_blank">Rust web application: MySQL server, sqlx, actix-web and tera</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/11/26/rust-learning-actix-web-middleware-01/" title="Rust: learning actix-web middleware 01" target="_blank">Rust: learning actix-web middleware 01</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/12/31/rust-retrofit-integration-tests-to-an-existing-actix-web-application/" title="Rust: retrofit integration tests to an existing actix-web application." target="_blank">Rust: retrofit integration tests to an existing actix-web application</a>.</li>
</ol>

The code we're developing in this post is a continuation of the code from the <a href="https://behainguyen.wordpress.com/2023/12/31/rust-retrofit-integration-tests-to-an-existing-actix-web-application/" title="Rust: retrofit integration tests to an existing actix-web application." target="_blank">third</a> post above. 🚀 To get the code of this <a href="https://behainguyen.wordpress.com/2023/12/31/rust-retrofit-integration-tests-to-an-existing-actix-web-application/" title="Rust: retrofit integration tests to an existing actix-web application." target="_blank">third</a> post, please use the following command:

```
git clone -b v0.3.0 https://github.com/behai-nguyen/rust_web_01.git
```

<strong>-- Note the tag <code>v0.3.0</code>.</strong>

The session storage backend we use with <a href="https://docs.rs/actix-session/latest/actix_session/" title="Crate actix_session" target="_blank">actix-session</a> is <a href="https://docs.rs/actix-session/latest/actix_session/storage/struct.RedisSessionStore.html" title="actix_session::storage::RedisSessionStore" target="_blank">RedisSessionStore</a>, it requires Redis server. We use the Redis Official Docker Image as discussed in the following post:

<ul>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/12/23/using-the-redis-official-docker-image-on-windows-10-and-ubuntu-22-10-kinetic/" title="Using the Redis Official Docker Image on Windows 10 and Ubuntu 22.10 kinetic." target="_blank">Using the Redis Official Docker Image on Windows 10 and Ubuntu 22.10 kinetic</a>.</li>
</ul>

<h3 style="color:teal;text-transform: none;">
  <a id="code-refactoring-integration">Code Refactoring and Integration</a>
</h3>

❶ Adding the two (2) crates to <code>Cargo.toml</code>:

```toml
[dependencies]
...
actix-session = {version = "0.8.0", features = ["redis-rs-session"]}
actix-identity = "0.6.0"
```

For crate <a href="https://docs.rs/actix-session/latest/actix_session/" title="Crate actix_session" target="_blank">actix-session</a>, we need to enable the <code>redis-rs-session</code> feature as per the official document instructions.

❷ Update function <code>run(...)</code> to <code>async</code>.

The current code as in <a href="https://behainguyen.wordpress.com/2023/12/31/rust-retrofit-integration-tests-to-an-existing-actix-web-application/" title="Rust: retrofit integration tests to an existing actix-web application." target="_blank">the last (third)</a> post has <code>run(...)</code> in <code>src/lib.rs</code> as a synchronous function:

```rust
pub fn run(listener: TcpListener) -> Result<Server, std::io::Error> {
...
```

This makes instantiating a required instance of <a href="https://docs.rs/actix-session/latest/actix_session/storage/struct.RedisSessionStore.html" title="actix_session::storage::RedisSessionStore" target="_blank">RedisSessionStore</a> impossible for me! <strong>“Impossible for me”</strong> because I tried and could not get it to work. I won't list out what I've tried, it'd be a waste of time.

The next best option is to refactor it to <code>async</code>, and follow the official documentations to register <a href="https://docs.rs/actix-identity/latest/actix_identity/struct.IdentityMiddleware.html" title="IdentityMiddleware" target="_blank">IdentityMiddleware</a> and <a href="https://docs.rs/actix-session/latest/actix_session/struct.SessionMiddleware.html" title="SessionMiddleware" target="_blank">SessionMiddleware</a>.

```
Updated src/lib.rs:
```

```rust
pub async fn run(listener: TcpListener) -> Result<Server, std::io::Error> {
    ...

    let pool = database::get_mysql_pool(config.max_connections, &config.database_url).await;

    let secret_key = Key::generate();
    let redis_store = RedisSessionStore::new("redis://127.0.0.1:6379")
        .await
        .unwrap();

    let server = HttpServer::new(move || {
        ...

        App::new()
            .app_data(web::Data::new(AppState {
                db: pool.clone()
            }))
            .wrap(IdentityMiddleware::default())
            .wrap(SessionMiddleware::new(
                    redis_store.clone(),
                    secret_key.clone()
            ))
            .wrap(cors)
			
            ...
    })
    .listen(listener)?
    .run();

    Ok(server)
}
```

💥 Please note the following:

<ol>
<li style="margin-top:10px;">The two (2) new middleware get registered before the existing <a href="https://docs.rs/actix-cors/latest/actix_cors/struct.Cors.html" title="Cors middleware" target="_blank">Cors middleware</a>, (i.e., <code>.wrap(cors)</code>). Recall from the <a href="https://docs.rs/actix-web/latest/actix_web/middleware/index.html" title="actix-web middleware" target="_blank">actix-web middleware</a> documenation that middleware get called in reverse order of registration, we want the <a href="https://docs.rs/actix-cors/latest/actix_cors/struct.Cors.html" title="Cors middleware" target="_blank">Cors middleware</a> to run first to reject invalid requests at an early stage.</li>
<li style="margin-top:10px;">Now that <code>run(...)</code> is an <code>async</code> function, we can call <code>.await</code> on <code>database::get_mysql_pool(...)</code> instead of wrap it in the <a href="https://docs.rs/async-std/latest/async_std/task/fn.block_on.html" title="Function async_std::task::block_on" target="_blank">async_std::task::block_on</a> function.</li>
<li style="margin-top:10px;">Apart from the above refactorings, nothing else has been changed.</li>
</ol>

All functions who call <code>run(...)</code> must also be refactored now that <code>run(...)</code> is an <code>async</code> function. They are <code>main()</code>, <code>spawn_app()</code> and all integration test methods which call <code>spawn_app()</code>.

❸ Update function <code>main()</code>.

```
Updated src/main.rs:
```

```rust
...
#[actix_web::main]
async fn main() -> Result<(), std::io::Error> {
    ...

    let server = run(listener).await.unwrap();
    server.await
}
```

Note, the code in the previous version:

```rust
    ...
    run(listener)?.await
```

❹ Update function <code>spawn_app()</code>.

```
Updated tests/common.rs:
```

```rust
pub async fn spawn_app() -> String {
    ...
    let server = run(listener).await.unwrap();
    let _ = tokio::spawn(server);
    ...
}
```

Note, the code in the previous version:

```rust
    ...
    let server = run(listener).expect("Failed to create server");
    let _ = tokio::spawn(server);
    ...
```

❺ Accordingly, in <code>tests/test_handlers.rs</code> all calls to <code>spawn_app()</code> updated to <code>let root_url = &spawn_app().await;</code>.

```
tests/test_handlers.rs with get_helloemployee_has_data() updated:
```

```rust
#[actix_web::test]
async fn get_helloemployee_has_data() {
    let root_url = &spawn_app().await;

    ...
}
```

❻ Other, unrelated and general refactorings.

⓵ This could be regarded as a bug fix. 

In <code>src/handlers.rs</code>, endpoint handler methods are <code>async</code>, and so where <code>get_employees(...)</code> gets called, chain <code>.await</code> to it instead of wrapping it in the <a href="https://docs.rs/async-std/latest/async_std/task/fn.block_on.html" title="Function async_std::task::block_on" target="_blank">async_std::task::block_on</a> function -- which does not make any sense!

⓶ In modules <code>src/database.rs</code> and <code>src/models.rs</code>, the documentations now have both synchronous and asynchronous examples where appropriate.

<h3 style="color:teal;text-transform: none;">
  <a id="session-identity-examples">Some Notes on Crates <code>actix-session</code> and <code>actix-identity</code> Examples</a>
</h3>

For each crate, I try out two (2) examples as listed in the documentations: one using cookie and one using Redis. <strong><em>I start off using <a href="https://testfully.io/" title="Testfully" target="_blank">Testfully</a> as the client, and none works! And they are short and easy to understand examples! </em></strong>

Then I try using browsers. This also involves writing a simple HTML page. All examples work in browsers.

❶ The <a href="https://docs.rs/actix-session/latest/actix_session/" title="Crate actix_session" target="_blank">actix-session</a> example using cookie.

```
Content of Cargo.toml:
```

```toml
[dependencies]
actix-session = {version = "0.8.0", features = ["cookie-session"]}
log = "0.4.20"
env_logger = "0.10.1"
```

The complete <a href="https://github.com/actix/examples/blob/master/auth/cookie-session/src/main.rs" title="https://github.com/actix/examples/blob/master/auth/cookie-session/src/main.rs" target="_blank">src/main.rs can be found on GitHub</a>. Run <code>http://localhost:8080/</code> on browsers to see how it works.

❷ The <a href="https://docs.rs/actix-session/latest/actix_session/" title="Crate actix_session" target="_blank">actix-session</a> example using Redis.

```
Content of Cargo.toml:
```

```toml
[dependencies]
actix-web = "4.4.0"
actix-session = {version = "0.8.0", features = ["redis-actor-session"]}
```

The actual example code I put together from the examples listed in the document page:

```rust
#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // The secret key would usually be read from a configuration file/environment variables.
    let secret_key = Key::generate();
    let redis_connection_string = "127.0.0.1:6379";
    HttpServer::new(move ||
            App::new()
            // Add session management to your application using Redis for session state storage
            .wrap(
                SessionMiddleware::new(
                    RedisActorSessionStore::new(redis_connection_string),
                    secret_key.clone()
                )
            )
            .route("/index", web::get().to(index))
            .default_service(web::to(|| HttpResponse::Ok())))            
        .bind(("0.0.0.0", 8080))?
        .run()
        .await
}

async fn index(session: Session) -> Result<&'static str, Error> {    
    // access the session state
    if let Some(count) = session.get::<i32>("counter")? {
        println!("SESSION value: {}", count);
        // modify the session state
        session.insert("counter", count + 1)?;
    } else {
        session.insert("counter", 1)?;
    }

    Ok("Welcome!")
}
```

On browsers, repeatedly run <code>http://localhost:8080/index</code>, watch both the output on browsers and on the console.

❸ The <a href="https://docs.rs/actix-identity/latest/actix_identity/" title="Crate actix_identity" target="_blank">actix-identity</a> example using cookie.

```
Content of Cargo.toml:
```

```toml
[dependencies]
actix-web = "4.4.0"
actix-identity = "0.6.0"
actix-session = {version = "0.8.0", features = ["cookie-session"]}
env_logger = "0.10.1"
```

The complete <a href="https://github.com/actix/actix-extras/blob/master/actix-identity/examples/identity.rs" title="https://github.com/actix/actix-extras/blob/master/actix-identity/examples/identity.rs" target="_blank">src/main.rs can be found on GitHub</a>. 

We describe how to run this example after the listing of the next and last example. As both can be run using the same HTML page.

❹ The <a href="https://docs.rs/actix-identity/latest/actix_identity/" title="Crate actix_identity" target="_blank">actix-identity</a> example using Redis.

```
Content of Cargo.toml:
```

```toml
[dependencies]
actix-web = "4.4.0"
actix-session = {version = "0.8.0", features = ["redis-rs-session"]}
actix-identity = "0.6.0"
```

The actual example code I put together from the examples listed in the document page:

```rust
#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let secret_key = Key::generate();
    let redis_store = RedisSessionStore::new("redis://127.0.0.1:6379")
        .await
        .unwrap();

    HttpServer::new(move || {
        App::new()
            // Install the identity framework first.
            .wrap(IdentityMiddleware::default())
            // The identity system is built on top of sessions. You must install the session
            // middleware to leverage `actix-identity`. The session middleware must be mounted
            // AFTER the identity middleware: `actix-web` invokes middleware in the OPPOSITE
            // order of registration when it receives an incoming request.
            .wrap(SessionMiddleware::new(
                 redis_store.clone(),
                 secret_key.clone()
            ))
            .service(index)
            .service(login)
            .service(logout)
    })
    .bind(("0.0.0.0", 8080))?
    .run()
    .await
}

#[get("/")]
async fn index(user: Option<Identity>) -> impl Responder {
    if let Some(user) = user {
        format!("Welcome! {}", user.id().unwrap())
    } else {
        "Welcome Anonymous!".to_owned()
    }
}

#[post("/login")]
async fn login(request: HttpRequest) -> impl Responder {
    // Some kind of authentication should happen here
    // e.g. password-based, biometric, etc.
    // [...]

    let token = String::from("test");

    // attach a verified user identity to the active session
    Identity::login(&request.extensions(), token.into()).unwrap();

    HttpResponse::Ok()
}

#[post("/logout")]
async fn logout(user: Identity) -> impl Responder {
    user.logout();
    HttpResponse::Ok()
}
```

Both the above two examples can be tested using the following HTML page:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
	<meta name="author" content="behai_nguyen@hotmail.com">
    <title>Test</title>
</head>

<body>
    <form method="post" action="http://localhost:8080/login" id="loginForm">
        <button type="submit">Login</button>
    </form>
	
    <form method="post" action="http://localhost:8080/logout" id="logoutForm">
        <button type="submit">Logout</button>
    </form>
</body>
</html>
```

Run the above HTML page, then:

<ol>
<li style="margin-top:10px;">Click on the <code>Login</code> button</li>
<li style="margin-top:10px;">Then run <code>http://localhost:8080/</code></li>
<li style="margin-top:10px;">Then click on the <code>Logout</code> button</li>
<li style="margin-top:10px;">Then run <code>http://localhost:8080/</code></li>
</ol>

Having been able to integrate these two (2) crates is a small step toward the authentication functionality which I'd like to build as a part of this learning application.

I write this post primarily just a record of what I've learned. I hope you somehow find the information helpful. Thank you for reading and stay safe as always.

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