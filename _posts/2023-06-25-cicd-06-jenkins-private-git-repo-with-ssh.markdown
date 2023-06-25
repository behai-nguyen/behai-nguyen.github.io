---
layout: post
title: "CI/CD #06. Jenkins: accessing private GitHub repos using SSH keys."

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.files.wordpress.com/2023/06/073-04-c.png"
    - "https://behainguyen.files.wordpress.com/2023/06/073-04-d.png"
    - "https://behainguyen.files.wordpress.com/2023/06/073-04-e.png"

gallery-image-list-2:
    - "https://behainguyen.files.wordpress.com/2023/06/073-04-f.png"
    - "https://behainguyen.files.wordpress.com/2023/06/073-04-g.png"

description: Using a generated public-private key pair, we set up a GitHub SSH key (public key), and Jenkins SSH username with private key credential to enable Jenkins projects to access private GitHub repositories.
tags:
- Jenkins
- private
- repo
- GitHub
- SSH
- credential
---

<em style="color:#111;">Using a generated public-private key pair, we set up a GitHub SSH key (public key), and Jenkins SSH username with private key credential to enable Jenkins projects to access private GitHub repositories.</em>

| ![073-feature-image.png](https://behainguyen.files.wordpress.com/2023/06/073-feature-image.png) |
|:--:|
| *CI/CD #06. Jenkins: accessing private GitHub repos using SSH keys.* |

The environment of this post is <code>Jenkins 2.401.1</code> running on an <code>Ubuntu 22.10</code> machine. It seems that Jenkins UI is slightly different between versions.

We can access GitHub private repositories using SSH (Secure Shell Protocol). <a href="https://docs.github.com/en/authentication/connecting-to-github-with-ssh" title="Connecting to GitHub with SSH" target="_blank">Connecting to GitHub with SSH</a> is the official GitHub document which provides instructions on how to do this.

In essence, we a need a public key for GitHub, and a private key to setting up a Jenkins credential with. Once we've done this, we can create Jenkins projects using the credential we've set up.

The issues we're going to address in this post are thus: ❶ generating the public-private key pair, ❷ configure GitHub SSH key using the generated public key, ❸ set up a new Jenkins credential using the generated private key, ❹ create a Jenkins project to access a private repo using the credential we've set up in ❸, and finally ❺ we're testing the new Jenkins project.

❶ Generating the public-private key pair.

We follow these two official documents:

<ol>
<li style="margin-top:10px;">
<a href="https://docs.github.com/en/authentication/connecting-to-github-with-ssh/checking-for-existing-ssh-keys" title="Checking for existing SSH keys" target="_blank">Checking for existing SSH keys</a>
</li>
<li style="margin-top:10px;">
<a href="https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent" title="Generating a new SSH key and adding it to the ssh-agent" target="_blank">Generating a new SSH key and adding it to the ssh-agent</a>
</li>
</ol>

I've done this under user <code>jenkins</code>. That is, I connect (via SSH) into the <code>Ubuntu 22.10</code> machine with user <code>jenkins</code>:

```
ssh jenkins@192.168.0.17
```

There're no existing SSH keys: I did not generate one before. And

```
$ ls -al ~/.ssh
```

also confirms no existing SSH keys. Follow the official document mentioned above, we generate the keys with:

```
$ ssh-keygen -t ed25519 -C "behai_nguyen@hotmail.com"
```

Whereby <code>behai_nguyen@hotmail.com</code> is the email I use to log in to GitHub.

I just accepted the suggested defaults. For the <code>passphrase</code>, I use <code>I live in Melbourne.</code> -- including <code>.</code> (a fullstop). A successful key generation looks like the screenshot below:

![073-01-1.png](https://behainguyen.files.wordpress.com/2023/06/073-01-1.png)

⓵ The <code>private key</code> is stored in the file <code>/var/lib/jenkins/.ssh/id_ed25519</code>. And the key looks like:

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABBEN+iqTy
/WQQPkwwkhvZzUAAAAEAAAAAEAAAAzAAAAC3NzaC1lZDI1NTE5AAAAIMTGu+OQjJlMk9jN
qAd8a8KwKijgjIJJgQvfiFd2USbTAAAAoM3Cpg7lnvRBLZbPDzWm4QN9LV7VcnXOOUGJYE
1qzASxnK6iaOQr4dLj0zR8Vi6FopELk7qydHgot/DFDnsygXnxrcTamviv0Z6K5KgKTQJT
C1atxPZUpHnOtPqMQkRz6JrOtg7ReecjVKetNn8NYo+zAlStWR7FuM+g07o40ff6sORZwj
+in8c4yfd5sKkc4Ab2dY6S9igTStyZS9gr1Ds=
-----END OPENSSH PRIVATE KEY-----
```

⓶ The <code>public key</code> is stored in the file <code>/var/lib/jenkins/.ssh/id_ed25519.pub</code>. And the key looks like:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMTGu+OQjJlMk9jNqAd8a8KwKijgjIJJgQvfiFd2USbT behai_nguyen@hotmail.com
```

⓷ Note also the <code>key fingerprint</code> of <code>SHA256:rcDT2TK2VGrmYaCgRYe7mwqlOgKKUR9JORq0D8Pw1PA behai_nguyen@hotmail.com</code>.

⓸ Pre-populate the SSH keys for each server. Please note, <strong><em>I documented this step, because I ran into the problem:</em> <code>stderr: No ED25519 host key is known for github.com and you have requested strict checking.</code> <em>You can certainly skip it and see what happens, if you encounter the same problem, then, you can certainly carry it out.</em></strong> Run the following command:

```
$ ssh-keyscan github.com >> ~/.ssh/known_hosts
```

The output looks like the below screenshot (I accidentally ran it a second time):

![073-02-a.png](https://behainguyen.files.wordpress.com/2023/06/073-02-a.png)

Without this SSH key re-population, Jenkins raises the following error when using the credential:

![073-02-b.png](https://behainguyen.files.wordpress.com/2023/06/073-02-b.png)

This less than a month old <a href="https://askubuntu.com/questions/1469884/i-am-facing-issue-while-configuring-github-ssh-key-to-jenkins-server-for-ci" title="I am facing issue while configuring GitHub ssh key to Jenkins server for ci?" target="_blank">Ask Ubuntu</a> post is about the exact same problem. And <a href="https://askubuntu.com/questions/1427446/stderr-no-ecdsa-host-key-is-known-for-github-com-and-you-have-requested-strict" title="stderr: No ECDSA host key is known for github.com and you have requested strict checking" target="_blank">this post</a> suggests the above command -- and it does work for me.

For <code>Jenkins 2.401.1</code>, <code>Known hosts file</code> verification is the default, as can be seen in the screenshot below:

![073-02-c.png](https://behainguyen.files.wordpress.com/2023/06/073-02-c.png)

❷ Configure GitHub SSH key using the generated public key.

Go to <a href="https://github.com/" title="https://github.com/" target="_blank">https://github.com/</a>, click on profile photo, then <code>Settings</code>:

![073-03-a.png](https://behainguyen.files.wordpress.com/2023/06/073-03-a.png)

Then click on <code>SSH and GPG keys</code> link on the left hand side bar:

![073-03-b.png](https://behainguyen.files.wordpress.com/2023/06/073-03-b.png)

Click on <code>New SSH key</code> button. On the next screen, for <code>Title</code>, enter something meaningful such as <code>ssh-private-repo</code>; for <code>Key</code>, enter the public key we've generated above, see the screenshot below:

![073-03-c.png](https://behainguyen.files.wordpress.com/2023/06/073-03-c.png)

Click on <code>Add SSH key</code>, we will be asked for security confirmation. Once completed, the next screen shows our new key added:

![073-03-d.png](https://behainguyen.files.wordpress.com/2023/06/073-03-d.png)

Note the value of <code>key fingerprint</code> (discussed above) displayed underneath <code>ssh-private-repo</code>; and other self-explanatory info.

❸ Create a new Jenkins credential using the generated private key.

There is more than one way to configure a new credential. In my thinking, the approach presented in this section is a bit more logical. We'll mention another approach in a later section. Click on the <code>Dashboard</code> link, the <code>Manage Jenkins</code> link, then the <code>Credentials</code> link:

![073-04-a.png](https://behainguyen.files.wordpress.com/2023/06/073-04-a.png)

There is no prior credential configured. Click on the <code>(global)</code> link:

![073-04-b.png](https://behainguyen.files.wordpress.com/2023/06/073-04-b.png)

Click on the <code>+ Add Credentials</code> button. On the next screen, fill in the information as per the following screenshots:

{% include image-gallery.html list=page.gallery-image-list-1 %}

<ul>
<li style="margin-top:10px;"> <code>ID</code>: <code>ssh-private-repo</code>, which is the value of the <code>Title</code> for GitHub SSH key discussed above.
</li>
<li style="margin-top:10px;">
<code>Description</code>: something meaningful. E.g. <code>SSH credential to access private repos</code>. This will become an entry in the credential selection list later on.
</li>
<li style="margin-top:10px;">
<code>Username</code>: this is the email we use to log into GitHub with.
</li>
<li style="margin-top:10px;">
<code>Private Key</code>: check <code>Enter directly</code>, then click on the <code>Add</code> button, copy and paste in the private key we've generated previously.
</li>
<li style="margin-top:10px;">
<code>Passphrase</code>: this is the <code>passphrase</code> we've specified when generating the key, it's <code>I live in Melbourne.</code> -- including <code>.</code> (a fullstop).
</li>
</ul>

Click on the <code>Create</code> button. Our new credential has been created: 

{% include image-gallery.html list=page.gallery-image-list-2 %}

❹ Create a Jenkins project to access a private repo.

The private repo I'm using for this Jenkins project is an old never-completed project of mine. It is in <a href="https://nodejs.org/en" title="NodeJs" target="_blank">NodeJs</a> and <a href="https://react.dev/" title="React" target="_blank">React</a>.

The objective of the Jenkins project is to demonstrate that we can use our SSH public-private key pair to access a private repo. All this Jenkins project does is to clone the target private repo down to local disk. We will use the <code>Freestyle project</code>.

⓵ We need to get the SSH URL for the repo. Select the repo, then click on the <code><> Code</code> button, then <code>SSH</code> tab, copy the SSH URL: <code>git@github.com:behai-nguyen/YouTubeManager.git</code>:

![073-05.png](https://behainguyen.files.wordpress.com/2023/06/073-05.png)

⓶ Back to Jenkins, click on the <code>Dashboard</code> link, then <code>+ New Item</code>. On the next page, under <code>Enter an item name</code>, enter <code>youtube_mgr</code> -- at runtime, Jenkins will create a directory with this name under Jenkins' work directory, i.e. <code>/var/lib/jenkins/workspace/youtube_mgr</code>.

And <code>/var/lib/jenkins/workspace/youtube_mgr</code> is the value of the <code>WORKSPACE</code> Jenkins environment variable.

⓷ Select <code>Freestyle project</code>, then click on the <code>OK</code> button to move to the <code>Configuration</code> page.

⓸ On the <code>Configuration</code> page, for <code>Description</code>, write something meaningful, e.g. <em>Cloning / downloading a private repo using SSH.</em>

Under the heading <code><strong>Source Code Management</strong></code>, check <code>Git</code>, then under <code>Repositories</code>, for <code>Repository URL</code>, enter the SSH URL above; i.e. <code>git@github.com:behai-nguyen/YouTubeManager.git</code>. We'll get the error as seen in the screenshot below:

![073-06-a.png](https://behainguyen.files.wordpress.com/2023/06/073-06-a.png)

This is normal, it is expected -- we need to select an existing credential or create a new one and use it. Remember earlier on we mentioned that there is more than one way to configure a new credential? Here is the second method, underneath the <code>Credentials</code> drop-down box, click on the <code>Add</code> button, then click on <code>Jenkins</code> drop-down menu item, we'll be taken to a screen similar to the previous one, whereby we can create a new credential:

![073-06-b.png](https://behainguyen.files.wordpress.com/2023/06/073-06-b.png)

But since we've done this already, we can now use it. Click the <code>Credentials</code> drop-down box, we should see our entry <code>SSH credential to access private repos</code> in there, select it:

![073-06-c.png](https://behainguyen.files.wordpress.com/2023/06/073-06-c.png)

After a few seconds, the error should go away:

![073-06-d.png](https://behainguyen.files.wordpress.com/2023/06/073-06-d.png)

Our credential works! 

Under <code>Branches to build</code>, for <code>Branch Specifier (blank for 'any')</code>, leave at <code>*/master</code> -- as mentioned before, this is an old repo, before GitHub changed the main branch to <code>*/main</code>.

Click on the <code>Save</code> button: we're taken to the <code>youtube_mgr</code> project page.

❺ Test <code>youtube_mgr</code> project.

⓵ Ensure there's no <code>youtube_mgr/</code> directory under 
<code>/var/lib/jenkins/workspace/</code>:

![073-07-a.png](https://behainguyen.files.wordpress.com/2023/06/073-07-a.png)

Click on the <code>▷ Build Now</code> link on the left hand side, it should run successfully:

![073-07-b.png](https://behainguyen.files.wordpress.com/2023/06/073-07-b.png)

The target private repo should be cloned to the local disk. That is, sub-directory <code>youtube_mgr/</code> should now exist under <code>/var/lib/jenkins/workspace/</code>:

![073-07-c.png](https://behainguyen.files.wordpress.com/2023/06/073-07-c.png)

We've successfully accessed our private repo using SSH. 

⓶ In this post <a href="https://behainguyen.wordpress.com/2023/06/20/ci-cd-05-jenkins-trigger-a-pipeline-via-git-webhook/" title="CI/CD #05. Jenkins: trigger a Pipeline via Git webhook." target="_blank">CI/CD #05. Jenkins: trigger a Pipeline via Git webhook</a>, we look at automatically trigger a Jenkins Pipeline whenever we push something onto the target <strong>public</strong> GitHub repo. I've tested an exact similar set up on a private repo, using the same credential, i.e. <code>ssh-private-repo</code> / <code>SSH credential to access private repos</code>, and it also works: repo gets cloned, virtual environment gets created, all Pytest get run and email gets sent.

<h3 style="color:teal;">
  <a id="my-other-jenkins-posts">Other Jenkins Posts Which I've Written</a>
</h3>

<ol>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/01/28/ci-cd-01-jenkins-manually-clone-a-python-github-repo-and-run-pytest/" title="CI/CD #01. Jenkins: manually clone a Python GitHub repo and run Pytest." target="_blank">CI/CD #01. Jenkins: manually clone a Python GitHub repo and run Pytest.</a> -- I'm describing the steps required to manually get Jenkins to: ⓵ clone a Python project GitHub repository, ⓶ create a virtual environment, ⓷ run editable install, and finally, ⓸ run Pytest for all tests.
</li>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/02/03/ci-cd-02-jenkins-basic-email-using-your-gmail-account/" title="CI/CD #02. Jenkins: basic email using your Gmail account." target="_blank">CI/CD #02. Jenkins: basic email using your Gmail account.</a> -- We look at the most basic approach to send emails in Jenkins. The SMTP server we use is the Gmail SMTP server.
</li>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/02/06/ci-cd-03-jenkins-using-pipeline-and-proper-bash-script-to-run-pytest/" title="CI/CD #03. Jenkins: using Pipeline and proper Bash script to run Pytest." target="_blank">CI/CD #03. Jenkins: using Pipeline and proper Bash script to run Pytest.</a> -- We write a proper and generic Bash script file to ⓵ create a virtual environment, ⓶ run editable install, and ⓷ run Pytest for all tests. Then we write a generic Jenkins Pipeline which will ⓵ clone a Python project GitHub repository, ⓶ call the Bash script file to do all the works.
</li>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/06/09/ci-cd-04-jenkins-trigger-a-freestyle-project-via-git-webhook/" title="CI/CD #04. Jenkins: trigger a Freestyle project via Git webhook." target="_blank">CI/CD #04. Jenkins: trigger a Freestyle project via Git webhook.</a> -- We're setting up a Jenkins “Freestyle project”, using “Execute shell” build step, to: ⓵ clone a Git repo, ⓶ create a virtual environment, ⓷ run editable install, and finally, ⓸ run Pytest. And this Jenkins job can be triggered remotely when we push some file(s) onto the target Git repo.
</li>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/06/20/ci-cd-05-jenkins-trigger-a-pipeline-via-git-webhook/" title="CI/CD #05. Jenkins: trigger a Pipeline via Git webhook." target="_blank">CI/CD #05. Jenkins: trigger a Pipeline via Git webhook.</a> -- We’re setting up a Jenkins “Pipeline script from SCM”, which uses a generic Bash script file to ⓵ create a virtual environment, ⓶ run editable install, and ⓷ run Pytest for all tests. And this Jenkins job can be triggered remotely when we push some file(s) onto the target Git repo.
</li>
</ol>

Thank you for reading... And I hope you find this post useful. Stay safe as always.

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
<a href="https://www.flaticon.com/free-icon/ssh_5261867?k=1687652052317" target="_blank">https://www.flaticon.com/free-icon/ssh_5261867?k=1687652052317</a>
</li>
<li>
<a href="https://pngimg.com/image/73422" target="_blank">https://pngimg.com/image/73422</a>
</li>
</ul>
