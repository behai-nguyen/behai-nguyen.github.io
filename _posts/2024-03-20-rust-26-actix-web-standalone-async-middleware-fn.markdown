---
layout: post
title: "Rust: Actix-web -- Async Functions as Middlewares"

description: In the tenth post of our actix-web learning application, we added an ad hoc middleware. In this post, with the assistance of the actix-web-lab crate, we will refactor this ad hoc middleware into a standalone async function to enhance the overall code readability. 

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.files.wordpress.com/2024/03/103-01.png"

gallery-image-list-2:
    - "https://behainguyen.files.wordpress.com/2024/03/103-02.png"

tags:
- Rust
- actix-web
- async function middleware
- middleware
---

<em>In the <a href="https://behainguyen.wordpress.com/2024/02/26/rust-actix-web-json-web-token-authentication/" title="Rust: actix-web JSON Web Token authentication" target="_blank">tenth</a> post of our <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> learning application, we added an ad hoc middleware. In this post, with the assistance of the <a href="https://docs.rs/actix-web-lab/latest/actix_web_lab/index.html" title="actix-web-lab" target="_blank">actix-web-lab</a> crate, we will refactor this ad hoc middleware into a standalone <code>async</code> function to enhance the overall code readability.</em>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rust_web_01" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![103-feature-image.png](https://behainguyen.files.wordpress.com/2024/03/103-feature-image.png) |
|:--:|
| *Rust: Actix-web -- Async Functions as Middlewares* |

<p>
🚀 <strong>Please note,</strong> complete code for this post
can be downloaded from GitHub with:
</p>

```
git clone -b v0.13.0 https://github.com/behai-nguyen/rust_web_01.git
```

The <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> learning application mentioned above has been discussed in the twelve previous posts. The index of the complete series <a href="https://github.com/behai-nguyen/rust_web_01" title="Index of the Complete Series" target="_blank">can be found here</a>.

The code we're developing in this post is a continuation of the code from the <a href="https://behainguyen.wordpress.com/2024/03/18/rust-actix-web-daily-logging-fix-local-offset-apply-event-filtering/" title="Rust: Actix-web Daily Logging -- Fix Local Offset, Apply Event Filtering" target="_blank">twelfth</a> post. 🚀 To get the code of this <a href="https://behainguyen.wordpress.com/2024/03/18/rust-actix-web-daily-logging-fix-local-offset-apply-event-filtering/" title="Rust: Actix-web Daily Logging -- Fix Local Offset, Apply Event Filtering" target="_blank">twelfth</a> post, please use the following command:

```
git clone -b v0.12.0 https://github.com/behai-nguyen/rust_web_01.git
```

<strong>-- Note the tag <code>v0.12.0</code>.</strong>

While this post continues from previous posts in this series, it can be read in conjunction with only the <a href="https://behainguyen.wordpress.com/2024/02/26/rust-actix-web-json-web-token-authentication/" title="Rust: actix-web JSON Web Token authentication" target="_blank">tenth</a> post, focusing particularly on the section titled <a href="https://behainguyen.wordpress.com/2024/02/26/rust-actix-web-json-web-token-authentication/#updated-request-auth-process-lib" title="Code Updated in the src/lib.rs Module" target="_blank">Code Updated in the src/lib.rs Module</a>.

<a id="project-layout"></a>
❶ For this post, no new modules are introduced. Instead, we will update existing modules and files. The layout chart below displays the updated files and modules, with those marked with <span style="font-size:1.5em;">★</span> indicating the ones that have been updated.

<a id="project-layout-chart"></a>
```
.
├── Cargo.toml ★
├── ...
├── README.md ★
└── src
  ├── lib.rs ★
  └── ...
```

<a id="the-cargo-file"></a>
❷ An update to the <a href="https://github.com/behai-nguyen/rust_web_01/blob/d22804332a55c683dbc272d66fa829c478681ea7/Cargo.toml#L24" title="The Cargo.toml file" target="_blank">Cargo.toml</a> file:

```toml
...
[dependencies]
...
actix-web-lab = "0.20.2"
```

We added the new crate <a href="https://docs.rs/actix-web-lab/latest/actix_web_lab/index.html" title="actix-web-lab" target="_blank">actix-web-lab</a>. This crate is:

> In-progress extractors and middleware for Actix Web.

