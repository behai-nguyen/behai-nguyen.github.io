---
layout: post
title: "Synology DS218: unsupported Docker installation and usage..."

---

Synology does not have Docker support for AArch64 NAS models. DS218 is an AArch64 NAS model. In this post, we're looking at how to install Docker for unsupported Synology DS218, and we're also conducting tests to prove that the installation works.

| ![029-feature-image.png](https://behainguyen.files.wordpress.com/2022/07/029-feature-image.png) |
|:--:|
| *Synology DS218: unsupported Docker installation and usage...* |

<div style="background-color:yellow;width:100%;height:100px;">
    <div style="float:left;width:100px;height:100px;
	    background-image: url('https://behainguyen.files.wordpress.com/2022/07/danger-2324940__340.png'); 
        background-repeat: no-repeat; 
		background-position: center center; 
        background-size: 80px 80px;">
    </div>
	
	<div style="float:right;width:570px;">
	    <ul style="font-weight:bold;color:red;padding-right:40px;">
            <li style="margin-top:5px;">I take no responsibilities for any damages or losses resulting from applying the procedures outlined in this post. </li>
            <li style="margin-top:10px;">Damages and losses include both hardware, software and data.</li>
	    </ul>	
	</div>
</div>

<p style="clear:both;"></p>

<!--------------------------------------------------------------------------------->

<h2>Table of contents</h2>

<ul>
	<li><a href="#environments">Environments</a></li>
	
	<li><a href="#aarch64-and-arm64">AArch64 and ARM64</a></li>
	
	<li><a href="#references">References</a></li>
	
	<li><a href="#installation-steps">Installation steps</a>
		<ol>
			<li><a href="#install-step-01">Download binary</a></li>

			<li><a href="#install-step-02">Extract content</a></li>

			<li><a href="#install-step-03">Copy extracted content to /usr/bin/</a></li>

			<li><a href="#install-step-04">Create the file /etc/docker/daemon.json</a></li>
			
			<li><a href="#install-step-05">Run the Docker daemon</a></li>			

			<li><a href="#install-step-06">Run the Portainer administrative UI</a></li>

			<li><a href="#install-step-07">A test build</a></li>
			
			<li><a href="#install-step-08">Mount more disk space</a></li>

			<li><a href="#install-step-09">Run the Docker daemon and Portainer UI</a></li>

			<li><a href="#install-step-10">Re-run the same build again</a></li>
		</ol>
	</li>

	<li><a href="#test-installation">Test installation</a>
		<ol>

			<li><a href="#test-install-01">Create a multi-arch build profile</a></li>

			<li><a href="#test-install-02">Clean up https://hub.docker.com/repositories</a></li>

			<li><a href="#test-install-03">Build image behai/python-docker for linux/arm64 platform and push it to https://hub.docker.com/repositories</a></li>
			
			<li><a href="#test-install-04">Test the image on Synology DS218</a></li>

			<li><a href="#test-install-05">Other commands</a></li>
		</ol>
	</li>
	
	<li><a href="#pending-issues">Pending issues</a></li>	

	<li><a href="#concluding-remarks">Concluding remarks</a></li>
</ul>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="environments">Environments</a>
</h3>

<ol>
<li style="margin-top:5px;">
<span class="keyword"> DSM 7.1-42661 Update 3</span>.
</li>

<li style="margin-top:10px;">
<span class="keyword"> Windows 10 Pro</span> -- <span class="keyword"> version 10.0.19044 build 19044</span>.
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
  <a id="aarch64-and-arm64">AArch64 and ARM64</a>
</h3>

<p>
The two terms refer to the same CPU architecture. Please see:
</p>

<ol>
<li style="margin-top:5px;">
<a href="https://www.instana.com/blog/the-future-is-now-arms-aarch64-on-the-rise-with-instana/" title="The Future Is Now; ARM’s AARCH64 on the Rise – with Instana" target="_blank">The Future Is Now; ARM’s AARCH64 on the Rise – with Instana</a>
</li>

<li style="margin-top:10px;">
<a href="https://en.wikipedia.org/wiki/AArch64" title="AArch64" target="_blank">Wikipedia -- AArch64</a>
</li>

<li style="margin-top:10px;">
<a href="https://en.wikipedia.org/wiki/ARM_architecture_family#ARMv8-A" title="ARM architecture family" target="_blank">Wikipedia -- ARM architecture family</a>
</li>
</ol>

<p>
<span class="keyword"> SSH</span> into <span class="keyword"> Synology NAS</span> box and run the following two ( 2 ) commands to get the processor and architecture:
</p>

```
$ cat /proc/cpuinfo | grep "model name" | uniq
$ uname -m
```

<p>
My unit gives the following two ( 2 ) outputs respectively:
</p>

```
model name      : ARMv8 Processor rev 4 (v8l)
aarch64
```

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="references">References</a>
</h3>

<p>
There're plenty of posts which assert that <span class="keyword"> Docker</span> does support <span class="keyword"> AArch64</span>, and it should be possible to install <span class="keyword"> Docker</span> on <span class="keyword"> Synology</span> models which use <span class="keyword"> AArch64</span>.
</p>

<ol>
<li style="margin-top:5px;">
<a href="https://wiki.servarr.com/docker-arm-synology" title="Installing Docker on a Synology ARM NAS" target="_blank">Installing Docker on a Synology ARM NAS</a> -- not my principal reference, I did not act on its instructions, but it does have some valuable information.
</li>

<li style="margin-top:10px;">
<a href="https://stackoverflow.com/questions/52520008/can-i-install-docker-on-arm8-based-synology-nas" title="Can I install Docker on arm8 based Synology Nas" target="_blank">Can I install Docker on arm8 based Synology Nas</a> -- <strong>this is the principal post</strong>, I follow the instructions given by user <a href="https://stackoverflow.com/users/6067276/hikariii" title="Hikariii" target="_blank">Hikariii</a> to carry out the installation.
</li>

<li style="margin-top:10px;">
<a href="https://salesjobinfo.com/multi-arch-container-images-for-docker-and-kubernetes/" title="Multi-arch container images for Docker and Kubernetes" target="_blank">Multi-arch container images for Docker and Kubernetes</a> -- I use instructions in section <i>“Modern multi-arch docker image build process with BuildKit (buildx)”</i> to build a <span class="keyword"> Docker image</span> for <span class="keyword"> <strong>linux/arm64</strong></span> platform, and use this image to test the installation.
</li>
</ol>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="installation-steps">Installation steps</a>
</h3>

<p>
<span class="keyword"> SSH</span> into <span class="keyword"> Synology DS218</span> to use command line.
</p>

<p>
❶ <a id="install-step-01">Download binary</a>. From <a href="https://download.docker.com/linux/static/stable/aarch64/" title="Index of linux/static/stable/aarch64/" target="_blank">https://download.docker.com/linux/static/stable/aarch64</a>, manually download the latest <span class="keyword"> Docker binary</span>, which is <span class="keyword"> docker-20.10.9.tgz</span> to <span class="keyword"> DS218</span> <span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">$HOME</span> directory.
</p>

<p>
❷ <a id="install-step-02">Extract content</a>. Run the following commands:
</p>

```
$ cd $HOME
$ tar xzvf docker-20.10.9.tgz
```

<p>

❸ <a id="install-step-03">Copy extracted content to <span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">/usr/bin/</span></a>:
</p>

```
$ sudo cp docker/* /usr/bin/
```

<p>
( I'm just being pedantic! ) Verify copy. Based on the content of extracted directory, <span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">$HOME/docker/</span>, verify files've been copied to <span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">/usr/bin/</span> with:
</p>

```
$ ls -l /usr/bin/containerd
$ ls -l /usr/bin/containerd-shim
$ ls -l /usr/bin/containerd-shim-runc-v2
$ ls -l /usr/bin/ctr
$ ls -l /usr/bin/docker
$ ls -l /usr/bin/dockerd
$ ls -l /usr/bin/docker-init
$ ls -l /usr/bin/docker-proxy
$ ls -l /usr/bin/runc
```

<p>
❹ <a id="install-step-04">Create the file <span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">/etc/docker/daemon.json</span></a>. We'll need to do this via <span class="keyword"> sudo</span>.
</p>

```
File /etc/docker/daemon.json
```

```json
{
  "storage-driver": "vfs",
  "iptables": false,
  "bridge": "none"
}
```

<p>
❺ <a id="install-step-05">Run the <span class="keyword">Docker daemon</span></a>:
</p>

```
$ sudo dockerd &
```

<p>
The output is very long, around 81 ( eighty one ) lines... There're a lot warnings, but the <span class="keyword"> daemon</span> does run.
</p>

<p>
❻ <a id="install-step-06">Run the <span class="keyword"> Portainer</span> administrative UI</a>. Based on <a href="https://raw.githubusercontent.com/wdmomoxx/catdriver/master/install-docker.sh" title="Docker automatic script" target="_blank">https://raw.githubusercontent.com/wdmomoxx/catdriver/master/install-docker.sh</a>, run:
</p>

```
$ sudo docker run -d --network=host -v "/run/docker.sock:/var/run/docker.sock" portainer/portainer:linux-arm64
```

<p>
This <span class="keyword"> Portainer</span> is listening on port <span class="keyword"> 9000</span>. On <span class="keyword"> Windows 10</span>, run a web browser with:
</p>

```
http://omphalos-nas-01:9000
```

<p>
We'll get the following screen:
</p>

![029-01-portainer.png](https://behainguyen.files.wordpress.com/2022/07/029-01-portainer.png)

<p style="clear:both;">
Create the <span class="keyword"> admin user</span> as required. We'll get logged in:
</p>

![029-02-portainer.png](https://behainguyen.files.wordpress.com/2022/07/029-02-portainer.png)

<p style="clear:both;">
Select the <span class="keyword"> <strong>Local</strong></span> tab, then click on the <span class="keyword"> <strong>Connect</strong></span> button on the bottom left hand corner: this <span class="keyword"> Portainer</span> UI is now connected to <span class="keyword"> Docker</span> on my <span class="keyword"> Synology DS218</span> box. This <span class="keyword"> Portainer</span> UI looks very similar to the <span class="keyword"> Docker Desktop</span> on <span class="keyword"> Windows 10</span>.
</p>

<p>
❼ <a id="install-step-07">A test build</a>. I didn't expect it to work. Recall, user <a href="https://stackoverflow.com/users/6067276/hikariii" title="Hikariii" target="_blank">Hikariii</a> mentions in <a href="https://stackoverflow.com/questions/52520008/can-i-install-docker-on-arm8-based-synology-nas" title="Can I install Docker on arm8 based Synology Nas" target="_blank">Can I install Docker on arm8 based Synology Nas</a>:
</p>

>you can easily run out of space for docker since the default dsm / mount is only 2GB, to prevent this you can create a docker folder on your volume, mount it to /docker and set it as data-root:
>...

<p>
Build a simple <span class="keyword"> Python</span> image:
</p>

```
behai@omphalos-nas-01:/var/services/web/app_demo$ sudo docker build --tag app-demo .
```

```
Password:
Sending build context to Docker daemon  19.97kB
Step 1/6 : FROM python:3.8-slim-buster
3.8-slim-buster: Pulling from library/python
...
Status: Downloaded newer image for python:3.8-slim-buster
 ---> 9f30b95a0f37
Step 2/6 : WORKDIR /app_demo
no space left on device
behai@omphalos-nas-01:/var/services/web/app_demo$
```

<p>
This last error was <span class="keyword"> <strong>no space left on device</strong></span>.
</p>

<p>
❽ <a id="install-step-08">Mount more disk space</a>.
</p>

<p>
⓵ Use <span class="keyword"> “File Station”</span> to create <span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">docker/</span> directory, and give it 10 GB.
</p>

<p>
⓶ This directory is <span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">/volume1/docker</span>
</p>

<p>
⓷ Mount <span class="keyword"> Docker</span> volume:
</p>

```
$ cd $HOME
$ sudo mkdir -p /volume1/@Docker/lib
$ sudo mount -o bind "/volume1/@Docker/lib" /volume1/docker
```

<p>
⓸ Modified <span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">/etc/docker/daemon.json</span> -- add <span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">{ "data-root": "/volume1/docker" }</span>:
</p>

```
File /etc/docker/daemon.json
```

```json
{
  "storage-driver": "vfs",
  "iptables": false,
  "bridge": "none",
  "data-root": "/volume1/docker"
}
```

<p>
Please note, at this point, <span class="keyword"> Portainer</span> administrative UI showed around five to six ( 5 to 6 ) entries for <span class="keyword"> Volumes</span>, one ( 1 ) was used by the <span class="keyword"> Portainer</span> container itself. Except for the <span class="keyword"> Portainer volume</span>, I manually removed all those others.
</p>

<p>
⓹ Restart the <span class="keyword"> DS218</span> box.
</p>

<p>
❾ <a id="install-step-09">Then run the <span class="keyword"> Docker daemon</span> and <span class="keyword"> Portainer</span> UI</a> with:
</p>

```
$ sudo dockerd &
$ sudo docker run -d --network=host -v "/run/docker.sock:/var/run/docker.sock" portainer/portainer:linux-arm64
```

<p>
It seemed to download the <span class="keyword"> Portainer</span> image again. <span class="keyword"> Portainer's Volumes</span> now shows:
</p>

![029-03-portainer.png](https://behainguyen.files.wordpress.com/2022/07/029-03-portainer.png)

<p style="clear:both;">
❿ <a id="install-step-10">Re-run the same build again</a>, the error <span class="keyword"> <strong>no space left on device</strong></span> has gone away. But there're still a lot of other errors which I can't solve yet:
</p>

![029-04-docker-build-app-demo.png](https://behainguyen.files.wordpress.com/2022/07/029-04-docker-build-app-demo.png)

<p style="clear:both;"></p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="test-installation">Test installation</a>
</h3>

<p>
I've attempted several fixes to get the build going on the <span class="keyword"> Synology DS218</span> box, I can't yet find a solution. I'm sleeping on it for the time being. <span class="keyword"> Docker CLI</span> and <span class="keyword"> Docker Desktop</span> are fully functional on my <span class="keyword"> Windows 10</span>, so I thought I would build images on <span class="keyword"> Windows 10</span>, push them onto <a href="https://hub.docker.com/repositories" title="Docker hub repositories" target="_blank">Docker hub repositories</a>, and then run these images on <span class="keyword"> Synology DS218</span>. The followings are what I've tried.
</p>

<p>
For this test build, I'm using the <a href="https://docs.docker.com/language/python/build-images/" title="Build your Python image" target="_blank">Build your Python image </a> tutorial -- the <span class="keyword"> Python</span> project is simpler than the <span class="keyword"> app_demo</span> project I use in the previous section. Note, since the project is simple, I didn't do <span class="keyword"> Flask</span> install, but constructed <span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">requirements.txt</span> manually. The project layout looks like this:
</p>

```
f:\python_docker
|
|-- app.py
|-- Dockerfile
|-- requirements.txt
```

```
File f:\python_docker\app.py
```

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Docker!'
```

```
File f:\python_docker\Dockerfile
```

```
# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=9880"]
```

```
File f:\python_docker\requirements.txt
```

```
Flask==2.1.3
```

<p>
I don't want to repeat my failed attempts. In short, I just tried whatever that popped into my head that seemed logical: none worked. Based on the errors, I did some searches, and eventually found this post <a href="https://salesjobinfo.com/multi-arch-container-images-for-docker-and-kubernetes/" title="Multi-arch container images for Docker and Kubernetes" target="_blank">Multi-arch container images for Docker and Kubernetes</a> -- The relevant section is <i>“Modern multi-arch docker image build process with BuildKit (buildx)”</i>:
</p>

<p>
❶ <a id="test-install-01">Create a <span class="keyword"> multi-arch build profile</span></a>. On <span class="keyword"> Windows 10</span>, run:
</p>

```
F:\python_docker>docker buildx create --name mybuilder --driver-opt network=host --use
```

<p>
Then inspect it:
</p>

```
F:\python_docker>docker buildx inspect --bootstrap
```

<p>My output:</p>

```
[+] Building 90.9s (1/1) FINISHED
 => [internal] booting buildkit                                                                                                                                                                            90.0s
 => => pulling image moby/buildkit:buildx-stable-1                                                                                                                                                         86.3s
 => => creating container buildx_buildkit_mybuilder0                                                                                                                                                        3.7s
Name:   mybuilder
Driver: docker-container

Nodes:
Name:      mybuilder0
Endpoint:  npipe:////./pipe/docker_engine
Status:    running
Platforms: linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/arm64, linux/riscv64, linux/ppc64le, linux/s390x, linux/386, linux/mips64le, linux/mips64, linux/arm/v7, linux/arm/v6

F:\python_docker>
```

<p>
❷ <a id="test-install-02">Clean up <span class="keyword"> https://hub.docker.com/repositories</span></a>. Delete <span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">behai/python-docker</span> image from <a href="https://hub.docker.com/repositories" title="Docker hub repositories" target="_blank">https://hub.docker.com/repositories</a> -- if exists.
</p>

<p>
❸ <a id="test-install-03">Build image <span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">behai/python-docker</span> for <span class="keyword"> linux/arm64 platform</span> and push it to <span class="keyword"> https://hub.docker.com/repositories</span></a>.
</p>

<p>
⓵ On <span class="keyword"> Windows 10</span> command prompt, log into <span class="keyword"> https://hub.docker.com</span> with:
</p>

```
F:\python_docker>docker login
```

<p>
⓶ Now run the build and push:
</p>

```
F:\python_docker>docker buildx build --platform linux/arm64 --tag behai/python-docker --push .
```

<p>
My successful output looks like the screen capture below:
</p>

![029-05-docker-buildx-build.png](https://behainguyen.files.wordpress.com/2022/07/029-05-docker-buildx-build.png)

<p style="clear:both;">
The image <span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">behai/python-docker</span> should now be pushed onto <span class="keyword"> https://hub.docker.com/repositories</span> -- we should verify that it's there.
</p>

<p>
❹ <a id="test-install-04">Test the image on <span class="keyword"> Synology DS218</span></a>.
</p>

<p>
⓵ On <span class="keyword">Synology DS218</span> command line, run:
</p>

```
$ sudo docker run -d --network=host -v "/run/docker.sock:/var/run/docker.sock" --rm behai/python-docker
```

<p>
It should run successfully, the output is as screen capture below:
</p>

![029-06-docker-run-linux-arm64-01-a.png](https://behainguyen.files.wordpress.com/2022/07/029-06-docker-run-linux-arm64-01-a.png)

<p style="clear:both;">
⓶ On <span class="keyword"> Windows 10</span>, run a web browser with:
</p>

```
http://omphalos-nas-01:9880
```

<p>
It should run with no problem:
</p>

![029-06-docker-run-linux-arm64-01-b.png](https://behainguyen.files.wordpress.com/2022/07/029-06-docker-run-linux-arm64-01-b.png)

<p style="clear:both;">
⓷ When finished testing, looks for <span class="keyword"> Container ID</span> with:
</p>

```
$ sudo docker ps -a
```

<p>
And then stop the target container with:
</p>

```
$ sudo docker container stop <Container ID>
```

<p>
We don't need to remove the container, since the <span class="keyword"> --rm</span> flag'll cause the container to be removed when stopped.
</p>

<p>
⓸ My second test is with <span class="keyword"> app-demo</span> discussed previously. I'll not be listing the build process presently. On the <span class="keyword"> Synology DS218</span> box, run it as:
</p>

```
$ sudo docker run -d --network=host -v "/run/docker.sock:/var/run/docker.sock" --rm behai/app-demo:arm64flask
```

<p style="clear:both;">
On <span class="keyword"> Windows 10</span>, run a web browser also with:
</p>

```
http://omphalos-nas-01:9880
```

<p>
The browser should just display:
</p>

```
Hello, World!
```

<p>
❺ <a id="test-install-05">Other commands</a> from <a href="https://salesjobinfo.com/multi-arch-container-images-for-docker-and-kubernetes/" title="Multi-arch container images for Docker and Kubernetes" target="_blank">Multi-arch container images for Docker and Kubernetes</a>. Run on <span class="keyword"> Windows 10</span>.
</p>

<p>
⓵ Inspect image command.

</p>

```
F:\python_docker>docker buildx imagetools inspect behai/python-docker
```

<p>
I did run this command, it works as described.
</p>

<p>
⓶ Remove the <span class="keyword"> multi-arch build profile</span> created previously:
</p>

```
( F:\python_docker> )docker buildx rm mybuilder
```

<p>
I didn't run the above command. Its offical documentation is at <a href="https://docs.docker.com/engine/reference/commandline/buildx_rm/ " title="docker buildx rm" target="_blank">docker buildx rm</a>.
</p>

<p>
On <span class="keyword"> Windows Docker Desktop</span>, the first screen on start up shows:
</p>

```
buildx_buildkit_mybuilder0 ... RUNNING
```

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="pending-issues">Pending issues</a>
</h3>

<p>
❶ I can't do builds as mentioned previously.
</p>

<p>
❷ While <span class="keyword"> Docker daemon</span> is running, the following warnings pop up on the <span class="keyword"> SSH</span> screen:
</p>

```
WARN[2022-07-15T14:17:35.016826267+10:00] Could not get operating system name: Error opening /usr/lib/os-release: open /usr/lib/os-release: no such file or directory
WARN[2022-07-15T14:17:35.017024230+10:00] Could not get operating system version: Error opening /usr/lib/os-release: open /usr/lib/os-release: no such file or directory
```

```
WARN[2022-07-19T14:25:48.160521974+10:00] seccomp is not enabled in your kernel, running container without default profile
time="2022-07-19T14:25:48.574068043+10:00" level=info msg="starting signal loop" namespace=moby path=/run/docker/containerd/daemon/io.containerd.runtime.v2.task/moby/e9997b732228c64610cdcc9fef2f785225539b47076bcac9b4470f9bac8a7d56 pid=16006
```

<p>
❸ I'm not using <span class="keyword"> Docker</span> everyday, so at the moment, I'm happy to start <span class="keyword"> Docker daemon</span> manually everytime I need to use it.
</p>

<p>
❹ I haven't set up <span class="keyword"> Docker Group</span> as per instructions either. I'm happy to run <span class="keyword"> docker CLI</span> under <span class="keyword"> sudo</span>.
</p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="concluding-remarks">Concluding remarks</a>
</h3>

<p>
On my <span class="keyword"> Synology DS218</span>, <span class="keyword"> Docker</span> is still not fully functional yet. For the time being, I can use <span class="keyword"> Windows 10</span> to build images for <span class="keyword"> AArch64</span> platform, and test these images on the <span class="keyword"> DS218</span> box -- so at least I can use it as a test box.
</p>

<p>
I would like to get rid of the build errors and warnings etc... I'll attempt to work on these -- this will be an ongoing task for me.
</p>

<p>
It has been an interesting learning exercise... I'm happy with the results. I hope you find this post useful, and you can use the information for your own attempt. Thank you for reading and happy <span class="keyword"> Dockering</span> 😂😂😂
</p>