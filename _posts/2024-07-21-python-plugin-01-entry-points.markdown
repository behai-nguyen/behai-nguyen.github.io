---
layout: post
title: "Python Plugin: Entry Points"

description: I’m keen on exploring the architecture of Python plugins. It appears that the first step is to understand “Entry Points”. In this post, I will describe my own detailed implementation of the examples presented in the aforementioned documentation. 

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/07/116-01.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/07/116-02.png"

tags:
- Python
- Plugin
- Entry
- Point
---

<em>
I’m keen on exploring the architecture of Python plugins. It appears that the first step is to understand <a href="https://setuptools.pypa.io/en/latest/userguide/entry_point.html" title="Entry Points" target="_blank">Entry Points</a>. In this post, I will describe my own detailed implementation of the examples presented in the aforementioned documentation.
</em>

| ![116-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/07/116-feature-image.png) |
|:--:|
| *Python Plugin: Entry Points* |

The official documentation briefly mentions what to do, but it does not 
contain any precise instructions on how to do the mentioned task.
I had to guess. It turns out my guess was correct, so I want to write it 
down for future reference.

💥 Please note the following. ⓵ In the aforementioned official documentation, 
the <code>timmins-plugin-fancy</code> plugin does not know anything about 
the <code>timmins</code> application. To further my own understanding, I modified 
the <code>timmins-plugin-fancy</code> plugin in my study to have access to the 
<code>timmins</code> application’s “API”. ⓶ I also added a command of 
my own into the <code>timmins</code> application.

Below are the final directory structures of the two projects.

<a id="timmins-project-layout"></a>
❶ The <code>timmins</code> application: 

```
▶️Windows 10: F:\timmins\
▶️Ubuntu 22.10: /home/behai/timmins
.
├── pyproject.toml
├── src
│ └── timmins
│     ├── bonjour.py
│     ├── hello_world_gui.py
│     ├── __init__.py
│     └── __main__.py
└── venv/
```

<a id="plugin-project-layout"></a>
❷ The <code>timmins-plugin-fancy</code> plugin: 

```
▶️Windows 10: F:\timmins_plugin_fancy\
▶️Ubuntu 22.10: /home/behai/timmins_plugin_fancy
.
├── pyproject.toml
├── src
│ └── timmins_plugin_fancy
│     └── __init__.py
└── venv/
```

I followed the documentation step by step, incorporating my own code at the appropriate 
stages. Below, I am providing the final version of the content for the files in each 
project.

<a id="timmins-project-code"></a>
❶ The <code>timmins</code> application: 

<a id="timmins-project-toml"></a>
```
⓵ Content of /home/behai/timmins/pyproject.toml:
```

```toml
[build-system]
requires      = ["setuptools>=69.5.1", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "timmins"
version = "0.0.0"
description = "Learning Entry Point."

authors = [{ name = "Van Be Hai Nguyen", email = "behai_nguyen@hotmail.com" }]

dependencies = [
    'tomli; python_version >= "3.12"',
    'PySimpleGUI',
]

requires-python = ">=3.10"

[project.optional-dependencies]
build = [
    'build', 
]

[project.scripts]
hello-world = "timmins:hello_world"
ca-va = "timmins.bonjour:ca_va"

[project.gui-scripts]
hello-world-gui = "timmins.hello_world_gui:hello_world"
```

● We need the <a href="https://pypi.org/project/build/" title="build" 
target="_blank">build</a> package to create the distribution wheel file 
<code>timmins-0.0.0-py3-none-any.whl</code>.

● The <code>ca-va</code> command is my own code, added to enhance my understanding 
of how <code>project.scripts</code> works.

<a id="timmins-project-toml-gui-cmd"></a>
● The <code>hello-world-gui</code> is from the section 
<a href="https://setuptools.pypa.io/en/latest/userguide/entry_point.html#gui-scripts" 
title="GUI Scripts" target="_blank">GUI Scripts</a>. Instead of replacing 
the <code>hello_world()</code> console script, I use a separate module 
<code>hello_world_gui.py</code> and this new command.

