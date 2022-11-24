---
layout: post
title: "Python: a workaround for SQLAlchemy “Table 'sessions' is already defined” exception during tests."
description: During tests, Flask-Session intermittently causes the exception “sqlalchemy.exc.InvalidRequestError&#58; Table 'sessions' is already defined for this MetaData instance. Specify 'extend_existing=True' to redefine options and columns on an existing Table object.” I'm presenting a workaround in this post.
tags:
- Python
- Flask-Session
- pytest
- sessions
---

*During tests, Flask-Session intermittently causes the exception **“sqlalchemy.exc.InvalidRequestError: Table 'sessions' is already defined for this MetaData instance. Specify 'extend_existing=True' to redefine options and columns on an existing Table object.”** I'm presenting a workaround in this post.*

| ![048-feature-images.png](https://behainguyen.files.wordpress.com/2022/11/048-feature-images.png) |
|:--:|
| *Python: a workaround for SQLAlchemy “Table 'sessions' is already defined” exception during tests.* |

I'm using 
<span class="keyword">
pytest</span>, and I've been experiencing intermittent tests failure 
due to exception <span class="keyword danger-text">“sqlalchemy.exc.InvalidRequestError: Table 'sessions' is already defined 
for this MetaData instance. Specify 'extend_existing=True' to redefine 
options and columns on an existing Table object.”</span>. It only
occurs if some tests are run together, run them individually one at 
a time, they pass. I've ignored this problem till a few days ago. Right 
now I have around 396 ( three hundreds and ninety six ) test cases, just 
by chance, I run some three ( 3 ) tests together, and two ( 2 ) consistently 
fail with the mentioned exception, only one ( 1 ) passes.

It turns out this is an ongoing issue with 
<a href="https://pypi.org/project/Flask-Session/" title="Flask-Session 0.4.0" target="_blank">Flask-Session 0.4.0</a>,
and still persists in the latest version
<span class="keyword">
0.4.0</span>. Latest as on the 24th, November 2022.

My research led to the following post, among other posts which report the same issue:

<a href="https://stackoverflow.com/questions/64721498/how-do-you-resolve-already-defined-in-this-metadata-instance-error-with-flask"
title="How do you resolve 'Already defined in this MetaData Instance' Error with Flask Pytest, SqlAlchemy, and Flask Sessions?"
target="_blank">How do you resolve 'Already defined in this MetaData Instance' Error with Flask Pytest, SqlAlchemy, and Flask Sessions?</a>
The answer by 
<a href="https://stackoverflow.com/users/8141870/tassaron" title="Tassaron" target="_blank">user Tassaron</a>
on 01/01/2021 leads to the following URLs:

<ul>
<li style="margin-top:5px;">
<a href="https://github.com/fengsp/flask-session/blob/1c1f7903184673682bd1d75432c8f455b62393a4/flask_session/sessions.py"
title="https://github.com/fengsp/flask-session/blob/1c1f7903184673682bd1d75432c8f455b62393a4/flask_session/sessions.py"
target="_blank">https://github.com/fengsp/flask-session/blob/1c1f7903184673682bd1d75432c8f455b62393a4/flask_session/sessions.py</a>
</li>

<li style="margin-top:10px;">
<a href="https://github.com/tassaron/muffin-shop/blob/main/src/helpers/main/session_interface.py"
title="https://github.com/tassaron/muffin-shop/blob/main/src/helpers/main/session_interface.py"
target="_blank">https://github.com/tassaron/muffin-shop/blob/main/src/helpers/main/session_interface.py</a>
</li>

<li style="margin-top:15px;">
<a href="https://github.com/fengsp/flask-session/pull/12"
title="https://github.com/fengsp/flask-session/pull/12" target="_blank">https://github.com/fengsp/flask-session/pull/12</a>
</li>
</ul>

The general consensus seems to be only creating the
<span class="keyword">
Model</span> for the database session table only if it does not already
exists via the condition:

```python
if table not in self.db.metadata:
```

It has been proposed a few years back, but for some reasons, it has not been 
implemented by the author.

Tassaron, herself, has implemented this in 
<a href="https://github.com/tassaron/muffin-shop/blob/main/src/helpers/main/session_interface.py"
title="https://github.com/tassaron/muffin-shop/blob/main/src/helpers/main/session_interface.py"
target="_blank">https://github.com/tassaron/muffin-shop/blob/main/src/helpers/main/session_interface.py</a>:

```python
class TassaronSessionInterface(SessionInterface):
    ...

    def __init__(self, app, db):
        ...

        if table not in self.db.metadata:
            # ^ Only create Session Model if it doesn't already exist
            # Fixes the SQLAlchemy "extend_existing must be true" exception during tests
            class Session(self.db.Model):
                ...
            self.sql_session_model = db.session_ext_session_model = Session
        else:
            self.sql_session_model = db.session_ext_session_model
```

Compared to the original 
<a href="https://pypi.org/project/Flask-Session/" title="Flask-Session 0.4.0" target="_blank">Flask-Session 0.4.0</a>:

```python
class SqlAlchemySessionInterface(SessionInterface):
    ...

    def __init__(self, app, db, table, key_prefix, use_signer=False,
                 permanent=True):
        ...

        class Session(self.db.Model):
            ...

        self.sql_session_model = Session
```

In
<span class="keyword">
TassaronSessionInterface</span>, when the 
<span class="keyword">
Session Model</span> is first created, it also gets assigned to 
<span class="keyword">
db</span> new attribute 
<span class="keyword">
session_ext_session_model</span>, afterwards 
<span class="keyword">
db.session_ext_session_model</span> is used.

Apart from exceptions intermittently raised during tests,
<a href="https://pypi.org/project/Flask-Session/" title="Flask-Session 0.4.0" target="_blank">Flask-Session 0.4.0</a>
works fine. I want to stick to it as much as possible. Following is my attempt, 
<strong>it feels like a workaround, a hack rather than a solution, I'm okay with
this for the time being</strong>:

```
Content of fixed_session.py
```

```python
from flask_session.sessions import SqlAlchemySessionInterface
from flask_session import Session

class FixedSqlAlchemySessionInterface( SqlAlchemySessionInterface ):
    def __init__(self, app, db, table, key_prefix, use_signer=False,
                 permanent=True):
        """
        Assumption: the way I use it, db is always a valid instance 
        at this point.
        """
        if table not in db.metadata:
            super().__init__( app, db, table, key_prefix, use_signer, permanent )
            db.session_ext_session_model = self.sql_session_model
        else:
            # print( "`sessions` table already exists..." )

            self.db = db
            self.key_prefix = key_prefix
            self.use_signer = use_signer
            self.permanent = permanent
            self.has_same_site_capability = hasattr(self, "get_cookie_samesite")

            self.sql_session_model = db.session_ext_session_model
            
class FixedSession( Session ):
    def _get_interface(self, app):
        config = app.config.copy()

        if config[ 'SESSION_TYPE' ] != 'sqlalchemy':
            return super()._get_interface( app )

        else:
            config.setdefault( 'SESSION_PERMANENT', True )
            config.setdefault( 'SESSION_KEY_PREFIX', 'session:' )

            return FixedSqlAlchemySessionInterface(
                app, config['SESSION_SQLALCHEMY'],
                config['SESSION_SQLALCHEMY_TABLE'],
                config['SESSION_KEY_PREFIX'], config['SESSION_USE_SIGNER'],
                config['SESSION_PERMANENT'] )
```

To use this implementation, import
<span class="keyword">
FixedSession</span> as 
<span class="keyword">
Session</span>, then carry on as normal:

```python
try:
    from xxx.yyyy.fixed_session import FixedSession as Session
except ImportError:
    from flask_session import Session
```

When 
<span class="keyword">
Flask-Session</span> is fixed, I can just remove
<span class="keyword">
fixed_session.py</span> without needing to update any codes -- 
however, I should update the import, exceptions are expensive.

Back to my attempt, in 
<span class="keyword">
FixedSqlAlchemySessionInterface</span>, I copied the idea of
<span class="keyword">
db.session_ext_session_model</span> from
<span class="keyword">
TassaronSessionInterface</span>. The following lines are copied from
the original codes:

```python
            self.db = db
            self.key_prefix = key_prefix
            self.use_signer = use_signer
            self.permanent = permanent
            self.has_same_site_capability = hasattr(self, "get_cookie_samesite")
```

That means, if
<span class="keyword">
Flask-Session</span> gets updated without fixing this issue, I might
have to update my codes!

In 
<span class="keyword">
class FixedSession</span>, the following lines in the overridden method <span class="keyword">def _get_interface(self, app):</span>

```python
            config.setdefault( 'SESSION_PERMANENT', True )
            config.setdefault( 'SESSION_KEY_PREFIX', 'session:' )
```

are also copied from the original codes, I never have 
<span class="keyword">SESSION_PERMANENT</span> and 
<span class="keyword">SESSION_KEY_PREFIX</span> in my environment variables file.

With, or without the 
<span class="keyword">
“sessions”</span> table in the database, my tests and application
run with no problems. If I drop 
<span class="keyword">
“sessions”</span> table, it gets created as expected.

It's been fun investigating this issue. I'm not too happy with 
my code, but it works for me for the time being. Hopefully, the 
author will fix it in the future releases. In the meantime, I 
really do hope this post helps others whom come across this 
same problem. Thank you for reading and stay safe as always.