This crate provides mechanisms for implementing middlewares as standalone <code>async</code> functions, rather than using <code>actix-web</code>'s <a href="https://docs.rs/actix-web/latest/actix_web/struct.App.html#method.wrap_fn" title="wrap_fn function" target="_blank">wrap_fn</a>.

According to the documentation, the <a href="https://docs.rs/actix-web-lab/latest/actix_web_lab/index.html" title="actix-web-lab" target="_blank">actix-web-lab</a> crate is essentially experimental. Functionalities implemented in this crate might eventually be integrated into the <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> crate. In such a case, we would need to update our code.

<a id="refactor-middleware-out-of-wrap-fn"></a>
❸ Refactor an existing ad hoc middleware out of <a href="https://docs.rs/actix-web/latest/actix_web/struct.App.html#method.wrap_fn" title="wrap_fn function" target="_blank">wrap_fn</a>. 

As mentioned at the beginning, this post should be read in conjunction with the <a href="https://behainguyen.wordpress.com/2024/02/26/rust-actix-web-json-web-token-authentication/" title="Rust: actix-web JSON Web Token authentication" target="_blank">tenth</a> post, where we introduced this <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/lib.rs#L156" title="src/lib.rs token forwarding ad hoc middleware" target="_blank">ad hoc middleware</a>. The description of this simple middleware functionality is found in the section <a href="https://behainguyen.wordpress.com/2024/02/26/rust-actix-web-json-web-token-authentication/#updated-request-auth-process-lib" title="Code Updated in the src/lib.rs Module" target="_blank">Code Updated in the src/lib.rs Module</a> of the tenth post.

Below, we reprint the code of this ad hoc middleware:

```rust
            //
            // This ad hoc middleware looks for the updated access token String attachment in 
            // the request extension, if there is one, extracts it and sends it to the client 
            // via both the ``authorization`` header and cookie.
            //
            .wrap_fn(|req, srv| {
                let mut updated_access_token: Option<String> = None;

                // Get set in src/auth_middleware.rs's 
                // fn update_and_set_updated_token(request: &ServiceRequest, token_status: TokenStatus).
                if let Some(token) = req.extensions_mut().get::<String>() {
                    updated_access_token = Some(token.to_string());
                }

                srv.call(req).map(move |mut res| {

                    if updated_access_token.is_some() {
                        let token = updated_access_token.unwrap();
                        res.as_mut().unwrap().headers_mut().append(
                            header::AUTHORIZATION, 
                            header::HeaderValue::from_str(token.as_str()).expect(TOKEN_STR_JWT_MSG)
                        );

                        let _ = res.as_mut().unwrap().response_mut().add_cookie(
                            &build_authorization_cookie(&token));
                    };

                    res
                })
            })
```

It's not particularly lengthy, but its inclusion in the application instance construction process makes it difficult to read. While <a href="https://doc.rust-lang.org/book/ch13-01-closures.html" title="closures" target="_blank">closures</a> can call <a href="https://doc.rust-lang.org/book/ch03-03-how-functions-work.html" title="functions" target="_blank">functions</a>, refactoring this implementation into a standalone function isn't feasible. This is because the function would require access to the parameter <code>srv</code>, which in this case refers to the <a href="https://github.com/actix/actix-web/blob/0383f4bdd1210e726143ca1ebcf01169b67a4b6c/actix-web/src/app_service.rs#L294" title="AppRouting struct" target="_blank">AppRouting</a> struct. Please refer to the screenshot below for clarification:

{% include image-gallery.html list=page.gallery-image-list-1 %}
<br/>

The <code>AppRouting</code> struct is located in the private module <a href="https://github.com/actix/actix-web/blob/0383f4bdd1210e726143ca1ebcf01169b67a4b6c/actix-web/src/app_service.rs" title="actix-web/src/app_service.rs" target="_blank">actix-web/src/app_service.rs</a>, which means we don't have direct access to it. I attempted to refactor it into a standalone function but encountered difficulties. Someone else had also attempted it before me and faced similar issues.

Please refer to the GitHub issue titled <a href="https://github.com/actix/actix-web/issues/2681" title="wrap_fn &AppRouting should use Arc&lt;AppRouting&gt; #2681" target="_blank">wrap_fn &AppRouting should use Arc&lt;AppRouting> #2681</a> for more details. <a href="https://github.com/actix/actix-web/issues/2681#issuecomment-1059769414" title="This reply" target="_blank">This reply</a> suggests using the <a href="https://docs.rs/actix-web-lab/latest/actix_web_lab/index.html" title="actix-web-lab" target="_blank">actix-web-lab</a> crate. 

