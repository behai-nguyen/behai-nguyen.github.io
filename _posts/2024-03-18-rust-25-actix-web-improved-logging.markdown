---
layout: post
title: "Rust: Actix-web Daily Logging -- Fix Local Offset, Apply Event Filtering"

description: In the last post of our actix-web learning application, we identified two problems. First, there is an issue with calculating the UTC time offset on Ubuntu 22.10, as described in the section 💥 Issue with calculating UTC time offset on Ubuntu 22.10. Secondly, loggings from other crates that match the logging configuration are also written onto log files, as mentioned in the Concluding Remarks section. We should be able to configure what gets logged. We will address both of these issues in this post. 

tags:
- Rust
- actix-web
- daily logging
- logging
- tracing
- event
- filter
---

<em>In the <a href="https://behainguyen.wordpress.com/2024/03/13/rust-actix-web-and-daily-logging/#project-layout" title="Rust: Actix-web and Daily Logging" target="_blank">last post</a> of our <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> learning application, we identified two problems. First, there is an issue with calculating the UTC time offset on Ubuntu 22.10, as described in the section <a href="https://behainguyen.wordpress.com/2024/03/13/rust-actix-web-and-daily-logging/#utcoffset-linux-problem" title="💥 Issue with calculating UTC time offset on Ubuntu 22.10" target="_blank">💥 Issue with calculating UTC time offset on Ubuntu 22.10</a>. Secondly, loggings from other crates that match the logging configuration are also written onto log files, as mentioned in the <a href="https://behainguyen.wordpress.com/2024/03/13/rust-actix-web-and-daily-logging/#concluding-remarks" title="Concluding Remarks" target="_blank">Concluding Remarks</a> section. We should be able to configure what gets logged. We will address both of these issues in this post.</em>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rust_web_01" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![102-feature-image.png](https://behainguyen.files.wordpress.com/2024/03/102-feature-image.png) |
|:--:|
| *Rust: Actix-web Daily Logging -- Fix Local Offset, Apply Event Filtering* |


🚀 <strong>Please note,</strong> complete code for this post can be downloaded from GitHub with:

```
git clone -b v0.12.0 https://github.com/behai-nguyen/rust_web_01.git
```

The <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> learning application mentioned above has been discussed in the eleven previous posts. The index of the complete series <a href="https://github.com/behai-nguyen/rust_web_01" title="Index of the Complete Series" target="_blank">can be found here</a>.

The code we're developing in this post is a continuation of the code from the <a href="https://behainguyen.wordpress.com/2024/03/13/rust-actix-web-and-daily-logging/#project-layout" title="Rust: Actix-web and Daily Logging" target="_blank">eleventh</a> post. 🚀 To get the code of this <a href="https://behainguyen.wordpress.com/2024/03/13/rust-actix-web-and-daily-logging/#project-layout" title="Rust: Actix-web and Daily Logging" target="_blank">eleventh</a> post, please use the following command:

```
git clone -b v0.11.0 https://github.com/behai-nguyen/rust_web_01.git
```

<strong>-- Note the tag <code>v0.11.0</code>.</strong>

While this post continues from previous posts in this series, it can be read in conjunction with only the <a href="https://behainguyen.wordpress.com/2024/03/13/rust-actix-web-and-daily-logging/#project-layout" title="Rust: Actix-web and Daily Logging" target="_blank">eleventh</a> post.

<a id="project-layout"></a>
❶ For this post, no new modules are introduced. Instead, we will update some existing modules and files. The layout chart below shows the updated files and modules, with those marked with <span style="font-size:1.5em;">★</span> indicating the updated ones.

<a id="project-layout-chart"></a>
```
.
├── .env ★
├── Cargo.toml ★
├── ...
├── README.md ★
├── src
│ ├── helper
│ │ ├── app_logger.rs ★
│ │ └── ...
│ ├── main.rs ★
│ └── ...
└── tests
    ├── common.rs ★
    └── ...
```

🦀 In the context of this post, our focus is solely on the <code>RUST_LOG</code> entry in the <code>.env</code> file, which we will discuss in a <a href="#logging-event-filter-rust-log-env-var">later section</a>.

