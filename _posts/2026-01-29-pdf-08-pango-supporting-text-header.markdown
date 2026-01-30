---
layout: post
title: "Rust: PDFs — Pango and Cairo Layout — Supporting Headers"

description: Headers are text rendered in larger font sizes, optionally in bold, italic, or bold italic. Following Markdown, we support six heading levels&#58; #..######. This article continues and extends the work from the sixth article. The final PDF produced here renders all natural headers using distinct, externally configured font settings. 

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2026/01/158-04.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2026/01/158-05.png"

tags:
- Rust
- FFI
- HarfBuzz
- hb-shape
- hb-subset
- Unicode
- font subset
- PDF
- multilingual
- line breaking
- text rotation
- rotate
- Pango
- Cairo
- heading
- header
---

<strong>Headers</strong> are text rendered in larger font sizes, optionally in <strong>bold</strong>, <em>italic</em>, or <strong><em>bold italic</em></strong>. Following <code>Markdown</code>, we support  <a href="https://www.markdownguide.org/basic-syntax/#headings" title="Markdown Guide" target="_blank">six heading levels</a>: <code>#</code>..<code>######</code>. This article continues and extends the work from the <a href="https://behainguyen.wordpress.com/2025/12/27/rust-pdfs-exploring-layout-with-pango-and-cairo/" title="Rust: PDFs — Exploring Layout with Pango and Cairo" target="_blank">sixth article</a>. The final PDF produced here renders all natural headers using distinct, externally configured font settings.

<h3>
🦀 <a href="https://github.com/behai-nguyen/polyglot_pdf" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![158-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/01/158-feature-image.png) |
|:--:|
| *Rust: PDFs — Pango and Cairo Layout — Supporting Headers* |

<a id="repository-cloning"></a>
🚀 The code for this post is in the following GitHub repository: 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header" 
title="Rust multilingual PDFs" target="_blank">pdf_05_header</a>.

💡 Please note that <code>Pango</code> also supports HTML markup. I am not taking 
that route because I prefer to retain as much control as possible over how the 
input text is processed.

<a id="repository-layout"></a>
❶ <strong>Repository Layout</strong>

💡 Please note: on both Windows and Ubuntu, I’m running Rust version 
<code>rustc 1.90.0 (1159e78c4 2025-09-14)</code>.

This is once again a one‑off project—I don’t plan to update it in future development. 
I want to keep a log of progress exactly as it occurred. Future code may copy this and 
make changes to it. I’ve placed the project under the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header" 
title="Rust multilingual PDFs" target="_blank">pdf_05_header</a> directory. 
The structure is:

```
.
├── Cargo.toml
├── set_env.bat
├── config
│   ├── config-linux.toml
│   └── config-windows.toml
├── src
│   ├── config.rs
│   ├── document.rs
│   ├── main.rs
│   └── page_geometry.rs
└── text
    └── essay.txt
```

<a id="repository-layout-desc"></a>
The <code>config.rs</code>, <code>document.rs</code>, and <code>main.rs</code> 
modules under <code>src/</code> are new code, which we will discuss in a later 
<a href="#the-main-code">section</a>.

<a id="page-geometry-mod"></a>
⓵ The <code>src/page_geometry.rs</code> module is copied unchanged from the 
<a href="https://behainguyen.wordpress.com/2026/01/16/rust-pdfs-text-rotation-with-cairo-and-pango/" 
title="Rust: PDFs — Text Rotation with Cairo and Pango" 
target="_blank">last article</a>.  
👉 Changing any margin value in the <code>A4_DEFAULT_MARGINS</code> constant will 
change the layout of the text in the PDF.

<a id="path-env-var"></a>
⓶ 💡 The code requires the <code>Pango</code>, <code>HarfBuzz</code>, <code>Cairo</code>, 
etc. libraries. 🐧 On Ubuntu, all required libraries are globally recognised. 🪟 On Windows, 
I haven’t added the paths for the libraries’ DLLs to the <code>PATH</code> environment 
variable. In each new Windows terminal session, I run the following once:

```
set PATH=C:\PF\harfbuzz\dist\bin\;%PATH%
set PATH=C:\PF\vcpkg\installed\x64-windows\bin\;%PATH%
set PATH=C:\PF\pango\dist\bin;C:\PF\cairo-1.18.4\dist\bin;C:\PF\fribidi\dist\bin;%PATH%
```

Alternatively, you can simply run 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header/set_env.bat" 
title="pdf_05_header/set_env.bat file" target="_blank"><code>set_env.bat</code></a>.  
After that, <code>cargo run</code> works as expected.

