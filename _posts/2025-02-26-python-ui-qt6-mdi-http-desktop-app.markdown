---
layout: post
title: "Python UI: A PyQt6 MDI HTTP Client Application"

description: An experimental HTTP client desktop application built using the PyQt6 GUI library, version 6.8.0, released on December 13, 2024. The server is the existing FastAPI Learning server, with the repository available at https://github.com/behai-nguyen/fastapi_learning.
tags:
- Python
- UI
- PyQt6
- PyQt
- Qt Designer
- FastAPI
- Server
---

<em>
An experimental HTTP client desktop application built using the <a href="https://pypi.org/project/PyQt6/" title="PyQt6" target="_blank">PyQt6</a> GUI library, version <code>6.8.0</code>, released on <code>December 13, 2024</code>.
</em>

<em>
The server is the existing <code>FastAPI Learning</code> server, with the repository available at <a href="https://github.com/behai-nguyen/fastapi_learning" title="FastAPI Learning" target="_blank">https://github.com/behai-nguyen/fastapi_learning</a>.
</em>

| ![136-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/02/136-feature-image.png) |
|:--:|
| *Python UI: A PyQt6 MDI HTTP Client Application* |

<a id="prerequisite"></a>
<p>
❶ This post utilises the HTTP libraries and the Qt Designer Application discussed in the following posts:
</p>

<ol>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2024/12/17/the-python-urllib3-http-library-and-ssl-https-for-localhost/" 
title="The Python urllib3 HTTP Library and SSL/HTTPS for localhost" 
target="_blank">The Python urllib3 HTTP Library and SSL/HTTPS for localhost</a>
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2024/12/20/python-ui-the-qt-designer-application-and-the-pyqt6-ui-library/" 
title="Python UI: The Qt Designer Application and the PyQt6 UI Library" 
target="_blank">Python UI: The Qt Designer Application and the PyQt6 UI Library</a>
</li>
</ol>

<p>
If readers are not yet familiar with these topics, it might be beneficial to read the above posts first.
</p>

<a id="app-specifics"></a>
<p>
❷ We will not discuss the implementation in detail. Instead, we will list some specific features and implementations of the application. It is up to the readers to explore further, as the code is fairly simple. We will also provide a video showing the application in action.
</p>

<a id="app-features-and-implementations"></a>

<a id="app-features"></a>

<h4>Application Features</h4>
<p>
⓵ Runtime Environment File: <code>.env</code>
</p>

<p>
● We configure where the server is running and the list of endpoints.
</p>

<p>
● We also have a Boolean <code>DEVELOPMENT_MODE</code> entry. 
When <code>True</code>, we attempt to load a cached JSON Web Token (JWT) from:
</p>

<ul>
<li style="margin-top:10px;">
<strong>Windows 10</strong>: <code>C:\Users\behai\AppData\Local\Temp\qt6_desktop_app\qt6_desktop_app.txt</code>
</li>
<li style="margin-top:10px;">
<strong>Ubuntu</strong>: <code>/tmp/qt6_desktop_app/qt6_desktop_app.txt</code>
</li>
</ul>

<p>
To remove this cached JWT file, use the following script:
</p>

<ul>
<li style="margin-top:10px;">
<strong>Windows 10</strong>: <code>remove_stored_token.bat</code>
</li>
<li style="margin-top:10px;">
<strong>Ubuntu</strong>: <code>remove_stored_token.sh</code>
</li>
</ul>

<p>
⓶ Theme File: <code>theme.toml</code>
</p>

<p>
We take advantage of 
<a href="https://pypi.org/project/PyQt6/" title="The PyQt6 library" target="_blank">PyQt6</a> 
<a href="https://developer.mozilla.org/en-US/docs/Web/CSS" 
title="Cascading Style Sheets (CSS)" target="_blank">Cascading Style Sheets (CSS)</a> 
support to implement a simple background color feature for the application. This is an experimental attempt, setting a foundation for future expansion.
</p>

<a id="app-impl-specifics"></a>

<h4>Application Implementation Specifics</h4>

<p>
⓵ We are using the 
<a href="https://behainguyen.wordpress.com/2024/12/20/python-ui-the-qt-designer-application-and-the-pyqt6-ui-library/#install-qt-designer" 
title="QT Designer" target="_blank">QT Designer</a> application to create 
the application screens. To convert the designed screens into Python modules 
<a href="https://behainguyen.wordpress.com/2024/12/20/python-ui-the-qt-designer-application-and-the-pyqt6-ui-library/#pyqt6-installation-usage" 
title="Convert QT Design UI into Python" 
target="_blank">as discussed</a>, use the provided script: 
</p>

