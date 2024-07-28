---
layout: post
title: "Python & MariaDB: Which Driver? An Example of Executing a Stored Procedure That Returns Multiple Result Sets"

description: In this discussion, I explain why I prefer the Python MySQL driver, mysql-connector-python, for the MariaDB database over the mariadb driver. The latter appears to be recommended by the official MariaDB documentation and is also mentioned on the SQLAlchemy page for MySQL and MariaDB.

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/07/118-01.png"

gallery-image-list-2:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/07/118-02.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/07/118-03.png"

tags:
- Python
- MariaDB
- Driver
---

<em>
In this discussion, I explain why I prefer the Python MySQL driver, <a href="https://pypi.org/project/mysql-connector-python/" title="MySQL driver written in Python" target="_blank">mysql-connector-python</a>, for the <a href="https://mariadb.com/" title="MariaDB" target="_blank">MariaDB</a> database over the <a href="https://pypi.org/project/mariadb/" title="MariaDB Connector/C client library for Python" target="_blank">mariadb</a> driver. The latter appears to be recommended by the official <a href="https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/" title="How to connect Python programs to MariaDB" target="_blank">MariaDB documentation</a> and is also mentioned on the SQLAlchemy page for <a href="https://docs.sqlalchemy.org/en/20/dialects/mysql.html" title="MySQL and MariaDB" target="_blank">MySQL and MariaDB</a>.
</em>

| ![118-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/07/118-feature-image.png) |
|:--:|
| *Python & MariaDB: Which Driver? An Example of Executing a Stored Procedure That Returns Multiple Result Sets* |

<a id="background-discussion"></a>
<p>
❶ This new post could be considered as related to some previous posts listed below:
</p>

<ol>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/07/01/synology-ds218-mariadb-10-enabling-remote-connection/" title="Synology DS218: MariaDB 10 enabling remote connection" target="_blank">Synology DS218: MariaDB 10 enabling remote connection</a>: This Synology DS218 Linux box, which serves as the MariaDB 10 database server, is used in this new post.
</li>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/11/09/python-executing-mysql-stored-procedures-which-return-multiple-result-sets/" title="Python: executing MySQL stored procedures which return multiple result sets" target="_blank">Python: executing MySQL stored procedures which return multiple result sets</a>: This new post is an extension of the previous one. We will be using the same database content, the same stored procedure, and the same Python test code.
</li>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/11/15/python-executing-postgresql-stored-functions-which-return-multiple-result-sets/" title="Python: executing PostgreSQL stored functions which return multiple result sets" target="_blank">Python: executing PostgreSQL stored functions which return multiple result sets</a>.
</li>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/09/17/rust-mysql-executing-mysql-stored-procedures-which-return-multiple-result-sets-using-crate-sqlx/" title="Rust & MySQL: executing MySQL stored procedures which return multiple result sets using crate sqlx" target="_blank">Rust & MySQL: executing MySQL stored procedures which return multiple result sets using crate sqlx</a>.
</li>
</ol>

<a id="mariadb"></a>
❷ Around two years ago, when I bought my Synology DS218 box, I became aware of the MariaDB database. My research suggests that it is superior to and also compatible with the <a href="https://www.mysql.com/" title="MySQL database" target="_blank">MySQL database</a>. As demonstrated in a previously mentioned post, <a href="https://behainguyen.wordpress.com/2022/07/01/synology-ds218-mariadb-10-enabling-remote-connection/" title="Synology DS218: MariaDB 10 enabling remote connection" target="_blank">Synology DS218: MariaDB 10 enabling remote connection</a>, I can use all MySQL client tools with the MariaDB database. Please refer to the following post, <a href="https://www.cloudways.com/blog/mariadb-vs-mysql/" title="MariaDB vs MySQL: A Detailed Comparison" target="_blank">MariaDB vs MySQL: A Detailed Comparison</a>, for further information.

<a id="mariadb-driver"></a>
❸ I have not been using the MariaDB database in my development, as I have both the MySQL and <a href="https://www.postgresql.org/" title="PostgreSQL" target="_blank">PostgreSQL</a> databases available.

I have been exploring the MariaDB database recently. I tried out the recommended <a href="https://pypi.org/project/mariadb/" title="MariaDB Connector/C client library for Python" target="_blank">mariadb</a> driver. Instead of following the official example, I experimented with my own stored procedure which returns multiple result sets, replicating the example in <a href="https://behainguyen.wordpress.com/2022/11/09/python-executing-mysql-stored-procedures-which-return-multiple-result-sets/" title="Python: executing MySQL stored procedures which return multiple result sets" target="_blank">a previously</a> mentioned post.

To recap:

⓵ The source database is the <code>MySQL test data</code> released by Oracle Corporation, downloadable from <a href="https://github.com/datacharmer/test_db" title="MySQL test data " target="_blank">https://github.com/datacharmer/test_db</a>. Using MySQL tools, I backed up a MySQL database and restored the backup content to the MariaDB database server on the Synology DS218 Linux box.

