---
layout: post
title: "Rust SQLx CLI: database migration with MySQL and PostgreSQL."

description: Database migration is the process of developing, and refactoring the application database as part of the application development process. SQLx CLI is Rust crate sqlx's associated command-line utility for managing this migration process. In this post, we're looking at how to use this CLI for both MySQL and PostgreSQL, on both Windows 10 and Ubuntu 22.10.

tags:
- Rust
- SQLx CLI 
- database 
- migration
- MySQL
- PostgreSQL
---

<em style="color:#111;">Database migration is the process of developing, and refactoring the application database as part of the application development process. <a href="https://github.com/launchbadge/sqlx/tree/main/sqlx-cli" title="SQLx CLI" target="_blank">SQLx CLI</a> is Rust crate <a href="https://docs.rs/sqlx/latest/sqlx" title="sqlx" target="_blank">sqlx</a>'s associated command-line utility for managing this migration process. In this post, we're looking at how to use this CLI for both MySQL and PostgreSQL, on both Windows 10 and Ubuntu 22.10.</em>

| ![086-feature-image.png](https://behainguyen.files.wordpress.com/2023/10/086-feature-image.png) |
|:--:|
| *Rust SQLx CLI: database migration with MySQL and PostgreSQL.* |

After trying <a href="https://github.com/launchbadge/sqlx/tree/main/sqlx-cli" title="SQLx CLI" target="_blank">SQLx CLI</a> out, I'd say that we could actually use this CLI as a generic tool for managing database development for applications written in languages other than Rust. I feel really fond of this CLI.

<!--------------------------------------------------------------------------------->

<h2>Table of contents</h2>

<ul>
    <li style="margin-top:10px;">
		<a href="#sqlx-cli-openssl">SQLx CLI Installation Requires OpenSSL</a>
	</li>
	
    <li style="margin-top:10px;">
        <a href="#sqlx-cli-installation">SQLx CLI Installation</a>
	</li>

	
    <li style="margin-top:10px;">
        <a href="#sqlx-cli-installation">Database Migration with SQLx CLI</a>
		
	    <ul>
            <li style="margin-top:10px;">
                <a href="#database-connection">Database Connection</a>
            </li>
			
            <li style="margin-top:10px;">
                <a href="#mysql-migration">MySQL Server</a>
            </li>			
			
            <li style="margin-top:10px;">
                <a href="#postgresql-migration">PostgreSQL Server</a>
            </li>						
	    </ul>
	</li>

	<!-- TO_DO: -->
    <li style="margin-top:10px;">
        Appendix: <a href="#win-10-openssl-installation-logs">Windows 10 OpenSSL Installation Logs</a>
	</li>

    <li style="margin-top:10px;">
        Appendix: <a href="#ubuntu-22-10-openssl-installation-logs">Ubuntu 22.10 OpenSSL Installation Logs</a>
	</li>

    <li style="margin-top:10px;">
        Appendix: <a href="#ubuntu-22-10-sqlx-cli-failure-installation-logs">Ubuntu 22.10 SQLx CLI Failure Installation Logs</a>
	</li>

    <li style="margin-top:10px;">
        Appendix: <a href="#ubuntu-22-10-sqlx-cli-success-installation-logs">Ubuntu 22.10 SQLx CLI Success Installation Logs</a>
	</li>
</ul>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="sqlx-cli-openssl">SQLx CLI Installation Requires OpenSSL</a>
</h3>

The <a href="https://github.com/launchbadge/sqlx/tree/main/sqlx-cli" title="SQLx CLI" target="_blank">SQLx CLI</a> documentation does not mention it, but it seems that it does require OpenSSL. I only find this one out after some failed attempt to install it.

Prior to installing <a href="https://github.com/launchbadge/sqlx/tree/main/sqlx-cli" title="SQLx CLI" target="_blank">SQLx CLI</a> on Windows 10, I had a problem with not having <code>OpenSSL</code> installed for some other Rust <a href="https://actix.rs/docs/">Actix Web</a> project.

This GitHub issue <a href="https://github.com/sfackler/rust-openssl/issues/1021" title="Ubuntu 18: failed to run custom build command for openssl-sys v0.9.39" target="_blank">Ubuntu 18: failed to run custom build command for openssl-sys v0.9.39</a>, <a href="https://github.com/sfackler/rust-openssl/issues/1021#issuecomment-1004042988" title="answer by riteshkumargiitian" target="_blank">answer by riteshkumargiitian</a> helps, to install, run:

```
C:\>choco install openssl
```

The installation directory is <code>C:\Program Files\OpenSSL-Win64</code>. For full detail logs, please see <a href="#win-10-openssl-installation-logs">Windows 10 OpenSSL Installation Logs</a>. 

The next step is to set environment variable <code>OPENSSL_DIR</code>. Note that there're no double quotes, (<code>""</code>) around the directory path:

```
C:\>set OPENSSL_DIR=C:\Program Files\OpenSSL-Win64
```

This is the state of my Windows 10 machine when I install <a href="https://github.com/launchbadge/sqlx/tree/main/sqlx-cli" title="SQLx CLI" target="_blank">SQLx CLI</a>. The installation just succeeds the first time.

On Ubuntu 22.10, the first installation attempt does not go through, it needs <code>OpenSSL</code>. For full detail logs, please see <a href="#ubuntu-22-10-sqlx-cli-failure-installation-logs">Ubuntu 22.10 SQLx CLI Failure Installation Logs</a>.

To install <code>OpenSSL</code>, run:

```
$ sudo apt install pkg-config
```

It should succeed. For full detail logs, please see <a href="#ubuntu-22-10-openssl-installation-logs">Ubuntu 22.10 OpenSSL Installation Logs</a>.

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="sqlx-cli-installation">SQLx CLI Installation</a>
</h3>

We install <a href="https://github.com/launchbadge/sqlx/tree/main/sqlx-cli" title="SQLx CLI" target="_blank">SQLx CLI</a> with <code>cargo</code>. I already have Rust installed on both OSes. It does not matter under which directory we run the installation command from.

On Windows 10:

```
C:\>cargo install sqlx-cli
```

On Ubuntu 22.10:

```
$ cargo install sqlx-cli
```

-- For the full Ubuntu 22.10 successful installation logs, please see <a href="#ubuntu-22-10-sqlx-cli-success-installation-logs">Ubuntu 22.10 SQLx CLI Success Installation Logs</a>.

Only after the installation, we get informed where the CLI executables are. The documentation does not mention it beforehand:

● On Windows 10: <code>C:\Users\behai\.cargo\bin\</code>. And <code>C:\Users\behai\.cargo</code> size on disk is about 1.32GB.

● On Ubuntu 22.10: <code>/home/behai/.cargo/bin/</code>. And <code>/home/behai/.cargo</code> is about 1.00GB.

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="sqlx-cli-installation">Database Migration with SQLx CLI</a>
</h3>

We'll look at both MySQL and PostgreSQL, illustrated examples are on Ubuntu 22.10. On Windows 10, commands are the same.

The MySQL server used is a Docker container discussed in <a href="https://behainguyen.wordpress.com/2023/09/22/docker-on-ubuntu-22-10-running-mysql8-0-34-debian-with-custom-config-socket-database-and-log-files-reside-on-host-machine/" title="Docker on Ubuntu 22.10: running mysql:8.0.34-debian with custom config, socket, database and log files reside on host machine." target="_blank">Docker on Ubuntu 22.10: running mysql:8.0.34-debian with custom config, socket, database and log files reside on host machine</a>.

The PostgreSQL server is also a Docker container, discussed in <a href="https://behainguyen.wordpress.com/2023/01/13/using-postgresql-official-docker-image-on-windows-10-and-ubuntu-22-10-kinetic/" title="Using PostgreSQL Official Docker image on Windows 10 and Ubuntu 22.10 kinetic." target="_blank">Using PostgreSQL Official Docker image on Windows 10 and Ubuntu 22.10 kinetic</a>.

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="database-connection">Database Connection</a>
</h4>

<a href="https://github.com/launchbadge/sqlx/tree/main/sqlx-cli#usage" title="SQLx CLI Usage" target="_blank">SQLx CLI Usage</a> discusses both <code>.env</code> file and command line option <code>--database-url</code>. We'll use the <code>.env</code>, later on, we could add more run time info to this file as required by the application. <strong>I think</strong> the <code>.env</code> file should sit in the same directory as the <code>Cargo.toml</code> file.

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="mysql-migration">MySQL Server</a>
</h4>

❶ We don't actually need an existing Rust project to start a database migration process. But I create one for this run. So I'll repeat it in this post.

While under <code>/home/behai/rust</code>, create a new project <code>sqlx-mysql-migration</code>, and change to the project directory:

```
$ cargo new sqlx-mysql-migration
$ cd sqlx-mysql-migration/
```

❷ Create the <code>.env</code> file.

```
Content of /home/behai/rust/sqlx-mysql-migration/.env:
```

```ini
DATABASE_URL=mysql://root:pcb.2176310315865259@localhost:3306/membership
```

We've seen the value of <code>DATABASE_URL</code> in other Rust code before, for example, <a href="https://behainguyen.wordpress.com/2023/09/12/rust-mysql-connect-execute-sql-statements-and-stored-procs-using-crate-sqlx/" title="Rust & MySQL: connect, execute SQL statements and stored procs using crate sqlx." target="_blank">Rust & MySQL: connect, execute SQL statements and stored procs using crate sqlx</a>, where it is <code>mysql://root:pcb.2176310315865259@localhost:3306/employees</code>. In this example, we're working with a <code>membership</code> database.

❸ Now that we have the <code>DATABASE_URL</code> ready, and of course the target MySQL server is running, we create the database with:

```
$ sqlx database create
```

If there was no problem, there would be no output. We should use MySQL Workbench to verify that the database has been created.

We can drop the database with:

```
$ sqlx database drop
```

It'll ask for confirmation. Again, we can use MySQL Workbench to verify that the database has been dropped.

<strong>Please note</strong>, from this point on, we need the database to exist.

❹ Create the first database script. The command takes the format:

```
$ sqlx migrate add -r <name>
```

For <code>&lt;name></code>, let's call it <code>init</code>. The command is then:

```
$ sqlx migrate add -r init
```

The output is:

```
Creating migrations/20231008021418_init.up.sql
Creating migrations/20231008021418_init.down.sql

Congratulations on creating your first migration!

Did you know you can embed your migrations in your application binary?
On startup, after creating your database connection or pool, add:

sqlx::migrate!().run(<&your_pool OR &mut your_connection>).await?;

Note that the compiler won't pick up new migrations if no Rust source files have changed.
You can create a Cargo build script to work around this with `sqlx migrate build-script`.

See: https://docs.rs/sqlx/0.5/sqlx/macro.migrate.html
```

A sub-directory named <code>migrations/</code> has been created, in it there're two (2) empty files <code>20231008021418_init.up.sql</code> and <code>20231008021418_init.down.sql</code>.

After we made some changes to the application database, we might want to revert these changes for some reason. The <code>20231008021418_init.up.sql</code> script file is where we write the SQL statements to update the database. The script file <code>20231008021418_init.down.sql</code> is where we write SQL statements to undo what <code>20231008021418_init.up.sql</code> does.

```
Content of migrations/20231008021418_init.up.sql:
```

```sql
-- 08/10/2023.

ALTER DATABASE `membership` DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `member`;
CREATE TABLE `member` (
  `id` int NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` varchar(100) NOT NULL,
  `birth_date` date NOT NULL,
  `first_name` varchar(32) NOT NULL,
  `last_name` varchar(32) NOT NULL,
  `gender` enum('M','F') NOT NULL,
  `joined_date` date NOT NULL,
  `created_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_unique` (`email`)
);
```

Basically, we alter some properties of <code>membership</code> database, then we create the first table: <code>member</code>.

```
Content of migrations/20231008021418_init.down.sql:
```

```sql
-- 08/10/2023.

