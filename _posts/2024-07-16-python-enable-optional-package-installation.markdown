---
layout: post
title: "How to Enable the Installation of Optional Packages"
description: My database wrapper package (bh-database) requires either the mysql-connector-python package or the psycopg2-binary package to function. Previously, it would install both packages regardless of which database the application was using. However, I recently learned how to make the installation of the required package optional. In this post, we will explore how to achieve this. 

tags:
- Python
- Installation
- Optional
- Package
---

<em>
My <a href="https://pypi.org/project/bh-database/" title="bh-database" target="_blank">database wrapper package (bh-database)</a> requires either the <a href="https://pypi.org/project/mysql-connector-python" title="mysql-connector-python" target="_blank">mysql-connector-python</a> package or the <a href="https://pypi.org/project/psycopg2" title="psycopg2-binary" target="_blank">psycopg2-binary</a> package to function. Previously, it would install both packages regardless of which database the application was using. However, I recently learned how to make the installation of the required package optional. In this post, we will explore how to achieve this.
</em>

| ![115-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/07/115-feature-image.png) |
|:--:|
| *Python: How to Enable the Installation of Optional Packages* |

Let’s take a look at the commands that enable <strong><em>the installation of optional packages</em></strong> <a href="https://pypi.org/project/mysql-connector-python" title="mysql-connector-python" target="_blank">mysql-connector-python</a> or <a href="https://pypi.org/project/psycopg2" title="psycopg2-binary" target="_blank">psycopg2-binary</a> for the <a href="https://pypi.org/project/bh-database/" title="bh-database" target="_blank">bh-database</a> package: 

```
pip install bh-database[mysql-connector-python]
pip install bh-database[psycopg2-binary]
```

<ol>
<li style="margin-top:10px;">The first command installs the <code>bh-database</code> and the required <code>mysql-connector-python</code> packages.</li>
<li style="margin-top:10px;">The second command installs the <code>bh-database</code> and the required <code>psycopg2-binary</code> packages.</li>
</ol>

👉 If the application works with both MySQL and PostgreSQL, then run both commands to install the two required packages.

To achieve this, we need to configure the <a href="https://github.com/behai-nguyen/bh_database/blob/707ff1683afa95803ecf0b523a456db36136f3c2/pyproject.toml#L34-L40" title="pyproject.toml file" target="_blank"><code>pyproject.toml</code> file</a> as follows: 

<figure class="highlight"><pre><code class="language-toml" data-lang="toml"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">34
35
36
37
38
39
40
</pre></td><td class="code"><pre><span class="nn">[project.optional-dependencies]</span>
<span class="py">mysql-connector-python</span> <span class="p">=</span> <span class="p">[</span>
    <span class="s">"mysql-connector-python"</span>
<span class="p">]</span>
<span class="err">psycopg</span><span class="mi">2</span><span class="err">-binary</span> <span class="err">=</span> <span class="p">[</span>
    <span class="s">"psycopg2-binary"</span>
<span class="p">]</span>
</pre></td></tr></tbody></table></code></pre></figure>

This is documented in the section titled <a href="https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#dependencies-and-requirements" title="Dependencies and requirements" target="_blank">Dependencies and requirements</a> of the official Python documentation page <a href="https://packaging.python.org/en/latest/guides/writing-pyproject-toml/" title="Writing your pyproject.toml" target="_blank">Writing your <code>pyproject.toml</code></a>.

The tokens to the right of the equal sign <code>equal sign (‘=’)</code> are <code>keys</code>. In this case, they are <code>mysql-connector-python</code> and <code>psycopg2-binary</code>. We could name them whatever seems appropriate, for example, <code>mysql</code> and <code>postgresql</code> respectively.

Basically, under the <code>project.optional-dependencies</code> table, we define our optional entries. Please note that each entry <code>key</code> can have more than one package listed as per the official documentation.

The current version of <code>bh-database</code> is <code>0.0.6</code>. The build command produces the following two files: <code>bh_database-0.0.6-py3-none-any.whl</code> and <code>bh_database-0.0.6.tar.gz</code>. We can also install <code>bh_database-0.0.6-py3-none-any.whl</code> into an active virtual environment using the below commands, given that <code>bh_database-0.0.6-py3-none-any.whl</code> resides at the same level as the active virtual environment’s directory: 

```
pip install bh_database-0.0.6-py3-none-any.whl[mysql-connector-python]
pip install bh_database-0.0.6-py3-none-any.whl[psycopg2-binary]
```

👎 However, configuring <code>bh_database-0.0.6-py3-none-any.whl</code> in <code>pyproject.toml</code> such as:

```
[project]
...
dependencies = [
    'tomli; python_version >= "3.12"',
    'fastapi',
    ...
    'bh_database-0.0.6-py3-none-any.whl[mysql-connector-python]',
    'bh_database-0.0.6-py3-none-any.whl[psycopg2-binary]',
    ...,
]
```

💥 will not work.

The above observations are based on my attempts at trying out <code>bh_database-0.0.6-py3-none-any.whl</code>. I have not come across any such discussions or official documentation. Please do not quote me, I am not taking responsibility for anything. Please try it out for yourselves and decide based on your own observations.

I have not come across any tutorials or sites which mentioned optional package installation in Python. I just assumed that this feature is not available. My <code>pyproject.toml</code> files just work, so I did not bother to look into the official documentation on <code>pyproject.toml</code> file. Only when I started learning <a href="https://fastapi.tiangolo.com/" title="FastAPI" target="_blank">FastAPI</a> did I see the optional package installation feature. It seems to be not a very actively discussed Python topic. Hence, I would just like to share my learning experience.

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
