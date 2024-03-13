---
layout: post
title: "Rust: Actix-web and Daily Logging"

description: Currently, our actix-web learning application simply prints debug information to the console using the println! macro. In this post, we will implement proper non-blocking daily logging to files. Daily logging entails rotating to a new log file each day. Non-blocking refers to having a dedicated thread for file writing operations. We will utilise the tracing, tracing-appender, and tracing-subscriber crates for our logging implementation. 

tags:
- Rust
- actix-web
- daily logging
- logging
- tracing
---

<em>Currently, our <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> learning application simply prints debug information to the console using the <code>println!</code> macro. In this post, we will implement proper non-blocking daily logging to files. <code>Daily logging</code> entails rotating to a new log file each day. <code>Non-blocking</code> refers to having a dedicated thread for file writing operations. We will utilise the <a href="https://docs.rs/tracing/latest/tracing/index.html" title="tracing" target="_blank">tracing</a>, <a href="https://docs.rs/tracing-appender/latest/tracing_appender/index.html" title="tracing-appender" target="_blank">tracing-appender</a>, and <a href="https://docs.rs/tracing-subscriber/latest/tracing_subscriber/index.html" title="tracing-subscriber" target="_blank">tracing-subscriber</a> crates for our logging implementation.</em>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rust_web_01" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![101-feature-image.png](https://behainguyen.files.wordpress.com/2024/03/101-feature-image.png) |
|:--:|
| *Rust: Actix-web and Daily Logging* |

🚀 <strong>Please note,</strong> complete code for this post can be downloaded from GitHub with: 

```
git clone -b v0.11.0 https://github.com/behai-nguyen/rust_web_01.git
```

The <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> learning application mentioned above has been discussed in the following ten previous posts:

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
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/02/26/rust-actix-web-json-web-token-authentication/" title="Rust: actix-web JSON Web Token authentication" target="_blank">Rust: actix-web JSON Web Token authentication</a>.</li>
</ol>

The code we're developing in this post is a continuation of the code from the <a href="https://behainguyen.wordpress.com/2024/02/26/rust-actix-web-json-web-token-authentication/" title="Rust: actix-web JSON Web Token authentication" target="_blank">tenth</a> post above. 🚀 To get the code of this <a href="https://behainguyen.wordpress.com/2024/02/26/rust-actix-web-json-web-token-authentication/" title="Rust: actix-web JSON Web Token authentication" target="_blank">tenth</a> post, please use the following command:

```
git clone -b v0.10.0 https://github.com/behai-nguyen/rust_web_01.git
```

<strong>-- Note the tag <code>v0.10.0</code>.</strong>

While this post continues from previous posts in this series, it can also be read independently. The logging module developed herein can be used in other projects without modification.

<a id="project-layout"></a>
❶ For this post, we introduce a new module <code>src/helper/app_logger.rs</code>, and some other modules and files are updated. The project layout remains the same as in the <a href="https://behainguyen.wordpress.com/2024/02/26/rust-actix-web-json-web-token-authentication/#project-layout" title="Rust: actix-web JSON Web Token authentication Project Layout" target="_blank">last post</a>. The layout chart below shows the affected files and modules: 

<strong>-- Please note that</strong> files marked with <span style="font-size:1.5em;">★</span> are updated, and <code>src/helper/app_logger.rs</code> is marked with <span style="font-size:1.5em;">☆</span>, as it is the only new module.

<a id="project-layout-chart"></a>
```
.
├── .env ★
├── Cargo.toml ★
├── ...
├── README.md ★
├── src
│ ├── auth_middleware.rs ★
│ ├── database.rs ★
│ ├── helper
│ │ ├── app_logger.rs ☆
│ │ └── ...
│ ├── helper.rs ★
│ ├── main.rs ★
│ ├── middleware.rs ★
│ └── ...
└── tests
    ├── common.rs ★
    └── ...
```

<a id="the-env-file"></a>
❷ An update to the <a href="https://github.com/behai-nguyen/rust_web_01/blob/d0005d87b4df15c775daa5167da3fc07c6935f59/.env#L12" title="The .env file" target="_blank">.env</a> file: a new entry has been added:

```ini
RUST_LOG=debug
```

The value of <code>RUST_LOG</code> is translated into <a href="https://docs.rs/tracing/latest/tracing/struct.Level.html" title="tracing::Level" target="_blank">tracing::Level</a>. Valid values include <code>trace</code>, <code>debug</code>, <code>info</code>, <code>warn</code> and <code>error</code>. Any other values are invalid and will default to <a href="https://docs.rs/tracing/latest/tracing/struct.Level.html#associatedconstant.DEBUG" title="Level::DEBUG" target="_blank">Level::DEBUG</a>.

<a id="the-cargo-file"></a>
❸ Updates to the <a href="https://github.com/behai-nguyen/rust_web_01/blob/d0005d87b4df15c775daa5167da3fc07c6935f59/Cargo.toml#L38" title="The Cargo.toml file" target="_blank">Cargo.toml</a> file: as expected, the new crates are added to the <code>[dependencies]</code> section.

```toml
...
[dependencies]
...
tracing = "0.1"
tracing-appender = "0.2"
tracing-subscriber = {version = "0.3", features = ["fmt", "std", "local-time", "time"]}
```

<a id="utcoffset-linux-problem"></a>
❹ 💥 Issue with calculating UTC time offset on Ubuntu 22.10.

In the new code added for this post, we need to calculate the UTC time offset to obtain local time. The following code works on Windows 10:

```rust
use time::UtcOffset;

let offset = UtcOffset::current_local_offset().unwrap();
```

However, on Ubuntu 22.10, it doesn't always function as expected. Sometimes, it raises the error <a href="https://docs.rs/time/latest/time/error/struct.IndeterminateOffset.html" title="IndeterminateOffset" target="_blank">IndeterminateOffset</a>. The inconsistency in its behavior makes it challenging to identify a clear pattern of when it works and when it doesn't.

After extensive searching, I came across this GitHub issue, <a href="https://github.com/time-rs/time/pull/297" title="Document #293 in local-offset feature description #297" target="_blank">Document #293 in local-offset feature description #297</a>. <em>It appears that even after three years, this issue remains unresolved.</em>

This complication adds an extra layer of difficulty in ensuring both the code and integration tests function properly. In the subsequent sections of this post, when discussing the code, we'll refer back to this issue when relevant. Please keep this in mind.

<a id="the-app-logger-module"></a>
❺ The <a href="https://github.com/behai-nguyen/rust_web_01/blob/d0005d87b4df15c775daa5167da3fc07c6935f59/src/helper/app_logger.rs" title="src/helper/app_logger.rs" target="_blank">src/helper/app_logger.rs</a> module has been designed to be easily copied into other projects, provided that the <code>Cargo.toml</code> file includes the required crates <a href="#the-cargo-file">discussed earlier</a>.

This module contains only a single public function, <code>pub fn init_app_logger(utc_offset: time::UtcOffset) -> WorkerGuard</code>, which the application calls to set up the log. Please refer to the notes and documentation within this module while reading the code.

Originally, the <code>utc_offset: time::UtcOffset</code> parameter was not present. However, due to the issue mentioned in <a href="#utcoffset-linux-problem">💥 Issue with calculating UTC time offset on Ubuntu 22.10</a>, the code was refactored to include this parameter, offering a bit more flexibility.

<a id="the-app-logger-module-log-file"></a>
⓵ Setting up the daily log files.

```rust
    let log_appender = RollingFileAppender::builder()
        .rotation(Rotation::DAILY) // Daily log file.
        .filename_suffix("log") // log file names will be suffixed with `.log`
        .build("./log") // try to build an appender that stores log files in `/var/log`
        .expect("Initialising rolling file appender failed");
```

To set up the daily log files, we begin by calling the <a href="https://docs.rs/tracing-appender/latest/tracing_appender/rolling/struct.RollingFileAppender.html#method.builder" title="pub fn builder() -&gt; Builder" target="_blank">pub fn builder() -> Builder</a> function.

