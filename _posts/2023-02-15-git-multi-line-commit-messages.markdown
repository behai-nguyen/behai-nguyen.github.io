---
layout: post
title: "Windows 10: multi-line Git Commit messages."
description: In Windows 10, how to do multi-line messages for a Git commit.

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list:
    - "https://behainguyen.files.wordpress.com/2023/02/059-01.png"
    - "https://behainguyen.files.wordpress.com/2023/02/059-02.png"
    - "https://behainguyen.files.wordpress.com/2023/02/059-03.png"
    - "https://behainguyen.files.wordpress.com/2023/02/059-04.png"
    - "https://behainguyen.files.wordpress.com/2023/02/059-05.png"

tags:
- Windows
- multi-line
- git
- commit
- messages
---

*In Windows 10, how to do multi-line messages for a Git commit.*

| ![059-feature-image.png](https://behainguyen.files.wordpress.com/2023/02/059-feature-image.png) |
|:--:|
| *Windows 10: multi-line Git Commit messages.* |

On Windows 10, my <code>git CLI</code> version is <code>2.37.3.windows.1</code>.
I am describing how do multi-line messages for a Git commit.

A <code>git commit</code> command, can take one (1) or two (2) 
text parameters, like so:

```
git commit -m "First message."
```

```
git commit -m "First message." -m "Detail description."
```

We can make <em>"Detail description."</em> a multi-line description as in the 
following example: we check in <code>D:\learn-git>some_js_funcs.js</code>, we
have to issue 3 (three) commands:

⓵ First command, add the file to be checked in (i.e. committed):

```
D:\learn-git>git add some_js_funcs.js
```

⓶ Second command, commit with a multi-line description:

```
D:\learn-git>git commit -m "Major refactoring." -m "Added:"^

"function runAjax( method, ..., errorCallback )."^

"const onAjaxErrorUseDialog = ( xhr, error, errorThrown ) => displayError( xhr, error, errorThrown );"^

"const onAjaxErrorUseForm = ( xhr, error, errorThrown ) => setFormErrorText( errorThrown );"^

""^

"Removed:"^

"function retrieveData( method, endPoint, csrfToken, data, successCallback )"^

"function saveData( endPoint, csrfToken, data, successCallback )"^

""^

"function jsonViewerDialog( jsonData, params ) moved to fullscreen_dialogs.js."^

""^

"Bug fixed:"^

"function clearFormInfoText() -- set '#firstMsg' to '&nbsp;' instead of blank."
```

It should be apparent that we prepare this command in a text editor, and just
copy and paste this command to the command line console. Note that:

<ul>
<li style="margin-top:10px;">Each message is enclosed within a pair of 
double quotes, i.e. <code>"function runAjax( method, ..., errorCallback )."^</code>.
</li>

<li style="margin-top:10px;">There is a caret <code>^</code> character 
at the end of each line, <strong>except the last line</strong>.
</li>

<li style="margin-top:10px;"><strong>THERE MUST BE NOTHING ELSE AFTER THE caret 
<code>^</code> character.</strong> A single space did cause a problem for me.
</li>

<li style="margin-top:10px;">
<code>""^</code> inserts a blank line into the Git commit description.
</li>

<li style="margin-top:10px;">
There is a blank line follows each text line, again <strong>except the last line</strong>.
</li>
</ul>

⓷ Third and last command, push to the remote repo:

```
D:\learn-git>git push -u origin main
```

The second command will pause twice for our input. The first phase, we
just click on the <code>Paste anyway</code> button, the second phase, we
just hit the <code>Enter key</code> -- please see illustrations:

{% include image-gallery.html list=page.gallery-image-list %}

<!--
https://behainguyen.files.wordpress.com/2023/02/059-01.png
https://behainguyen.files.wordpress.com/2023/02/059-02.png
https://behainguyen.files.wordpress.com/2023/02/059-03.png
https://behainguyen.files.wordpress.com/2023/02/059-04.png
https://behainguyen.files.wordpress.com/2023/02/059-05.png
-->

The multi-line description as seen in the repo UI:

![059-06.png](https://behainguyen.files.wordpress.com/2023/02/059-06.png)

I took me a few tries to get this working on Windows 10: I document
so if I forget, I can look it up later... This would not work on a 
Linux environment, or at least I have not tested yet. Thank you for
reading, I hope you find this useful. Stay safe as always.