I believe I've come across this crate before, particularly the function <a href="https://docs.rs/actix-web-lab/latest/actix_web_lab/middleware/fn.from_fn.html" title="Function actix_web_lab::middleware::from_fn" target="_blank">actix_web_lab::middleware::from_fn</a>, but it didn't register with me at the time.

Drawing from the official example <a href="https://github.com/robjtede/actix-web-lab/blob/7f5ce616f063b0735fb423a441de7da872847c5c/actix-web-lab/examples/from_fn.rs" title="actix-web-lab/actix-web-lab/examples/from_fn.rs" target="_blank">actix-web-lab/actix-web-lab/examples/from_fn.rs</a> and compiler suggestions, I've successfully refactored the ad hoc middleware mentioned above into the standalone async function <a href="https://github.com/behai-nguyen/rust_web_01/blob/d22804332a55c683dbc272d66fa829c478681ea7/src/lib.rs#L143" title="src/lib.rs async fn update_return_jwt&lt;B&gt;(req: ServiceRequest, next: Next&lt;B&gt;) -&gt; Result&lt;ServiceResponse&lt;B&gt;, Error&gt;" target="_blank">async fn update_return_jwt&lt;B>(req: ServiceRequest, next: Next&lt;B>) -> Result&lt;ServiceResponse&lt;B>, Error></a>. The screenshot below, taken from Visual Studio Code with the <a href="https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer" title="the Rust-Analyzer" target="_blank">Rust-Analyzer</a> plugin, displays the full source code and variable types:

{% include image-gallery.html list=page.gallery-image-list-2 %}
<br/>

Compared to the original ad hoc middleware, the code is virtually unchanged. It's worth noting that this final version is the result of my sixth or seventh attempt; without the compiler suggestions, I would not have been able to complete it. We register it with the application instance using only a <a href="https://github.com/behai-nguyen/rust_web_01/blob/d22804332a55c683dbc272d66fa829c478681ea7/src/lib.rs#L202" title="src/lib.rs register async function update_return_jwt as a middleware" target="_blank">single line</a>, as per the documentation:

```rust
            .wrap(from_fn(update_return_jwt))
```

<a id="other-minor-refactorings"></a>
❹ Other minor refactorings include optimising the application instance builder code for brevity. Specifically, I've moved the code to create the CORS instance to the standalone function <a href="https://github.com/behai-nguyen/rust_web_01/blob/d22804332a55c683dbc272d66fa829c478681ea7/src/lib.rs#L47" title="src/lib.rs fn cors_config(config: &config::Config) -&gt; Cors" target="_blank">fn cors_config(config: &config::Config) -> Cors</a>, and the code to create the session store to the standalone async function <a href="https://github.com/behai-nguyen/rust_web_01/blob/d22804332a55c683dbc272d66fa829c478681ea7/src/lib.rs#L62" title="src/lib.rs async fn config_session_store() -&gt; (actix_web::cookie::Key, RedisSessionStore)" target="_blank">async fn config_session_store() -> (actix_web::cookie::Key, RedisSessionStore)</a>.

Currently, the <a href="https://github.com/behai-nguyen/rust_web_01/blob/d22804332a55c683dbc272d66fa829c478681ea7/src/lib.rs" title="src/lib.rs" target="_blank">src/lib.rs</a> module is less than 250 lines long, housing 7 helper functions that are completely unrelated. I find it still very manageable. The code responsible for creating the server instance and the application instance, encapsulated in the function <a href="https://github.com/behai-nguyen/rust_web_01/blob/d22804332a55c683dbc272d66fa829c478681ea7/src/lib.rs#L179" title="src/lib.rs pub async fn run(listener: TcpListener) -&gt; Result&lt;Server, std::io::Error&gt;" target="_blank">pub async fn run(listener: TcpListener) -> Result&lt;Server, std::io::Error></a>, remains around 60 lines. Although I anticipate it will grow a bit more as we add more functionalities, I don't foresee it becoming overly lengthy.

<a id="concluding-remarks"></a>
❺ I am happy to have learned something new about <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a>. And I hope you find the information useful. Thank you for reading. And stay safe, as always.

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