<ul>
<li style="margin-top:10px;">
<strong>Windows 10</strong>: <code>convert_ui_to_py.bat</code>
</li>
<li style="margin-top:10px;">
<strong>Ubuntu</strong>: <code>convert_ui_to_py.sh</code>
</li>
</ul>

<p>
The designed screens are in the 
<a href="https://github.com/behai-nguyen/qt6_desktop_app/tree/80014cea5d1404d6fa5f4fb2b481191c6ae45332/src/qt6_desktop_app/templates" 
title="src/qt6_desktop_app/templates" target="_blank">src/qt6_desktop_app/templates</a>
directory of the repository. The Python modules and their subclass modules are in the 
<a href="https://github.com/behai-nguyen/qt6_desktop_app/tree/80014cea5d1404d6fa5f4fb2b481191c6ae45332/src/qt6_desktop_app/templates" 
title="src/qt6_desktop_app/ui" target="_blank">src/qt6_desktop_app/ui</a> directory.
</p>

<p>
⓶ We use the 
<a href="https://behainguyen.wordpress.com/2024/12/20/python-ui-the-qt-designer-application-and-the-pyqt6-ui-library/#install-qt-designer" 
title="QT Designer" target="_blank">QT Designer</a> 
QT Designer layout feature to layout the screens. I have found that this layout feature can be a bit hard to get right.
</p>

<a id="app-impl-uis-enabled"></a>
<p>
⓷ Unlike the web application, where we can optionally 
<a href="https://behainguyen.wordpress.com/2024/10/19/python-fastapi-oauth2-scopes-part-02-ui-elements-and-user-assigned-scopes/" 
title="Python FastAPI: OAuth2 Scopes Part 02 - UI Elements and User-Assigned Scopes" 
target="_blank">disable UIs</a> 
based on the logged-in user's scope assignment, in this application the UIs are always enabled. Permissions are checked at the server end only. The logged-in user's assigned scopes are in the payload of the JWT. To get the scopes, this application must decode the JWT token, which is rather messy. It is better to implement a separate API to query users' assigned scopes. We might implement this in the future.
</p>

<p>
⓸ We take full advantage of 
<a href="https://pypi.org/project/PyQt6/" title="The PyQt6 library" target="_blank">PyQt6</a>'s 
Signals, Slots, and Events features to reduce interdependency between functionalities. I have found that it is similar to traditional Windows messaging.
</p>

<p>
⓹ The module <code>server_api.py</code> under the 
<a href="https://github.com/behai-nguyen/qt6_desktop_app/tree/80014cea5d1404d6fa5f4fb2b481191c6ae45332/src/qt6_desktop_app/middleware" 
title="src/qt6_desktop_app/middleware" target="_blank">src/qt6_desktop_app/middleware</a> 
provides all HTTP wrapper methods which submit requests to the server. 
</p>

<p>
⓺ The component which displays the logged-in user information in HTML is the 
<a href="https://pypi.org/project/PyQt6-WebEngine/" 
title="PyQt6-WebEngine - Python Bindings for the Qt WebEngine Framework" 
target="_blank">PyQt6-WebEngine - Python Bindings for the Qt WebEngine Framework</a> 
library. In fact, it displays the same HTML page as the web application.
</p>

<p>
Since we are using a self-signed certificate, this component generates the following error. I understand what it is, but I don't yet know how to address it:
</p>

```
[5832:5708:0226/110010.891:ERROR:cert_verify_proc_builtin.cc(874)] CertVerifyProcBuiltin for 192.168.0.16 failed:
----- Certificate i=0 (emailAddress=behai_nguyen@hotmail.com,CN=DESKTOP-7BA02KU,OU=Development,O=Personal,L=Melbourne,ST=Victoria,C=AU) -----
ERROR: No matching issuer found


[5832:19644:0226/110010.892:ERROR:ssl_client_socket_impl.cc(970)] handshake failed; returned -1, SSL error code 1, net_error -202
[5832:19644:0226/110010.916:ERROR:ssl_client_socket_impl.cc(970)] handshake failed; returned -1, SSL error code 1, net_error -202
```

<a id="application-video"></a>
<p>
❸ And finally, this is the video showing the application running on both Windows 10 and Ubuntu 24.04:
</p>

[![Watch the video](https://img.youtube.com/vi/CegAXXz84p8/maxresdefault.jpg)](https://youtu.be/CegAXXz84p8)

<a id="concluding-remarks"></a>
<p>
❹ I want to understand 
<a href="https://pypi.org/project/PyQt6/" title="The PyQt6 library" target="_blank">PyQt6</a> 
better, so I wrote this little application. I hope you find it interesting too.
</p>

<p>
Thank you for reading. I hope you find the information in this post useful. Stay safe, as always.
</p>


<p>✿✿✿</p>

<p>
Feature image sources:
</p>

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
