---
layout: post
title: "Rust: actix-web get SSL/HTTPS for localhost."

description: We are going to enable our actix-web learning application to run under HTTPS. As a result, we need to do some minor refactoring to existing integration tests. We also move and rename an existing module for better code organisation.

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.files.wordpress.com/2024/02/097-01.png"

gallery-image-list-2:
    - "https://behainguyen.files.wordpress.com/2024/02/097-03-firefox.png"
    - "https://behainguyen.files.wordpress.com/2024/02/097-03-chrome.png"
    - "https://behainguyen.files.wordpress.com/2024/02/097-03-opera.png"

tags:
- Rust
- actix-web
- localhost
- ssl
- https
- self-signed certificate
- certificate
---

<em>We are going to enable our <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> learning application to run under <code>HTTPS</code>. As a result, we need to do some minor refactoring to existing integration tests. We also move and rename an existing module for better code organisation.</em>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rust_web_01" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![097-feature-image.png](https://behainguyen.files.wordpress.com/2024/02/097-feature-image.png) |
|:--:|
| *Rust: actix-web get SSL/HTTPS for localhost.* |

🚀 <strong>Please note,</strong> complete code for this post can be downloaded from GitHub with:

```
git clone -b v0.7.0 https://github.com/behai-nguyen/rust_web_01.git
```

The <a href="https://docs.rs/actix-web/latest/actix_web/" title="actix-web" target="_blank">actix-web</a> learning application mentioned above has been discussed in the following six previous posts:

<ol>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/10/18/rust-web-application-mysql-server-sqlx-actix-web-and-tera/" title="Rust web application: MySQL server, sqlx, actix-web and tera" target="_blank">Rust web application: MySQL server, sqlx, actix-web and tera</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/11/26/rust-learning-actix-web-middleware-01/" title="Rust: learning actix-web middleware 01" target="_blank">Rust: learning actix-web middleware 01</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/12/31/rust-retrofit-integration-tests-to-an-existing-actix-web-application/" title="Rust: retrofit integration tests to an existing actix-web application." target="_blank">Rust: retrofit integration tests to an existing actix-web application</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/01/03/rust-adding-actix-session-and-actix-identity-to-an-existing-actix-web-application/" title="Rust: adding actix-session and actix-identity to an existing actix-web application." target="_blank">Rust: adding actix-session and actix-identity to an existing actix-web application</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/01/14/rust-actix-web-endpoints-which-accept-both-application-x-www-form-urlencoded-and-application-json-content-types/" title="Rust: actix-web endpoints which accept both application/x-www-form-urlencoded and application/json content types." target="_blank">Rust: actix-web endpoints which accept both <code>application/x-www-form-urlencoded</code> and <code>application/json</code> content types</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/" title="Rust: simple actix-web email-password login and request authentication using middleware." target="_blank">Rust: simple actix-web email-password login and request authentication using middleware</a>.</li>
</ol>

The code we're developing in this post is a continuation of the code from the <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/" title="Rust: simple actix-web email-password login and request authentication using middleware." target="_blank">sixth</a> post above. 🚀 To get the code of this <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/" title="Rust: simple actix-web email-password login and request authentication using middleware." target="_blank">sixth</a> post, please use the following command:

```
git clone -b v0.6.0 https://github.com/behai-nguyen/rust_web_01.git
```

<strong>-- Note the tag <code>v0.6.0</code>.</strong>