We specify <a href="https://docs.rs/tracing-appender/latest/tracing_appender/rolling/struct.Rotation.html#daily-rotation" title="DAILY rotation" target="_blank">DAILY</a> rotation to generate daily log files. However, it's important to note that according to <a href="https://docs.rs/tracing-appender/latest/tracing_appender/rolling/fn.daily.html" title="Function tracing_appender::rolling::daily" target="_blank">the documentation</a>, the file names are appended with the current date in UTC. Since I'm in the Australian Eastern Standard Time (AEST) zone, which is 10-11 hours ahead of UTC, there were instances where my log file names were created with dates from the previous day.

To give log files the <code>.log</code> extension, we use the method <a href="https://docs.rs/tracing-appender/latest/tracing_appender/rolling/struct.Builder.html#method.filename_suffix" title="pub fn filename_suffix(self, suffix: impl Into&lt;String&gt) -&gt; Self" target="_blank">pub fn filename_suffix(self, suffix: impl Into&lt;String>) -> Self</a>.

The format of the daily log file names follows the pattern <code>YYYY-MM-DD.log</code>, for example, <code>2024-03-10.log</code>.

We then invoke the method <a href="https://docs.rs/tracing-appender/latest/tracing_appender/rolling/struct.Builder.html#method.build" title="pub fn build(&self, directory: impl AsRef&lt;Path&gt) -&gt Result&lt;RollingFileAppender, InitError&gt" target="_blank">pub fn build( &self, directory: impl AsRef&lt;Path>) -> Result&lt;RollingFileAppender, InitError></a> to specify the location of the log files within the <code>log/</code> sub-directory relative to where the application is executed. For instance:

```
▶️<code>Windows 10:</code> F:\rust\actix_web>target\debug\learn_actix_web.exe
▶️<code>Ubuntu 22.10:</code> behai@hp-pavilion-15:~/rust/actix_web$ /home/behai/rust/actix_web/target/debug/learn_actix_web
```

This results in the log files being stored at <code>F:\rust\actix_web\log\</code> and <code>/home/behai/rust/actix_web/target/debug/learn_actix_web/log/</code> respectively.

<a id="the-app-logger-module-non-blocking-writer"></a>
⓶ We create a non-blocking writer thread using the following code: 

```rust
    let (non_blocking_appender, log_guard) = tracing_appender::non_blocking(log_appender);
```

This is the documentation section for the function <a href="https://docs.rs/tracing-appender/latest/tracing_appender/fn.non_blocking.html" title="Function tracing_appender::non_blocking" target="_blank">tracing_appender::non_blocking</a>. For more detailed documentation, refer to the <a href="https://docs.rs/tracing-appender/latest/tracing_appender/non_blocking/index.html" title="Module tracing_appender::non_blocking" target="_blank">tracing_appender::non_blocking</a> module. Please note the following: 

<a id="the-app-logger-module-log-guard"></a>
> This function returns a tuple of <code>NonBlocking</code> and <code>WorkerGuard</code>. <code>NonBlocking</code> implements <a href="https://docs.rs/tracing-subscriber/0.3.18/x86_64-unknown-linux-gnu/tracing_subscriber/fmt/writer/trait.MakeWriter.html" title="MakeWriter" target="_blank">MakeWriter</a> which integrates with <code>tracing_subscriber</code>. <code>WorkerGuard</code> is a drop guard that is responsible for flushing any remaining logs when the program terminates.
> 
> Note that the <code>WorkerGuard</code> returned by <code>non_blocking</code> <em>must</em> be assigned to a binding that is not <code>_</code>, as <code>_</code> will result in the <code>WorkerGuard</code> being dropped immediately. Unintentional drops of <code>WorkerGuard</code> remove the guarantee that logs will be flushed during a program’s termination, in a panic or otherwise.

What this means is that we must keep <code>log_guard</code> alive for the application to continue logging. <code>log_guard</code> is an instance of the <a href="https://docs.rs/tracing-appender/latest/tracing_appender/non_blocking/struct.WorkerGuard.html" title="WorkerGuard" target="_blank">WorkerGuard</a> struct and is also the returned value of the public function <code>pub fn init_app_logger(utc_offset: time::UtcOffset) -> WorkerGuard</code>. We will revisit this returned value in a <a href="#the-app-main-module">later section</a>.

