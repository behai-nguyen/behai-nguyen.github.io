---
layout: post
title: "Python: SQLAlchemy -- user-defined query classes for scoped_session.query_property(query_cls=None)."
description: We are discussing SQLAlchemy user-defined query classes. A user-defined query class can be passed to scoped_session.query_property(query_cls=None) in place of parameter query_cls, i.e. scoped_session.query_property(MyQuery).
tags:
- Python
- SQLAlchemy
- scoped_session
- query_property
- query_cls
---

*We are discussing SQLAlchemy user-defined query classes. A user-defined query class can be passed to scoped_session.query_property(query_cls=None) in place of parameter query_cls: i.e. scoped_session.query_property(MyQuery).*

| ![051-feature-image.png](https://behainguyen.files.wordpress.com/2022/12/051-feature-image.png) |
|:--:|
| *Python: SQLAlchemy -- user-defined query classes for scoped_session.query_property(query_cls=None).* |

<p>
SQLAlchemy's <code>scoped_session.query_property(query_cls=None)</code> accepts a 
user-defined query class via parameter 
<code>query_cls</code>. If one is provided, then when we use
<code>scoped_session.query property</code> to query the database, our 
user-defined query class will be used instead of the default one.
</p>

<p>
This post is a continuation of 
<a href="https://behainguyen.wordpress.com/2022/12/14/python-sqlalchemy-understanding-sessions-and-associated-queries/"
title="Python: SQLAlchemy — understanding sessions and associated queries."
target="_blank">Python: SQLAlchemy — understanding sessions and associated queries</a>; 
we have previous touched 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
scoped_session.query_property(query_cls=None)</span> in 
<a href="https://behainguyen.wordpress.com/2022/12/14/python-sqlalchemy-understanding-sessions-and-associated-queries/#five-dash-one"
title="Python: SQLAlchemy — understanding sessions and associated queries"
target="_blank">point ❺⓵</a> and 
<a href="https://behainguyen.wordpress.com/2022/12/14/python-sqlalchemy-understanding-sessions-and-associated-queries/#five-dash-two"
title="Python: SQLAlchemy — understanding sessions and associated queries"
target="_blank">point ❺⓶</a>, but we did not do user-defined query class: 
<em>we are looking at it in this post.</em>
</p>

<p>
The source database used is still the
<span class="keyword">
MySQL test data</span> released by Oracle Corporation. Downloadable from
<a href="https://github.com/datacharmer/test_db" title="MySQL test data " target="_blank">https://github.com/datacharmer/test_db</a>.
And we continue with the 
<span class="keyword">
<strong>employees</strong></span> table and the 
<span class="keyword">
<strong>Employees</strong></span> class.
</p>

<p>
Let's get to the codes, and we'll discuss documentation later.
</p>

{% highlight python linenos %}
from threading import get_ident
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Date,
    String,
)
from sqlalchemy.orm import (
    sessionmaker, 
    scoped_session, 
    declarative_base, 
    Query,
)

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:pcb.2176310315865259@localhost/employees"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False, future=True)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

database_sesssion = scoped_session(session_factory, scopefunc=get_ident)

class BaseQuery(Query):
    def print_all(self):        
        print(f"\nThere are {self.count()} rows.")

        resultset = self.all()
        for row in resultset:
            print(row.__dict__)

        return self

class BaseModel(object):
    query = database_sesssion.query_property(BaseQuery)

    @classmethod
    def set_query(cls, query_cls: Query) -> None:
        cls.query = database_sesssion.query_property(query_cls)

Base = declarative_base(cls=BaseModel)

class Employees(Base):
    __tablename__ = 'employees'

    emp_no = Column(Integer, primary_key=True)
    birth_date = Column(Date, nullable=False)
    first_name = Column(String(14), nullable=False)
    last_name = Column(String(16), nullable=False)
    gender = Column(String(1), nullable=False )
    hire_date = Column(Date, nullable=False )
{% endhighlight %}

<ul>
<li style="margin-top:10px;">
Lines 1-22 -- this block is a repeat from the last mentioned post. We're 
just establishing the database connection, leading to defining our 
<code>scoped_session</code> session.
</li>

