---
layout: post
title: "( Python / ReportLab. ) How UTF-8 Gets Displayed by Browsers and PDF creation tools?"

---

A new question popped into my head recently, triggered by working with ReportLab. 
When we declare an HTML page as UTF-8, we can display all kinds of human languages 
using the “font-family that we specify in the CSS” ( my erroneous assumption! ). 
Whereas with PDF tools, we need to select appropriate fonts for target human 
languages that we want to display. The question, therefore, is: how do browsers 
manage that?

| ![022-feature-image.png](https://behainguyen.files.wordpress.com/2022/05/022-feature-image.png) |
|:--:|
| *How UTF-8 Gets Displayed by Browsers and PDF creation tools?* |

<h4><a id="environments">Environments</a></h4>

<ol>
<li>
<span class="keyword">
Windows 10 Pro, version 21H2, OS build 19044.1706</span>.
</li>

<li style="margin-top:10px;">
<span class="keyword">
FireFox 100.0.2 (64-bit)</span>.
</li>


<li style="margin-top:10px;">
<span class="keyword">
Python 3.10.1</span>.
</li>

<li style="margin-top:10px;">
<span class="keyword">
ReportLab 3.6.9</span>.
</li>

<li style="margin-top:10px;">
<span class="keyword">
ReportLab User Guide</span> version 
<span class="keyword">
3.5.56</span>, 
<span class="keyword">
“Document generated on 2020/12/02 11:31:59”</span>;
henceforth <span class="keyword">
“User Guide”</span>, downloadable from 
<a href="https://www.reportlab.com/docs/reportlab-userguide.pdf" 
title="ReportLab User Guide version 3.5.56, Document generated on 2020/12/02 11:31:59" 
target="_blank">https://www.reportlab.com/docs/reportlab-userguide.pdf</a>
</li>
</ol>

The following 
 <span class="keyword">
HTML</span> page illustrates 
<span class="keyword">
UTF-8</span> declaration mentioned in the introduction. I purposely 
specify only <span style="font-family:Arial;">Arial</span> font for 
the page:

{% highlight html %}
<!doctype html>
<html lang="en">
<head>
    <title>Test UTF-8</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>

	<style>
        body { font-family: Arial; }
        div { margin: 50px 0 0 50px; }
	</style>
</head>

<body>
    <div>
        <p>“Australia” in some other languages:</p>
        <p>Chinese ( Simplified ): 澳大利亚</p>
        <p>Chinese ( Traditional ): 澳大利亞</p>
        <p>Japanese: オーストラリア</p>
        <p>Khmer: អូស្ត្រាលី</p>
        <p>Korean: 호주 -- I think this is Australia continent.</p>
        <p>Russian: Австралия</p>
        <p>Vietnamese: Úc Châu -- Australia continent.</p>
        <p>Vietnamese: Úc Đại Lợi -- Long form of Australia country.</p>
    </div>
</body>

</html>
{% endhighlight %}

We understand that, within
<span class="keyword">
Windows</span>, available fonts are in the
<span class="keyword">
“Fonts”</span> folder ( directory ), directly under the 
<span class="keyword">
Windows</span> installation directory. In my case, it is:

```
C:\Windows\Fonts
```

<p style="font-style:italic;font-weight:bold;color:blue;font-family:Arial;">
-- I had always assumed that, the Arial fonts shipped with Windows are capable
of displaying all human languages available under the UTF-8 character encoding 
as defined by the Unicode Standard!
</p>

<span class="keyword">
ReportLab User Guide</span> section 
<span class="keyword">
3.6 Asian Font Support</span>, page 53, spells out clearly that 
we need to load appropriate fonts for languages that we want to 
work with. Under the above aforementioned assumption, I thought 
loading <span class="keyword">
Windows Arial</span> font would give me a 
<span class="keyword">
PDF</span> text similar to the
<span class="keyword">
HTML</span> above:

{% highlight python %}
import os

import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.colors import tan, green, yellow, red

def get_font_height( font_name, font_size ):    
    ascent, descent = pdfmetrics.getAscentDescent( font_name, font_size )
    return ( ascent - descent ) + ( ascent / 2 )

font_name = 'ArialMT'
font_file = 'arial.ttf'
font_size = 12

font_path = 'C:\\Windows\\Fonts\\' # os.path.join( os.path.dirname(__file__), 'fonts\\' )
pdfmetrics.registerFont( TTFont(font_name, font_path + font_file) )

font_height = get_font_height( font_name, font_size )

canvas = canvas.Canvas( '022-reportlab-utf8-a.pdf' )

canvas.setFont( font_name, font_size )

y = 800
canvas.drawString( 100, y, '“Australia” in some other languages:' )

y -= ( font_height * 2 )
canvas.drawString( 100, y, 'Chinese ( Simplified ): 澳大利亚' )

y -= font_height
canvas.drawString( 100, y, 'Chinese ( Traditional ): 澳大利亞' )

y -= font_height
canvas.drawString( 100, y, 'Japanese: オーストラリア' )

y -= font_height
canvas.drawString( 100, y, 'Khmer: អូស្ត្រាលី' )

y -= font_height
canvas.drawString( 100, y, 'Korean: 호주 -- I think this is Australia continent.' )

y -= font_height
canvas.drawString( 100, y, 'Russian: Австралия' )

# Vietnamese -- Australia continent
y -= font_height
canvas.drawString( 100, y, 'Vietnamese: Úc Châu -- Australia continent.' )

y -= font_height
canvas.drawString( 100, y, 'Vietnamese: Úc Đại Lợi -- Long form of Australia country.' )

canvas.save()
{% endhighlight %}

<p style="color:blue;">
-- Note: to work out the file name: 
<span class="keyword">
arial.ttf</span> -- I just copy the
<span class="keyword">
“Arial icon”</span> in my 
<span class="keyword">
C:\Windows\Fonts</span> folder to the
<span class="keyword">
Python script</span>'s 
<span class="keyword">
“fonts”</span> sub-directory. It will then list several
<span class="keyword">
tff files</span>. Double click on any one of them, 
<span class="keyword">
Windows</span> will bring up the font sample dialog, the name of the font 
is listed in this dialog. I repeat this process for other fonts.
</p>

The result was not what I assumed:

![022-01.png](https://behainguyen.files.wordpress.com/2022/05/022-01.png)

In <span class="keyword">
Acrobat-Reader</span>, under 
<span class="keyword">
File | Properties... | Font tab</span> shows all embedded fonts in the
document: <span class="keyword">
ArialMT</span> is used in the document. 
<span class="keyword">
ArialMT</span> is loaded and used.

<span style="color:blue;">Why FireFox is able to display all these languages correctly?</span>
After some searching, I came across this post 
<a href="https://stackoverflow.com/questions/884177/how-can-i-determine-what-font-a-browser-is-actually-using-to-render-some-text" 
title="How can I determine what font a browser is actually using to render some text?" 
target="_blank">https://stackoverflow.com/questions/884177/how-can-i-determine-what-font-a-browser-is-actually-using-to-render-some-text</a>,
the answer provided by user 
<a href="https://stackoverflow.com/users/84237/arjan" 
title="Arjan" 
target="_blank">Arjan</a> led me to inspect my page:

![022-02.png](https://behainguyen.files.wordpress.com/2022/05/022-02.png)

<span style="font-style:italic;font-weight:bold;">
-- FireFox loads other fonts on its own accord as necessary to display the content correctly.
</span>I do the same:

{% highlight python %}
import os

import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.colors import tan, green, yellow, red

def get_font_height( font_name, font_size ):    
    ascent, descent = pdfmetrics.getAscentDescent( font_name, font_size )
    return ( ascent - descent ) + ( ascent / 2 )

arial_font_name = 'ArialMT'
arial_font_file = 'arial.ttf'
leelawadee_ui_font_name = 'Leelawadee UI'
leelawadee_ui_font_file = 'LeelawUI.ttf'
malgun_gothic_font_name = 'Malgun Gothic'
malgun_gothic_font_file = 'malgun.ttf'
microsoft_yahei_font_name = 'Microsoft YaHei'
microsoft_yahei_font_file = 'MicrosoftYaHei-01.ttf'

font_size = 12

font_path = 'C:\\Windows\\Fonts\\' # os.path.join( os.path.dirname(__file__), 'fonts\\' )
pdfmetrics.registerFont( TTFont(arial_font_name, font_path + arial_font_file) )
pdfmetrics.registerFont( TTFont(leelawadee_ui_font_name, font_path + leelawadee_ui_font_file) )
pdfmetrics.registerFont( TTFont(malgun_gothic_font_name, font_path + malgun_gothic_font_file) )

font_path = os.path.join( os.path.dirname(__file__), 'fonts\\' )
pdfmetrics.registerFont( TTFont(microsoft_yahei_font_name, font_path + microsoft_yahei_font_file) )

font_height = get_font_height( arial_font_name, font_size )

canvas = canvas.Canvas( '022-reportlab-utf8-b.pdf' )

canvas.setFont( arial_font_name, font_size )
canvas.setFont( leelawadee_ui_font_name, font_size )
canvas.setFont( malgun_gothic_font_name, font_size )
canvas.setFont( microsoft_yahei_font_name, font_size )

y = 800
canvas.drawString( 100, y, '“Australia” in some other languages:' )

"""
Chinese Simplified and Traditional font.
"""
canvas.setFont( microsoft_yahei_font_name, font_size )

y -= ( font_height * 2 )
canvas.drawString( 100, y, 'Chinese ( Simplified ): 澳大利亚' )

y -= font_height
canvas.drawString( 100, y, 'Chinese ( Traditional ): 澳大利亞' )

"""
Japanese font.
"""
canvas.setFont( malgun_gothic_font_name, font_size )
y -= font_height
canvas.drawString( 100, y, 'Japanese: オーストラリア' )

"""
Khmer font.
"""
canvas.setFont( leelawadee_ui_font_name, font_size )
y -= font_height
canvas.drawString( 100, y, 'Khmer: អូស្ត្រាលី' )

"""
Korean font.
"""
canvas.setFont( malgun_gothic_font_name, font_size )
y -= font_height
canvas.drawString( 100, y, 'Korean: 호주 -- I think this is Australia continent.' )

"""
Russian and Vietnamese font.
"""
canvas.setFont( arial_font_name, font_size )

y -= font_height
canvas.drawString( 100, y, 'Russian: Австралия' )

y -= font_height
canvas.drawString( 100, y, 'Vietnamese: Úc Châu -- Australia continent.' )

y -= font_height
canvas.drawString( 100, y, 'Vietnamese: Úc Đại Lợi -- Long form of Australia country.' )

canvas.save()
{% endhighlight %}

<span class="keyword">
Microsoft YaHei</span> font files have 
<span class="keyword">
ttc</span> extension. I use
<a href="https://transfonter.org/" title="Transfonter" target="_blank">https://transfonter.org/</a>
to convert 
<span class="keyword">
msyhl.ttc</span> to 
<span class="keyword">
ttf</span>, and store the result files in the
<span class="keyword">
Python script</span>'s 
<span class="keyword">
“fonts”</span> sub-directory. This time, the result is what I have
anticipated:

![022-03.png](https://behainguyen.files.wordpress.com/2022/05/022-03.png)

On font, I found this article 
<a href="https://css-tricks.com/understanding-web-fonts-getting/" 
title="Understanding Web Fonts and Getting the Most Out of Them" 
target="_blank">https://css-tricks.com/understanding-web-fonts-getting/</a>
very informative.

Font is a very large subject. I was just trying to answer my own question.
I am happy with what I have found. And I hope you find this post useful, 
and thank you for visiting. 