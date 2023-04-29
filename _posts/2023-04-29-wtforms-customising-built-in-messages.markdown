---
layout: post
title: "Python: WTForms 3.0.1 customising built-in error messages."
description: An approach to customise WTForms 3.0.1 built-in error messages before (possible) translation and sending back to the callers.

tags:
- Python
- WTForms
- built-in
- message
---

<em>An approach to customise WTForms 3.0.1 built-in error messages before (possible) translation and sending back to the callers.</em>

| ![064-feature-image.png](https://behainguyen.files.wordpress.com/2023/04/064-feature-image.png)
|:--:|
| *Python: WTForms 3.0.1 customising built-in error messages.* |

I am using <a href="https://pypi.org/project/WTForms/" title="WTForms 3.0.1" target="_blank">WTForms 3.0.1</a> to do basic data validations, and I would like to customise built-in messages before sending them back to the callers; or possibly translating them into other languages, then sending back to the callers.

-- An example of such built-in message is <code>“Not a valid integer value.”</code>

And by customising, I mean making them a bit clearer, such as prefix them with the field label. E.g.:

● <code>Employee Id: Not a valid integer value.</code>

These built-in messages are often exception messages raised by the method <code>def process_formdata(self, valuelist):</code> of the appropriate field class. The message <code>Not a valid integer value.</code> comes from <code>class IntegerField(Field)</code>, in the <code>numeric.py</code> module:

```python
    def process_formdata(self, valuelist):
        if not valuelist:
            return

        try:
            self.data = int(valuelist[0])
        except ValueError as exc:
            self.data = None
            raise ValueError(self.gettext("Not a valid integer value.")) from exc
```

This method gets called when we instantiate a <code>Form</code> with data to be validated. 

```python
self.gettext("Not a valid integer value.")
```

is related to internationalisation. It is the <code>def gettext(self, string):</code> method in <code>class DummyTranslations:</code>, in module <code>i18n.py</code>.

In <code>class DummyTranslations:</code>, <code>def gettext(self, string):</code> just returns the string as is, i.e. <code>Not a valid integer value.</code>

According to <a href="https://wtforms.readthedocs.io/en/3.0.x/i18n/#writing-your-own-translations-provider" title="Internationalization (i18n) | Writing your own translations provider" target="_blank">Internationalization (i18n) | Writing your own translations provider</a> -- we can replace <code>class DummyTranslations:</code> with our own, following the example thus given, I came up with the following test script:

```python
from pprint import pprint

from wtforms import Form

from wtforms import (
    IntegerField,
    DateField,
)
from wtforms.validators import (
    InputRequired, 
    NumberRange,
)
from werkzeug.datastructures import MultiDict

class MyTranslations(object):
    def gettext(self, string):

        return f"MyTranslations: {string}"

    def ngettext(self, singular, plural, n):
        if n == 1:
            return f"MyTranslations: {singular}"

        return f"MyTranslations: {plural}"

class MyBaseForm(Form):
    def _get_translations(self):
        return MyTranslations()
    
class TestForm(MyBaseForm):
    id = IntegerField('Id', validators=[InputRequired('Id required'), NumberRange(1, 32767)])
    hired_date = DateField('Hired Date', validators=[InputRequired('Hired Date required')], 
                           format='%d/%m/%Y')
    
form_data = MultiDict(mapping={'id': '', 'hired_date': ''})

form = TestForm(form_data)

res = form.validate()

assert res == False

pprint(form.errors)
```

Basically, I just prepend built-in messages with <code>MyTranslations:</code>, so that the above message would come out as <code>“MyTranslations: Not a valid integer value.”</code>.

<code>class MyBaseForm(Form):</code> is taken from the documentation. In <code>class TestForm(MyBaseForm)</code>, there are two required fields, an integer field and a date field. The rest of the code is pretty much run-of-the-mill Python code.

The output I expected is:

```
{'hired_date': ['MyTranslations: Not a valid date value.'],
 'id': ['MyTranslations: Not a valid integer value.',
        'MyTranslations: Number must be between 1 and 32767.']}
```

But I get:

```
{'hired_date': ['Not a valid date value.'],
 'id': ['Not a valid integer value.', 'Number must be between 1 and 32767.']}
```

👎 It is still using the default <code>DummyTranslations</code> class -- I am certain, because I did trace into it. <strong>The documentation appears misleading.</strong>

I could not find any solution online, in fact there is very little discussion on this topic. I finally able to correct <code>class MyBaseForm(Form):</code> following <code>class FlaskForm(Form):</code> in the <a href="https://flask-wtf.readthedocs.io/en/1.0.x/" title="Flask-WTF" target="_blank">Flask-WTF</a> library:

```python
from wtforms.meta import DefaultMeta
...

class MyBaseForm(Form):
    class Meta(DefaultMeta):
        def get_translations(self, form):
            return MyTranslations()
```

The rest of the code remains unchanged. I now got the output I expected, which is:

```
{'hired_date': ['MyTranslations: Not a valid date value.'],
 'id': ['MyTranslations: Not a valid integer value.',
        'MyTranslations: Number must be between 1 and 32767.']}
```

How do I replace <code>MyTranslations</code> with respective field labels, <code>Id</code> and <code>Hired Date</code> in this case? We know method <code>def gettext(self, string)</code> of the <code>MyTranslations class</code> gets called from the fields, but <code>def gettext(self, string)</code> does not have any reference to calling field instance.

Enable to find anything from the code. I finally choose to use introspection, that is, getting the caller information at runtime. The caller in this case is the field instance. <strong>Please note, it is possible that Python introspection might not always work.</strong>

<code>MyTranslations class</code> gets updated as follows:

```python
import inspect
...

class MyTranslations(object):
    def gettext(self, string):
        caller = inspect.currentframe().f_back.f_locals
    
        return f"{caller['self'].label.text}: {string}"

    def ngettext(self, singular, plural, n):
        caller = inspect.currentframe().f_back.f_locals

        if n == 1:
            return f"{caller['self'].label.text}: {singular}"

        return f"{caller['self'].label.text}: {plural}"
```

And this is the output I am looking for:

```
{'hired_date': ['Hired Date: Not a valid date value.'],
 'id': ['Id: Not a valid integer value.',
        'Id: Number must be between 1 and 32767.']}
```

Complete listing of the final test script:
		
```python
from pprint import pprint

import inspect

from wtforms import Form
from wtforms.meta import DefaultMeta

from wtforms import (
    IntegerField,
    DateField,
)
from wtforms.validators import (
    InputRequired, 
    NumberRange,
)
from werkzeug.datastructures import MultiDict

class MyTranslations(object):
    def gettext(self, string):
        caller = inspect.currentframe().f_back.f_locals
    
        return f"{caller['self'].label.text}: {string}"

    def ngettext(self, singular, plural, n):
        caller = inspect.currentframe().f_back.f_locals

        if n == 1:
            return f"{caller['self'].label.text}: {singular}"

        return f"{caller['self'].label.text}: {plural}"

class MyBaseForm(Form):
    class Meta(DefaultMeta):
        def get_translations(self, form):
            return MyTranslations()
            
class TestForm(MyBaseForm):
    id = IntegerField('Id', validators=[InputRequired('Id required'), NumberRange(1, 32767)])
    hired_date = DateField('Hired Date', validators=[InputRequired('Hired Date required')], 
                           format='%d/%m/%Y')
    

form_data = MultiDict(mapping={'id': '', 'hired_date': ''})

form = TestForm(form_data)

res = form.validate()

assert res == False

pprint(form.errors)
```

Please note that I am not sure if this is the final solution for what I want to achieve, for me, it is interesting regardless: I finally know how to write my own translation class (I am aware that <code>MyTranslations class</code> in this post might not be at all a valid implementation.)

Furthermore, we could always argue that, since the final errors dictionary does contain field names, i.e. <code>hired_date</code> and <code>id</code>:

```
{'hired_date': ['Hired Date: Not a valid date value.'],
 'id': ['Id: Not a valid integer value.',
        'Id: Number must be between 1 and 32767.']}
```

We could always use field names to access field information from the still valid form instance, and massage the error messages. Translating into other languages can still take place -- but prior via translation also. But I don't like this approach. Regardless of the validity of this post, I did enjoy investigating this issue.

Thank you for reading. I hope you could somehow use this information... Stay safe as always.

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
<li>
<a href="https://github.com/wtforms/wtforms/issues/569" target="_blank">https://github.com/wtforms/wtforms/issues/569</a>, <a href="https://user-images.githubusercontent.com/19359364/116413884-4b4e7500-a838-11eb-83b0-704ebb3454b0.png" target="_blank">https://user-images.githubusercontent.com/19359364/116413884-4b4e7500-a838-11eb-83b0-704ebb3454b0.png</a>
</li>
</ul>