<a id="timmins-project-init"></a>
```
⓶ Content of /home/behai/timmins/src/timmins/__init__.py:
```

```python
from importlib.metadata import entry_points

display_eps = entry_points(group='timmins.display')

"""
try:
    display = display_eps[0].load()
except IndexError:
    def display(text):
        print(text)
        
def hello_world():
    display('Hello world')
"""

# OR

"""
try:
    display = display_eps['lined'].load()
except KeyError:
    def display(text):
        print(text)

def hello_world():
    display('Hello world')
"""

def hello_world():
    for ep in display_eps:
        display = ep.load()
        display('Hello world')

def plugin_api():
    print("This is the timmins application plugin_api()")
```

Please note, the commented out codes are the prior steps discussed 
in the documentation which I carried out. They are all valid code. 
Everything should be self-explanatory.

<a id="timmins-project-init-api"></a>
👉 Please pay attention to the method <code>plugin_api()</code>. This is my own 
code, added to enhance my understanding of plugins. The <code>timmins-plugin-fancy</code> 
plugin will call this method.

To call this method, any plugin at all will have to install the 
<code>timmins-0.0.0-py3-none-any.whl</code> application package, 
which we will discuss in a <a href="#timmins-setup-package">later section</a>.

<a id="timmins-project-main"></a>
```
⓷ Content of /home/behai/timmins/src/timmins/__main__.py:
```

```python
from . import hello_world

if __name__ == '__main__':
    hello_world()
```

The content of this module is exactly as in the documentation.

<a id="timmins-project-bonjour"></a>
```
⓸ Content of /home/behai/timmins/src/timmins/bonjour.py:
```

```python
def ca_va():
    print("Bonjour, comment ça va?")
```

This module implements the <code>ca-va</code> command.

<a id="timmins-project-gui"></a>
```
⓹ Content of /home/behai/timmins/src/timmins/hello_world_gui.py:
```

```python
import PySimpleGUI as sg

def hello_world():
    sg.Window(title="Hello world", layout=[[]], margins=(100, 50)).read()
```

As <a href="#timmins-project-toml-gui-cmd">mentioned previously</a>, 
this module is from the section 
<a href="https://setuptools.pypa.io/en/latest/userguide/entry_point.html#gui-scripts" 
title="GUI Scripts" target="_blank">GUI Scripts</a>.

If you haven’t used the 
<a href="https://pypi.org/project/PySimpleGUI/" title="PySimpleGUI" target="_blank">PySimpleGUI</a> 
package before, you’ll need to register as a hobbyist to obtain a free product key.

<a id="plugin-project-code"></a>
❷ The <code>timmins-plugin-fancy</code> plugin: 

<a id="plugin-project-toml"></a>
```
⓵ Content of /home/behai/timmins_plugin_fancy/pyproject.toml:
```

```toml
[build-system]
requires      = ["setuptools>=61.0.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "timmins-plugin-fancy"
version = "0.0.3"
description = "timmins-plugin-fancy"
authors = [
    {name = "Van Be Hai Nguyen", email = "behai_nguyen@hotmail.com"}
]
maintainers = [
    {name = "Van Be Hai Nguyen", email = "behai_nguyen@hotmail.com"}
]

dependencies = [
    'tomli; python_version >= "3.10"',
]

requires-python = ">=3.10"

[project.optional-dependencies]

build = [
    "build", 
]

# Note the quotes around timmins.display in order to escape the dot .
[project.entry-points."timmins.display"]
excl = "timmins_plugin_fancy:excl_display"
lined = "timmins_plugin_fancy:lined_display"
```

<a id="plugin-project-init"></a>
```
⓶ Content of /home/behai/timmins_plugin_fancy/src/timmins_plugin_fancy/__init__.py:
```

