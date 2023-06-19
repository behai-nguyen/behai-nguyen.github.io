---
layout: post
title: "CI/CD #04. Jenkins: trigger a Freestyle project via Git webhook."

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.files.wordpress.com/2023/06/070-01.png"
    - "https://behainguyen.files.wordpress.com/2023/06/070-02.png"

gallery-image-list-2:
    - "https://behainguyen.files.wordpress.com/2023/06/070-06-a.png"
    - "https://behainguyen.files.wordpress.com/2023/06/070-06-b.png"

gallery-image-list-3:
    - "https://behainguyen.files.wordpress.com/2023/06/070-07-e.png"
    - "https://behainguyen.files.wordpress.com/2023/06/070-07-f.png"

gallery-image-list-4:
    - "https://behainguyen.files.wordpress.com/2023/06/070-08-b.png"
    - "https://behainguyen.files.wordpress.com/2023/06/070-08-c.png"
    - "https://behainguyen.files.wordpress.com/2023/06/070-08-d.png"

gallery-image-list-5:
    - "https://behainguyen.files.wordpress.com/2023/06/070-10-a.png"
    - "https://behainguyen.files.wordpress.com/2023/06/070-10-b.png"

description: We're setting up a Jenkins “Freestyle project”, using “Execute shell” build step, to&#58; ⓵ clone a Git repo, ⓶ create a virtual environment, ⓷ run editable install, and finally, ⓸ run Pytest. And this Jenkins job can be triggered remotely when we push some file(s) onto the target Git repo.
tags:
- Jenkins
- Freestyle project
- Pytest
- Git
- GitHub
- webhook
---

<em style="color:#111;">We're setting up a Jenkins “Freestyle project”, using “Execute shell” build step, to: ⓵ clone a Git repo, ⓶ create a virtual environment, ⓷ run editable install, and finally, ⓸ run Pytest. And this Jenkins job can be triggered remotely when we push some file(s) onto the target Git repo.</em>

