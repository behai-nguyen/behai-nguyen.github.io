---
layout: post
title: "Python FastAPI: Implementing Non-Blocking Logging with Built-In QueueHandler and QueueListener Classes"

description: Continuing with our Python FastAPI learning series, this post explores the implementation of non-blocking logging using Python’s built-in QueueHandler and QueueListener classes. 

tags:
- Python 
- FastAPI
- Non-Blocking Logging
- Non-Blocking
- Logging
- QueueHandler
- QueueListener
---

<em>
Continuing with our <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Python FastAPI Complete Series" target="_blank">Python FastAPI learning series</a>, this post explores the implementation of non-blocking logging using Python’s built-in <a href="https://docs.python.org/3/library/logging.config.html#configuring-queuehandler-and-queuelistener" title="Configuring QueueHandler and QueueListener" target="_blank">QueueHandler and QueueListener classes</a>.
</em>

<h3>
🐍 <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![114-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/07/114-feature-image.png) |
|:--:|
| *Python FastAPI: Implementing Non-Blocking Logging with Built-In QueueHandler and QueueListener Classes* |

Starting from this post, the code will require Python 3.12.4. Please refer to the <a href="https://github.com/behai-nguyen/fastapi_learning#the-code-after-tag-v040-requires-python-3124" title="The Code After Tag v0.4.0 Requires Python 3.12.4" target="_blank">following discussion</a> on how to upgrade to Python 3.12.4.

🚀 <strong>Please note,</strong> complete code for this post can be downloaded from GitHub with:

```
git clone -b v0.5.0 https://github.com/behai-nguyen/fastapi_learning.git
```

<h2>Table Of Contents</h2>

<ul style="list-style: none;">
<li style="margin-top:10px;">
<a href="#non-blocking-logging">❶ Definition and Complete Working Example of <code>Non-Blocking Logging</code></a>
</li>
<li style="margin-top:10px;">
<a href="#logging-functionality">❷ Structure of Logging</a>
</li>
<li style="margin-top:10px;">
<a href="#project-layout">❸ Project Layout</a>
</li>
<li style="margin-top:10px;">
<a href="#the-implementation">❹ Implementation of <code>Non-Blocking Logging</code></a>
<ul style="list-style: none;">
<li style="margin-top:10px;">
<a href="#impl-logger-config">⓵ YAML Logger Configuration File</a>
</li>
<li style="margin-top:10px;">
<a href="#impl-python-code">⓶ New Python Module: <code>common/queue_logging.py</code></a>
</li>
<li style="margin-top:10px;">
<a href="#impl-python-main-mod">⓷ Updates to the <code>main.py</code> Module</a>
</li>
<li style="margin-top:10px;">
<a href="#impl-python-use-logging">⓸ Incorporating Logging into Existing Modules</a>
</li>
</ul>
</li>
<li style="margin-top:10px;">
<a href="#documentation">❺ Essential Official Documentation</a>
</li>
<li style="margin-top:10px;">
<a href="#concluding-remarks">❻ Concluding Remarks</a>
</li>
</ul>

<a id="non-blocking-logging"></a>
❶ In essence, <code>non-blocking logging</code> means that the actual logging task does not hold up the thread performing the logging. This thread does not have to wait for the logging to complete and can move to the next instruction immediately.

<code>Non-blocking logging</code> is achieved via three principal built-in classes: <a href="https://docs.python.org/3/library/queue.html#queue.Queue" title="queue.Queue" target="_blank">queue.Queue</a>, <a href="https://docs.python.org/3/library/logging.handlers.html#queuehandler" title="QueueHandler" target="_blank">QueueHandler</a>, and <a href="https://docs.python.org/3/library/logging.handlers.html#queuelistener" title="QueueListener" target="_blank">QueueListener</a>. An instance of <code>queue.Queue</code> is accessible by both a <code>non-blocking</code> <code>QueueHandler</code> instance and a <code>QueueListener</code> instance. The <code>QueueListener</code> instance passes the logging messages to its own <code>blocking</code> handler(s), such as a <a href="https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler" title="RotatingFileHandler" target="_blank">RotatingFileHandler</a>.