```python
from timmins import plugin_api

def excl_display(text):
    plugin_api()
    print('!!!', text, '!!!')

def lined_display(text):
    plugin_api()
    print(''.join(['-' for _ in text]))
    print(text)
    print(''.join(['-' for _ in text]))
```

👉 Please note the import statement and the calls to the method 
<a href="#timmins-project-init-api">plugin_api()</a>. Apart from the 
<code>plugin_api()</code> method, the code in this module is identical 
to that in the documentation.

We will now describe the steps to set up and to run the examples. Recall the following:

● On Windows 10, the <code>timmins</code> application is in the <code>F:\timmins\</code> 
directory, on Ubuntu 22.10 it is <code>/home/behai/timmins/</code>.

● On Windows 10, the <code>timmins-plugin-fancy</code> plugin is in the 
<code>F:\timmins_plugin_fancy\</code> directory, on Ubuntu 22.10 it is 
<code>/home/behai/timmins_plugin_fancy/</code>.

<a id="timmins-setup"></a>
❶ Prepare and build the <code>timmins</code> application: 

Create the virtual environment <code>venv</code>:

```
▶️Windows 10: F:\timmins>C:\PF\Python312\python.exe -m venv venv
▶️Ubuntu 22.10: behai@hp-pavilion-15:~/timmins$ /usr/local/bin/python3.12 -m venv venv
```

Activate the virtual environment <code>venv</code>:

```
▶️Windows 10: F:\timmins>venv\Scripts\activate
▶️Ubuntu 22.10: behai@hp-pavilion-15:~/timmins$ source ./venv/bin/activate
```

Editable install the required dependencies:

```
▶️Windows 10: (venv) F:\timmins>venv\Scripts\pip.exe install -e .
▶️Ubuntu 22.10: (venv) behai@hp-pavilion-15:~/timmins$ ./venv/bin/pip install -e .
```

Editable install the optional <code>build</code> dependencies:

```
▶️Windows 10: (venv) F:\timmins>venv\Scripts\pip.exe install -e .[build]
▶️Ubuntu 22.10: (venv) behai@hp-pavilion-15:~/timmins$ ./venv/bin/pip install -e .[build]
```

<a id="timmins-setup-package"></a>
Create the distribution wheel file <code>timmins-0.0.0-py3-none-any.whl</code>:

```
▶️Windows 10: (venv) F:\timmins>venv\Scripts\python.exe -m build
▶️Ubuntu 22.10: (venv) behai@hp-pavilion-15:~/timmins$ ./venv/bin/python -m build
```

A new sub-directory <code>./dist</code> is created, the wheel file 
<code>timmins-0.0.0-py3-none-any.whl</code> is in there, together with 
<code>timmins-0.0.0.tar.gz</code>.

👉 Copy the <code>timmins-0.0.0-py3-none-any.whl</code> file to the root 
directory of the <code>timmins-plugin-fancy</code> plugin, which is 
<code>F:\timmins_plugin_fancy\</code> on Windows 10 and 
<code>/home/behai/timmins_plugin_fancy/</code> on Ubuntu 22.10.

<a id="plugin-setup"></a>
❷ Prepare and build the <code>timmins-plugin-fancy</code> plugin: 

Create the virtual environment <code>venv</code>:

```
▶️Windows 10: F:\timmins_plugin_fancy>C:\PF\Python312\python.exe -m venv venv
▶️Ubuntu 22.10: behai@hp-pavilion-15:~/timmins_plugin_fancy$ /usr/local/bin/python3.12 -m venv venv
```

Activate the virtual environment <code>venv</code>:

```
▶️Windows 10: F:\timmins_plugin_fancy>venv\Scripts\activate
▶️Ubuntu 22.10: behai@hp-pavilion-15:~/timmins_plugin_fancy$ source ./venv/bin/activate
```

Editable install the required dependencies:

```
▶️Windows 10: (venv) F:\timmins_plugin_fancy>venv\Scripts\pip.exe install -e .
▶️Ubuntu 22.10: (venv) behai@hp-pavilion-15:~/timmins_plugin_fancy$ ./venv/bin/pip install -e .
```

