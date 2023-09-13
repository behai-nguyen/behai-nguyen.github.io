---
layout: post
title: "Rust & MySQL: delete, insert data using crate sqlx."

description: We'll look at&#58; how to delete data from and insert data into MySQL tables using crate sqlx.

tags:
- Rust
- MySQL
- sqlx
- delete
- insert
- write
---

<em style="color:#111;">We'll look at: how to delete data from and insert data into MySQL tables using crate <a href="https://docs.rs/sqlx/latest/sqlx" title="Crate sqlx" target="_blank">sqlx</a>.</em>

| ![082-feature-image.png](https://behainguyen.files.wordpress.com/2023/09/082-feature-image.png) |
|:--:|
| *Rust & MySQL: delete, insert data using crate sqlx.* |

This post is a continuation of <a href="https://behainguyen.wordpress.com/2023/09/12/rust-mysql-connect-execute-sql-statements-and-stored-procs-using-crate-sqlx/" title="Rust & MySQL: connect, execute SQL statements and stored procs using crate sqlx." target="_blank">Rust & MySQL: connect, execute SQL statements and stored procs using crate sqlx</a>. We'll use the same <a href="https://github.com/datacharmer/test_db" title="Oracle Corporation MySQL test data" target="_blank">Oracle Corporation MySQL test data</a> database. We'll also use the <a id="employees-table"><code>employees</code></a> table. To recap, its structure is:

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

And also the stored procedure:

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

<strong>Please note:</strong> <em>the example code has been tested on both Windows 10 and Ubuntu 22.10.</em>

❀❀❀

The followings are the references used to develop the code for this post:

<ul>
<li style="margin-top:10px;"><a href="https://docs.rs/sqlx/latest/sqlx/query/index.html" title="Module sqlx::query" target="_blank">Module sqlx::query</a></li>
<li style="margin-top:10px;"><a href="https://docs.rs/sqlx/latest/sqlx/query/struct.Query.html" title="Struct sqlx::query::Query" target="_blank">Struct sqlx::query::Query</a></li>
<li style="margin-top:10px;"><a href="https://stackoverflow.com/questions/75630538/inserting-a-struct-into-an-sqlite-db-using-sqlx-and-rust" title="Inserting a struct into an sqlite db using sqlx and rust" target="_blank">Inserting a struct into an sqlite db using sqlx and rust</a></li>
</ul>

<code>Cargo.toml</code> is also identical to the one used in the previous quoted post. Its <code>dependencies</code> section is as follow:

```toml
...
[dependencies]
async-std = "1.12.0"
sqlx = {version = "0.7", default-features = false, features = ["runtime-async-std", "macros", "mysql", "time"]}
time = {version = "0.3.22", default-features = false, features = ["formatting", "macros"]}
```

The example code is simple. We delete the employee whose number is <code>600000</code> from the database. If the deletion was successful, we would insert a new employee whose number is <code>600000</code>. Finally, if the addition was successful, we would retrieve the just inserted employee by calling the stored procedure <code>get_employees(...)</code>, with partial last name and partial first name of the just inserted employee.

The complete working example is presented below.

```
Content of src/main.rs:
```

```rust
use sqlx::{FromRow, Pool, MySql, Row, Error, MySqlPool};
use sqlx::types::time::Date;
use time::macros::{date, format_description};

use async_std::task;

#[derive(FromRow, Debug)]
pub struct Employee {
    pub emp_no: i32,
    pub birth_date: Date,
    pub first_name: String,
    pub last_name: String,    
    pub gender: String,
    pub hire_date: Date,
}

const TEST_EMP_NO: i32 = 600000; // Last emp_no in database is 500113.

async fn connect() -> Result<Pool<MySql>, Error> {
    return MySqlPool::connect("mysql://root:pcb.2176310315865259@localhost:3306/employees").await;
}

async fn do_delete(pool: &sqlx::Pool<MySql>, emp_no: i32) -> bool {
    let result = sqlx::query("delete from employees where emp_no = ?")
        .bind(emp_no)
        .execute(pool).await;

    match result {
        Err(e) => {
            println!("Error deleting employee: {}\n", e.to_string());
            return false;
        }

        Ok(res) => {
            println!("Employee number: {} has been deleted.", emp_no);
            println!("Number of Employees deleted: {}", res.rows_affected());            
        }
    }

    true
}

async fn do_insert(pool: &sqlx::Pool<MySql>, emp: &Employee) -> bool {
    let result = sqlx::query(
        "insert into employees (
            emp_no, 
            birth_date, 
            first_name, 
            last_name, 
            gender, 
            hire_date) 
        values (?, ?, ?, ?, ?, ?)")
        .bind(&emp.emp_no)
        .bind(&emp.birth_date)
        .bind(&emp.first_name)
        .bind(&emp.last_name)
        .bind(&emp.gender)
        .bind(&emp.hire_date)
        .execute(pool).await;

    match result {
        Err(e) => {
            println!("Error inserting employee: {:#?}", emp);
            println!("Error message: [{}].\n", e.to_string());
            return false;
        }

        Ok(res) => {
            println!("Employee has been inserted.");
            println!("Number of employees inserted: {}", res.rows_affected());
        }
    }

    true
}

async fn do_query(pool: &sqlx::Pool<MySql>, last_name: &str, first_name: &str) {
    let result = sqlx::query("call get_employees(?, ?)")
    .bind(last_name)
    .bind(first_name)
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
    .fetch_all(pool).await;

    match result {
        Err(e) => {
            println!("Error select employee with last name: {}, first name: {}", last_name, first_name);
            println!("Error message: [{}].\n", e.to_string());
        }

        Ok(query_result) => {
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

async fn do_delete_insert_data() {
    let result: Result<sqlx::Pool<sqlx::MySql>, sqlx::Error> = task::block_on(connect());

    match result {
        Err(err) => {
            println!("Cannot connect to database [{}]", err.to_string());
        }        

        Ok(pool) => {
            if !task::block_on(do_delete(&pool, TEST_EMP_NO)) {
                panic!("Failed to delete test employee.");
            }

            if !task::block_on(do_insert(&pool, &Employee {
                emp_no: TEST_EMP_NO,
                birth_date: date!(1999-11-24),
                first_name: String::from("Bé Hai"),
                last_name: String::from("Nguyễn"),
                gender: String::from("M"),
                hire_date: date!(2022-04-29)
            })) {
                panic!("Failed to insert test employee.");
            }

            task::block_on(do_query(&pool, "%uyễn", "%é H%"));
        }
    }
}

fn main() {
    task::block_on(do_delete_insert_data());
}
```

Some of the code should be familiar, based on the last <a href="https://behainguyen.wordpress.com/2023/09/12/rust-mysql-connect-execute-sql-statements-and-stored-procs-using-crate-sqlx/" title="Rust & MySQL: connect, execute SQL statements and stored procs using crate sqlx." target="_blank">mentioned post above</a>. We'll go over the new code.

<ul>
<li style="margin-top:10px;">Method <code>do_delete(pool: &sqlx::Pool&lt;MySql>, emp_no: i32) -> bool</code> is where test record deletion takes place. We call <a href="https://docs.rs/sqlx/latest/sqlx/query/index.html" title="Module sqlx::query" target="_blank">sqlx::query</a> with a parameterised <code>delete</code> SQL statement, this call returns <a href="https://docs.rs/sqlx/latest/sqlx/query/struct.Query.html" title="Struct sqlx::query::Query" target="_blank">struct sqlx::query::Query</a>. We then call its <a href="https://docs.rs/sqlx/latest/sqlx/query/struct.Query.html#method.bind" title="bind(...)" target="_blank">bind(...)</a> method to pass the value of <code>do_delete(...)</code>'s parameter <code>emp_no</code> to SQL statement parameter. We then chained-call to the <a href="https://docs.rs/sqlx/latest/sqlx/query/struct.Query.html#method.execute" title="execute(...)" target="_blank">execute(...)</a> method to run the <code>delete</code> SQL statement. If the deletion fails, we return <code>false</code> otherwise <code>true</code>.</li>
<li style="margin-top:10px;">Method <code>do_insert(pool: &sqlx::Pool&lt;MySql>, emp: &Employee) -> bool</code> is where test record insertion takes place. Its internal working is pretty much identical to <code>do_delete(...)</code>.</li>
<li style="margin-top:10px;">Method <code>do_query(pool: &sqlx::Pool&lt;MySql>, last_name: &str, first_name: &str)</code> is a just a refactored version of the last example in the <a href="https://behainguyen.wordpress.com/2023/09/12/rust-mysql-connect-execute-sql-statements-and-stored-procs-using-crate-sqlx/" title="Rust & MySQL: connect, execute SQL statements and stored procs using crate sqlx." target="_blank">above mentioned post</a>.</li>
<li style="margin-top:10px;">Method <code>do_delete_insert_data()</code> should be self-explanatory.</li>
</ul>

I write this example code for my own understanding, and this post so that I will have something to go back to if I forgot how to do this 😂. It has been easier than the last one. I do hope it's useful for somebody. Thank you for reading and stay safe as always.

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