<a id="the-cargo-file"></a>
❷ Updates to the <a href="https://github.com/behai-nguyen/rust_web_01/blob/ded522aa79c0a5f82200dce585e1dad164918bd4/Cargo.toml" title="The Cargo.toml file" target="_blank">Cargo.toml</a> file:

```
...
[dependencies]
...
time-tz = {version = "2.0", features = ["system"]}
tracing-subscriber = {version = "0.3", features = ["fmt", "std", "local-time", "time", "env-filter"]}
```

We added the new crate <a href="https://docs.rs/time-tz/2.0.0/time_tz/" title="time-tz" target="_blank">time-tz</a>, and for <a href="https://docs.rs/tracing-subscriber/latest/tracing_subscriber/index.html" title="tracing-subscriber" target="_blank">tracing-subscriber</a>, we added the crate feature <code>env-filter</code>. We will discuss these additions in later sections.

<a id="utc-time-offset"></a>
❸ Resolve the issue with calculating the UTC time offset to ensure reliable functionality on both Ubuntu 22.10 and Windows 10.

⓵ As <a href="https://behainguyen.wordpress.com/2024/03/13/rust-actix-web-and-daily-logging/#utcoffset-linux-problem" title="💥 Issue with calculating UTC time offset on Ubuntu 22.10" target="_blank">mentioned</a> in the last post:

> After extensive searching, I came across this GitHub issue, <a href="https://github.com/time-rs/time/pull/297" title="Document #293 in local-offset feature description #297" target="_blank">Document #293 in local-offset feature description #297</a>. <em>It appears that even after three years, this issue remains unresolved.</em>

<code>Document #293</code> is dated December 19, 2020. Additionally, there are other relevant documents that I did not come across during my previous “extensive searching”:

<ol>
<li style="margin-top:10px;">
November 25, 2020 -- <a href="https://github.com/time-rs/time/issues/296" title="Time 0.2.23 fails to determine local offset #296" target="_blank">Time 0.2.23 fails to determine local offset #296</a>.
</li>
<li style="margin-top:10px;">
November 2, 2021 -- <a href="https://github.com/time-rs/time/issues/380" title="Better solution for getting local offset on unix #380" target="_blank">Better solution for getting local offset on unix #380</a>.
</li>
<li style="margin-top:10px;">
Dec 5, 2019 -- <a href="https://github.com/time-rs/time/issues/193" title="tzdb support #193" target="_blank">tzdb support #193</a>.
</li>
</ol>

<a href="https://github.com/time-rs/time/issues/193#issuecomment-1037227056" title="This reply"target="_blank">This reply</a> posted on February 13, 2022 mentions the crate <a href="https://crates.io/crates/time-tz" title="time-tz" target="_blank">time-tz</a>, which resolves the previously mentioned issue.

The parameter <code>utc_offset: time::UtcOffset</code> was removed from the function <a href="https://github.com/behai-nguyen/rust_web_01/blob/ded522aa79c0a5f82200dce585e1dad164918bd4/src/helper/app_logger.rs#L38" title="src/helper/app_logger.rs pub fn init_app_logger() -&gt; WorkerGuard" target="_blank">pub fn init_app_logger() -> WorkerGuard</a>, and the offset calculation is now carried out internally:

```rust
    let timer = OffsetTime::new(
        localtime.offset(),
        format_description!("[year]-[month]-[day] [hour]:[minute]:[second]"),
    );
```

⓶ Offset calculations were accordingly removed from both the function <a href="https://github.com/behai-nguyen/rust_web_01/blob/ded522aa79c0a5f82200dce585e1dad164918bd4/src/main.rs#L10" title="src/main.rs async fn main() -&gt; Result&lt;(), std::io::Error&gt;" target="_blank">async fn main() -> Result&lt;(), std::io::Error></a> in the module <a href="https://github.com/behai-nguyen/rust_web_01/blob/ded522aa79c0a5f82200dce585e1dad164918bd4/src/main.rs" title="src/main.rs" target="_blank">src/main.rs</a>, and the function <a href="https://github.com/behai-nguyen/rust_web_01/blob/ded522aa79c0a5f82200dce585e1dad164918bd4/tests/common.rs#L56" title="tests/common.rs function pub async fn spawn_app() -&gt; TestApp" target="_blank">pub async fn spawn_app() -> TestApp</a> in the module <a href="https://github.com/behai-nguyen/rust_web_01/blob/ded522aa79c0a5f82200dce585e1dad164918bd4/tests/common.rs" title="tests/common.rs" target="_blank">tests/common.rs</a>.

