---
layout: post
title: "Rust web application: MySQL server, sqlx, actix-web and tera."

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.files.wordpress.com/2023/10/087-02-a.png"
    - "https://behainguyen.files.wordpress.com/2023/10/087-02-b.png"

gallery-image-list-2:
    - "https://behainguyen.files.wordpress.com/2023/10/087-03-a.png"
    - "https://behainguyen.files.wordpress.com/2023/10/087-03-b.png"

gallery-image-list-3:
    - "https://behainguyen.files.wordpress.com/2023/10/087-04-a.png"
    - "https://behainguyen.files.wordpress.com/2023/10/087-04-b.png"

gallery-image-list-4:
    - "https://behainguyen.files.wordpress.com/2023/10/087-05-a.png"
    - "https://behainguyen.files.wordpress.com/2023/10/087-05-b.png"

gallery-image-list-5:
    - "https://behainguyen.files.wordpress.com/2023/10/087-06.png"

description: We write a Rust web application using a MySQL database. We use the already familiar crate sqlx for database works. The web framework we're using is crate actix-web. For Cross-Origin Resource Sharing (CORS) controls, we use crate actix-cors. For HTML template processing, we use crate tera, which implements Jinja2 template syntax.
tags:
- Rust
- mysql
- web
- sqlx
- actix-web
- tera
- jinja2
---

<em style="color:#111;">We write a Rust web application using a MySQL database. We use the already familiar crate <a href="https://docs.rs/sqlx/latest/sqlx" title="Crate sqlx" target="_blank">sqlx</a> for database works. The web framework we're using is crate <a href="https://actix.rs/docs/" title="actix-web" target="_blank">actix-web</a>. For Cross-Origin Resource Sharing (CORS) controls, we use crate <a href="https://docs.rs/actix-cors/latest/actix_cors/" title="actix-cors" target="_blank">actix-cors</a>. For HTML template processing, we use crate <a href="https://docs.rs/tera/latest/tera/" title="tera" target="_blank">tera</a>, which implements <a href="http://jinja.pocoo.org/" title="Jinja2" target="_blank">Jinja2</a> template syntax.</em>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rust_web_01" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![087-feature-image.png](https://behainguyen.files.wordpress.com/2023/10/087-feature-image.png) |
|:--:|
| *Rust web application: MySQL server, sqlx, actix-web and tera.* |

The test project built in this post will have the following routes:

<ul>
<li style="margin-top:10px;">
JSON response route <code>http://0.0.0.0:5000/data/employees</code> -- method: <code>POST</code>; content type: <code>application/json</code>; request body: <code>{"last_name": "%chi", "first_name": "%ak"}</code>.
</li>
<li style="margin-top:10px;">
JSON response route <code>http://0.0.0.0:5000/data/employees/%chi/%ak</code> -- method <code>GET</code>.
</li>
<li style="margin-top:10px;">
HTML response route <code>http://0.0.0.0:5000/ui/employees</code> -- method: <code>POST</code>; content type: <code>application/x-www-form-urlencoded; charset=UTF-8</code>; request body: <code>last_name=%chi&first_name=%ak</code>.
</li>
<li style="margin-top:10px;">
HTML response route <code>http://0.0.0.0:5000/ui/employees/%chi/%ak</code> -- method: <code>GET</code>.
</li>
</ul>

This post does not discuss authentication, i.e. login, as this's a learning journey for me, I'm deliberately avoiding this potentially complex subject, perhaps we'll look into it in the future.

<h2>Table of contents</h2>

