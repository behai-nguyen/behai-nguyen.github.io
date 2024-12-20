---
layout: post
title: "Python UI: The Qt Designer Application and the PyQt6 UI Library"

description: In this article, we will first discuss how to install the desktop UI designer application known as Qt Designer from Qt Software. We will install Qt Designer as a system-wide independent application on both Windows 10 and Ubuntu 24.04. Next, we will briefly discuss using Qt Designer to make a simple dialog with two buttons. In the third step, we install the Python PyQt software version 6, the PyQt6 library. Still in this third step, we are using a utility that comes with PyQt6 to convert the dialog we made in the second step into Python code. In the fourth step, we write a simple Python script which subclasses the generated dialog in the previous step, adds some code to the subclass, and displays the dialog. Finally, we discuss some background information.

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/12/130-01-ubuntu.png"

gallery-image-list-2:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/12/130-02-windows.png"

gallery-image-list-3:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/12/130-03-windows.png"

gallery-image-list-4:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/12/130-04-ubuntu.png"

gallery-image-list-5:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/12/130-05-windows.png"

gallery-image-list-6:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/12/130-06-ubuntu.png"

gallery-image-list-7:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/12/130-07-ubuntu.png"

tags:
- Python
- UI
- PyQt6
- PyQt
- Qt Designer
---

<em>
In this article, we will first discuss how to install the desktop UI designer application known as <strong>Qt Designer</strong> from <a href="https://www.qt.io/" title="The Qt Group" target="_blank">Qt Software</a>. We will install Qt Designer as a system-wide independent application on both Windows 10 and Ubuntu 24.04. Next, we will briefly discuss using Qt Designer to make a simple dialog with two buttons.
</em>

<em>
In the third step, we install the Python <a href="https://en.wikipedia.org/wiki/PyQt" title="PyQt" target="_blank">PyQt</a> software version 6, the <a href="https://pypi.org/project/PyQt6/" title="The PyQt6 library" target="_blank">PyQt6</a> library. Still in this third step, we are using a utility that comes with PyQt6 to convert the dialog we made in the second step into Python code. In the fourth step, we write a simple Python script which subclasses the generated dialog in the previous step, adds some code to the subclass, and displays the dialog. Finally, we discuss some background information.
</em>

| ![130-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/12/130-feature-image.png) |
|:--:|
| *Python UI: The Qt Designer Application and the PyQt6 UI Library* |

<a id="install-qt-designer"></a>
❶ <strong>Install Qt Designer as a System-Wide Independent Application</strong>

Please note that <strong><em>independent</em></strong> means not depending on the 
<a href="https://pypi.org/project/pyqt6-tools/" 
title="The pyqt6-tools library" target="_blank">pyqt6-tools</a> library 
<a href="#pyqt6-tools">as described</a> in a later section.

<a id="install-qt-designer-ubuntu"></a>
⓵ <strong>On Ubuntu 24.04</strong>

The instructions in this section are based on the 
<a href="https://askubuntu.com/questions/1532597/how-to-install-pyqt-6-designer-in-ubuntu-24-10" 
title="How to install PyQt 6 Designer in Ubuntu 24.10" target="_blank">How to install PyQt 6 Designer in Ubuntu 24.10</a> 
post. Run the following commands to install:

```
$ sudo apt install qt6-base-dev
$ sudo apt install qt6-tools-dev
```

The location of the executable is <code>/usr/lib/qt6/bin/designer</code>. 
We can verify with the following command:

```
behai@HP-Pavilion-15:~$ ls -l /usr/lib/qt6/bin/designer
```

For my installation, the output is:

```
-rwxr-xr-x 1 root root 564576 Apr 16  2024 /usr/lib/qt6/bin/designer
```

To create an entry for Qt Designer in the Application area, we need to create the 
<code>/home/behai/.local/share/application/desginer.desktop</code> file.
Replace <strong><code>behai</code></strong> with your own user name.

```
Content of /home/behai/.local/share/application/desginer.desktop:
```

```
[Desktop Entry]
Version=1.0
Name=Qt Designer 6
Comment=Qt Designer 6
Exec=/usr/lib/qt6/bin/designer
Icon=/home/behai/.local/share/applications/qt.ico
Terminal=false
Type=Application
Categories=Utility;Application;
```

