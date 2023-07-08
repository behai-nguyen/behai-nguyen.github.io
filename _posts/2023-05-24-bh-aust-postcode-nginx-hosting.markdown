---
layout: post
title: "Ubuntu 22.10: hosting a Python Flask web API with Gunicorn and Nginx."

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list:
    - "https://behainguyen.files.wordpress.com/2023/05/067-01.png"
    - "https://behainguyen.files.wordpress.com/2023/05/067-02.png"

description: The Python Flask web API is a simple web API to search for Australian postcodes based on locality aka suburb. With a newly installed Ubuntu 22.10 environment, we will go through the steps to host this web API using Gunicorn and Nginx.
tags:
- Ubuntu
- Python
- Flask
- Gunicorn
- Nginx
---

<em style="color:#111;">The Python Flask web API is a simple web API to search for Australian postcodes based on locality aka suburb. With a newly installed Ubuntu 22.10 environment, we will go through the steps to host this web API using Gunicorn and Nginx.</em>

| ![067-feature-image.png](https://behainguyen.files.wordpress.com/2023/05/067-feature-image.png) |
|:--:|
| *Ubuntu 22.10: hosting a Python Flask web API with Gunicorn and Nginx.* |

In this post
<a href="https://behainguyen.wordpress.com/2023/05/18/python-a-simple-web-api-to-search-for-australian-postcodes-based-on-locality-aka-suburb/"
title="Python: A simple web API to search for Australian postcodes based on locality aka suburb."
target="_blank">Python: A simple web API to search for Australian postcodes based on locality aka suburb</a>,
I've developed a complete working web API. I'm discussing the steps to host this web API on 
<a href="https://releases.ubuntu.com/kinetic/" title="Ubuntu 22.10 (Kinetic Kudu)" target="_blank">Ubuntu 22.10 (Kinetic Kudu)</a>,
using <a href="https://gunicorn.org/" title="Gunicorn" target="_blank">Gunicorn</a>
and <a href="https://www.nginx.com/" title="Nginx" target="_blank">Nginx</a>.

The final content of this post has been written based on a fresh installation 
of Ubuntu 22.10. The firewall was disabled by default. We enable it:

```
$ sudo ufw enable
```

Verify that it has been enabled via:

```
$ sudo ufw status
```

The Ubuntu 22.10 machine name (host name) is
<code>hp-pavilion-15</code>, its IP address is <code>192.168.0.17</code>.
These two identifiers will be used throughout this post.

<span style="color:blue;">
The first draft of this post was based on my existing Ubuntu 22.10 installation,
whereby accessing the final site was working for both <code>hp-pavilion-15</code> 
and <code>192.168.0.17</code>. Then I did something which damaged Ubuntu, and
I don't know how to recover, so did a fresh reinstallation: <code>hp-pavilion-15</code> 
is no longer working!
</span>

<!--------------------------------------------------------------------------------->

<h2>Table of contents</h2>

<ul>
	<li style="margin-top:10px;"><a href="#install-required-software">Install required software</a></li>
	<li style="margin-top:10px;"><a href="#nginx-config">Nginx configuration -- /etc/nginx/nginx.conf</a></li>
	<li style="margin-top:10px;"><a href="#user-behai">About <code>user behai;</code> in /etc/nginx/nginx.conf</a></li>
	<li style="margin-top:10px;"><a href="#project-set-up">Set up the web API project in Ubuntu 22.10</a></li>
	<li style="margin-top:10px;"><a href="#configure-service">Configure the virtual host service for the web API</a></li>
	<li style="margin-top:10px;"><a href="#vhost-port-82">Assign port 82 to the web API virtual host</a></li>
	<li style="margin-top:10px;"><a href="#restart-nginx">Restart Nginx</a></li>
	<li style="margin-top:10px;"><a href="#windows-10-test">Test the final virtual host from Windows 10</a></li>
	<li style="margin-top:10px;"><a href="#current-firewall-status">Current firewall status</a></li>
	<li style="margin-top:10px;"><a href="#concluding-remarks">Concluding remarks</a></li>
</ul>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="install-required-software">Install required software</a>
</h3>

We need to install some <code>Python related tools</code>, <code>Nginx</code> 
and <code>git</code>. Run the following commands:

```
$ sudo apt-get update
$ sudo apt-get install python3-pip python3-dev nginx
$ sudo apt install python3-virtualenv
$ sudo apt install git
```

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="nginx-config">Nginx configuration -- /etc/nginx/nginx.conf</a>
</h3>

We make two changes to Nginx configuration file <code>/etc/nginx/nginx.conf</code>:

<ol>
	<li style="margin-top:10px;">
        <code>user behai;</code> -- <code>user</code> changed to <code>behai</code>.
        (I.e. commented out <code>user www-data;</code>.) <code>behai</code> is the 
        user I use to log into Ubuntu.
    </li>

	<li style="margin-top:10px;">
		Enable <code>server_names_hash_bucket_size 64;</code> -- remove comment <code>#</code>.
	</li>
</ol>

Using <code>nano</code> to edit the Nginx config file 
<code>/etc/nginx/nginx.conf</code>:

```
$ sudo nano /etc/nginx/nginx.conf
```

```conf
# user www-data;
user behai;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

...

http {

	##
	# Basic Settings
	##

	sendfile on;
	tcp_nopush on;
	types_hash_max_size 2048;
	# server_tokens off;

	server_names_hash_bucket_size 64;

...
```

Check Nginx configuration:

```
$ sudo nginx -t
```

If everything is okay, the output should be as follows:

```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

Restart Nginx and verify its status with the following commands:

```
$ sudo systemctl restart nginx
$ systemctl status nginx.service
```

Opens both <code>port 80</code> and <code>port 443</code> to 
allow both unencrypted and encrypted web traffic:

```
$ sudo ufw allow 'Nginx Full'
```

Nginx should now be ready, default site should be available.
From Windows 10, I can get to the Nginx default site with 
<a href="http://hp-pavilion-15" title="http://hp-pavilion-15" target="_blank">http://hp-pavilion-15</a>
and
<a href="http://192.168.0.17" title="http://192.168.0.17" target="_blank">http://192.168.0.17</a>:

![067-03.png](https://behainguyen.files.wordpress.com/2023/05/067-03.png)

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="user-behai">About <code>user behai;</code> in /etc/nginx/nginx.conf</a>
</h3>

Quoting  
<a href="https://docs.gunicorn.org/en/stable/deploy.html"
title="Deploying Gunicorn"
target="_blank">Deploying Gunicorn</a> -- a Gunicorn official documentation page:

> 
> <code>www-data</code> is the default nginx user in debian, other distributions use different users (for example: <code>http</code> or <code>nginx</code>). Check your distro to know what to put for the socket user, and for the sudo command.
> 

And see also this 
<a href="https://stackoverflow.com/a/24035502/20728472" title="Stack Overflow answer" target="_blank">Stack Overflow answer</a>,
<span style="color:red;font-weight:bold;">I DID ALSO ATTEMPT 
<a href="https://stackoverflow.com/a/24830777/6381711" title="Joseph Barbere's solution" target="_blank">Joseph Barbere's solution</a> --
DO NOT DO THAT! As a part of that suggested solution, I had to install SELinux, which is no longer
compatible with Ubuntu 22.10; it damaged mine, I don't know how to recover from the 
GRUB menu, that was why I did a fresh reinstallation.
</span>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="project-set-up">Set up the web API project in Ubuntu 22.10</a>
</h3>

This step has been documented in 
<a href="https://github.com/behai-nguyen/bh_aust_postcode/blob/main/README.md" title="GitHub Read Me" target="_blank">GitHub Read Me</a>.
It is reproduced in this section.

Get the repo <a href="https://github.com/behai-nguyen/bh_aust_postcode.git" title="https://github.com/behai-nguyen/bh_aust_postcode.git" target="_blank">https://github.com/behai-nguyen/bh_aust_postcode.git</a>
to directory <code>/home/behai/webwork/bh_aust_postcode</code>. Its content should 
look like the screenshot below:

![067-04.png](https://behainguyen.files.wordpress.com/2023/05/067-04.png)

Create the virtual environment <code>venv</code>:

```
behai@HP-Pavilion-15:~/webwork/bh_aust_postcode$ virtualenv venv
```

To activate virtual environment <code>venv</code>:

```
behai@HP-Pavilion-15:~/webwork/bh_aust_postcode$ source venv/bin/activate
```

Editable install project:

```
(venv) behai@HP-Pavilion-15:~/webwork/bh_aust_postcode$ venv/bin/pip install -e .
```

Install <code>gunicorn</code> separately:

```
(venv) behai@HP-Pavilion-15:~/webwork/bh_aust_postcode$ venv/bin/pip install gunicorn
```

Download postcodes and write to SQLite database file:

```
(venv) behai@HP-Pavilion-15:~/webwork/bh_aust_postcode$ venv/bin/flask update-postcode
```

-- Please note, the above step is only specific to this project.

Enable <code>port 5000</code>:

```
$ sudo ufw allow 5000
```

Run the web server via <code>gunicorn</code>:

```
(venv) behai@HP-Pavilion-15:~/webwork/bh_aust_postcode$ venv/bin/gunicorn --bind 0.0.0.0:5000 wsgi:app
```

At this point, the following should be accessible from Windows 10, 
or other devices connected to the Wifi network for that matter:

<ul>
	<li style="margin-top:10px;">👎 
	<a href="http://hp-pavilion-15:5000/api/v0/ui" title="http://hp-pavilion-15:5000/api/v0/ui" target="_blank">http://hp-pavilion-15:5000/api/v0/ui</a>
    -- <span style="color:red;font-weight:bold;">it should work, but does not 👎!</span>
	</li>

	<li style="margin-top:10px;">👎 
    <a href="http://hp-pavilion-15:5000/api/v0/aust-postcode/spring" title="http://hp-pavilion-15:5000/api/v0/aust-postcode/spring" target="_blank">http://hp-pavilion-15:5000/api/v0/aust-postcode/spring</a>
    -- <span style="color:red;font-weight:bold;">it should work, but does not 👎!</span>
	</li>

	<li style="margin-top:10px;">🚀 
	<a href="http://192.168.0.17:5000/api/v0/ui" title="http://192.168.0.17:5000/api/v0/ui" target="_blank">http://192.168.0.17:5000/api/v0/ui</a>
    -- <span style="color:blue;font-weight:bold;">it does work 🚀!</span>
	</li>

	<li style="margin-top:10px;">🚀 
    <a href="http://192.168.0.17:5000/api/v0/aust-postcode/spring" title="http://192.168.0.17:5000/api/v0/aust-postcode/spring" target="_blank">http://192.168.0.17:5000/api/v0/aust-postcode/spring</a>
    -- <span style="color:blue;font-weight:bold;">it does work 🚀!</span>
	</li>
</ul>

I have spent a lot of hours trying to get host name (<code>hp-pavilion-15</code>) 
to work, no avail so far: it does work if I turn off the firewall -- but we don't 
want to do that. I think it has something to do with the socket, because we've seen
the default Nginx site can be accessed via <code>hp-pavilion-15</code>. And also, I've
reinstalled Jenkins, and I can access it via 
<a href="http://hp-pavilion-15:8080" title="http://hp-pavilion-15:8080" target="_blank">http://hp-pavilion-15:8080</a>.

Stop the <code>gunicorn</code> web server with <code>Ctrl+C</code>, and 
deactivate the virtual environment with:

```
(venv) behai@HP-Pavilion-15:~/webwork/bh_aust_postcode$ deactivate
```

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="configure-service">Configure the virtual host service for the web API</a>
</h3>

Please note, the current working directory is still <code>/home/behai/webwork/bh_aust_postcode</code>.
Run the test service command, this command will be used in the 
service configuration file, test it first to ensure that it works:

```
$ /home/behai/webwork/bh_aust_postcode/venv/bin/gunicorn --workers 3 --bind unix:bh_aust_postcode.sock -m 007 wsgi:app
```

Output:

```
[2023-05-20 21:20:27 +1000] [5295] [INFO] Starting gunicorn 20.1.0
[2023-05-20 21:20:27 +1000] [5295] [INFO] Listening at: unix:bh_aust_postcode.sock (5295)
[2023-05-20 21:20:27 +1000] [5295] [INFO] Using worker: sync
[2023-05-20 21:20:27 +1000] [5296] [INFO] Booting worker with pid: 5296
[2023-05-20 21:20:27 +1000] [5297] [INFO] Booting worker with pid: 5297
[2023-05-20 21:20:27 +1000] [5298] [INFO] Booting worker with pid: 5298
```

Create the service file <code>/etc/systemd/system/bh_aust_postcode.service</code>:

```
$ sudo nano /etc/systemd/system/bh_aust_postcode.service
```

This is the content, note the directories and the above command:

```conf
[Unit]

Description=bh-aust-postcode

After=network.target

[Service]

User=behai
Group=www-data
WorkingDirectory=/home/behai/webwork/bh_aust_postcode

Environment="PATH=/home/behai/webwork/bh_aust_postcode/venv/bin"

ExecStart=/home/behai/webwork/bh_aust_postcode/venv/bin/gunicorn --workers 3 --bind unix:bh_aust_postcode.sock -m 007 wsgi:app

[Install]

WantedBy=multi-user.target
```

Enable the service:

```
$ sudo systemctl start bh_aust_postcode
```

This command has no output. And the next command:

```
$ sudo systemctl enable bh_aust_postcode
```

And its output:

```
Created symlink /etc/systemd/system/multi-user.target.wants/bh_aust_postcode.service → /etc/systemd/system/bh_aust_postcode.service.
```

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="vhost-port-82">Assign port 82 to the web API virtual host</a>
</h3>

The virtual host configuration file is <code>/etc/nginx/sites-available/bh_aust_postcode</code>, 
create it with the command:

```
$ sudo nano /etc/nginx/sites-available/bh_aust_postcode
```

And its content is:

```conf
server {
    listen 82;

    server_name localhost;
    location / {
        include proxy_params;

        proxy_pass http://unix:/home/behai/webwork/bh_aust_postcode/bh_aust_postcode.sock;
    }
}
```

We're assigning <code>port 82</code> to this virtual host,
and get Nginx to forward requests to, effectively, <code>/home/behai/webwork/bh_aust_postcode</code>.
For explanation on <code>proxy_pass</code>, please see 
<a href="https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/" title="NGINX Reverse Proxy" target="_blank">NGINX Reverse Proxy</a>

Next, we must enable the virtual host. Verify that it has not been enabled:

```
$ sudo ls -l /etc/nginx/sites-enabled
```

In the output, there should not be an entry for 
<code>/etc/nginx/sites-available/bh_aust_postcode</code>.

Enable it by creating a link to <code>sites-enabled</code>:

```
$ sudo ln -s /etc/nginx/sites-available/bh_aust_postcode /etc/nginx/sites-enabled
```

Verify to ensure it has been enabled, i.e. there should be a symlink:

```
$ sudo ls -l /etc/nginx/sites-enabled
```

Among the entries, there should be an entry like the below:

```
lrwxrwxrwx 1 root root 43 May 20 10:22 bh_aust_postcode -> /etc/nginx/sites-available/bh_aust_postcode
```

See 
<a href="https://serverfault.com/questions/527630/difference-in-sites-available-vs-sites-enabled-vs-conf-d-directories-nginx" title="Difference in sites-available vs sites-enabled vs conf.d directories (Nginx)?" target="_blank">Difference in sites-available vs sites-enabled vs conf.d directories (Nginx)?</a>
for more discussion on this topic.

Open incoming TCP <code>port 82</code> <strong>to all IP addresses</strong>:

```
$ sudo ufw allow from any to any port 82 proto tcp
```

Output:

```
Rule added
Rule added (v6)
```

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="restart-nginx">Restart Nginx</a>
</h3>

Given that we've verified that Nginx configuration valid, we can now restart it, via:

```
$ sudo systemctl restart nginx
```

The above command has no output. We should check out the status of Nginx, with:

```
$ systemctl status nginx.service
```

We can see that it is <code>active (running)</code>, that means we have it working:

```
● nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; preset: enabled)
     Active: active (running) since Sat 2023-05-20 10:38:03 AEST; 5s ago
       Docs: man:nginx(8)
    Process: 4154 ExecStartPre=/usr/sbin/nginx -t -q -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
    Process: 4155 ExecStart=/usr/sbin/nginx -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
   Main PID: 4156 (nginx)
      Tasks: 5 (limit: 9363)
     Memory: 4.8M
        CPU: 26ms
     CGroup: /system.slice/nginx.service
             ├─4156 "nginx: master process /usr/sbin/nginx -g daemon on; master_process on;"
             ├─4157 "nginx: worker process"
             ├─4158 "nginx: worker process"
             ├─4159 "nginx: worker process"
             └─4160 "nginx: worker process"