<ul>
    <li style="margin-top:10px;">
		<a href="#database-mysql-server-used">The Database and MySQL Database Server</a>
	</li>

    <li style="margin-top:10px;">
        <a href="#crates-used-in-this-post">Crates Used In This Post</a>		
	    <ul>
            <li style="margin-top:10px;">
                <a href="#new-crates">Crates Which We Have Not Covered Before</a>
            </li>
			
            <li style="margin-top:10px;">
                <a href="#covered-crates">Crates Which We Have Covered Before</a>
            </li>			
	    </ul>
	</li>
	
    <li style="margin-top:10px;">
        <a href="#the-example-code">The Example Code</a>
		
	    <ul>
            <li style="margin-top:10px;">
                <a href="#the-cargo-file">The Cargo.toml File</a>
            </li>
			
            <li style="margin-top:10px;">
                <a href="#the-env-file">The .env File</a>
            </li>			
			
            <li style="margin-top:10px;">
                <a href="#the-employees-template-file">The templates/employees.html File</a>
            </li>						
			
            <li style="margin-top:10px;">
                <a href="#the-rust-code">The Rust Code</a>
				
                <ul>
                    <li style="margin-top:10px;">
					    <a href="#src-config">src/config.rs</a>
                    </li>
					
                    <li style="margin-top:10px;">
					    <a href="#src-utils">src/utils.rs</a>
                    </li>
					
                    <li style="margin-top:10px;">
					    <a href="#src-database">src/database.rs</a>
                    </li>

                    <li style="margin-top:10px;">
					    <a href="#src-models">src/models.rs</a>
                    </li>
					
                    <li style="margin-top:10px;">
					    <a href="#src-handlers">src/handlers.rs</a>
                    </li>
					
                    <li style="margin-top:10px;">
					    <a href="#src-main">src/main.rs</a>
                    </li>
                </ul>				
            </li>									
	    </ul>
	</li>

    <li style="margin-top:10px;">
        <a href="#some-visual-test-Runs">Some Visual Test Runs</a>
	</li>

    <li style="margin-top:10px;">
        <a href="#concluding-remarks">Concluding Remarks</a>
	</li>
</ul>

<h2 style="color:teal;text-transform: none;">
  <a id="database-mysql-server-used">The Database and MySQL Database Server</a>
</h2>

❶ We'll use the same 
<a href="https://github.com/datacharmer/test_db" title="Oracle Corporation MySQL test data" target="_blank">Oracle Corporation MySQL test database</a>, the same <code>employees</code> table and the same <code>get_employees</code> stored procedure; which we've used in other Rust and none-Rust posts.

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

<p>
❷ The MySQL server used is a Docker container discussed in the following posts:

<ul>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/09/22/docker-on-ubuntu-22-10-running-mysql8-0-34-debian-with-custom-config-socket-database-and-log-files-reside-on-host-machine/" title="Docker on Ubuntu 22.10: running mysql:8.0.34-debian with custom config, socket, database and log files reside on host machine." target="_blank">Docker on Ubuntu 22.10: running mysql:8.0.34-debian with custom config, socket, database and log files reside on host machine</a>.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2022/08/09/docker-on-windows-10-running-mysql8-0-30-debian-with-a-custom-config-file/" title="Docker on Windows 10: running mysql:8.0.30-debian with a custom config file." target="_blank">Docker on Windows 10: running mysql:8.0.30-debian with a custom config file.</a></li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2022/10/21/docker-on-windows-10-mysql8-0-30-debian-log-files/" title="Docker on Windows 10: mysql:8.0.30-debian log files" target="_blank">Docker on Windows 10: mysql:8.0.30-debian log files</a></li>
</ul>
</p>

<h2 style="color:teal;text-transform: none;">
  <a id="crates-used-in-this-post">Crates Used In This Post</a>
</h2>

Let's discuss the crates, to get them out of the way. 

<h3 style="color:teal;text-transform: none;">
  <a id="new-crates">Crates Which We Have Not Covered Before</a>
</h3>

● Crate <a href="https://actix.rs/docs/" title="actix-web" target="_blank">actix-web</a> -- this's the web development framework that I choose to learn. I'm aware of several others. I choose this one due to the comparison presented by the following sites:

<ul>
<li style="margin-top:10px;">
<a href="https://www.arewewebyet.org/topics/frameworks/" title="Web Frameworks" target="_blank">Web Frameworks</a>
</li>
<li style="margin-top:10px;">
<a href="https://kerkour.com/rust-web-framework-2022" title="Which Rust web framework to choose in 2022 (with code examples)" target="_blank">Which Rust web framework to choose in 2022 (with code examples)</a>
</li>
</ul>

Crate <a href="https://actix.rs/docs/" title="actix-web" target="_blank">actix-web</a> ranks top based on popularity and supported features. For beginners, the official tutorial can be a bit daunting, at least for me. But after completing all tutorials, we should've an overall understanding of this crate. It's a good investment.