The icon located at <code>/home/behai/.local/share/applications/qt.ico</code> is sourced from 
<a href="https://www.shareicon.net/qt-101908" title="qt.ico" target="_blank">qt.ico</a>.
Finally, set the required permissions for designer.desktop:

```
$ chmod 755 designer.desktop
```

💥 I have found that I have to reboot to get the icon to display. Please see the screenshot below: 

{% include image-gallery.html list=page.gallery-image-list-1 %}
<br/>

<a id="install-qt-designer-windows"></a>
⓶ <strong>On Windows 10</strong>

It is fairly simple. Download the installation file <code>Qt Designer Setup.exe</code> 
from <a href="https://build-system.fman.io/qt-designer-download" 
title="Qt Designer Download" target="_blank">Qt Designer Download</a>, it is only 
40MB. After a successful installation, Qt Designer should appear in the Start Menu as shown in the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-2 %}
<br/>

<a id="qt-designer-usage"></a>
❷ <strong>Qt Designer Usage</strong>

<a id="qt-designer-usage-windows"></a>
⓵ <strong>On Windows 10</strong>

On starting, Qt Designer greets us with the <strong>New Form - Qt Designer</strong> window, 
where we can choose what we want to create. Select the first entry, 
<code>Dialog with Buttons Bottom</code>. Then, on the right-hand side, under the last entry 
<code>Display Widgets</code>, drag and drop a <code>Label</code> onto the dialog. 
Use the <code>QWidget Property Editor</code> on the right-hand side to change the label to something, as shown in the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-3 %}
<br/>

I saved this dialog to <code>F:\pydev\designer_ui\learn_dlg.ui</code>. It is in 
<a href="https://en.wikipedia.org/wiki/XML" title="XML Format" target="_blank">XML format</a>.

<a id="qt-designer-usage-ubuntu"></a>
⓶ <strong>On Ubuntu 24.04</strong>

I don't want to start from the beginning, so I just copied 
<code>F:\pydev\designer_ui\learn_dlg.ui</code> from Windows 10 to 
the corresponding directory on Ubuntu 24.04: <code>~/pydev/designer_ui/learn_dlg.ui</code>.
Double-click on the Qt Designer icon in the Application area, as 
<a href="#install-qt-designer-ubuntu">previously discussed</a>, 
then open <code>~/pydev/designer_ui/learn_dlg.ui</code>:

{% include image-gallery.html list=page.gallery-image-list-4 %}
<br/>

It looks better than the Windows 10 one; the buttons have icons like the classic Borland Delphi form designer. 
To get finer positional placements and sizes, under the 
<code>QWidget Property Editor</code> on the right-hand side, look for 
<code><strong>geometry</strong></code>. We can use the keyboard to punch in the coordinates and sizes for each widget, allowing for finer adjustments by directly entering the numbers rather than using the mouse to drag them around.

<a id="pyqt6-installation-usage"></a>
❸ <strong>The 
<a href="https://pypi.org/project/PyQt6/" title="The PyQt6 library" target="_blank">PyQt6</a> 
Library Installation and Usage</strong>

The active virtual environment is <code>F:\pydev\venv</code> on Windows 10 
and <code>/home/behai/pydev/venv</code> on Ubuntu 24.04. Install <code>PyQt6</code> 
using the following command:

```
▶️Windows 10: .\venv\Scripts\pip.exe install PyQt6
▶️Ubuntu 24.04: ./venv/bin/pip install PyQt6
```

<!--
https://stackoverflow.com/questions/66613380/downloading-qtdesigner-for-pyqt6-and-converting-ui-file-to-py-file-with-pyuic6
Downloading QtDesigner for PyQt6 and converting .ui file to .py file with pyuic6
-->
The following discussion is based on <a href="https://stackoverflow.com/a/66621465" 
title="Downloading QtDesigner for PyQt6 and converting .ui file to .py file with pyuic6" 
target="_blank">this discussion</a>. 👉 Please note that the sub-directory <code>pydev/py_ui/</code> must be created first.

<a id="pyqt6-covert-ui-to-py-ubuntu"></a>
⓵ <strong>On Ubuntu 24.04</strong>

