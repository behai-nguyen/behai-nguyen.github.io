---
layout: post
title: "Python: executing PostgreSQL stored functions which return multiple result sets."
description: PostgreSQL stored functions can return multiple result sets. In this post, we're looking at calling such stored function; for each returned record set, retrieving its column names and records, then store these in a structure of our own choosing. We're using SQLAlchemy, and the psycopg2 connector library.
tags:
- Python
- PostgreSQL
- stored procedures
- multiple result sets
- psycopg2
---

*PostgreSQL stored functions can return multiple result sets. In this post, we're looking at calling such stored function; for each returned record set, retrieving its column names and records, then store these in a structure of our own choosing. We're using SQLAlchemy, and the psycopg2 connector library.*

| ![047-feature-images.png](https://behainguyen.files.wordpress.com/2022/11/047-feature-images.png) |
|:--:|
| *Python: executing PostgreSQL stored functions which return multiple result sets.* |

This SQLAlchemy page 
<a href="https://docs.sqlalchemy.org/en/14/dialects/postgresql.html" title="PostgreSQL" target="_blank">PostgreSQL</a>
lists several connector packages. I'm using 
<a href="https://pypi.org/project/psycopg2/" title="psycopg2 2.9.57" target="_blank">psycopg2 2.9.57</a>,
since it is on top of the list, and also it seems to be used by everybody else.

I am replicating the MySQL database, and the stored procedure discussed in 
<a href="https://behainguyen.wordpress.com/2022/11/09/python-executing-mysql-stored-procedures-which-return-multiple-result-sets/"
title="Python: executing MySQL stored procedures which return multiple result sets."
target="_blank">Python: executing MySQL stored procedures which return multiple result sets</a>
over to PostgreSQL.

To recap, the source database is the
<span class="keyword">
MySQL test data </span>		
released by Oracle Corporation. Downloadable from
<a href="https://github.com/datacharmer/test_db" title="MySQL test data " target="_blank">https://github.com/datacharmer/test_db</a>.
I've migrated it over to PostgreSQL as discussed in 
<a href="https://behainguyen.wordpress.com/2022/11/13/pgloader-docker-migrating-from-docker-localhost-mysql-to-localhost-postgresql/#migrating-commands"
title="pgloader Docker: migrating from Docker & localhost MySQL to localhost PostgreSQL."
target="_blank">pgloader Docker: migrating from Docker & localhost MySQL to localhost PostgreSQL</a>,
please see command ❷.

The stored function in this post is exactly identical to the one in MySQL.
That is:

<ul>
<li style="margin-top:5px;">
Each returned record set is in its own list. And in this list:
<ul>
<li style="margin-top:10px;">
The first element is the list of column names.
</li>
<li style="margin-top:10px;">
The subsequent elements are lists of data records.
</li>
</ul>
</li>

<li style="margin-top:10px;">
All record set lists are stored within a another list.
</li>

<li style="margin-top:10px;">
When there is no data, extract only column names for each record set.
</li>
</ul>

I've not done PostgreSQL before. I've commercial experiences with Microsoft 
SQL Server, Oracle, InterBase and MySQL: the PostgreSQL learning curve is
not too steep for me... Before writing this post, I've finished porting 
fourteen ( 14 ) stored methods in MySQL to PostgreSQL for the project 
I'm currently working on. The objective is to get the server application 
supports both MySQL and PostgreSQL seamlessly. None of the stored method 
I've ported returns multiple result sets, I'm looking at this issue 
just for my own understanding. Principal references used in this post are:

<ol>
<li style="margin-top:10px;">
<a href="https://stackoverflow.com/questions/36717138/postgres-function-return-multiple-tables"
title="Postgres function: return multiple tables"
target="_blank">Postgres function: return multiple tables</a> -- please see the accepted answer.
The stored function does not have any named cursor in the argument list, just 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
RETURNS setof refcursor</span>.
</li>

<li style="margin-top:5px;">
<a href="https://stackoverflow.com/questions/71848646/is-there-a-proper-way-to-handle-cursors-returned-from-a-postgresql-function-in-p"
title="Is there a proper way to handle cursors returned from a postgresql function in psycopg?"
target="_blank">Is there a proper way to handle cursors returned from a postgresql function in psycopg?</a>
This is not about multiple result sets, but about using named cursor. I.e. 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
cur1.callproc('reffunc', ['curname'])</span>. I'm not sure if this is a correct answer 
( it was accepted ) or not, but it does give me some more information to experiment with, especially
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
['curname']</span>.
</li>

<li style="margin-top:10px;">
<a href="https://stackoverflow.com/questions/49020718/get-a-list-of-column-names-from-a-psycopg2-cursor-executing-stored-proc"
title="Get a list of column names from a psycopg2 cursor executing stored proc?"
target="_blank">Get a list of column names from a psycopg2 cursor executing stored proc?</a> -- please
see the answer by 
<a href="https://stackoverflow.com/users/10138/piro" title="user piro" target="_blank">user piro</a>
on Mar 1, 2018. He's one of the maintainers of the
<a href="https://pypi.org/project/psycopg2/" title="psycopg2 2.9.57" target="_blank">psycopg2 2.9.57</a>
library. 

<p>
Also, the Python codes presented by the post initiator give me information
on how to work the named cursor, too.
</p>
</li>
</ol>

It is a bit hard to articulate, but these three ( 3 ) posts have given me
enough to do my own experiments: <em><strong>I don't like the idea of having
to specify a list of returned named cursors in the manner of reference 
posts 2 ( two ) and 3 ( three )</strong>. I like the flexibility in
reference post 1 ( one ) much better.</em>

This is my first version of the stored method:

```sql
create or replace function DemoStoredProc1( pm_dept_no varchar(4) )
returns setof refcursor
language plpgsql
as
$$
declare 
  c1 refcursor;
  c2 refcursor;
begin
  open c1 for 
  select * from departments where dept_no = pm_dept_no;
  return next c1;
  
  open c2 for   
  select * from dept_manager where dept_no = pm_dept_no;
  return next c2;
end;
$$
```

I test it within pgAdmin with:

```sql
select * from DemoStoredProc1( 'd001' );
```

And the output is:

```
demostoredproc1 refcursor
<unnamed portal 1>;
<unnamed portal 2>;
```

From what I can gather, each of these 
<span class="keyword">
unnamed portal refcursor</span> is called a 
<span class="keyword">
server side cursor</span>? 

After some experimentations, this is the resulting Python codes:

```python
from sqlalchemy import create_engine
from contextlib import closing

engine = create_engine( 'postgresql+psycopg2://postgres:secret-password@localhost/employees', echo = False )
connection = engine.raw_connection()

def collect_result_set( connection, named_cursor: str, data: list ) -> None:
    cursor = connection.cursor( named_cursor )

    dataset = []
    row = cursor.fetchone()
    columns = [ column[0] for column in cursor.description ]
    dataset.append( columns )

    if ( row != None ): 
        dataset.append( list(row) )
        for row in cursor:
            dataset.append( list(row) )
				
    data.append( dataset )
    cursor.close()

try:
    with closing( connection.cursor() ) as cursor:
        cursor.callproc( 'DemoStoredProc1', [ 'd001' ] )

        data = []		
        for cur in cursor:             
            collect_result_set( connection, cur[0], data )
			
        cursor.close()
		
        import pprint
        print( '\n' )
        pprint.pprint( data )
			
except Exception as e:
    print( f'Exception. Type {type(e)}: {str(e)}' )
finally:
    if 'connection' in locals():
        connection.close()
```

In 

```python
def collect_result_set( connection, named_cursor: str, data: list ) -> None:
```

to get column names, after getting the server side cursor, 
as per reference post 3 ( three ) above, we need to call
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
.fetchone()</span> to make the column names available.
After this, the column names are available regardless if there
is any data or not:

```python
columns = [ column[0] for column in cursor.description ]
```

The above one liner we've seen before in the post for MySQL.
Parameter 
<span class="keyword">
named_cursor: str</span> is my own try, and my own lucky guess! 
In the main loop, if we add the 
<span class="keyword">
print( cur, cur[0], type(cur[0]) )</span> statement:

```python
        for cur in cursor: 
            print( cur, cur[0], type(cur[0]) )
```

We would get the following printouts:

```
('<unnamed portal 1>;',) <unnamed portal 1>; <class 'str'>;
('<unnamed portal 2>;',) <unnamed portal 2>; <class 'str'>;
```

Based on the information given in reference posts 1 ( one ) and 2 ( two ), 
I thought I should try 
<span class="keyword">
cur[0]</span> -- and it just happens to work.

I try another implementation of the above stored method, using
named cursor arguments, as per reference posts 2 ( two ) and 
3 ( three ):

```sql
create or replace function DemoStoredProc2( pm_dept_no varchar(4),
    c1 refcursor, c2 refcursor )
returns setof refcursor
language plpgsql
as
$$
begin
  open c1 for 
  select * from departments where dept_no = pm_dept_no;
  return next c1;
  
  open c2 for   
  select * from dept_manager where dept_no = pm_dept_no;
  return next c2;
end;
$$
```

And following is the Python implementation:

```python
<pre>
from sqlalchemy import create_engine
from contextlib import closing

engine = create_engine( 'postgresql+psycopg2://postgres:secret-password@localhost/employees', echo = False )
connection = engine.raw_connection()

def collect_result_set( connection, named_cursor: str, data: list ) -> None:
    cursor = connection.cursor( named_cursor )

    dataset = []
    row = cursor.fetchone()
    columns = [ column[0] for column in cursor.description ]
    dataset.append( columns )

    if ( row != None ): 
        dataset.append( list(row) )
        for row in cursor:
            dataset.append( list(row) )
				
    data.append( dataset )
    cursor.close()

try:
    with closing( connection.cursor() ) as cursor:
        cursor.callproc( 'DemoStoredProc2', [ 'd001', 'c1', 'c2' ] )

        data = []

        collect_result_set( connection, 'c1', data )
        collect_result_set( connection, 'c2', data )

        cursor.close()
		
        import pprint
        print( '\n' )
        pprint.pprint( data )
			
except Exception as e:
    print( f'Exception. Type {type(e)}: {str(e)}' )
finally:
    if 'connection' in locals():
        connection.close()
```

```python
def collect_result_set( connection, named_cursor: str, data: list ) -> None:
```

remains unchanged in this implementation. Only the main block has to
be changed: method 
<span class="keyword">
collect_result_set( ... )</span> is called explicitly with the two
named cursors. That means, if the stored method must return another
additional result set, the codes of the main block must be modified
to handle this new result set:

-- This is the reason why I like the first implementation better.

Both of these implementations return the same result:

```python
[
    [
        ['dept_no', 'dept_name'], 
        ['d001', 'Marketing']
    ],
    [
        ['emp_no', 'dept_no', 'from_date', 'to_date'],
        [110022, 'd001', datetime.date(1985, 1, 1), datetime.date(1991, 10, 1)],
        [110039, 'd001', datetime.date(1991, 10, 1), datetime.date(9999, 1, 1)]
    ]
]
```

Changed 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
d001</span>
to, for example, 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
dxx1</span>, we will get:

```python
[
    [
        ['dept_no', 'dept_name']
    ], 
    [
        ['emp_no', 'dept_no', 'from_date', 'to_date']
    ]
]
```

✿✿✿

I find this interesting and helpful. I hope you do too. Thank you for reading and 
stay safe as always.
