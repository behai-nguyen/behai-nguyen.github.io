---
layout: post
title: "CI/CD #01. Jenkins: manually clone a Python GitHub repo and run Pytest."
description: I'm describing the steps required to manually get Jenkins to -- ⓵ clone a Python project GitHub repository, ⓶ create a virtual environment, ⓷ run editable install, and finally, ⓸ run Pytest for all tests.
tags:
- CICD
- Jenkins
- GitHub
- Python
- pytest
---

*I'm describing the steps required to manually get Jenkins to: ⓵ clone a Python project GitHub repository, ⓶ create a virtual environment, ⓷ run editable install, and finally, ⓸ run Pytest for all tests.*

| ![055-feature-image.png](https://behainguyen.files.wordpress.com/2023/01/055-feature-image.png) |
|:--:|
| *CI/CD #01. Jenkins: manually clone a Python GitHub repo and run Pytest.* |

<em>Manual</em>, in the context of this post, means we have 
to click something on the Jenkins UI to get a build going.

I've installed <a href="https://www.jenkins.io/" title="Jenkins" target="_blank">Jenkins</a>
2.388 LTS on my Ubuntu 22.10. The installation process is pretty straight forward, I'm 
including the installation description in the last part of this post.

Once successfully installed and running, we can access Jenkins front-end at 
<code>http://&lt;machine-ip-address&gt;&lt;machine-name&gt;:8080</code>.
In my case, from 
Windows 10, <code>http://hp-pavilion-15:8080/</code>, or on Ubuntu 22.10 where 
Jenkins is installed, <code>http://localhost:8080</code>.

As usual, I had failed several times before getting my first project going. I am
documenting what I've learned in this post, so it is by no means a tutorial. I'm planning 
to write more on it as I go along, so that is why <em>CI/CD #01</em> is in the title.

I'm going back to this
<a href="https://github.com/behai-nguyen/app-demo.git" title="App Demo" target="_blank">https://github.com/behai-nguyen/app-demo.git</a>
repo for this post. We'll set up a <code>Jenkins</code> project to carry out the four (4) 
steps outlined in the introduction. Let's get to it.

❶ Log into Jenkins using the admin user name and password created as part 
of the installation. Click on <strong>Dashboard</strong> located on top left 
hand side corner; then click on <strong>+ New Item</strong> underneath.

❷ On the next page:

<ul>
<li style="margin-top:10px;">
<strong>Enter an item name</strong>: <code>app_demo</code> -- this name matches the directory 
name of the project. (In hindsight, the name of the repo should've been <code>app_demo</code>
instead of <code>app-demo</code>!)
</li>

<li style="margin-top:10px;">
Then select the first option <code>Freestyle project</code>.
</li>

<li style="margin-top:10px;">
Finally, click on the <code>OK</code> button to move to the <strong>Configure</strong> page.
</li>
</ul>

❸ On the <strong>Configure</strong> page:

<ul>
<li style="margin-top:10px;">
Under <strong>General</strong>, enter something meaningful for 
<code>Description</code>, e.g.: <em>“Try Jenkins on app-demo repo.”</em>
</li>

<li style="margin-top:10px;">
Under <strong>Source Code Management</strong>:
  
  <ul>
	  <li style="margin-top:10px;">
	  Select <code>Git</code>. Then,
	  </li>
	  
	  <li style="margin-top:10px;">
	  For <strong>Repository URL</strong>, enter 
	  <code>https://github.com/behai-nguyen/app-demo.git</code>. Since this 
	  is a public repo, anybody can clone it, we don't need any credential 
	  to access it.
	  </li>
	  
	  <li style="margin-top:10px;">
	  For <strong>Branch Specifier (blank for 'any')</strong>, enter 
	  <code>*/main</code> -- since we are interested in the main branch of 
	  this repo.
	  </li>
  </ul>
</li>

<li style="margin-top:10px;">
Scrolling down, under <strong>Build Steps</strong>, drop down
<strong>Add build step</strong>, then select <code>Execute shell</code>.
Enter the following content:

<pre style="border:1px solid silver;width:95%;padding:1em;margin:10px;font-family:Monaco,Consolas,Menlo,Courier,monospace;font-size:1.2em;overflow-x: scroll;">
PYENV_HOME=$WORKSPACE/venv

# Delete previously built virtualenv
if [ -d $PYENV_HOME ]; then
    rm -rf $PYENV_HOME
fi

# Create virtualenv and install necessary packages
virtualenv $PYENV_HOME
. $PYENV_HOME/bin/activate
$PYENV_HOME/bin/pip install -e .
$PYENV_HOME/bin/pytest
</pre>

<p>
This script starts off by deleting the existing virtual environment; create 
a new one; activate it; then editable install all required packages; finally,
run <code>Pytest</code>.
</p>

<p>
Note, because of how the script works, it can use a lot of data depending on 
how many packages are in the project.
</p>
</li>

<li style="margin-top:10px;">
Finally, click on the <code>Save</code> button to move to the project 
page. The breadcrumb on the top left hand corner should now show 
<code>Dashboard > app_demo ></code>.
</li>
</ul>

❹ Underneath <strong>Dashboard</strong>, the fourth (4th) item is
<code>▷ Build Now</code>. Click on <code>▷ Build Now</code> to build!

With a bit of luck 😂, it should “build” successful, the screen should
look like:

![055-01.png](https://behainguyen.files.wordpress.com/2023/01/055-01.png)

Underneath <strong>Build History</strong>, there is a green tick 
preceding <code>#1</code>, which indicates that 
this build has been successful. In case of a failure, it's 
a red x. In either case, clicking on <code>#1</code>,
will go to the build detail screen, then on the left hand side,
clicking on <code>Console Output</code> will show the full log 
of the build -- which is very informatively rich. On the failure 
ones, I have been able to use the information to get rid of the 
problems.

❺ Let's look at what happens on disk. Jenkins' work directory is
<code>/var/lib/jenkins/workspace/</code>:

![055-02.png](https://behainguyen.files.wordpress.com/2023/01/055-02.png)

<code>app_demo</code> can be seen on top of the list, it has been created by 
Jenkins during the build. It is a ready to use Python development environment.
Let's go to it, and activate the virtual environment: 

```
$ cd /var/lib/jenkins/workspace/app_demo/
$ source venv/bin/activate
```

The virtual environment was activated successfully:

![055-03.png](https://behainguyen.files.wordpress.com/2023/01/055-03.png)

Let's run <code>Pytest</code>. All tests should just pass:

```
$ venv/bin/pytest
```

![055-04.png](https://behainguyen.files.wordpress.com/2023/01/055-04.png)

All tests passed as should be the case. Deactivate the virtual environment with:

```
$ deactivate
```

<h2>Tutorial References</h2>

<ol>
<li style="margin-top:10px;">
<a href="http://www.alexconrad.org/2011/10/jenkins-and-python.html" title="Jenkins and Python" target="_blank">Jenkins and Python</a>.
</li>

<li style="margin-top:10px;">
<a href="https://www.youtube.com/watch?v=OB7fGZ32n-s" title="How Do I Run a Python Script From Jenkins Pipeline?" target="_blank">YouTube: How Do I Run a Python Script From Jenkins Pipeline?</a>
</li>
</ol>

<h2>Jenkins Installation</h2>

I tried installing Jenkins on my Ubuntu 22.10 three (3) times, all went smoothly. 
But all failed to start. The last installation instruction I have used is from 
this link <a href="https://community.jenkins.io/t/ubuntu-20-04-initial-jenkins-startup-failure/1419"
title="Ubuntu 20.04 Initial Jenkins startup failure" target="_blank">https://community.jenkins.io/t/ubuntu-20-04-initial-jenkins-startup-failure/1419</a>
-- the answer by Mr. Mark Waite -- Jenkins Governance Board.

Basically, run these commands one after the other:

```
$ sudo apt-get install openjdk-11-jdk-headless
$ curl -fsSL https://pkg.jenkins.io/debian/jenkins.io.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
$ echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
$ sudo apt-get update
$ sudo apt-get install jenkins
```

But it still failed to start. I had forgotten that I have set 
<strong>port 8080</strong> for Apache2. I free up the port <strong>8080</strong> 
and start Jenkins with:

```
$ systemctl start jenkins.service
```

And it starts with no problem. I am guessing the previous two installations were also 
successful. But it does not matter now.

After successfully installed, we need to do some initial configurations. 
I just followed the instructions in this DigitalOcean article 
<a href="https://www.digitalocean.com/community/tutorials/how-to-install-jenkins-on-ubuntu-22-04"
title="How To Install Jenkins on Ubuntu 22.04"
target="_blank">How To Install Jenkins on Ubuntu 22.04</a>.

We can access Jenkins front-end at 
<code>http://&lt;machine-ip-address&gt;&lt;machine-name&gt;:8080</code>. In my case, from 
Windows 10, <code>http://hp-pavilion-15:8080/</code>, or on Ubuntu 22.10 where Jenkins is installed,
<code>http://localhost:8080</code>.

✿✿✿

I like Jenkins thus far, it makes sense. I have worked in an environment 
where the build server and the unit test server are two VMware machines.
The build process is written using Windows Powershell script, it also gets 
source codes from a source code management software installed in-house. 
Jenkins offers same capability, but the process seems much simpler. I hope 
you find the information useful. Thank you for reading and stay safe as always. 