<a id="logging-event-filter"></a>
❸ Configuration to determine what get logged.

We use <code>tracing_subscriber</code>'s <a href="https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html" title="Struct tracing_subscriber::filter::EnvFilter" target="_blank">filter::EnvFilter</a> struct to filter which events are logged. This functionality requires the crate feature <code>env-filter</code>, as <a href="#the-cargo-file">described</a> above.

Event filtering is configured via the environment variable <code>RUST_LOG</code>. Its value can be much more sophisticated than simply <code>trace</code>, <code>debug</code>, <code>info</code>, <code>warn</code> and <code>error</code>. The documentation in the section <a href="https://docs.rs/env_logger/latest/env_logger/#enabling-logging" title="Enabling logging" target="_blank">Enabling logging</a> of the <code>env_logger</code> crate describes the syntax of <code>RUST_LOG</code> with plenty of informative examples.

<a id="logging-event-filter-code-refactorings"></a>
⓵ Implementing event filtering for the function <a href="https://github.com/behai-nguyen/rust_web_01/blob/ded522aa79c0a5f82200dce585e1dad164918bd4/src/helper/app_logger.rs#L110" title="src/helper/app_logger.rs pub fn init_app_logger() -&gt; WorkerGuard" target="_blank">pub fn init_app_logger() -> WorkerGuard</a>:

```rust
    let filter_layer = EnvFilter::try_from_default_env()
        .or_else(|_| EnvFilter::try_new("debug"))
        .unwrap();

    let subscriber = tracing_subscriber::registry()
        .with(
            ...
                .with_filter(filter_layer)
        );
```

Please note that the code to convert the value of <code>RUST_LOG</code> to <a href="https://docs.rs/tracing/latest/tracing/struct.Level.html" title="tracing::Level" target="_blank">tracing::Level</a> has also been removed.

For further documentation, please refer to <a href="https://docs.rs/tracing-subscriber/latest/tracing_subscriber/fmt/index.html#filtering-events-with-environment-variables" title="Filtering Events with Environment Variables" target="_blank">Filtering Events with Environment Variables</a>. The code above is from the section <a href="https://docs.rs/tracing-subscriber/latest/tracing_subscriber/fmt/index.html#composing-layers" title="Composing Layers" target="_blank">Composing Layers</a> of the mentioned documentation page. As for the two functions being called, please see:

● <a href="https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#method.try_from_default_env" title="pub fn try_from_default_env() -&gt; Result&lt;Self, FromEnvError&gt;" target="_blank">pub fn try_from_default_env() -> Result&lt;Self, FromEnvError></a>.

● <a href="https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#method.try_new" title="pub fn try_new&lt;S: AsRef&lt;str&gt;&gt;(dirs: S) -&gt; Result&lt;Self, ParseError&gt;" target="_blank">pub fn try_new&lt;S: AsRef&lt;str>>(dirs: S) -> Result&lt;Self, ParseError></a>.

<p>
And finally, the line:
</p>

```rust
            ...
                .with_filter(filter_layer)
```

is from the trait <a href="https://docs.rs/tracing-subscriber/latest/tracing_subscriber/layer/trait.Layer.html" title="Trait tracing_subscriber::layer::Layer" target="_blank">tracing_subscriber::layer::Layer</a>, which is a “a composable handler for <code>tracing</code> events.”

<a id="logging-event-filter-rust-log-env-var"></a>
⓶ As for the value of <code>RUST_LOG</code>, there are three cases that do not behave as I initially assumed:

The first two cases are <code>RUST_LOG=xxxx</code> and <code>RUST_LOG=</code>, <strong>where nothing gets logged.</strong> I had assumed that this error handling would default the logging event to <code>debug</code>:

```rust
        .or_else(|_| EnvFilter::try_new("debug"))
```

I attempted several times to default them to <code>debug</code>, but unfortunately, I was unsuccessful.

The third case is <code>RUST_LOG</code>, where only the <code>RUST_LOG</code> variable name is present in the <code>.env</code> file without any value assigned to it. Based on the above two instances, I expected that nothing would be logged. However, it defaults to <code>debug</code>!

