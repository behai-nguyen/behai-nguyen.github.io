---
layout: post
title: "Installing Python 3.12.4 as an Additional Interpreter on Ubuntu 22.10 and Windows 10"

description: We describe the steps to install Python 3.12.4 as an additional interpreter on both Windows 10 and Ubuntu 22.10. This installation will add Python 3.12.4 while keeping the existing installations of other Python versions intact. 

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/113-01.png"

gallery-image-list-2:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/113-02.png"

gallery-image-list-3:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/113-03.png"

tags:
- Install
- Python 3.12.4
- installation
- Python
- 3.12.4
- 3.12
---

<em>
We describe the steps to install Python 3.12.4 as an additional interpreter on both Windows 10 and Ubuntu 22.10. This installation will add Python 3.12.4 while keeping the existing installations of other Python versions intact.
</em>

| ![113-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/06/113-feature-image.png) |
|:--:|
| *Installing Python 3.12.4 as an Additional Interpreter on Ubuntu 22.10 and Windows 10* |

<a id="on-windows-10"></a>
❶ Let's cover Windows 10 first, since it is simpler.

<ol>
<li style="margin-top:10px;">
Go to <a href="https://www.python.org/downloads/windows/" title="Python Releases for Windows" 
target="_blank">https://www.python.org/downloads/windows/</a> and download the 
appropriate installer for your Windows 10 machine, such as <code>python-3.12.4-amd64.exe</code>.
</li>
<li style="margin-top:10px;">
Run the installer as an Administrator. Choose the custom installation 
option to install it to <code>C:\PF\Python312\</code>.
</li>
</ol>	

Please note that the <code>C:\PF\Python312\Scripts\</code> directory now 
contains only the following executables: <code>pip.exe</code>, <code>pip3.12.exe</code> 
and <code>pip3.exe</code>. The executable <code>virtualenv.exe</code> is no longer 
included.

<a id="windows-10-venv-virtual-env"></a>
To create a virtual environment (<code>venv</code>) for Python 3.12.4, 
use the following command:

```
C:\PF\Python312\python.exe -m venv venv
```

<a id="on-ubuntu-22-10"></a>
❷ On Ubuntu 22.10, I succeeded the first time, but I just did 
not know where it was installed 😂.

On June 25, 2022, I installed Python 3.9 Beta on a non-Ubuntu Linux. Please 
refer to this post: 
<a href="https://behainguyen.wordpress.com/2022/06/25/synology-ds218-preparing-python-3-9-beta-compelete-devepment-environment/"
title="Synology DS218: preparing Python 3.9 Beta compelete development environment"
target="_blank">Synology DS218: preparing Python 3.9 Beta compelete development environment</a>. 
That was the only time I installed Python on a Linux system.

For Python 3.12.4, it appears we need to install it from the source code, as 
indicated on this 
<a href="https://www.python.org/downloads/source/" title="Python Source Releases" 
target="_blank">download page</a>.

I followed the instructions in the section “<em>Method 2: Install Python From Source Code</em>” 
from the post <a href="https://phoenixnap.com/kb/how-to-install-python-3-ubuntu" 
title="How to Install Python 3 on Ubuntu 20.04 or 22.04" 
target="_blank">How to Install Python 3 on Ubuntu 20.04 or 22.04</a>.

My steps are as follows:

<a id="ubuntu-22-10-step-1"></a>
⓵ Checking the currently active Python version and its installation path 
using the following commands:

```
python3 --version
which python3
```

Please refer to the illustration in the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-1 %}
<br/>

<a id="ubuntu-22-10-step-2"></a>
⓶ Download <code>Python-3.12.4.tgz</code> to <code>/home/behai/Public/</code>.

<a id="ubuntu-22-10-step-3"></a>
⓷ Extract the compressed files using the following command:

```
tar -xf /home/behai/Public/Python-3.12.4.tgz
```

The files are extracted to <code>/home/behai/Python-3.12.4/</code>.
Please see the screenshot illustration below:

{% include image-gallery.html list=page.gallery-image-list-2 %}
<br/>

<a id="ubuntu-22-10-step-4"></a>
⓸ Change to the directory <code>/home/behai/Python-3.12.4/</code>. 
The command is:

```
behai@hp-pavilion-15:~$ cd Python-3.12.4/
```

<a id="ubuntu-22-10-step-5"></a>
⓹ Test system and optimise Python. The command is:

```
behai@hp-pavilion-15:~/Python-3.12.4$ ./configure --enable-optimizations
```

This command produces a long output and takes a few minutes to complete. 
I did not encounter any problems.

<a id="ubuntu-22-10-step-6"></a>
⓺ Finally, install Python 3.12.4. As stated in the introduction, I want 
this version to be an additional installation, so the command is: 

```
behai@hp-pavilion-15:~/Python-3.12.4$ sudo make altinstall
```

It took nearly 20 minutes to complete, with a very long output. No errors were reported.

💥 <strong>I would like to point out that</strong> I had some vague ideas about what the above steps do: they compile and build the Python interpreter from the source. However, I did not know where Python 3.12.4 was installed. From the output, I knew the installation was successful, but I was unsure of the installation path for Python 3.12.4.

<a id="ubuntu-22-10-step-7"></a>
⓻ Verify Python version. I reran the first command from 
<a href="#ubuntu-22-10-step-1">Step 1</a>: 

```
python3 --version
```

I was unsure, but I was expecting Python 3.10.7. And it is.

<a id="ubuntu-22-10-step-8"></a>
⓼ 🐍 Python 3.12.4's path is <code>/usr/local/bin/python3.12</code>.

After some searching, I came across this page 
<a href="https://docs.python.org/3/using/unix.html#building-python" 
title="2.2. Building Python" 
target="_blank">https://docs.python.org/3/using/unix.html#building-python</a>,
which discusses installing Python from source code. This page led me to 
this section 
<a href="https://docs.python.org/3/using/configure.html#cmdoption-prefix" 
title="--prefix=PREFIX" 
target="_blank">https://docs.python.org/3/using/configure.html#cmdoption-prefix</a>.

These two pages effectively point out that the default installation location 
for the command <code>make altinstall</code> is <code>/usr/local</code>. 
I have been able to verify that. Please see the screenshot illustration below:

{% include image-gallery.html list=page.gallery-image-list-3 %}
<br/>

<a id="ubuntu-22-10-venv-virtual-env"></a>
To create a virtual environment (<code>venv</code>) for Python 3.12.4, 
use the following command:

```
behai@hp-pavilion-15:~/fastapi$ /usr/local/bin/python3.12 -m venv venv
```

🚀 Before writing this post, I tested the Python 3.12.4 installation by creating 
a virtual environment (<code>venv</code>) and running a web server application 
from this <code>venv</code>.

The installation of Python 3.12.4 as an additional interpreter on Ubuntu 22.10 and Windows 10 appears to be in working order.

Thank you for reading. I hope you find the information in this post useful. Stay safe, as always.

✿✿✿

Feature image source:

<ul>
<li>
<a href="https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper" target="_blank">https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper</a>
</li>
<li>
<a href="https://in.pinterest.com/pin/337277459600111737/" target="_blank">https://in.pinterest.com/pin/337277459600111737/</a>
</li>
<li>
<a href="https://www.python.org/downloads/release/python-3124/" target="_blank">https://www.python.org/downloads/release/python-3124/</a>
</li>
</ul>