<a id="the-app-logger-module-local-datetime"></a>
⓷ Next, we specify the date and time format for each log line. Each line begins with a local date and time. For instance, <code>2024-03-12-08:19:13</code>:

```rust
    // Each log line starts with a local date and time token.
    // 
    // On Ubuntu 22.10, calling UtcOffset::current_local_offset().unwrap() after non_blocking()
    // causes IndeterminateOffset error!!
    // 
    // See also https://github.com/time-rs/time/pull/297.
    //
    let timer = OffsetTime::new(
        //UtcOffset::current_local_offset().unwrap(),
        utc_offset,
        format_description!("[year]-[month]-[day]-[hour]:[minute]:[second]"),
    );
```

We've discussed local dates in some detail in <a href="https://behainguyen.wordpress.com/2023/09/03/rust-baby-step-some-preliminary-look-at-date/" title="Rust: baby step -- some preliminary look at date." target="_blank">this post</a>.

🚀 Please note that this is a local date and time. In my time zone, Australian Eastern Standard Time (AEST), which is 10-11 hours ahead of UTC, the log file name for a log line that starts with <code>2024-03-12-08:19:13</code> would actually be <code>log/2024-03-11.log</code>.

<a id="the-app-logger-module-tracing-level"></a>
⓸ Next, we attempt to define the <a href="https://docs.rs/tracing/latest/tracing/struct.Level.html" title="tracing::Level" target="_blank">tracing::Level</a> based on the environment variable <code>RUST_LOG</code> discussed <a href="#the-env-file">previously</a>: 

```rust
    // Extracts tracing::Level from .env RUST_LOG, if there is any problem, 
    // defaults to Level::DEBUG.
    //
    let level: Level = match std::env::var_os("RUST_LOG") {
        None => Level::DEBUG,

        Some(text) => {
            match Level::from_str(text.to_str().unwrap()) {
                Ok(val) => val,
                Err(_) => Level::DEBUG
            }
        }
    };
```

💥 <strong><em>I initially assumed that having <code>RUST_LOG</code> defined in the environment file <code>.env</code> would suffice. However, it turns out that we need to explicitly set it in the code.</em></strong> 

<a id="the-app-logger-module-create-subscriber"></a>
⓹ We then proceed to <em>“create a subscriber”</em>, I hope I'm using the correct terminology:

```rust
    let subscriber = tracing_subscriber::registry()
        .with(
            Layer::new()
                .with_timer(timer)
                .with_ansi(false)
                .with_writer(non_blocking_appender.with_max_level(level)
                    .and(std::io::stdout.with_max_level(level)))
        );
```

The function <a href="https://docs.rs/tracing-subscriber/latest/tracing_subscriber/fn.registry.html" title="Function tracing_subscriber::registry()" target="_blank">tracing_subscriber::registry()</a> returns a <a href="https://docs.rs/tracing-subscriber/latest/tracing_subscriber/registry/struct.Registry.html" title="Struct tracing_subscriber::registry::Registry" target="_blank">tracing_subscriber::registry::Registry</a> struct. This struct implements the trait <a href="https://docs.rs/tracing-subscriber/latest/tracing_subscriber/layer/trait.SubscriberExt.html" title="Trait tracing_subscriber::layer::SubscriberExt" target="_blank">tracing_subscriber::layer::SubscriberExt</a>. The method <a href="https://docs.rs/tracing-subscriber/latest/tracing_subscriber/layer/trait.SubscriberExt.html#method.with" title="fn with&lt;L&gt;(self, layer: L) -&gt; Layered&lt;L, Self&gt;" target="_blank">fn with&lt;L>(self, layer: L) -> Layered&lt;L, Self></a> from this trait returns a <a href="https://docs.rs/tracing-subscriber/latest/tracing_subscriber/layer/struct.Layered.html" title="Struct tracing_subscriber::layer::Layered" target="_blank">tracing_subscriber::layer::Layered</a> struct, which is a: 

