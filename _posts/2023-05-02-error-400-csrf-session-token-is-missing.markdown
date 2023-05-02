---
layout: post
title: "Python: Flask “400 Bad Request: The CSRF session token is missing.”"
description: I am describing the condition under which exception “400 Bad Request&#58; The CSRF session token is missing.” occurs in my application, and how I use the Flask application global exception handler to deal with this exception in a generic manner (or so I hope).
tags:
- Python
- Flask
- CSRF
- Session
- Token
---

<em>I am describing the condition under which exception “400 Bad Request: The CSRF session token is missing.” occurs in my application, and how I use the Flask application global exception handler to deal with this exception in a generic manner (or so I hope).</em>

| ![065-feature-image.png](https://behainguyen.files.wordpress.com/2023/05/065-feature-image.png) |
|:--:|
| *Python: Flask “400 Bad Request: The CSRF session token is missing.”* |

To start off, I'd like to note that, based on what I've 
gathered during my research, <code>“400 Bad Request: The CSRF session token is missing.”</code>
seems to happen under a variety of different conditions. In this post, I'm only
describing a specific instance related to my application -- it might not be 
relevant to similar problems you might have.

I'm using 
<a href="https://flask-wtf.readthedocs.io/en/1.0.x/" title="Flask-WTF" target="_blank">Flask-WTF</a>,
and I've 
<a href="https://flask-wtf.readthedocs.io/en/1.0.x/api/#module-flask_wtf.csrf"
title="Developer Interface | CSRF Protection"
target="_blank">CSRF Protection</a> in place:

```python
import flask
...
from flask_wtf.csrf import CSRFProtect
...

csrf = CSRFProtect()

...

def create_app(config=None):
    """Construct the core application."""

    app = flask.Flask(__name__, instance_relative_config=True)

    ...

    csrf.init_app(app)
	
	...

    return app
```

This exception occurs when I just stop at the login page,
wait until the web session expires, and then log in. 

My login form is pretty much a
<a href="https://flask-wtf.readthedocs.io/en/1.0.x/" title="Flask-WTF" target="_blank">Flask-WTF</a> 
recommended one, please note <code>{{ form.csrf_token }}</code>:

```html
    <form method="post" action="{{ request.path }}" id="loginForm">
        {{ form.csrf_token }}
		
		...
    
        <h1 class="h3 mb-3 fw-normal">Please login</h1>

        <div class="form-floating">
            <input type="email" class="form-control" id="email" name="email" placeholder="name@example.com" data-parsley-trigger="change" required>
            <label for="email">Email address</label>
        </div>

		...

        <div class="form-floating">
            <input type="password" class="form-control" id="password" name="password" placeholder="Password" data-parsley-trigger="change" required>
            <label for="password">Password</label>
        </div>
		
		...
		
        <button class="w-100 btn btn-lg btn-primary" type="submit">Login</button>
    </form>
```

A log in when the web session is still valid sees the following 
form data submitted: <code>csrf_token</code> <code>email</code> and 
<code>password</code>, as per the screen capture below:

![065-01-2.png](https://behainguyen.files.wordpress.com/2023/05/065-01-2.png)

<a href="https://flask-wtf.readthedocs.io/en/1.0.x/" title="Flask-WTF" target="_blank">Flask-WTF</a>'s
<code>def validate_csrf(data, secret_key=None, time_limit=None, token_key=None)</code> in
module <code>csrf.py</code> gets run before our code:

<figure class="highlight"><pre><code class="language-python" data-lang="python"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">102
103
</pre></td><td class="code"><pre>    <span class="k">if</span> <span class="n">field_name</span> <span class="ow">not</span> <span class="ow">in</span> <span class="n">session</span><span class="p">:</span>
        <span class="k">raise</span> <span class="n">ValidationError</span><span class="p">(</span><span class="s">"The CSRF session token is missing."</span><span class="p">)</span>
</pre></td></tr></tbody></table></code></pre></figure>

The value for <code>field_name</code> is <code>'csrf_token'</code>, and the
<code>session</code> instance is:

```
<SqlAlchemySession {'_permanent': True, 'csrf_token': '616c3b20d4b1760fb04a6988befd05102b7e6422', '_fresh': False}>
```

And so the exception will not be raised, <code>validate_csrf(...)</code> exits
successfully. <strong>Have we noticed that the value for the submitted 
<code>csrf_token</code> is different to the value shows in server code?
There must be a conversion / translation takes place prior?</strong>

A log in when the web session has already been expired, 
<strong>still has</strong> <code>csrf_token</code> submitted.
But the <code>session</code> instance shows:

```
<SqlAlchemySession {'_permanent': True}>
```

<code>validate_csrf(...)</code> will raise 
<code>ValidationError("The CSRF session token is missing.")</code>.
Since this exception is outside of the application code, it 
is handled by the application global exception handler 
<code>def handle_error(e)</code> method defined in the
application module, <code>app.py</code>:

```python
"""
App entry point.
"""

...
from bh_apistatus.result_status import make_500_status
...
from XXX import create_app
...
app = create_app()

@app.errorhandler(Exception)
def handle_error(e):
    """ 
    Global error handler for uncaught exceptions.
    Exceptions raised by @requires_access_role( ... ) will go to this handler.
    """
    return make_500_status(str(e)).as_dict()
```

<code>make_500_status(...)</code> is a method from the 
<a href="https://bh-apistatus.readthedocs.io/en/latest/" title="bh-apistatus" target="_blank">bh-apistatus</a>
library which I've written to manage data which would be returned
as <code>JSON</code>. Browsers will then just display the exception 
as <code>JSON</code> -- it makes absolutely no sense to the users.
<code>def handle_error(e)</code> is to catch exceptions which the
application code have not a chance to handle.

Now that I understand the condition under which 
<code>“400 Bad Request: The CSRF session token is missing.”</code>
would occur, I'd like to redirect users to the login page again with a 
friendly message. Furthermore, I'd like to be able to configure how 
<code>def handle_error(e)</code> handles exceptions in a generic manner,
I'd attempt to postulate that there are only a handful of exception which
goes through this code path. 

I came up with the following <code>JSON</code> configuration, 
which stores in a file named <code>exception_config.json</code>, under
the application 
<a href="https://flask.palletsprojects.com/en/2.3.x/config/#instance-folders"
title="Instance Folders" target="_blank">Instance Folders</a>:

```javascript
[
	{
		"typeName": "CSRFError",
		"code": 400,
		"name": "Bad Request",
		"description": "The CSRF session token is missing.",
		"action": {
			"name": "redirect",
			"data1": "auths.login",
			"data2": "Oops... Too much idle time has passed... Please try again."
		}
	}
]
```

We've seen that the exception being raised is <code>ValidationError</code>,
but its <code>type(e).__name__</code> is actually <code>'CSRFError'</code>,
and it has three (3) attributes: <code>code</code>, <code>name</code> and
<code>description</code>: when all four (4) pieces of information match,
I'll take the <code>action</code>, otherwise default to <code>make_500_status(...)</code>.

Accordingly <code>def handle_error(e)</code> gets updated as follows:

```python
@app.errorhandler(Exception)
def handle_error(e):
    """Global error handler for uncaught exceptions.

    Exceptions raised by @requires_access_role( ... ), \Lib\site-packages\flask_wtf\csrf.py's
      def validate_csrf(...) etc. will go to this handler.
    """
    import os
    import simplejson as json

    filename = os.path.join(app.instance_path, '', 'exception_config.json')
    with open(filename) as file:
        json_str = file.read()
    file.close()

    exception_config = json.loads(json_str)

    found = False
    action = None
    for itm in exception_config:
        if (itm['typeName'] != type(e).__name__): 
            continue
        
        if (itm['code'] == e.code and itm['name'] == e.name and 
            itm['description'] == e.description):
            action = itm['action']
            found = True
            break

    if found:
        if (action['name'] == 'redirect'): 
            flash(action['data2'], 'danger')
            return redirect(url_for(action['data1']))

    return make_500_status(str(e)).as_dict()
```

It should be self-explanatory. I don't yet know what other
exceptions might come through this code path, I'll leave it
at this implementation for the time being. I'm sure this would
not be its final shape.

With this update in place, the response is much friendlier:

![065-02.png](https://behainguyen.files.wordpress.com/2023/05/065-02.png)

I hope this post is useful. Thank you for reading and stay safe as always.

✿✿✿

Feature image sources:

<ul>
<li>
<a href="https://in.pinterest.com/pin/337277459600111737/"
target="_blank">https://in.pinterest.com/pin/337277459600111737/</a>
</li>
<li>
<a href="https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper" target="_blank">https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper</a>
</li>
<li>
<a href="https://seeklogo.com/vector-logo/332789/python" target="_blank">https://seeklogo.com/vector-logo/332789/python</a>
</li>
</ul>