<a id="text-essay-file"></a>
⓷ The <code>text/essay.txt</code> file — this is the same text file used in the 
<a href="https://behainguyen.wordpress.com/2025/12/07/rust-pdfs-basic-text-layout/" 
title="Rust: PDFs — Basic Text Layout" target="_blank">fourth article</a> and 
<a href="https://behainguyen.wordpress.com/2025/12/27/rust-pdfs-exploring-layout-with-pango-and-cairo/" 
title="Rust: PDFs — Exploring Layout with Pango and Cairo" target="_blank">sixth article</a>. 
However, the actual intended content is only about one‑fifth of the versions used in those 
two articles. I have just realised that both contained a lot of duplicated text—some 
paragraphs appeared several times. This was purely a copy‑and‑paste mistake.

Also, all Unicode characters <code>“═”</code> <code>(U+2550)</code> have been replaced 
with the <code>=</code> (equal sign) character. 🙏 We discuss these updates further in a 
<a href="#the-updated-input-text-file">later section</a>.

<a id="no-build-mod"></a>
⓸ 💥 The <code>build.rs</code> module is not required—the code for the 
<a href="https://behainguyen.wordpress.com/2026/01/16/rust-pdfs-text-rotation-with-cairo-and-pango/" 
title="Rust: PDFs — Text Rotation with Cairo and Pango" target="_blank">last article</a> 
does not include a <code>build.rs</code> module. I did not notice this until finishing 
that article. It appears that this module is no longer necessary, even though 
<code>Pango</code> still uses the 
<a href="https://en.wikipedia.org/wiki/HarfBuzz" title="HarfBuzz" 
target="_blank">HarfBuzz</a> library underneath.

<a id="install-be-vietnam-pro"></a>
❷ <strong>Download and Install the 
<a href="https://fonts.google.com/specimen/Be+Vietnam+Pro" title="Be Vietnam Pro" 
target="_blank"><code>Be Vietnam Pro</code></a> Font Program</strong>

As mentioned at the outset, for heading text we support <strong>bold</strong>, 
<em>italic</em>, and <strong><em>bold italic</em></strong>. The font program 
used must include faces for <strong>bold</strong>, <em>italic</em>, and 
<strong><em>bold italic</em></strong>; otherwise, <code>Pango</code> will simply 
fall back to the default face. The <code>Arial Unicode MS</code> font program 
has only a single face, so it cannot be used to demonstrate the features we are 
going to implement.

The <a href="https://fonts.google.com/specimen/Be+Vietnam+Pro" title="Be Vietnam Pro" 
target="_blank"><code>Be Vietnam Pro</code></a> font program includes all the 
required faces and is well suited for our needs. Regarding copyright, we are not 
using it for commercial purposes, so I hope that is okay 😂

⓵ <strong>Download the Font Program</strong>

Download <code>Be_Vietnam_Pro.zip</code> from  
<a href="https://fonts.google.com/specimen/Be+Vietnam+Pro" 
title="Google font Be Vietnam Pro" target="_blank">https://fonts.google.com/specimen/Be+Vietnam+Pro</a>.

⓶ <strong>Install On 🪟 Windows</strong>

Unpack all individual <code>ttf</code> files from <code>Be_Vietnam_Pro.zip</code>.  
Right‑click each <code>ttf</code> file and select <strong>Install</strong> from the 
pop‑up menu.

You can verify the installation using Windows <strong>Font settings</strong>, as 
illustrated in the screenshot below:

![158-01.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/01/158-01.png)

⓷ <strong>Install On 🐧 Ubuntu</strong>

Unpack all <code>ttf</code> files from <code>Be_Vietnam_Pro.zip</code> into 
<code>/home/behai/Public/</code>, then copy them to 
<code>/usr/local/share/fonts/</code> using:

```
$ sudo mv /home/behai/Public/*.* /usr/local/share/fonts/.
```

We can verify they are present using <code>sudo ls -l /usr/local/share/fonts</code>.  
The result is shown in the screenshot below:

![158-02.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/01/158-02.png)

Next, update the system font cache using:

```
$ sudo fc-cache -f -v
```

This command produces a long output. To confirm that the new font program 
<code>Be Vietnam Pro</code> has been installed, run:

```
$ fc-list | grep "Be Vietnam Pro"
```

It appears that <code>Be Vietnam Pro</code> has indeed been installed, as shown 
in the screenshot below:

![158-03.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/01/158-03.png)

<a id="the-main-code"></a>
❸ <strong>The Main Code</strong>