> A <a href="https://docs.rs/tracing-core/0.1.32/tracing_core/subscriber/trait.Subscriber.html" title="Trait tracing_core::subscriber::Subscriber" target="_blank">Subscriber</a> composed of a <code>Subscriber</code> wrapped by one or more <a href="https://docs.rs/tracing-subscriber/latest/tracing_subscriber/layer/trait.Layer.html" title="Trait tracing_subscriber::layer::Layer" target="_blank">Layer</a>s.

We create the new <a href="https://docs.rs/tracing-subscriber/latest/tracing_subscriber/layer/trait.Layer.html" title="Trait tracing_subscriber::layer::Layer" target="_blank">Layer</a> using <a href="https://docs.rs/tracing-subscriber/latest/tracing_subscriber/fmt/struct.Layer.html" title="Struct tracing_subscriber::fmt::Layer" target="_blank">tracing_subscriber::fmt::Layer</a> implementation.

Note that <code>non_blocking_appender</code> is an instance of <a href="https://docs.rs/tracing-appender/latest/tracing_appender/non_blocking/struct.NonBlocking.html" title="Struct tracing_appender::non_blocking::NonBlocking" target="_blank">tracing_appender::non_blocking::NonBlocking</a> struct. This struct implements the trait <a href="https://docs.rs/tracing-subscriber/latest/tracing_subscriber/fmt/writer/trait.MakeWriterExt.html" title="Trait tracing_subscriber::fmt::writer::MakeWriterExt" target="_blank">tracing_subscriber::fmt::writer::MakeWriterExt</a>, where the method <a href="https://docs.rs/tracing-subscriber/0.3.18/tracing_subscriber/fmt/writer/trait.MakeWriterExt.html#method.with_max_level" title="fn with_max_level(self, level: Level) -&gt; WithMaxLevel&lt;Self&gt;" target="_blank">fn with_max_level(self, level: Level) -> WithMaxLevel&lt;Self></a> is defined.

🚀 <code>.and(std::io::stdout.with_max_level(level))</code> means that anything logged to the log file will also be printed to the console.

<a id="the-app-logger-module-register-subscriber"></a>
⓺ Next, the new <a href="https://docs.rs/tracing-core/0.1.32/tracing_core/subscriber/trait.Subscriber.html" title="Trait tracing_core::subscriber::Subscriber" target="_blank">Subscriber</a> is set as the global default for the duration of the entire program:

```rust
    // tracing::subscriber::set_global_default(subscriber) can only be called once. 
    // Subsequent calls raise SetGlobalDefaultError, ignore these errors.
    //
    // There are integeration test methods which call this init_app_logger(...) repeatedly!!
    //
    match tracing::subscriber::set_global_default(subscriber) {
        Err(err) => tracing::error!("Logger set_global_default, ignored: {}", err),
        _ => (),
    }
```

The documentation for the function <a href="https://docs.rs/tracing/latest/tracing/subscriber/fn.set_global_default.html" title="Function tracing::subscriber::set_global_default" target="_blank">tracing::subscriber::set_global_default</a> states: 

> Can only be set once; subsequent attempts to set the global default will fail. Returns whether the initialization was successful.

Since some integration test methods call the <code>pub fn init_app_logger(utc_offset: time::UtcOffset) -> WorkerGuard</code> more than once, we catch potential errors and ignore them. 

<a id="the-app-logger-module-return"></a>
⓻ Finally, <code>pub fn init_app_logger(utc_offset: time::UtcOffset) -> WorkerGuard</code> returns <code>log_guard</code>, as <a href="#the-app-logger-module-non-blocking-writer">discussed above</a>.

<a id="the-app-main-module"></a>
❻ Updates to the <a href="https://github.com/behai-nguyen/rust_web_01/blob/d0005d87b4df15c775daa5167da3fc07c6935f59/src/main.rs" title="src/main.rs" target="_blank">src/main.rs</a> module.