To convert <code>/behai/home/pydev/designer_ui/learn_dlg.ui</code> to
<code>/behai/home/pydev/py_ui/learn_dlg.py</code>, either of the below commands will work:

```
$ ./venv/bin/pyuic6 -o ./py_ui/learn_dlg.py -x ./designer_ui/learn_dlg.ui
$ ./venv/bin/python -m PyQt6.uic.pyuic -o ./py_ui/learn_dlg.py -x ./designer_ui/learn_dlg.ui
```

💥 As <code>/home/behai/pydev/py_ui/learn_dlg.py</code> is a generated module, the next time the conversion takes place, it gets overwritten. In our code, we must subclass it rather than adding code directly to it.

<a id="pyqt6-covert-ui-to-py-windows"></a>
⓶ <strong>On Windows 10</strong>

The commands are similar:

```
.\venv\Scripts\pyuic6.exe -o .\py_ui\learn_dlg.py -x .\designer_ui\learn_dlg.ui
.\venv\Scripts\python.exe -m PyQt6.uic.pyuic -o .\py_ui\learn_dlg.py -x .\designer_ui\learn_dlg.ui
```

The generated module <code>./py_ui/learn_dlg.py</code> is fairly straightforward. Most of the code is about preparing the UI widgets, and it assumes that the methods for the buttons' click events exist.

<a id="pyqt6-example"></a>
❹ <strong>
<a href="https://pypi.org/project/PyQt6/" title="The PyQt6 library" target="_blank">PyQt6</a> 
Example: Subclassing <code>./pydev/py_ui/learn_dlg.py's Class Ui_Dialog</code></strong>

The script below implements the click-events for each button. To shut down the script, users need to click on the dialog's <code>Close</code> button.

```python
import sys

from PyQt6.QtWidgets import QMainWindow

from py_ui.learn_dlg import *

class LearnPyQtWindow(QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowType.CustomizeWindowHint | 
                            QtCore.Qt.WindowType.WindowCloseButtonHint )
        self.show()

    def accept(self):
    
    print("You clicked the OK button...")
        # Enable self.close() to close the dialog on clicking.
        # self.close()

    def reject(self):
        print("You clicked the Cancel button...")
        # Enable self.close() to close the dialog on clicking.
        # self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    login = LearnPyQtWindow()
    sys.exit(app.exec())
```

Let's briefly explain the script:

● Turning off the dialog's <code>Maximize</code> and <code>Minimize</code> buttons:

```
        self.setWindowFlags(QtCore.Qt.WindowType.CustomizeWindowHint | 
                            QtCore.Qt.WindowType.WindowCloseButtonHint )
```

This line actually means only the dialog's <code>Close</code> button is shown.

● The <code>accept</code> and <code>reject</code> methods:
These are the buttons' click-event methods that the generated module 
<code>./pydev/py_ui/learn_dlg.py</code> assumes are implemented. See lines 33 and 34:

<figure class="highlight"><pre><code class="language-python" data-lang="python"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">33
34
</pre></td><td class="code"><pre>        <span class="bp">self</span><span class="p">.</span><span class="n">buttonBox</span><span class="p">.</span><span class="n">accepted</span><span class="p">.</span><span class="n">connect</span><span class="p">(</span><span class="n">Dialog</span><span class="p">.</span><span class="n">accept</span><span class="p">)</span> <span class="c1"># type: ignore
</span>        <span class="bp">self</span><span class="p">.</span><span class="n">buttonBox</span><span class="p">.</span><span class="n">rejected</span><span class="p">.</span><span class="n">connect</span><span class="p">(</span><span class="n">Dialog</span><span class="p">.</span><span class="n">reject</span><span class="p">)</span> <span class="c1"># type: ignore</span>
</pre></td></tr></tbody></table></code></pre></figure>

On Windows 10, the script shows:

{% include image-gallery.html list=page.gallery-image-list-5 %}
<br/>

We can see that only the <code>Close</code> button is visible and functional. The dialog is shown in the center of the screen; I did not set this position in the design—it is its default behavior.

On Ubuntu 24.04, the script shows:

{% include image-gallery.html list=page.gallery-image-list-6 %}
<br/>