I did struggle a bit while developing the code. It took several iterations to arrive at 
the final version presented in this article. The final code feels straightforward enough 
that I decided not to include any intermediate versions.

<a id="the-updated-input-text-file"></a>
⓵ <strong>The Updated 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header/text/essay.txt" 
title="The pdf_05_header/text/essay.txt input text file" target="_blank">
<code>pdf_05_header/text/essay.txt</code></a> File</strong>

Further to the fixes <a href="#text-essay-file">discussed earlier</a>, we also 
made additional updates to support headers. The first lines now look like this:

```
# Thỏa Hiệp Án Fontainebleau 14/09/1946: ông Hồ cấu kết với Pháp để tiêu diệt các đảng quốc gia. 

###Tác Giả: Hứa Hoành.

## Kéo rốc sang Pháp làm gì?
...
```

As mentioned at the outset, we are using <code>Markdown</code> format: 
<code>#</code> indicates <code>header 1</code>, <code>##</code> indicates 
<code>header 2</code>, and so on. The input text file uses headers only up to 
<code>header 3</code>.
	
<a id="the-main-code-config"></a>
⓶ <strong>Font Configuration</strong>

We now discuss the configuration files  
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header/config/config-windows.toml" 
title="The pdf_05_header/config/config-windows.toml TOML file" target="_blank">
<code>pdf_05_header/config/config-windows.toml</code></a> and  
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header/config/config-linux.toml" 
title="The pdf_05_header/config/config-linux.toml TOML file" target="_blank">
<code>pdf_05_header/config/config-linux.toml</code></a>, where we specify 
font information for the different text types; and their management module  
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header/src/config.rs" 
title="The pdf_05_header/src/config.rs module" target="_blank">
<code>pdf_05_header/src/config.rs</code></a>.

Instead of having both <code>config-windows.toml</code> and <code>config-linux.toml</code>, 
we could use a single <code>config.toml</code>. For now, let’s look at 
<code>config-windows.toml</code>:

```toml
[fonts]
paragraph = { family = "Be Vietnam Pro", size = 12, weight = "normal", style = "normal" }

# Headers 1, 2, 3, 4, 5, 6.
headers = [
    { family = "Be Vietnam Pro", size = 20, weight = "bold",   style = "italic" },
    { family = "Be Vietnam Pro", size = 16, weight = "bold",   style = "normal" },
    { family = "Be Vietnam Pro", size = 14, weight = "bold", style = "italic" },
    { family = "Be Vietnam Pro", size = 15, weight = "bold",   style = "italic" },
    { family = "Be Vietnam Pro", size = 14, weight = "normal", style = "normal" },
    { family = "Be Vietnam Pro", size = 13, weight = "bold",   style = "normal" }
]

page_number = { family = "Arial", size = 10, weight = "bold", style = "normal" }
```

● <code>paragraph</code> — the font applied to normal text. The <code>family</code> 
is <code>Be Vietnam Pro</code>; <code>size</code> is <code>12</code> points; 
<code>weight = "normal"</code> means regular (not bold); 
<code>style = "normal"</code> means upright (not italic).

● <code>headers</code> — loosely speaking, <code>headers[0]</code> is the font 
applied to <code>header 1</code>, and <code>headers[5]</code> is the font applied 
to <code>header 6</code>.

● <code>page_number</code> — the font applied to the page number.  This is the only difference from <code>config-linux.toml</code>, where we also use <code>Be Vietnam Pro</code> instead of <code>Arial</code>.

The <a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header/src/config.rs" title="The pdf_05_header/src/config.rs module" target="_blank"><code>pdf_05_header/src/config.rs</code></a> module is simple and should be self‑explanatory. We take advantage of the <a href="https://crates.io/crates/serde" title="The serde crate" target="_blank">serde</a> and <a href="https://crates.io/crates/toml" title="The toml crate" target="_blank">toml</a> crates to load the configuration. 🦀 We define the <a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header/src/config.rs#L25-L28" title="The pdf_05_header/src/config.rs module | Config struct" target="_blank"><code>struct Config</code></a> so that deserialisation can take place automatically.

<a id="the-main-code-document-mod"></a>
⓷ <strong>The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header/src/document.rs" 
title="The pdf_05_header/src/document.rs module" target="_blank">
<code>pdf_05_header/src/document.rs</code></a> Module</strong>

This module defines the structures that hold the parsed contents of the input text file.