DROP TABLE IF EXISTS `member`;
```

We undo what the <code>up</code> script does: we remove the <code>member</code> table from the database.

❺ Let's run the <code>init</code> migration. The command is:

```
$ sqlx migrate run
```

The output is brief:

```
Applied 20231008021418/migrate init (2.419887162s)
```

MySQL Workbench shows that the <code>member</code> table has been created, and there's also an additional table <code>_sqlx_migrations</code> -- and there's one (1) row in it, this row should be self-explanatory.

Let's just undo that. The command is:

```
$ sqlx migrate revert
```

The output is:

```
Applied 20231008021418/revert init (810.615999ms)
```

Verify that the <code>member</code> table has been removed, and the table <code>_sqlx_migrations</code> is empty?

❻ Let's create another database update script, we name it <code>stage1</code>:

```
$ sqlx migrate add -r stage1
```

```
Content of migrations/20231008081406_stage1.up.sql:
```

```sql
-- 08/10/2023.

DROP TABLE IF EXISTS `duration`;
CREATE TABLE `duration` (
  `id` smallint NOT NULL,
  `months` smallint NOT NULL,
  `expiry_date` date NULL,
  PRIMARY KEY (`id`)
) comment='Membership duration in months.';

insert into duration ( id, months )
values
    ( 1, 6 ),
    ( 2, 12 ),
    ( 3, 18 ),
    ( 4, 24 );
]
```

```
Content of migrations/20231008081406_stage1.down.sql:
```

```sql
-- 08/10/2023.

