---
layout: post
title: "Python FastAPI: Some Further Studies on OAuth2 Security"

description: FastAPI provides excellent tutorials that thoroughly introduce the framework. Two sections on security, namely Tutorial - User Guide Security and Advanced User Guide Security , have sparked further questions, which we are discussing in this post. Hopefully, this discussion will lead to a better understanding of how FastAPI security works.

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list:
    - "https://behainguyen.files.wordpress.com/2024/05/105-07a.png"
    - "https://behainguyen.files.wordpress.com/2024/05/105-07b.png"
    - "https://behainguyen.files.wordpress.com/2024/05/105-07c.png"

tags:
- Python 
- FastAPI
- OAuth2
- Security
---

<em><code>FastAPI</code> provides <a href="https://fastapi.tiangolo.com/learn/" title="FastAPI tutorials" target="_blank">excellent tutorials</a> that thoroughly introduce the framework. Two sections on security, namely <a href="https://fastapi.tiangolo.com/tutorial/security/" title="Tutorial - User Guide Security" target="_blank">Tutorial - User Guide Security</a> and <a href="https://fastapi.tiangolo.com/advanced/security/" title="Advanced User Guide Security" target="_blank">Advanced User Guide Security</a>, have sparked further questions, which we are discussing in this post. Hopefully, this discussion will lead to a better understanding of how <code>FastAPI</code> security works.</em>

<h3>
🐍 <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![105-feature-image.png](https://behainguyen.files.wordpress.com/2024/05/105-feature-image.png) |
|:--:|
| *Python FastAPI: Some Further Studies on OAuth2 Security* |

I intend to conduct further studies on the <a href="https://fastapi.tiangolo.com/learn/" 
title="FastAPI" target="_blank">FastAPI</a> framework and document any necessary 
issues I encounter.

This post begins with an example from the 
<a href="https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/" 
title="Simple OAuth2 with Password and Bearer" 
target="_blank">Simple OAuth2 with Password and Bearer</a> section of the 
<a href="https://fastapi.tiangolo.com/tutorial/security/" 
title="Tutorial - User Guide Security" target="_blank">Tutorial - User Guide Security</a>. 
The discussions in this post will also be applicable to later 
<code>OAuth2</code> examples in the official tutorial, which include 
<code>JSON Web Token</code> and <code>scopes</code>.

❶ My first question concerns <strong><code>OAuth2PasswordBearer</code>: 
how does Swagger UI remember the access_token?</strong>

When running this example and accessing Swagger UI, we encounter a page like the one shown in the screenshot below:

![105-01.png](https://behainguyen.files.wordpress.com/2024/05/105-01.png)

Following the tutorial, logging in via the <code>Authorize</code> button with 
the credentials <code>johndoe</code> and <code>secret</code>, and accessing the 
<code>/users/me</code> path, we receive a successful response, as shown in the 
screenshot below:

![105-02.png](https://behainguyen.files.wordpress.com/2024/05/105-02.png)

We can observe that the token <code>johndoe</code> was sent via the 
<code>Authorization</code> header, as indicated in the tutorial. We 
understand that it is the client's responsibility to remember the 
<code>access_token</code>. Initially, I assumed that Swagger UI might store it as a cookie. However, as seen in the screenshot below, this was not the case:

![105-03.png](https://behainguyen.files.wordpress.com/2024/05/105-03.png)

<em>If we refresh the Swagger UI page now and access the <code>/users/me</code> 
path again, we find ourselves no longer authenticated. This can be verified by 
attempting to <code>Authorize</code> again, then refreshing the browser; 
accessing <code>/users/me</code> would return as <code>not authenticated</code>.</em>

<strong>🚀 It appears that the Swagger UI client merely remembers the 
<code>access_token</code> in memory.</strong> While this point may not be 
significantly important, I would still like to understand it.

❷ The second question is <strong>whether the <code>/token</code> path within 
the Swagger UI functions equivalently to the <code>Authorize</code> button.</strong>

This question arises logically because the <code>/token</code> path displays 
the same login screen as the <code>Authorize</code> button, as depicted in 
the screenshot below:

![105-04.png](https://behainguyen.files.wordpress.com/2024/05/105-04.png)

Additionally, the response from the <code>/token</code> path is identical 
to that of the <code>Authorize</code> button, as shown in the screenshot below:

![105-05.png](https://behainguyen.files.wordpress.com/2024/05/105-05.png)

However, despite this similarity, accessing <code>/users/me</code> returns 
as <code>not authenticated</code>, as seen below:

![105-06.png](https://behainguyen.files.wordpress.com/2024/05/105-06.png)

<strong>🚀 It seems that within the Swagger UI, the <code>/token</code> path does NOT 
work the same as the <code>Authorize</code> button.</strong> 

I feel the need to emphasize this point because I experienced confusion when 
I based my code on this example. Absent-mindedly, I clicked on the <code>/token</code> 
path, and while the login was successful, the protected paths “suddenly failed” within 
Swagger UI! This left me confused for a little while until I realised what I had done.

❸ Building upon the two previous questions, <strong>the final question is: if I use 
Postman to access the path <code>/users/me</code> with the header <code>Authorization</code> 
set to <code>Bearer johndoe</code> and <code>Bearer alice</code>, would I receive 
successful responses?</strong> My anticipation was that I would, and indeed, that was 
the case, as shown in the screenshots below:

{% include image-gallery.html list=page.gallery-image-list %}
<br/>

<strong>🚀 It's quite logical. Everything would fall apart if this didn't work 😂</strong>

We conclude this post here. While it may not cover anything significant, these 
are the questions that enable me to understand <code>FastAPI</code> better. 
In a future post, we'll delve into building our own login UI and how the 
<code>/token</code> path, <code>OAuth2PasswordBearer</code>, and 
<code>OAuth2PasswordRequestForm</code> come together in our custom login process.

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
<a href="https://fastapi.tiangolo.com/" target="_blank">https://fastapi.tiangolo.com/</a>
</li>
</ul>

<h3>
🐍 <a href="https://github.com/behai-nguyen/fastapi_learning" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>