Please note that for the next example discussion, it's important to keep in mind that the <a href="https://github.com/behai-nguyen/rust_web_01/blob/ded522aa79c0a5f82200dce585e1dad164918bd4/Cargo.toml#L11" title="The Cargo.toml file" target="_blank">Cargo.toml</a> file contains the following declaration, where <code>learn_actix_web</code> is defined: 

```toml
[[bin]]
path = "src/main.rs"
name = "learn_actix_web"
```

Examples of some valid values:

<ol>
<li style="margin-top:10px;">
<code>RUST_LOG=off,learn_actix_web=debug</code> -- Only <code>debug</code> logging events from the <code>learn_actix_web</code> crate are logged. All logging events from other crates are ignored.
</li>
<li style="margin-top:10px;">
<code>RUST_LOG=off,learn_actix_web=info</code> -- Only <code>info</code> logging events from the application are logged. If there are no <code>info</code> events in the application, nothing gets logged and the log files remain empty.
</li>
<li style="margin-top:10px;">
<code>RUST_LOG=off,learn_actix_web=debug,actix_server=info</code> -- Only <code>debug</code> events from the application and <code>info</code> events from the <code>actix_server</code> crate are logged.
</li>
<li style="margin-top:10px;">
<code>RUST_LOG=off,learn_actix_web::middleware=debug</code> -- Only <code>debug</code> events from the <a href="https://github.com/behai-nguyen/rust_web_01/blob/d0005d87b4df15c775daa5167da3fc07c6935f59/src/middleware.rs" title="src/middleware.rs" target="_blank">src/middleware.rs</a> module of the application are logged. This middleware is triggered when accessing the <code>GET</code> route <code>http://0.0.0.0:5000/helloemployee/{partial last name}/{partial first name}</code> from an <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-authenticated-session" title="authenticated session" target="_blank"><code>authenticated session</code></a>.
</li>
</ol>

A further illustration for example 4 above: Log in and click on the last button as shown in the screenshot below:

https://behainguyen.files.wordpress.com/2024/03/102-01.png

The current log file should contain the following three new lines:

```
2024-03-18 00:51:15 DEBUG learn_actix_web::middleware: Hi from start. You requested: /helloemployee/%chi/%ak
2024-03-18 00:51:15 DEBUG learn_actix_web::middleware: Middleware. last name: %chi, first name: %ak.
2024-03-18 00:51:15 DEBUG learn_actix_web::middleware: Hi from response -- some employees found.
```

This finer control demonstrates the power, utility, and helpfulness of tracking an intermittent bug that is not reproducible on staging and development environments. By enabling debug and tracing logging for specific modules, we can effectively troubleshoot such issues.

<a id="unique-web-ssession-id"></a>
❹ Logging events should be grouped within the unique ID of the <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-authenticated-session" title="authenticated session" target="_blank"><code>authenticated session</code></a>.

For each <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-authenticated-session" title="authenticated session" target="_blank"><code>authenticated session</code></a>, there is a third-party <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#notes-on-cookies-third-party" title="actix-sesion id" target="_blank">session ID</a>. I have conducted some studies on this cookie, and its value seems to change after each request. For further discussion of this <code>ID</code> under <code>HTTPS</code>, please refer to this <a href="https://behainguyen.wordpress.com/2024/02/13/rust-actix-web-cors-cookies-and-ajax-calls/#cookies-ajax-https" title="actix-sesion id updated" target="_blank">discussion</a>.

My initial plan is to group logging for each request under the value of this <code>ID</code>. For example:

```
** 2024-03-18 00:51:15 DEBUG learn_actix_web::middleware: {value of id} entered.
2024-03-18 00:51:15 DEBUG learn_actix_web::middleware: Hi from start. You requested: /helloemployee/%chi/%ak
...
** 2024-03-18 00:51:15 DEBUG learn_actix_web::middleware: {value of id} exited.
```

I have not yet determined how to achieve this; further study is required.

<a id="concluding-remarks"></a>
❺ We have concluded this post. I'm pleased to have resolved the offset issue and to have implemented logging in a more effective manner.

I hope you find the information useful. Thank you for reading. And stay safe, as always.

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
