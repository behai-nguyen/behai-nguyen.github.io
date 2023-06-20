---
layout: post
title: "CI/CD #05. Jenkins: trigger a Pipeline via Git webhook."

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list:
    - "https://behainguyen.files.wordpress.com/2023/06/072-01-a.png"
    - "https://behainguyen.files.wordpress.com/2023/06/072-01-b.png"
    - "https://behainguyen.files.wordpress.com/2023/06/072-01-c.png"
    - "https://behainguyen.files.wordpress.com/2023/06/072-01-d.png"

description: We’re setting up a Jenkins “Pipeline script from SCM”, which uses a generic Bash script file to ⓵ create a virtual environment, ⓶ run editable install, and ⓷ run Pytest for all tests. And this Jenkins job can be triggered remotely when we push some file(s) onto the target Git repo.
tags:
- Jenkins
- Bash
- Pipeline
- Pytest
- Git
- GitHub 
- webhook
---

<em style="color:#111;">We’re setting up a Jenkins “Pipeline script from SCM”, which uses a generic Bash script file to ⓵ create a virtual environment, ⓶ run editable install, and ⓷ run Pytest for all tests. And this Jenkins job can be triggered remotely when we push some file(s) onto the target Git repo.</em>

| ![072-feature-image.png](https://behainguyen.files.wordpress.com/2023/06/072-feature-image.png) |
|:--:|
| *CI/CD #05. Jenkins: trigger a Pipeline via Git webhook.* |

This post combines material we've gone through in the following posts:

<ol>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/01/28/ci-cd-01-jenkins-manually-clone-a-python-github-repo-and-run-pytest/" title="CI/CD #01. Jenkins: manually clone a Python GitHub repo and run Pytest." target="_blank">CI/CD #01. Jenkins: manually clone a Python GitHub repo and run Pytest.</a>
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/02/03/ci-cd-02-jenkins-basic-email-using-your-gmail-account/" title="CI/CD #02. Jenkins: basic email using your Gmail account." target="_blank">CI/CD #02. Jenkins: basic email using your Gmail account.</a>
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/02/06/ci-cd-03-jenkins-using-pipeline-and-proper-bash-script-to-run-pytest/" title="CI/CD #03. Jenkins: using Pipeline and proper Bash script to run Pytest." target="_blank">CI/CD #03. Jenkins: using Pipeline and proper Bash script to run Pytest.</a>
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/06/09/ci-cd-04-jenkins-trigger-a-freestyle-project-via-git-webhook/" title="CI/CD #04. Jenkins: trigger a Freestyle project via Git webhook." target="_blank">CI/CD #04. Jenkins: trigger a Freestyle project via Git webhook.</a>
</li>
</ol>

In the above last post (post 4), as a concluding remark, I've written:

>
> I started this post using both Pipeline implementations discussed in <a href="https://behainguyen.wordpress.com/2023/02/06/ci-cd-03-jenkins-using-pipeline-and-proper-bash-script-to-run-pytest/" title="CI/CD #03. Jenkins: using Pipeline and proper Bash script to run Pytest." target="_blank">CI/CD #03. Jenkins: using Pipeline and proper Bash script to run Pytest</a>. I could not get Jenkins to trigger the build.
>

I still have not been able to find any documentation or tutorial discussing 
this issue. Through repeated experimentations, I seem to get a hang of it:

<strong>🚀 After creating the Jenkins Pipeline, WE MUST FIRST DO a manual build 
using the <code>▷ Build Now</code> link.</strong>

<div style="background-color:yellow;width:100%;height:100px;display:flex;margin-bottom:10px;">
    <div style="flex:100px;height:100px;
	    background-image:url('https://behainguyen.files.wordpress.com/2022/12/info-symbol.png');
		background-position: center center;background-size:100px 100px;
		background-repeat: no-repeat">
    </div>

	<div style="flex:550px;font-weight:bold;color:blue;padding-right:40px;padding-left:40px;height:100px;display:flex;align-items:center">
		<div style="height:90px">
           This behaviour has been consistent during my experimentations. But 
		   since I do not have any documentation to back it up, please treat 
		   it with caution.		   
		</div>
	</div>
</div>

Let's get to it. The issues we'll have to attend to are: ⓵ the Bash script,
⓶ the Jenkinsfile, ⓷ the Jenkins Pipeline, ⓸ using <code>ngrok</code> to make
our local Jenkins server publicly accessible, ⓹ set up Git webhook, and finally 
⓺ test the entire set up.

❶ The Bash script.

The Bash script used in this post has been checked in at 
<a href="https://github.com/behai-nguyen/linux-scripts/blob/main/pytest.sh" title="Jenkins Pytest Bash script" target="_blank">https://github.com/behai-nguyen/linux-scripts/blob/main/pytest.sh</a>.
We've previously discussed this script 
<a href="https://behainguyen.wordpress.com/2023/02/06/ci-cd-03-jenkins-using-pipeline-and-proper-bash-script-to-run-pytest/#bash-script"
title="CI/CD #03. Jenkins: using Pipeline and proper Bash script to run Pytest. | The Bash script."
target="_blank">in this section</a> -- please refer to it for set up and usage.

These two are essentially identical. The GitHub version has its
comments (documentation) fixed, the codes are identical.

❷ The Jenkinsfile.

We're also using the <code>https://github.com/behai-nguyen/app-demo.git</code> 
repo for this new Pipeline, the same Jenkinsfile 
<a href="https://behainguyen.wordpress.com/2023/02/06/ci-cd-03-jenkins-using-pipeline-and-proper-bash-script-to-run-pytest/#jenkins-pipeline"
title="CI/CD #03. Jenkins: using Pipeline and proper Bash script to run Pytest. | The Jenkinsfile." target="_blank">in this section</a>
is also used for this new Pipeline. It has been checked into the repo at  
<a href="https://github.com/behai-nguyen/app-demo/blob/main/Jenkinsfile"
title="The Jenkinsfile." target="_blank">https://github.com/behai-nguyen/app-demo/blob/main/Jenkinsfile</a>.

❸ The Jenkins Pipeline.

As mentioned at the beginning, we're setting up a <code>Pipeline script from SCM</code>
project. 

⓵ Log into Jenkins, remove any existing <code>app_demo</code> project. 

⓶ Click on <code>+ New Item</code>. On the next page,
under <code>Enter an item name</code>, enter <code>app_demo</code> --
at runtime, Jenkins will create a directory with this name under Jenkins'
work directory, i.e. <code>/var/lib/jenkins/workspace/app_demo</code>.

And <code>/var/lib/jenkins/workspace/app_demo</code> is the value of the
<code>WORKSPACE</code> Jenkins environment variable.

⓷ Select <code>Pipeline</code>, then click on the <code>OK</code> button 
to move to the <code>Configuration</code> page.

⓸ On the <code>Configuration</code> page, for <code>Description</code>, 
write something meaningful, e.g. <em>CI/CD #05. Jenkins: trigger a Pipeline via Git webhook.</em>

For <code><strong>Build Triggers</strong></code> check 
<code>GitHub hook trigger for GITScm polling</code>.
Without checking this option, Jenkins will not process the
push events from Git, the on-screen explanation should sufficiently
explain the purpose of this option.

Under the heading <code><strong>Advanced Project Options</strong></code>, 
click on the <code>Advanced ⌄</code> button, for <code>Display Name</code>, 
enter something descriptive, e.g. <code>Jenkins Pipeline and GitHub 
Webhooks.</code>

Under the heading <code><strong>Pipeline</strong></code>, for 
<code>Definition</code>, select <code>Pipeline script from SCM</code>.

For <code>SCM</code>, select <code>Git</code>.

Under <code>Repositories</code>, for <code>Repository URL</code>,
enter the address of the repo; e.g. <code>https://github.com/behai-nguyen/app-demo.git</code>.

Under <code>Branches to build</code>, for <code>Branch Specifier (blank for 'any')</code>,
enter <code>*/main</code> -- you can try some other branch, I've only tested with 
<code>*/main</code>.

Finally, <code>Script Path</code> -- leave the default value of <code>Jenkinsfile</code>.

Our new <code>app_demo</code> Pipeline should look like the following screenshots:

{% include image-gallery.html list=page.gallery-image-list %}

Click on the <code>Save</code> button: we're taken
to the <code>app_demo</code> project page.

❹ Using <code>ngrok</code> to make our local Jenkins server publicly accessible.

Please 
<a href="https://behainguyen.wordpress.com/2023/06/09/ci-cd-04-jenkins-trigger-a-freestyle-project-via-git-webhook/#free-ngrok-setup"
title="CI/CD #04. Jenkins: trigger a Freestyle project via Git webhook. | ngrok setup."
target="_blank">refer to this section</a> of a previous post. It's exactly the same for this post.

❺ Set up Git webhook for repo <code>https://github.com/behai-nguyen/app-demo.git</code>.

First, if there is any existing webhook on <code>https://github.com/behai-nguyen/app-demo.git</code>,
we might need to remove it, since the payload URL might have become invalid, because
we terminated <code>ngrok</code> since our last run, etc.

And we've have also done this exact same process before. Please 
<a href="https://behainguyen.wordpress.com/2023/06/09/ci-cd-04-jenkins-trigger-a-freestyle-project-via-git-webhook/#setup-repo-webhook"
title="CI/CD #04. Jenkins: trigger a Freestyle project via Git webhook. | Setup Git repo webhook."
target="_blank">refer to this section</a> of a previous post. 

❻ Now, we're testing the Pipeline and hence the entire set up.

⓵ Remove <code>app_demo/</code> from <code>/var/lib/jenkins/workspace/</code>:

```
jenkins@hp-pavilion-15:~/workspace$ rm -rf app_demo/
```

⓶ <strong>🚀 WE MUST DO a manual build first</strong>:

-- Click on the <code>▷ Build Now</code> link on the left hand 
side to do a the first build for this Pipeline.

This build should just pass. Sub-directory <code>app_demo/</code> 
should now exist under <code>/var/lib/jenkins/workspace/</code>.

For testing purposes, we'll again remove <code>app_demo/</code> 
from <code>/var/lib/jenkins/workspace/</code>.

The build log should show the following output lines:

```
...
tests/functional/test_routes.py .....                                    [ 83%]
tests/jenkins_demo/test_push_01.py .                                     [100%]

=============================== warnings summary ===============================
src/app_demo/utils/functions.py:10
  /var/lib/jenkins/workspace/app_demo/src/app_demo/utils/functions.py:10: DeprecationWarning: invalid escape sequence '\p'
    """This method assumes the project has the following layout:

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
========================= 6 passed, 1 warning in 0.05s =========================
...
```

Note that we have two (2) test modules, and six (6) tests. We're ready to 
do automatic tests.

⓷ Add another test module <code>D:\app_demo\tests\jenkins_demo\test_push_02.py</code>,
this module <strong>has only a single test method</strong>:

![072-02.png](https://behainguyen.files.wordpress.com/2023/06/072-02.png)

We've gone through this similar testing process in this post 
<a href="https://behainguyen.wordpress.com/2023/06/09/ci-cd-04-jenkins-trigger-a-freestyle-project-via-git-webhook/" title="CI/CD #04. Jenkins: trigger a Freestyle project via Git webhook." target="_blank">CI/CD #04. Jenkins: trigger a Freestyle project via Git webhook.</a>
This testing process is the same. We'll go over the key points briefly,
not in as much detail as the mentioned post.

It should now automatically trigger build 2 (two). The build log
should show something similar to the following screenshot:

![072-03.png](https://behainguyen.files.wordpress.com/2023/06/072-03.png)

This screenshot shows the new test module, and the total tests increased
by 1 (one), to seven (7): <code>7 passed, 1 warning</code>.

We can see that, except for the Pipeline, every other processes described
in this post are, more or less, identical to those in the <code>Freestyle project</code>,
which we've already covered.

The main difference is:

<strong>🚀 After creating the Jenkins Pipeline, WE MUST FIRST DO a manual build 
using the <code>▷ Build Now</code> link.</strong>

-- And as I have stated before, please treat the above conclusion with caution!

✿✿✿

Prior to writing this post, I've spent almost two (2) days on this issue. I have
carried out numerous tests. Let's describe some tests, so that you can verify
if interested. The tests that I'm going to describe could be regarded as 
“narrowed down tests” or “focused tests” -- by which I mean the tests that I have
singled out to prove that <strong>we must first do a manual build before auto
builds can happen</strong>.

Please note, I did not carry out these 
tests on the <code>https://github.com/behai-nguyen/app-demo.git</code> repo, I 
don't want to pollute
it with testing commits, I created another repo and played with that.

⓵ Continue on with the environment above intact, stop and start Jenkins. 
Then do a push: this should trigger another build.

Commands to stop, start and check Jenkins status are:

```
sudo systemctl stop jenkins
sudo systemctl start jenkins
systemctl status jenkins	
```

⓶ Remove this Pipeline. Re-create it, but DO NOT RUN a build manually. 
Do a push: no build happens, even though <code>ngrok</code> receives the
push notification with no problem. And Git also reports a successful 
delivery.

⓷ Continue on from ⓶ -- do the first manual build. Then do a push: this 
should automatically trigger another build.

⓸ Remove <code>app_demo/</code> from <code>/var/lib/jenkins/workspace/</code>,
then push to verify that the Pipeline is responsible for 
cloning the repo. That is, <em>as long as we did the first manual build, 
it does not matter if the repo is on disk or not</em>, the Pipeline 
should always clone on each build. (How else can it get the latest code
to run Pytest on?)

⓹ Replace webhook: restart <code>ngrok</code> to get a new URL,
remove the existing webhook with the previous URL, then set up a 
new one with this new URL. Then do a push: this should trigger 
another automatic build.

That's about it for this post. I do hope you find the information useful. 
<strong>And please kindly let me know if I've made any mistakes</strong>.
Thank you for reading and stay safe as always.

✿✿✿

Feature image sources:

<ul>
<li>
<a href="https://in.pinterest.com/pin/337277459600111737/" target="_blank">https://in.pinterest.com/pin/337277459600111737/</a>
</li>
<li>
<a href="https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper" target="_blank">https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper</a>
</li>
<li>
<a href="https://branditechture.agency/brand-logos/download/jenkins/#google_vignette" target="_blank">https://branditechture.agency/brand-logos/download/jenkins/#google_vignette</a>
</li>
<li>
<a href="https://status.ngrok.com/" target="_blank">https://status.ngrok.com/</a>
</li>
<li>
<a href="https://pngimg.com/image/73422" target="_blank">https://pngimg.com/image/73422</a>
</li>
<li>
<a href="https://seeklogo.com/vector-logo/332789/python" target="_blank">https://seeklogo.com/vector-logo/332789/python</a>
</li>
<li>
<a href="https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Pytest_logo.svg/2048px-Pytest_logo.svg.png" target="_blank">https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Pytest_logo.svg/2048px-Pytest_logo.svg.png</a>
</li>
<li>
<a href="https://www.wildjar.com/platform/webhook-integration" target="_blank">https://www.wildjar.com/platform/webhook-integration</a>
</li>
<li>
<a href="https://bashlogo.com/img/logo/png/full_colored_light.png" target="_blank">https://bashlogo.com/img/logo/png/full_colored_light.png</a>
</li>
</ul>
