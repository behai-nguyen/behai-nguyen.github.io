---
layout: post
title: "Using the Redis Official Docker Image on Windows 10 and Ubuntu 22.10 kinetic."

description: The Redis Docker Official Image includes both the Redis server and the Redis CLI. We discuss the setup process to use both on Windows 10 Pro and Ubuntu 22.10 kinetic. The actual Redis database file resides in a directory of our own designation on the host machine. We test the setup using the container CLI, as well as a very simple Rust program and a simple Python script.

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list:
    - "https://behainguyen.files.wordpress.com/2023/12/092-04.png"
    - "https://behainguyen.files.wordpress.com/2023/12/092-05.png"

tags:
- Docker
- Redis
- Rust
- Python
---

<em>The <a href="https://hub.docker.com/_/redis" title="Redis Docker Official Image" target="_blank">Redis Docker Official Image</a> includes both the <a href="https://redis.io/" title="Redis server" target="_blank">Redis server</a> and the <a href="https://redis.io/docs/connect/cli/" title="Redis CLI" target="_blank">Redis CLI</a>. We discuss the setup process to use both on Windows 10 Pro and Ubuntu 22.10 kinetic. The actual Redis database file resides in a directory of our own designation on the host machine. We test the setup using the container CLI, as well as a very simple Rust program and a simple Python script.</em>