Install the <code>timmins</code> application wheel file, 
<code>timmins-0.0.0-py3-none-any.whl</code>, which was created 
and copied over in the <a href="#timmins-setup-package">previous step</a>:

```
▶️Windows 10: (venv) F:\timmins_plugin_fancy>venv\Scripts\pip.exe install timmins-0.0.0-py3-none-any.whl
▶️Ubuntu 22.10: (venv) behai@hp-pavilion-15:~/timmins_plugin_fancy$ ./venv/bin/pip install timmins-0.0.0-py3-none-any.whl
```

Editable install the optional <code>build</code> dependencies:

```
▶️Windows 10: (venv) F:\timmins_plugin_fancy>venv\Scripts\pip.exe install -e .[build]
▶️Ubuntu 22.10: (venv) behai@hp-pavilion-15:~/timmins_plugin_fancy$ ./venv/bin/pip install -e .[build]
```

<a id="plugin-setup-package"></a>
Create the distribution wheel file <code>timmins_plugin_fancy-0.0.3-py3-none-any.whl</code>:

```
▶️Windows 10: (venv) F:\timmins_plugin_fancy>venv\Scripts\python.exe -m build
▶️Ubuntu 22.10: (venv) behai@hp-pavilion-15:~/timmins_plugin_fancy$ ./venv/bin/python -m build
```

A new sub-directory <code>./dist</code> is created, the wheel file 
<code>timmins_plugin_fancy-0.0.3-py3-none-any.whl</code> is in there, together with 
<code>timmins_plugin_fancy-0.0.3.tar.gz</code>.

👉 Copy the <code>timmins_plugin_fancy-0.0.3-py3-none-any.whl</code> to 
the <code>timmins</code> application, which is 
<code>F:\timmins\</code> on Windows 10 and <code>/home/behai/timmins/</code> 
on Ubuntu 22.10.

<a id="timmins-final"></a>
❸ Running the <code>timmins</code> application: 

Install the <code>timmins-plugin-fancy</code> plugin wheel file, 
<code>timmins_plugin_fancy-0.0.3-py3-none-any.whl</code>, which was 
created and copied over in the <a href="#plugin-setup-package">previous step</a>:

```
▶️Windows 10: (venv) F:\timmins>venv\Scripts\pip.exe install timmins_plugin_fancy-0.0.3-py3-none-any.whl
▶️Ubuntu 22.10: (venv) behai@hp-pavilion-15:~/timmins$ ./venv/bin/pip install timmins_plugin_fancy-0.0.3-py3-none-any.whl
```

We are now ready to run all commands implemented by the application. They are:

<strong>▶️Windows 10:</strong>

```
(venv) F:\timmins>venv\Scripts\python -m timmins
(venv) F:\timmins>hello-world
(venv) F:\timmins>ca-va
(venv) F:\timmins>hello-world-gui
```

<strong>▶️Ubuntu 22.10:</strong>

```
(venv) behai@hp-pavilion-15:~/timmins$ ./venv/bin/python -m timmins
(venv) behai@hp-pavilion-15:~/timmins$ hello-world
(venv) behai@hp-pavilion-15:~/timmins$ ca-va
```

The screenshots below illustrate the responses from each command.
I hope they make sense to you:

{% include image-gallery.html list=page.gallery-image-list %}
<br/>

I didn’t run the <code>hello-world-gui</code> command on Ubuntu 22.10 because 
my laptop is in another room. I was running an <code>SSH</code> session and 
didn’t feel like fetching the laptop. 😂

This is the first time I’ve delved into this area of Python. I hope to build 
a system that can extend its functionalities through plugins. I believe this 
is the first step towards building such a system.

I am not sure if the approach I have described in this post is the best to 
fully implement the examples. Please treat it as my learning attempts only, 
and keep an open mind that there can be better approaches.

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