● The example code in this post applies Cross-Origin Resource Sharing (CORS) controls. This Amazon Web Services article <a href="https://aws.amazon.com/what-is/cross-origin-resource-sharing/" title="What is Cross-Origin Resource Sharing?" target="_blank">What is Cross-Origin Resource Sharing?</a> offers a very good explanation of what CORS is.

<a id="crate-actix-cors"></a> Crate <a href="https://docs.rs/actix-cors/latest/actix_cors/" title="actix-cors" target="_blank">actix-cors</a> -- this's a middleware which implements CORS controls for <a href="https://actix.rs/docs/" title="actix-web" target="_blank">actix-web</a>. Take note of the given <a href="https://docs.rs/actix-cors/latest/actix_cors/index.html#example" title="Example" target="_blank">Example</a>, the example code will copy this implementation as is, and we'll also call <a href="https://docs.rs/actix-cors/latest/actix_cors/struct.Cors.html#method.supports_credentials" title="pub fn supports_credentials(self) -> Cors" target="_blank">pub fn supports_credentials(self) -> Cors</a> to make the implementation a bit more secured:

```rust
        let cors = Cors::default()
            .allowed_origin(&config.allowed_origin)
            .allowed_methods(vec!["GET", "POST"])
            .allowed_headers(vec![
                header::CONTENT_TYPE,
                header::AUTHORIZATION,
                header::ACCEPT,
            ])
            .max_age(config.max_age)
            .supports_credentials();
```

<a id="crate-tera"></a>
● Crate <a href="https://docs.rs/tera/latest/tera/" title="tera" target="_blank">tera</a> -- this's a template processing engine middleware. It's based on the <a href="http://jinja.pocoo.org/" title="Jinja2" target="_blank">Jinja2</a> engine, which I'am familiar with. There're several crates which were <a href="http://jinja.pocoo.org/" title="Jinja2" target="_blank">Jinja2</a>-based. I choose this one due to the comparison presented by the following site <a href="https://rust.libhunt.com/compare-askama-vs-tera" title="Compare askama and tera's popularity and activity" target="_blank">Compare askama and tera's popularity and activity</a>, and <a href="https://docs.rs/tera/latest/tera/" title="tera" target="_blank">tera</a> seems to be more popular, and the documentation page offers a usage example, although it's a bit weak.

This page <a href="https://zsiciarz.github.io/24daysofrust/book/vol2/day15.html" title="Day 15 - tera" target="_blank">Day 15 - tera</a> offers a more comprehensive example, whereby a <a href="https://doc.rust-lang.org/std/vec/struct.Vec.html" title="Rust vector" target="_blank">Rust vector</a> is passed to the template. <strong>Please note, the code is a bit outdated, but together with the official example, we can make it works with little effort.</strong>

This GitHub page <a href="https://github.com/Keats/tera#tera" title="Tera" target="_blank">Tera</a> has an example of how a template renders data passed in.

● Crate <a href="https://docs.rs/dotenv/latest/dotenv/" title="dotenv" target="_blank">dotenv</a> -- supports <code>.env</code> file. We'll use the code presented in the <a href="https://docs.rs/dotenv/latest/dotenv/fn.dotenv.html#examples" title="Example" target="_blank">Example</a> page.

We've used the <code>.env</code> file before, in this post <a href="https://behainguyen.wordpress.com/2023/10/10/rust-sqlx-cli-database-migration-with-mysql-and-postgresql/" title="Rust SQLx CLI: database migration with MySQL and PostgreSQL." target="_blank">Rust SQLx CLI: database migration with MySQL and PostgreSQL</a>.

<h3 style="color:teal;text-transform: none;">
  <a id="covered-crates">Crates Which We Have Covered Before</a>
</h3>

In addition to the above new crates, we also use some of the crates which we have used before: <a href="https://docs.rs/time/latest/time/" title="Crate time" target="_blank">time</a>, <a href="https://docs.rs/sqlx/latest/sqlx" title="Crate sqlx" target="_blank">sqlx</a>, <a href="https://github.com/async-rs/async-std" title="async-std" target="_blank">async-std</a>, <a href="https://docs.rs/serde/latest/serde/" title="Crate serde" target="_blank">serde</a> and <a href="https://docs.rs/serde_json/1.0.107/serde_json/" title="Crate serde_json" target="_blank">serde_json</a>.