According to the official documentation for <a href="https://docs.python.org/3/library/logging.handlers.html#queuehandler" title="QueueHandler" target="_blank">QueueHandler</a> and <a href="https://docs.python.org/3/library/logging.handlers.html#queuelistener" title="QueueListener" target="_blank">QueueListener</a>, they have their own separate thread for logging. This frees the main thread from waiting for the logging to finish, <strong>thereby preventing it from being blocked</strong>.

<a id="non-blocking-logging-example"></a>
The complete working example below, adapted from a <a href="https://stackoverflow.com/a/70716053" title="Python - asynchronous logging" target="_blank">Stack Overflow answer</a> and a <a href="https://medium.com/@dresraceran/implementing-async-logging-in-fastapi-middleware-b112aa9c0db8" title="Implementing Async Logging in FastAPI Middleware" target="_blank">Medium post</a>, illustrates how the aforementioned classes fit together to implement <code>non-blocking logging</code>. Logging messages are written to the <code>queue.log</code> file in the same directory as the Python script file:

{% highlight python linenos %}
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
import logging

import queue
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

log_queue = queue.Queue()
# Non-blocking handler.
queue_handler = QueueHandler(log_queue)  

queue_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# Attached to the root logger.
logger.addHandler(queue_handler)           

# The blocking handler.
rot_handler = RotatingFileHandler('queue.log')

# Sitting comfortably in its own thread, isolated from async code.
queue_listener = QueueListener(log_queue, rot_handler)

# Start listening.
queue_listener.start()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    logger = logging.getLogger()
    logger.info("Application is shutting down.")

    # Should stop listening.
    queue_listener.stop()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root(request: Request):
    logger.debug(f"I am {request.url}")

    return {"message": "Hello World"}
{% endhighlight %}

I am not entirely sure if the above logging approach can also be classified as <code>asynchronous logging</code>, because only one thread can control the Python interpreter at a time, as discussed in <a href="https://realpython.com/python-gil/" title="What Is the Python Global Interpreter Lock (GIL)?" target="_blank">this article</a>.

The final implementation for this post is slightly more complex than the example above, but the underlying technical principles remain the same.

<a id="logging-functionality"></a>
❷ Let’s discuss how the logging messages for each request should be structured.

<ul>
<li style="margin-top:10px;">
When a request is being served, the application automatically logs the following message: <code>* Request Started [&lt; Session Id not available &gt;][UUID session Id]</code>
</li>
<li style="margin-top:10px;">
The request's endpoint handler can optionally log its own messages.
</li>
<li style="margin-top:10px;">
After a request has been served, the application automatically logs the following message: <code>* Request Finished [&lt; Session Id not available &gt;][UUID session Id]</code>
</li>
</ul>

We will refer to the two messages <code>* Request Started ...</code> and <code>* Request Finished ...</code> as a <strong><em>marker pair</em></strong> throughout the rest of this post.

As you may recall from the <a href="https://behainguyen.wordpress.com/2024/05/21/python-fastapi-implementing-persistent-stateful-http-sessions-with-redis-session-middleware-and-extending-oauth2passwordbearer-for-oauth2-security/" title="Python FastAPI: Implementing Persistent Stateful HTTP Sessions with Redis Session Middleware and Extending OAuth2PasswordBearer for OAuth2 Security" target="_blank">third post</a>, we implemented the <code>UUID session Id</code>. An <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-authenticated-session" title="authenticated session" target="_blank"><code>authenticated session</code></a> is uniquely identified by a <code>UUID session Id</code>. Thus, a <code>UUID session Id</code> will be logged with the marker pair if one is available, otherwise the text <code>&lt; Session Id not available &gt;</code> will be logged. Please see the following illustrative examples.

<a id="logging-func-without-uuid"></a>
⓵ Logging where a <code>UUID session Id</code> is not yet available, i.e., the request is from an <code><strong>un</strong> <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-authenticated-session" title="authenticated session" target="_blank">authenticated session</a></code>:

```
INFO:     ... * Request Started < Session Id not available >
INFO:     ... Path: http://192.168.0.16:5000/auth/login?state=0
DEBUG:    ... Attempt to deliver the login page.
DEBUG:    ... Delivering the login page.
INFO:     ... * Request Finished < Session Id not available >
INFO:     ... 192.168.0.2:61019 - "GET /auth/login?state=0 HTTP/1.1" 200
```

