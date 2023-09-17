---
layout: post
title: "Rust & MySQL: executing MySQL stored procedures which return multiple result sets using crate sqlx."

description: MySQL stored procedures can return multiple result sets. In this post, we’re looking at calling such stored procedure. For each returned record set, we extract column values into a corresponding struct instance; and store this instance in a vector.

tags:
- Rust
- MySQL
- sqlx
- stored procedure
- multiple result sets
---

<em style="color:#111;">MySQL stored procedures can return multiple result sets. In this post, we’re looking at calling such stored procedure. For each returned record set, we extract column values into a corresponding <a href="https://doc.rust-lang.org/book/ch05-01-defining-structs.html" title="Defining and Instantiating Structs" target="_blank"><code>struct</code> </a> instance; and store this instance in a <a href="https://doc.rust-lang.org/std/vec/struct.Vec.html" title="Struct std::vec::Vec" target="_blank"><code>vector</code></a>.</em>

| ![083-feature-image.png](https://behainguyen.files.wordpress.com/2023/09/083-feature-image.png) |
|:--:|
| *Rust & MySQL: executing MySQL stored procedures which return multiple result sets using crate sqlx.* |

<!--
D:\Posts\083-rust-08-mysql-sqlx-multi-rsets-stored-procs\
-->

This post is a continuation of:

<ol>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/09/12/rust-mysql-connect-execute-sql-statements-and-stored-procs-using-crate-sqlx/" title="Rust & MySQL: connect, execute SQL statements and stored procs using crate sqlx." target="_blank">Rust & MySQL: connect, execute SQL statements and stored procs using crate sqlx</a>.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/09/13/rust-mysql-delete-insert-data-using-crate-sqlx/" title="Rust & MySQL: delete, insert data using crate sqlx." target="_blank">Rust & MySQL: delete, insert data using crate sqlx.</a>
</li>
</ol>

We'll use the same <a href="https://github.com/datacharmer/test_db" title="Oracle Corporation MySQL test data" target="_blank">Oracle Corporation MySQL test data</a> database. This time, we'll use the <code>departments</code> and the <code>dept_manager</code> tables. 

The <a id="departments-table"><code>departments</code> table</a>:

```sql
CREATE TABLE `departments` (
  `dept_no` char(4) NOT NULL,
  `dept_name` varchar(40) NOT NULL,
  PRIMARY KEY (`dept_no`),
  UNIQUE KEY `dept_name` (`dept_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

The <a id="dept_manager-table"><code>dept_manager</code> table</a>:

```sql
CREATE TABLE `dept_manager` (
  `emp_no` int NOT NULL,
  `dept_no` char(4) NOT NULL,
  `from_date` date NOT NULL,
  `to_date` date NOT NULL,
  PRIMARY KEY (`emp_no`,`dept_no`),
  KEY `dept_no` (`dept_no`),
  CONSTRAINT `dept_manager_ibfk_1` FOREIGN KEY (`emp_no`) REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,
  CONSTRAINT `dept_manager_ibfk_2` FOREIGN KEY (`dept_no`) REFERENCES `departments` (`dept_no`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

The <a id="demostoredproc1-stored-proc"><code>DemoStoredProc1</code> stored procedure:</a>

```sql
DELIMITER $$
CREATE DEFINER=`root`@`%` PROCEDURE `DemoStoredProc1`( pm_dept_no varchar(4) )
    READS SQL DATA
begin
  select * from departments where dept_no = pm_dept_no;
  select * from dept_manager where dept_no = pm_dept_no;
end$$
DELIMITER ;
```

Stored procedure <code>DemoStoredProc1(pm_dept_no varchar(4))</code> returns two result sets whose data come from tables <code>departments</code> and <code>dept_manager</code> respectively.

<strong>Please note:</strong> <em>the example code has been tested on both Windows 10 and Ubuntu 22.10.</em>

❀❀❀

I could not find any example or documentation on this multiple result sets issue. The final example code is the result of experimentation with crate <a href="https://docs.rs/sqlx/latest/sqlx" title="Crate sqlx" target="_blank">sqlx</a>.

The final <code>dependencies</code> section of the <code>Cargo.toml</code> file used in this post:

```toml
...
[dependencies]
async-std = "1.12.0"
sqlx = {version = "0.7", default-features = false, features = ["runtime-async-std", "macros", "mysql", "time"]}
```

To keep the example simple, we won't do time formatting, hence we don't need crate <a href="https://docs.rs/time/latest/time/" title="Crate time" target="_blank">time</a>.

As you can guess, for the example, we'll call the stored procedure <code>DemoStoredProc1</code> with a 4-character <code>dept_no</code>. The first resultant record set, from the <code>departments</code> table, will have at most one (1) record. The second resultant record set, from the <code>dept_manager</code> table, will have at least one (1) record.

The complete working example is presented below.

```
Content of src/main.rs:
```

```rust
use sqlx::{FromRow, Pool, MySql, Error, MySqlPool, Row};
use sqlx::types::time::Date;

use async_std::task;

#[derive(FromRow, Debug)]
pub struct Department {
    pub dept_no: String,
    pub dept_name: String,
}

#[derive(FromRow, Debug)]
pub struct DepartmentManager {
    pub emp_no: i32,
    pub dept_no: String,
    pub from_date: Date,
    pub to_date: Date,
}

async fn connect() -> Result<Pool<MySql>, Error> {
    return MySqlPool::connect("mysql://root:pcb.2176310315865259@localhost:3306/employees").await;
}

async fn do_run_stored_proc(pool: &sqlx::Pool<MySql>, dept_no: &str) {
    let result = sqlx::query("call DemoStoredProc1(?)")
    .bind(dept_no)
    .fetch_all(pool).await;

    match result {
        Err(e) => {
            println!("Error select data for department number: {}", dept_no);
            println!("Error message: [{}].\n", e.to_string());
        }

        Ok(query_result) => {
            let mut dept_vec = Vec::<Department>::new(); 
            let mut dept_mgr_vec = Vec::<DepartmentManager>::new();

            println!("dept_vec.len() = {}", dept_vec.len());
            println!("dept_mgr_vec.len() = {}", dept_mgr_vec.len());

            for row in query_result {
                if row.columns().len() == 2 {
                    dept_vec.push(Department{dept_no: row.get(0), dept_name: row.get(1)});
                }
                else {
                    dept_mgr_vec.push(DepartmentManager{
                        emp_no: row.get(0),
                        dept_no: row.get(1),
                        from_date: row.get(2),
                        to_date: row.get(3),
                    });
                }
            }

            println!("{:#?}", dept_vec);
            println!("{:#?}", dept_mgr_vec);
        }
    }
}

fn main() {
    let result: Result<sqlx::Pool<sqlx::MySql>, sqlx::Error> = task::block_on(connect());

    match result {
        Err(err) => {
            println!("Cannot connect to database [{}]", err.to_string());
        }        

        Ok(pool) => {
            task::block_on(do_run_stored_proc(&pool, "d009"));
        }
    }
}
```

The code is pretty much a refactored version of the code in the previous two mentioned posts. We declare two (2) new <code>struct</code>s: <code>Department</code> and <code>DepartmentManager</code> to capture the two (2) result sets.

We're interested the <code>for</code> loop in <code>async fn do_run_stored_proc(pool: &sqlx::Pool&lt;MySql>, dept_no: &str)</code>:

```rust
            ...
            for row in query_result {
                if row.columns().len() == 2 {
                    dept_vec.push(Department{dept_no: row.get(0), dept_name: row.get(1)});
                }
                else {
                    dept_mgr_vec.push(DepartmentManager{
                        emp_no: row.get(0),
                        dept_no: row.get(1),
                        from_date: row.get(2),
                        to_date: row.get(3),
                    });
                }
            }
            ...
```
			
Basically, for each row, if there're two (2) columns, we extract the values into an instance of the <code>struct Department</code>, and push this instance onto vector <code>dept_vec</code>. Otherwise, the row values go to an instance of the <code>struct DepartmentManager</code>, and this instance goes to vector <code>dept_mgr_vec</code>. <em>This logic is very weak. What should we do if the stored procedure returns three (3) result sets, and two (2) of them have two (2) columns each?</em> But, for the purpose of this post, we'll ignore this issue.

⓵ As mentioned previously, I've done several iterations before this final version of the code. My first attempt looking at the returned result is:

```rust
            ...
            for (rindex, row) in query_result.iter().enumerate() {
                println!("* Row number: {}", rindex+1);
                println!("* Total columns: {}", row.columns().len());
                println!("{:#?}\n", row);
            }
            ...
```

In total, there are only five (5) rows returned between the two (2) result sets, but the output is pretty long. Please see section <a href="#appendix-01">First Iteration Output</a> for the full printout.

⓶ Based on the output, we can see that all result sets returned. And there are no separate result sets. There're just rows, with different column meta. My first attempt, then, at extracting values out is to get the column data type, then case out (<code>match</code>) the data type: i.e. for each column data type, declare a variable of corresponding type, and extract the target column value into this variable. My attempt at getting the column data type:

```rust
use sqlx::{FromRow, Pool, MySql, Error, MySqlPool, Row, TypeInfo, Column};
...
            ...
            for (rindex, row) in query_result.iter().enumerate() {
                println!("* Row number: {}", rindex+1);
                println!("* Total columns: {}\n", row.columns().len());

                for (cindex, col) in row.columns().iter().enumerate() {
                    println!("{:#?}", col.type_info());
                    // println!("> {}. Name: {}. Value: {}.", cindex+1, col.name(), row.get(cindex));
                    println!("> {}. Name: {}. Type Name: {}.", cindex+1, col.name(), col.type_info().name());
                }
            }
            ...
```

<p>
-- Note, the two (2) additional traits added to the <code>use </code> declarations: <a href="https://docs.rs/sqlx/latest/sqlx/trait.TypeInfo.html" title="Trait sqlx::TypeInfo" target="_blank">Trait sqlx::TypeInfo</a> and <a href="https://docs.rs/sqlx/latest/sqlx/trait.Column.html" title="Trait sqlx::Column" target="_blank">trait sqlx::Column</a>.
</p>

<p>
Please see section <a href="#appendix-02">Second Iteration Output</a> for the output of the above <code>for</code> loop. <a href="https://docs.rs/sqlx/latest/sqlx/trait.TypeInfo.html" title="Trait sqlx::TypeInfo" target="_blank">Trait sqlx::TypeInfo</a> and <a href="https://docs.rs/sqlx-mysql/0.7.1/sqlx_mysql/struct.MySqlTypeInfo.html" title="Struct sqlx_mysql::MySqlTypeInfo" target="_blank">struct sqlx_mysql::MySqlTypeInfo</a> do give info on column meta data. But still <strong>I could not get to <code>pub enum ColumnType</code></strong>, and the documentation does not seem to have anything about <code>pub enum ColumnType</code> either (?). 
</p>

<p>
In hindsight, checking individual columns' data types, declaring variables, etc. is a bad idea... <strong>I can see in my mind, how messy, and error prone the code is going to be.<em> I'm not sure if the above solution is a correct or even an acceptable one</em></strong>, but it seems much cleaner. 
</p>

<p>
Again, this post is just a documentation of my learning progress. I do hope someone would find it useful. Thank you for reading and stay safe as always.
</p>

<p>✿✿✿</p>

<p>
Feature image source:
</p>

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

<p>✿✿✿</p>

<h3><a id="appendix-01">First Iteration Output</a></h3>

```
* Row number: 1
* Total columns: 2
MySqlRow {
    row: Row {
        storage: b"\0\x04d009\x10Customer Service",
        values: [
            Some(
                2..6,
            ),
            Some(
                7..23,
            ),
        ],
    },
    format: Binary,
    columns: [
        MySqlColumn {
            ordinal: 0,
            name: dept_no,
            type_info: MySqlTypeInfo {
                type: String,
                flags: ColumnFlags(
                    NOT_NULL | PRIMARY_KEY | NO_DEFAULT_VALUE,
                ),
                char_set: 224,
                max_size: Some(
                    16,
                ),
            },
            flags: Some(
                ColumnFlags(
                    NOT_NULL | PRIMARY_KEY | NO_DEFAULT_VALUE,
                ),
            ),
        },
        MySqlColumn {
            ordinal: 1,
            name: dept_name,
            type_info: MySqlTypeInfo {
                type: VarString,
                flags: ColumnFlags(
                    NOT_NULL | UNIQUE_KEY | NO_DEFAULT_VALUE,
                ),
                char_set: 224,
                max_size: Some(
                    160,
                ),
            },
            flags: Some(
                ColumnFlags(
                    NOT_NULL | UNIQUE_KEY | NO_DEFAULT_VALUE,
                ),
            ),
        },
    ],
    column_names: {},
}

* Row number: 2
* Total columns: 4
MySqlRow {
    row: Row {
        storage: b"\0L\xb4\x01\0\x04d009\x04\xc1\x07\x01\x01\x04\xc4\x07\n\x11",
        values: [
            Some(
                1..5,
            ),
            Some(
                6..10,
            ),
            Some(
                10..15,
            ),
            Some(
                15..20,
            ),
        ],
    },
    format: Binary,
    columns: [
        MySqlColumn {
            ordinal: 0,
            name: emp_no,
            type_info: MySqlTypeInfo {
                type: Long,
                flags: ColumnFlags(
                    NOT_NULL | PRIMARY_KEY | NO_DEFAULT_VALUE,
                ),
                char_set: 63,
                max_size: Some(
                    11,
                ),
            },
            flags: Some(
                ColumnFlags(
                    NOT_NULL | PRIMARY_KEY | NO_DEFAULT_VALUE,
                ),
            ),
        },
        MySqlColumn {
            ordinal: 1,
            name: dept_no,
            type_info: MySqlTypeInfo {
                type: String,
                flags: ColumnFlags(
                    NOT_NULL | PRIMARY_KEY | MULTIPLE_KEY | NO_DEFAULT_VALUE,
                ),
                char_set: 224,
                max_size: Some(
                    16,
                ),
            },
            flags: Some(
                ColumnFlags(
                    NOT_NULL | PRIMARY_KEY | MULTIPLE_KEY | NO_DEFAULT_VALUE,
                ),
            ),
        },
        MySqlColumn {
            ordinal: 2,
            name: from_date,
            type_info: MySqlTypeInfo {
                type: Date,
                flags: ColumnFlags(
                    NOT_NULL | BINARY | NO_DEFAULT_VALUE,
                ),
                char_set: 63,
                max_size: Some(
                    10,
                ),
            },
            flags: Some(
                ColumnFlags(
                    NOT_NULL | BINARY | NO_DEFAULT_VALUE,
                ),
            ),
        },
        MySqlColumn {
            ordinal: 3,
            name: to_date,
            type_info: MySqlTypeInfo {
                type: Date,
                flags: ColumnFlags(
                    NOT_NULL | BINARY | NO_DEFAULT_VALUE,
                ),
                char_set: 63,
                max_size: Some(
                    10,
                ),
            },
            flags: Some(
                ColumnFlags(
                    NOT_NULL | BINARY | NO_DEFAULT_VALUE,
                ),
            ),
        },
    ],
    column_names: {
        emp_no: 0,
        dept_no: 1,
        from_date: 2,
        to_date: 3,
    },
}

* Row number: 3
* Total columns: 4
MySqlRow {
    row: Row {
        storage: b"\0\xa8\xb4\x01\0\x04d009\x04\xc4\x07\n\x11\x04\xc8\x07\t\x08",
        values: [
            Some(
                1..5,
            ),
            Some(
                6..10,
            ),
            Some(
                10..15,
            ),
            Some(
                15..20,
            ),
        ],
    },
    format: Binary,
    columns: [
        MySqlColumn {
            ordinal: 0,
            name: emp_no,
            type_info: MySqlTypeInfo {
                type: Long,
                flags: ColumnFlags(
                    NOT_NULL | PRIMARY_KEY | NO_DEFAULT_VALUE,
                ),
                char_set: 63,
                max_size: Some(
                    11,
                ),
            },
            flags: Some(
                ColumnFlags(
                    NOT_NULL | PRIMARY_KEY | NO_DEFAULT_VALUE,
                ),
            ),
        },
        MySqlColumn {
            ordinal: 1,
            name: dept_no,
            type_info: MySqlTypeInfo {
                type: String,
                flags: ColumnFlags(
                    NOT_NULL | PRIMARY_KEY | MULTIPLE_KEY | NO_DEFAULT_VALUE,
                ),
                char_set: 224,
                max_size: Some(
                    16,
                ),
            },
            flags: Some(
                ColumnFlags(
                    NOT_NULL | PRIMARY_KEY | MULTIPLE_KEY | NO_DEFAULT_VALUE,
                ),
            ),
        },
        MySqlColumn {
            ordinal: 2,
            name: from_date,
            type_info: MySqlTypeInfo {
                type: Date,
                flags: ColumnFlags(
                    NOT_NULL | BINARY | NO_DEFAULT_VALUE,
                ),
                char_set: 63,
                max_size: Some(
                    10,
                ),
            },
            flags: Some(
                ColumnFlags(
                    NOT_NULL | BINARY | NO_DEFAULT_VALUE,
                ),
            ),
        },
        MySqlColumn {
            ordinal: 3,
            name: to_date,
            type_info: MySqlTypeInfo {
                type: Date,
                flags: ColumnFlags(
                    NOT_NULL | BINARY | NO_DEFAULT_VALUE,
                ),
                char_set: 63,
                max_size: Some(
                    10,
                ),
            },
            flags: Some(
                ColumnFlags(
                    NOT_NULL | BINARY | NO_DEFAULT_VALUE,
                ),
            ),
        },
    ],
    column_names: {
        emp_no: 0,
        dept_no: 1,
        from_date: 2,
        to_date: 3,
    },
}

* Row number: 4
* Total columns: 4
MySqlRow {
    row: Row {
        storage: b"\0\x05\xb5\x01\0\x04d009\x04\xc8\x07\t\x08\x04\xcc\x07\x01\x03",
        values: [
            Some(
                1..5,
            ),
            Some(
                6..10,
            ),
            Some(
                10..15,
            ),
            Some(
                15..20,
            ),
        ],
    },
    format: Binary,
    columns: [
        MySqlColumn {
            ordinal: 0,
            name: emp_no,
            type_info: MySqlTypeInfo {
                type: Long,
                flags: ColumnFlags(
                    NOT_NULL | PRIMARY_KEY | NO_DEFAULT_VALUE,
                ),
                char_set: 63,
                max_size: Some(
                    11,
                ),
            },
            flags: Some(
                ColumnFlags(
                    NOT_NULL | PRIMARY_KEY | NO_DEFAULT_VALUE,
                ),
            ),
        },
        MySqlColumn {
            ordinal: 1,
            name: dept_no,
            type_info: MySqlTypeInfo {
                type: String,
                flags: ColumnFlags(
                    NOT_NULL | PRIMARY_KEY | MULTIPLE_KEY | NO_DEFAULT_VALUE,
                ),
                char_set: 224,
                max_size: Some(
                    16,
                ),
            },
            flags: Some(
                ColumnFlags(
                    NOT_NULL | PRIMARY_KEY | MULTIPLE_KEY | NO_DEFAULT_VALUE,
                ),
            ),
        },
        MySqlColumn {
            ordinal: 2,
            name: from_date,
            type_info: MySqlTypeInfo {
                type: Date,
                flags: ColumnFlags(
                    NOT_NULL | BINARY | NO_DEFAULT_VALUE,
                ),
                char_set: 63,
                max_size: Some(
                    10,
                ),
            },
            flags: Some(
                ColumnFlags(
                    NOT_NULL | BINARY | NO_DEFAULT_VALUE,
                ),
            ),
        },
        MySqlColumn {
            ordinal: 3,
            name: to_date,
            type_info: MySqlTypeInfo {
                type: Date,
                flags: ColumnFlags(
                    NOT_NULL | BINARY | NO_DEFAULT_VALUE,
                ),
                char_set: 63,
                max_size: Some(
                    10,
                ),
            },
            flags: Some(
                ColumnFlags(
                    NOT_NULL | BINARY | NO_DEFAULT_VALUE,
                ),
            ),
        },
    ],
    column_names: {
        emp_no: 0,
        dept_no: 1,
        from_date: 2,
        to_date: 3,
    },
}

* Row number: 5
* Total columns: 4
MySqlRow {
    row: Row {
        storage: b"\0C\xb5\x01\0\x04d009\x04\xcc\x07\x01\x03\x04\x0f'\x01\x01",
        values: [
            Some(
                1..5,
            ),
            Some(
                6..10,
            ),
            Some(
                10..15,
            ),
            Some(
                15..20,
            ),
        ],
    },
    format: Binary,
    columns: [
        MySqlColumn {
            ordinal: 0,
            name: emp_no,
            type_info: MySqlTypeInfo {
                type: Long,
                flags: ColumnFlags(
                    NOT_NULL | PRIMARY_KEY | NO_DEFAULT_VALUE,
                ),
                char_set: 63,
                max_size: Some(
                    11,
                ),
            },
            flags: Some(
                ColumnFlags(
                    NOT_NULL | PRIMARY_KEY | NO_DEFAULT_VALUE,
                ),
            ),
        },
        MySqlColumn {
            ordinal: 1,
            name: dept_no,
            type_info: MySqlTypeInfo {
                type: String,
                flags: ColumnFlags(
                    NOT_NULL | PRIMARY_KEY | MULTIPLE_KEY | NO_DEFAULT_VALUE,
                ),
                char_set: 224,
                max_size: Some(
                    16,
                ),
            },
            flags: Some(
                ColumnFlags(
                    NOT_NULL | PRIMARY_KEY | MULTIPLE_KEY | NO_DEFAULT_VALUE,
                ),
            ),
        },
        MySqlColumn {
            ordinal: 2,
            name: from_date,
            type_info: MySqlTypeInfo {
                type: Date,
                flags: ColumnFlags(
                    NOT_NULL | BINARY | NO_DEFAULT_VALUE,
                ),
                char_set: 63,
                max_size: Some(
                    10,
                ),
            },
            flags: Some(
                ColumnFlags(
                    NOT_NULL | BINARY | NO_DEFAULT_VALUE,
                ),
            ),
        },
        MySqlColumn {
            ordinal: 3,
            name: to_date,
            type_info: MySqlTypeInfo {
                type: Date,
                flags: ColumnFlags(
                    NOT_NULL | BINARY | NO_DEFAULT_VALUE,
                ),
                char_set: 63,
                max_size: Some(
                    10,
                ),
            },
            flags: Some(
                ColumnFlags(
                    NOT_NULL | BINARY | NO_DEFAULT_VALUE,
                ),
            ),
        },
    ],
    column_names: {
        emp_no: 0,
        dept_no: 1,
        from_date: 2,
        to_date: 3,
    },
}
```

<h3><a id="appendix-02">Second Iteration Output</a></h3>

```
* Row number: 1
* Total columns: 2

MySqlTypeInfo {
    type: String,
    flags: ColumnFlags(
        NOT_NULL | PRIMARY_KEY | NO_DEFAULT_VALUE,
    ),
    char_set: 224,
    max_size: Some(
        16,
    ),
}
> 1. Name: dept_no. Type Name: CHAR.
MySqlTypeInfo {
    type: VarString,
    flags: ColumnFlags(
        NOT_NULL | UNIQUE_KEY | NO_DEFAULT_VALUE,
    ),
    char_set: 224,
    max_size: Some(
        160,
    ),
}
> 2. Name: dept_name. Type Name: VARCHAR.
* Row number: 2
* Total columns: 4

MySqlTypeInfo {
    type: Long,
    flags: ColumnFlags(
        NOT_NULL | PRIMARY_KEY | NO_DEFAULT_VALUE,
    ),
    char_set: 63,
    max_size: Some(
        11,
    ),
}
> 1. Name: emp_no. Type Name: INT.
MySqlTypeInfo {
    type: String,
    flags: ColumnFlags(
        NOT_NULL | PRIMARY_KEY | MULTIPLE_KEY | NO_DEFAULT_VALUE,
    ),
    char_set: 224,
    max_size: Some(
        16,
    ),
}
> 2. Name: dept_no. Type Name: CHAR.
MySqlTypeInfo {
    type: Date,
    flags: ColumnFlags(
        NOT_NULL | BINARY | NO_DEFAULT_VALUE,
    ),
    char_set: 63,
    max_size: Some(
        10,
    ),
}
> 3. Name: from_date. Type Name: DATE.
MySqlTypeInfo {
    type: Date,
    flags: ColumnFlags(
        NOT_NULL | BINARY | NO_DEFAULT_VALUE,
    ),
    char_set: 63,
    max_size: Some(
        10,
    ),
}
> 4. Name: to_date. Type Name: DATE.
* Row number: 3
* Total columns: 4

MySqlTypeInfo {
    type: Long,
    flags: ColumnFlags(
        NOT_NULL | PRIMARY_KEY | NO_DEFAULT_VALUE,
    ),
    char_set: 63,
    max_size: Some(
        11,
    ),
}
> 1. Name: emp_no. Type Name: INT.
MySqlTypeInfo {
    type: String,
    flags: ColumnFlags(
        NOT_NULL | PRIMARY_KEY | MULTIPLE_KEY | NO_DEFAULT_VALUE,
    ),
    char_set: 224,
    max_size: Some(
        16,
    ),
}
> 2. Name: dept_no. Type Name: CHAR.
MySqlTypeInfo {
    type: Date,
    flags: ColumnFlags(
        NOT_NULL | BINARY | NO_DEFAULT_VALUE,
    ),
    char_set: 63,
    max_size: Some(
        10,
    ),
}
> 3. Name: from_date. Type Name: DATE.
MySqlTypeInfo {
    type: Date,
    flags: ColumnFlags(
        NOT_NULL | BINARY | NO_DEFAULT_VALUE,
    ),
    char_set: 63,
    max_size: Some(
        10,
    ),
}
> 4. Name: to_date. Type Name: DATE.
* Row number: 4
* Total columns: 4

MySqlTypeInfo {
    type: Long,
    flags: ColumnFlags(
        NOT_NULL | PRIMARY_KEY | NO_DEFAULT_VALUE,
    ),
    char_set: 63,
    max_size: Some(
        11,
    ),
}
> 1. Name: emp_no. Type Name: INT.
MySqlTypeInfo {
    type: String,
    flags: ColumnFlags(
        NOT_NULL | PRIMARY_KEY | MULTIPLE_KEY | NO_DEFAULT_VALUE,
    ),
    char_set: 224,
    max_size: Some(
        16,
    ),
}
> 2. Name: dept_no. Type Name: CHAR.
MySqlTypeInfo {
    type: Date,
    flags: ColumnFlags(
        NOT_NULL | BINARY | NO_DEFAULT_VALUE,
    ),
    char_set: 63,
    max_size: Some(
        10,
    ),
}
> 3. Name: from_date. Type Name: DATE.
MySqlTypeInfo {
    type: Date,
    flags: ColumnFlags(
        NOT_NULL | BINARY | NO_DEFAULT_VALUE,
    ),
    char_set: 63,
    max_size: Some(
        10,
    ),
}
> 4. Name: to_date. Type Name: DATE.
* Row number: 5
* Total columns: 4

MySqlTypeInfo {
    type: Long,
    flags: ColumnFlags(
        NOT_NULL | PRIMARY_KEY | NO_DEFAULT_VALUE,
    ),
    char_set: 63,
    max_size: Some(
        11,
    ),
}
> 1. Name: emp_no. Type Name: INT.
MySqlTypeInfo {
    type: String,
    flags: ColumnFlags(
        NOT_NULL | PRIMARY_KEY | MULTIPLE_KEY | NO_DEFAULT_VALUE,
    ),
    char_set: 224,
    max_size: Some(
        16,
    ),
}
> 2. Name: dept_no. Type Name: CHAR.
MySqlTypeInfo {
    type: Date,
    flags: ColumnFlags(
        NOT_NULL | BINARY | NO_DEFAULT_VALUE,
    ),
    char_set: 63,
    max_size: Some(
        10,
    ),
}
> 3. Name: from_date. Type Name: DATE.
MySqlTypeInfo {
    type: Date,
    flags: ColumnFlags(
        NOT_NULL | BINARY | NO_DEFAULT_VALUE,
    ),
    char_set: 63,
    max_size: Some(
        10,
    ),
}
> 4. Name: to_date. Type Name: DATE.
```