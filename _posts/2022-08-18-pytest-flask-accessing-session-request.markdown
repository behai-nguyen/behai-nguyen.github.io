---
layout: post
title: "Python: pytest accessing Flask session and request context variables."
description: How to enable pytest methods to access Flask's context variables, session and request.
tags:
- Python
- pytest 
- session
- request
---

How to enable pytest methods to access Flask's context variables, session and request.

| ![036-feature-image.png](https://behainguyen.files.wordpress.com/2022/08/036-feature-image.png) |
|:--:|
| *Python: pytest accessing Flask session and request context variables.* |

I've previously blogged about 
<span class="keyword">
pytest</span>'s 
<span class="keyword">
application fixture</span> and 
<span class="keyword">
test client fixture</span> in 
<a href="https://behainguyen.wordpress.com/2022/08/06/814/"
title="Python: pytest and Flask template context processor functions."
target="_blank">Python: pytest and Flask template context processor functions.</a>
( Please see section 
<a href="https://behainguyen.wordpress.com/2022/08/06/814/#pytest-entry-module"
title="pytest entry module conftest.py"
target="_blank">pytest entry module conftest.py</a>. )

The 
<span class="keyword">
test client fixture</span> in the mentioned post:

```python
@pytest.fixture(scope='module')
def test_client( app ):
    """
    Creates a test client.
	app.test_client() is able to submit HTTP requests.
	
    The app argument is the app() fixture above.	
    """
	
    with app.test_client() as testing_client:
        yield testing_client  # Return to caller.
```

When testing the codes that access 
<a href="https://flask.palletsprojects.com/en/2.2.x/api/#flask.session"
title="Flask’s context variable session"
target="_blank">Flask’s context variable session</a>, the above
fixture will not work. To access this variable, the official 
document states:

>If you want to access or set a value in the session **before** making a request, use the client’s <a href="https://flask.palletsprojects.com/en/2.2.x/api/#flask.testing.FlaskClient.session_transaction" title="session_transaction()" target="_blank">session_transaction()</a> method in a <span class="keyword">with</span> statement. It returns a session object, and will save the session once the block ends.
>
><a href="https://flask.palletsprojects.com/en/2.2.x/testing/" title="Testing Flask Applications" target="_blank">https://flask.palletsprojects.com/en/2.2.x/testing/</a>


I tried that, and it does not work... It's a “popular” problem.
It's been around for a few years. There are a few posts on it, 
however, most suggestions fail to work for me.

<a href="https://github.com/pytest-dev/pytest-flask/issues/69 "
title="Sessions are empty when testing #69"
target="_blank">Sessions are empty when testing #69</a>
raises this problem, and user 
<a href="https://github.com/russmac"
title="User russmac"
target="_blank">russmac</a> suggests a solution:

```python
@pytest.fixture(scope='module')
def test_client( app ):
    """
    Creates a test client.
	app.test_client() is able to submit HTTP requests.
	
    The app argument is the app() fixture above.	
    """
	
    with app.test_client() as testing_client:
        """
        See: https://github.com/pytest-dev/pytest-flask/issues/69 
		Sessions are empty when testing #69 
        """
        with testing_client.session_transaction() as session:
            session['Authorization'] = 'redacted'
			
        yield testing_client  # Return to caller.
```

This works for me. However, to access 
<a href="https://flask.palletsprojects.com/en/2.2.x/api/#flask.session"
title="Flask’s context variable session"
target="_blank">variable session</a> my test codes must be within:

```python
with app.test_request_context():
```

Or else, it raises the error 
<span class="keyword">
<span style="color:red;font-weight:bold;">RuntimeError: Working outside of request context.
</span></span>Also, without the above call, the codes proper would not
be able to access the 
<span class="keyword">
request variable</span> during testing.

Following is a proper test method of a project I'm working on:

```python
@pytest.mark.timesheet_bro
def test_close( app ):
    bro_obj = TimesheetBRO( 1 )

    #
    # RuntimeError: Working outside of request context.
    #
    # session[ 'user_id' ] = 100
    #

    with app.test_request_context( '?searchType={}'.format(UNRESTRICT_SEARCH_TYPE) ):
        assert request.args[ 'searchType' ] == UNRESTRICT_SEARCH_TYPE
        assert request.values.get( 'searchType' ) == UNRESTRICT_SEARCH_TYPE

        session[ 'user_id' ] = 1

        data = bro_obj.close( 326 )

    assert bro_obj.last_message == ''
    assert data['status']['code'] == HTTPStatus.OK.value
```

Please note, within the codes proper, 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
session[ 'user_id' ]</span> is set after a user has successfully 
logged in. Setting this value in the test codes to create a correct 
pre-condition for the codes being tested. Please also note, 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
request.values.get( 'searchType' )</span> is also used in the codes 
under testing.

Following is another proper test method which does not submit
any request parameters:

```python
@pytest.mark.timesheet_bro
def test_update_last_timesheet_id( app ):
    bro_obj = TimesheetBRO( 1 )

    with app.test_request_context():
        session[ 'user_id' ] = 1

        data = bro_obj.update_last_timesheet_id( 1, 1123 )

    assert bro_obj.last_message == ''
    assert data['status']['code'] == HTTPStatus.OK.value
```

I hope you will find this helpful at some point... And thank you for reading.