⓶ The stored procedure is reprinted below:

{% highlight sql linenos %}
delimiter //

drop procedure if exists DemoStoredProc1; //

create procedure DemoStoredProc1( pm_dept_no varchar(4) )
reads sql data
begin
  select * from departments where dept_no = pm_dept_no;
  select * from dept_manager where dept_no = pm_dept_no;
end; //
{% endhighlight %}

👉 I verified that this stored procedure works as expected with the MariaDB database. If there is a match, the first record set will have only a single record, the second record set will have one or more records: they are </strong> distinct record sets. Please note, we could have more than two, but for the purpose of this post, two should suffice.

⓷ Install the <a href="https://pypi.org/project/mariadb/" title="MariaDB Connector/C client library for Python" target="_blank">mariadb</a> driver into the active virtual environment.

⓸ The Python code is copied from the <a href="https://behainguyen.wordpress.com/2022/11/09/python-executing-mysql-stored-procedures-which-return-multiple-result-sets/" title="Python: executing MySQL stored procedures which return multiple result sets" target="_blank">previous post</a> as mentioned several times above. <strong>The only modification is:</strong> replacing the connection string as appropriate for the <code>mariadb</code> driver.

```
Content of mariadb-example.py:
```

{% highlight python linenos %}
from sqlalchemy import create_engine
from contextlib import closing

engine = create_engine( 'mariadb+mariadbconnector://behai:O,U#n*m:5QB3_zbQ@192.168.0.14:3306/employees', echo = False )
# engine = create_engine( 'mysql+mysqlconnector://behai:O,U#n*m:5QB3_zbQ@192.168.0.14:3306/employees', echo = False )

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
{% endhighlight %}

Please note, <code>192.168.0.14</code> is the IP address of my Synology DS218 Linux box.

It produces the following runtime error:

<code><strong style="color:red;">Exception. Type &lt;class 'AttributeError'&gt;: 'Cursor' object has no attribute 'stored_results'</strong></code>

Please also see the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-1 %}
<br/>

This is not a database server error, but rather a driver error. However, we know the MariaDB server executes the above stored procedure correctly, so there is no problem on the server-side. The following page is the official MySQL documentation on the <a href="https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-stored-results.html" title="MySQLCursor.stored_results() method" target="_blank"><code>MySQLCursor.stored_results()</code> method</a>. I have not been able to locate an equivalent for the MariaDB database.

Having already installed the <a href="https://pypi.org/project/mysql-connector-python/" title="MySQL driver written in Python" target="_blank">mysql-connector-python</a> driver, switching the connection string to <code>mysql+mysqlconnector</code>:

```python
# engine = create_engine( 'mariadb+mariadbconnector://behai:O,U#n*m:5QB3_zbQ@192.168.0.14:3306/employees', echo = False )
engine = create_engine( 'mysql+mysqlconnector://behai:O,U#n*m:5QB3_zbQ@192.168.0.14:3306/employees', echo = False )
```

produces the expected results. Please refer to the two screenshots below:

{% include image-gallery.html list=page.gallery-image-list-2 %}
<br/>

I am not sure if I missed something about the <a href="https://pypi.org/project/mariadb/" title="MariaDB Connector/C client library for Python" target="_blank">mariadb</a> driver. I have looked through its documentation, and I have yet to find an equivalent of <code>MySQLCursor.stored_results()</code>.

❹ Testing with the <a href="https://pypi.org/project/bh-database/" title="bh-database" target="_blank">bh-database</a> wrapper classes for SQLAlchemy.

For the two <a href="https://github.com/behai-nguyen/bh_database/tree/main/examples" title="bh-database examples" target="_blank">examples</a> provided, if you want to access the MariaDB <code>employees</code> database, simply modify the connection string to match the one used in the above example:

```
SQLALCHEMY_DATABASE_URI = mysql+mysqlconnector://behai:O,U#n*m:5QB3_zbQ@192.168.0.14:3306/employees
```

All functions from the two <a href="https://github.com/behai-nguyen/bh_database/tree/main/examples" title="bh-database examples" target="_blank">examples</a> will continue to operate correctly when using the MariaDB database.

❺ Given all the observations discussed above, the <a href="https://pypi.org/project/mysql-connector-python/" title="MySQL driver written in Python" target="_blank">mysql-connector-python</a> driver appears to be suitable for the MariaDB database. I plan to undertake some development work with MariaDB in the future. I will share any interesting findings I encounter with the MariaDB database.

Thank you for reading. I hope you find the information in this post useful. Stay safe, as always.

✿✿✿

Feature image source:

<ul>
<li>
<a href="https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper" target="_blank">https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper</a>
</li>
<li>
<a href="https://in.pinterest.com/pin/337277459600111737/" target="_blank">https://in.pinterest.com/pin/337277459600111737/</a>
</li>
<li>
<a href="https://www.python.org/downloads/release/python-3124/" target="_blank">https://www.python.org/downloads/release/python-3124/</a>
</li>
</ul>