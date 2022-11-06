---
layout: post
title: "JavaScript and CSS minification."
description: I'm discussing minification of JavaScript and CSS using UglifyJS 3 and UglifyCSS packages.
tags:
- JavaScript
- CSS
- minify
- uglify
---

<em>I'm discussing minification of JavaScript and CSS using <strong>UglifyJS 3</strong> and <strong>UglifyCSS</strong> packages.</em>

| ![044-feature-image.png](https://behainguyen.files.wordpress.com/2022/11/044-feature-image.png) |
|:--:|
| <em><span style="color:rgb(17, 17, 17);">Web browsers: confirm leaving page when there is modified data.</span></em> |

In my understanding, 
<a href="https://www.npmjs.com/package/uglify-js" title="UglifyJS 3" target="_blank">UglifyJS 3</a>
is the most popular JavaScript minifier tool presently -- it has a very high weekly download too.
And as per the official documentation, it supports ES6.

For CSS, I've tried 
<a href="https://www.npmjs.com/package/uglifycss" title="UglifyCSS" target="_blank">UglifyCSS</a>,
and it seems to do what it's supposed to do. The last publication date for this package is about
5 ( five ) years ago. Its weekly download is around 40,000+ ( fourty thousands plus )
times.

Both of these require 
<a href="https://nodejs.org/en/" title="NodeJS" target="_blank">NodeJS</a> 
-- the version I have installed is 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
v18.12.0</span>. Follow the instructions, I've chosen to install them 
globally on my 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
Windows 10 Pro version 10.0.19044 Build 19044</span>:

<strong>Installing UglifyJS 3 globally:</strong>

```
npm install uglify-js -g
```

<strong>Installing UglifyCSS globally:</strong>

```
npm install uglifycss -g
```

Their executable scripts are:

```
C:\Users\behai\AppData\Roaming\npm\uglifyjs
C:\Users\behai\AppData\Roaming\npm\uglifycss
```

Where 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
behai</span> is the Windows user I've logged in with, and installed the two packages.

Following are two Windows batch files I've written for my project:

<strong>Content of F:\my_project\minify\js-minify.bat</strong>

```
@echo off

echo Final output file is my_project.min.js when finished.

C:\Users\behai\AppData\Roaming\npm\uglifyjs ^
    D:\Codes\WebWork\jquery\js\jquery-3.6.0.js ^
    D:\Codes\WebWork\bootstrap\dist\js\bootstrap.bundle.js ^
    D:\Codes\WebWork\parsley\dist\parsley.js ^
    D:\Codes\WebWork\js\date_funcs.js ^
    D:\Codes\WebWork\js\mime_types.js ^
    D:\Codes\WebWork\js\http_status.js ^
    D:\Codes\WebWork\js\drags.js ^
    D:\Codes\WebWork\js\bootstrap_funcs.js ^
    D:\Codes\WebWork\js\bootstrap_dialogs.js ^
    D:\Codes\WebWork\js\client_dialogs.js ^
    D:\Codes\WebWork\js\ajax_dialog.js ^
    D:\Codes\WebWork\js\elem_height_funcs.js ^
    F:\my_project\src\my_project\static\js\my_project.js ^
    --compress --mangle -o F:\my_project\src\my_project\static\js\my_project.min.js
```

<strong>Content of F:\my_project\minify\css-minify.bat</strong>

```
@echo off

echo Final output file is my_project.min.css when finished.

C:\Users\behai\AppData\Roaming\npm\uglifycss ^
    D:\Codes\WebWork\bootstrap\dist\css\bootstrap.css ^
    D:\Codes\WebWork\bootstrap\icons-1.9.1\font\bootstrap-icons.css ^
    D:\Codes\WebWork\parsley\src\parsley.css ^
    D:\Codes\WebWork\css\bootstrap-common.css ^
    F:\my_project\src\my_project\static\css\my_project.css ^
    --output F:\my_project\src\my_project\static\css\my_project.min.css
```

<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
my_project.min.js</span> is around 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
227 KB</span> ( two hundreds and twenty seven kilobytes ); and 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
my_project.min.css</span> is around 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
241 KB</span> ( two hundreds and forty one kilobytes ). They're fairly sizeable 
as anticipated, and I have tested all pages, there are no errors. I am sticking to these
two packages till they become outdated and unusable.

Backtrack a few years, at work, we've used  
<a href="http://www.java2s.com/example/jar/y/yuicompressor-index.html" title="Jar y yuicompressor" target="_blank">Jar y yuicompressor</a>
<span class="keyword">
version 2.4.6</span> to do both JavaScript and CSS minifications, it does not 
handle multiple input files, my boss has written a Windows PowerShell script
to process multiple files into a single output minification file.
I have tried the latest, which is 
<span class="keyword">
version 2.4.8</span> -- and it fails on me: I'm using some ES6 features.

As demonstrated, both 
<a href="https://www.npmjs.com/package/uglify-js" title="UglifyJS 3" target="_blank">UglifyJS 3</a>
and 
<a href="https://www.npmjs.com/package/uglifycss" title="UglifyCSS" target="_blank">UglifyCSS</a>
handle multiple input files quite nicely. And 
<a href="https://www.npmjs.com/package/uglify-js" title="UglifyJS 3" target="_blank">UglifyJS 3</a>
supports ES6.

I hope you find this useful. Thank you for reading. And stay safe as always.
