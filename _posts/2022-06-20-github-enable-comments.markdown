---
layout: post
title: "GitHub: enable comments using Utterances comment widget."

---

I've been blogging with GitHub for a bit, please see 
https://behai-nguyen.github.io/. In this post, we discuss how 
to enable comments for GitHub repositories using https://utteranc.es/ 
comment widget.

| ![024-feature-image.png](https://behainguyen.files.wordpress.com/2022/06/024-feature-image.png) |
|:--:|
| *GitHub: Enable Comments Using https://utteranc.es/ Comment Widget.* |

This is how I did it:

<span class="medium-font-size">1.</span> Install 
<span class="keyword">
utterances</span> app for the target 
<span class="keyword">
GitHub repo</span> via the following link 
<a href="https://github.com/apps/utterances/installations/new" 
title="Setuptools Keywords" 
target="_blank">https://github.com/apps/utterances/installations/new</a> 
-- the instructions should be self-explanatory. After each step, 
please read the on screen instructions carefully.

<span class="medium-font-size">2.</span> I'd like to enable comments for my 
<span class="keyword">
GitHub Pages</span>, so the repo I selected is 
<span class="keyword">
https://github.com/behai-nguyen/behai-nguyen.github.io</span>. 
The plugin snippet is customised like below:

{% highlight python %}
<script src="https://utteranc.es/client.js"
    repo="behai-nguyen/behai-nguyen.github.io "
    issue-term="pathname"
    label="Comment"
    theme="github-light"
    crossorigin="anonymous"
    async>
</script>
{% endhighlight %}

<span class="medium-font-size">3.</span> The 
<a href="https://jekyllrb.com/" 
title="Jekyll" target="_blank">Jekyll -- https://jekyllrb.com/</a> theme
I'm using is 
<a href="https://rubygems.org/gems/minima/versions/2.5.1" 
title="minima 2.5.1" 
target="_blank">minima 2.5.1 -- https://rubygems.org/gems/minima/versions/2.5.1
</a>, I modified the 
<span class="keyword">
footer.html</span> file to include the plugin snippet as shown:

```
File: \_includes\footer.html
```

{% highlight html %}
<footer class="site-footer h-card">
  <data class="u-url" href="{{ "/" | relative_url }}"></data>

  <div class="wrapper">
  
    <div class="utterances">
		<script src="https://utteranc.es/client.js"
			repo="behai-nguyen/behai-nguyen.github.io"
			issue-term="pathname"
			label="Comment"
			theme="github-light"
			crossorigin="anonymous"
			async>
		</script>	  
    </div>

    <h2 class="footer-heading">{{ site.title | escape }}</h2>

    <div class="footer-col-wrapper">
      <div class="footer-col footer-col-1">
        <ul class="contact-list">
          <li class="p-name">
            {%- if site.author -%}
              {{ site.author | escape }}
            {%- else -%}
              {{ site.title | escape }}
            {%- endif -%}
            </li>
            {%- if site.email -%}
            <li><a class="u-email" href="mailto:{{ site.email }}">{{ site.email }}</a></li>
            {%- endif -%}
        </ul>
      </div>
	  
      <div class="footer-col footer-col-2">
        {%- include social.html -%}
      </div>

      <div class="footer-col footer-col-3">
        <p>{{- site.description | escape -}}</p>
      </div>
    </div>

  </div>

</footer>
{% endhighlight %}

Of course, you can place it anywhere you like.

<span class="medium-font-size">4.</span> After update <span class="keyword">
GitHub repo</span> with the change, we might need to issue the followings to 
get it to rebuild:

```
git commit --allow-empty -m "Trigger rebuild"
git push
```

Please note the followings:

<ul>
<li style="margin-top:5px;">
The 
<a href="https://utteranc.es/" 
title="Utterances Widget" target="_blank">Utterances Widget -- https://utteranc.es/</a>
supports 
<span class="keyword">
Markdown Styling</span> -- see 
<a href="https://github.com/adam-p/markdown-here/wiki/Markdown-Here-Cheatsheet#code" 
title="Markdown Here Cheatsheet" target="_blank">Markdown Here Cheatsheet</a>.
</li>

<li style="margin-top:10px;">
To comment, users must sign into their 
<span class="keyword">
GitHub</span> account. Anonymous users are not supported.
</li>

<li style="margin-top:10px;">
It seems that after submitting comments, users can't edit them. 
Only the 
<span class="keyword">
GitHub repo</span> owners can edit comments ( or issues ).
</li>

<li style="margin-top:10px;">
Comments are stored as issues inside the target
<span class="keyword">
GitHub repo</span> -- we, as target repo owner, can manage these issues.
</li>
</ul>

I hope you get something out of this post... If you happen to read it on 
<span class="keyword">
GitHub</span> and found it useful, please give me a comment 😆...
and thank you for reading.
