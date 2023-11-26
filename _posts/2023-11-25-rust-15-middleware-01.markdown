---
layout: post
title: "Rust: learning actix-web middleware 01."

description: We add request path extractor and MySQL database query calls to the official SayHi middleware example. The middleware creates a text message, attaches it to the request via extension. This text message contains the detail of the first matched record, if any found, otherwise a no record found message. A resource endpoint service handler then extracts this message, and returns it as HTML to the client.

tags:
- Rust
- actix-web
- middleware
---

<em>We add request path extractor and MySQL database query calls to the official <code>SayHi</code> middleware example. The middleware creates a text message, attaches it to the request via extension. This text message contains the detail of the first matched record, if any found, otherwise a no record found message. A resource endpoint service handler then extracts this message, and returns it as HTML to the client.</em>

| ![091-feature-image.png](https://behainguyen.files.wordpress.com/2023/11/091-feature-image.png) |
|:--:|
| *Rust: learning actix-web middleware 01.* |

We've previously discussed a simple web application in 
<a href="https://behainguyen.wordpress.com/2023/10/18/rust-web-application-mysql-server-sqlx-actix-web-and-tera/" title="Rust web application: MySQL server, sqlx, actix-web and tera" target="_blank">Rust web application: MySQL server, sqlx, actix-web and tera</a>.
We're going to add this refactored <code>SayHi</code> middleware to
this existing web application.

🚀 <strong>Please note:</strong> complete code for this post
can be downloaded from GitHub with:

```
git clone -b v0.2.0 https://github.com/behai-nguyen/rust_web_01.git
```

Following are documentation, posts and examples which help me
to write the example code in this post:

<ul>
<li style="margin-top:10px;">
<a href="https://docs.rs/actix-web/latest/actix_web/middleware/index.html" title="Module actix_web::middleware" target="_blank">Module actix_web::middleware</a> 
-- official documentation on middleware.
</li>

<li style="margin-top:10px;">
<a href="https://imfeld.dev/writing/actix-web-middleware" title="Demystifying Actix Web Middleware" target="_blank">Demystifying Actix Web Middleware</a>
-- I find the author explains middleware in a “programmer context”, greatly complements the official documentation.
</li>

<li style="margin-top:10px;">
<a href="https://github.com/actix/examples/tree/master/middleware"
title="GitHub actix examples middleware" target="_blank">GitHub actix examples middleware</a>
-- I don't know if this's the official repo or not, they seem to demonstrate a lot of middleware capabilities.
</li>

<li style="margin-top:10px;">
<a href="https://github.com/actix/examples/tree/master/middleware/request-extensions)"
title="actix GitHub middleware request-extensions example" target="_blank">actix GitHub middleware request-extensions example</a>
-- this example demonstrates how to attach custom data to request extension in a middleware, 
and having an endpoint handler to extract and return this custom data to the requesting client.
</li>

<li style="margin-top:10px;">
<a href="https://users.rust-lang.org/t/how-to-pass-data-to-an-actix-middleware/75262"
title="Rust language user forum | How to pass data to an actix middleware"
target="_blank">Rust language user forum | How to pass data to an actix middleware</a>
-- discussions and a solution on how a middleware can access application state data.
</li>
</ul>

<a id="the-first-example"></a>
❶ To start off, we'll get the <code>SayHi</code> middleware to run
as an independent web project. I'm reprinting the example code with 
a complete <code>fn main()</code>.

<code>Cargo.toml</code> <code>dependencies</code> section is as follow:

```toml
...
[dependencies]
actix-web = "4.4.0"
```

```
Content of src/main.rs:
```

```rust
use std::{future::{ready, Ready, Future}, pin::Pin};

use actix_web::{
    dev::{forward_ready, Service, ServiceRequest, ServiceResponse, Transform},
    Error,
};

use actix_web::{web, App, HttpServer};

pub struct SayHi;

// `S` - type of the next service
// `B` - type of response's body
impl<S, B> Transform<S, ServiceRequest> for SayHi
where
    S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = Error>,
    S::Future: 'static,
    B: 'static,
{
    type Response = ServiceResponse<B>;
    type Error = Error;
    type InitError = ();
    type Transform = SayHiMiddleware<S>;
    type Future = Ready<Result<Self::Transform, Self::InitError>>;

    fn new_transform(&self, service: S) -> Self::Future {
        ready(Ok(SayHiMiddleware { service }))
    }
}

pub struct SayHiMiddleware<S> {
    /// The next service to call
    service: S,
}

// This future doesn't have the requirement of being `Send`.
// See: futures_util::future::LocalBoxFuture
type LocalBoxFuture<T> = Pin<Box<dyn Future<Output = T> + 'static>>;

// `S`: type of the wrapped service
// `B`: type of the body - try to be generic over the body where possible
impl<S, B> Service<ServiceRequest> for SayHiMiddleware<S>
where
    S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = Error>,
    S::Future: 'static,
    B: 'static,
{
    type Response = ServiceResponse<B>;
    type Error = Error;
    type Future = LocalBoxFuture<Result<Self::Response, Self::Error>>;

    // This service is ready when its next service is ready
    forward_ready!(service);

    fn call(&self, req: ServiceRequest) -> Self::Future {
        println!("Hi from start. You requested: {}", req.path());

        // A more complex middleware, could return an error or an early response here.

        let fut = self.service.call(req);

        Box::pin(async move {
            let res = fut.await?;

            println!("Hi from response");
            Ok(res)
        })
    }
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .wrap(SayHi)
            .route("/", web::get().to(|| async { "Hello, middleware!" }))
    })
    .bind(("0.0.0.0", 5000))?
    .run()
    .await      
}
```

<strong>Please note:</strong> <em>all examples have been tested 
on both Windows 10 and Ubuntu 22.10.</em>

<code>192.168.0.16</code> is the address of my Ubuntu 22.10 machine, I run tests
from my Windows 10 Pro machine.

Run <code>http://192.168.0.16:5000/</code>, we see the
following response on the browser and screen:

![091-01.png](https://behainguyen.files.wordpress.com/2023/11/091-01.png)

We can see the flow of the execution path within the different
parts of the middleware.

<em>(I'm using the same project to test completely different pieces of code,
by replacing the content of <code>main.rs</code> and the <code>[dependencies]</code>
section of <code>Cargo.toml</code>, that is why the target executable is
<code>learn-actix-web</code>.)</em>

<a id="the-second-example"></a>
❷ Integrate <code>SayHi</code> into
<a href="https://behainguyen.wordpress.com/2023/10/18/rust-web-application-mysql-server-sqlx-actix-web-and-tera/" title="Rust web application: MySQL server, sqlx, actix-web and tera" target="_blank">Rust web application: MySQL server, sqlx, actix-web and tera</a>.

🚀 We're just showing new code snippets added throughout the discussions. 
The complete source code for this post is on 
<a href="https://github.com/behai-nguyen/rust_web_01.git" title="Source code on GitHub" target="_blank">GitHub</a>.
<span style="font-weight:bold;color:blue;">It's been tagged with <code>v0.2.0</code></span>.
To download, run the command:

```
git clone -b v0.2.0 https://github.com/behai-nguyen/rust_web_01.git
```

The code also has a fair amount of documentation 
which hopefully makes the reading a bit easier.

⓵ Copy the entire <code>src/main.rs</code> in 
<a href="#the-first-example">the above example</a> to this 
project <code>src/middleware.rs</code>, then remove the following
from the new <code>src/middleware.rs</code>:

<ol>
<li style="margin-top:10px;">
The import line: <code>use actix_web::{web, App, HttpServer};</code>
</li>

<li style="margin-top:10px;">
The entire <code>fn main()</code>, starting from the line 
<code>#[actix_web::main]</code>.
</li>
</ol>

The project directory now looks like in the screenshot below:

![091-02.png](https://behainguyen.files.wordpress.com/2023/11/091-02.png)

Module <code>src/middleware.rs</code> now contains the 
stand-alone <code>SayHi</code> middleware as per in the 
official documentation. It is ready for integration into
any web project.

⓶ Initially, apply <code>SayHi</code> middleware as is
to a new application resource <code>http://0.0.0.0:5000/helloemployee</code>.

In <code>src/main.rs</code>, we need to include 
<code>src/middleware.rs</code> module, and create another
service which wraps both resource <code>/helloemployee</code>
and <code>SayHi</code> middleware.

```
Updated content of src/main.rs:
```

```rust
...
mod handlers;

mod middleware;

pub struct AppState {
...

            .service(
                web::scope("/ui")
                    .service(handlers::employees_html1)
                    .service(handlers::employees_html2),
            )
            .service(
                web::resource("/helloemployee")
                    .wrap(middleware::SayHi)
                    .route(web::get().to(|| async { "Hello, middleware!" }))
            )
...			
```

It should compile and run successfully.
All existing four (4) routes should operate as before:

🚀 <strong>And they should not trigger the <code>SayHi</code> middleware!</strong>

The new route, <code>http://0.0.0.0:5000/helloemployee</code> should run as per <a href="#the-first-example">the above example</a>:

![091-03.png](https://behainguyen.files.wordpress.com/2023/11/091-03.png)

⓷ As has been outlined above, all I'd like to do in this learning 
exercise is to get the middleware to do request path extractions, 
database query, and return some text message to the middleware 
endpoint service handler. Accordingly, the resource route changed 
to <code>/helloemployee/{last_name}/{first_name}</code>.

```
Updated content of src/main.rs:
```

```rust
...
            .service(
                web::resource("/helloemployee/{last_name}/{first_name}")
                    .wrap(middleware::SayHi)
                    .route(web::get().to(|| async { "Hello, middleware!" }))
            )
...			
```

In the middleware, <code>fn call(&self, req: ServiceRequest) -> Self::Future</code>
has new code to extract <code>last_name</code> and <code>first_name</code> from the 
path, and print them out to stdout:

```
Updated content of src/middleware.rs:
```

```rust
...
    fn call(&self, req: ServiceRequest) -> Self::Future {
        println!("Hi from start. You requested: {}", req.path());

        let last_name: String = req.match_info().get("last_name").unwrap().parse::<String>().unwrap();
        let first_name: String = req.match_info().get("first_name").unwrap().parse::<String>().unwrap();

        println!("Middleware. last name: {}, first name: {}.", last_name, first_name);

        // A more complex middleware, could return an error or an early response here.

        let fut = self.service.call(req);

        Box::pin(async move {
            let res = fut.await?;

            println!("Hi from response");
            Ok(res)
        })
    }
...	
```

When we run the updated route <code>http://192.168.0.16:5000/helloemployee/%chi/%ak</code>,
the output on the browser should stay the same. The output on the screen changes to:

```
Hi from start. You requested: /helloemployee/%chi/%ak
Middleware. last name: %chi, first name: %ak.
Hi from response
```

⓸ The next step is to query the database using the extracted
partial last name and partial first name. For that, we need to 
get access to the application state which has the database 
connection pool attached. This 
<a href="https://users.rust-lang.org/t/how-to-pass-data-to-an-actix-middleware/75262"
title="How to pass data to an actix middleware"
target="_blank">Rust language user forum post</a> has a complete
solution 😂 Accordingly, the middleware code is updated as follows:

```
Updated content of src/middleware.rs:
```

```rust
...
use actix_web::{
    dev::{forward_ready, Service, ServiceRequest, ServiceResponse, Transform},
    // New import web::Data.
    web::Data, Error,
};

use async_std::task;

use super::AppState;
use crate::models::get_employees;
...

    fn call(&self, req: ServiceRequest) -> Self::Future {
        ...
        println!("Middleware. last name: {}, first name: {}.", last_name, first_name);

        // Retrieve the application state, where the database connection object is.
        let app_state = req.app_data::<Data<AppState>>().cloned().unwrap();
        // Query the database using the partial last name and partial first name.
        let query_result = task::block_on(get_employees(&app_state.db, &last_name, &first_name));
        ...		
```

Not to bore you with so many intermediate debug steps, I just show
the final code. But to get to this, I did do debug print out over several
iterations to verify I get what I expected to get, etc. 
I also print out content of <code>query_result</code> 
to assert that I get the records I expected. (I should learn the Rust debugger!)

⓹ For the final step, which is getting the middleware to attach
a custom text message to the request, and then the middleware endpoint 
service handler extracts this message, process it further, before sending
it back the requesting client.

The principle reference for this part of the code is the 
<a href="https://github.com/actix/examples/tree/master/middleware/request-extensions" title="actix GitHub middleware request-extensions example" target="_blank">actix GitHub middleware request-extensions example</a>.
The middleware needs to formulate the message and attach it to the request via 
the extension. The final update to <code>src/middleware.rs</code>:

```
Updated content of src/middleware.rs:
```

```rust
...
use actix_web::{
    dev::{forward_ready, Service, ServiceRequest, ServiceResponse, Transform},
    // New import HttpMessage.
    web::Data, Error, HttpMessage,
};
...
#[derive(Debug, Clone)]
pub struct Msg(pub String);
...
    fn call(&self, req: ServiceRequest) -> Self::Future {
        ...
        // Attached message to request.
        req.extensions_mut().insert(Msg(hello_msg.to_owned()));
        ...		
```

For the endpoint service handler, we add a new function
<code>hi_first_employee_found</code> to <code>src/handlers.rs</code>:

```
Updated content of src/handlers.rs:
```

```rust
...
// New import web::ReqData.
use actix_web::{get, post, web, HttpRequest, HttpResponse, Responder, web::ReqData};
...
use crate::middleware::Msg;
...
pub async fn hi_first_employee_found(msg: Option<ReqData<Msg>>) -> impl Responder {
    match msg {
        None => return HttpResponse::InternalServerError().body("No message found."),

        Some(msg_data) => {
            let Msg(message) = msg_data.into_inner();

            HttpResponse::Ok()
                .content_type("text/html; charset=utf-8")
                .body(format!("&lt;h1>{}&lt;/h1>", message))    
        },
    }
}
```

To make it a bit “dynamic”, if the request extension <code>Msg</code>
is found, we wrap it in an HTML <code>h1</code> tag, and return the 
response as HTML. Otherwise, we just return an <code>HTTP 500</code> 
error code. But given the code as it is, the only way to trigger this 
error is to comment out the <code>req.extensions_mut().insert(Msg(hello_msg.to_owned()));</code>
in the middleware <code>fn call(&self, req: ServiceRequest) -> Self::Future</code> above.

The last step is to make function <code>hi_first_employee_found</code>
the middleware endpoint service handler.

```
Updated content of src/main.rs:
```

```rust
...
            .service(
                web::resource("/helloemployee/{last_name}/{first_name}")
                    .wrap(middleware::SayHi)
                    .route(web::get().to(handlers::hi_first_employee_found))
            )
...			
```

The route <code>http://192.168.0.16:5000/helloemployee/%chi/%ak</code>
should now respond:

![091-04.png](https://behainguyen.files.wordpress.com/2023/11/091-04.png)

When no employee found, e.g., route <code>http://192.168.0.16:5000/helloemployee/%xxx/%yyy</code>,
the response is:

![091-05.png](https://behainguyen.files.wordpress.com/2023/11/091-05.png)

This middleware does not do much, but it's a good learning curve for me.
I hope you find this post helpful somehow. Thank you for reading and
stay safe as always.

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