<a id="logging-func-with-uuid"></a>
⓶ Logging with a <code>UUID session Id</code>, i.e., the request is from an <a href="https://behainguyen.wordpress.com/2024/01/28/rust-simple-actix-web-email-password-login-and-request-authentication-using-middleware/#definition-authenticated-session" title="authenticated session" target="_blank"><code>authenticated session</code></a>:

```
INFO:     ... * Request Started f9b96bcdab8b5153c44ca02e0a489c7d
INFO:     ... Path: http://192.168.0.16:5000/admin/me
DEBUG:    ... Returning a valid logged-in user.
INFO:     ... * Request Finished f9b96bcdab8b5153c44ca02e0a489c7d
INFO:     ... 192.168.0.2:61016 - "GET /admin/me HTTP/1.1" 200
```

💥 <strong>Please note the last line</strong> in each of the above two examples. It originates from the <code>httptools_impl.py</code> module, specifically the method <code>send</code> on line <code>466</code>. It is outside of the marker pair, and I did not attempt to have it logged within the marker pair. I believe that, together with the <code>thread Id</code> (not shown) and the path, we can visually trace the originating request.

<a id="project-layout"></a>
❸ The changes to the code are quite minimal. Essentially, we’re adding a new <a href="https://yaml.org/" title="YAML" target="_blank">YAML</a> logging configuration file, a new Python module, and incorporating logging into other modules. The updated structure of the project is outlined below.

<strong>-- Please note,</strong> those marked with <span style="font-size:1.5em;">★</span> are updated, and those marked with <span style="font-size:1.5em;">☆</span> are new.

```
/home/behai/fastapi_learning/
.
├── logger_config.yaml ☆ 
├── main.py ★
├── pyproject.toml ★ 
├── pytest.ini
├── README.md ★
├── src
│ └── fastapi_learning
│     ├── common
│     │ ├── consts.py
│     │ └── queue_logging.py ☆
│     ├── controllers
│     │ ├── admin.py ★
│     │ ├── auth.py ★
│     │ └── __init__.py
│     ├── __init__.py
│     ├── models
│     │ └── employees.py
│     ├── static
│     │ └── styles.css
│     └── templates
│         ├── admin
│         │ └── me.html
│         ├── auth
│         │ ├── home.html
│         │ └── login.html
│         └── base.html
└── tests
    ├── conftest.py
    ├── __init__.py
    ├── integration
    │ ├── test_admin_itgt.py
    │ ├── test_api_itgt.py
    │ └── test_auth_itgt.py
    └── README.md
```

<a id="the-implementation"></a>
❹ In this section, we discuss the implementation of <code>non-blocking logging</code>.

I have used <a href="https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler" title="RotatingFileHandler" target="_blank">RotatingFileHandler</a> for logging via an external <a href="https://yaml.org/" title="YAML" target="_blank">YAML</a> configuration file before. I appreciate this approach because we can adjust the logging by tweaking the configuration file without having to refactor the code. I would like to adopt the same approach for this implementation. We will first examine the YAML configuration file and then the associated Python code.

<a id="impl-logger-config"></a>
⓵ The full content of the YAML configuration file, <a href="https://github.com/behai-nguyen/fastapi_learning/blob/68890892801be114aab17cf656d8ebbd6eca06b0/logger_config.yaml" title="The YAML logger configuration file" target="_blank"><code>logger_config.yaml</code></a>, is listed below:

```yaml
version: 1
disable_existing_loggers: False
formatters:
  default:
    (): uvicorn.logging.DefaultFormatter
    format: '{levelprefix} [{asctime}] {thread} {filename} {funcName} {lineno} {message}'
    style: '{'
    datefmt: '%d-%m-%Y %H:%M:%S'
  colours_removed:
    (): uvicorn.logging.DefaultFormatter
    format: '{levelname} [{asctime}] {thread} {filename} {funcName} {lineno} {message}'
    style: '{'
handlers:
  console:
    formatter: default
    class: logging.StreamHandler
    stream: ext://sys.stdout
  rotating_file:
    formatter: colours_removed
    class: logging.handlers.RotatingFileHandler
    filename: ./logs/fastapi_learning.log
    maxBytes: 4096
    backupCount: 5  # Keep 5 old log files    
    encoding: utf-8
  queue_rotating_file:
    class: logging.handlers.QueueHandler
    # queue: fastapi_learning.common.queue_logging.queue_factory
    # listener: fastapi_learning.common.queue_logging.CustomListener
    handlers:
      - rotating_file
loggers:
  # uvicorn.error is also valid. It is the equivalence of root.
  # uvicorn.error: 
  #  level: INFO  
  #  handlers:
  #    - console
  #    - qhand
  #  propagate: no
  fastapi_learning.debug:
    level: DEBUG
    handlers:
      - console
      - queue_rotating_file
    propagate: no
root:
  level: INFO
  handlers:
    - console
    - queue_rotating_file
```