<a id="the-app-main-module-worker-guard"></a>
⓵ Coming back to <a href="https://github.com/behai-nguyen/rust_web_01/blob/d0005d87b4df15c775daa5167da3fc07c6935f59/src/helper/app_logger.rs#L40" title="src/helper/app_logger.rs pub fn init_app_logger(utc_offset: time::UtcOffset) -&gt; WorkerGuard" target="_blank">pub fn init_app_logger(utc_offset: time::UtcOffset) -> WorkerGuard</a>, specifically regarding the returned value <a href="#the-app-logger-module-non-blocking-writer">discussed previously</a>, I read and understood the quoted documentation, and I believe the code was correct. However, it did not write to log files as expected. I <a href="https://users.rust-lang.org/t/actix-web-tracing-subscriber-does-not-write-to-log-file-from-other-modules/107986/5" title="Actix-web tracing-subscriber does not write to log file from other modules" target="_blank">sought help</a>. As per my help request post, I initially called <code>init_app_logger</code> in the <code>src/lib.rs</code> module's <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/lib.rs#L126" title="src/lib.rs pub async fn run(listener: TcpListener) -&gt; Result&lt;Server, std::io::Error&gt;" target="_blank">pub async fn run(listener: TcpListener) -> Result&lt;Server, std::io::Error></a>. Consequently, as soon as <code>run</code> went of scope, the returned <code>WorkerGuard</code> was dropped, and the writer thread terminated.

<a id="the-app-main-module-worker-guard-init-app-logger"></a>
Simply moved it to <code>src/main.rs</code>'s <a href="https://github.com/behai-nguyen/rust_web_01/blob/d0005d87b4df15c775daa5167da3fc07c6935f59/src/main.rs#L21" title="src/main.rs async fn main() -&gt; Result&lt;(), std::io::Error&gt;" target="_blank">async fn main() -> Result&lt;(), std::io::Error></a>, fixed this problem:

```rust
    // Call this to load RUST_LOG.
    dotenv().ok(); 

    // Calling UtcOffset::current_local_offset().unwrap() here works in Ubuntu 22.10, i.e.,
    // it does not raise the IndeterminateOffset error.
    //
    // TO_DO. But this does not guarantee that it will always work! 
    //
    let _guards = init_app_logger(UtcOffset::current_local_offset().unwrap());
```

<strong>Please note the call</strong> <code>UtcOffset::current_local_offset().unwrap()</code>. This is due to the problem discussed in the section <a href="#utcoffset-linux-problem">💥 Issue with calculating UTC time offset on Ubuntu 22.10</a>.

<a id="the-app-main-module-dotenv-ok"></a>
⓶ The function <a href="https://github.com/behai-nguyen/rust_web_01/blob/d0005d87b4df15c775daa5167da3fc07c6935f59/src/helper/app_logger.rs#L40" title="src/helper/app_logger.rs pub fn init_app_logger(utc_offset: time::UtcOffset) -&gt; WorkerGuard" target="_blank">pub fn init_app_logger(utc_offset: time::UtcOffset) -> WorkerGuard</a> requires the environment variable <code>RUST_LOG</code> as <a href="#the-env-file">discussed previously</a>. That's why <code>dotenv().ok()</code> is called in <a href="https://github.com/behai-nguyen/rust_web_01/blob/d0005d87b4df15c775daa5167da3fc07c6935f59/src/main.rs#L14" title="src/main.rs async fn main() -&gt; Result&lt;(), std::io::Error&gt;" target="_blank">async fn main() -> Result&lt;(), std::io::Error></a>.

Recall that <code>dotenv().ok()</code> is also called in the <code>src/lib.rs</code> module's <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/lib.rs#L127" title="src/lib.rs pub async fn run(listener: TcpListener) -&gt; Result&lt;Server, std::io::Error&gt;" target="_blank">pub async fn run(listener: TcpListener) -> Result&lt;Server, std::io::Error></a> to load other environment variables. <em>This setup might seem clunky, but I haven't found a better solution yet!</em>

<a id="update-integration-tests"></a>
❼ Updating integration tests. We want integration tests to be able to log as well. These updates are made solely in the <a href="https://github.com/behai-nguyen/rust_web_01/blob/d0005d87b4df15c775daa5167da3fc07c6935f59/tests/common.rs" title="tests/common.rs module" target="_blank">tests/common.rs</a> module.