DROP TABLE IF EXISTS `duration`;
```

Apply <code>stage1</code> with command:

```
$ sqlx migrate run
```

Assuming that <code>init</code> has been applied. The output is:

```
Applied 20231008081406/migrate stage1 (1.742237765s)
```

Table <code>_sqlx_migrations</code> should now contain two (2) entries. Table <code>duration</code> should also have been created.

❼ Let's undo:

```
$ sqlx migrate revert
```

Output:

```
Applied 20231008081406/revert stage1 (488.29367ms)
```

Let's do another undo:

```
$ sqlx migrate revert
```

Output:

```
Applied 20231008021418/revert init (445.333376ms)
```

We can see that the last update gets undo first. Also, the <code>membership</code> database is now an empty database. And table <code>_sqlx_migrations</code> has no entry.

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="postgresql-migration">PostgreSQL Server</a>
</h4>

The process for PostgreSQL databases is identical to MySQL databases.

❶ Create a new directory for this migration. 

While under <code>/home/behai/rust</code>, create a new sub-directory <code>sqlx-postgresql-migration</code>, and move to this new sub-directory:

```
$ mkdir sqlx-postgresql-migration
$ cd sqlx-postgresql-migration
```

❷ The <code>.env</code> file.

```
Content of /home/behai/rust/sqlx-postgresql-migration/.env:
```

```ini
DATABASE_URL=postgresql://postgres:pcb.2176310315865259@localhost:5432/membership?schema=public
```

💥 <span style="font-weight:bold;color:blue;">Please note:</span> the parameter <code>schema=public</code> might cause the error:

<span style="font-weight:bold;color:red;"><code>
ERROR: no schema has been selected to create in
</code></span>

In the PostgreSQL server config file <code>postgresql.conf</code>, ensure that the <code>search_path</code> entry value has <code>public</code>. For example:

```ini
search_path = 'ompdev1, "$user", public'	# schema names
```

❸ Database creation and removal commands are the same, respectively as:

```
$ sqlx database create
$ sqlx database drop
```

We can use a client tool such as pgAdmin 4 to verify that the <code>membership</code> database has been created on the target server.

<strong>Please note</strong>, from this point on, we need the database to exist.

❹ Create the first <code>init</code> database script:

```
$ sqlx migrate add -r init
```

```
Content of migrations/20231008104430_init.up.sql
```

```sql
-- 08/10/2023.