| ![092-feature-image.png](https://behainguyen.files.wordpress.com/2023/12/092-feature-image.png) |
|:--:|
| *Using the Redis Official Docker Image on Windows 10 and Ubuntu 22.10 kinetic.* |

<h2>Table of contents</h2>

<ul>
    <li style="margin-top:10px;">
		<a href="#read-in-5-steps">Get It Ready in 5 (Five) Steps</a>
	</li>

    <li style="margin-top:10px;">
        <a href="#pulling-storing-loading-img">After Pulling, Storing and Loading the Image Locally</a>
	</li>
	
    <li style="margin-top:10px;">
        <a href="#running-redis-cli">Running the Redis CLI</a>
	</li>
	
    <li style="margin-top:10px;">
        <a href="#test-code">Rust and Python test code</a>
		
	    <ul>
            <li style="margin-top:10px;">
                <a href="#rust-test-code">Rust test code</a>
            </li>			
            <li style="margin-top:10px;">
                <a href="#Python-test-code">Python test code</a>
            </li>						
	    </ul>
	</li>
	
    <li style="margin-top:10px;">
        <a href="#custom-config-remote-connection">Unable to Apply Custom Config: no Remote Connection</a>
	</li>

    <li style="margin-top:10px;">
        <a href="#my-other-docker-posts">Other Docker Posts Which I've Written</a>
	</li>
</ul>

<h3 style="color:teal;">
  <a id="read-in-5-steps">Get It Ready in 5 (Five) Steps</a>
</h3>

❶ Pull the latest <a href="https://hub.docker.com/_/redis" title="Redis Docker Official Image" target="_blank">Redis Docker Official Image</a>.

```
▶️Windows 10: docker pull redis
▶️Ubuntu 22.10: $ sudo docker pull redis
```

❷ Create a bridge network to enable running <a href="https://redis.io/docs/connect/cli/" title="Redis CLI" target="_blank">Redis CLI</a>.

```
▶️Windows 10: docker network create -d bridge redis-network
▶️Ubuntu 22.10: $ sudo docker network create -d bridge redis-network
```

❸ Prepare database directory, i.e. data volume.

On Windows 10, the database directory is <code>D:\Database\Redis</code>, which translates to <code>//d/database/redis</code> for volume mounting. On Ubuntu 22.10, the database directory is <code>/home/behai/Public/database/redis</code>.

The data volume mountings are then:

```
▶️Windows 10: --mount type=bind,source=//d/database/redis,target=/data
▶️Ubuntu 22.10: --mount type=bind,source=/home/behai/Public/database/redis,target=/data
```

❹ 🚀 The final command is:

```
▶️Windows 10: docker run --publish=6379:6379 --network redis-network -d -it --mount type=bind,source=//d/database/redis,target=/data --name redis-docker redis
▶️Ubuntu 22.10: $ sudo docker run --publish=6379:6379 --network redis-network -d -it --mount type=bind,source=/home/behai/Public/database/redis,target=/data --name redis-docker redis 
```

❺ Verify the container is running.

```
▶️Windows 10: docker logs redis-docker
▶️Ubuntu 22.10: $ sudo docker logs redis-docker
```

The output should look like:

![092-01.png](https://behainguyen.files.wordpress.com/2023/12/092-01.png)

The following warning line <strong>should not</strong> be in the above output:

```
# Warning: Could not create server TCP listening socket ::1:16379: bind: Cannot assign requested address
```

The Redis container should now be ready. We can now talk to the Redis server <a href="#running-redis-cli">using Redis CLI</a>. And also programmatically via <a href="#rust-test-code">Rust</a> and <a href="#Python-test-code">Python</a>.

<h3 style="color:teal;">
  <a id="pulling-storing-loading-img">After Pulling, Storing and Loading the Image Locally</a>
</h3>

After pulling any image, we can save it locally and later load it from another machine etc., which helps saving some bandwidth data 😂...

I pull the Redis image on my Windows 10 machine using the command:

```
F:\>docker pull redis
```

We can then verify it's been pulled successfully, and also to find out the image <code>TAG</code> label, with:

```
F:\>docker images
```

We should find it in the output list:

```
REPOSITORY          TAG                       IMAGE ID       CREATED         SIZE
redis               latest                    e40e2763392d   2 weeks ago     138MB
...
```

We can then save it locally:

```
F:\>docker save redis:latest --output E:\docker-images\redis-7-2-3-latest.tar
```

I copy <code>redis-7-2-3-latest.tar</code> to Ubuntu 22.10's <code>Public/</code> directory, and load it up with the command:

```
$ sudo docker load --input Public/redis-7-2-3-latest.tar
```

<h3 style="color:teal;">
  <a id="running-redis-cli">Running the Redis CLI</a>
</h3>

There're two (2) ways to run the <a href="https://redis.io/docs/connect/cli/" title="Redis CLI" target="_blank">Redis CLI</a>: Bash mode interactive and directly via the container.

<a id="running-redis-cli-bash"></a>
❶ Bash mode interactive.

Given that the Redis container discussed above is running, get into the container Bash mode interactive with the command: 

```
▶️Windows 10: docker exec -it redis-docker bash
▶️Ubuntu 22.10: $ sudo docker exec -it redis-docker bash
```

The prompt changes to something like the following <code>root@b764904a70a6:/data#</code>. Now run <code>redis-cli</code>:

```
root@b764904a70a6:/data# redis-cli
```

The prompt changes to <code>127.0.0.1:6379></code>. 🚀 Run the <code>ping</code> command, we should get the <code>PONG</code> response. 

Now try setting some data and retrieving it using the following two (2) commands:

```
127.0.0.1:6379> SET mykey "Hello\nWorld"
127.0.0.1:6379> GET mykey
```

To quit, use the <code>exit</code> command until we get returned to the console.

<a id="running-redis-cli-container"></a>
❷ Directly via the container. 

```
▶️Windows 10: docker run -it --network redis-network --rm redis redis-cli -h redis-docker
▶️Ubuntu 22.10: $ sudo docker run -it --network redis-network --rm redis redis-cli -h redis-docker
```

💥 Note the <code>--network redis-network</code> parameter, without it, we won't be able to run the CLI via the container.

The prompt changes to <code>127.0.0.1:6379></code>, we can now repeat the above command sequence.

The screenshot below shows the running and the output of the processes just discussed:

![092-02.png](https://behainguyen.files.wordpress.com/2023/12/092-02.png)

We can now stop the container with:

```
▶️Windows 10: docker stop redis-docker
▶️Ubuntu 22.10: $ sudo docker stop redis-docker
```

The in-memory data'll be written to <code>dump.rdb</code> in the database directory specified above. We can view it as text. The above test produces something similar to the content below:

```
REDIS0011�      redis-ver7.2.3�
redis-bits�@�ctime�]�eused-mem� Xaof-base���mykey
                                                 Hello
```

Restart the container again with:

```
▶️Windows 10: docker restart redis-docker
▶️Ubuntu 22.10: $ sudo docker restart redis-docker
```

Try the CLI again, and run the command <code>get mykey</code>, the data should still be there. New data are written to the same file.

<h3 style="color:teal;">
  <a id="test-code">Rust and Python test code</a>
</h3>

The test code is extremely simple, taken directly from respective official documentations. The primary purpose of the test code is to verify that we can programmatically access the Docker Redis server.

<h4 style="color:teal;">
  <a id="rust-test-code">Rust test code</a>
</h4>

<p>
The Redis official page <a href="https://redis.io/docs/connect/clients/" title="Connect with Redis clients" target="_blank">Connect with Redis clients</a> doesn't mention Rust. <a href="https://docs.rs/redis/latest/redis/" title="Crate redis" target="_blank">Crate redis</a> seems popular on <a href="https://crates.io/" title="https://crates.io/" target="_blank">https://crates.io/</a>.
</p>

The Rust test code is taken directly from the <a href="https://docs.rs/redis/latest/redis/" title="Crate redis" target="_blank">crate redis</a> official documentation.

```
Content of Cargo.toml:
```

```toml
[package]
name = "redis"
version = "0.1.0"
edition = "2021"

# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

[dependencies]
redis = "0.24.0"
```

```
Content of src/main.rs:
```

```rust
use redis::Commands;

fn do_something() -> redis::RedisResult<i32> {
    let client = redis::Client::open("redis://127.0.0.1/")?;
    let mut con = client.get_connection()?;

    let _ : () = con.set("my_key", 42)?;
    let res = con.get("my_key")?;

    Ok(res)
}

fn main() {
    match do_something() {
        Ok(i) => println!("result: {}", i),
        Err(e) => println!("Error {}", e)
    }
}
```

The screenshot below shows the output of the program, and some CLI tests to verify that the program has successfully written data to the database file:

![092-03.png](https://behainguyen.files.wordpress.com/2023/12/092-03.png)

<h4 style="color:teal;">
  <a id="Python-test-code">Python test code</a>
</h4>

The test code is taken from the following official documents: <a href="https://redis.io/docs/connect/clients/python/" title="Redis Python guide" target="_blank">Redis Python guide</a> and <a href="https://github.com/redis/redis-py" title="GitHub redis-py" target="_blank">GitHub redis-py</a>.

Activate a virtual environment and install the Python <code>redis-py</code> package:

```
pip install redis
```

```
Content of redis1.py:
```

```python
import redis

def some_thing():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    print('my_key value, set previously: ', r.get('my_key'))
    print('mykey value, set previously: ', r.get('mykey'))

    r.set('python', 'Python and Redis')
    print('python value, just set: ', r.get('python'))

some_thing()
```

The command to run the <code>redis1.py</code> script:

```
▶️Windows 10: (venv) F:\pydev>venv\Scripts\python.exe redis1.py
▶️Ubuntu 22.10: (venv) behai@hp-pavilion-15:~/pydev$ venv/bin/python redis1.py
```

Output on Windows 10 and Ubuntu 22.10:

{% include image-gallery.html list=page.gallery-image-list %}

<br/>

<h3 style="color:teal;">
  <a id="custom-config-remote-connection">Unable to Apply Custom Config: no Remote Connection</a>
</h3>

The <a href="https://hub.docker.com/_/redis" title="Redis Docker Official Image" target="_blank">Redis Docker Official Image</a> states that we can run the image with a custom configuration file which lives locally on the host machine:

>Alternatively, you can specify something along the same lines with docker run options.
>
><code>$ docker run -v /myredis/conf:/usr/local/etc/redis --name myredis redis redis-server /usr/local/etc/redis/redis.conf</code>
>
>Where <code>/myredis/conf/</code> is a local directory containing your <code>redis.conf</code> file. Using this method means that there is no need for you to have a Dockerfile for your redis container.
>
>The mapped directory should be writable, as depending on the configuration and mode of operation, Redis may need to create additional configuration files or rewrite existing ones.

<p>
And I've taken the example configuration from this official page <a href="https://redis.io/docs/management/config-file/" title="Redis configuration file example" target="_blank">Redis configuration file example</a>. And the location of the custom configuration file in each host machine is:
</p>

```
Windows 10: E:\redis-config\redis.conf
Ubuntu 22.10: /home/behai/Public/database/redis-config/redis.conf
```

The command to run with a custom configuration file:

```
▶️Windows 10: docker run --publish=6379:6379 --network redis-network -d -it --rm --mount type=bind,source=//d/database/redis,target=/data -v //e/redis-config:/usr/local/etc/redis --name redis-docker redis redis-server /usr/local/etc/redis/redis.conf
▶️Ubuntu 22.10: $ sudo docker run --publish=6379:6379 --network redis-network -d -it --rm --mount type=bind,source=/home/behai/Public/database/redis,target=/data -v /home/behai/Public/database/redis-config:/usr/local/etc/redis --name redis-docker redis redis-server /usr/local/etc/redis/redis.conf
```

It does not report any problem, but checking the status with:

```
▶️Windows 10: docker logs redis-docker
▶️Ubuntu 22.10: $ sudo docker logs redis-docker
```

shows the following warning:

```
Warning: Could not create server TCP listening socket ::1:6379: bind: Cannot assign requested address
```

👎 We won't be able to run the CLI <a href="#running-redis-cli-container">directly via the container</a> as discussed. 🚀 However, the <a href="#running-redis-cli-bash">Bash mode interactive</a> still works.

From my Windows 10 machine, I can't programmatically connect to the Redis container running on Ubuntu 22.10 -- see <a href="#test-code">Rust and Python test code</a> section. 

-- I just change <code>localhost</code> to the IP address of the Ubuntu 22.10 machine, and also allow traffics through port <code>6379</code> with command <code>sudo ufw allow 6379</code>.

I <strong>assume</strong> that the server has been configured to recognise only traffics from <code>localhost</code>? A custom configure would help to overwrite this, but I'm not able to do this... This is a task for another day.

<h3 style="color:teal;">
  <a id="my-other-docker-posts">Other Docker Posts Which I've Written</a>
</h3>

<ol>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2023/07/24/synology-ds218-sudo-password-and-unsupported-docker-problems-update/" title="Synology DS218: sudo password and unsupported Docker problems update..." target="_blank">Synology DS218: sudo password and unsupported Docker problems update...</a> -- I have been updating the DSM without running <code>sudo</code> or <code>docker</code>. I have just tried both recently, both failed. I'm describing how I've managed to fix these two problems.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2022/11/29/docker-compose-how-to-wait-for-the-mysql-server-container-to-be-ready/" title="Docker Compose: how to wait for the MySQL server container to be ready?" target="_blank">Docker Compose: how to wait for the MySQL server container to be ready?</a> -- Waiting for a database server to be ready before starting our own application, such as a middle-tier server, is a familiar issue. Docker Compose is no exception. Our own application container must also wait for their own database server container ready to accept requests before sending requests over. I've tried two ( 2 ) “wait for” tools which are officially recommended by Docker. I'm discussing my attempts in this post, and describing some of the pending issues I still have.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2022/07/20/synology-ds218-unsupported-docker-installation-and-usage/" title="Synology DS218: unsupported Docker installation and usage..." target="_blank">Synology DS218: unsupported Docker installation and usage...</a> -- Synology does not have Docker support for AArch64 NAS models. DS218 is an AArch64 NAS model. In this post, we're looking at how to install Docker for unsupported Synology DS218, and we're also conducting tests to prove that the installation works.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2022/07/22/python-docker-image-build-install-required-packages-via-requirements-txt-vs-editable-install/" title="Python: Docker image build -- install required packages via requirements.txt vs editable install." target="_blank">Python: Docker image build -- install required packages via requirements.txt vs editable install.</a> -- Install via requirements.txt means using this image build step command “RUN pip3 install -r requirements.txt”. Editable install means using the “RUN pip3 install -e .” command. I've experienced that install via requirements.txt resulted in images that do not run, whereas using editable install resulted in images that do work as expected. I'm presenting my findings in this post.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2022/07/25/python-docker-image-build-the-werkzeug-problem-%f0%9f%a4%96/" title="Python: Docker image build -- “the Werkzeug” problem 🤖!" target="_blank">Python: Docker image build -- “the Werkzeug” problem 🤖!</a> -- I've experienced Docker image build installed a different version of the Werkzeug dependency package than the development editable install process. And this caused the Python project in the Docker image failed to run. Development editable install means running the “pip3 install -e .” command within an active virtual environment. I'm describing the problem and how to address it in this post.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2022/07/27/python-docker-image-build-save-to-and-load-from-tar-files/" title="Python: Docker image build -- save to and load from *.tar files." target="_blank">Python: Docker image build -- save to and load from *.tar files.</a> -- We can save Docker images to local *.tar files, and later load and run those Docker images from local *.tar files. I'm documenting my learning experimentations in this post.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2022/07/29/python-docker-volumes-where-is-my-sqlite-database-file/" title="Python: Docker volumes -- where is my SQLite database file?" target="_blank">Python: Docker volumes -- where is my SQLite database file?</a> -- The Python application in a Docker image writes some data to a SQLite database. Stop the container, and re-run again, the data are no longer there! A volume must be specified when running an image to persist the data. But where is the SQLite database file, in both Windows 10 and Linux? We're discussing volumes and where volumes are on disks for both operating systems.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2022/08/09/docker-on-windows-10-running-mysql8-0-30-debian-with-a-custom-config-file/" title="Docker on Windows 10: running mysql:8.0.30-debian with a custom config file." target="_blank">Docker on Windows 10: running mysql:8.0.30-debian with a custom config file.</a> -- Steps required to run the official mysql:8.0.30-debian image on Windows 10 with custom config file E:\mysql-config\mysql-docker.cnf.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2022/10/21/docker-on-windows-10-mysql8-0-30-debian-log-files/" title="Docker on Windows 10: mysql:8.0.30-debian log files" target="_blank">Docker on Windows 10: mysql:8.0.30-debian log files </a> -- Running the Docker Official Image mysql:8.0.30-debian on my Windows 10 Pro host machine, I want to log all queries, slow queries and errors to files on the host machine. In this article, we're discussing how to go about achieving this.</li>
<li style="margin-top:10px;"><a href="https://behainguyen.wordpress.com/2022/11/13/pgloader-docker-migrating-from-docker-localhost-mysql-to-localhost-postgresql/" title="pgloader Docker: migrating from Docker & localhost MySQL to localhost PostgreSQL." target="_blank">pgloader Docker: migrating from Docker & localhost MySQL to localhost PostgreSQL.</a> -- Using the latest dimitri/pgloader Docker image build, I've migrated a Docker MySQL server 8.0.30 database, and a locally installed MySQL server 5.5 database to a locally installed PostgreSQL server 14.3 databases. I am discussing how I did it in this post.</li>
</ol>

I hope you find the information in this post helpful. Thank you for reading. Wishing you a Merry Christmas and a New Year full of Happiness and Health. Stay safe as always.

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
<a href="https://1000logos.net/download-image/" target="_blank">https://1000logos.net/download-image/</a>
</li>
<li>
<a href="https://www.cleanpng.com/png-docker-software-deployment-intermodal-container-mi-3369341/download-png.html" target="_blank">https://www.cleanpng.com/png-docker-software-deployment-intermodal-container-mi-3369341/download-png.html</a>
</li>
</ul>