The function <a href="https://github.com/behai-nguyen/rust_web_01/blob/d0005d87b4df15c775daa5167da3fc07c6935f59/tests/common.rs#L57" title="tests/common.rs function pub async fn spawn_app() -&gt; TestApp" target="_blank">pub async fn spawn_app() -> TestApp</a> in <code>tests/common.rs</code> calls the <code>src/lib.rs</code> module's function <a href="https://github.com/behai-nguyen/rust_web_01/blob/4b7c3acf8af1f18f99553e7a728f05d9493fb885/src/lib.rs#L127" title="src/lib.rs pub async fn run(listener: TcpListener) -&gt; Result&lt;Server, std::io::Error&gt;" target="_blank">pub async fn run(listener: TcpListener) -> Result&lt;Server, std::io::Error></a> to create application server instances. 

This means that <code>spawn_app()</code> must be refactored to call <a href="https://github.com/behai-nguyen/rust_web_01/blob/d0005d87b4df15c775daa5167da3fc07c6935f59/src/helper/app_logger.rs#L40" title="src/helper/app_logger.rs pub fn init_app_logger(utc_offset: time::UtcOffset) -&gt; WorkerGuard" target="_blank">pub fn init_app_logger(utc_offset: time::UtcOffset) -> WorkerGuard</a> and somehow keep the writer thread alive after <code>spawn_app()</code> goes out of scope. We manage this by:

⓵ Update <code>TestApp</code> struct by adding <a href="https://github.com/behai-nguyen/rust_web_01/blob/d0005d87b4df15c775daa5167da3fc07c6935f59/tests/common.rs#L45" title="TestApp pub guard: WorkerGuard" target="_blank">pub guard: WorkerGuard</a>.

⓶ Update the function <a href="https://github.com/behai-nguyen/rust_web_01/blob/d0005d87b4df15c775daa5167da3fc07c6935f59/tests/common.rs#L57" title="tests/common.rs function pub async fn spawn_app() -&gt; TestApp" target="_blank">pub async fn spawn_app() -> TestApp</a> with additional calls:

```rust
    // To load RUST_LOG from .env file.
    dotenv().ok(); 

    /*
    On Ubuntu 22.10, calling UtcOffset's offset methods causes IndeterminateOffset error!!

    See also https://github.com/time-rs/time/pull/297

    ...
    */

    // TO_DO: 11 is the current number of hours the Australian Eastern Standard Time (AEST)
    // is ahead of UTC. This value need to be worked out dynamically -- if it is at all 
    // possible on Linux!!
    // 
    let guard = init_app_logger(UtcOffset::from_hms(11, 0, 0).unwrap());
```

<a id="update-integration-tests-utcoffset-problem"></a>
Note the call <code>UtcOffset::from_hms(11, 0, 0).unwrap()</code>. This is due to the problem discussed in section <a href="#utcoffset-linux-problem">💥 Issue with calculating UTC time offset on Ubuntu 22.10</a>:

-- 👎 Unlike <a id="the-app-main-module-worker-guard-init-app-logger">src/main.rs</a>, where <code>UtcOffset::current_local_offset().unwrap()</code> works, calling it here consistently results in the <a href="https://docs.rs/time/latest/time/error/struct.IndeterminateOffset.html" title="IndeterminateOffset" target="_blank">IndeterminateOffset</a> error! <code>UtcOffset::from_hms(11, 0, 0).unwrap()</code> works, but again, this is not a guarantee it will keep working.

👎 <strong>The value 11 is hardcoded.</strong> Presently, the Australian Eastern Standard Time (AEST) zone is 11 hours ahead of UTC. To get the AEST date and time, we need to offset UTC by 11 hours. However, 11 is not a constant value; due to daylight savings, in Southern Hemisphere winters, it changes to 10 hours (I think). This means that this code will no longer be correct.

<a id="concluding-remarks"></a>
❽ We've reached the conclusion of this post. I'd like to mention that the ecosystem surrounding tracing and logging is incredibly vast. While this post only scratches the surface, it provides a complete working example nonetheless. We can build upon this foundation as needed.

The UTC offset issue on Ubuntu 22.10, <a href="#utcoffset-linux-problem">as described</a>, must be addressed definitively. However, that task is for another day.

I'm not entirely satisfied with the numerous debug loggings from other crates. These can be filtered and removed, but that's a topic for another post, perhaps.

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