| ![070-feature-image.png](https://behainguyen.files.wordpress.com/2023/06/070-feature-image.png) |
|:--:|
| *CI/CD #04. Jenkins: trigger a Freestyle project via Git webhook.* |

We're going to recreate the <code>Freestyle project</code> discussed in
<a href="https://behainguyen.wordpress.com/2023/01/"
title="CI/CD #01. Jenkins: manually clone a Python GitHub repo and run Pytest."
target="_blank">CI/CD #01. Jenkins: manually clone a Python GitHub repo and run Pytest</a>,
you don't need to read this post, all necessary steps are described where appropriate.

❶ Log into Jenkins, click on <code>+ New Item</code>. On the next page,
under <code>Enter an item name</code>, enter <code>app_demo</code> --
at runtime, Jenkins will create a directory with this name under Jenkins'
work directory, i.e. <code>/var/lib/jenkins/workspace/app_demo</code>.

And <code>/var/lib/jenkins/workspace/app_demo</code> is the value of the
<code>WORKSPACE</code> Jenkins environment variable.

❷ Select <code>Freestyle project</code>, then click on the
<code>OK</code> button to move to the <code>Configuration</code>
page.

For <code>Description</code>, write something meaningful, e.g.
<em>CI/CD #04. Jenkins: trigger a Freestyle project via Git webhook.</em>

The rest of the options are shown in the following two (2) screenshots:

{% include image-gallery.html list=page.gallery-image-list-1 %}

Basically:

<ol>
<li style="margin-top:10px;">
<code>Repository URL</code>: <code>https://github.com/behai-nguyen/app-demo.git</code>.
</li>
<li style="margin-top:10px;">
<code>Branch Specifier (blank for 'any')</code>: <code>*/main</code>.
</li>
<li style="margin-top:10px;">
MOST IMPORTANTLY, see the second screenshot, under
<code>Build Triggers</code> check <code>GitHub hook trigger for GITScm polling</code>.
Without checking this option, Jenkins will not process the
push events from Git, the on-screen explanation should sufficiently
explain the purpose of this option.
</li>
</ol>

Under <code>Build Steps</code>, pull down <code>Add build step</code>,
and select <code>Execute shell</code>, then paste in this content:

```
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
```

![070-03.png](https://behainguyen.files.wordpress.com/2023/06/070-03.png)

Finally, click on the <code>Save</code> button: we're taken
to the <code>app_demo</code> project page.

❸ To test that this project is working, I removed <code>app_demo/</code>
from <code>/var/lib/jenkins/workspace/</code>. Then clicked on <code>▷ Build Now</code>
to run the first build.

It ran successfully for me. And <code>app_demo/</code> was created
under <code>/var/lib/jenkins/workspace/</code>, so was the virtual
directory <code>app_demo/venv/</code>.

Remove <code>app_demo/</code> with:

```
jenkins@hp-pavilion-15:~/workspace$ rm -rf app_demo
```

❹ <a id="free-ngrok-setup">Next, we need to make our Jenkins server available publicly.</a> For this,
we're using <code>ngrok</code> -- this has been discussed previously in
<a href="https://behainguyen.wordpress.com/2023/02/#install-ngrok-ubuntu"
title="Install ngrok for Ubuntu 22.10 kinetic" target="_blank">Install ngrok for Ubuntu 22.10 kinetic</a>.

For Jenkins, the port is <code>8080</code>:

```
$ ngrok http 8080
```

We'll get something similar to the screenshot below:

![070-04.png](https://behainguyen.files.wordpress.com/2023/06/070-04.png)

In this instance, our Jenkins “public” URL is <code>https://5b3c-58-109-142-244.ngrok-free.app</code>.
For Git payload URL (discussed later), we need to append <code>github-webhook<strong>/</strong></code>.

-- Please notice that it is <code>github-webhook<strong>/</strong></code>: DO NOT FORGET
the trailing <code><strong><span style="color:blue;">/</span></strong></code>!

The complete Git payload URL is <code>https://5b3c-58-109-142-244.ngrok-free.app/github-webhook/</code>.

❺ <a id="setup-repo-webhook">The next step is to set up webhook for repo <code>https://github.com/behai-nguyen/app-demo.git</code>.</a>
A similar process has been described before, in
<a href="https://behainguyen.wordpress.com/2023/02/#github-webhook-test-our-server"
title="Set up GitHub Webhook and test our server" target="_blank">Set up GitHub Webhook and test our server</a>.
Follow the steps described below.

⓵ Go to <code>https://github.com/behai-nguyen/app-demo.git</code>, or yours one.
Click on <code>Settings</code> on top right hand corners, then click on
<code>Webhooks</code> on the left hand side bar.

⓶ On the next screen, click on the <code>Add webhook</code> button on the
top right hand corner.

⓷ On the next screen:

<ol>
<li style="margin-top:10px;">
<code>Payload URL *</code>: <code>https://5b3c-58-109-142-244.ngrok-free.app/github-webhook/</code>
-- the URL we've discussed above.
</li>
<li style="margin-top:10px;">
<code>Content type</code>: <code>application/json</code>
</li>
<li style="margin-top:10px;">
I left everything else at their default values.
</li>
</ol>

This screen should look like:

![070-05.png](https://behainguyen.files.wordpress.com/2023/06/070-05.png)

Click on the <code>Add webhook</code> button to continue.
Git should send a ping event, we should receive it successfully:

{% include image-gallery.html list=page.gallery-image-list-2 %}

❻ Test the webhook. Let's ensure our Jenkins session is still
active. Our project should show one successful build from the
previous manual run. And there is no <code>app_demo/</code>
under <code>/var/lib/jenkins/workspace/</code>.

I added another marker to <code>D:\app_demo\pytest.ini</code>, check this one in:

![070-07-a.png](https://behainguyen.files.wordpress.com/2023/06/070-07-a.png)

It should automatically trigger another build. The <code>ngrok</code> console shows another event:

![070-07-b.png](https://behainguyen.files.wordpress.com/2023/06/070-07-b.png)

Git records another successful push event, details should match our commit:

![070-07-c.png](https://behainguyen.files.wordpress.com/2023/06/070-07-c.png)

Refresh Jenkins, it should show another successful build:

![070-07-d.png](https://behainguyen.files.wordpress.com/2023/06/070-07-d.png)

The detail of the second build:

{% include image-gallery.html list=page.gallery-image-list-3 %}

Note the second screenshot: there was only one test module
<code>tests/functional/test_routes.py</code>; and a total
of <code>5 passed, 1 warning</code>.

❼ Test the webhook. Remove <code>app_demo/</code> from <code>/var/lib/jenkins/workspace/</code>:

```
jenkins@hp-pavilion-15:~/workspace$ rm -rf app_demo/
```

Add another test module <code>D:\app_demo\tests\jenkins_demo\test_push_01.py</code>,
this module <strong>has only a single test method</strong>:

![070-08-a.png](https://behainguyen.files.wordpress.com/2023/06/070-08-a.png)

It should automatically trigger another build.
Both Git and <code>ngrok</code> should show another successful push event.
And Jenkins should show a third successful build:

{% include image-gallery.html list=page.gallery-image-list-4 %}

The last screenshot shows the new test module, and the total tests increased
by 1 (one), to six (6): <code>6 passed, 1 warning</code>.

And of course, <code>app_demo</code> gets recreated, together with the
virtual environment directory:

![070-09.png](https://behainguyen.files.wordpress.com/2023/06/070-09.png)

❽ Still testing the webhook. Leave everything as they are. Using GitHub UI,
I edit
<code>https://github.com/behai-nguyen/app-demo/blob/main/tests/jenkins_demo/test_push_01.py</code>,
adding the comment <code># This is a manual test comment.</code>; and commit
the change:

{% include image-gallery.html list=page.gallery-image-list-5 %}

Both Git and <code>ngrok</code> should show another successful push event.
That makes four (4) push events so far. The following screenshot, Git shows the
details of the push:

![070-10-c.png](https://behainguyen.files.wordpress.com/2023/06/070-10-c.png)

And Jenkins also shows a fourth (4th) successful build, whose
details match the push event's. There were no changes to code,
tests should naturally pass and the total number of tests remains
the same:

![070-10-d.png](https://behainguyen.files.wordpress.com/2023/06/070-10-d.png)

As the concluding remark to finish off this post. Are you wondering
why I use <code>Freestyle project</code> to explore Git webhook?

I started this post using both Pipeline implementations discussed in
<a href="https://behainguyen.wordpress.com/2023/02/06/ci-cd-03-jenkins-using-pipeline-and-proper-bash-script-to-run-pytest/"
title="CI/CD #03. Jenkins: using Pipeline and proper Bash script to run Pytest." target="_blank">CI/CD #03. Jenkins: using Pipeline and proper Bash script to run Pytest</a>.
I could not get Jenkins to trigger the build. I need to do more studies
on this, and I will discuss my findings in later posts. And I still have
not come across any documentation explaining why <code>Freestyle project</code>
works in this instance. Studies and more studies 😂

Thank you for reading. I hope this post is informative. Stay safe as always.

✿✿✿

Feature image sources:

<ul>
<li>
<a href="https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper" target="_blank">https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper</a>
</li>
<li>
<a href="https://pngimg.com/image/73422" target="_blank">https://pngimg.com/image/73422</a>
</li>
<li>
<a href="https://status.ngrok.com/" target="_blank">https://status.ngrok.com/</a>
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
</ul>
