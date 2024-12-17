---
layout: post
title: "The Python urllib3 HTTP Library and SSL/HTTPS for localhost"

description: I am studying the urllib3 HTTP library. I am accessing my own servers written in Rust and Python. Both servers implement SSL/HTTPS for localhost using self-signed certificates. As it turns out, we need to disable SSL verification in this scenario. This post documents my attempts to understand this feature of the urllib3 HTTP library. 

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/12/129-01.png"

gallery-image-list-2:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/12/129-02.png"

tags:
- urllib3
- http
- library
- ssl
- https
- localhost
- python
- rust
---

<em>
I am studying the <a href="https://pypi.org/project/urllib3/" title="The urllib3 library" target="_blank">urllib3</a> HTTP library. I am accessing my own servers written in <a href="https://www.rust-lang.org/" title="The Rust language" target="_blank">Rust</a> and <a href="https://www.python.org/" title="The Python language" target="_blank">Python</a>. Both servers implement SSL/HTTPS for localhost using self-signed certificates. As it turns out, we need to disable SSL verification in this scenario. This post documents my attempts to understand this feature of the <a href="https://pypi.org/project/urllib3/" title="The urllib3 library" target="_blank">urllib3</a> HTTP library.
</em>

| ![129-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/12/129-feature-image.png) |
|:--:|
| *The Python urllib3 HTTP Library and SSL/HTTPS for localhost* |

<a id="the-urllib3-lib"></a>
❶ It seems that there are two popular Python HTTP libraries: 
<a href="https://pypi.org/project/requests/" title="The Requests library" target="_blank">Requests</a> 
and 
<a href="https://pypi.org/project/urllib3/" title="The urllib3 library" target="_blank">urllib3</a>. 
Under the hood, the former uses the latter. I chose <code>urllib3</code> 
as I don't see <code>Requests</code> offering any significant advantages. 

To install the <a href="https://pypi.org/project/urllib3/" title="The urllib3 library" target="_blank">urllib3</a> 
library in an active <code>venv</code> virtual environment, run the following command: 

```
▶️Windows 10: .\venv\Scripts\pip.exe install urllib3
▶️Ubuntu 24.04: ./venv/bin/pip install urllib3
```

<a id="simple-google-homepage-get"></a>
❷ Let's start off with a simple script that retrieves the Google home page.

```
Content of urllib3_000_get_ssl.py:
```

```python
import urllib3

http = urllib3.PoolManager()

resp = http.request("GET", "https://google.com")

status = resp.status
print(f"status: {status}\n")
print(f"data: {resp.data.decode('utf-8')}")
```

Run the script with the following command:

```
▶️Windows 10: .\venv\Scripts\python.exe urllib3_000_get_ssl.py
▶️Ubuntu 24.04: ./venv/bin/python urllib3_000_get_ssl.py
```

It should run successfully. The output should be:

```
status: 200

data: <!doctype html><html itemscope="" 
...
<meta content="Seasonal Holidays 2024" property="twitter:title">
...
<title>Google</title>
...
</body></html>
```

<a id="rust-python-servers"></a>
❸ <a href="https://behainguyen.wordpress.com/2024/02/10/rust-actix-web-get-ssl-https-for-localhost/" 
title="Rust: actix-web get SSL/HTTPS for localhost" target="_blank">This article</a> 
This article describes the SSL/HTTPS implementation for localhost using self-signed certificates for the server written in 
<a href="https://www.rust-lang.org/" title="The Rust language" target="_blank">Rust</a>. 
🦀 Here is the index for the <a href="https://github.com/behai-nguyen/rust_web_01" title="Index of the Complete Series" target="_blank">complete series</a>. 
From here on, it is referred to as the <strong><code>Rust server</code></strong>. Similarly, 
<a href="https://behainguyen.wordpress.com/2024/07/25/python-fastapi-implementing-ssl-https-and-cors/" 
title="Python FastAPI: Implementing SSL/HTTPS and CORS" target="_blank">this article</a> 
describes the Python server. 🐍 Here is the index for the 
<a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">complete series</a>. 
From here on, it is referred to as the <strong><code>Python server</code></strong>.

<a id="python-server-login-1"></a>
🐍 Let's first try the Python server's login endpoint at <code>https://localhost:5000/auth/token</code>.

```
Content of urllib3_001_login_python.py:
```

