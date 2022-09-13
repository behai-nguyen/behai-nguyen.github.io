---
layout: post
title: "Python: Flask, dictionaries as JSON objects ready to be used by JavaScript."
description: We have a Python dictionary sitting on a server, and we want to write this dictionary out to a page as a JSON object, ready for client-side Javascript codes. Not all Flask template functions work as I thought they would. I'm documenting my experimentations in this post.
tags:
- Python, 
- Flask, 
- Dictionary, 
- JSON object, 
- JavaScript
---

We have a Python dictionary sitting on a server, and we want to write this dictionary out to a page as a JSON object, ready for client-side Javascript codes. Not all Flask template functions work as I thought they would. I'm documenting my experimentations in this post.

| ![038-feature-image.png](https://behainguyen.files.wordpress.com/2022/09/038-feature-image.png) |
|:--:|
| *Python: Flask, dictionaries as JSON objects ready to be used by JavaScript.* |

Let's go straight to the short discussion first, hopefully it's enough, then readers should not have to go the next section, where I'm demonstrating with codes built upon existing code from some other posts.

Converting a 
<span class="keyword">
Python dictionary</span> to 
<span class="keyword">
JSON</span> is fairly straightforward:

```python
import simplejson as json

data = { ... }

print( json.dumps(data) )
```

The returned value of 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
json.dumps( obj: dict )</span> is a valid 
<span class="keyword">
JSON object</span>, which client-side 
<span class="keyword">
JavaScript</span> can use immediately. I've tried the following
to get this returned value to the page:

```python
...
def json_dumps( obj: dict ):
    return json.dumps( obj )

@app.context_processor
def json_dumps_context_processor():
    def __json_dumps_context_processor( obj: dict ):
        return json_dumps( obj )

    return dict( json_dumps_context_processor=__json_dumps_context_processor )

@app.template_global()
def json_dumps_template_global( obj: dict ):
    return json_dumps( obj )

@app.template_filter()
def json_dumps_decorator_filter( obj: dict ):
    return json_dumps( obj )
	
"""
This registration gets executed automatically by the import 
statement, thereby enabling json_dumps_jinja_filter available
to template rendering function.
"""
app.jinja_env.filters[ 'json_dumps_jinja_filter' ] = json_dumps
```

**Please note**: four ( 4 ) different methods, but 
they all call to the same function to do the work.

The codes to render a template:

```python
data = { ... }
return render_template( 'some_template_file.html', json_obj=data )
```

Inside 
<span class="keyword">
some_template_file.html</span>, we call the above four ( 4 )
template functions as illustrated:

```html
<script>
var jsonObj1 = {{ "{{ json_dumps_context_processor(json_obj) " }}}};
var jsonObj2 = {{ "{{ json_dumps_template_global(json_obj) " }}}};
var jsonObj3 = {{ "{{ json_obj|json_dumps_decorator_filter|safe " }}}};
var jsonObj4 = {{ "{{ json_obj|json_dumps_jinja_filter|safe " }}}};
</script>
```

The final 
<span class="keyword">
HTML</span> will cause run-time errors due to the first two ( 2 ) 
lines: 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
double quotation marks ( " )</span> are output as 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
escape code &amp;#34;</span>.

The 
<span class="keyword">
@app.template_filter()</span> and 
<span class="keyword">
app.jinja_env.filters</span> work as expected. Personally, I like 
<span class="keyword">
@app.template_filter()</span> much better: I'm using it for this 
task.

I did not investigate why 
<span class="keyword">
@app.context_processor</span> and 
<span class="keyword">
@app.template_global()</span> do not work in this case, ( because 
there's already a ready-made solution ).

For <span class="keyword">
@app.template_global()</span>, please see 
<a href="https://flask.palletsprojects.com/en/2.2.x/api/"
title="API"
target="_blank">https://flask.palletsprojects.com/en/2.2.x/api/</a> 
-- we have to search for 
<span class="keyword">
template_global</span>. For the others, please see 
<a href="https://flask.palletsprojects.com/en/2.2.x/templating/"
title="Templates"
target="_blank">https://flask.palletsprojects.com/en/2.2.x/templating/</a>.

The demo codes for this post can be downloaded via:

```
git clone -b v1.0.5 https://github.com/behai-nguyen/app-demo.git
```

Please note, the tag is **v1.0.5**. Please ignore all 
<span class="keyword">
Docker</span> related files.

✿✿✿

I've previously discussed 
<span class="keyword">
@app.context_processor</span> in 
<a href="https://behainguyen.wordpress.com/2022/08/06/814/"
title="Python: pytest and Flask template context processor functions."
target="_blank">Python: pytest and Flask template context processor functions.</a>
The demo codes for this post will build upon the existing codes in the
just mentioned post.

The diagram below shows the project layout when completed.
Please note <span style="font-size:1.5em;">★</span> indicates 
new files, and <span style="font-size:1.5em;">☆</span> indicates 
files which have been modified: 

```
D:\app_demo\
|
|-- .env
|-- app.py
|-- setup.py ☆
|-- pytest.ini
|
|-- src\
|   |
|   |-- app_demo\
|       |   
|       |-- __init__.py
|       |-- config.py
|       |-- urls.py ☆
|       |
|       |-- controllers\
|       |   |
|       |   |-- __init__.py ☆
|       |   |-- echo.py
|       |   |-- json_dumps.py ★
|       |   
|       |-- utils\
|       |   |
|       |   |-- __init__.py 
|       |   |-- context_processor.py ☆
|       |   |-- functions.py
|       |
|       |-- templates\
|       |   |
|       |   |-- base_template.html
|       |   |-- echo\
|       |   |   |
|       |   |   |--echo.html
|       |   |
|       |   |-- json\
|       |   |   |
|       |   |   |--json_dumps.html ★
|       
|-- tests
|   ...
|
|-- venv\
```

The codes are very simple, most are one liner. We briefly look at
the changes below.

❶ <a href="https://github.com/behai-nguyen/app-demo/blob/main/setup.py"
title="setup.py" target="_blank">setup.py</a> -- include new package 
<span class="keyword">
simplejson</span>. To install, run:

```
(venv) D:\app_demo>venv\Scripts\pip.exe install -e .
(venv) behai@omphalos-nas-01:/volume1/web/app_demo$ sudo venv/bin/pip install -e .
```

❷ <a href="https://github.com/behai-nguyen/app-demo/blob/main/src/app_demo/utils/context_processor.py"
title="src/app_demo/utils/context_processor.py"
target="_blank">src/app_demo/utils/context_processor.py</a> -- added new template processing functions discussed above:

```python
def json_dumps_context_processor():
def json_dumps_template_global( obj: dict ):
def json_dumps_decorator_filter( obj: dict ):
app.jinja_env.filters[ 'json_dumps_jinja_filter' ] = json_dumps
```

❸ <a href="https://github.com/behai-nguyen/app-demo/blob/main/src/app_demo/controllers/__init__.py"
title="src/app_demo/controllers/__init__.py"
target="_blank">src/app_demo/controllers/&#95;&#95;init__.py</a> -- added new 
<span class="keyword">
Blueprint: json_blueprint</span>.

❹ <a href="https://github.com/behai-nguyen/app-demo/blob/main/src/app_demo/controllers/json_dumps.py"
title="src/app_demo/controllers/json_dumps.py"
target="_blank">src/app_demo/controllers/json_dumps.py</a> -- controller code 
which serves static response for new route 
<span class="keyword">
/json</span>. The hard-coded dictionary is real data from a project I'm
currently working on.

❺ <a href="https://github.com/behai-nguyen/app-demo/blob/main/src/app_demo/templates/json/json_dumps.html"
title="src/app_demo/templates/json/json_dumps.html"
target="_blank">src/app_demo/templates/json/json_dumps.html</a> -- demo 
template for new route 
<span class="keyword">
/json</span>. We've discussed this template in the first section. 

The new route 
<a href="http://localhost:5000/json"
title="http://localhost:5000/json"
target="_blank">http://localhost:5000/json</a> -- serves the 
final content of this template. This is a static content. 
We have to do browsers' **view page source** 
to see the actual output.

❻ <a href="https://github.com/behai-nguyen/app-demo/blob/main/src/app_demo/urls.py"
title="src/app_demo/urls.py" target="_blank">src/app_demo/urls.py</a> -- register
the new 
<span class="keyword">
Blueprint: json_blueprint</span>, and new route 
<span class="keyword">
/json</span> discussed above.

To recap, the codes for this post can be downloaded using:

```
git clone -b v1.0.5 https://github.com/behai-nguyen/app-demo.git
```

The tag is **v1.0.5**. Please ignore all 
<span class="keyword">
Docker</span> related files.

I hope you find this post useful... Thank you for reading and stay safe.
