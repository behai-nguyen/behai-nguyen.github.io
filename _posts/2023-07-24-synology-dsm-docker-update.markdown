---
layout: post
title: "Synology DS218: sudo password and unsupported Docker problems update..."

description: I have been updating the DSM without running sudo or docker. I have just tried both recently, both failed. I'm describing how I've managed to fix these two problems. 
tags: 
- Synology
- DS218
- sudo 
- Docker
---

<em>I have been updating the DSM without running <code>sudo</code> or <code>docker</code>. I have just tried both recently, both failed. I'm describing how I've managed to fix these two problems.</em>

| ![075-feature-image.png](https://behainguyen.files.wordpress.com/2023/07/075-feature-image.png) |
|:--:|
| *Synology DS218: sudo password and unsupported Docker problems update...* |

❶ The problem with <code>sudo</code> not accepting admin password.

Since July, 2022, I've applied <code>DSM</code> updates as they 
came out. But I've not been running command lines on it. Recently, 
during this July, 2023, I <code>ssh</code>ed into it using the normal 
admin password, this works as before, but once in the shell, 
<code>sudo</code> refused to accept the admin password. 

This seems to be a recurring problem. Suggestions to fix are very different,
and some are very complicated. I did try some simple ones, none worked for 
me.

Since my <code>DSM</code> was already outdated, and 
<code>DSM 7.2-64570 Update 1</code> was available, I applied that: and
<code>sudo</code> just works once again.

-- I am not sure when it will break!

❷ Problem with the unsupported Docker installation.

We've previously covered installing Docker for unsupported <code>AArch64</code> 
processors in
<a href="https://behainguyen.wordpress.com/2022/07/20/synology-ds218-unsupported-docker-installation-and-usage/"
title="Synology DS218: unsupported Docker installation and usage..."
target="_blank">Synology DS218: unsupported Docker installation and usage...</a>

Now having <code>sudo</code> working, I started Docker <code>daemon</code> with:

```
$ sudo dockerd &
```

The command line responded with command not found error. I could not 
find anything related to Docker under <code>/usr/bin/</code>, but 
other Docker files that I am aware of seem to be still in place. It 
would seem that updating the <code>DSM</code> has cleaned out Docker 
executable files. This is my assumption -- only. I'm keeping this 
in mind to verify at the next <code>DSM</code> update.

I just downloaded the latest version, which is 
<a href="https://download.docker.com/linux/static/stable/aarch64/docker-24.0.4.tgz"
title="docker-24.0.4.tgz" target="_blank"><code>docker-24.0.4.tgz</code></a>, and
carry the out installation steps in the above mentioned post: Docker works again,
including the Portainer, and previous existing volumes.

Thank you for reading. And stay safe as always.

✿✿✿

Feature image source:

<ul>
<li>
<a href="https://www.stickpng.com/img/icons-logos-emojis/tech-companies/jenkins-logo-landscape" target="_blank">https://www.stickpng.com/img/icons-logos-emojis/tech-companies/jenkins-logo-landscape</a>
</li>
</ul>