The <code>Maximize</code> and <code>Minimize</code> buttons are visible but disabled. The <code>Close</code> button is functional. 💥 The dialog is not centered on the screen as it is on Windows 10.

<a id="pyqt6-tools"></a>
❺ <strong>The 
<a href="https://pypi.org/project/pyqt6-tools/" 
title="The pyqt6-tools library" target="_blank">pyqt6-tools</a> Library, 
Released: Mar 28, 2023</strong>

On Windows 10, I first installed Qt Designer with the <code>pyqt6-tools</code> library, 
but only with Python version <strong>3.11.9</strong>; versions 
<strong>3.12.xx</strong> and <strong>3.13.xx</strong> fail to install 
<code>pyqt6-tools</code>. In a virtual environment <code>venv</code>, 
the Qt Designer executable location is 
<code>.\venv\Lib\site-packages\qt6_applications\Qt\bin\designer.exe</code>.

On Ubuntu 24.04, Python <strong>3.11.xx</strong> is no longer available.
I have version <strong>3.13.0</strong> installed. Installing <code>pyqt6-tools</code> 
using Python <code>3.13.0</code> results in other errors as well. Please see the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-7 %}
<br/>

Trying to solve these problems has led me to the realization that the Qt Designer application can be installed as an independent application, <a href="#install-qt-designer">as discussed</a>. This should make sense too, as we do not need this application on a per-virtual-environment basis.

<a id="the-qt-group"></a>
❻ While trying to sort out the problems with installing Qt Designer, I came across 
<a href="https://www.qt.io/" title="The Qt Group" target="_blank">The Qt Group</a> 
website, where they offer a <a href="https://www.qt.io/download-qt-installer-oss" 
title="Qt Installer" target="_blank">Qt Installer</a> application for download. 
The installer itself is about 50 MB. When I ran it, the default installation requires <strong>300 GB</strong> (three hundred gigabytes). 
I attempted to turn off most options, leaving only what I assumed would install the Qt Designer application, but it still required around <strong>40 GB</strong>—so I abandoned it altogether.

<a id="other-resources"></a>
❼ Other related sites that I find helpful:

<ol>
<li style="margin-top:10px;">
<a href="https://www.tutorialspoint.com/pyqt5" title="PyQt5 Tutorial" target="_blank">PyQt5 Tutorial</a> 
-- I started off learning 
<a href="https://en.wikipedia.org/wiki/PyQt" title="PyQt" target="_blank">PyQt</a> 
with this site. I completed all the tutorials, and then I found out that 
<a href="https://pypi.org/project/PyQt6/" title="The PyQt6 library" target="_blank">PyQt6</a> 
is the latest version.
</li>

<li style="margin-top:10px;">
<a href="https://www.pythonguis.com/" title="PythonGUIs" target="_blank">PythonGUIs</a> 
-- I have found some useful information on 
<a href="https://pypi.org/project/PyQt6/" title="The PyQt6 library" target="_blank">PyQt6</a> 
from this site.
</li>
</ol>	

<a id="concluding-remarks"></a>
❽ Having successfully gathered the information to install the Qt Designer application on both operating systems is satisfying. The information is readily available on the internet, but strangely enough, not centralized. I still have not figured out the actual official home page for the Qt Designer application yet 😂... I assume it is the <a href="https://www.qt.io/" title="The Qt Group" target="_blank">Qt Group</a> website.

Thank you for reading. I hope you find the information in this post useful. Stay safe, as always.

✿✿✿

Feature image sources:

<ul>
<li>
<a href="https://www.omgubuntu.co.uk/2024/03/ubuntu-24-04-wallpaper" target="_blank">https://www.omgubuntu.co.uk/2024/03/ubuntu-24-04-wallpaper</a>
</li>
<li>
<a href="https://in.pinterest.com/pin/337277459600111737/" target="_blank">https://in.pinterest.com/pin/337277459600111737/</a>
</li>
<li>
<a href="https://www.python.org/downloads/release/python-3124/" target="_blank">https://www.python.org/downloads/release/python-3124/</a>
</li>
<li>
<a href="https://www.shareicon.net/qt-101908" target="_blank">https://www.shareicon.net/qt-101908</a>
</li>
</ul>