```python
import urllib3

http = urllib3.PoolManager()

resp = http.request(
    "POST",
    "https://localhost:5000/auth/token",
    fields={"username": "behai_nguyen@hotmail.com", "password": "password"},
    headers={
        "x-expected-format": "application/json"
    }
)

status = resp.json()

print( f"Status code: {status['status']['code']}" )
print( f"Status text: {status['status']['text']}" )

data = status['data']

print( f"Access Token: {data['access_token']}" )
print( f"Detail: {data['detail']}" )
print( f"Token Type: {data['token_type']}" )
```

I was expecting it to just work, but it did not. On Windows 10, the error is:

<span style="font-weight:bold;color:red;font-family: Consolas,monaco,monospace;">urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='localhost', port=5000): Max retries exceeded with url: /auth/token (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate (_ssl.c:1006)')))</span>

And on Ubuntu, the error is:

<span style="font-weight:bold;color:red;font-family: Consolas,monaco,monospace;">urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='localhost', port=5000): Max retries exceeded with url: /auth/token (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate (_ssl.c:1020)')))</span>

<a id="rust-server-login-1"></a>
🦀 And so, I did not expect the Rust server's login endpoint to work. The endpoint is <code>https://localhost:5000/api/login</code>.

```
Content of urllib3_001_login_rust.py:
```

```python
import json
import urllib3

http = urllib3.PoolManager()

encoded_body = json.dumps({
    "email": "saniya.kalloufi.10008@gmail.com", 
    "password": "password",
})

# See F:/rust/actix_web/tests/test_auth_handlers.rs
#     https://github.com/behai-nguyen/rust_web_01/blob/125378410c5afa06e22646deacb68c80021a303f/tests/test_auth_handlers.rs#L178-L207
#       async fn post_login_json()
resp = http.request(
    "POST",
    "https://localhost:5000/api/login",
    body=encoded_body,
    headers={
        "content-type": "application/json"
    }    
)

status = resp.json()

print( f"Code: {status['code']}" )
print( f"Message: {status['message']}" )
print( f"Session Id: {status['session_id']}\n" )

data = status['data']

print( f"Email: {data['email']}" )
print( f"Access Token: {data['access_token']}" )
print( f"Token Type: {data['token_type']}" )
```

Windows 10 error:

<span style="font-weight:bold;color:red;font-family: Consolas,monaco,monospace;">urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='192.168.0.16', port=5000): Max retries exceeded with url: /api/login (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1006)')))</span>

Ubuntu error:

<span style="font-weight:bold;color:red;font-family: Consolas,monaco,monospace;">urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='192.168.0.16', port=5000): Max retries exceeded with url: /api/login (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate (_ssl.c:1020)')))</span>

<a id="urllib3-certificate-bundle"></a>
❹ According to the official page 
<a href="https://urllib3.readthedocs.io/en/1.25.10/advanced-usage.html#custom-ssl-certificates" 
title="Custom SSL certificates" target="_blank">Custom SSL certificates</a>, 
the pool manager should be initiated with the certificate information as follows:

```python
>>> import urllib3
>>> http = urllib3.PoolManager(
...     cert_reqs='CERT_REQUIRED',
...     ca_certs='/path/to/your/certificate_bundle')
```

<a id="create-certificate-chain"></a>
This article 
<a href="https://www.golinuxcloud.com/openssl-create-certificate-chain-linux/" 
title="OpenSSL create Certificate Chain [Root & Intermediate CA]" 
target="_blank">OpenSSL create Certificate Chain [Root & Intermediate CA]</a> 
dated 27/07/2024 discusses certificate bundles. After completing all the certificate creation steps, we should have the following directory content:

```
behai@HP-Pavilion-15:~$ tree myCA/
myCA/
├── intermediateCA
│   ├── certs
│   │   ├── ca-chain.cert.pem
│   │   ├── intermediate.cert.pem
│   │   ├── intermediate.csr.pem
│   │   └── localhost.cert.pem
│   ├── crl
│   ├── crlnumber
│   ├── csr
│   │   └── localhost.csr.pem
│   ├── index.txt
│   ├── index.txt.attr
│   ├── index.txt.old
│   ├── newcerts
│   │   └── 1000.pem
│   ├── openssl_intermediate.cnf
│   ├── private
│   │   ├── intermediate.key.pem
│   │   └── localhost.key.pem
│   ├── serial
│   └── serial.old
└── rootCA
    ├── certs
    │   └── ca.cert.pem
    ├── crl
    ├── crlnumber
    ├── csr
    ├── index.txt
    ├── index.txt.attr
    ├── index.txt.old
    ├── newcerts
    │   └── 1000.pem
    ├── openssl_root.cnf
    ├── private
    │   └── ca.key.pem
    ├── serial
    └── serial.old

13 directories, 25 files
behai@HP-Pavilion-15:~$
```

👉 Please note that for the final, local certificate, I replaced the file name prefix <code>www.example.com</code> with <code>localhost</code>.

The following two files: 

<ol>
<li style="margin-top:10px;">
<code>/home/behai/myCA/intermediateCA/certs/localhost.cert.pem</code>
</li>
<li style="margin-top:10px;">
<code>/home/behai/myCA/intermediateCA/private/localhost.key.pem</code>
</li>
</ol>	

are the certificate and key files that can be used in the Python and Rust server code. And the file:

<ul>
<li style="margin-top:10px;">
<code>/home/behai/myCA/intermediateCA/certs/ca-chain.cert.pem</code>
</li>
</ul>	

is the certificate bundle 
<code>ca_certs='/home/behai/myCA/intermediateCA/certs/ca-chain.cert.pem'</code>.

As discussed in the two <a href="#rust-python-servers">server posts</a>, 
during the certificate creation, we should answer a series of questions as listed below: 

```
Country Name (2 letter code) []: AU
State or Province Name []: Victoria
Locality Name []: Melbourne
Organization Name []: Personal
Organizational Unit Name []: Development
Common Name []: HP-Pavilion-15/localhost/192.168.0.16
Email Address []: behai_nguyen@hotmail.com
```

💥 For the <code>Common Name</code> field, contrary to what I have discussed before, 
I also tried <code>localhost</code> and the Ubuntu IP address <code>192.168.0.16</code>.
All three values produce the same result.

<a id="servers-local-reafactoring-new-cert-files"></a>
❺ 👉 Please note that the following local modifications and testing have been carried out on Ubuntu only.

<a id="servers-local-python-new-cert-files"></a>
<strong>🐍 Refactor the Python Server</strong>

To use the newly generated certificate file in the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/436c732e248d84876cfa11863c639f0e3d5abab4/main.py" 
title="The main.py module" target="_blank"><code>main.py</code></a> module, 
replace the last 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/436c732e248d84876cfa11863c639f0e3d5abab4/main.py#L130-L132" 
title="The main.py module" target="_blank">three lines</a>:

<figure class="highlight"><pre><code class="language-python" data-lang="python"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">130
131
132
</pre></td><td class="code"><pre><span class="k">if</span> <span class="n">__name__</span> <span class="o">==</span> <span class="s">"__main__"</span><span class="p">:</span>
    <span class="n">uvicorn</span><span class="p">.</span><span class="n">run</span><span class="p">(</span><span class="s">"main:app"</span><span class="p">,</span> <span class="n">host</span><span class="o">=</span><span class="s">"0.0.0.0"</span><span class="p">,</span> <span class="n">port</span><span class="o">=</span><span class="mi">5000</span><span class="p">,</span> \
                <span class="n">ssl_keyfile</span><span class="o">=</span><span class="s">"./cert/key.pem"</span><span class="p">,</span> <span class="n">ssl_certfile</span><span class="o">=</span><span class="s">"./cert/cert.pem"</span><span class="p">)</span>
</pre></td></tr></tbody></table></code></pre></figure>

with:

```python
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, \
                ssl_keyfile="/home/behai/myCA/intermediateCA/private/localhost.key.pem", \
                ssl_certfile="/home/behai/myCA/intermediateCA/certs/localhost.cert.pem")
```

<a id="python-server-login-2"></a>
Update <code>urllib3_001_login_python.py</code> to use the certificate bundle:

```python
...
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                           ca_certs="/home/behai/myCA/intermediateCA/certs/ca-chain.cert.pem")
...
```

This does not address the problem. The error message is slightly different:

<span style="font-weight:bold;color:red;font-family: Consolas,monaco,monospace;">urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='localhost', port=5000): Max retries exceeded with url: /auth/token (Caused by SSLError(SSLCertVerificationError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not valid for 'localhost'. (_ssl.c:1020)")))</span>

<a id="servers-local-rust-new-cert-files"></a>
<strong>🦀 Refactor the Rust Server</strong>
In the 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/41734efbfe31ada987d9e19694e487d532230691/src/lib.rs" 
title="The src/lib.rs module" target="_blank"><code>src/lib.rs</code></a> module, replace 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/41734efbfe31ada987d9e19694e487d532230691/src/lib.rs#L80" 
title="The src/lib.rs module" target="_blank">line 80</a>:

<figure class="highlight"><pre><code class="language-python" data-lang="python"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">80
</pre></td><td class="code"><pre><span class="n">let</span> <span class="n">mut</span> <span class="nb">file</span> <span class="o">=</span> <span class="n">File</span><span class="p">::</span><span class="nb">open</span><span class="p">(</span><span class="s">"./cert/key-pass.pem"</span><span class="p">).</span><span class="n">unwrap</span><span class="p">();</span>
</pre></td></tr></tbody></table></code></pre></figure>

with:

```rust
let mut file = File::open("/home/behai/myCA/intermediateCA/private/localhost.key.pem").unwrap();
```

And replace 
<a href="https://github.com/behai-nguyen/rust_web_01/blob/41734efbfe31ada987d9e19694e487d532230691/src/lib.rs#L98" 
title="The src/lib.rs module" target="_blank">line 98</a>:

<figure class="highlight"><pre><code class="language-python" data-lang="python"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">98
</pre></td><td class="code"><pre><span class="n">builder</span><span class="p">.</span><span class="n">set_certificate_chain_file</span><span class="p">(</span><span class="s">"./cert/cert-pass.pem"</span><span class="p">).</span><span class="n">unwrap</span><span class="p">();</span>
</pre></td></tr></tbody></table></code></pre></figure>

with:

```rust
builder.set_certificate_chain_file("/home/behai/myCA/intermediateCA/certs/localhost.cert.pem").unwrap();
```

<a id="rust-server-login-2"></a>
Then update <code>urllib3_001_login_rust.py</code> to use the certificate bundle:

```python
...
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', 
                           ca_certs="/home/behai/myCA/intermediateCA/certs/ca-chain.cert.pem")
...
```

As anticipated, the error is:

<span style="font-weight:bold;color:red;font-family: Consolas,monaco,monospace;">urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='192.168.0.16', port=5000): Max retries exceeded with url: /api/login (Caused by SSLError(SSLCertVerificationError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: IP address mismatch, certificate is not valid for '192.168.0.16'. (_ssl.c:1020)"))) IP address mismatch, certificate is not valid for '192.168.0.16'</span>

<a id="disable-ssl-verification"></a>
❻ This article, 
<a href="https://hayageek.com/disable-ssl-verification-in-python/#urllib3" 
title="Disable SSL Verification in Python – requests, urllib3" 
target="_blank">Disable SSL Verification in Python – requests, urllib3</a>, 
discusses disabling SSL verification. The pool manager should be initiated as follows:

```python
urllib3.disable_warnings()
http = urllib3.PoolManager(
    cert_reqs='CERT_NONE',
    assert_hostname=False
)
```

👉 Please note, we leave the above local changes in place for both servers.

<a id="python-server-login-3"></a>
<strong>🐍 Update the Python Server Login Script</strong>
```
Update urllib3_001_login_python.py to:
```

```python
...
urllib3.disable_warnings()
http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)
...
```

And we are now able to access the Python server. The output of the test script is:

```
Status code: 200
Status text:
Access Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiZWhhaV9uZ3V5ZW5AaG90bWFpbC5jb20iLCJlbXBfbm8iOjUwMDIyMiwic2NvcGVzIjpbInVzZXI6cmVhZCIsInVzZXI6d3JpdGUiXSwiZXhwIjoxNzM0MzIzMzMzfQ.Xi4q2LbqVax06sRaxLx2R1oTN38CMyQarpd_8mQrwII
Detail:
Token Type: bearer
```

<a id="python-server-admin-me-route"></a>
<strong>🐍 Python Server New HTTP GET Test Script</strong>
Using the above access token in a new test script 
<code>urllib3_002_admin_me_python.py</code> to access the Python server endpoint 
<code>https://localhost:5000/admin/me</code>.

```
Content of urllib3_002_admin_me_python.py:
```

```python
import urllib3

# Disable SSL verification and warning.
urllib3.disable_warnings()
http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)

resp = http.request(
    "GET",
    "https://localhost:5000/admin/me",
    headers={
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiZWhhaV9uZ3V5ZW5AaG90bWFpbC5jb20iLCJlbXBfbm8iOjUwMDIyMiwic2NvcGVzIjpbInVzZXI6cmVhZCIsInVzZXI6d3JpdGUiXSwiZXhwIjoxNzM0MzIzMzMzfQ.Xi4q2LbqVax06sRaxLx2R1oTN38CMyQarpd_8mQrwII",
		"x-expected-format": "application/json"
    }
)

print( resp.json() )
```

The new test script executes successfully. The response is captured in the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-1 %}
<br/>

<a id="rust-server-login-3"></a>
<strong>🦀 Update the Rust Server Login Script</strong>
Apply the same modification to the Rust server login test code. Update <code>urllib3_001_login_rust.py</code> to:

```python
...
urllib3.disable_warnings()
http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)
...
```

And the successful output is:

```
Code: 200
Message: None
Session Id: None

Email: saniya.kalloufi.10008@gmail.com
Access Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InNhbml5YS5rYWxsb3VmaS4xMDAwOEBnbWFpbC5jb20iLCJzZXNzaW9uX2lkIjoiNDlhZDQ4OWUtYjk4NC00ZTg4LTlhMWItYjJhZTM3ZDA0YzgzIiwiaWF0IjoxNzM0MzIzMTcwLCJleHAiOjE3MzQzMjQ5NzAsImxhc3RfYWN0aXZlIjoxNzM0MzIzMTcwfQ.zuZ2bIW5R65fNhEYMjkTqWaLqnKJbeTGmVBRs7ioNa8
Token Type: bearer
```

<a id="rust-server-data-employees-route"></a>
<strong>🦀 Rust Server New HTTP POST Test Script</strong>
Using the above access token in a new test script 
<code>urllib3_002_data_employees_rust.py</code> to access the Rust server endpoint 
<code>https://localhost:5000/data/employees</code>.

```
Content of urllib3_002_data_employees_rust.py:
```

```python
import json
import urllib3

# Disable SSL verification and warning.
urllib3.disable_warnings()
http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)

encoded_body = json.dumps({
    "last_name": "%chi",
    "first_name": "%ak",
})

# See F:/rust/actix_web/tests/test_handlers.rs
#     https://github.com/behai-nguyen/rust_web_01/blob/125378410c5afa06e22646deacb68c80021a303f/tests/test_handlers.rs#L65-L102
#       async fn post_employees_json1()
resp = http.request(
    "POST",
    "https://localhost:5000/data/employees",
    body=encoded_body,
    headers={
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InNhbml5YS5rYWxsb3VmaS4xMDAwOEBnbWFpbC5jb20iLCJzZXNzaW9uX2lkIjoiNDlhZDQ4OWUtYjk4NC00ZTg4LTlhMWItYjJhZTM3ZDA0YzgzIiwiaWF0IjoxNzM0MzIzMTcwLCJleHAiOjE3MzQzMjQ5NzAsImxhc3RfYWN0aXZlIjoxNzM0MzIzMTcwfQ.zuZ2bIW5R65fNhEYMjkTqWaLqnKJbeTGmVBRs7ioNa8",
        "content-type": "application/json",
    }    
)

status = resp.json()
print(f"status: {status}")
```

It is also successful. The output is captured in the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-2 %}
<br/>

👉 From Windows 10, to access the Rust and Python servers, just replace <code>https://localhost:5000/</code> with <code>https://192.168.0.16:5000/</code> in the test scripts.

<a id="concluding-remarks"></a>
❼ The primary purpose of implementing SSL/HTTPS for localhost using a self-signed certificate is to better manage cookies, as discussed in the two 
<a href="#rust-python-servers">server posts</a>. Therefore, disabling SSL verification is not a problem, as it is not about security. 
In hindsight, I would prefer the method of creating a self-signed certificate 
<a href="#create-certificate-chain">as discussed</a> in this post, 
rather than the methods employed in the two <a href="#rust-python-servers">server posts</a>.

Thank you for reading. I hope you find the information in this post useful. Stay safe, as always.

✿✿✿

Feature image sources:

<ul>
<li>
<a href="https://www.omgubuntu.co.uk/2024/03/ubuntu-24-04-wallpaper" target="_blank">https://www.omgubuntu.co.uk/2024/03/ubuntu-24-04-wallpaper</a>
</li>
<li>
<a href="https://in.pinterest.com/pin/337277459600111737/" target="_blank">https://in.pinterest.com/pin/337277459600111737/</a>
</li>
<li>
<a href="https://www.python.org/downloads/release/python-3124/" target="_blank">https://www.python.org/downloads/release/python-3124/</a>
</li>
<li>
<a href="https://www.pngitem.com/download/ibmJoR_rust-language-hd-png-download/" target="_blank">https://www.pngitem.com/download/ibmJoR_rust-language-hd-png-download/</a>
</li>
</ul>
