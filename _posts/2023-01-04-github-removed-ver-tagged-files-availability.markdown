---
layout: post
title: "GitHub: are removed version-tagged files still available for downloading?"
description: A repo was tagged, then some files were removed. Are those removed files still available for cloning (downloading) at the tagged version?
tags:
- GitHub
- tag
- clone
- remove
---

*A repo was tagged, then some files were removed. Are those removed files still available for cloning (downloading) at the tagged version?*

| ![052-feature-image.png](https://behainguyen.files.wordpress.com/2023/01/052-feature-image.png) |
|:--:|
| *GitHub: are removed version-tagged files still available for downloading?* |

Let's elaborate the question a little bit more. My project is fully functional, I version-tagged its GitHub repo with <code>“v1.0.0”</code>. I continue working on this project. In the process, I have made some modules at <code>v1.0.0</code> obsolete, and I removed these. At a later date, I clone tag <code>v1.0.0</code> to my local machine; do I actually have the modules that were removed?

<div style="background-color:yellow;width:100%;height:100px;margin-bottom:10px;">
    <div style="float:left;width:100px;height:100px;
	    background-image:url('https://behainguyen.files.wordpress.com/2022/12/info-symbol.png');
		background-repeat: no-repeat;
		background-position: center center;
		background-size:100px 100px;">
    </div>

	<div style="float:right;width:550px;">
	    <p style="font-weight:bold;color:blue;padding-right:10px;">
           I take no responsibilities for any damages or losses resulting from 
		   applying the procedures outlined in this post.
	    </p>
	</div>
</div>

<strong>-- The answer is yes; the removed files associated with version-tagged <code>v1.0.0</code> is still available.</strong> My verification attempts are discussed below.

✿✿✿

❶ I created a new repo <code>https://github.com/behai-nguyen/learn-git.git</code>; my local working directory is <code>D:\learn-git</code>, there are two (2) files in this directory <code>01-mysqlconnector.py</code> and <code>02-mysqlclient.py</code>.

⓵ Initialise the repo and check the two (2) files in:

```
git init

git config user.name "behai-nguyen"
git config user.email "behai_nguyen@hotmail.com"

git add .
git commit -m "Two (2) files to be tagged v1.0.0."

git branch -M main
git remote add origin https://github.com/behai-nguyen/learn-git.git
git push -u origin main
```

⓶ Version-tag the repo with <code>v1.0.0</code>:

```
git tag -a v1.0.0 -m "First version: 01-mysqlconnector.py and 02-mysqlclient.py."
git push origin --tags
```

My local working directory <code>D:\learn-git</code> and my repo:

![052-01.png](https://behainguyen.files.wordpress.com/2023/01/052-01.png)

❷ Remove <code>01-mysqlconnector.py</code> from my local directory, and repo:

```
git rm  -f 01-mysqlconnector.py
git commit -m "Obsolete."
git branch -M main
git push -u origin main
```

Manually verify that it was removed from both local directory and repo.

❸ Now, clone version-tagged <code>v1.0.0</code> to ascertain if <code>01-mysqlconnector.py</code> is still available. My working drive is <code>E:</code>, and it <strong>should not have directory <code>learn-git</code></strong>:

```
git clone -b v1.0.0 https://github.com/behai-nguyen/learn-git.git
```

<code>01-mysqlconnector.py</code> is still available for version-tagged <code>v1.0.0</code>:

![052-02.png](https://behainguyen.files.wordpress.com/2023/01/052-02.png)

❹ Now add a new file <code>03-pymysql.py</code>, and then create a new version-tag <code>v1.0.1</code>.

⓵ Add the new file <code>03-pymysql.py</code>, the working directory is <code>D:\learn-git</code>:

```
git add 03-pymysql.py
git commit -m "Test package pymysql."
git push -u origin main
```

⓶ Create the new version-tag <code>v1.0.1</code>:

```
git tag -a v1.0.1 -m "Second version: 02-mysqlclient.py and 03-pymysql.py."
git push origin --tags
```

❺ At this point: 

⓵ With clone command for <code>v1.0.0</code>:

```
git clone -b v1.0.0 https://github.com/behai-nguyen/learn-git.git
```

We should get:

<ol>
<li style="margin-top:10px;"><code>01-mysqlconnector.py</code></li>
<li style="margin-top:10px;"><code>02-mysqlclient.py</code></li>
</ol>

⓶ While downloading <code>v1.0.1</code>:

```
git clone -b v1.0.1 https://github.com/behai-nguyen/learn-git.git
```

We should get:

<ol>
<li style="margin-top:10px;"><code>02-mysqlclient.py</code></li>
<li style="margin-top:10px;"><code>03-pymysql.py</code></li>
</ol>

![052-03.png](https://behainguyen.files.wordpress.com/2023/01/052-03.png)

I needed to know this for myself. I hope you find this useful as I do. Thank you for reading and stay safe as always.