<li style="margin-top:10px;">
Lines 41-51 -- this block is also a repeat. We're defining our 
<code>Employees</code> declarative model.
</li>

<li style="margin-top:10px;">
Lines 24-32 -- this is our user-defined query class:
</li>
</ul>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code><table class="rouge-table"><tbody><tr><td class="rouge-gutter gl"><pre class="lineno">24
25
26
27
28
29
30
31
32
</pre></td><td class="rouge-code"><pre><span class="k">class</span> <span class="nc">BaseQuery</span><span class="p">(</span><span class="n">Query</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">print_all</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>        
        <span class="k">print</span><span class="p">(</span><span class="sa">f</span><span class="s">"</span><span class="se">\n</span><span class="s">There are </span><span class="si">{</span><span class="bp">self</span><span class="p">.</span><span class="n">count</span><span class="p">()</span><span class="si">}</span><span class="s"> rows."</span><span class="p">)</span>

        <span class="n">resultset</span> <span class="o">=</span> <span class="bp">self</span><span class="p">.</span><span class="nb">all</span><span class="p">()</span>
        <span class="k">for</span> <span class="n">row</span> <span class="ow">in</span> <span class="n">resultset</span><span class="p">:</span>
            <span class="k">print</span><span class="p">(</span><span class="n">row</span><span class="p">.</span><span class="n">__dict__</span><span class="p">)</span>

        <span class="k">return</span> <span class="bp">self</span>
</pre></td></tr></tbody></table></code></pre></div></div>

<ul style="list-style-type: none;">
<li style="margin-top:10px;">
<p>
A user-defined query class must descend from 
<code>sqlalchemy.orm.Query</code>. <code>BaseQuery</code> defines its own
method <code>print_all()</code>, which get all available results from a
<em>previous method call (✿)</em>, and for each row, prints out the value
of the <code>__dict__</code> attribute. And finally <code>print_all()</code>
returns <code>self</code>: this is to maintain methods chainability.
</p>
<p>
(✿) <em>previous method call</em>: e.g. <code>filter(...)</code>, which 
also maintains methods chainability.
</p>
</li>
</ul>

<ul>
<li style="margin-top:10px;">
Lines 34-39 -- our <code>BaseModel</code>:
</li>
</ul>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code><table class="rouge-table"><tbody><tr><td class="rouge-gutter gl"><pre class="lineno">34
35
36
37
38
39
</pre></td><td class="rouge-code"><pre><span class="k">class</span> <span class="nc">BaseModel</span><span class="p">(</span><span class="nb">object</span><span class="p">):</span>
    <span class="n">query</span> <span class="o">=</span> <span class="n">database_sesssion</span><span class="p">.</span><span class="n">query_property</span><span class="p">(</span><span class="n">BaseQuery</span><span class="p">)</span>

    <span class="o">@</span><span class="nb">classmethod</span>
    <span class="k">def</span> <span class="nf">set_query</span><span class="p">(</span><span class="n">cls</span><span class="p">,</span> <span class="n">query_cls</span><span class="p">:</span> <span class="n">Query</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="bp">None</span><span class="p">:</span>
        <span class="n">cls</span><span class="p">.</span><span class="n">query</span> <span class="o">=</span> <span class="n">database_sesssion</span><span class="p">.</span><span class="n">query_property</span><span class="p">(</span><span class="n">query_cls</span><span class="p">)</span>
</pre></td></tr></tbody></table></code></pre></div></div>

<ul style="list-style-type: none;">
<li style="margin-top:10px;">
We've used a simpler version of this <code>BaseModel</code> 
in the previously mentioned post, too. This time, we define 
our own query class, via:
</li>
</ul>

```python
    query = database_sesssion.query_property(BaseQuery)
```

<ul style="list-style-type: none;">
<li style="margin-top:10px;">
<p>
That means <code>BaseQuery</code> is the default query class for any model
which has <code>BaseModel</code> as a base class. So, <code>BaseQuery</code> 
is the default query class for the <code>Employees</code> model.
</p>

<p>
Another new addition to the <code>BaseModel</code> is the class method <code>set_query(...)</code>.
This is an experimentation as we shall see later: I was wondering if we could swap out 
<code>BaseQuery</code>, and replace it with another new user-defined query class like this:
</p>
</li>
</ul>

```python
Employees.set_query(SerialiseQuery)
```

<p>
We'll discuss it more in the next example. Back to this example, now that 
our classes are in place. Let's test out our custom query:
</p>

```python
result = Employees.query.filter(Employees.emp_no==16621)
print(type(result))
```

<p>
The output:
</p>

```
<class '__main__.BaseQuery'>
```

<p>
As mentioned previously, <code>filter(...)</code> maintains methods 
chainability, the output should make sense -- we can call other 
<code>BaseQuery</code>'s methods using <code>result</code>:
</p>

<p>
❶ The followings are equivalent and should produce the same output:
</p>

```python
result.print_all()
Employees.query.filter(Employees.emp_no==16621).print_all()
```

<p>
Both give:
</p>

```
There are 1 rows.
{'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x0000022903034AC0>, 'last_name': 'Strehl', 'emp_no': 16621, 'hire_date': datetime.date(1992, 6, 11), 'first_name': 'Parviz', 'gender': 'M', 'birth_date': datetime.date(1962, 5, 30)}
```

<p>
❷ Similarly:
</p>

```python
print(result.first().__dict__)
print(Employees.query.filter(Employees.emp_no==16621).first().__dict__)
```

```
{'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x000001B91670BE50>, 'first_name': 'Parviz', 'gender': 'M', 'birth_date': datetime.date(1962, 5, 30), 'last_name': 'Strehl', 'emp_no': 16621, 'hire_date': datetime.date(1992, 6, 11)}
```

<p>
❸ Consider the following two statements:
</p>

```python
first_rec = Employees.query.filter(Employees.hire_date.between('2000-01-01', '2000-12-31'))\
    .order_by(Employees.emp_no).print_all().first()
	
print(first_rec.__dict__)
```

<p>
We're selecting all employees whom have been hired during the year 2000, order by 
integer primary key column 
<span class="keyword">emp_no</span>,
then we call to method <code>print_all()</code> to display all rows, finally we 
call method <code>first()</code>, which returns the result to variable
<code>first_rec</code>. Finally, we print the value of <code>first_rec</code>'s
<code>__dict__</code> attribute.
</p>

<p>
-- We've discussed how <code>print_all()</code> maintains method chainability
earlier.
</p>

<p>
For this next example, we add another user-defined query class <code>SerialiseQuery</code>,
which via its own <code>serialise()</code> method, converts each data row into a dictionary 
by calling model new method <code>as_dict()</code>, and returns all dictionaries as a list, 
in a new attribute <code>serialised_array</code>. Method <code>serialise()</code> must also 
maintain chainability. New method <code>as_dict()</code> is added onto <code>BaseModel</code>. 
The new example, lines 1-22 ( one to twenty two ) are identical to the previous example:
</p>

<!-- TO_DO: -->
<figure class="highlight"><pre><code class="language-python" data-lang="python"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
</pre></td><td class="code"><pre><span class="p">...</span>
<span class="k">class</span> <span class="nc">BaseQuery</span><span class="p">(</span><span class="n">Query</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">print_all</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>        
        <span class="k">print</span><span class="p">(</span><span class="sa">f</span><span class="s">"</span><span class="se">\n</span><span class="s">There are </span><span class="si">{</span><span class="bp">self</span><span class="p">.</span><span class="n">count</span><span class="p">()</span><span class="si">}</span><span class="s"> rows."</span><span class="p">)</span>

        <span class="n">resultset</span> <span class="o">=</span> <span class="bp">self</span><span class="p">.</span><span class="nb">all</span><span class="p">()</span>
        <span class="k">for</span> <span class="n">row</span> <span class="ow">in</span> <span class="n">resultset</span><span class="p">:</span>
            <span class="k">print</span><span class="p">(</span><span class="n">row</span><span class="p">.</span><span class="n">__dict__</span><span class="p">)</span>

        <span class="k">return</span> <span class="bp">self</span>

<span class="k">class</span> <span class="nc">SerialiseQuery</span><span class="p">(</span><span class="n">BaseQuery</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">serialise</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="bp">self</span><span class="p">.</span><span class="n">serialised_array</span> <span class="o">=</span> <span class="p">[]</span>
        <span class="n">resultset</span> <span class="o">=</span> <span class="bp">self</span><span class="p">.</span><span class="nb">all</span><span class="p">()</span>
        <span class="k">for</span> <span class="n">row</span> <span class="ow">in</span> <span class="n">resultset</span><span class="p">:</span>
            <span class="bp">self</span><span class="p">.</span><span class="n">serialised_array</span><span class="p">.</span><span class="n">append</span><span class="p">(</span><span class="n">row</span><span class="p">.</span><span class="n">as_dict</span><span class="p">())</span>

        <span class="k">return</span> <span class="bp">self</span>

<span class="k">class</span> <span class="nc">BaseModel</span><span class="p">(</span><span class="nb">object</span><span class="p">):</span>
    <span class="n">query</span> <span class="o">=</span> <span class="n">database_sesssion</span><span class="p">.</span><span class="n">query_property</span><span class="p">(</span><span class="n">BaseQuery</span><span class="p">)</span>

    <span class="o">@</span><span class="nb">classmethod</span>
    <span class="k">def</span> <span class="nf">set_query</span><span class="p">(</span><span class="n">cls</span><span class="p">,</span> <span class="n">query_cls</span><span class="p">:</span> <span class="n">Query</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="bp">None</span><span class="p">:</span>
        <span class="n">cls</span><span class="p">.</span><span class="n">query</span> <span class="o">=</span> <span class="n">database_sesssion</span><span class="p">.</span><span class="n">query_property</span><span class="p">(</span><span class="n">query_cls</span><span class="p">)</span>

    <span class="k">def</span> <span class="nf">as_dict</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="s">"""
        Converts an instance to dictionary.

        References:
            https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
            How to serialize SqlAlchemy result to JSON?
            https://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
            How to convert SQLAlchemy row object to a Python dict?
        """</span>
        <span class="k">return</span> <span class="p">{</span> <span class="n">c</span><span class="p">.</span><span class="n">name</span><span class="p">:</span> <span class="nb">getattr</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">c</span><span class="p">.</span><span class="n">name</span><span class="p">)</span> <span class="k">for</span> <span class="n">c</span> <span class="ow">in</span> <span class="bp">self</span><span class="p">.</span><span class="n">__table__</span><span class="p">.</span><span class="n">columns</span> <span class="p">}</span>

<span class="n">Base</span> <span class="o">=</span> <span class="n">declarative_base</span><span class="p">(</span><span class="n">cls</span><span class="o">=</span><span class="n">BaseModel</span><span class="p">)</span>

<span class="k">class</span> <span class="nc">Employees</span><span class="p">(</span><span class="n">Base</span><span class="p">):</span>
    <span class="n">__tablename__</span> <span class="o">=</span> <span class="s">'employees'</span>

    <span class="n">emp_no</span> <span class="o">=</span> <span class="n">Column</span><span class="p">(</span><span class="n">Integer</span><span class="p">,</span> <span class="n">primary_key</span><span class="o">=</span><span class="bp">True</span><span class="p">)</span>
    <span class="n">birth_date</span> <span class="o">=</span> <span class="n">Column</span><span class="p">(</span><span class="n">Date</span><span class="p">,</span> <span class="n">nullable</span><span class="o">=</span><span class="bp">False</span><span class="p">)</span>
    <span class="n">first_name</span> <span class="o">=</span> <span class="n">Column</span><span class="p">(</span><span class="n">String</span><span class="p">(</span><span class="mi">14</span><span class="p">),</span> <span class="n">nullable</span><span class="o">=</span><span class="bp">False</span><span class="p">)</span>
    <span class="n">last_name</span> <span class="o">=</span> <span class="n">Column</span><span class="p">(</span><span class="n">String</span><span class="p">(</span><span class="mi">16</span><span class="p">),</span> <span class="n">nullable</span><span class="o">=</span><span class="bp">False</span><span class="p">)</span>
    <span class="n">gender</span> <span class="o">=</span> <span class="n">Column</span><span class="p">(</span><span class="n">String</span><span class="p">(</span><span class="mi">1</span><span class="p">),</span> <span class="n">nullable</span><span class="o">=</span><span class="bp">False</span> <span class="p">)</span>
    <span class="n">hire_date</span> <span class="o">=</span> <span class="n">Column</span><span class="p">(</span><span class="n">Date</span><span class="p">,</span> <span class="n">nullable</span><span class="o">=</span><span class="bp">False</span> <span class="p">)</span>
</pre></td></tr></tbody></table></code></pre></figure>

<p>
❶ Recall that we have postponed the discussion of class method <code>set_query(...)</code>.
We will discuss it now. It should be apparent that for the new codes, the default query
class is still <code>BaseQuery</code>; let's replace it with <code>SerialiseQuery</code>,
and also see how the new one works:
</p>

```python
Employees.set_query(SerialiseQuery)

result = Employees.query.filter(Employees.hire_date.between('2000-01-01', '2000-12-31'))\
    .order_by(Employees.emp_no).serialise()

from pprint import pprint
pprint(result.serialised_array)
```

<p>
I am printing out just the first and the last rows:
</p>

```
[{'birth_date': datetime.date(1960, 9, 9),
  'emp_no': 47291,
  'first_name': 'Ulf',
  'gender': 'M',
  'hire_date': datetime.date(2000, 1, 12),
  'last_name': 'Flexer'},
  ...
   {'birth_date': datetime.date(1954, 5, 6),
  'emp_no': 499553,
  'first_name': 'Hideyuki',
  'gender': 'F',
  'hire_date': datetime.date(2000, 1, 22),
  'last_name': 'Delgrande'}]
```

<p>
❷ Since <code>serialise()</code> maintains chainability, the following
should also work:
</p>

```python
result.print_all()
```

<p>
❸ And also:
</p>

```python
first_rec = result.first()
print(first_rec.__dict__)
```

<p>
❹ Chaining <code>print_all()</code> and <code>serialise()</code>
in either order:
</p>

```python
result = Employees.query.filter(Employees.emp_no==16621).print_all().serialise()
print("\n")
print(result.serialised_array)
```

<p>
In the context of this example, the chaining order should not matter:
</p>

```python
result = Employees.query.filter(Employees.emp_no==16621).serialise().print_all()
print("\n")
print(result.serialised_array)
```

<p>
-- Since both methods return <code>self</code>: this should make sense.
</p>

<p>
❺ Let's make <code>BaseQuery</code> the default query class:
</p>

```python
Employees.set_query(BaseQuery)
```

<p>
This code should raise an exception:
</p>

```python
result = Employees.query.filter(Employees.emp_no==16621).print_all().serialise()
```

<p>
And it does:
</p>

```
There are 1 rows.
{'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x0000012B96511FF0>, 'first_name': 'Parviz', 'gender': 'M', 'birth_date': datetime.date(1962, 5, 30), 'last_name': 'Strehl', 'emp_no': 16621, 'hire_date': datetime.date(1992, 6, 11)}
Traceback (most recent call last):
  File "F:\my_project\src\my_project\my_python_script.py", line 109, in <module>
    result = Employees.query.filter(Employees.emp_no==16621).print_all().serialise()
AttributeError: 'BaseQuery' object has no attribute 'serialise'
```

<p>
This makes sense, <code>BaseQuery</code> only has <code>print_all()</code> method.
</p>

<p>
The official document 
<a href="https://docs.sqlalchemy.org/en/14/orm/contextual.html#sqlalchemy.orm.scoping.scoped_session.query_property"
title="method sqlalchemy.orm.scoping.scoped_session.query_property(query_cls=None)"
target="_blank">method sqlalchemy.orm.scoping.scoped_session.query_property(query_cls=None)</a>, states:
</p>

>...
>There is no limit to the number of query properties placed on a class.
>...

<p>
My interpretation is: we can give our models as many query properties 
as required -- though I'm not certain this is right. However, this 
interpretation works, that is:
</p>

```python
...
class BaseModel(object):
    query = database_sesssion.query_property(BaseQuery)
    serialise_query = database_sesssion.query_property(SerialiseQuery)
    ...
	
...	
```

<p>
The rest of the codes stay the same. And we can now do:
</p>

```python
result1 = Employees.query.filter(Employees.emp_no==16621).print_all()
result2 = Employees.serialise_query.filter(Employees.emp_no==16621).print_all().serialise()

print(result2.serialised_array)
```

<p>
This also means the class method <code>set_query(...)</code> in 
<code>BaseModel</code> is obsolete!
</p>

<p>
The <code>sqlalchemy.orm.Query</code> class has many interesting and useful
methods, e.g. <code>offset(int)</code> and <code>limit(int)</code>:
</p>

```python
result = Employees.serialise_query.filter(Employees.hire_date.between('2000-01-01', '2000-12-31'))\
    .order_by(Employees.emp_no).offset(2).limit(3).serialise()

from pprint import pprint
pprint(result.serialised_array)
```

<p>
<code>offset(int)</code> is a 0-based index. After querying the database and getting the 
result, we then serialise rows 3 ( offset 2 ), 4 and 5, and print out the list of all 
three ( 3 ) dictionary entries:
</p>

```
[{'birth_date': datetime.date(1953, 2, 9),
  'emp_no': 72329,
  'first_name': 'Randi',
  'gender': 'F',
  'hire_date': datetime.date(2000, 1, 2),
  'last_name': 'Luit'},
 {'birth_date': datetime.date(1955, 4, 14),
  'emp_no': 108201,
  'first_name': 'Mariangiola',
  'gender': 'M',
  'hire_date': datetime.date(2000, 1, 1),
  'last_name': 'Boreale'},
 {'birth_date': datetime.date(1960, 9, 12),
  'emp_no': 205048,
  'first_name': 'Ennio',
  'gender': 'F',
  'hire_date': datetime.date(2000, 1, 6),
  'last_name': 'Alblas'}]
```

<p>
<code>sqlalchemy.orm.Query</code> class provides enough capabilities
out of the box to implement our own pagination functionality. I'm 
working on one at the moment, it's progressing quite well:
</p>

```python
class BaseQuery(Query):
    def paginate(self, page: int, per_page: int):
        return Paginator(self, page, per_page).execute()
```

<p>
I have not found any official example -- at all -- on how to construct 
user-defined query classes. After some searching, I found the following three 
( 3 ), rather old, Stackoverflow posts:
</p>

<ol>
<li style="margin-top:10px;">
<a href="https://stackoverflow.com/questions/12350807/whats-the-difference-between-model-query-and-session-querymodel-in-sqlalchemy"
title="What's the difference between Model.query and session.query(Model) in SQLAlchemy?"
target="_blank">What's the difference between Model.query and session.query(Model) in SQLAlchemy?</a>
</li>

<li style="margin-top:10px;">
<a href="https://stackoverflow.com/questions/38631651/can-you-extend-sqlalchemy-query-class-and-use-different-ones-in-the-same-session"
title="Can you extend SQLAlchemy Query class and use different ones in the same session?"
target="_blank">Can you extend SQLAlchemy Query class and use different ones in the same session?</a>
</li>

<li style="margin-top:10px;">
<a href="https://stackoverflow.com/questions/15936111/sqlalchemy-can-you-add-custom-methods-to-the-query-object"
title="SQLAlchemy - can you add custom methods to the query object?"
target="_blank">SQLAlchemy - can you add custom methods to the query object?</a>
</li>
</ol>

<p>
These posts set me in the right direction, and this post is the result 
of that learning process... SQLAlchemy is a large library, there are still
so much to get through.
</p>

<p>
I found this all very interesting, since I am very interested in database works.
I hope you find this post helpful in some way. Thank you for reading and stay safe as always.
</p>
