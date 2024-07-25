---
layout: post
title: "Python FastAPI: Implementing SSL/HTTPS and CORS"

description: In this installment of our Python FastAPI learning series, we explore the implementation of SSL/HTTPS for localhost and also the enabling of Cross-Origin Resource Sharing, or CORS.

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/07/117-01_edge.png"

gallery-image-list-2:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/07/117-02_edge.png"

gallery-image-list-3:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/07/117-03_edge.png"

gallery-image-list-4:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/07/117-04.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/07/117-05_firefox.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/07/117-06.png"

tags:
- Python
- FastAPI
- SSL
- HTTPS
- CORS
- AJAX
- Cross Domain
---

<em>
In this installment of our <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Python FastAPI Complete Series" target="_blank">Python FastAPI learning series</a>, we explore the implementation of SSL/HTTPS for <code>localhost</code> and also the enabling of Cross-Origin Resource Sharing, or CORS.
</em>

<h3>
🐍 <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![117-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/07/117-feature-image.png) |
|:--:|
| *Python FastAPI: Implementing SSL/HTTPS and CORS* |

The code requires Python 3.12.4. Please refer to the 
<a href="https://github.com/behai-nguyen/fastapi_learning#the-code-after-tag-v040-requires-python-3124" 
title="The Code After Tag v0.4.0 Requires Python 3.12.4" target="_blank">following 
discussion</a> on how to upgrade to Python 3.12.4.

🚀 <strong>Please note,</strong> complete code for this post
can be downloaded from GitHub with:

```
git clone -b v0.6.0 https://github.com/behai-nguyen/fastapi_learning.git
```

<a id="background-discussion"></a>
❶ I have previously implemented both of these using Rust. Please refer 
to the following two posts below:

<ol>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2024/02/10/rust-actix-web-get-ssl-https-for-localhost/" 
title="Rust: actix-web get SSL/HTTPS for localhost" 
target="_blank">Rust: actix-web get SSL/HTTPS for localhost</a>. The sections on 
<a href="https://behainguyen.wordpress.com/2024/02/10/rust-actix-web-get-ssl-https-for-localhost/#openssl-toolkit" 
title="The OpenSSL Toolkit" target="_blank">OpenSSL Toolkit</a>
and 
<a href="https://behainguyen.wordpress.com/2024/02/10/rust-actix-web-get-ssl-https-for-localhost/#generate-key-and-certificate" 
title="Generate a Self-Signed Encrypted Private Key and a Certificate" 
target="_blank">Generate a Self-Signed Encrypted Private Key and a Certificate</a>
are relevant to this post. If you’re not yet familiar with self-signed certificates, 
please refer to these sections. They discuss concepts that aren’t specific to Rust.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2024/02/13/rust-actix-web-cors-cookies-and-ajax-calls/" 
title="Rust: actix-web CORS, Cookies and AJAX calls" 
target="_blank">Rust: actix-web CORS, Cookies and AJAX calls</a>.
The general discussion on CORS and AJAX calls in this post should 
complement the official <code>FastAPI</code> tutorial 
<a href="https://fastapi.tiangolo.com/tutorial/cors/"
title="CORS (Cross-Origin Resource Sharing)" 
target="_blank">CORS (Cross-Origin Resource Sharing)</a>.
</li>
</ol>

<a id="project-layout"></a>
❷ The changes to the code are quite minimal. The updated structure of the 
project is outlined below. Since there are no changes to any files in the 
<code>./src</code> and <code>./tests</code> directories, we have omitted 
these two from the illustration below.

<strong>-- Please note,</strong> those marked with <span style="font-size:1.5em;">★</span> are updated, and those marked with <span style="font-size:1.5em;">☆</span> are new.

```
/home/behai/fastapi_learning/
.
├── cert ☆
│ ├── cert.pem
│ └── key.pem
├── .env ☆
├── logger_config.yaml
├── main.py ★
├── pyproject.toml ★
├── pytest.ini
├── README.md ★
└── ...
```