<h2>Table of contents</h2>
<ul>
<li style="margin-top:10px;"><a href="#define-running-under-https">Define “to run under <code>HTTPS</code>”</a></li>
<li style="margin-top:10px;"><a href="#project-layout">Project Layout</a></li>
<li style="margin-top:10px;"><a href="#openssl-toolkit">The OpenSSL Toolkit</a>
<ul>
<li style="margin-top:10px;"><a href="#openssl-toolkit-installation">Installation</a></li>
<li style="margin-top:10px;"><a href="#win10-openssl-rust-analyzer-env-var">Windows 10, the Rust Analyzer plug-in and the OpenSSL Toolkit environment variable <code>OPENSSL_DIR</code></a></li>
</ul>
</li>
<li style="margin-top:10px;"><a href="#generate-key-and-certificate">Generate a Self-Signed Encrypted Private Key and a Certificate</a></li>
<li style="margin-top:10px;"><a href="#refactor-code-to-enable-https">Code Refactoring to Enable <code>HTTPS</code></a></li>
<li style="margin-top:10px;"><a href="#refactor-integration-tests">Refactor Integration Tests</a>
<ul>
<li style="margin-top:10px;"><a href="#refactor-integration-tests-common">The tests/common.rs Module</a></li>
<li style="margin-top:10px;"><a href="#refactor-integration-tests-modules">The tests/test_handlers.rs and tests/test_auth_handlers.rs Modules</a></li>
</ul>
</li>
<li style="margin-top:10px;"><a href="#general-code-refactoring">Moving src/utils.rs to src/bh_libs/australian_date.rs</a></li>
<li style="margin-top:10px;"><a href="#concluding-remarks">Concluding Remarks</a></li>	
</ul>

<a id="define-running-under-https"></a>
❶ To run under <code>HTTPS</code>. That is:

```
https://localhost:5000/ui/login
https://192.168.0.16:5000/ui/login
```

<a id="project-layout"></a>
❷ Project Layout.

This post introduces a self-signed encrypted private key file and a certificate file. The updated directory layout for the project is listed below.

<strong>-- Please note,</strong> those marked with <span style="font-size:1.5em;">★</span> are updated, and those marked with <span style="font-size:1.5em;">☆</span> are new.

<a id="project-layout-chart"></a>
```
.
├── Cargo.toml ★
├── cert
│ ├── cert-pass.pem ☆ -- Self-signed encrypted private key
│ └── key-pass.pem ☆ -- Certificate
├── .env
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
│ ├── auth_handlers.rs
│ ├── auth_middleware.rs
│ ├── bh_libs
│ │ ├── api_status.rs
│ │ └── australian_date.rs ★
│ ├── bh_libs.rs ★
│ ├── config.rs
│ ├── database.rs
│ ├── handlers.rs
│ ├── helper
│ │ ├── app_utils.rs ★
│ │ ├── constants.rs
│ │ ├── endpoint.rs
│ │ └── messages.rs
│ ├── helper.rs
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
    └── test_handlers.rs ★
```

<a id="openssl-toolkit"></a>
❸ In this post, we are using the <a href="https://www.openssl.org/" title="Open SSL Cryptography and SSL/TLS Toolkit" target="_blank">OpenSSL Cryptography and SSL/TLS Toolkit</a> to generate the self-signed encrypted private key and the certificate files.

<a id="openssl-toolkit-installation"></a>
⓵ We have previously discussed its installation on both Windows 10 Pro and Ubuntu 22.10 in <a href="https://behainguyen.wordpress.com/2023/10/10/rust-sqlx-cli-database-migration-with-mysql-and-postgresql/#sqlx-cli-openssl" title="Rust SQLx CLI: database migration with MySQL and PostgreSQL | SQLx CLI Installation Requires OpenSSL" target="_blank">this section</a> of another post.

<a id="win10-openssl-rust-analyzer-env-var"></a>
⓶ 💥 On Windows 10 Pro, I have observed that, once we include the <a href="https://docs.rs/openssl/latest/openssl/" title="Crate openssl" target="_blank">openssl</a> crate, we should set the environment variable <code>OPENSSL_DIR</code> at the system level, otherwise the <a href="https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer" title="Rust Analyzer" target="_blank">Rust Analyzer</a> Visual Studio Code plug-in would run into trouble.

The environment variable <code>OPENSSL_DIR</code> indicates where OpenSSL has been installed. For example, <code>C:\Program Files\OpenSSL-Win64</code>. Following are the steps to access Windows 10 Pro environment variable setting dialog.

Right click on <strong>This PC</strong> ➜ <strong>Properties</strong> ➜ <strong>Advance system settings</strong> (right hand side) ➜ <strong>Advanced</strong> tab ➜ <strong>Environment Variables...</strong> button ➜ under <strong>System variables</strong> ➜ <strong>New...</strong> ➜ enter variable name and value in the dialog ➜ <strong>OK</strong> button.

The screenshot below is a brief visual representation of the above steps, including the environment variable <code>OPENSSL_DIR</code> in place:

{% include image-gallery.html list=page.gallery-image-list-1 %}

We might need to restart Visual Studio Code to get the new setting recognised.

<a id="generate-key-and-certificate"></a>
❹ Generate the self-signed encrypted private key and the certificate files using the <a href="https://www.openssl.org/" title="Open SSL Cryptography and SSL/TLS Toolkit" target="_blank">OpenSSL Toolkit</a>.

The OpenSSL command to generate the files will prompt a series of questions. One important question is the <code>Common Name</code> which is the server name or <code>FQDN</code> where the certificate is going to be used. If we are not yet familiar with this process, this <a href="https://www.hostinger.com/tutorials/fqdn" title="FQDN (Fully Qualified Domain Name): What It Is, Examples, and More" target="_blank">FQDN (Fully Qualified Domain Name): What It Is, Examples, and More</a> article would be an essential reading, in my humble opnion.

I did seek help working on this issue, please see <a href="https://users.rust-lang.org/t/actix-web-openssl-ssl-https-for-localhost-is-it-possible-please/106444" title="Actix-web OpenSSL SSL/HTTPS for Localhost, is it possible please?" target="_blank">Actix-web OpenSSL SSL/HTTPS for Localhost, is it possible please?</a> And I was pointed to <a href="https://github.com/actix/examples/tree/master/https-tls/openssl" title="examples/https-tls/openssl/" target="_blank">examples/https-tls/openssl/</a> -- and this is my primary source of reference for getting this learning application to run under <code>HTTPS</code>.

The command I choose to use is:

```
$ openssl req -x509 -newkey rsa:4096 -keyout key-pass.pem -out cert-pass.pem -sha256 -days 365
```

Be prepared, we will be asked the following questions:

```
Enter PEM pass pharse: 

Country Name (2 letter code) [AU]: 
State or Province Name (full name) [Some-State]: 
Locality Name (eg, city) []: Melbourne
Organization Name (eg, company) [Internet Widgits Pty Ltd]: 
Organizational Unit Name (eg, section) []: 
Common Name (e.g. server FQDN or YOUR name) []: 
Email Address []: 

Please enter the following 'extra' attributes
to be sent with your certificate request

A challenge password []: 
An optional company name []: 
```

Both <code>key-pass.pem</code> and <code>cert-pass.pem</code> are in the <code>cert/</code> sub-directory as seen in the <a href="#project-layout-chart">Project Layout</a> section.

💥 Please note I also use these two files on Windows 10 Pro to run the application. It works, I am not sure why yet. I need to keep an eye out for this.

<a id="refactor-code-to-enable-https"></a>
❺ Code refactoring to enable <code>HTTPS</code>. 

We are also taking the code from <a href="https://github.com/actix/examples/tree/master/https-tls/openssl" title="examples/https-tls/openssl/" target="_blank">examples/https-tls/openssl/</a>. In <a href="https://github.com/behai-nguyen/rust_web_01/blob/1738173addc7c4db0832ed7678358e0bae2a2a2d/src/lib.rs" title="src/lib.rs" target="_blank">src/lib.rs</a>, we add two private functions <a href="https://github.com/behai-nguyen/rust_web_01/blob/1738173addc7c4db0832ed7678358e0bae2a2a2d/src/lib.rs#L35" title="fn load_encrypted_private_key() -> PKey<Private>" target="_blank"><code>fn load_encrypted_private_key() -> PKey&lt;Private></code></a> and <a href="https://github.com/behai-nguyen/rust_web_01/blob/1738173addc7c4db0832ed7678358e0bae2a2a2d/src/lib.rs#L46" title="fn ssl_builder() -> SslAcceptorBuilder" target="_blank"><code>fn ssl_builder() -> SslAcceptorBuilder</code></a>. They are basically the code copied from the above example re-arranged into two separate functions.

And for the actual <a href="https://docs.rs/actix-web/latest/actix_web/struct.HttpServer.html" title="HttpServer" target="_blank">HttpServer</a> object, we call <a href="https://docs.rs/actix-web/latest/actix_web/struct.HttpServer.html#method.listen_openssl" title="Method listen_openssl(...)" target="_blank">method listen_openssl(...)</a> instead of <a href="https://docs.rs/actix-web/latest/actix_web/struct.HttpServer.html#method.listen" title="Method listen(...)" target="_blank">method listen(...)</a>:

