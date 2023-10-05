---
layout: post
title: "Rust & MySQL: JSON serialisation of result sets retrieved using crate sqlx."

description: We run a MySQL stored procedure which returns a result set which has date columns. Using crates serde and serde_json we serialise this result set into a JSON array of objects, whereby date columns are in Australian date format of dd/mm/yyyy.

tags:
- Rust
- MySQL
- sqlx
- JSON
- serialize
- deserialize
---

<em style="color:#111;">We run a MySQL stored procedure which returns a result set which has date columns. Using crates <a href="https://docs.rs/serde/latest/serde/" title="Crate serde" target="_blank">serde</a> and <a href="https://docs.rs/serde_json/1.0.107/serde_json/" title="Crate serde_json" target="_blank">serde_json</a>, we serialise this result set into a JSON array of objects, whereby date columns are in Australian date format of <code>dd/mm/yyyy</code>.</em>

| ![085-feature-image.png](https://behainguyen.files.wordpress.com/2023/10/085-feature-image.png) |
|:--:|
| *Rust & MySQL: JSON serialisation of result sets retrieved using crate sqlx.* |

This post is an extension of <a href="https://behainguyen.wordpress.com/2023/09/12/rust-mysql-connect-execute-sql-statements-and-stored-procs-using-crate-sqlx/" title="Rust & MySQL: connect, execute SQL statements and stored procs using crate sqlx." target="_blank">Rust & MySQL: connect, execute SQL statements and stored procs using crate sqlx</a>. We'll use the same <a href="https://github.com/datacharmer/test_db" title="Oracle Corporation MySQL test data" target="_blank">Oracle Corporation MySQL test database</a>, the same <code>employees</code> table and the same <code>get_employees</code> stored procedure.

To recap, the <a id="employees-table"><code>employees</code></a> table has the following structure:

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

And the <a id="get-employees-stored-proc"><code>get_employees</code></a> stored procedure is:

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

The code is an extension of the final version of the code in <a href="https://behai-nguyen.github.io/2023/09/11/rust-06-mysql-sqlx.html#stored-procedure" title="Rust & MySQL: connect, execute SQL statements and stored procs using crate sqlx" target="_blank">Select data via running a stored procedure</a> section of the previously mentioned post:

🚀 In this post, instead of manually formatting and printing each row of data, we serialise the entire result set into JSON and printing the JSON data out in a single operation.

The updated <code>dependencies</code> of the <code>Cargo.toml</code> file used in this post:

```toml
...
[dependencies]
async-std = "1.12.0"
sqlx = {version = "0.7", default-features = false, features = ["runtime-async-std", "macros", "mysql", "time"]}
time = {version = "0.3.22", default-features = false, features = ["formatting", "macros", "serde"]}
serde = {version = "1.0.188", features = ["derive"]}
serde_json = "1.0.107"
```

● For <a href="https://docs.rs/time/latest/time/" title="Crate time" target="_blank">time</a> crate, we add <code>serde</code> crate feature, so that we can do date serialising.

● We add two more crates for serialising and deserialising: <a href="https://docs.rs/serde/latest/serde/" title="Crate serde" target="_blank">serde</a> and <a href="https://docs.rs/serde_json/1.0.107/serde_json/" title="Crate serde_json" target="_blank">serde_json</a>.

The complete working example is presented below.

```
Content of src/main.rs:
```

```rust
use sqlx::{FromRow, Pool, MySql, Error, MySqlPool, Row};
use sqlx::types::time::Date;
use async_std::task;
use serde::Serialize;

#[derive(FromRow, Serialize)]
struct Employee {    
    emp_no: i32,
    #[serde(with = "my_date_format")]
    birth_date: Date,
    first_name: String,
    last_name: String,    
    gender: String,
    #[serde(with = "my_date_format")]
    hire_date: Date,
}

mod my_date_format {
    use sqlx::types::time::Date;
    use time::macros::format_description;
    use serde::{self, Serializer};

    pub fn serialize<S>(
        date: &Date,
        serializer: S,
    ) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let format = format_description!("[day]/[month]/[year]");
        let s = &date.format(&format).unwrap();
        serializer.serialize_str(&s)
    }    
}

async fn connect() -> Result<Pool<MySql>, Error> {
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

            let json = serde_json::to_string_pretty(&query_result).unwrap();
            println!("{}", json);
        }
    }
}

fn main() {
    task::block_on(do_run_stored_proc());
}
```

Let's walk through the code:

● Trait <a href="https://docs.rs/serde/latest/serde/trait.Serialize.html" title="Trait serde::Serialize" target="_blank">serde::Serialize</a> -- the <code>struct Employee</code> needs to implement this trait, so that it can be serialised.

● This documentation page <a href="https://serde.rs/custom-date-format.html" title="Date in a custom format" target="_blank">Date in a custom format</a> from crate <a href="https://docs.rs/serde/latest/serde/" title="Crate serde" target="_blank">serde</a> provides an example for date time serialisation and deserialisation. The <code>mod my_date_format</code> above comes from this example, but I implement only the serialisation part.

The date format in <code>pub fn serialize&lt;S></code> has been discussed in the <a href="https://behainguyen.wordpress.com/2023/09/12/rust-mysql-connect-execute-sql-statements-and-stored-procs-using-crate-sqlx/" title="Rust & MySQL: connect, execute SQL statements and stored procs using crate sqlx." target="_blank">previous mentioned post</a>, and in detail in <a href="https://behainguyen.wordpress.com/2023/09/03/rust-baby-step-some-preliminary-look-at-date/" title="Rust: baby step -- some preliminary look at date." target="_blank">Rust: baby step -- some preliminary look at date</a>.

● The derive macro helper attribute <code>#[serde(with = "my_date_format")]</code> also comes from <a href="https://serde.rs/custom-date-format.html" title="Date in a custom format" target="_blank">Date in a custom format</a>. Through trial and error, I've found out that it needs to be added to above all fields which need to be serialised.

● <code>let json = serde_json::to_string_pretty(&query_result).unwrap();</code> is also from <a href="https://serde.rs/custom-date-format.html" title="Date in a custom format" target="_blank">Date in a custom format</a>. Although the use of the variable <code>query_result</code> is trial and error... and by sheer luck, I have it working the first time round. Originally I thought of extracting each row into a vector, then serialise the vector: but that is too much additional work. <strong>If you asked me why <code>query_result</code> works in this case, I would not be able to explain!</strong> Hopefully, I will come to understand this in the future.

<strong>Please note:</strong> <em>the example code has been tested on both Windows 10 and Ubuntu 22.10.</em>

The following screenshot shows the output of the above example:

![085-01.png](https://behainguyen.files.wordpress.com/2023/10/085-01.png)

One final point, we look at deleting and inserting data in <a href="https://behainguyen.wordpress.com/2023/09/13/rust-mysql-delete-insert-data-using-crate-sqlx/" title="Rust & MySQL: delete, insert data using crate sqlx." target="_blank">Rust & MySQL: delete, insert data using crate sqlx</a>, also using the <a href="#employees-table"><code>employees</code></a> table. The updated <code>struct Employee</code> in this post would still work in the just mentioned post. This is because when we manually create an instance of <code>struct Employee</code>, we have the two date columns in the correct format, hence no deserialisation is required:

```rust
                ...
                birth_date: date!(1999-11-24),
                hire_date: date!(2022-04-29)
                ...   
```

Thank you for reading. I hope you find this post useful and stay safe as always.

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
<a href="https://icon-icons.com/download/168490/PNG/512/" target="_blank">https://icon-icons.com/download/168490/PNG/512/</a>
</li>
<li>
<a href="https://www.pngitem.com/download/ibmJoR_rust-language-hd-png-download/" target="_blank">https://www.pngitem.com/download/ibmJoR_rust-language-hd-png-download/</a>
</li>
</ul>