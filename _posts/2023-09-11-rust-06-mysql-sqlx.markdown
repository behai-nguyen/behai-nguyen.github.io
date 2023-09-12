---
layout: post
title: "Rust & MySQL: connect, execute SQL statements and stored procs using crate sqlx."

description: We'll discuss&#58; how to connect to a MySQL server, run queries to select some data and display returned data, finally, execute stored procedures which return a single dataset.

tags:
- Rust
- MySQL
- sqlx
- stored procs
---

<em style="color:#111;">We'll discuss: ⓵ how to connect to a MySQL server, ⓶ run queries to select some data and display returned data, ⓷ finally, execute stored procedures which return a single dataset.</em>

| ![081-feature-image.png](https://behainguyen.files.wordpress.com/2023/09/081-feature-image.png) |
|:--:|
| *Rust & MySQL: connect, execute SQL statements and stored procs using crate sqlx.* |

First, please let me state that I'm aware of at least three (3) different crates for MySQL: ⓵ <a href="https://crates.io/crates/mysql" title="Crate mysql" target="_blank">mysql</a>, ⓶ <a href="https://docs.rs/sqlx/latest/sqlx" title="Crate sqlx" target="_blank">sqlx</a>, and ⓷ <a href="https://diesel.rs/" title="Crate Diesel" target="_blank">Diesel</a>.

I did look at <a href="https://crates.io/crates/mysql" title="Crate mysql" target="_blank">mysql</a> initially. Then I started checking other crates. <a href="https://diesel.rs/" title="Crate Diesel" target="_blank">Diesel</a> is an Object Relation Model (ORM), I'm not yet keen on taking on the complication of learning ORM, I give this crate a pass in the meantime. 

According to the documentation, crate <a href="https://docs.rs/sqlx/latest/sqlx" title="Crate sqlx" target="_blank">sqlx</a> is implemented in Rust, and it's database agnostic: it supports <a href="http://postgresql.org/" title="PostgreSQL" target="_blank">PostgreSQL</a>, <a href="https://www.mysql.com/" title="MySQL" target="_blank">MySQL</a>, <a href="https://sqlite.org/" title="SQLite" target="_blank">SQLite</a>, and <a href="https://www.microsoft.com/en-us/sql-server" title="MSSQL" target="_blank">MSSQL</a>.

-- It sounds enticing 😂... We learn one crate for several database servers. The learning process is tough for me. The Rust standard library gives examples. This crate lacks that... It takes a long time for me to be able to write the example code in this post, with help from the <a href="https://users.rust-lang.org/" title="Rust Users Community Forum" target="_blank">Rust Users Community Forum</a>.

The database used in this post is the <a href="https://github.com/datacharmer/test_db" title="Oracle Corporation MySQL test data" target="_blank">Oracle Corporation MySQL test data</a>; it's also been used in the following posts:

<ol>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2022/05/24/python-reportlab-a-master-detail-report/" title="Python: ReportLab -- a Master Detail Report." target="_blank">Python: ReportLab -- a Master Detail Report.</a></li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2022/11/09/python-executing-mysql-stored-procedures-which-return-multiple-result-sets/" title="Python: executing MySQL stored procedures which return multiple result sets." target="_blank">Python: executing MySQL stored procedures which return multiple result sets.</a></li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2022/11/13/pgloader-docker-migrating-from-docker-localhost-mysql-to-localhost-postgresql/" title="pgloader Docker: migrating from Docker & localhost MySQL to localhost PostgreSQL." target="_blank">pgloader Docker: migrating from Docker & localhost MySQL to localhost PostgreSQL.</a></li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2022/11/15/python-executing-postgresql-stored-functions-which-return-multiple-result-sets/" title="Python: executing PostgreSQL stored functions which return multiple result sets." target="_blank">Python: executing PostgreSQL stored functions which return multiple result sets.</a></li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2022/12/14/python-sqlalchemy-understanding-sessions-and-associated-queries/" title="Python: SQLAlchemy -- understanding sessions and associated queries." target="_blank">Python: SQLAlchemy -- understanding sessions and associated queries.</a></li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2022/12/17/python-sqlalchemy-user-defined-query-classes-for-scoped_session-query_propertyquery_clsnone/" title="Python: SQLAlchemy -- user-defined query classes for scoped_session.query_property(query_cls=None)." target="_blank">Python: SQLAlchemy -- user-defined query classes for scoped_session.query_property(query_cls=None).</a></li>
</ol>

In this post, we use the <a id="employees-table"><code>employees</code></a> table, whose structure is:

```sql
CREATE TABLE `employees` (
  `emp_no` int NOT NULL,
  `birth_date` date NOT NULL,
  `first_name` varchar(14) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `gender` enum('M','F') COLLATE utf8mb4_unicode_ci NOT NULL,
  `hire_date` date NOT NULL,
  PRIMARY KEY (`emp_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

<code>Cargo.toml</code> is common for all examples. Its <code>dependencies</code> section is as follow:

```toml
...
[dependencies]
async-std = "1.12.0"
sqlx = {version = "0.7", default-features = false, features = ["runtime-async-std", "macros", "mysql", "time"]}
time = {version = "0.3.22", default-features = false, features = ["formatting", "macros"]}
```

Crate <a href="https://github.com/async-rs/async-std" title="async-std" target="_blank">async-std</a> is required as stated in crate <a href="https://docs.rs/sqlx/latest/sqlx" title="Crate sqlx" target="_blank">sqlx</a>'s documentation.

On <a href="https://docs.rs/sqlx/latest/sqlx" title="Crate sqlx" target="_blank">sqlx</a> crate features <code>macros</code> and <code>time</code>. Crate feature <code>macros</code> is required to make the constraint <code>FromRow</code> available for the <code>derive</code> <em>attribute</em>. It took me a while to figure this one out, the documentation does not seem to mention it. Crate feature <code>time</code> must be enabled, otherwise <code>sqlx::types::time::Date</code> would not work: I think it's crate <a href="https://docs.rs/time/latest/time/" title="Crate time" target="_blank">time</a> that <a href="https://docs.rs/sqlx/latest/sqlx" title="Crate sqlx" target="_blank">sqlx</a> uses. Although I could not find any documentation to back this up.

We've discussed crate <a href="https://docs.rs/time/latest/time/" title="Crate time" target="_blank">time</a> in this post <a href="https://behainguyen.wordpress.com/2023/09/03/rust-baby-step-some-preliminary-look-at-date/" title="Rust: baby step -- some preliminary look at date." target="_blank">Rust: baby step -- some preliminary look at date. </a>

-- Without explicitly including crate <a href="https://docs.rs/time/latest/time/" title="Crate time" target="_blank">time</a>, and enable crate features, <code>formatting</code> and <code>macros</code>, I can't use date formatting function. I'm unsure of how this relates to <code>sqlx::types::time::Date</code>. <strong>So please keep this point in mind, there might be a better alternative.</strong>

<strong>Please note:</strong> <em>I only tested these examples on Windows 10.</em>

❶ <a id="database-connection">Establishing a MySQL server database connection</a>. Based on <a href="https://docs.rs/sqlx/latest/sqlx/struct.MySqlConnection.html" title="Struct sqlx::MySqlConnection" target="_blank">Struct sqlx::MySqlConnection</a>, and examples given in <a href="https://github.com/async-rs/async-std" title="async-std" target="_blank">async-std</a> and <a href="https://github.com/launchbadge/sqlx" title="launchbadge/sqlx" target="_blank">launchbadge/sqlx</a>, I came up with the following example:

```
Content of src/main.rs:
```

```rust
use sqlx::{Pool, MySql, Error, MySqlPool};

use async_std::task;

async fn connect() -> Result&lt;Pool&lt;MySql>, Error> {
    return MySqlPool::connect("mysql://root:pcb.2176310315865259@localhost:3306/employees").await;
}

async fn do_test_connection() {
    let result = task::block_on(connect());

    match result {
        Err(err) => {
            println!("Cannot connect to database [{}]", err.to_string());
        }        

        Ok(_) => {
            println!("Connected to database successfully.");
        }
    }
}

fn main() {
    task::block_on(do_test_connection());
}
```

❷ <a id="sql-statement">Select data using a SQL statement</a>. In addition to the references quoted in <a href="#database-connection">Establishing a MySQL server database connection</a> above, the following posts help me write this example:

<ul>
<li style="margin-top:10px;"><a href="https://stackoverflow.com/questions/74882459/returning-rows-from-mysql-with-rust-sqlx-when-a-varbinary16-column-is-part-of" title="Returning rows from MySQL with RUST sqlx when a VARBINARY(16) column is part of the where clause" target="_blank">Returning rows from MySQL with RUST sqlx when a VARBINARY(16) column is part of the where clause</a></li>
<li style="margin-top:10px;"><a href="https://tms-dev-blog.com/rust-sqlx-basics-with-sqlite/" title="Rust SQLx basics with SQLite: super easy how to" target="_blank">Rust SQLx basics with SQLite: super easy how to</a></li>
<li style="margin-top:10px;"><a href="https://docs.shuttle.rs/tutorials/databases-with-rust" title="Working with Databases in Rust" target="_blank">Working with Databases in Rust</a></li>
<li style="margin-top:10px;"><a href="https://github.com/launchbadge/sqlx/issues/44" title="Can't get value form mysql row #44" target="_blank">Can't get value form mysql row #44</a></li>
</ul>

```
Content of src/main.rs:
```

```rust
use sqlx::{FromRow, Pool, MySql, Error, MySqlPool};
use sqlx::types::time::Date;
use time::macros::format_description;

use async_std::task;

#[derive(FromRow)]
struct Employee {
    emp_no: i32,
    birth_date: Date,
    first_name: String,
    last_name: String,    
    gender: String,
    hire_date: Date,
}

async fn connect() -> Result&lt;Pool&lt;MySql>, Error> {
    return MySqlPool::connect("mysql://root:pcb.2176310315865259@localhost:3306/employees").await;
}

async fn do_run_query() {
    let result = task::block_on(connect());

    match result {
        Err(err) => {
            println!("Cannot connect to database [{}]", err.to_string());
        }        

        Ok(pool) => {
            let query_result = sqlx::query_as::&lt;_, Employee>("select * from employees where emp_no &lt;= 10010")
                .fetch_all(&pool).await.unwrap();

            println!("Number of Employees selected: {}", query_result.len());

            let format = format_description!("[day]/[month]/[year]");

            for (rindex, employee) in query_result.iter().enumerate() {
                println!("{}. No.: {}, Birth Date: {}, First Name: {}, Last Name: {}, Gender: {}, Hire Date: {}", 
                    rindex+1,
                    &employee.emp_no,
                    &employee.birth_date.format(&format).unwrap(),
                    &employee.first_name,
                    &employee.last_name,
                    &employee.gender,
                    &employee.hire_date.format(&format).unwrap());
            }
        }
    }
}

fn main() {
    task::block_on(do_run_query());
}
```

The fields in <code>struct Employee</code> match table <a href="#employees-table"><code>employees</code>'s</a> exactly. I think the code is self-explanatory, please see the relevant documentation for detail, I can't explain better than the official crates' documentation.

❸ <a id="stored-procedure">Select data via running a stored procedure</a>. The stored procedure is simple:

```sql
DELIMITER $$
CREATE DEFINER=`root`@`%` PROCEDURE `get_employees`( pmLastName varchar(16), pmFirstName varchar(14) )
    READS SQL DATA
begin
  select * from employees e where (e.last_name like pmLastName)
    and (e.first_name like pmFirstName) order by e.emp_no;
end$$
DELIMITER ;
```

Within MySQL Workbench, it can be called with:

```sql
call get_employees('%chi', '%ak'); 
call get_employees('%CHI', '%AK'); 
```

I could not find any example or documentation on how to call stored procedures. So willy-nilly, instead of a query, as seen in <a href="#sql-statement">Select data using a SQL statement</a> above, I pass in the stored procedure call:

```rust
            ...
            let query_result = sqlx::query_as::<_, Employee>("call get_employees('%chi', '%ak')")
                //.bind("%chi").bind("%ak")
                .fetch_all(&pool).await.unwrap();

            println!("Number of Employees selected: {}", query_result.len());
            ...			
```

It panics with:

```
F:\rust\sqlx>set RUST_BACKTRACE=1

F:\rust\sqlx>target\debug\learn_sqlx.exe
thread 'main' panicked at 'called `Result::unwrap()` on an `Err` value: ColumnNotFound("emp_no")', src\main.rs:32:41
stack backtrace:
...
```

I asked for help: <a href="https://users.rust-lang.org/t/how-to-call-a-mysql-stored-proc-using-crate-sqlx/99582" title="How to call a MySQL stored proc using crate sqlx?" target="_blank">How to call a MySQL stored proc using crate sqlx?</a> It seems that crate <a href="https://docs.rs/sqlx/latest/sqlx" title="Crate sqlx" target="_blank">sqlx</a> has some unresolved bug -- accessing resultant dataset column by name would cause a panic.

My first attempt based on the suggested solution: access the resultant dataset column by index, and copy column values into individual variables, then (process and) display these variables:

```
Content of src/main.rs:
```

```rust
use sqlx::{Pool, MySql, Error, MySqlPool, Row};
use sqlx::types::time::Date;
use time::macros::format_description;

use async_std::task;

async fn connect() -> Result&lt;Pool&lt;MySql>, Error> {
    return MySqlPool::connect("mysql://root:pcb.2176310315865259@localhost:3306/employees").await;
}

async fn do_run_stored_proc() {
    let result = task::block_on(connect());

    match result {
        Err(err) => {
            println!("Cannot connect to database [{}]", err.to_string());
        }        

        Ok(pool) => {
            let query_result = sqlx::query("call get_employees(?, ?)")
                .bind("%chi").bind("%ak")
                .fetch_all(&pool).await.unwrap();

            println!("Number of Employees selected: {}", query_result.len());

            let format = format_description!("[day]/[month]/[year]");

            for (rindex, row) in query_result.iter().enumerate() {
                let emp_no: i32 = row.get(0);
                let birth_date: Date = row.get(1);
                let first_name: String = row.get(2);
                let last_name: String = row.get(3);
                let gender: String = row.get(4);
                let hire_date: Date = row.get(5);

                println!("{}. No.: {}, Birth Date: {}, First Name: {}, Last Name: {}, Gender: {}, Hire Date: {}", 
                    rindex+1,
                    emp_no,
                    birth_date.format(&format).unwrap(),
                    first_name,
                    last_name,
                    gender,
                    hire_date.format(&format).unwrap());
            }
        }
    }
}

fn main() {
    task::block_on(do_run_stored_proc());
}
```

Based on the following posts:

<ul>
<li style="margin-top:10px;"><a href="https://stackoverflow.com/questions/61556540/how-do-i-load-sqlx-records-to-vec-of-structs-in-rust" title="How do I load SQLX records to Vec of structs in Rust" target="_blank">How do I load SQLX records to Vec of structs in Rust</a></li>
<li style="margin-top:10px;"><a href="https://gist.github.com/jeremychone/34d1e3daffc38eb602b1a9ab21298d10" title="jeremychone/rust-xp-02-postgresql-sqlx.rs" target="_blank">jeremychone/rust-xp-02-postgresql-sqlx.rs</a></li>
<li style="margin-top:10px;"><a href="https://juejin.cn/post/7239739777688092728" title="https://juejin.cn/post/7239739777688092728" target="_blank">https://juejin.cn/post/7239739777688092728</a></li>
</ul>

My second attempt at calling the stored procedure and manually map to <code>struct Employee</code>:

```
Content of src/main.rs:
```

```rust
use sqlx::{FromRow, Pool, MySql, Error, MySqlPool, Row};
use sqlx::types::time::Date;
use time::macros::format_description;

use async_std::task;

#[derive(FromRow)]
struct Employee {
    emp_no: i32,
    birth_date: Date,
    first_name: String,
    last_name: String,    
    gender: String,
    hire_date: Date,
}

async fn connect() -> Result&lt;Pool&lt;MySql>, Error> {
    return MySqlPool::connect("mysql://root:pcb.2176310315865259@localhost:3306/employees").await;
}

async fn do_run_stored_proc() {
    let result = task::block_on(connect());

    match result {
        Err(err) => {
            println!("Cannot connect to database [{}]", err.to_string());
        }        

        Ok(pool) => {
            let query_result = sqlx::query("call get_employees(?, ?)")
                .bind("%chi").bind("%ak")
                .map(|row: sqlx::mysql::MySqlRow| { 
                    Employee {
                        emp_no: row.get(0),
                        birth_date: row.get(1),
                        first_name: row.get(2),
                        last_name: row.get(3),
                        gender: row.get(4),
                        hire_date: row.get(5)
                    }
                })
                .fetch_all(&pool).await.unwrap();

            println!("Number of Employees selected: {}", query_result.len());

            let format = format_description!("[day]/[month]/[year]");

            for (rindex, employee) in query_result.iter().enumerate() {
                println!("{}. No.: {}, Birth Date: {}, First Name: {}, Last Name: {}, Gender: {}, Hire Date: {}", 
                    rindex+1,
                    &employee.emp_no,
                    &employee.birth_date.format(&format).unwrap(),
                    &employee.first_name,
                    &employee.last_name,
                    &employee.gender,
                    &employee.hire_date.format(&format).unwrap());
            }
        }
    }
}

fn main() {
    task::block_on(do_run_stored_proc());
}
```

Crate <a href="https://docs.rs/sqlx/latest/sqlx" title="Crate sqlx" target="_blank">sqlx</a> is very large, it'd take a lot of time to be fluent in this crate. This is my first step. It takes a lot of time to write these simple examples: Rust is certainly tougher to learn than Python!

I'm writing this post to have a record of my progress. But I do hope some newcomers find it helpful and useful. Thank you for reading and stay safe as always.

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
<a href="https://www.rust-lang.org/" target="_blank">https://www.rust-lang.org/</a>
</li>
<li>
<a href="https://www.pngitem.com/download/ibmJoR_rust-language-hd-png-download/" target="_blank">https://www.pngitem.com/download/ibmJoR_rust-language-hd-png-download/</a>
</li>
</ul>