DROP TYPE IF EXISTS genders;

CREATE TYPE genders AS ENUM ('M', 'F');

DROP TABLE IF EXISTS "member";

CREATE TABLE "member" (
  id integer NOT NULL PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password varchar(100) NOT NULL,
  birth_date date NOT NULL,
  first_name varchar(32) NOT NULL,
  last_name varchar(32) NOT NULL,
  gender genders NOT NULL,
  joined_date date NOT NULL,
  created_date timestamp with time zone NOT NULL
);

CREATE INDEX member_email_idx ON member (email);
```

```
Content of migrations/20231008104430_init.down.sql
```

```sql
-- 08/10/2023.

DROP TABLE IF EXISTS "member";
DROP TYPE IF EXISTS genders;
```

❺ Let's also create the second database script <code>stage1</code>:

```
$ sqlx migrate add -r stage1
```

```
Content of migrations/20231008111030_stage1.up.sql
```

```sql
-- 08/10/2023.

DROP TABLE IF EXISTS "duration";
CREATE TABLE "duration" (
  id smallint NOT NULL PRIMARY KEY,
  months smallint NOT NULL,
  expiry_date date NULL
);

COMMENT ON TABLE duration IS 'Membership duration in months.';

insert into duration ( id, months )
values
    ( 1, 6 ),
    ( 2, 12 ),
    ( 3, 18 ),
    ( 4, 24 );
```

```
Content of migrations/20231008111030_stage1.down.sql
```

```sql
-- 08/10/2023.

DROP TABLE IF EXISTS "duration";
```

❻ Commands to apply and to undo are as discussed before:

```
$ sqlx migrate run
$ sqlx migrate revert
```

If we now apply the migration scripts, the output is:

```
Applied 20231008104430/migrate init (121.005913ms)
Applied 20231008111030/migrate stage1 (55.043293ms)
```

And tables, including <code>_sqlx_migrations</code>, are created under schema <code>public</code> as shown in the screenshot below:

![086-01.png](https://behainguyen.files.wordpress.com/2023/10/086-01.png)

So barring database specific syntax differences, the process is identical for MySQL and PostgreSQL.

Thank you for reading, and I do hope you find this post useful. Stay safe as always.

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
<a href="https://icon-icons.com/download/170836/PNG/512/" target="_blank">https://icon-icons.com/download/170836/PNG/512/</a>
</li>
</ul>

✿✿✿

<h3><a id="win-10-openssl-installation-logs">Windows 10 OpenSSL Installation Logs</a></h3>

```
C:\>choco install openssl
Chocolatey v1.2.0
Installing the following packages:
openssl
By installing, you accept licenses for the packages.

openssl v3.1.1 [Approved]
openssl package files install completed. Performing other installation steps.
The package openssl wants to run 'chocolateyinstall.ps1'.
Note: If you don't run this script, the installation will fail.
Note: To confirm automatically next time, use '-y' or consider:
choco feature enable -n allowGlobalConfirmation
Do you want to run the script?([Y]es/[A]ll - yes to all/[N]o/[P]rint): Y

Installing 64-bit openssl...
openssl has been installed.
WARNING: No registry key found based on  'OpenSSL-Win'
PATH environment variable does not have C:\Program Files\OpenSSL-Win64\bin in it. Adding...
WARNING: OPENSSL_CONF has been set to C:\Program Files\OpenSSL-Win64\bin\openssl.cfg
  openssl can be automatically uninstalled.
Environment Vars (like PATH) have changed. Close/reopen your shell to
 see the changes (or in powershell/cmd.exe just type `refreshenv`).
 The install of openssl was successful.
  Software installed to 'C:\Program Files\OpenSSL-Win64\'

Chocolatey installed 1/1 packages.
 See the log for details (C:\ProgramData\chocolatey\logs\chocolatey.log).
```

<!--------------------------------------------------------------------------------->

<h3><a id="ubuntu-22-10-openssl-installation-logs">Ubuntu 22.10 OpenSSL Installation Logs</a></h3>

```
behai@hp-pavilion-15:~$ pwd
```

It is:

```
/home/behai
```

Full installation log:

```
behai@hp-pavilion-15:~$ sudo apt install pkg-config
[sudo] password for behai:
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following NEW packages will be installed:
  pkg-config
