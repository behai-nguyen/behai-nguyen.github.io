---
layout: post
title: "Python: SQLAlchemy extracting column names and data from a MySQL stored procedure returned dataset."
description: How to enable pytest methods to access Flask's context variables, session and request.
tags:
- Python
- SQLAlchemy
- Stored Procedure
- Dataset
- Column Names
---

Using the SQLAlchemy library for Python, how to run a MySQL stored procedure, and extracting the column names and data from the stored procedure returned dataset.

| ![037-feature-images.png](https://behainguyen.files.wordpress.com/2022/08/037-feature-images.png) |
|:--:|
| *Python: SQLAlchemy extracting column names and data from a MySQL stored procedure returned dataset.* |

I've been using the
<span class="keyword">
SQLAlchemy</span> library for a tiny little while now... Learning 
how to run 
<span class="keyword">
MySQL stored procedures</span> with it was not that difficult. 
However, I feel that it can be difficult to find information on 
certain aspects of this library... It certainly is a toughest
database library to learn up to this point for me, personally.

It took me a bit of searching to be able to extract column names
from a dataset returned by a
<span class="keyword">
MySQL stored procedure</span>... Solutions suggested by some of the
posts which I've come across did not work for me. The one which works 
is <a href="https://dba.stackexchange.com/questions/198216/calling-mysql-stored-procedure-in-python-with-field-names" 
title="Calling MySQL stored procedure in python with field names" target="_blank">Calling MySQL stored procedure in python with field names</a>
by user 
<a href="https://dba.stackexchange.com/users/207207/mathieu-feraud"
title="mathieu FERAUD"
target="_blank">mathieu FERAUD</a>. I'm documenting this with 
a simplified example stored procedure.

Below is the simplified version of the
<span class="keyword">
MySQL stored procedure</span>, it returns only a single row, but 
that's inconsequential:

```sql
delimiter //

drop procedure if exists DemoStoredProc; //

create procedure DemoStoredProc( userId int, timesheetId int, 
                                 searchType varchar(10), roundDir varchar(4) )
                                 reads sql data
begin
  declare TOTAL_HOURS int;
  declare TOTAL_MINUTES int;
  declare ROUNDED_HOUR float(5,2);  
  
  set TOTAL_HOURS = 11;
  set TOTAL_MINUTES = 44;  
  set ROUNDED_HOUR = 0.5;  
  
  select TOTAL_HOURS, TOTAL_MINUTES, TOTAL_HOURS + ROUNDED_HOUR as ROUNDED_TOTAL_HOURS;  
end; //
```

The 
<span class="keyword">
Python</span> example, the script makes no assumption
on how many rows are in the final dataset.

```
File sqlalchemy-stored-proc.py:
```

```python
from sqlalchemy import create_engine
from contextlib import closing

engine = create_engine( 'mysql+mysqlconnector://behai1:password@localhost/ompdev1', echo = False )
connection = engine.raw_connection()

try:
    with closing( connection.cursor() ) as cursor:
        cursor.callproc( 'DemoStoredProc', [ 1, 111, 'all', 'down' ] )

        result = next( cursor.stored_results() )
        dataset = result.fetchall()
        has_data = len( dataset ) > 0

        if has_data:
            """
            Copying columns names into a list.

            Reference:
                https://dba.stackexchange.com/questions/198216/calling-mysql-stored-procedure-in-python-with-field-names
                Calling MySQL stored procedure in python with field names

                mathieu FERAUD -- https://dba.stackexchange.com/users/207207/mathieu-feraud
            """

            for column_id in cursor.stored_results():
                columns_properties = ( column_id.description )
                columns = [ column[0] for column in columns_properties ]

            data = []
            for row in dataset:
                record = {}
                for idx, name in enumerate( columns ):
                    record[ name ] = row[ idx ]
                data.append( record )

except Exception as e:
    has_data = False
    print( 'Exception. Type {}', type(e), '--', str(e) )
finally:
    if 'result' in locals():
        result.close()

    if 'conn' in locals():
        conn.close()

    if has_data:
        import pprint
        print( '\n' )
        pprint.pprint( data )
    else:
        print( '\nI am sorry...there is no data to print.\n' )
```

Basically, each row is turned into a 
<span class="keyword">
dictionary</span> with column names as key names. And the 
<span class="keyword">
dictionary</span> gets added to a list. Finally the list gets printed.

Before I could extract column names, I actually had everything else worked out. 
I did not know, and could not find information that points to 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
cursor.stored_results()</span>.

Others, from posts that I've read when searching for solution,
seem to have this same problem too... and even confusions, 
where a hack was suggested. There's a post which suggests using 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
cursor.description</span>, I did try that: 

```python
...
    with closing( connection.cursor() ) as cursor:
        cursor.callproc( 'DemoStoredProc', [1, 111, 'all', 'up'] )

        for field in cursor.description:
	        print( field )
...			
```

```
('DemoStoredProc_arg1', 8, None, None, None, None, 1, 32896, 63)
('DemoStoredProc_arg2', 8, None, None, None, None, 1, 32896, 63)
('DemoStoredProc_arg3', 251, None, None, None, None, 1, 0, 255)
('DemoStoredProc_arg4', 251, None, None, None, None, 1, 0, 255)
```

```
It is the stored procedure's argument information, not the 
returned column name information.
```

We can run the above script with:

```
(venv) F:\project_xyz>venv\Scripts\python.exe sqlalchemy-stored-proc.py
```

And we've the output as expected:

```
[{'ROUNDED_TOTAL_HOURS': 11.5, 'TOTAL_HOURS': 11, 'TOTAL_MINUTES': 44}]
```

I hope you find this post helpful. Thank you for reading. Happy 
programming and stay safe.
