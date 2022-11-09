---
layout: post
title: "Python: executing MySQL stored procedures which return multiple result sets."
description: MySQL stored procedures can return multiple result sets. In this post, we're looking at calling such stored procedure; for each returned record set, retrieving its column names and records, then store these in a structure of our own choosing. We're using SQLAlchemy, and the following three ( 3 ) connector packages, mysqlclient, PyMySQL and mysql-connector-python. mysqlclient and PyMySQL handle multiple result sets in a similar manner, while mysql-connector-python does it differently.
tags:
- Python
- MySQL 
- stored procedures
- multiple result sets
- mysql-connector-python
- mysqlclient
- PyMySQL
---

*MySQL stored procedures can return multiple result sets. In this post, we're looking at calling such stored procedure; for each returned record set, retrieving its column names and records, then store these in a structure of our own choosing. We're using SQLAlchemy, and the following three ( 3 ) connector packages: mysqlclient, PyMySQL and mysql-connector-python. mysqlclient and PyMySQL handle multiple result sets in a similar manner, while mysql-connector-python does it differently.*

| ![045-feature-images.png](https://behainguyen.files.wordpress.com/2022/11/045-feature-images.png) |
|:--:|
| *Python: executing MySQL stored procedures which return multiple result sets.* |

This SQLAlchemy page 
<a href="https://docs.sqlalchemy.org/en/20/dialects/mysql.html"
title="MySQL and MariaDB" target="_blank">MySQL and MariaDB</a>
lists several MySQL Python connector packages, but the previously
mentioned ones are on top of the list, and seem to be the most 
mentioned ones across forums. These're the reasons why I pick 
them for this study. Their web pages: 
<a href="https://pypi.org/project/mysql-connector-python/"
title="mysql-connector-python" target="_blank">mysql-connector-python</a>, 
<a href="https://pypi.org/project/mysqlclient/" title="mysqlclient" target="_blank">mysqlclient</a>
and 
<a href="https://pypi.org/project/PyMySQL/" title="PyMySQL" target="_blank">PyMySQL</a>.

The source database is the
<span class="keyword">
MySQL test data </span>		
released by Oracle Corporation. Downloadable from
<a href="https://github.com/datacharmer/test_db" title="MySQL test data " target="_blank">https://github.com/datacharmer/test_db</a>.
It is a simple database with only a few tables, easy to setup.

Below is the stored procedure we're using in this post:

```sql
delimiter //

drop procedure if exists DemoStoredProc1; //

create procedure DemoStoredProc1( pm_dept_no varchar(4) )
reads sql data
begin
  select * from departments where dept_no = pm_dept_no;
  select * from dept_manager where dept_no = pm_dept_no;
end; //
```

If there is a match, the first record set will have only 
a single record, the second record set will have one or more
records: they are two ( 2 ) distinct record sets. Please note,
we could have more than two, but for the purpose of this post, 
two should suffice.

I'd like to extract column names and records into a 
multi-dimensional list as illustrated below:

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
</ul>

When there is no data, only column names are extracted:

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

<a href="https://stackoverflow.com/questions/15320265/cannot-return-results-from-stored-procedure-using-python-cursor"
title="Cannot return results from stored procedure using Python cursor"
target="_blank">Cannot return results from stored procedure using Python cursor</a>
is the principal post which helps me figure out how 
 <span class="keyword">
mysqlclient</span> and 
<span class="keyword">
PyMySQL</span> work.

<h3>mysql-connector-python</h3>

<a href="https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-stored-results.html"
title="MySQLCursor.stored_results() method" target="_blank">MySQLCursor.stored_results() method</a>
provides access to individual result sets:

```python
from sqlalchemy import create_engine
from contextlib import closing

engine = create_engine( 'mysql+mysqlconnector://behai:super-secret-password@localhost/employees', echo = False )
connection = engine.raw_connection()

try:
    with closing( connection.cursor() ) as cursor:
        cursor.callproc( 'DemoStoredProc1', [ 'd001' ] )

        data = []
        for sr in cursor.stored_results():
            #-- 
            columns = [ column[0] for column in sr.description ]
            ds = sr.fetchall()

            dataset = []
            dataset.append( columns )
            for row in ds:
                dataset.append( list(row) )

            data.append( dataset )
            #--
            sr.close()

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

Each iterator returned by <span class="keyword">
MySQLCursor.stored_results()</span> is a
<a href="https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor.html"
title="MySQLCursor class" target="_blank">MySQLCursor class</a>, where
<a href="https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-description.html"
title="MySQLCursor.description property" target="_blank">MySQLCursor.description property</a>
provides access to column information. The rest of the codes should be self-explanatory.

<h3>mysqlclient and PyMySQL</h3>

<span class="keyword">
mysqlclient</span> and 
<span class="keyword">
PyMySQL</span> cursor classes do not implement the 
<span class="keyword">
stored_results()</span> method. Instead, they implement the
<a href="https://peps.python.org/pep-0249/#nextset"
title=".nextset()" target="_blank">.nextset()</a> method.
Their respective documentations, 
<a href="https://github.com/PyMySQL/mysqlclient/blob/main/doc/user_guide.rst#cursor-objects"
title="mysqlclient/MySQLdb | Cursor Objects" target="_blank">mysqlclient/MySQLdb | Cursor Objects</a>
and 
<a href="https://pymysql.readthedocs.io/en/latest/modules/cursors.html"
title="PyMySQL Cursor Objects" target="_blank">PyMySQL Cursor Objects</a>.

<span class="keyword">
.nextset()</span>-based looping is not as elegant as iterating with
<span class="keyword">
stored_results()</span>:

```python
from sqlalchemy import create_engine
from contextlib import closing

# mysqlclient
engine = create_engine( 'mysql://behai:super-secret-password@localhost/employees', echo = False )
# PyMySQL
engine = create_engine( 'mysql+pymysql://behai:super-secret-password@localhost/employees', echo = False )

connection = engine.raw_connection()

try:
    with closing( connection.cursor() ) as cursor:
        cursor.callproc( 'DemoStoredProc1', [ 'd001' ] )

        data = []
        ns = cursor
        while ns != None:
            if ( cursor.description != None ):
                #--
                columns = [ column[0] for column in cursor.description ]
                ds = cursor.fetchall()				
				
                dataset = []
                dataset.append( columns )
                for row in ds:
                    dataset.append( list(row) )

                data.append( dataset )
                #--
				
            ns = cursor.nextset()
			
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

According to the documentations, I should not need the condition:

```python
if ( cursor.description != None ):
```

But without it, the loop will result in an exception when at the end!
I have not been able to work that one out yet... and probably never
will: I am not using these two packages.

Personally, I like 
<a href="https://pypi.org/project/mysql-connector-python/"
title="mysql-connector-python" target="_blank">mysql-connector-python</a> best:
rich documentation and it is written by MySQL themselves, and
so is likely always up to date.

I looked into this out of curiosity. I have not taken advantage of this 
feature of MySQL in any of the projects yet. I hope you find this useful.
Thank you for reading and stay safe as always.