<a id="document-mod-block"></a>
● The <a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header/src/document.rs#L6-L13" title="The pdf_05_header/src/document.rs module | enum Block" target="_blank"><code>enum Block</code></a> — each <code>Block</code> represents a single line from the input text file. Consider the first few lines shown <a href="#the-updated-input-text-file">earlier</a>:

```
# Thỏa Hiệp Án Fontainebleau 14/09/1946: ông Hồ cấu kết với Pháp để tiêu diệt các đảng quốc gia. 

###Tác Giả: Hứa Hoành.

## Kéo rốc sang Pháp làm gì?
...
```

This results in five <code>Block</code>s:

<ol>
<li style="margin-top:10px;">
<code>Header</code> — <code>level</code>: 1; <code>text</code>: “Thỏa...gia.”.
</li>

<li style="margin-top:10px;">
<code>Paragraph</code> — <code>text</code>: blank line.
</li>

<li style="margin-top:10px;">
<code>Header</code> — <code>level</code>: 3; 
<code>text</code>: “Tác Giả: Hứa Hoành.”.
</li>

<li style="margin-top:10px;">
<code>Paragraph</code> — <code>text</code>: blank line.
</li>

<li style="margin-top:10px;">
<code>Header</code> — <code>level</code>: 2; 
<code>text</code>: “Kéo rốc sang Pháp làm gì?”.
</li>
</ol>	

<a id="document-mod-positionedblock"></a>
● The  
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header/src/document.rs#L15-L31" 
title="The pdf_05_header/src/document.rs module | enum PositionedBlock" target="_blank">
<code>struct PositionedBlock</code></a> — we apply the appropriate font to each 
<code>Block</code> and ask <code>Pango</code> to lay out the text in memory. As we have 
studied before, <code>Pango</code> breaks the text into lines. Each 
<code>PositionedBlock</code> contains the measured and broken lines that fit on a single 
page. It follows that <strong>a single <code>Block</code> may span multiple 
<code>PositionedBlock</code>s.</strong> Refer to the inline documentation for a detailed 
description of each field.

We discard the layout memory after measuring. When writing to the PDF, we iterate over 
the <code>PositionedBlock</code> vector, apply the same font again (ensuring identical 
line breaking), and write the lines to the PDF document.

<a id="the-main-code-main-mod"></a>
⓸ <strong>The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header/src/main.rs" 
title="The pdf_05_header/src/main.rs module" target="_blank">
<code>pdf_05_header/src/main.rs</code></a> Module</strong>

We cover some of the new code here; the rest is very similar to what we have already 
discussed in previous articles in this series.

<a id="main-mod-to_pango_description"></a>
● The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header/src/main.rs#L49-L76" 
title="The pdf_05_header/src/main.rs module | method to_pango_description()" target="_blank">
<code>to_pango_description()</code></a> method — creates and returns a 
<a href="https://docs.rs/pango/latest/pango/struct.FontDescription.html" 
title="Struct FontDescription" target="_blank"><code>pango::FontDescription</code></a> 
based on the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header/src/config.rs#L10-L16" 
title="The pdf_05_header/src/config.rs module | FontSpec struct" target="_blank">
<code>struct FontSpec</code></a> information defined in <code>config.rs</code>. 
As <a href="#install-be-vietnam-pro">mentioned earlier</a>, the selected font must 
provide the faces for the weights and styles referenced in this method.

<a id="main-mod-parse_blocks"></a>
● The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header/src/main.rs#L118-L138" 
title="The pdf_05_header/src/main.rs module | function parse_blocks_from_file()" target="_blank">
<code>parse_blocks_from_file()</code></a> function — reads the input text file 
line by line and parses each line into a <code>Block</code>, as described in 
<a href="#document-mod-block">this section</a>. It returns a vector of 
<code>Block</code>s representing the entire input text file.

<a id="main-mod-measure_block"></a>
● The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header/src/main.rs#L170-L227" 
title="The pdf_05_header/src/main.rs module | function measure_block()" target="_blank">
<code>measure_block()</code></a> function — this is perhaps the most 
tricky part of the entire codebase. For each <code>Block</code> in the vector, 
we create a memory layout using the nominated font. Then, for each layout line, 
we determine whether there is enough vertical space remaining on the current page 
to fit it; if not, we advance to the next page. This process is very similar to 
writing to the actual PDF document, except that we do not draw anything yet. 
Instead, we store the relevant layout information in 
<code>PositionedBlock</code>, as <a href="#document-mod-positionedblock">discussed earlier</a>.

