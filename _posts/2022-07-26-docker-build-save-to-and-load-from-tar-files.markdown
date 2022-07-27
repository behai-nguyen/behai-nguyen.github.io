---
layout: post
title: "Python: Docker image build -- save to and load from *.tar files."

---

We can save Docker images to local *.tar files, and later load and run those Docker images from local *.tar files. I'm documenting my learning experimentations in this post.

| ![032-feature-image.png](https://behainguyen.files.wordpress.com/2022/07/032-feature-image.png) |
|:--:|
| *Python: Docker image build -- save to and load from *.tar files.* |

<p>
I'm aware that we can create a 
<span class="keyword">
local registry</span> and push 
<span class="keyword">
Docker images</span> into this 
<span class="keyword">
registry</span> instead of the public ones. I like local files, I'm
exploring this option first.
</p>

<p>
The code used in this post is the exact code developed for 
<a href="https://behainguyen.wordpress.com/2022/07/25/python-docker-image-build-the-werkzeug-problem-%f0%9f%a4%96/"
title="Python: Docker image build -- “the Werkzeug” problem 🤖!"
target="_blank">Python: Docker image build -- “the Werkzeug” problem 🤖!</a>
It can be cloned with:
</p>

```
git clone -b v1.0.2 https://github.com/behai-nguyen/flask-restx-demo.git
```

<p>
<strong>Please note</strong>, in this post, all 
<span class="keyword">
Docker images</span> are built on 
<span class="keyword"> Windows 10 Pro</span>.
</p>

<!--------------------------------------------------------------------------------->

<h2>Table of contents</h2>

<ul>
	<li style="margin-top:5px;"><a href="#environments">Environments</a></li>
	
	<li style="margin-top:10px;"><a href="#build-save-windows-images">Build and Save Windows images</a></li>
	
	<li style="margin-top:10px;"><a href="#build-save-linux-arm64-images">Build and Save linux/arm64 images</a></li>
	
	<li style="margin-top:10px;"><a href="#load-run-windows-images">Load and run Windows images</a>
		<ol>
			<li style="margin-top:10px;"><a href="#load-run-windows-image-id">flask_restx_demo-win-by-id.tar</a></li>

			<li style="margin-top:10px;"><a href="#load-run-windows-image-tag">flask_restx_demo-win-by-name.tar</a></li>
		</ol>
	</li>

	<li style="margin-top:10px;"><a href="#load-run-linux-arm64-image">Load and run linux/arm64 image on Synology DS218</a></li>
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
  <a id="build-save-windows-images">Build and Save Windows images</a>
</h3>

<p>
Please see also this official document  
<a href="https://docs.docker.com/engine/reference/commandline/save/"
title="docker save" target="_blank">docker save</a>.
</p>

<p>
To make it clean, I also removed all related containers and images 
before testing.
</p>

<p>
❶ Build as normal:
</p>

```
F:\flask_restx_demo\>docker build --tag flask-restx-demo .
```

<p>
We can save images by using 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
standard output redirection ></span> or by the
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
--output</span> option. Images can be identified by their 
<span class="keyword">
names</span>, i.e. the values in the 
<span class="keyword">
REPOSITORY</span> column when listing images, or by their 
<span class="keyword">
Ids</span>.
</p>

<p>
❷ Save by 
<span class="keyword">
image name</span>:
</p>

```
F:\flask_restx_demo\>docker save flask-restx-demo > E:\docker-images\flask_restx_demo-win-by-name.tar
```

<p>
❸ Save by 
<span class="keyword">
image Id</span>: 
</p>

<p>
<span class="keyword">
Images' Ids</span> can be obtained via command:
</p>

```
docker images
```

<p>
Saving the same image using its 
<span class="keyword">
Id</span> and 
<span class="keyword">
--output</span></span> option:
</p>

```
F:\flask_restx_demo\>docker save 1bbe6c6752a2 --output E:\docker-images\flask_restx_demo-win-by-id.tar
```

<p>
The 
<span class="keyword">
docker save</span> command does not seem to print out anything:
</p>

![031-01-windows-windows-save-to-files-a.png](https://behainguyen.files.wordpress.com/2022/07/031-01-windows-windows-save-to-files-a.png)

<p style="clear:both;">
The two ( 2 ) output files and their sizes. Please note the slight
difference in sizes:
</p>

![031-01-windows-windows-save-to-files-b.png](https://behainguyen.files.wordpress.com/2022/07/031-01-windows-windows-save-to-files-b.png)

<p style="clear:both;"></p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="build-save-linux-arm64-images">Build and Save linux/arm64 images</a>
</h3>

<p>
We've previously discussed how to prepare for and to build 
<span class="keyword">
multi-arch</span> images on 
<span class="keyword">
Windows 10 Pro</span>. Please see 
<a href="https://behainguyen.wordpress.com/2022/07/20/synology-ds218-unsupported-docker-installation-and-usage/#test-installation" 
title="Synology DS218: unsupported Docker installation and usage... | Test installation"
target="_blank">Synology DS218: unsupported Docker installation and usage... | Test installation</a> -- 
points ❶ and ❸.
</p>

<p>
Basically, to prepare 
<span class="keyword">
multi-arch</span> build profile
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
mybuilder</span>, run:
</p>

```
C:\>docker buildx create --name mybuilder --driver-opt network=host --use
```

<p>
Then to build, and to push to 
<a href="https://hub.docker.com/" title="https://hub.docker.com/" target="_blank">https://hub.docker.com/</a>
after finishing building:
</p>

```
F:\some_project>docker buildx build --platform linux/arm64 --tag username/some-project --push .
```

<p>
❶ Try building an image for 
<span class="keyword">
linux/arm64</span> only, that is, do not push the image onto the registry
afterward:
</p>

```
F:\flask_restx_demo>docker buildx build --platform linux/arm64 --tag flask-restx-demo-arm64 .
```

<p>
No image loaded: this should make sense, since this build is for 
<span class="keyword">
linux/arm64</span> not 
<span class="keyword">
Windows</span>.
</p>

<p>
While research for the problem, I found this post 
<a href="https://github.com/docker/buildx/issues/166"
title="Where did the built multi-platform image go? #166" 
target="_blank">Where did the built multi-platform image go? #166</a>,
answers by user 
<a href="https://github.com/barcus" title="barcus" target="_blank">barcus</a>
provide the solution.
</p>

<p>
❷ To build and to save locally:
</p>

```
F:\flask_restx_demo>docker buildx build --platform linux/arm64 --output "type=docker,push=false,name=flask-restx-demo-arm64,dest=E:\docker-images\flask-restx-demo-arm64.tar" .
```

<p>
Image file 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
E:\docker-images\flask-restx-demo-arm64.tar</span>, its size is 
less than half of the previous two ( 2 ):
</p>

![031-02-windows-linux-arm64-save-to-files.png](https://behainguyen.files.wordpress.com/2022/07/031-02-windows-linux-arm64-save-to-files.png)

<p style="clear:both;"></p>

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="load-run-windows-images">Load and run Windows images</a>
</h3>

<p>
Please see also this official document  
<a href="https://docs.docker.com/engine/reference/commandline/load/"
title="docker load" target="_blank">docker load</a>.
</p>

<p>
The two image files 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
flask_restx_demo-win-by-id.tar</span> and 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
flask_restx_demo-win-by-name.tar</span> should be the same. 
I'm testing them both anyway.
</p>

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="load-run-windows-image-id">flask_restx_demo-win-by-id.tar</a>
</h4>

<p>
❶ Start clean. Remove any existing related containers and images.
</p>

<p>
❷ To load an image file, use:
</p>
 
```
F:\>docker load --input E:\docker-images\flask_restx_demo-win-by-id.tar
```

<p>
The loaded image has the same 
<span class="keyword">
Id</span> with the original image's: 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
1bbe6c6752a2</span> -- please see the screen capture below:
</p>

![031-03-load-win-image-by-id-on-windows.png](https://behainguyen.files.wordpress.com/2022/07/031-03-load-win-image-by-id-on-windows.png)

<p style="clear:both;">
Since the loaded image does not have an
<span class="keyword">
image name</span> assigned, we have to run it via its 
<span class="keyword">
image Id</span>.
</p>

<p>
❸ Run the loaded image by its 
<span class="keyword">
Id</span>:
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
1bbe6c6752a2</span>
</p>

```
F:\>docker run --publish 8000:8000 --rm 1bbe6c6752a2
```

<p>
We run it in none detached mode, that is, without option 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
-d</span>, so that we can see the output on command line screen:
</p>

![031-04-run-win-image-by-id-on-windows.png](https://behainguyen.files.wordpress.com/2022/07/031-04-run-win-image-by-id-on-windows.png)

<p style="clear:both;"></p>

<p>
❹ We can access the 
<span class="keyword">
container</span> via the following URLs:
</p>

<p>Swagger UI URL:</p>

```
http://localhost:8000/api/v1/ui
```

<p>API URL:</p>

```
http://localhost:8000/api/v1/trees
```

<!--------------------------------------------------------------------------------->
<h4 style="color:teal;">
  <a id="load-run-windows-image-tag">flask_restx_demo-win-by-name.tar</a>
</h4>

<p>
❶ Start clean. Stop and remove previous test container.
</p>

<p>
❷ Remove any existing related images.
</p>

<p>
❸ To load:
</p>

```
F:\>docker load --input E:\docker-images\flask_restx_demo-win-by-name.tar
```

<p>
This time, the loaded image has both 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
REPOSITORY</span> and 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
TAG</span> properties defined:
</p>

![031-05-load-win-image-by-tag-on-windows.png](https://behainguyen.files.wordpress.com/2022/07/031-05-load-win-image-by-tag-on-windows.png)

<p style="clear:both;">
❹ Run the loaded image with a different port to the previous run
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
--publish 9010:8000</span>: 
</p> 

```
F:\>docker run --publish 9010:8000 --rm flask-restx-demo
```

<p>
❺ As before, we can access the 
<span class="keyword">
container</span> via the following URLs, please note the 
<strong>port</strong>:
</p> 

```
http://localhost:9010/api/v1/ui
http://localhost:9010/api/v1/trees
```

<!--------------------------------------------------------------------------------->
<h3 style="color:teal;">
  <a id="load-run-linux-arm64-image">Load and run linux/arm64 image on Synology DS218</a>
</h3>

<p>
Recall from section 
<a href="#build-save-linux-arm64-images">Build and Save linux/arm64 images</a>,
the image file has been saved to 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
E:\docker-images\flask-restx-demo-arm64.tar</span>.
</p>

<p>
❶ On the 
<span class="keyword">
Synology DS218</span> box, start the 
<span class="keyword">
Docker daemon</span> if not already started:
</p>

```
$ sudo dockerd &
```

<p>
❷ Start clean. On the 
<span class="keyword">
Synology DS218</span> box, remove all related containers and images.
</p> 

<p>
❸ Copy 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
E:\docker-images\flask-restx-demo-arm64.tar</span> to
<span class="keyword">
Synology DS218</span> box's 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
$HOME/Test/</span>.
</p> 

<p>
❹ Load the image file with:
</p> 

```
behai@omphalos-nas-01:~/Test$ sudo docker load --input flask-restx-demo-arm64.tar
```

<p>
The image loads successfully, please see verifications in the screen capture below:
</p>

![031-06-load-linux-arm64-on-ds218.png](https://behainguyen.files.wordpress.com/2022/07/031-06-load-linux-arm64-on-ds218.png)

<p style="clear:both;">
❺ Run the loaded image with:
</p>

```
behai@omphalos-nas-01:~/Test$ sudo docker run --network=host -v "/run/docker.sock:/var/run/docker.sock" --rm flask-restx-demo-arm64
```

<p>
It runs successfully:
</p>

![031-07-run-linux-arm64-on-ds218.png](https://behainguyen.files.wordpress.com/2022/07/031-07-run-linux-arm64-on-ds218.png)

<p style="clear:both;">
❻ As before, we can access the 
<span class="keyword">
container</span> via the following URLs from 
<span class="keyword">
Windows 10 Pro</span>:
</p> 

```
http://omphalos-nas-01:8000/api/v1/ui
http://omphalos-nas-01:8000/api/v1/trees
```

<p>
<strong>Please note</strong>, the repo now includes a test 
<span class="keyword">HTML</span>
page using 
<span class="keyword">JQuery</span> 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
test_client_app\jquery-ajax\TreeAPIClient.html</span>, 
just copy it to a web site or a virtual web directory, and run it from there, for
<strong>API URL</strong> use 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
http://omphalos-nas-01:8000/api/v1/trees</span>.
</p>

<p>✿✿✿</p>

<p>
I do enjoy learning and blogging about this feature of
<span class="keyword">
Docker</span>, I find this feature very useful... Thank you for reading, 
and I hope you find the info in this post useful also.
</p>
