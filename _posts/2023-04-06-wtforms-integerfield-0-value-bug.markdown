---
layout: post
title: "Python: WTForms 3.0.1 IntegerField and InputRequired do not accept 0 as valid!"
description: 0 is a valid integer value. In the latest version of WTForms, version 3.0.1, IntegerField and InputRequired don't accept 0 as valid. This appears to be an ongoing issue dating back several years. I am proposing a patch, which seems to be working for me.

tags:
- Python
- WTForms
- IntegerField
- InputRequired
---

*0 is a valid integer value. In the latest version of WTForms, version 3.0.1, IntegerField and InputRequired don't accept 0 as valid. This appears to be an ongoing issue dating back several years. I am proposing a patch, which seems to be working for me.*

| ![061-feature-image-1.png](https://behainguyen.files.wordpress.com/2023/04/061-feature-image-1.png)
|:--:|
| *Python: WTForms 3.0.1 IntegerField and InputRequired do not accept 0 as valid!* |

<a href="https://pypi.org/project/WTForms/" title="WTForms 3.0.1" target="_blank">WTForms 3.0.1</a> 
is a great validation library. And I think it is also framework-independent: we can implement
our own generic business rules classes, and use it as a basic data validation engine, we can then
use these business rules classes in any framework of our own choosing.

I have recently found an issue with it, my form has an 
<a href="https://wtforms.readthedocs.io/en/2.3.x/fields/#basic-fields" title="IntegerField" target="_blank">IntegerField</a>,
and the 
<a href="https://wtforms.readthedocs.io/en/2.3.x/validators/#built-in-validators"
title="InputRequired" target="_blank">InputRequired</a> validator, whereby <code>0</code>
is an acceptable value.

-- But <code>0</code> gets rejected!

This issue has been reported over the years, but so far, it is still 
in this latest version:

<ul>
<li style="margin-top:10px">
<a href="https://stackoverflow.com/questions/72801044/wtforms-integerfield-doesnt-work-properly-with-numberrange-as-validator"
title="WTForms IntegerField doesn't work properly with NumberRange as validator"
target="_blank">WTForms IntegerField doesn't work properly with NumberRange as validator</a>
</li>

<li style="margin-top:10px">
<a href="https://stackoverflow.com/questions/17041787/flask-wtf-how-to-allow-zero-upon-datarequired-validation"
title="Flask-WTF: How to allow zero upon DataRequired() validation"
target="_blank">Flask-WTF: How to allow zero upon DataRequired() validation</a>
</li>

<li style="margin-top:10px">
<a href="https://github.com/wtforms/wtforms/issues/100"
title="InputRequired doesn't accept 0 as valid #100"
target="_blank">InputRequired doesn't accept 0 as valid #100</a>
</li>
</ul>

Following is my attempt to reproduce this issue, and how to get around it.
❶ Create project virtual environment. ❷ Write a test script.

❶ Create project virtual environment. We will need 
<a href="https://werkzeug.palletsprojects.com/en/2.2.x/" title="Werkzeug"target="_blank">Werkzeug</a>
and 
<a href="https://pypi.org/project/WTForms/" title="WTForms 3.0.1" target="_blank">WTForms 3.0.1</a>
packages.

The test project lives under <code>/webwork/wtforms_test</code>:

```
$ cd webwork/
$ mkdir wtforms_test
$ cd wtforms_test/
behai@HP-Pavilion-15:~/webwork/wtforms_test$ virtualenv venv
behai@HP-Pavilion-15:~/webwork/wtforms_test$ source venv/bin/activate
(venv) behai@HP-Pavilion-15:~/webwork/wtforms_test$ ./venv/bin/pip install werkzeug WTForms
```

![061-01.png](https://behainguyen.files.wordpress.com/2023/04/061-01.png)

❷ Test script.

```
Content of /webwork/wtforms_test$/wtforms_bug.py
```

```python
from pprint import pprint

from werkzeug.datastructures import MultiDict

from wtforms import (    
    Form,
    IntegerField,
)

from wtforms.validators import (
    InputRequired,
    NumberRange,
)

BREAK_HOUR_01_MSG = "Break Hour must have a value."
BREAK_HOUR_02_MSG = "Break Hour is between 0 and 23."

class TestForm(Form):
    break_hour = IntegerField('Break Hour', validators=[InputRequired(BREAK_HOUR_01_MSG), 
                                                        NumberRange(0, 23, BREAK_HOUR_02_MSG)])

def validate(data: dict, form: Form) -> tuple():
    form_data = MultiDict(mapping=data)

    f = form(form_data)
    res = f.validate()
    return res, f.errors

print("\n--break_hour: -1")
res, errors = validate({'break_hour': -1}, TestForm)
print(res)
pprint(errors)

print("\n--break_hour: 'xx'")
res, errors = validate({'break_hour': 'xx'}, TestForm)
print(res)
pprint(errors)

print("\n--break_hour: 0")
res, errors = validate({'break_hour': 0}, TestForm)
print(res)
pprint(errors)

print("\n--break_hour: 1")
res, errors = validate({'break_hour': 1}, TestForm)
print(res)
pprint(errors)
```

It is simple, the form has only a single integer field <code>break_hour</code>,
it is a required field, and accepts any value in the range of <code>0</code> to
<code>23</code> -- and follows by 4 ( four ) tests.

To run:

```
(venv) behai@HP-Pavilion-15:~/webwork/wtforms_test$ venv/bin/python wtforms_bug.py
```

Output:

```
--break_hour: -1
False
{'break_hour': ['Break Hour is between 0 and 23.']}

--break_hour: 'xx'
False
{'break_hour': ['Not a valid integer value.',
                'Break Hour is between 0 and 23.']}

--break_hour: 0
False
{'break_hour': ['Break Hour must have a value.']}

--break_hour: 1
True
{}
```

![061-02.png](https://behainguyen.files.wordpress.com/2023/04/061-02.png)

<code>-1</code> and <code>'xx'</code> get rejected, which are correct.
But <code>0</code> gets rejected is a bug: <code>0</code> is a valid value.

I traced the issue to <code>InputRequired</code>, I am printing the
code for this class below:


```
InputRequired in ./venv/lib/python3.10/site-packages/wtforms/validators.py
```

```python
class InputRequired:
    """
    Validates that input was provided for this field.

    Note there is a distinction between this and DataRequired in that
    InputRequired looks that form-input data was provided, and DataRequired
    looks at the post-coercion data.

    Sets the `required` attribute on widgets.
    """

    def __init__(self, message=None):
        self.message = message
        self.field_flags = {"required": True}

    def __call__(self, form, field):
        if field.raw_data and field.raw_data[0]:
            return

        if self.message is None:
            message = field.gettext("This field is required.")
        else:
            message = self.message

        field.errors[:] = []
        raise StopValidation(message)
```

The issue is caused by the first line in <code>def __call__(self, form, field)</code>:

```python
    def __call__(self, form, field):
        if field.raw_data and field.raw_data[0]:
            return
```

<code>field.raw_data[0]</code> is evaluated to <code>0</code>, and 
it is a <code>False</code>, causing the whole <code>if</code> statement 
to evaluate to <code>False</code>.

Change it to:

```python
        if field.raw_data and len(field.raw_data):
```

And it will accept <code>0</code> as a value. The correct expected output
is now:

```
--break_hour: -1
False
{'break_hour': ['Break Hour is between 0 and 23.']}

--break_hour: 'xx'
False
{'break_hour': ['Not a valid integer value.',
                'Break Hour is between 0 and 23.']}

--break_hour: 0
True
{}

--break_hour: 1
True
{}
```

![061-03.png](https://behainguyen.files.wordpress.com/2023/04/061-03.png)

Right now, I am just having the change made locally. I am not sure what to
do with it just yet. Thank you for reading. I hope this info is useful. Stay
safe as always.

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
<a href="https://github.com/wtforms/wtforms/issues/569"
target="_blank">https://github.com/wtforms/wtforms/issues/569</a>,
<a href="https://user-images.githubusercontent.com/19359364/116413884-4b4e7500-a838-11eb-83b0-704ebb3454b0.png"
target="_blank">https://user-images.githubusercontent.com/19359364/116413884-4b4e7500-a838-11eb-83b0-704ebb3454b0.png</a>
</li>
</ul>