```rust
...
    .listen_openssl(listener, ssl_builder())?
...	
```

I have tested with the latest version of the following browsers: <strong>Firefox</strong>, <strong>Chrome</strong>, <strong>Edge</strong>, <strong>Opera</strong>, <strong>Brave</strong> and <strong>Vivaldi</strong>, for both:

```
https://localhost:5000/ui/login
https://192.168.0.16:5000/ui/login
```

We might get a warning of <span style="color:red;font-weight:bold;"> <code>potential security risk...</code></span> For example, see the <strong>Firefox</strong> warning in the below screenshot:

![097-02.png](https://behainguyen.files.wordpress.com/2024/02/097-02.png)

I just ignore the warning and choose to go ahead. Even though <code>https://</code> works, but all mentioned browsers state that the connection is <span style="color:red;">not secure</span>. Please see <strong>Firefox</strong>, <strong>Chrome</strong> and <strong>Opera</strong> sample screenshots below:

{% include image-gallery.html list=page.gallery-image-list-2 %}

<a id="refactor-integration-tests"></a>
❻ We have to make changes to both integration tests common code and actual test code.

<a id="refactor-integration-tests-common"></a>
⓵ It's quite obvious that we should access the routes via <code>HTTPS</code>. The first change would be <a href="https://github.com/behai-nguyen/rust_web_01/blob/1738173addc7c4db0832ed7678358e0bae2a2a2d/tests/common.rs#L27" title="pub async fn spawn_app() -> TestApp" target="_blank"><code>pub async fn spawn_app() -> TestApp</code></a> in module <a href="https://github.com/behai-nguyen/rust_web_01/blob/1738173addc7c4db0832ed7678358e0bae2a2a2d/tests/common.rs" title="tests/common.rs" target="_blank">tests/common.rs</a>. We should set the scheme of <code>app_url</code> to <code>https://</code>:

```rust
...
    TestApp {
        app_url: format!("https://127.0.0.1:{}", port)
    }
}	
```

I did run integration tests after making this change. They failed. Base on the error messages, it seems that <a href="https://docs.rs/reqwest/latest/reqwest/struct.Client.html" title="reqwest::Client" target="_blank">reqwest::Client</a> should “have” the certificate as well (?). 

Looking through the <a href="https://docs.rs/reqwest/latest/reqwest/index.html" title="Crate reqwest" target="_blank">reqwest</a> crate documentation, <a href="https://docs.rs/reqwest/latest/reqwest/struct.ClientBuilder.html#method.add_root_certificate" title="pub fn add_root_certificate(self, cert: Certificate) -&gt; ClientBuilder" target="_blank"><code>pub fn add_root_certificate(self, cert: Certificate) -> ClientBuilder</code></a> seems like a good candidate... 

Base on the example given in <a href="https://docs.rs/reqwest/latest/reqwest/tls/struct.Certificate.html" title="reqwest::tls::Certificate" target="_blank">reqwest::tls::Certificate</a>, I come up with <a href="https://github.com/behai-nguyen/rust_web_01/blob/1738173addc7c4db0832ed7678358e0bae2a2a2d/tests/common.rs#L42" title="pub fn load_certificate() -&gt; Certificate" target="_blank"><code>pub fn load_certificate() -> Certificate</code></a> and <a href="https://github.com/behai-nguyen/rust_web_01/blob/1738173addc7c4db0832ed7678358e0bae2a2a2d/tests/common.rs#L72" title="pub fn reqwest_client() -&gt; reqwest::Client" target="_blank"><code>pub fn reqwest_client() -> reqwest::Client</code></a>.

I have tried to document all my observations during developing these two helper functions. They are short and simple, I think the inline documentation explains the code quite sufficiently.

-- Initially, <code>reqwest_client()</code> does not include <code>.danger_accept_invalid_certs(true)</code>, resulting in a certificate error. <a href="https://stackoverflow.com/questions/76724036/how-to-resolve-a-rust-reqwest-error-invalid-certificate#comment135281495_76724036" title="Invalid certificate potential correct answer" target="_blank">This solution</a>, provided in the following Stack Overflow thread titled <a href="https://stackoverflow.com/questions/76724036/how-to-resolve-a-rust-reqwest-error-invalid-certificate" title="How to resolve a Rust Reqwest Error: Invalid Certificate" target="_blank">How to resolve a Rust Reqwest Error: Invalid Certificate</a> suggests adding <code>.danger_accept_invalid_certs(true)</code>, which appears to resolve the issue.

<a id="refactor-integration-tests-possible-certificate-issue"></a>
💥 Base on all evidences presented so far, including the <code>connection not secure</code> warnings reported by browsers and the need to call <code>.danger_accept_invalid_certs(true)</code> when creating a <a href="https://docs.rs/reqwest/latest/reqwest/struct.Client.html" title="reqwest::Client" target="_blank">reqwest::Client</a> instance, it seems to suggest that <strong><em> there may still be an issue with this implementation. Or is it common for a self-signed certificate, which is not issued by a trusted certificate authority, to encounter such problems? </em></strong> However, having the application run under <code>https://</code> addresses issues I have had with cookies. For now, I will leave it as is. We will discuss cookie in another new post.

<a id="refactor-integration-tests-modules"></a>
⓶ In both integration test modules, <a href="https://github.com/behai-nguyen/rust_web_01/blob/1738173addc7c4db0832ed7678358e0bae2a2a2d/tests/test_handlers.rs" title="tests/test_handlers.rs" target="_blank">tests/test_handlers.rs</a> and <a href="https://github.com/behai-nguyen/rust_web_01/blob/1738173addc7c4db0832ed7678358e0bae2a2a2d/tests/test_auth_handlers.rs" title="tests/test_auth_handlers.rs TO_DO" target="_blank">tests/test_auth_handlers.rs</a>, we use the <a href="https://github.com/behai-nguyen/rust_web_01/blob/1738173addc7c4db0832ed7678358e0bae2a2a2d/tests/common.rs#L72" title="pub fn reqwest_client() -&gt; reqwest::Client" target="_blank"><code>pub fn reqwest_client() -> reqwest::Client</code></a> function to create instances of <a href="https://docs.rs/reqwest/latest/reqwest/struct.Client.html" title="reqwest::Client" target="_blank">reqwest::Client</a> for testing purposes, instead of creating instances directly in each test method.

<a id="general-code-refactoring"></a>
❼ The final task of this post involves moving <a href="https://github.com/behai-nguyen/rust_web_01/blob/d6d60d7d2e2bac2a0f1a626df50c0c24575dfd53/src/utils.rs" title="src/utils.rs" target="_blank">src/utils.rs</a> to <a href="https://github.com/behai-nguyen/rust_web_01/blob/86d2a4d902c5b8f585cea9407720dcc93fcf6a51/src/bh_libs/australian_date.rs" title="src/bh_libs/australian_date.rs" target="_blank">src/bh_libs/australian_date.rs</a>, as it is a generic module, even though it depends on other third-party crates. It is possible that this module will be moved elsewhere again.

The module <a href="https://github.com/behai-nguyen/rust_web_01/blob/86d2a4d902c5b8f585cea9407720dcc93fcf6a51/src/bh_libs/australian_date.rs" title="src/bh_libs/australian_date.rs" target="_blank">src/bh_libs/australian_date.rs</a> is generic enough to used as-is in other projects.

As a result, the <a href="https://github.com/behai-nguyen/rust_web_01/blob/1738173addc7c4db0832ed7678358e0bae2a2a2d/src/models.rs#L TO_DO Employee struct" title="src/models.rs Employee struct" target="_blank">src/models.rs</a> module is updated.

<a id="concluding-remarks"></a>
❽ We've reached the end of this post. I'd like to mention that I also followed the tutorial <a href="https://hackernoon.com/how-to-get-sslhttps-for-localhost-i11s3342" title="How to Get SSL/HTTPS for Localhost" target="_blank">How to Get SSL/HTTPS for Localhost</a>. I completed it successfully on Ubuntu 22.10, but browsers still warn about the connection not being secure. Perhaps this is to be expected with a self-signed certificate?

Overall, it's been an interesting exercise. I hope you find the information in this post useful. Thank you for reading. And stay safe, as always.

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