Among other previous posts, we've covered these crates in the following posts in chronological order of most recent to least:

<ul>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/10/05/rust-mysql-json-serialisation-of-result-sets-retrieved-using-crate-sqlx/" title="Rust & MySQL: JSON serialisation of result sets retrieved using crate sqlx." target="_blank">Rust & MySQL: JSON serialisation of result sets retrieved using crate sqlx</a>.
</li>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/09/12/rust-mysql-connect-execute-sql-statements-and-stored-procs-using-crate-sqlx/" title="Rust & MySQL: connect, execute SQL statements and stored procs using crate sqlx." target="_blank">Rust & MySQL: connect, execute SQL statements and stored procs using crate sqlx</a>.
</li>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/09/03/rust-baby-step-some-preliminary-look-at-date/" title="Rust: baby step -- some preliminary look at date." target="_blank">Rust: baby step -- some preliminary look at date</a>.
</li>
</ul>

<h2 style="color:teal;text-transform: none;">
  <a id="the-example-code">The Example Code</a>
</h2>

The complete source code for this post is on <a href="https://github.com/behai-nguyen/rust_web_01.git" title="Source code on GitHub" target="_blank">GitHub</a>. <span style="font-weight:bold;color:blue;">The code for this post has been tagged with <code>v0.1.0</code></span>. To get the code at this tag, i.e. the code for this post, run the command:

```
git clone -b v0.1.0 https://github.com/behai-nguyen/rust_web_01.git
```

The layout of the project is shown the screenshot below:

![087-01.png](https://behainguyen.files.wordpress.com/2023/10/087-01.png)

To keep it simple, all modules live in the <code>src/</code> directory. 

<h3 style="color:teal;text-transform: none;">
  <a id="the-cargo-file">The Cargo.toml File</a>
</h3>

The <code>Cargo.toml</code> file includes all crates we've discussed in the previous section. View the content of <a href="https://github.com/behai-nguyen/rust_web_01/blob/main/Cargo.toml" title="Cargo.toml on GitHub." target="_blank">Cargo.toml on GitHub</a>. We've covered <a href="https://doc.rust-lang.org/cargo/reference/features.html#dependency-features" title="crate features" target="_blank">crate features</a> in some other previous posts.

<h3 style="color:teal;text-transform: none;">
  <a id="the-env-file">The .env File</a>
</h3>

We store some configuration items in the <code>.env</code> file. Its content is reproduced below:

```ini
MAX_CONNECTIONS=15
DATABASE_URL=mysql://root:pcb.2176310315865259@localhost:3306/employees

ALLOWED_ORIGIN=http://localhost
MAX_AGE=3600
```

<ul>
<li style="margin-top:10px;">
<code>MAX_CONNECTIONS</code>: the maximum total number of database connections in the pool.
</li>
<li style="margin-top:10px;">
<code>DATABASE_URL</code>: MySQL database connection string. We've seen this connection string in other Rust posts.
</li>
<li style="margin-top:10px;">
<code>ALLOWED_ORIGIN</code>: CORS' <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin" title="Access-Control-Allow-Origin" target="_blank">Access-Control-Allow-Origin</a>. This value can be a list, but to keep the example simple, we use only one.
</li>
<li style="margin-top:10px;">
<code>MAX_AGE</code>: CORS' <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Max-Age" title="Access-Control-Max-Age" target="_blank">Access-Control-Max-Age</a>. This value specifies the duration, in seconds, that the preflight results can be cached in the browser. When this duration elapses, the browser'll need to send another <a href="https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request" title="preflight request" target="_blank">preflight request</a>.
</li>
</ul>

<h3 style="color:teal;text-transform: none;">
  <a id="the-employees-template-file">The templates/employees.html File</a>
</h3>

The <a href="https://github.com/behai-nguyen/rust_web_01/blob/main/templates/employees.html" title="templates/employees.html on GitHub" target="_blank">templates/employees.html on GitHub</a>. This's a <a href="http://jinja.pocoo.org/" title="Jinja2" target="_blank">Jinja2</a> template. Rust code passes to it the <code>employees</code> vector, where each element is a JSON object.

If there is at least one (1) element in the vector, we'll display the list of employees in an HTML table. We first render the header row, then enter the <code>for loop</code> to display each employee. It's a simple template, there isn't any CSS.

<h3 style="color:teal;text-transform: none;">
  <a id="the-rust-code">The Rust Code</a>
</h3>

To recap, please note that: <span style="font-weight:bold;color:blue;">the code for this post has been tagged with <code>v0.1.0</code></span>.

Except for <code>src/main.rs</code>, all other module files should have sufficient documentation to explain the code. To view the documentation in a browser, on the terminal command line, just change to the project root directory, i.e. where <code>Cargo.toml</code> file is, and run the following command:

```
cargo doc --open
```

But I think it's easier just to open the file and read it!

<h4 style="color:teal;text-transform: none;">
  <a id="src-config">src/config.rs</a>
</h4>

This's the run time representation of the <code>.env</code> file. We define a <code>struct</code> with fields that match the corresponding entries in the <code>.env</code> file, and a function to load field values from the file to the <code>struct</code>.

<h4 style="color:teal;text-transform: none;">
  <a id="src-utils">src/utils.rs</a>
</h4>

It has only a short, single <code>mod australian_date_format</code>, which serialises MySQL date into an Australian date format <code>dd/mm/yyyy</code>. It's also in <a href="https://behainguyen.wordpress.com/2023/10/05/rust-mysql-json-serialisation-of-result-sets-retrieved-using-crate-sqlx/" title="Rust & MySQL: JSON serialisation of result sets retrieved using crate sqlx." target="_blank">Rust & MySQL: JSON serialisation of result sets retrieved using crate sqlx</a>, where its name is <code>mod my_date_format</code>.

<h4 style="color:teal;text-transform: none;">
  <a id="src-database">src/database.rs</a>
</h4>

The intention is, this module is responsible for database connection. In a proper application, I imagine it would be a substantial module. But for this project, there's only a single method <code>get_mysql_pool</code>, it attempts to connect to the target MySQL database, if successful, it prints a success message to the console, and returns the pool. Otherwise, it prints some failure messages, and terminates the application.

<h4 style="color:teal;text-transform: none;">
  <a id="src-models">src/models.rs</a>
</h4>

This module is about the <a href="#employees-table"><code>employees</code></a> table. Please note, <code>struct Employee</code> as defined in this module, has also been used in the previously mentioned post <a href="https://behainguyen.wordpress.com/2023/10/05/rust-mysql-json-serialisation-of-result-sets-retrieved-using-crate-sqlx/" title="Rust & MySQL: JSON serialisation of result sets retrieved using crate sqlx." target="_blank">Rust & MySQL: JSON serialisation of result sets retrieved using crate sqlx</a>.

I imagine that, in a proper application, it would be a <code>models/</code> sub-directory instead of a single file. And underneath this <code>models/</code> directory, there would be the actual <code>employees.rs</code> module among other modules for other tables. And each module would've all relevant functions that operate on the target database table.

For this project, we have only a single <code>pub async fn get_employees(...)</code> which attempts to retrieve data from the <code>employees</code> table based on partial last name and partial first name. This function is a refactored version of the function <code>async fn do_run_stored_proc()</code>, which is also in the previously mentioned post <a href="https://behainguyen.wordpress.com/2023/10/05/rust-mysql-json-serialisation-of-result-sets-retrieved-using-crate-sqlx/" title="Rust & MySQL: JSON serialisation of result sets retrieved using crate sqlx." target="_blank">Rust & MySQL: JSON serialisation of result sets retrieved using crate sqlx</a>, and also in some other earlier posts.

<h4 style="color:teal;text-transform: none;">
  <a id="src-handlers">src/handlers.rs</a>
</h4>

This's where all the HTTP request handler methods are. In a <a href="https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller" title="Model–view–controller" target="_blank">Model–View–Controller</a> pattern, I think this's the <code>controller</code>? Again, in a proper application, there'd be several of these modules, and <code>handlers/</code> or <code>controllers/</code> would be a project sub-directory where these modules live. In Python, I've seen others use <code>controllers/</code>, and I follow, too.

We've four (4) methods to handle POST and GET requests. These methods demonstrate the most common and basic tasks any web application usually implements. ⓵ Accepting <code>POST</code> requests in <code>JSON</code> and <code>x-www-form-urlencoded</code>, and returning a response in either JSON or HTML. ⓶ Accepting <code>GET</code> requests where data are in <code>request paths</code> and returning a response in either JSON or HTML.

<ol>
<li style="margin-top:10px;">
<code>pub async fn employees_json1(...)</code>: accepting <code>POST</code> requests in <code>JSON</code>, and returning responses in JSON. See also: 
<ul>
<li style="margin-top:10px;">
<a href="https://actix.rs/docs/extractors/#json" title="Request JSON Extractor" target="_blank">Request JSON Extractor</a>.
</li>
<li style="margin-top:10px;">
<a href="https://actix.rs/docs/response/#json-response" title="JSON Response" target="_blank">JSON Response</a>.
</li>
</ul>
</li>

<li style="margin-top:10px;">
<code>pub async fn employees_json2(...)</code>: accepting <code>GET</code> requests where data are in <code>request paths</code> and returning responses in JSON. See also:
<ul>
<li style="margin-top:10px;">
<a href="https://actix.rs/docs/extractors/#path" title="Request Path Extractor" target="_blank">Request Path Extractor</a>.
</li>
<li style="margin-top:10px;">
<a href="https://actix.rs/docs/response/#json-response" title="JSON Response" target="_blank">JSON Response</a>.
</li>
</ul>
</li>

<li style="margin-top:10px;">
<code>pub async fn employees_html1(...)</code>: accepting <code>POST</code> requests in <code>x-www-form-urlencoded</code>, and returning responses in HTML. See also: 
<ul>
<li style="margin-top:10px;">
<a href="https://actix.rs/docs/extractors/#url-encoded-forms" title="Request URL-Encoded Forms Extractor" target="_blank">Request URL-Encoded Forms Extractor</a>.
</li>
<li style="margin-top:10px;">
Template processing <a href="#crate-tera">using crate Tera</a> section.
</li>
<li style="margin-top:10px;">
Return HTML: there isn't an explicit section within <a href="https://actix.rs/docs/" title="actix-web" target="_blank">actix-web</a> discussing returning HTML... It seems that any text responses other than JSON imply HTML? However, this example explicitly shows an <a href="https://github.com/actix/examples/tree/master/forms/multipart" title="HTML response" target="_blank">HTML response</a>.
</li>
</ul>
</li>

<li style="margin-top:10px;">
<code>pub async fn employees_html2(...)</code>: accepting <code>GET</code> requests where data are in <code>request paths</code> and returning responses in HTML. See also:
<ul>
<li style="margin-top:10px;">
<a href="https://actix.rs/docs/extractors/#path" title="Request Path Extractor" target="_blank">Request Path Extractor</a>
</li>
<li style="margin-top:10px;">
Template processing <a href="#crate-tera">using crate Tera</a> section.
</li>
<li style="margin-top:10px;">
Return HTML.
</li>
</ul>
</li>
</ol>

We have not covered <a href="https://actix.rs/docs/extractors/#query" title="Query string requests" target="_blank">query string requests</a>, it's not much too different to others that we've covered above.

On the later two (2) HTML response methods, we could've written the final response as:

```rust
    HttpResponse::Ok()
        .body(render_employees_template(&query_result))    
```

Instead of:

```rust
    HttpResponse::Ok()
        .content_type("text/html; charset=utf-8")
        .body(render_employees_template(&query_result))
```

The <code>Content-Type</code> header <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type" title="Content-Type header" target="_blank">might get ignored</a>. I have it in just to remember how we can set it in case we need to.

Finally, the private worker <code>fn render_employees_template(...)</code> is just a copy version of examples from other articles in the section where <a href="#crate-tera">we discuss crate tera</a>.

<h4 style="color:teal;text-transform: none;">
  <a id="src-main">src/main.rs</a>
</h4>

We use the <a href="https://actix.rs/docs/application/#state" title="Application state" target="_blank">application state</a> to persist database connection across the application:

```rust
...
pub struct AppState {
    db: Pool<MySql>,
}
...
            .app_data(web::Data::new(AppState {
                db: pool.clone()
            }))
...			
```

This code is just about an exact copy of the code from the above official documentation 😂.

The CORS code's been discussed in section <a href="#crate-actix-cors">crate actix-cors</a>.

In <a href="#src-handlers">src/handlers.rs</a> module, the root route for all handler methods is <code>/employees</code>. We use <a href="https://actix.rs/docs/url-dispatch/#scoping-routes" title="route scoping" target="_blank">route scoping</a> to route methods which return JSON to <code>/data/employees</code>, and methods which return HTML to <code>/ui/employees</code>:

```rust
...
            .service(
                web::scope("/data")
                    .service(handlers::employees_json1)
                    .service(handlers::employees_json2),
            )
            .service(
                web::scope("/ui")
                    .service(handlers::employees_html1)
                    .service(handlers::employees_html2),
            )
...			
```

I'd like to be able to visually test this project across my home network, so I bind it to <code>0.0.0.0</code>. Port <code>5000</code> just happens to be the port that I allocate to test work in progress projects.

<h2 style="color:teal;text-transform: none;">
  <a id="some-visual-test-Runs">Some Visual Test Runs</a>
</h2>

For some reasons, <a href="https://www.postman.com/" title="Postman" target="_blank">Postman</a> reports <code>403 Forbidden</code> for some of the routes... While these routes are okay on browsers. I use <a href="https://testfully.io/" title="Testfully" target="_blank">Testfully</a> instead.

<code>192.168.0.16</code> is the address of my Ubuntu 22.10 machine, I run the tests from my Windows 10 Pro machine.

<p>
❶ <code>http://192.168.0.16:5000/data/employees</code>
</p>

{% include image-gallery.html list=page.gallery-image-list-1 %}

<p style="clear:both;">
❷ <code>http://192.168.0.16:5000/data/employees/%chi/%ak</code>
</p>

{% include image-gallery.html list=page.gallery-image-list-2 %}

<p style="clear:both;">
❸ <code>http://192.168.0.16:5000/ui/employees</code>
</p>

{% include image-gallery.html list=page.gallery-image-list-3 %}

<p style="clear:both;">
❹ <code>http://192.168.0.16:5000/ui/employees/%chi/%ak</code>
</p>

{% include image-gallery.html list=page.gallery-image-list-4 %}

<p style="clear:both;">
❺ <code>http://192.168.0.16:5000/ui/employees/%yễn/%Hai%</code>
</p>

{% include image-gallery.html list=page.gallery-image-list-5 %}

<h2 style="color:teal;text-transform: none;">
  <a id="concluding-remarks">Concluding Remarks</a>
</h2>

We've not written any test for any of the modules in this project. It's my intention to do so in the near future, but I'm not too certain if I can actually see it through. I've written tests before, for example, in the <a href="https://behainguyen.wordpress.com/2023/08/04/rust-baby-step-a-fibonacci-sequence-function/" title="first Rust post" target="_blank">first Rust post</a>, and some later ones.

We've covered some only very basic features crate <a href="https://actix.rs/docs/" title="actix-web" target="_blank">actix-web</a> has. It's worth studying the tutorials provided by the official documentation.

I hope you find this post useful. Thank you for reading and stay safe as always.

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
<a href="https://www.freepnglogos.com/uploads/logo-mysql-png/logo-mysql-mysql-logo-png-images-are-download-crazypng-21.png" target="_blank">https://www.freepnglogos.com/uploads/logo-mysql-png/logo-mysql-mysql-logo-png-images-are-download-crazypng-21.png</a>
</li>
<li>
<a href="https://actix.rs/img/logo.png" target="_blank">https://actix.rs/img/logo.png</a>
</li>
<li>
<a href="https://quintagroup.com/cms/python/images/jinja2.png/@@images/919c2c3d-5b4e-4650-943a-b0df263f851b.png" target="_blank">https://quintagroup.com/cms/python/images/jinja2.png/@@images/919c2c3d-5b4e-4650-943a-b0df263f851b.png</a>
</li>
</ul>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rust_web_01" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>