May 20 10:38:03 HP-Pavilion-15 systemd[1]: Starting A high performance web server and a reverse proxy server...
May 20 10:38:03 HP-Pavilion-15 systemd[1]: Started A high performance web server and a reverse proxy server.
```

The simple web API to search for Australian postcodes based on locality 
virtual host setup is now completed. 

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="windows-10-test">Test the final virtual host from Windows 10</a>
</h3>

At this point, the following should be accessible from Windows 10, 
or other devices connected to the Wifi network for that matter:

<ul>
	<li style="margin-top:10px;">👎 
	<a href="http://hp-pavilion-15:82/api/v0/ui" title="http://hp-pavilion-15:82/api/v0/ui" target="_blank">http://hp-pavilion-15:82/api/v0/ui</a>
    -- <span style="color:red;font-weight:bold;">it should work, but does not 👎!</span>
	</li>

	<li style="margin-top:10px;">👎 
    <a href="http://hp-pavilion-15:82/api/v0/aust-postcode/spring" title="http://hp-pavilion-15:82/api/v0/aust-postcode/spring" target="_blank">http://hp-pavilion-15:82/api/v0/aust-postcode/spring</a>
    -- <span style="color:red;font-weight:bold;">it should work, but does not 👎!</span>
	</li>

	<li style="margin-top:10px;">🚀 
	<a href="http://192.168.0.17:82/api/v0/ui" title="http://192.168.0.17:82/api/v0/ui" target="_blank">http://192.168.0.17:82/api/v0/ui</a>
    -- <span style="color:blue;font-weight:bold;">it does work 🚀!</span>
	</li>

	<li style="margin-top:10px;">🚀 
    <a href="http://192.168.0.17:82/api/v0/aust-postcode/spring" title="http://192.168.0.17:82/api/v0/aust-postcode/spring" target="_blank">http://192.168.0.17:82/api/v0/aust-postcode/spring</a>
    -- <span style="color:blue;font-weight:bold;">it does work 🚀!</span>
	</li>
</ul>

The following screenshots show the API in action. I took these 
using the previous Ubuntu installation, which was still version 22.10. I
did have the host name working (as shown) then, but not now:

{% include image-gallery.html list=page.gallery-image-list %}

Now, the problem is:

![067-05.png](https://behainguyen.files.wordpress.com/2023/05/067-05.png)

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="current-firewall-status">Current firewall status</a>
</h3>

The current status of my firewall.

```
$ sudo ufw status verbose
```

```
[sudo] password for behai:
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere
445                        ALLOW IN    Anywhere
5000                       ALLOW IN    Anywhere
80,443/tcp (Nginx Full)    ALLOW IN    Anywhere
8080                       ALLOW IN    Anywhere
82/tcp                     ALLOW IN    Anywhere
22/tcp (v6)                ALLOW IN    Anywhere (v6)
445 (v6)                   ALLOW IN    Anywhere (v6)
5000 (v6)                  ALLOW IN    Anywhere (v6)
80,443/tcp (Nginx Full (v6)) ALLOW IN    Anywhere (v6)
8080 (v6)                  ALLOW IN    Anywhere (v6)
82/tcp (v6)                ALLOW IN    Anywhere (v6)
```

<code>Port 5000</code> which's been enabled previously is no longer required, it could be deleted.

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="concluding-remarks">Concluding remarks</a>
</h3>

Prior to this post, I have set up several other virtual hosts with 
my original Ubuntu 22.10 installation, when I started this post, it
was probably behind with some updates... When it got damaged, the 
first reinstallation I did was 
<a href="https://releases.ubuntu.com/lunar/" title="Ubuntu 23.04 (Lunar Lobster)" target="_blank">Ubuntu 23.04 (Lunar Lobster)</a>,
I could not get host name to work. I reversed back to this 22.10 version,
this time, I upgraded all packages, and host name is still not working
for this virtual host.

It's been an interesting exercise... I could not get what I wanted, but
it's been a useful exercise for me, regardless. I'm sure something will 
turn up, and I will able to fix this annoying problem in the future.

I hope you find the info useful. Thank you for reading and stay safe as always.

✿✿✿

Feature image sources:

<ul>
<li>
<a href="https://in.pinterest.com/pin/337277459600111737/" target="_blank">https://in.pinterest.com/pin/337277459600111737/</a>
</li>
<li>
<a href="https://www.pngwing.com/en/free-png-azefz/download" target="_blank">https://www.pngwing.com/en/free-png-azefz/download</a>
</li>
<li>
<a href="https://icon-icons.com/download/170045/PNG/512/" target="_blank">https://icon-icons.com/download/170045/PNG/512/</a>
</li>
<li>
<a href="https://seeklogo.com/vector-logo/332789/python" target="_blank">https://seeklogo.com/vector-logo/332789/python</a>
</li>
<li>
<a href="https://flask-restx.readthedocs.io/en/latest/" target="_blank">https://flask-restx.readthedocs.io/en/latest/</a>
</li>
<li>
<a href="https://www.vectorstock.com/royalty-free-vector/australia-map-with-flag-blue-red-background-vector-25323215" target="_blank">https://www.vectorstock.com/royalty-free-vector/australia-map-with-flag-blue-red-background-vector-25323215</a>
</li>
<li>
<a href="https://logos-world.net/australia-post-logo/" target="_blank">https://logos-world.net/australia-post-logo/</a>
</li>
</ul>
