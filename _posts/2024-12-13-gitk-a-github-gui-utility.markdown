---
layout: post
title: "Gitk: A “git log” GUI Utility"

description: In this YouTube video, the author mentions the Gitk GUI utility for GitHub, which I find interesting. Here, I will describe how to install it on Ubuntu and briefly look at its usage. 

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/12/128-01.png"

gallery-image-list-2:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/12/128-02.png"

gallery-image-list-3:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/12/128-03.png"

tags:
- git
- github
- gitk
- linux
---

<em>
In <a href="https://www.youtube.com/watch?v=_c1o8tqoR-0&list=PL9xPdBFt5g3Qnn3ZY2wYh7L2yzZ377UwI&index=5" title="LinuxCNC HAL #1(b): Using Linux efficiently" target="_blank">this YouTube video</a>, the author mentions the <code>Gitk</code> GUI utility for GitHub, which I find interesting. Here, I will describe how to install it on Ubuntu and briefly look at its usage.
</em>

| ![128-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/12/128-feature-image.png) |
|:--:|
| *Gitk: A “git log” GUI Utility* |

The <code>Gitk</code> GUI is free of charge. I spent some time looking for it on the internet, but I was unable to find its official home page. I installed it on Ubuntu 24.04.1 LTS (Noble Numbat) with the following command:

```
$ sudo apt install gitk
```

On the Ubuntu machine, navigate to a local directory where there is a valid <code>.git</code> sub-directory. For example, <code>/home/behai/fastapi_learning</code>, which is the working directory of the <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Python FastAPI learning series</a>. Then launch <code>Gitk</code> with the following command:

```
$ gitk
```

You will be greeted with the screen shown in the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-1 %}
<br/>

Please refer to the <a href="https://behainguyen.wordpress.com/2024/12/02/python-fastapi-finishing-off-the-pending-items-code-cleanup-and-improvements/" title="Python FastAPI: Finishing Off the Pending Items, Code Cleanup, and Improvements" target="_blank">last post</a> of this <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Python FastAPI learning series</a>. The last tag is <strong><code>v0.13.0</code></strong>,  which is shown in the first entry of the above screenshot. In the <a href="https://behainguyen.wordpress.com/2024/12/02/python-fastapi-finishing-off-the-pending-items-code-cleanup-and-improvements/#code-refactorings" title="Python FastAPI: Finishing Off the Pending Items, Code Cleanup, and Improvements" target="_blank">Complete GitHub check-in commands</a> section, the <code>README.md</code> file is the last file that was checked in, and it is shown first. The second entry is illustrated in the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-2 %}
<br/>

The <code>Gitk</code> application displays checked-in files in reverse order. Changes are shown in the bottom left pane of the screen, as illustrated in the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-3 %}
<br/>

The above screenshot shows two additions to the file. Removed text would be shown <span style="color:red;">in red</span>.

Note that running:

```
$ git log
```

from the same directory <code>/home/behai/fastapi_learning</code> results in similar outputs as shown in the above screenshots. However, it seems that the file names are not readily available.

I'm not sure if there is a Windows version of <code>Gitk</code> available. I couldn't find it. I have some other Windows utilities installed, such as <code>Git Bash</code> and <code>Git GUI</code>, but I don't find them very useful. <a href="https://git-scm.com/downloads/guis" title="Git GUI Clients" target="_blank">This site</a> lists other GitHub-related GUI applications, some of which are paid and some are free.

Thank you for reading. I hope you find the information in this post useful. Stay safe, as always.

✿✿✿

Feature image source:

<ul>
<li>
<a href="https://www.omgubuntu.co.uk/2024/03/ubuntu-24-04-wallpaper" target="_blank">https://www.omgubuntu.co.uk/2024/03/ubuntu-24-04-wallpaper</a>
</li>
</ul>
