---
layout: post
title: "Python: SQLAlchemy -- understanding sessions and associated queries."
description: In this post, we look at some of the basics of sessionmaker, scoped_session and their associated query methods.
tags:
- Python
- SQLAlchemy
- session
- query
---

*In this post, we look at some of the basics of sessionmaker, scoped_session and their associated query methods.*

| ![050-feature-images.png](https://behainguyen.files.wordpress.com/2022/12/050-feature-images.png) |
|:--:|
| *SQLAlchemy -- understanding sessions and associated queries.* |

Please note that this post is not a tutorial. I sought to answer some
of my own questions. And I'm merely writing down my answers.

The source database used in this post is the
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
MySQL test data </span>		
released by Oracle Corporation. Downloadable from
<a href="https://github.com/datacharmer/test_db" title="MySQL test data " target="_blank">https://github.com/datacharmer/test_db</a>.

Let's start with the Session class. SQLAlchemy official documentation 
<a href="https://docs.sqlalchemy.org/en/14/orm/session.html#lifespan-of-a-contextual-session"
title="Using the Session" target="_blank">Using the Session</a>.

❶ We can use instances of 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
sessionmaker</span> to run full text queries:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://behai:pcb.2176310315865259@localhost/employees"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False, future=True)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

session = session_factory()

sql = "select * from employees where last_name like '%treh%' limit 0, 10"

dataset = session.execute(text(sql))
for r in dataset:
    print(r)

dataset.close()
session.close()
```

For 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
future=True</span>, please see 
<a href="https://docs.sqlalchemy.org/en/14/core/future.html"
title="SQLAlchemy 2.0 Future (Core)" target="_blank">SQLAlchemy 2.0 Future (Core)</a>

❷ Next comes the 
<span class="keyword">
scoped_session</span>. Basically, it is the session that we should use in 
web applications: each scoped session is “local” to the context a 
web request. Please see 
<a href="https://docs.sqlalchemy.org/en/14/orm/contextual.html#unitofwork-contextual" 
title="Contextual/Thread-local Sessions" target="_blank">Contextual/Thread-local Sessions</a>.

For the purpose of this discussion, we will not be doing any web applications.
Simple command line Python scripts would suffice for illustration purposes:

```python
from threading import get_ident
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import text

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://behai:pcb.2176310315865259@localhost/employees"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False, future=True)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

database_sesssion = scoped_session(session_factory, scopefunc=get_ident)

session = database_sesssion(future=True)

sql = "select * from employees where last_name like '%treh%' limit 0, 10"

dataset = session.execute(text(sql))
for r in dataset:
    print(r)

dataset.close()
session.close()
```

This script does the same thing as the previous one, barring one addition,
and one modification:

The addition is 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
line 12</span>:

```python
database_sesssion = scoped_session(session_factory, scopefunc=get_ident)
```

For 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
scopefunc=get_ident</span>, please see 
<a href="https://docs.sqlalchemy.org/en/14/orm/contextual.html#sqlalchemy.orm.scoping.scoped_session"
title="sqlalchemy.orm.scoping.scoped_session" target="_blank">sqlalchemy.orm.scoping.scoped_session</a>,
and this Stackoverflow post 
<a href="https://stackoverflow.com/questions/71695691/flask-app-ctx-stack-ident-func-error-due-to-ident-func-deprecated-in-we"
title="flask _app_ctx_stack.__ident_func__ error due to __ident_func__ deprecated in werkzeug 2.1"
target="_blank">flask _app_ctx_stack.__ident_func__ error due to __ident_func__ deprecated in werkzeug 2.1</a>
should make it clearer.

The modification is 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
line 14</span>:

```python
session = database_sesssion(future=True)
```

In this second script, instead of getting a session directly from 
<span class="keyword">
sessionmaker</span>, we get one indirectly from 
<span class="keyword">
scoped_session</span>. We are running the same query as the previous script, 
so the final output is also the same.

<div style="background-color:yellow;width:100%;height:100px;display:flex;">
    <div style="flex:100px;height:100px;
	    background-image:url('https://behainguyen.files.wordpress.com/2022/12/info-symbol.png');
		background-repeat: no-repeat;
		background-position: center center;
		background-size:100px 100px;">
    </div>

	<div style="flex:550px;font-weight:bold;color:blue;
	    padding-right:40px;padding-left:40px;height:100px;display:flex;align-items:center;">
		<div style="height:60px;">
           From here on, scripts all have lines 1-12 ( one to twelve ) identical,
		   I will only list the relevant new codes for the current discussions.
		</div>
	</div>
</div>

❸ According to 
<a href="https://docs.sqlalchemy.org/en/14/orm/contextual.html#unitofwork-contextual" 
title="Contextual/Thread-local Sessions" target="_blank">Contextual/Thread-local Sessions</a>,
after:

```python
session = database_sesssion(future=True)
```

If we make repeated calls to 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
database_sesssion()</span>, we get back the same session:

```python
...
session = database_sesssion(future=True)
session1 = database_sesssion()

print(f"1. database_sesssion: {id(database_sesssion)}")
print(f"1. session: {id(session)}")
print(f"1. session1: {id(session1)}")
print(f"1. session is session1: {session is session1}")
```

```
1. database_sesssion: 1724058633408
1. session: 1724061992896
1. session1: 1724061992896
1. session is session1: True
```

We can call
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
database_sesssion(future=True)</span> only once, subsequent calls must be
made with no parameters, otherwise it will result in the following exception:

```
(venv) F:\my_project>venv\Scripts\python.exe src\my_project\my_python_script.py
Traceback (most recent call last):
  File "F:\my_project\src\my_project\my_python_script.py", line 15, in <module>
    session1 = database_sesssion(future=True)
  File "F:\my_project\venv\lib\site-packages\sqlalchemy\orm\scoping.py", line 39, in __call__
    raise sa_exc.InvalidRequestError(
sqlalchemy.exc.InvalidRequestError: Scoped session is already present; no new arguments may be specified.
```

❹ According to 
<a href="https://docs.sqlalchemy.org/en/13/orm/contextual.html#sqlalchemy.orm.scoping.scoped_session.remove"
title="method sqlalchemy.orm.scoping.scoped_session.remove()" 
target="_blank">method sqlalchemy.orm.scoping.scoped_session.remove()</a>:

> Dispose of the current Session, if present.
> 
> This will first call Session.close() method on the current Session, which releases any existing transactional/connection resources still being held; transactions specifically are rolled back. The Session is then discarded. Upon next usage within the same scope, the scoped_session will produce a new Session object.

Let's see what that means, the following script produces the 
same results as the first script:

```python
...
session = database_sesssion(future=True)
session.close()

database_sesssion.remove()

session = database_sesssion(future=True)

sql = "select * from employees where last_name like '%treh%' limit 0, 10"

dataset = session.execute(text(sql))
for r in dataset:
    print(r)

dataset.close()
session.close()
```

After calling 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
database_sesssion.remove()</span>, a subsequent call with parameter 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
session = database_sesssion(future=True)</span> actually works, it does not 
raise an exception.

This makes sense in the context of the above statement: the internal registry is now empty, 
there is no active scoped session present, so we can create a new one with whatever configurations
we see fit.

This would suggest that the <span class="keyword">
database_sesssion</span> itself is still the same object after calling 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
database_sesssion.remove()</span>. Let's test it out with the following script:

```python
...
session = database_sesssion(future=True)
session1 = database_sesssion()

print(f"1. database_sesssion: {id(database_sesssion)}")
print(f"1. session: {id(session)}")
print(f"1. session1: {id(session1)}")
print(f"1. session is session1: {session is session1}")

session1.close()
session.close()

database_sesssion.remove()

session = database_sesssion(future=True)
session1 = database_sesssion()

print(f"2. database_sesssion: {id(database_sesssion)}")
print(f"2. session: {id(session)}")
print(f"2. session1: {id(session1)}")
```

We can see that it is, in the output:

```
1. database_sesssion: 2102627796160
1. session: 2102631155648
1. session1: 2102631155648
1. session is session1: True
2. database_sesssion: 2102627796160
2. session: 2102631155792
2. session1: 2102631155792
```

❺ We will introduce a model, which basically is a SQLAlchemy class representation 
of a database table. As per documentation, we will descend our model from 
<a href="https://docs.sqlalchemy.org/en/14/orm/mapping_api.html#sqlalchemy.orm.declarative_base"
title="function sqlalchemy.orm.declarative_base(...)" 
target="_blank">function sqlalchemy.orm.declarative_base(...)</a>, then we can 
use 
<a href="https://docs.sqlalchemy.org/en/14/orm/contextual.html#sqlalchemy.orm.scoping.scoped_session.query_property"
title="method sqlalchemy.orm.scoping.scoped_session.query_property(query_cls=None)"
target="_blank">method sqlalchemy.orm.scoping.scoped_session.query_property(query_cls=None)</a>
with this model. We will do a model for the 
<span class="keyword">
<strong>employees</strong></span> table.

<a id="five-dash-one">❺⓵</a> Despite the official document example, I wanted to try using 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
database_sesssion.query_property()</span> directly, this is my first attempt
( I'm listing a complete new script ):

```python
from threading import get_ident
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Date,
    String,
)
from sqlalchemy.orm import sessionmaker, scoped_session
"""
Any one of these import of declarative_base will work.
"""
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://behai:pcb.2176310315865259@localhost/employees"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False, future=True)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

database_sesssion = scoped_session(session_factory, scopefunc=get_ident)

class Employees(declarative_base()):
    __tablename__ = 'employees'

    emp_no = Column(Integer, primary_key=True)
    birth_date = Column(Date, nullable=False)
    first_name = Column(String(14), nullable=False)
    last_name = Column(String(16), nullable=False)
    gender = Column(String(1), nullable=False )
    hire_date = Column(Date, nullable=False )

query = database_sesssion.query_property()
result = query.filter(Employees.emp_no==16621).first()
```

I did expect it to work, but it did not:

```
(venv) F:\my_project>venv\Scripts\python.exe src\my_project\my_python_script.py
Traceback (most recent call last):
  File "F:\my_project\src\my_project\my_python_script.py", line 35, in <module>
    result = query.filter(Employees.emp_no==16621).first()
AttributeError: 'query' object has no attribute 'filter'
```

<div style="background-color:yellow;width:100%;height:100px;display:flex;">
    <div style="flex:100px;height:100px;
	    background-image:url('https://behainguyen.files.wordpress.com/2022/12/info-symbol.png');
		background-repeat: no-repeat;
		background-position: center center;
		background-size:100px 100px;">
    </div>

	<div style="flex:550px;font-weight:bold;color:blue;
	    padding-right:40px;padding-left:40px;height:100px;display:flex;align-items:center;">
		<div style="height:80px;">
           From here on, scripts will have lines 1-22 ( one to twenty two ) identical
		   to <a href="#five-dash-one">❺⓵</a>,
		   I will only list the relevant additions and changes for the current discussions.
		</div>
	</div>
</div>

<a id="five-dash-two">❺⓶</a> The example snippet listed under 
<a href="https://docs.sqlalchemy.org/en/14/orm/contextual.html#sqlalchemy.orm.scoping.scoped_session.query_property"
title="method sqlalchemy.orm.scoping.scoped_session.query_property(query_cls=None)"
target="_blank">method sqlalchemy.orm.scoping.scoped_session.query_property(query_cls=None)</a> is:

```python
<pre>
Session = scoped_session(sessionmaker())

class MyClass(object):
    query = Session.query_property()

# after mappers are defined
result = MyClass.query.filter(MyClass.name=='foo').all()
```

Accordingly, I modify <a href="#five-dash-one">❺⓵</a> as follows:

```python
...
class BaseModel(object):
    query = database_sesssion.query_property()

Base = declarative_base(cls=BaseModel)

class Employees(Base):
    __tablename__ = 'employees'

    ...

result = Employees.query.filter(Employees.emp_no==16621).first()
print(result.__dict__)
```

And it does work as expected:

```
(venv) F:\my_project>venv\Scripts\python.exe src\my_project\my_python_script.py
{'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x0000026A680079A0>, 'last_name': 'Strehl', 'emp_no': 16621, 'hire_date': datetime.date(1992, 6, 11), 'first_name': 'Parviz', 'gender': 'M', 'birth_date': datetime.date(1962, 5, 30)}
```

<strong>I don't know why it has to be like this. But the official document 
states that it must be, and my experimentation confirms it.</strong> I'm not 
going to dig into the SQLAlchemy codes to see why! I have a feeling that it's 
going to be futile, too 😂...

We've seen previously that 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
scoped_session(...)([...])</span> and 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
sessionmaker(...)()</span> both result in a 
<a href="https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session"
title="class sqlalchemy.orm.Session(...)"
target="_blank">class sqlalchemy.orm.Session(...)</a>, and this class has a 
<a href="https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session.query"
title="method sqlalchemy.orm.Session.query(*entities, **kwargs)"
target="_blank">method sqlalchemy.orm.Session.query(*entities, **kwargs)</a>.
This method can be used to do what 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
scoped_session(...).query_property()</span> does, barring some differences. 
The first is that the model can descend directly from 
<span class="keyword">
declarative_base()</span>. Secondly, the syntax is slightly different.

<a id="five-dash-three">❺⓷</a>The modified script which uses
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
scoped_session(...)([...])'s</span>
<span class="keyword">
query() method</span>:

```python
...
class Employees(declarative_base()):
    __tablename__ = 'employees'

    ...

session = database_sesssion(future=True)
result = session.query(Employees).filter(Employees.emp_no==10545).first()
print( result.__dict__ )
```

<a id="five-dash-four">❺⓸</a> And similarly for 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
sessionmaker(...)()</span>:

```python
...
class Employees(declarative_base()):
    __tablename__ = 'employees'

    ...

session = session_factory()
result = session.query(Employees).filter(Employees.emp_no==11000).first()
print( result.__dict__ )
```

Let's reiterate that we use
<span class="keyword">
scoped_session</span> with web applications -- 
<a href="https://docs.sqlalchemy.org/en/14/orm/contextual.html#unitofwork-contextual" 
title="Contextual/Thread-local Sessions" target="_blank">Contextual/Thread-local Sessions</a>.
We include <span class="keyword">
sessionmaker</span> for the shake of comparison and completeness. Back to 
<span class="keyword">
scoped_session's query() method and query property</span>:

● <a href="#five-dash-two">❺⓶</a>: 
<span class="keyword">
result = Employees.query.filter(Employees.emp_no==16621).first()</span>

● <a href="#five-dash-three">❺⓷</a>: 
<span class="keyword">
result = session.query(Employees).filter(Employees.emp_no==10545).first()</span>

I choose to use <a href="#five-dash-two">❺⓶</a> approach, despite having to have
an extra base class. I.e.:

```python
class BaseModel(object):
    query = database_sesssion.query_property()
```

This 
<span class="keyword">
BaseModel</span> can be the parent class for all of the database tables, 
so in the long run, it sort of pays for itself. 

✿✿✿

As I have stated up front, this post is not a tutorial. I find SQLAlchemy 
to be a tough row to hoe... I set out to answer my own questions. I hope
the content of this post will be useful for others who are learning 
SQLAlchemy. I do hope I have not made any mistakes in this post. Thank 
you for reading and stay safe as always.