🦀 The same font is applied to the entire <code>Block</code>'s text, which means 
all layout lines have the same height. However, inside the loop we still retrieve 
the height of each layout line:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">196
197
</pre></td><td class="code"><pre>        <span class="k">for</span> <span class="n">line_index</span> <span class="n">in</span> <span class="mi">0</span><span class="o">..</span><span class="n">layout</span><span class="nf">.line_count</span><span class="p">()</span> <span class="p">{</span>
            <span class="n">line_height</span> <span class="o">=</span> <span class="nf">measure_line_height</span><span class="p">(</span><span class="n">line_index</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">layout</span><span class="p">);</span>
</pre></td></tr></tbody></table></code></pre></figure>

I am aware of this oddity. In the future, we may support additional features that 
could vary text height within a single <code>Block</code>, so keeping this logic 
in place is safer.

I was caught by the following detail:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">209
210
211
</pre></td><td class="code"><pre>                <span class="c">//</span> <span class="c">Advance</span> <span class="c">y</span> <span class="c">so</span> <span class="c">the</span> <span class="c">next</span> <span class="c">line</span> <span class="c">does</span> <span class="c">not</span> <span class="c">overlap</span><span class="c">.</span>
                <span class="c">//</span> <span class="c">`</span><span class="c">line_height</span><span class="c">`</span> <span class="c">of</span> <span class="c">the</span> <span class="c">line</span> <span class="c">that</span> <span class="c">`</span><span class="c">line_index</span><span class="c">`</span> <span class="c">points</span> <span class="c">to</span><span class="c">.
                y</span> <span class="o">+=</span> <span class="n">line_height</span><span class="p">;</span>
</pre></td></tr></tbody></table></code></pre></figure>

Without advancing <code>y</code> by <code>line_height</code>, under certain 
conditions the first blank line on the next page is lost.

This method returns a vector of <code>PositionedBlock</code>. There can be more 
<code>PositionedBlock</code>s than <code>Block</code>s — this is not important 
for the implementation, but it is an interesting detail from a logical perspective.

<a id="main-mod-output-positioned-block"></a>
● The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header/src/main.rs#L229-L252" 
title="The pdf_05_header/src/main.rs module | function output_positioned_block()" target="_blank">
<code>output_positioned_block()</code></a> function — it should be clear by now 
that a <code>PositionedBlock</code> contains either <strong>the entire text</strong> or 
<strong>a partial segment</strong> of <strong>only a single <code>Block</code></strong>. 
It uses the <code>Block</code> information to create the font for the layout, and the 
<code>PositionedBlock</code> information to write the corresponding text to the PDF.

● The remaining code that we have not discussed should be straightforward and 
self‑explanatory.

The screenshots below show some PDF pages generated on 🐧 Ubuntu:

{% include image-gallery.html list=page.gallery-image-list %}
<br/>

<a id="concluding-remarks"></a>
❹ <strong>What’s Next</strong>

This heading feature feels very useful, and I’m really glad I took the time to explore it. 
In the future, I would like to support additional features—for example, 
<strong>bold</strong>, <em>italic</em>, and <strong><em>bold italic</em></strong> 
within normal paragraphs. That will be a story for another day.

Thanks for reading! I hope this post helps others who are looking to deepen their 
understanding of PDF technology. As always—stay curious, stay safe 🦊

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
<a href="https://medium.com/analytics-vidhya/rust-adventures-from-java-class-to-rust-struct-1d63b66890cf/" target="_blank">https://medium.com/analytics-vidhya/rust-adventures-from-java-class-to-rust-struct-1d63b66890cf/</a>
</li>
<li>
<a href="https://www.pngitem.com/download/ibmJoR_rust-language-hd-png-download/" target="_blank">https://www.pngitem.com/download/ibmJoR_rust-language-hd-png-download/</a>
</li>
<li>
<a href="https://en.wikipedia.org/wiki/Cairo_%28graphics%29#/media/File:Cairo_banner_closeup.svg" target="_blank">https://en.wikipedia.org/wiki/Cairo_%28graphics%29#/media/File:Cairo_banner_closeup.svg</a>
</li>
<li>
<a href="https://ur.wikipedia.org/wiki/%D9%81%D8%A7%D8%A6%D9%84:HarfBuzz.svg" target="_blank">https://ur.wikipedia.org/wiki/%D9%81%D8%A7%D8%A6%D9%84:HarfBuzz.svg</a>
</li>
<li>
<a href="https://en.wikipedia.org/wiki/Pango" target="_blank">https://en.wikipedia.org/wiki/Pango</a>
</li>
</ul>

<h3>
🦀 <a href="https://github.com/behai-nguyen/polyglot_pdf" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>