0 to upgrade, 1 to newly install, 0 to remove and 1 not to upgrade.
Need to get 48.2 kB of archives.
After this operation, 134 kB of additional disk space will be used.
Get:1 http://au.archive.ubuntu.com/ubuntu kinetic/main amd64 pkg-config amd64 0.29.2-1ubuntu3 [48.2 kB]
Fetched 48.2 kB in 0s (697 kB/s)
Selecting previously unselected package pkg-config.
(Reading database ... 237915 files and directories currently installed.)
Preparing to unpack .../pkg-config_0.29.2-1ubuntu3_amd64.deb ...
Unpacking pkg-config (0.29.2-1ubuntu3) ...
Setting up pkg-config (0.29.2-1ubuntu3) ...
Processing triggers for man-db (2.10.2-2) ...
behai@hp-pavilion-15:~$
```

<!--------------------------------------------------------------------------------->

<h3><a id="ubuntu-22-10-sqlx-cli-failure-installation-logs">Ubuntu 22.10 SQLx CLI Failure Installation Logs</a></h3>

```
behai@hp-pavilion-15:~/rust/sqlx-mysql-migration$ cargo install sqlx-cli
    Updating crates.io index
  Downloaded sqlx-cli v0.7.2
  Downloaded 1 crate (94.4 KB) in 0.73s
  Installing sqlx-cli v0.7.2
    Updating crates.io index
  Downloaded openssl-macros v0.1.1
  Downloaded fd-lock v3.0.13
  Downloaded native-tls v0.2.11
  Downloaded byteorder v1.5.0
  Downloaded md-5 v0.10.6
  Downloaded openssl-probe v0.1.5
  Downloaded endian-type v0.1.2
  Downloaded nibble_vec v0.1.0
  Downloaded errno v0.3.4
  Downloaded tokio-macros v2.1.0
  Downloaded sqlx-macros v0.7.2
  Downloaded anstyle v1.0.4
  Downloaded memchr v2.6.4
  Downloaded unicode-width v0.1.11
  Downloaded futures-macro v0.3.28
  Downloaded cargo_metadata v0.14.2
  Downloaded cargo-platform v0.1.4
  Downloaded anstyle-parse v0.2.2
  Downloaded semver v1.0.19
  Downloaded sha1 v0.10.6
  Downloaded num_cpus v1.16.0
  Downloaded fastrand v2.0.1
  Downloaded promptly v0.3.1
  Downloaded anstream v0.6.4
  Downloaded thiserror v1.0.49
  Downloaded sqlx-macros-core v0.7.2
  Downloaded backoff v0.4.0
  Downloaded libm v0.2.8
  Downloaded thiserror-impl v1.0.49
  Downloaded sha2 v0.10.8
  Downloaded tokio-stream v0.1.14
  Downloaded futures v0.3.28
  Downloaded clap_complete v4.4.3
  Downloaded num-traits v0.2.17
  Downloaded unicode-ident v1.0.12
  Downloaded sqlx-mysql v0.7.2
  Downloaded clap v4.4.6
  Downloaded typenum v1.17.0
  Downloaded socket2 v0.5.4
  Downloaded indexmap v2.0.2
  Downloaded sqlx-sqlite v0.7.2
  Downloaded openssl-sys v0.9.93
  Downloaded flume v0.11.0
  Downloaded sqlx-postgres v0.7.2
  Downloaded rustyline v9.1.2
  Downloaded sqlx-core v0.7.2
  Downloaded hashbrown v0.14.1
  Downloaded sqlx v0.7.2
  Downloaded clap_builder v4.4.6
  Downloaded chrono v0.4.31
  Downloaded radix_trie v0.2.1
  Downloaded nix v0.23.2
  Downloaded openssl v0.10.57
  Downloaded rustix v0.38.17
  Downloaded proc-macro2 v1.0.68
  Downloaded smallvec v1.11.1
  Downloaded syn v2.0.38
  Downloaded libc v0.2.149
  Downloaded tokio v1.32.0
  Downloaded linux-raw-sys v0.4.8
  Downloaded 60 crates (6.6 MB) in 2.06s (largest was `linux-raw-sys` at 1.4 MB)
   Compiling proc-macro2 v1.0.68
   Compiling unicode-ident v1.0.12
   Compiling libc v0.2.149
   Compiling autocfg v1.1.0
   Compiling cfg-if v1.0.0
   Compiling version_check v0.9.4
   Compiling serde v1.0.188
   Compiling quote v1.0.33
   Compiling typenum v1.17.0
   Compiling syn v2.0.38
   Compiling generic-array v0.14.7
   Compiling const-oid v0.9.5
   Compiling getrandom v0.2.10
   Compiling cc v1.0.83
   Compiling pkg-config v0.3.27
   Compiling vcpkg v0.2.15
   Compiling futures-core v0.3.28
   Compiling libm v0.2.8
   Compiling smallvec v1.11.1
   Compiling crypto-common v0.1.6
   Compiling block-buffer v0.10.4
   Compiling num-traits v0.2.17
   Compiling once_cell v1.18.0
   Compiling subtle v2.5.0
   Compiling digest v0.10.7
   Compiling memchr v2.6.4
   Compiling pin-project-lite v0.2.13
   Compiling serde_derive v1.0.188
   Compiling openssl-sys v0.9.93
   Compiling lock_api v0.4.10
   Compiling ahash v0.8.3
   Compiling slab v0.4.9
   Compiling tinyvec_macros v0.1.1
   Compiling futures-sink v0.3.28
   Compiling scopeguard v1.2.0