All aspects of the above configuration file are documented in the <a href="https://docs.python.org/3/library/logging.html" title="logging — Logging facility for Python" target="_blank">official Python logging documentation</a>. We will discuss some implementation details below.

<ol>
<li style="margin-top:10px;">
For completeness, we log to both the console (<code>stdout</code>) and log files. The <code>default</code> formatter is for the console, where we retain the default colours. The <code>colours_removed</code> formatter is for the log file. Without removing the text colours, log files will have control codes written in place of text colours. For example, <code>^[[32mINFO^[[0m:</code>, where <code>^[</code> denotes the <code>ESC</code> control character, whose ASCII code is <code>27</code>. Please refer to <a href="https://behainguyen.wordpress.com/wp-content/uploads/2024/07/114-01.png" title="Control colour codes print out illustrations" target="_blank">this screenshot</a> for the exact printout. Please further note the following:
<ul>
<li style="margin-top:10px;">
Log attributes such as <code>levelname</code>, <code>thread</code> etc., are covered by the official documentation on <a href="https://docs.python.org/3/library/logging.html#logrecord-attributes" title="LogRecord attributes" target="_blank">LogRecord attributes</a>.
</li>
<li style="margin-top:10px;">
I <strong>cannot find official documentation</strong> for <code>levelprefix</code>. However, it is mentioned and used in discussions about Python logging across the internet. I have observed that <code>levelprefix</code> and <code>levelname</code> both print out the text logging level such as <code>DEBUG</code>, <code>INFO</code> etc.; <code>levelprefix</code> prints out with colours while <code>levelname</code> does not.
</li>
<li style="margin-top:10px;">
For the rather unusual entry <code>(): uvicorn.logging.DefaultFormatter</code>, please refer to the official documentation on <a href="https://docs.python.org/3/library/logging.config.html#logging-config-dict-userdef" title="User-defined objects" target="_blank">User-defined objects</a>. 
</li>
</ul>
</li>
<a id="impl-logger-config-rotating-file"></a>
<li style="margin-top:10px;">
For the <code>rotating_file</code> handler, please note:
<ul>
<li style="margin-top:10px;">
💥 For the <code>filename: ./logs/fastapi_learning.log</code> property, we configured the log files to be written to the <code>./logs</code> sub-directory. This is not something supported out of the box. We will discuss this property in a <a href="#impl-python-logs-sub-dir">later section</a>.
</li>
<li style="margin-top:10px;">
The values of <code>maxBytes</code> and <code>backupCount</code> are deliberately set low for debugging purposes.
</li>
</ul>
</li>
<li style="margin-top:10px;">
For the <code>queue_rotating_file</code> handler, please note:
<ul>
<a id="impl-logger-config-queue-listener"></a>
<li style="margin-top:10px;">
<p>
The YAML configuration is a copy of the snippet from the Python documentation on <a href="https://docs.python.org/3/library/logging.config.html#configuring-queuehandler-and-queuelistener" title="Configuring QueueHandler and QueueListener" target="_blank">Configuring QueueHandler and QueueListener</a>. We left both the <code>queue</code> key and the <code>listener</code> out. We use the standard implementations as documented. 
</p>
<p>
💥 It is the application’s responsibility to start and stop any <a href="https://docs.python.org/3/library/logging.handlers.html#logging.handlers.QueueListener" title="QueueListener" target="_blank">QueueListener</a> instances in use. We will discuss this in a <a href="#impl-python-listeners">later section</a>.
</p>
</li>
<li>
<p>
The <a href="https://docs.python.org/3/library/logging.handlers.html#logging.handlers.QueueHandler" title="QueueHandler" target="_blank">QueueHandler</a> is a special case: it has its own handlers, in this case, it is the <code>rotating_file</code>.
</p>
<p>
It is worth noting that the structure of the <code>queue_rotating_file</code> is very similar to the <a href="#non-blocking-logging-example">non-blocking logging example</a> presented in an earlier section.
</p>
</li>
</ul>
</li>
<a id="impl-logger-config-logger"></a>
<li style="margin-top:10px;">
We configure only one logger: <code>fastapi_learning.debug</code>. Its log messages are consumed by both the console and the <code>queue_rotating_file</code> handlers.
</li>
</ol>	

<a id="impl-python-code"></a>
⓶ We will now discuss the new Python module, <a href="https://github.com/behai-nguyen/fastapi_learning/blob/68890892801be114aab17cf656d8ebbd6eca06b0/src/fastapi_learning/common/queue_logging.py" title="Logging management common/queue_logging.py" target="_blank"><code>common/queue_logging.py</code></a>, which works in conjunction with the <a href="#impl-logger-config">above YAML configuration file</a>. This is a straightforward module, comprising less than 90 lines.

<ol>
<a id="impl-python-logs-sub-dir"></a>
<li style="margin-top:10px;">
<p>
In the <a href="#impl-logger-config-rotating-file"><code>rotating_file</code> handler</a> section, we mentioned that the <code>./logs</code> sub-directory is not supported out of the box. As it is configured, it is a sub-directory immediately under the directory where the <a href="https://github.com/behai-nguyen/fastapi_learning/blob/68890892801be114aab17cf656d8ebbd6eca06b0/main.py" title="fastapi_learning application entry script" target="_blank"><code>main.py</code></a> module resides.
</p>

<p>
We need to manage this sub-directory ourselves: we must ensure that this sub-directory exists before the <a href="#impl-logger-config">YAML configuration file</a> is loaded, otherwise Python will raise an exception. 
</p>

<p>
💥 Therefore, passing the YAML configuration file in the command line, such as <code>uvicorn main:app --log-config=logger_config.yaml</code>, is not possible, or more accurately, <strong>I don’t know how to enable that</strong>. I tried and failed to run my code before the configuration file was loaded.
</p>

<p>
The next best option is to load the configuration file ourselves: we have full control. Please refer to the function <a href="https://github.com/behai-nguyen/fastapi_learning/blob/68890892801be114aab17cf656d8ebbd6eca06b0/src/fastapi_learning/common/queue_logging.py#L57-L65" title="prepare_logging_and_start_listeners" target="_blank"><code>prepare_logging_and_start_listeners</code>, lines 57-65</a>, in the new <code>common/queue_logging.py</code> module. The actual code consists of only 4 lines:
</p>

<ul>
<li style="margin-top:10px;">
Always create the <code>./logs</code> sub-directory.
</li>
<li style="margin-top:10px;">
We then load the configuration file and pass it to <a href="https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig" title="logging.config.dictConfig" target="_blank">logging.config.dictConfig</a>.
</li>
</ul>

<p>
💥 <strong>Please note that</strong>, due to the above implementation, the loggers have not been configured yet when the application starts up. The startup messages below are not written to the current log file. The default existing loggers are still in use at this point.
</p>

<pre>
INFO:     Started server process [29204]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
</pre>
</li>

<a id="impl-python-listeners"></a>
<li style="margin-top:10px;">
<p>
In a <a href="#impl-logger-config-queue-listener">previous section</a>, we mentioned that it is the application’s responsibility to start and stop any <a href="https://docs.python.org/3/library/logging.handlers.html#logging.handlers.QueueListener" title="QueueListener" target="_blank">QueueListener</a> instances. The last part of the function <a href="https://github.com/behai-nguyen/fastapi_learning/blob/68890892801be114aab17cf656d8ebbd6eca06b0/src/fastapi_learning/common/queue_logging.py#L67-L69" title="prepare_logging_and_start_listeners" target="_blank"><code>prepare_logging_and_start_listeners</code></a>, lines <code>67</code> to <code>69</code>, implements the code to get the listeners to start listening. 
</p>

<p>
We retrieve all listener instances and start each one. The private helper function <a href="https://github.com/behai-nguyen/fastapi_learning/blob/68890892801be114aab17cf656d8ebbd6eca06b0/src/fastapi_learning/common/queue_logging.py#L39-L47" title="__retrieve_queue_listeners" target="_blank"><code>__retrieve_queue_listeners</code></a> should be self-explanatory. 
</p>

<p>
We currently have only one listener instance, but in the future, we might configure more, such as for sending out emails. In such a case, we would need to update only the private function <code>__retrieve_queue_listeners</code>.
</p>

<p>
Before the application shuts down, it should call <a href="https://github.com/behai-nguyen/fastapi_learning/blob/68890892801be114aab17cf656d8ebbd6eca06b0/src/fastapi_learning/common/queue_logging.py#L79-L87" title="logging_stop_listeners" target="_blank"><code>logging_stop_listeners</code></a> to get the listeners to stop listening.
</p>
</li>

<a id="impl-python-request-markers"></a>
<li style="margin-top:10px;">And finally, the <a href="https://github.com/behai-nguyen/fastapi_learning/blob/68890892801be114aab17cf656d8ebbd6eca06b0/src/fastapi_learning/common/queue_logging.py#L12-L37" title="RequestLoggingMiddleware class" target="_blank"><code>RequestLoggingMiddleware</code></a> class implements the request logging marker pair that was mentioned in an <a href="#logging-functionality">in an earlier section</a>.
</li>
</ol>

<a id="impl-python-main-mod"></a>
⓷ The changes in <a href="https://github.com/behai-nguyen/fastapi_learning/blob/68890892801be114aab17cf656d8ebbd6eca06b0/main.py" title="fastapi_learning application entry script" target="_blank"><code>main.py</code></a> are straightforward and should be self-explanatory.

For information on the new <a href="https://github.com/behai-nguyen/fastapi_learning/blob/68890892801be114aab17cf656d8ebbd6eca06b0/main.py#L36-L45" title="fastapi_learning application entry script" target="_blank"><code>lifespan</code></a> function, please refer to the official FastAPI documentation on <a href="https://fastapi.tiangolo.com/ru/advanced/events/#lifespan" title="Lifespan" target="_blank">Lifespan</a>.

<a id="impl-python-use-logging"></a>
⓸ Having implemented all of the above, we are finally able to incorporate logging into the methods in the two modules, <a href="https://github.com/behai-nguyen/fastapi_learning/blob/68890892801be114aab17cf656d8ebbd6eca06b0/src/fastapi_learning/controllers/auth.py" title="controllers/auth.py" target="_blank"><code>controllers/auth.py</code></a> and <a href="https://github.com/behai-nguyen/fastapi_learning/blob/68890892801be114aab17cf656d8ebbd6eca06b0/src/fastapi_learning/controllers/admin.py" title="controllers/admin.py" target="_blank"><code>controllers/admin.py</code></a>.

<a id="documentation"></a>
❺ Some of the referenced official documentation has already been mentioned throughout the discussion. However, I believe it is rather essential, so I would like to reiterate it in this separate section. I have personally read through all the Python documentation on logging. They include:

<ol>
<li style="margin-top:10px;">
<a href="https://docs.python.org/3/library/logging.html" title="logging — Logging facility for Python" target="_blank">logging — Logging facility for Python</a>.
</li>
<li style="margin-top:10px;">
<a href="https://docs.python.org/3/howto/logging.html#logging-basic-tutorial" title="Basic Logging Tutorial" target="_blank">Basic Logging Tutorial</a>.
</li>
<li style="margin-top:10px;">
<a href="https://docs.python.org/3/howto/logging.html#logging-advanced-tutorial" title="Advanced Logging Tutorial" target="_blank">Advanced Logging Tutorial</a>.
</li>
<li style="margin-top:10px;">
<a href="https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook" title="Logging Cookbook" target="_blank">Logging Cookbook</a>.
</li>
</ol>

The last one is particularly interesting. Python logging is indeed a powerful library.

<a id="concluding-remarks"></a>
❻ When I first started this logging process, I thought it was going to be simple. However, it took a bit longer than I anticipated. I encountered some problems, but I managed to find solutions. The code presented in this post has gone through several refactorings. This is the first time I have explored Python logging in detail. I learned a lot during the writing of this post. There is room for improvement, but overall, I think the implementation is acceptable.

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
