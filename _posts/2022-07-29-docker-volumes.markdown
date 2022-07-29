---
layout: post
title: "Python: Docker volumes -- where is my SQLite database file?"

---

The Python application in a Docker image writes some data to a SQLite database. 
Stop the container, and re-run again, the data are no longer there! 
A volume must be specified when running an image to persist the data. 
But where is the SQLite database file, in both Windows 10 and Linux? 
We're discussing volumes and where volumes are on disks for both operating systems.

| ![033-feature-image.png](https://behainguyen.files.wordpress.com/2022/07/033-feature-image.png) |
|:--:|
| *Python: Docker volumes -- where is my SQLite database file?* |

<p>
In this post, we're using the images created in 
<a href="https://behainguyen.wordpress.com/2022/07/27/python-docker-image-build-save-to-and-load-from-tar-files/" 
title="Python: Docker image build -- save to and load from *.tar files."
target="_blank">Python: Docker image build -- save to and load from *.tar files.</a> 
<strong>In a nutshell</strong>, these images contain a 
<span class="keyword">
Python</span> project, which uses a 
<span class="keyword">
SQLite</span> database. The same images are built for both 
<span class="keyword">
Windows 10 Pro</span> ( 64-bit, x64-based ),
and 
<span class="keyword">
linux/arm64</span> ( AArch64 ): which is my 
<span class="keyword">
Synology DS218</span> box. And we're going to look at 
<span class="keyword">
Docker volumes</span> on both operating systems.
</p>

<p>
The code used to build 
<span class="keyword">
Docker images</span> in this post can be cloned with:
</p>

```
git clone -b v1.0.2 https://github.com/behai-nguyen/flask-restx-demo.git
```

<p>
<strong>Please also note</strong> the 
<span class="keyword">
git clone</span> command above also includes a test 
<span class="keyword">HTML</span>
page using 
<span class="keyword">JQuery</span> 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
test_client_app\jquery-ajax\TreeAPIClient.html</span>, 
just copy it to a web site or a virtual web directory, and run it from there, for
<strong>API URL</strong> use 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
http://ip-address:port/api/v1/trees</span>.
</p>

<!--------------------------------------------------------------------------------->

<h2>Table of contents</h2>

<ul>
	<li style="margin-top:5px;"><a href="#environments">Environments</a></li>
	
	<li style="margin-top:10px;"><a href="#docker-desktop-installation">Docker Desktop uses WSL 2 based engine</a></li>

	<li style="margin-top:10px;"><a href="#docker-volumes-on-windows">Docker volumes on Windows 10 Pro</a>
		<ol>
			<li style="margin-top:10px;"><a href="#docker-volumes-options">Docker volume options</a></li>

			<li style="margin-top:10px;"><a href="#docker-volumes-options-values">“datavolume” and “flask_restx_demo” values</a></li>

			<li style="margin-top:10px;"><a href="#docker-volumes-name-container">Name container and “flask_restx_demo”</a></li>

			<li style="margin-top:10px;"><a href="#docker-volumes-on-disk">Docker volumes on disk</a></li>
		</ol>
	</li>

	<li style="margin-top:10px;"><a href="#docker-volumes-linux-arm64">Docker volumes on Synology DS218 ( linux/arm64 )</a></li>
	
	<li style="margin-top:10px;"><a href="#volume-or-mount-option">--volume / -v or --mount option?</a></li>

	<li style="margin-top:10px;"><a href="#concluding-remarks">Concluding remarks</a></li>
</ul>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="environments">Environments</a>
</h3>

<ol>
<li style="margin-top:5px;">
<span class="keyword"> Synology DS218</span> -- <span class="keyword"> DSM 7.1-42661 Update 3</span>.
</li>

<li style="margin-top:10px;">
<span class="keyword"> Windows 10 Pro</span> -- <span class="keyword"> version 10.0.19044 build 19044</span>.
System name is 
<span class="keyword">
<strong>DESKTOP-7BA02KU</strong></span>.
</li>

<li style="margin-top:10px;">
<span class="keyword">
Windows Subsystem for Linux ( WSL 2 )</span> -- running 
<span class="keyword">
Ubuntu 20.04.4 LTS (Focal Fossa)</span>.
</li>

<li style="margin-top:10px;">
<span class="keyword"> Windows “docker” CLI</span> -- <span class="keyword"> version 20.10.12, build e91ed57</span>.
</li>

<li style="margin-top:10px;">
<span class="keyword"> Windows Docker Desktop</span> -- <span class="keyword"> version 4.4.3</span>. The latest version is <span class="keyword"> 4.10.1</span>.
</li>

<li style="margin-top:10px;">
<span class="keyword"> Synology DS218</span> -- it's accessed via its device name <span class="keyword"> <strong>omphalos-nas-01</strong></span> instead of its IP address.
</li>
</ol>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="docker-desktop-installation">Docker Desktop uses WSL 2 based engine</a>
</h3>

<p>
I installed 
<span class="keyword">
Windows Subsystem for Linux ( WSL 2 )</span> prior to 
<span class="keyword">
Docker Desktop</span> and all associated
<span class="keyword">
CLIs</span>. I think I've installed 
<span class="keyword">
Docker Desktop</span> using all recommended options, when the installer 
picked <span class="keyword">
WSL 2 based engine</span>, I did agree with that, even though I was not 
at all sure what it means:
</p>

![033-01-docker-desktop-installation-1.png](https://behainguyen.files.wordpress.com/2022/07/033-01-docker-desktop-installation-1.png)

<p style="clear:both;">
I have found out that when we run 
<span class="keyword">
Docker images</span> using
<span class="keyword">
Docker volumes</span> on my 
<span class="keyword">
Windows 10 Pro</span>, 
<span class="keyword">
Docker volumes</span> actually live on
<span class="keyword">
WSL 2</span>.
</p>

<p>
That means, in this post, for 
<span class="keyword">
Windows 10 Pro</span>,
<span class="keyword">
Docker volumes</span> discussions are in the context of
<span class="keyword">
WSL 2 based engine</span> only.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="docker-volumes-on-windows">Docker volumes on Windows 10 Pro</a>
</h3>

<p>
If we don't specify a valid volume when running, then 
<span class="keyword">
SQLite</span> data only persists as long as the container is active,
when we stop this container, the data will be lost, next time we
run the same image again, we will have no data.
</p>

<p>
Official documents related to volumes:
</p>

<ul>
<li style="margin-top:5px;">
<a href="https://docs.docker.com/storage/volumes/" title="Use volumes" target="_blank">Use volumes</a>
</li>

<li style="margin-top:10px;">
<a href="https://docs.docker.com/engine/reference/commandline/run/"
title="docker run" target="_blank">docker run</a>
</li>
</ul>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="docker-volumes-options">Docker volume options</a>
</h4>

<p>
To use volumes, we must use either the 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
-v</span> short for
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
--volume</span>, or the 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
--mount</span> option. For examples:
</p>

```
C:\>docker run -v datavolume:/flask_restx_demo -d --publish 8000:8000 --rm flask-restx-demo
C:\>docker run --mount source=datavolume,target=/flask_restx_demo -d --publish 8000:8000 --rm flask-restx-demo
```

<p>
The above two ( 2 ) commands cause the containers to use the same volume. 
We can use the 
<span class="keyword">
Swagger UI</span> page 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
http://localhost:8000/api/v1/ui</span> to enter and to query data; 
or the client test page 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
http://localhost/work/TreeAPIClient.html</span>, for
<strong>API URL</strong> use 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
http://localhost:8000/api/v1/trees</span>.
</p>

<p>
Change some data. Stop the container. Start again using either command -- 
regardless of the test client, we should see the data from the previous run.
</p>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="docker-volumes-options-values">“datavolume” and “flask_restx_demo” values</a>
</h4>

<p>
Consider the below two ( 2 ) commands:
</p>

```
C:\>docker run -v datavolume:/xyz -d --publish 8000:8000 --rm flask-restx-demo
C:\>docker run --mount source=datavolume,target=/abc -d --publish 8000:8000 --rm flask-restx-demo
```

<p>
they'll start and run successfully. 
But the data will not be persisted. That is, if we stop the container, 
and re-run the same command again, any data previously entered will
no longer exist:
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
-v datavolume:/xyz</span> and 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
--mount source=datavolume,target=/abc</span> are not valid volumes.
</p>

<p>
❶ <span class="keyword">
datavolume</span> -- in the context of this post, this value will 
become a sub-directory on the file system as we shall see later. 
And we should be free to specify anything we see fit, as long as 
it's unique.
</p>

<p>
❷ <span class="keyword">
flask_restx_demo</span>, 
<span class="keyword">
xyz </span> and 
<span class="keyword">
abc</span> -- in the context of this post, they mean the same thing.
The official documents listed above explain this, but I could not fully
understand it. My experimentations show that <span style="font-weight:bold;">
this value must match the value specified for
<span class="keyword">
WORKDIR</span> in the 
<span class="keyword">
Dockerfile</span></span>. For this image, it is:
</p>

```
WORKDIR /flask_restx_demo
```

<p>
Please see 
<a href="https://github.com/behai-nguyen/flask-restx-demo/blob/main/Dockerfile"
title="Dockerfile on GitHub"
target="_blank">Dockerfile on GitHub</a>. So that means only
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
flask_restx_demo</span> is valid. I've come to this observation 
by building and running another image with a different value for 
<span class="keyword">
WORKDIR</span>.
</p>

<p>
Further to the above, these two ( 2 ) commands:
</p>

```
C:\>docker run --mount source=datavolume,target=/flask_restx_demo -d --publish 8000:8000 --rm flask-restx-demo
C:\>docker run --mount source=behaivolume,target=/flask_restx_demo -d --publish 8000:8000 --rm flask-restx-demo
```

<p>
will result in two ( 2 ) valid and <strong>independent</strong> volumes.
</p>

<p>
The next section, <a href="#docker-volumes-name-container">Name container and “flask_restx_demo”</a>, should illustrate 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
flask_restx_demo</span> a bit further.
</p>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="docker-volumes-name-container">Name container and “flask_restx_demo”</a>
</h4>

<p>
We can start a container with a specific name via the 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
--name</span> option, see 
<a href="https://docs.docker.com/engine/reference/run/#name---name"
title="Docker run reference | Name (--name)" target="_blank">Docker run reference | Name (--name)</a>:
</p>

```
D:\>docker run --name restx-demo --mount source=datavolume,target=/flask_restx_demo --publish 8000:8000 --rm flask-restx-demo
```

<p>
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
restx-demo</span> should be listed for command:
</p>

```
D:\>docker ps -a
```

<p>
We can inspect <span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
restx-demo</span> using:
</p>

```
D:\>docker inspect restx-demo
```

<p>
The output is very long, but we're interested in the following extracted sections:
</p>

```javascript
...
            "Mounts": [
                {
                    "Type": "volume",
                    "Source": "datavolume",
                    "Target": "/flask_restx_demo"
                }
            ],
...
        "Mounts": [
            {
                "Type": "volume",
                "Name": "datavolume",
                "Source": "/var/lib/docker/volumes/datavolume/_data",
                "Destination": "/flask_restx_demo",
                "Driver": "local",
                "Mode": "z",
                "RW": true,
                "Propagation": ""
            }
        ],
...
            "Image": "flask-restx-demo",
            "Volumes": null,
            "WorkingDir": "/flask_restx_demo",
            "Entrypoint": null,
            "OnBuild": null,
            "Labels": {}
...
```

<p>
Do the values of properties 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
Target</span>, 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
Destination</span> and 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
WorkingDir</span> suggest any relationship to
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
WORKDIR /flask_restx_demo</span> in 
<span class="keyword">
Dockerfile</span>?
</p>

<p>
We discuss 
</p>

```javascript
"Source": "/var/lib/docker/volumes/datavolume/_data",
```

<p>
in the next section <a href="#docker-volumes-on-disk">Docker volumes on disk</a>.
</p>


<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="docker-volumes-on-disk">Docker volumes on disk</a>
</h4>

<p>
On 
<span class="keyword">
Windows 10</span>, 
<span class="keyword">
Docker Desktop</span> lists volumes, and individual volume data as
per screen capture below:
</p>

![033-02-docker-desktop-volume.png](https://behainguyen.files.wordpress.com/2022/07/033-02-docker-desktop-volume.png)

<p style="clear:both;">
List volumes using 
<span class="keyword">
CLI</span>:
</p>

```
D:\>docker volume ls
```

<p>
At the time of this post, there was only one:
</p>

```
D:\>docker volume ls
DRIVER    VOLUME NAME
local     datavolume
```

<p>
We can inspect the a volume to get more detail on it, with:
</p>

```
D:\>docker volume inspect datavolume
```

```javascript
[
    {
        "CreatedAt": "2022-07-28T13:33:51Z",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/datavolume/_data",
        "Name": "datavolume",
        "Options": null,
        "Scope": "local"
    }
]
```

<p>
I didn't understand what property
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
Mountpoint</span> is about, only that it is a 
<span class="keyword">
Unix</span> path:
</p>

```javascript
"Mountpoint": "/var/lib/docker/volumes/datavolume/_data",
```

<p>
The answer provided by user <a href="https://stackoverflow.com/users/1709793/craftsmannadeem"
title="craftsmannadeem" target="_blank">craftsmannadeem</a>
in 
<a href="https://stackoverflow.com/questions/43181654/locating-data-volumes-in-docker-desktop-windows"
title="Locating data volumes in Docker Desktop (Windows)"
target="_blank">Locating data volumes in Docker Desktop (Windows)</a> 
helps me. But within 
<span class="keyword">
WSL 2</span>, under  
<span class="keyword">
root</span> privilege, I don't see anything under
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
/mnt/wsl/docker-desktop-data/</span>, please see screen capture below:
</p>

![033-03-wsl-docker-desktop-data.png](https://behainguyen.files.wordpress.com/2022/07/033-03-wsl-docker-desktop-data.png)

<p style="clear:both;">
However, if I paste this 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
\\wsl$\docker-desktop-data\version-pack-data\community\docker</span>
to
<span class="keyword">
Windows File Explorer</span>, I can see its content:
</p>

![033-04-wsl-docker-desktop-data-explorer.png](https://behainguyen.files.wordpress.com/2022/07/033-04-wsl-docker-desktop-data-explorer.png)

<p style="clear:both;">
-- Are 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
/mnt/wsl/docker-desktop-data/</span> and
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
\\wsl$\docker-desktop-data\</span> referring to the same location? 
<strong>Or am I barking up the wrong tree?</strong>
</p>

<p>
Drill down to 
<span class="keyword">
<strong>volumes</strong></span> | 
<span class="keyword">
<strong>datavolume</strong></span> | 
<span class="keyword">
<strong>_data</strong></span>, the entries are somewhat similar to
those displayed in <span class="keyword">
Docker Desktop</span> above:
</p>

![033-05-wsl-docker-desktop-data-explorer.png](https://behainguyen.files.wordpress.com/2022/07/033-05-wsl-docker-desktop-data-explorer.png)

<p style="clear:both;">
The data entries in 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
flask_restx_demo.db</span> match those retrieved by 
<span class="keyword">
Swagger UI</span>.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="docker-volumes-linux-arm64">Docker volumes on Synology DS218 ( linux/arm64 )</a>
</h3>

<p>
I've already had the image 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
flask-restx-demo-arm64</span> loaded in the post mentioned at the beginning:
</p>

![033-06-ds218-existing-images.png](https://behainguyen.files.wordpress.com/2022/07/033-06-ds218-existing-images.png)

<p style="clear:both;">
Run it:
</p>

```
$ sudo docker run --network=host --mount source=datavolume,target=/flask_restx_demo -v "/run/docker.sock:/var/run/docker.sock" --rm flask-restx-demo-arm64
```

<p>
To recap, the 
<span class="keyword">
Swagger UI</span> URL is 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
http://omphalos-nas-01:8000/api/v1/ui</span>; the test client page is 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
http://localhost/work/TreeAPIClient.html</span>, where the 
<strong>API URL</strong> is  
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
http://omphalos-nas-01:8000/api/v1/trees</span>.
</p>

<p>
Let's inspect the volume:
</p>

```
$ sudo docker volume inspect datavolume
```

<p>
We've seen similar output in the previous section:
</p>

```javascript
[
    {
        "CreatedAt": "2022-07-26T11:13:59+10:00",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/volume1/docker/volumes/datavolume/_data",
        "Name": "datavolume",
        "Options": null,
        "Scope": "local"
    }
]
```

<p>
We're interested in 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
Mountpoint</span> as before:
</p>

```javascript
"Mountpoint": "/volume1/docker/volumes/datavolume/_data",
```

<p>
Where does 
 <span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
/volume1/docker</span> come from? Please see 
<a href="https://behainguyen.wordpress.com/2022/07/20/synology-ds218-unsupported-docker-installation-and-usage/#install-step-08"
title="Synology DS218: unsupported Docker installation and usage… | Mount more disk space"
target="_blank">Synology DS218: unsupported Docker installation and usage… | Mount more disk space</a> 
-- basically, it's
<span class="keyword">
Docker</span>'s root folder which I've manually configured.
</p>

<p>
Let's see the 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
Mountpoint</span> content:
</p>

![033-07-ds218-docker-volume.png](https://behainguyen.files.wordpress.com/2022/07/033-07-ds218-docker-volume.png)

<p style="clear:both;">
The entries are similar to those in 
<span class="keyword">
Windows 10 Pro</span> -- but the directory path is much easier to 
understand and to locate 🙈
</p>

<p>
The 
<span class="keyword">
Portainer</span> administrative UI also shows volume entries:
</p>

![033-08-ds218-docker-volume.png](https://behainguyen.files.wordpress.com/2022/07/033-08-ds218-docker-volume.png)

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="volume-or-mount-option">--volume / -v or --mount option?</a>
</h3>

<p>
This official document 
<a href="https://docs.docker.com/engine/reference/commandline/run/"
title="docker run" target="_blank">docker run</a>, section 
<strong><em>Add bind mounts or volumes using the --mount flag</em></strong>, 
states:
</p>

> Even though there is no plan to deprecate --volume, usage of --mount is recommended.

<p>
Personally, I find  
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
--mount</span> much clearer than 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
-v / --volume</span>. I'll be using the 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
--mount</span> option from now on.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="concluding-remarks">Concluding remarks</a>
</h3>

<p>
I do hope I haven't made any mistakes in this post.
</p>

<p>
I do also understand that the issues discussed in this post are only 
<span class="keyword">
Docker volume</span>'s basics. I did read through the official documents,
but they are not registered yet.
</p>

<p>
Thank you for reading... and I hope you find this post of some helps.
</p>