error: failed to run custom build command for `openssl-sys v0.9.93`

Caused by:
  process didn't exit successfully: `/tmp/cargo-installCJHaz3/release/build/openssl-sys-9774aa6210709b08/build-script-main` (exit status: 101)
  --- stdout
  cargo:rerun-if-env-changed=X86_64_UNKNOWN_LINUX_GNU_OPENSSL_LIB_DIR
  X86_64_UNKNOWN_LINUX_GNU_OPENSSL_LIB_DIR unset
  cargo:rerun-if-env-changed=OPENSSL_LIB_DIR
  OPENSSL_LIB_DIR unset
  cargo:rerun-if-env-changed=X86_64_UNKNOWN_LINUX_GNU_OPENSSL_INCLUDE_DIR
  X86_64_UNKNOWN_LINUX_GNU_OPENSSL_INCLUDE_DIR unset
  cargo:rerun-if-env-changed=OPENSSL_INCLUDE_DIR
  OPENSSL_INCLUDE_DIR unset
  cargo:rerun-if-env-changed=X86_64_UNKNOWN_LINUX_GNU_OPENSSL_DIR
  X86_64_UNKNOWN_LINUX_GNU_OPENSSL_DIR unset
  cargo:rerun-if-env-changed=OPENSSL_DIR
  OPENSSL_DIR unset
  cargo:rerun-if-env-changed=OPENSSL_NO_PKG_CONFIG
  cargo:rerun-if-env-changed=PKG_CONFIG_x86_64-unknown-linux-gnu
  cargo:rerun-if-env-changed=PKG_CONFIG_x86_64_unknown_linux_gnu
  cargo:rerun-if-env-changed=HOST_PKG_CONFIG
  cargo:rerun-if-env-changed=PKG_CONFIG
  cargo:rerun-if-env-changed=OPENSSL_STATIC
  cargo:rerun-if-env-changed=OPENSSL_DYNAMIC
  cargo:rerun-if-env-changed=PKG_CONFIG_ALL_STATIC
  cargo:rerun-if-env-changed=PKG_CONFIG_ALL_DYNAMIC
  cargo:rerun-if-env-changed=PKG_CONFIG_PATH_x86_64-unknown-linux-gnu
  cargo:rerun-if-env-changed=PKG_CONFIG_PATH_x86_64_unknown_linux_gnu
  cargo:rerun-if-env-changed=HOST_PKG_CONFIG_PATH
  cargo:rerun-if-env-changed=PKG_CONFIG_PATH
  cargo:rerun-if-env-changed=PKG_CONFIG_LIBDIR_x86_64-unknown-linux-gnu
  cargo:rerun-if-env-changed=PKG_CONFIG_LIBDIR_x86_64_unknown_linux_gnu
  cargo:rerun-if-env-changed=HOST_PKG_CONFIG_LIBDIR
  cargo:rerun-if-env-changed=PKG_CONFIG_LIBDIR
  cargo:rerun-if-env-changed=PKG_CONFIG_SYSROOT_DIR_x86_64-unknown-linux-gnu
  cargo:rerun-if-env-changed=PKG_CONFIG_SYSROOT_DIR_x86_64_unknown_linux_gnu
  cargo:rerun-if-env-changed=HOST_PKG_CONFIG_SYSROOT_DIR
  cargo:rerun-if-env-changed=PKG_CONFIG_SYSROOT_DIR
  cargo:rerun-if-env-changed=OPENSSL_STATIC
  cargo:rerun-if-env-changed=OPENSSL_DYNAMIC
  cargo:rerun-if-env-changed=PKG_CONFIG_ALL_STATIC
  cargo:rerun-if-env-changed=PKG_CONFIG_ALL_DYNAMIC
  cargo:rerun-if-env-changed=PKG_CONFIG_PATH_x86_64-unknown-linux-gnu
  cargo:rerun-if-env-changed=PKG_CONFIG_PATH_x86_64_unknown_linux_gnu
  cargo:rerun-if-env-changed=HOST_PKG_CONFIG_PATH
  cargo:rerun-if-env-changed=PKG_CONFIG_PATH
  cargo:rerun-if-env-changed=PKG_CONFIG_LIBDIR_x86_64-unknown-linux-gnu
  cargo:rerun-if-env-changed=PKG_CONFIG_LIBDIR_x86_64_unknown_linux_gnu
  cargo:rerun-if-env-changed=HOST_PKG_CONFIG_LIBDIR
  cargo:rerun-if-env-changed=PKG_CONFIG_LIBDIR
  cargo:rerun-if-env-changed=PKG_CONFIG_SYSROOT_DIR_x86_64-unknown-linux-gnu
  cargo:rerun-if-env-changed=PKG_CONFIG_SYSROOT_DIR_x86_64_unknown_linux_gnu
  cargo:rerun-if-env-changed=HOST_PKG_CONFIG_SYSROOT_DIR
  cargo:rerun-if-env-changed=PKG_CONFIG_SYSROOT_DIR
  run pkg_config fail: Could not run `PKG_CONFIG_ALLOW_SYSTEM_CFLAGS="1" "pkg-config" "--libs" "--cflags" "openssl"`
  The pkg-config command could not be found.

  Most likely, you need to install a pkg-config package for your OS.
  Try `apt install pkg-config`, or `yum install pkg-config`,
  or `pkg install pkg-config`, or `apk add pkgconfig` depending on your distribution.

  If you've already installed it, ensure the pkg-config command is one of the
  directories in the PATH environment variable.

  If you did not expect this build to link to a pre-installed system library,
  then check documentation of the openssl-sys crate for an option to
  build the library from source, or disable features or dependencies
  that require pkg-config.

  --- stderr
  thread 'main' panicked at '

  Could not find directory of OpenSSL installation, and this `-sys` crate cannot
  proceed without this knowledge. If OpenSSL is installed and this crate had
  trouble finding it,  you can set the `OPENSSL_DIR` environment variable for the
  compilation process.

  Make sure you also have the development packages of openssl installed.
  For example, `libssl-dev` on Ubuntu or `openssl-devel` on Fedora.

  If you're in a situation where you think the directory *should* be found
  automatically, please open a bug at https://github.com/sfackler/rust-openssl
  and include information about your system as well as this message.

  $HOST = x86_64-unknown-linux-gnu
  $TARGET = x86_64-unknown-linux-gnu
  openssl-sys = 0.9.93


  It looks like you're compiling on Linux and also targeting Linux. Currently this
  requires the `pkg-config` utility to find OpenSSL but unfortunately `pkg-config`
  could not be found. If you have OpenSSL installed you can likely fix this by
  installing `pkg-config`.

  ', /home/behai/.cargo/registry/src/index.crates.io-6f17d22bba15001f/openssl-sys-0.9.93/build/find_normal.rs:190:5
  note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