<a id="implementing-ssl-https"></a>
❸ The implementation of SSL/HTTPS for <code>localhost</code>.

<a href="https://fastapi.tiangolo.com/tutorial/" title="FastAPI" target="_blank">FastAPI</a>
makes the implementation of SSL/HTTPS for <code>localhost</code> fairly easy.
My principle reference is this post 
<a href="https://medium.com/@mariovanrooij/adding-https-to-fastapi-ad5e0f9e084e" 
title="Adding HTTPS to FastAPI" target="_blank">Adding HTTPS to FastAPI</a>. It is
more than a year old: the <code>ssl</code> paramater in this call 
<code>uvicorn.run("main:app", host="0.0.0.0", port=8000, ssl=ssl_context)</code> 
is outdated, and so we don't actually need the <a href="https://pypi.org/project/cryptography/" 
title="The cryptography package" target="_blank">cryptography</a> package 
either.

The implementation is straightfoward. First, we need to generate the self-signed 
certificate files. Then, we need to get application to load and use these files.

<a id="ssl-https-generating-self-signed-cert"></a>
⓵ To generate the self-signed certificate, on both Windows 10 and Ubuntu 22.10 
run the command: 

```
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

Be prepared, you will need to fill in the following prompts:

```
Country Name (2 letter code) [AU]: AU
State or Province Name (full name) [Some-State]: Victoria
Locality Name (eg, city) []: Melbourne
Organization Name (eg, company) [Internet Widgits Pty Ltd]: Personal
Organizational Unit Name (eg, section) []: Development
Common Name (e.g. server FQDN or YOUR name) []: <Windows: Full computer name> <Linux: hostname --fqdn>
Email Address []: behai_nguyen@hotmail.com
```

For <code>Common Name (e.g. server FQDN or YOUR name)</code>, on Windows 10, 
it is the full computer name, in Linux it is the hostname. For more information,
please refer to the 
<a href="https://behainguyen.wordpress.com/2024/02/10/rust-actix-web-get-ssl-https-for-localhost/#generate-key-and-certificate" 
title="Generate a Self-Signed Encrypted Private Key and a Certificate" 
target="_blank">Generate a Self-Signed Encrypted Private Key and a Certificate</a> 
section <a href="#background-discussion">mentioned previously</a>.

The self-signed encrypted private key and the certificate files, 
<code>key.pem</code> and <code>cert.pem</code>, are stored in the 
<code>./cert</code> sub-directory.

<a id="ssl-https-code-changes"></a>
⓶ The code changes occur only in the 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/cc6a59a36ea9a21373bb3f69b3bc2ef36811df9e/main.py#L82-L93" 
title="The main.py module" 
target="_blank"><code>main.py</code></a> module:

<figure class="highlight"><pre><code class="language-python" data-lang="python"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">82
83
84
85
86
87
88
89
90
91
92
93
</pre></td><td class="code"><pre><span class="c1">#
# Remove the code block below to use the command:
#
#    (venv) &lt;venv path&gt; uvicorn main:app --host 0.0.0.0 --port 5000 --ssl-keyfile ./cert/key.pem --ssl-certfile ./cert/cert.pem
#
# The command to run with the below code block:
#
#    (venv) &lt;venv path&gt; python main.py
#
</span><span class="k">if</span> <span class="n">__name__</span> <span class="o">==</span> <span class="s">"__main__"</span><span class="p">:</span>
    <span class="n">uvicorn</span><span class="p">.</span><span class="n">run</span><span class="p">(</span><span class="s">"main:app"</span><span class="p">,</span> <span class="n">host</span><span class="o">=</span><span class="s">"0.0.0.0"</span><span class="p">,</span> <span class="n">port</span><span class="o">=</span><span class="mi">5000</span><span class="p">,</span> \
                <span class="n">ssl_keyfile</span><span class="o">=</span><span class="s">"./cert/key.pem"</span><span class="p">,</span> <span class="n">ssl_certfile</span><span class="o">=</span><span class="s">"./cert/cert.pem"</span><span class="p">)</span>
</pre></td></tr></tbody></table></code></pre></figure>

<a href="https://fastapi.tiangolo.com/tutorial/" title="FastAPI" target="_blank">FastAPI</a>
certainly makes it a lot easier.

<a id="available-routes"></a>
The available routes should now be accessed via <code>https</code>:

<ol>
<li style="margin-top:10px;">
<code>GET</code>, <code>https://0.0.0.0:port/admin/me</code>: 
Returns the currently logged-in user’s information in either JSON or HTML format. 
This route is accessible only to
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-authenticated-session"
title="Authenticated sessions" target="_blank"><code>authenticated sessions</code></a>.
</li>

<li style="margin-top:10px;">	
<code>GET</code>, <code>https://0.0.0.0:port/auth/login</code>: 
Returns the application login page in HTML format.
</li>

<li style="margin-top:10px;">
<code>POST</code>, <code>https://0.0.0.0:port/auth/token</code>: 
Authenticates users. The response can be in either JSON or HTML format.
</li>

<li style="margin-top:10px;">
<code>POST</code>, <code>https://0.0.0.0:port/auth/logout</code>: 
Logs out the currently logged-in or authenticated user. Currently, 
this redirects to the application’s HTML login page.
</li>
	
<li style="margin-top:10px;">
<code>GET</code>, <code>https://0.0.0.0:port/</code>: This is the same as <code>https://0.0.0.0:port/auth/login</code>.
</li>

<li style="margin-top:10px;">
<code>GET</code>, <code>https://0.0.0.0:port/auth/home</code>: Returns the application 
home page in HTML format after a user has successfully logged in. This route is 
accessible only to 
<a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-authenticated-session" 
title="Authenticated sessions" target="_blank"><code>authenticated sessions</code></a>.
</li>

<li style="margin-top:10px;">
<code>GET</code>, <code>https://0.0.0.0:port/api/me</code>: 
This is a duplicate of <code>https://0.0.0.0:port/admin/me</code>, 
but this route returns the currently logged-in user’s information in JSON only.
</li>

<li style="margin-top:10px;">
<code>POST</code>, <code>https://0.0.0.0:port/api/login</code>: 
This is a duplicate of <code>https://0.0.0.0:port/auth/token</code>,
but the response is in JSON only.
</li>
</ol>

<a id="implementing-cors"></a>
❹ Enabling Cross-Origin Resource Sharing, or CORS.

We can just follow the official tutorial page 
<a href="https://fastapi.tiangolo.com/tutorial/cors/"
title="CORS (Cross-Origin Resource Sharing)" 
target="_blank">CORS (Cross-Origin Resource Sharing)</a> to enable 
CORS. Instead of hard-coding the CORS information, we can load 
them from the <a href="https://github.com/behai-nguyen/fastapi_learning/blob/cc6a59a36ea9a21373bb3f69b3bc2ef36811df9e/.env" 
title="The environment file .env" target="_blank"><code>.env</code></a> file.

We will need the 
<a href="https://pypi.org/project/python-dotenv/" 
title="The python-dotenv package" target="_blank">python-dotenv</a> package. 
Please re-run the editable install command:

```
(venv) <venv path> pip install -e .
```

The 
<a href="https://github.com/behai-nguyen/fastapi_learning/blob/cc6a59a36ea9a21373bb3f69b3bc2ef36811df9e/main.py#L61-L68" 
title="The main.py module" 
target="_blank">code changes in the <code>main.py</code></a> module should be self-explanatory.

<a id="cors-ajax-cross-domain"></a>
❺ CORS, AJAX and cross domain in action.

In this final section, we will illustrate how CORS behaves. We use the HTML page 
<a href="https://github.com/behai-nguyen/behai-nguyen.github.io/blob/6fb0781e412765716a8a79b4bc3e0007a745224c/tools/ajax_test.html" 
title="The HTML page with AJAX call" target="_blank">ajax_test.html</a> 
which calls the function 
<a href="https://github.com/behai-nguyen/js/blob/c49e8ba9651e6b4453bf9c9e5573dd8ec25d084c/ajax_funcs.js#L88-L128"
title="runAjaxCrossDomain(...)" target="_blank">runAjaxCrossDomain(...)</a> 
to send AJAX requests to the application. You can just copy this 
<code>ajax_test.html</code> page to your <code>localhost</code> and 
run it locally.

💥 <strong><span style="color:red;">Please note, about HTTPS and 
<code>localhost:</code></span></strong> I have observed that some browsers, 
such as DuckDuckGo, will not allow access to self-signed certificate endpoints 
like <code>https://localhost/...</code> or <code>https://0.0.0.0/...</code>
The error displayed is <code>NET::ERR_CERT_AUTHORITY_INVALID</code>.

FireFox and other Chromium-based browsers warn about security risk, 
just accept and proceed. <strong>You still might have problems accessing
<code>https://0.0.0.0/...</code> endpoints via AJAX. I have found that,
first access a <code>GET</code> endpoint, 
such as <code>https://192.168.0.16:5000/auth/login</code>, accept
the risk and proceed, and you should get a valid response. <em>Then, 
using the same browser to run the <code>ajax_test.html</code> page</em>. 
This will get around the AJAX accessing problem.</strong>

<a id="cors-ajax-cross-domain-valid"></a>
⓵ The <code>ALLOW_ORIGINS</code> for CORS is set to <code>http://localhost</code>. 
We will illustrate the following requests: logging in, retrieving the logged-in 
user information, and finally, logging out.

● The login request:

```
URL: https://192.168.0.16:5000/auth/token
Method: POST
Content Type: application/x-www-form-urlencoded; charset=UTF-8
Body: username=behai_nguyen@hotmail.com&password=password
Header: {"x-expected-format": "application/json"}
```

We should receive a response as illustrated in the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-1 %}
<br/>

● The request to retrieve the information of the logged-in user:

```
URL: https://192.168.0.16:5000/admin/me
Method: GET
Content Type: application/x-www-form-urlencoded; charset=UTF-8
Body: 
Header: {"Authorization":"Bearer behai_nguyen@hotmail.com", "x-expected-format":"application/json"}
```

We don’t actually need to include the “Content Type” and the “Body” fields.”

We should receive a response as illustrated in the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-2 %}
<br/>

● The logout request: 

```
URL: https://192.168.0.16:5000/auth/logout
Method: GET
Content Type: application/x-www-form-urlencoded; charset=UTF-8
Body: 
Header: {"Authorization":"Bearer behai_nguyen@hotmail.com"}
```

We don’t actually need to include the “Content Type” and the “Body” fields.”

We should receive a response as illustrated in the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-3 %}
<br/>

<a id="cors-ajax-cross-domain-invalid"></a>
⓶ The <code>ALLOW_ORIGINS</code> for CORS is set to <code>https://google.com</code>.
This means that the application expects AJAX requests to come from 
<code>https://google.com</code>. Since we are sending AJAX requests from 
<code>http://localhost</code>, they should be rejected. And indeed, they are, 
as illustrated in the screenshots below:

{% include image-gallery.html list=page.gallery-image-list-4 %}
<br/>

<a id="concluding-remarks"></a>
❻ Writing this post has made me appreciate 
<a href="https://fastapi.tiangolo.com/tutorial/" title="FastAPI" target="_blank">FastAPI</a> 
even more 😂… Implementing SSL/HTTPS for <code>localhost</code> is straightforward; 
I didn’t expect it to be this easy.

Thank you for reading. I hope you find the information in this post useful. Stay safe, as always.

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
<a href="https://www.python.org/downloads/release/python-3124/" target="_blank">https://www.python.org/downloads/release/python-3124/</a>
</li>
<li>
<a href="https://fastapi.tiangolo.com/" target="_blank">https://fastapi.tiangolo.com/</a>
</li>
<li>
<a href="https://1000logos.net/download-image/" target="_blank">https://1000logos.net/download-image/</a>
</li>
</ul>

<h3>
🐍 <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>