warning: build failed, waiting for other jobs to finish...
error: failed to compile `sqlx-cli v0.7.2`, intermediate artifacts can be found at `/tmp/cargo-installCJHaz3`
behai@hp-pavilion-15:~/rust/sqlx-mysql-migration$
```

<!--------------------------------------------------------------------------------->

<h3><a id="ubuntu-22-10-sqlx-cli-success-installation-logs">Ubuntu 22.10 SQLx CLI Success Installation Logs</a></h3>

```
behai@hp-pavilion-15:~/rust/sqlx-mysql-migration$ cargo install sqlx-cli
    Updating crates.io index
  Installing sqlx-cli v0.7.2
    Updating crates.io index
   Compiling proc-macro2 v1.0.68
   Compiling unicode-ident v1.0.12
   Compiling libc v0.2.149
   Compiling autocfg v1.1.0
   Compiling cfg-if v1.0.0
   Compiling version_check v0.9.4
   Compiling serde v1.0.188
   Compiling typenum v1.17.0
   Compiling quote v1.0.33
   Compiling syn v2.0.38
   Compiling generic-array v0.14.7
   Compiling const-oid v0.9.5
   Compiling getrandom v0.2.10
   Compiling cc v1.0.83
   Compiling futures-core v0.3.28
   Compiling vcpkg v0.2.15
   Compiling pkg-config v0.3.27
   Compiling libm v0.2.8
   Compiling smallvec v1.11.1
   Compiling crypto-common v0.1.6
   Compiling block-buffer v0.10.4
   Compiling num-traits v0.2.17
   Compiling subtle v2.5.0
   Compiling once_cell v1.18.0
   Compiling digest v0.10.7
   Compiling pin-project-lite v0.2.13
   Compiling memchr v2.6.4
   Compiling openssl-sys v0.9.93
   Compiling lock_api v0.4.10
   Compiling ahash v0.8.3
   Compiling slab v0.4.9
   Compiling futures-task v0.3.28
   Compiling tinyvec_macros v0.1.1
   Compiling scopeguard v1.2.0
   Compiling futures-channel v0.3.28
   Compiling futures-sink v0.3.28
   Compiling serde_derive v1.0.188
   Compiling tinyvec v1.6.0
   Compiling rand_core v0.6.4
   Compiling log v0.4.20
   Compiling futures-util v0.3.28
   Compiling parking_lot_core v0.9.8
   Compiling unicode-normalization v0.1.22
   Compiling futures-macro v0.3.28
   Compiling tokio-macros v2.1.0
   Compiling mio v0.8.8
   Compiling num_cpus v1.16.0
   Compiling socket2 v0.5.4
   Compiling foreign-types-shared v0.1.1
   Compiling unicode-bidi v0.3.13
   Compiling serde_json v1.0.107
   Compiling bytes v1.5.0
   Compiling allocator-api2 v0.2.16
   Compiling base64ct v1.6.0
   Compiling zeroize v1.6.0
   Compiling pin-utils v0.1.0
   Compiling openssl v0.10.57
   Compiling ppv-lite86 v0.2.17
   Compiling futures-io v0.3.28
   Compiling crossbeam-utils v0.8.16
   Compiling rand_chacha v0.3.1
   Compiling pem-rfc7468 v0.7.0
   Compiling hashbrown v0.14.1
   Compiling tokio v1.32.0
   Compiling bitflags v2.4.0
   Compiling either v1.9.0
   Compiling foreign-types v0.3.2
   Compiling openssl-macros v0.1.1
   Compiling num-integer v0.1.45
   Compiling utf8parse v0.2.1
   Compiling ryu v1.0.15
   Compiling byteorder v1.5.0
   Compiling crossbeam-queue v0.3.8
   Compiling minimal-lexical v0.2.1
   Compiling itoa v1.0.9
   Compiling paste v1.0.14
   Compiling cpufeatures v0.2.9
   Compiling native-tls v0.2.11
   Compiling thiserror v1.0.49
   Compiling percent-encoding v2.3.0
   Compiling form_urlencoded v1.2.0
   Compiling nom v7.1.3
   Compiling parking_lot v0.12.1
   Compiling itertools v0.11.0
   Compiling der v0.7.8
   Compiling rand v0.8.5
   Compiling idna v0.4.0
   Compiling tracing-attributes v0.1.26
   Compiling thiserror-impl v1.0.49
   Compiling tracing-core v0.1.31
   Compiling num-iter v0.1.43
   Compiling spin v0.5.2
   Compiling unicode_categories v0.1.1
   Compiling equivalent v1.0.1
   Compiling openssl-probe v0.1.5
   Compiling crc-catalog v2.2.0
   Compiling crc v3.0.1
   Compiling sqlformat v0.2.2
   Compiling tracing v0.1.37
   Compiling indexmap v2.0.2
   Compiling lazy_static v1.4.0
   Compiling url v2.4.1
   Compiling spki v0.7.2
   Compiling futures-intrusive v0.5.0
   Compiling tokio-stream v0.1.14
   Compiling sha2 v0.10.8
   Compiling hashlink v0.8.4
   Compiling atoi v2.0.0
   Compiling memoffset v0.6.5
   Compiling num-bigint-dig v0.8.4
   Compiling event-listener v2.5.3
   Compiling dotenvy v0.15.7
   Compiling rustix v0.38.17
   Compiling hex v0.4.3
   Compiling pkcs8 v0.10.2
   Compiling sqlx-core v0.7.2
   Compiling anstyle-parse v0.2.2
   Compiling hmac v0.12.1
   Compiling libsqlite3-sys v0.26.0
   Compiling colorchoice v1.0.0
   Compiling anstyle v1.0.4
   Compiling linux-raw-sys v0.4.8
   Compiling finl_unicode v1.2.0
   Compiling anstyle-query v1.0.0
   Compiling anstream v0.6.4
   Compiling stringprep v0.1.4
   Compiling hkdf v0.12.3
   Compiling pkcs1 v0.7.5
   Compiling sha1 v0.10.6
   Compiling futures-executor v0.3.28
   Compiling signature v2.1.0
   Compiling spin v0.9.8
   Compiling md-5 v0.10.6
   Compiling nibble_vec v0.1.0
   Compiling dirs-sys-next v0.1.2
   Compiling base64 v0.21.4
   Compiling unicode-width v0.1.11
   Compiling camino v1.1.6
   Compiling clap_lex v0.5.1
   Compiling bitflags v1.3.2
   Compiling strsim v0.10.0
   Compiling semver v1.0.19
   Compiling endian-type v0.1.2
   Compiling whoami v1.4.1
   Compiling heck v0.4.1
   Compiling radix_trie v0.2.1
   Compiling clap_derive v4.4.2
   Compiling clap_builder v4.4.6
   Compiling nix v0.23.2
   Compiling dirs-next v2.0.0
   Compiling flume v0.11.0
   Compiling rsa v0.9.2
   Compiling fd-lock v3.0.13
   Compiling async-trait v0.1.73
   Compiling unicode-segmentation v1.10.1
   Compiling home v0.5.5
   Compiling anyhow v1.0.75
   Compiling sqlx-postgres v0.7.2
   Compiling rustyline v9.1.2
   Compiling sqlx-mysql v0.7.2
   Compiling clap v4.4.6
   Compiling cargo-platform v0.1.4
   Compiling instant v0.1.12
   Compiling iana-time-zone v0.1.57
   Compiling chrono v0.4.31
   Compiling backoff v0.4.0
   Compiling cargo_metadata v0.14.2
   Compiling clap_complete v4.4.3
   Compiling promptly v0.3.1
   Compiling console v0.15.7
   Compiling futures v0.3.28
   Compiling filetime v0.2.22
   Compiling glob v0.3.1
   Compiling sqlx-sqlite v0.7.2
   Compiling sqlx v0.7.2
   Compiling sqlx-cli v0.7.2
    Finished release [optimized] target(s) in 3m 19s
  Installing /home/behai/.cargo/bin/cargo-sqlx
  Installing /home/behai/.cargo/bin/sqlx
   Installed package `sqlx-cli v0.7.2` (executables `cargo-sqlx`, `sqlx`)
behai@hp-pavilion-15:~/rust/sqlx-mysql-migration$
```
