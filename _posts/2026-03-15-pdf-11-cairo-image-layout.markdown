---
layout: post
title: "Rust: PDFs — Cairo and Pango — Image Block Layout"

description: An image block is defined as an image and its caption, treated as a single unit for layout purposes. This article focuses on developing an algorithm capable of ensuring that image blocks can be rendered properly within the available effective height, as mentioned in the closing section of the immediate previous article.

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2026/03/161-01-a.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2026/03/161-01-b.png"

gallery-image-list-2:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2026/03/161-02.png"

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
- attribute
- style
- bold
- italic
- render
- image
---

<em>
An <code>image block</code> is defined as an image and its caption, treated as a single unit for layout purposes. This article focuses on developing an algorithm capable of ensuring that image blocks can be rendered properly within the available effective height, as mentioned in the closing section of the immediate <a href="https://behainguyen.wordpress.com/2026/03/06/rust-pdfs-cairo-and-pango-an-introduction-to-image-rendering/#concluding-remarks" title="Rust: PDFs — Cairo and Pango — An Introduction to Image Rendering" target="_blank">previous article</a>.
</em>

<h3>
🦀 <a href="https://github.com/behai-nguyen/polyglot_pdf" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![161-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/03/161-feature-image.png) |
|:--:|
| *Rust: PDFs — Cairo and Pango — Image Block Layout* |

<a id="repository-cloning"></a>
🚀 The code for this post is in the following GitHub repository: 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout" 
title="Rust multilingual PDFs" target="_blank">pdf_08_image_layout</a>.

<a id="ref-documentation"></a>
❶ <strong>Reference Documentation</strong>

In this article we use another method from the 
<a href="https://gtk-rs.org/gtk-rs-core/stable/latest/docs/cairo/struct.Context.html" 
title="Struct Context" target="_blank"><code>Context</code></a> <code>struct</code>:

<a href="https://gtk-rs.org/gtk-rs-core/stable/latest/docs/cairo/struct.Context.html#method.rel_move_to" 
title="Context struct | pub fn rel_move_to(&self, dx: f64, dy: f64)" 
target="_blank"><code>pub fn rel_move_to(&self, dx: f64, dy: f64)</code></a>

Its native 
<a href="https://www.cairographics.org/" title="CairoGraphics" target="_blank">
<code>CairoGraphics</code></a> documentation:

<ul>
<li style="margin-top:10px;">
<a href="https://www.cairographics.org/manual/cairo-Paths.html#cairo-rel-move-to" 
title="cairo_rel_move_to()" target="_blank"><code>cairo_rel_move_to()</code></a>
</li>
</ul>

<a id="repository-layout"></a>
❷ <strong>Repository Layout</strong>

💡 Please note: on both Windows and Ubuntu, I’m running Rust version 
<code>rustc 1.90.0 (1159e78c4 2025-09-14)</code>.

This is once again a one‑off project — I don’t plan to update it in future development. 
I want to keep a log of progress exactly as it occurred. Future code may copy this and 
make changes to it. I’ve placed the project under the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout" 
title="Rust multilingual PDFs" target="_blank">pdf_08_image_layout</a> directory. 
The structure is:

```
.
├── Cargo.toml
├── set_env.bat
├── config
│   └── config.toml
├── img
│   ├── 139015.png
│   ├── KTmCgCBjQXKLsO2JeBMVrA.png
│   ├── Readme.md
│   └── unscalable.png
├── src
│   ├── config.rs
│   ├── document.rs
│   ├── font_utils.rs
│   ├── image_layout.rs
│   ├── main.rs
│   ├── page_geometry.rs
│   └── text_layout.rs
└── .vscode
    └── launch.json
```

<a id="repository-layout-desc"></a>
We describe some modules in the following subsections. The rest will be covered in 
the sections that follow.

<a id="page-geometry-mod"></a>
⓵ The <code>src/page_geometry.rs</code> module is copied unchanged from 
<a href="https://behainguyen.wordpress.com/2026/02/23/rust-pdfs-pango-and-cairo-layout-supporting-bold-italic-and-bold-italic-text/" 
title="Rust: PDFs — Pango and Cairo Layout — Supporting Bold, Italic, and Bold Italic Text" 
target="_blank">the ninth</a> article. 👉 Changing any margin value in the 
<code>A4_DEFAULT_MARGINS</code> constant will change the layout of the text in the PDF.

<a id="font-utils-mod"></a>
⓶ The <code>src/font_utils.rs</code> and <code>src/document.rs</code> modules 
are also copied unchanged from 
<a href="https://behainguyen.wordpress.com/2026/02/23/rust-pdfs-pango-and-cairo-layout-supporting-bold-italic-and-bold-italic-text/" 
title="Rust: PDFs — Pango and Cairo Layout — Supporting Bold, Italic, and Bold Italic Text" 
target="_blank">the ninth</a> article.

<a id="path-env-var"></a>
⓷ 💡 The code requires the <code>Pango</code>, <code>HarfBuzz</code>, <code>Cairo</code>, 
etc. libraries. 🐧 On Ubuntu, all required libraries are globally recognised. 🪟 On Windows, 
I haven’t added the paths for the libraries’ DLLs to the <code>PATH</code> environment 
variable. In each new Windows terminal session, I run the following once:

```
set PATH=C:\PF\harfbuzz\dist\bin\;%PATH%
set PATH=C:\PF\vcpkg\installed\x64-windows\bin\;%PATH%
set PATH=C:\PF\pango\dist\bin;C:\PF\cairo-1.18.4\dist\bin;C:\PF\fribidi\dist\bin;%PATH%
```

Alternatively, you can simply run 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout/set_env.bat" 
title="pdf_08_image_layout/set_env.bat file" target="_blank"><code>set_env.bat</code></a>. 
After that, <code>cargo run</code> works as expected.

<a id="pkg-config-path-env-var"></a>
⓸ 💡 In the fifth article, we discussed the 
<a href="https://behainguyen.wordpress.com/2025/12/19/rust-pdfs-build-and-install-pango-and-associated-libraries/#windows-build-install-pango" 
title="Rust: PDFs — Build and Install Pango and Associated Libraries" target="_blank">
<code>PKG_CONFIG_PATH</code></a> user environment variable. This setting applies to all 
later articles. I did not mention it again from the sixth article onward. In the 
<code>set_env.bat</code> above, I include setting this variable so that we don't forget 
it and avoid potential surprises.

<a id="layout-algorithm"></a>
❸ <strong>The Image Block Layout Algorithm</strong>

As <a href="https://behainguyen.wordpress.com/2026/03/06/rust-pdfs-cairo-and-pango-an-introduction-to-image-rendering/#concluding-remarks" 
title="Rust: PDFs — Cairo and Pango — An Introduction to Image Rendering" 
target="_blank">previously mentioned</a>, we are going to extend the existing 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro/src/image_layout.rs#L39-L111" 
title="The pdf_07_image_intro/src/image_layout.rs module | render_image_block() function" target="_blank">
<code>render_image_block()</code></a> function to support rendering an image and its 
caption as a single image block, and give the extended version some essential intelligence, 
such as ensuring the image block can be rendered properly within the available effective 
height.

<a id="layout-algorithm-new-params"></a>
The new algorithm introduces several additional parameters:

<ol>
<li style="margin-top:10px;">
<code>step_scale_factor</code> — a factor used to progressively reduce the 
image scale when attempting to make the image block fit within the available 
vertical space.
</li>

<li style="margin-top:10px;">
<code>min_allowed_scale</code> — the minimum acceptable scale factor. 
If the scale falls below this value, layout is considered to have failed.
</li>

<li style="margin-top:10px;">
<code>image_block_spacing</code> — vertical spacing (in points) added below 
each image caption to create a natural visual gap before the next block. This 
parameter is not included in the scaling calculation; as long as the image block 
fits, it does not matter whether there is enough remaining vertical space for this 
gap — if not, a new page will be created for the next block.
</li>
</ol>

<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro/src/image_layout.rs#L39-L111" 
title="The pdf_07_image_intro/src/image_layout.rs module | render_image_block() function" target="_blank">
<code>render_image_block()</code></a> already performs the following:

<ul>
<li style="margin-top:10px;">
Computes the scale factor required to fit the image within
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/page_geometry.rs#L30-L32" 
title="The pdf_06_text_styling/src/page_geometry.rs module | a4_default_content_width() function" 
target="_blank"><code>a4_default_content_width()</code></a>.
</li>

<li style="margin-top:10px;">
Applies <code>reduction_factor</code> to obtain the initial final scale factor.
(The image is not scaled yet; this value is used only for layout calculations.)
</li>
</ul>

<a id="layout-algorithm-extended"></a>
The extended algorithm then carries out the following steps:

<ol>
<li style="margin-top:10px;"> <!-- 1 -->
If the image scaled by the final scale factor, together with its caption,
fits in the remaining space on the current page, render the block and
return successfully.
</li>

<li style="margin-top:10px;"> <!-- 2 -->
If the block does not fit, progressively reduce the final scale factor by
multiplying it with <code>step_scale_factor</code>.

    <ol type="a">
    <li style="margin-top:10px;"> <!-- a -->
    After each reduction, if the block fits on the current page, render it
    and return successfully.
    </li>	

    <li style="margin-top:10px;"> <!-- b -->
    If the scale factor becomes smaller than <code>min_allowed_scale</code>, proceed
    to step 3.
    </li>	
	</ol>
</li>

<li style="margin-top:10px;"> <!-- 3 -->
Attempt to render the image block on a new page:

    <ol type="a">
    <li style="margin-top:10px;"> <!-- a -->
    Repeat the progressive‑reduction loop described in step <strong>2a</strong> 
	(<strong>2.1</strong>).
    </li>

    <li style="margin-top:10px;"> <!-- b -->
    If the block still does not fit even on a fresh page, return an error.
    It is up to the caller to decide how to handle this failure.
    </li>	
	</ol>
</li>
</ol>

🦀 It should be apparent that the image block is either rendered on the current page 
at the current y‑coordinate, or on a new page at 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout/src/page_geometry.rs#L18-L28" 
title="The pdf_08_image_layout/src/config.rs module | A4_DEFAULT_MARGINS" target="_blank">
<code>A4_DEFAULT_MARGINS.top</code></a>.

<a id="configuration-updates"></a>
❹ <strong>Configuration Updates</strong>

We discuss the configuration updates required to support the extended algorithm: the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout/config/config.toml" 
title="The pdf_08_image_layout/config/config.toml file" target="_blank">
<code>pdf_08_image_layout/config/config.toml</code></a> file, and the 
Rust configuration module 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout/src/config.rs" 
title="The pdf_08_image_layout/src/config.rs module" target="_blank">
<code>pdf_08_image_layout/src/config.rs</code></a>.

<a id="config-toml"></a>
⓵ <strong>The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout/config/config.toml" 
title="The pdf_08_image_layout/config/config.toml file" target="_blank">
<code>pdf_08_image_layout/config/config.toml</code></a> File
</strong>

We made a few additions:

● Under <code>[fonts]</code>, added  
<code>caption = { family = "Be Vietnam Pro", size = 12, weight = "normal", style = "italic" }</code>,  
which is the font used for image captions. 💡 The <code>Be Vietnam Pro</code> font 
was installed in the  
<a href="https://behainguyen.wordpress.com/2026/01/30/rust-pdfs-pango-and-cairo-layout-supporting-headers/" 
title="Rust: PDFs — Pango and Cairo Layout — Supporting Headers" 
target="_blank">eighth post</a>.

● Added 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout/config/config.toml#L18-L36" 
title="[layout] and [image_block] entries" target="_blank"><code>[layout]</code> and 
<code>[image_block]</code></a> sections:

🙏️ Under <code>[image_block]</code>, the entries <code>reduction_factor</code> and 
<code>centre_aligned</code> correspond to the  
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro/src/image_layout.rs#L39-L111" 
title="The pdf_07_image_intro/src/image_layout.rs module | render_image_block() function" target="_blank">
<code>render_image_block()</code></a> parameters that have now been externalised. 
The entries <code>step_scale_factor</code> and <code>min_allowed_scale</code> are the new 
parameters <a href="#layout-algorithm-new-params">discussed above</a>.

🙏️ Under <code>[layout]</code>, the <code>image_block_spacing</code> entry has also been 
discussed in the same <a href="#layout-algorithm-new-params">section</a>.

<a id="config-mod"></a>
⓶ <strong>The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout/src/config.rs" 
title="The pdf_08_image_layout/src/config.rs module" target="_blank">
<code>pdf_08_image_layout/src/config.rs</code></a> Module
</strong>

We added new fields to existing structs and introduced new structs to hold the newly added 
configuration tables <code>[image_block]</code> and <code>[layout]</code> — these should be 
self‑explanatory. A more general 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout/src/config.rs#L126-L129" 
title="The pdf_08_image_layout/src/config.rs module | load_config()" target="_blank">
<code>load_config()</code></a> function replaces the previous 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout/src/config.rs#L119-L124" 
title="The pdf_08_image_layout/src/config.rs module | load_font_config()" target="_blank">
<code>load_font_config()</code></a>.

<a id="text-layout-mod"></a>
❺ <strong>The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout/src/text_layout.rs" 
title="The pdf_08_image_layout/src/text_layout.rs module" target="_blank">
<code>pdf_08_image_layout/src/text_layout.rs</code></a>
</strong>

This module is new, but most of the code has already been covered in earlier articles.

⓵ The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout/src/text_layout.rs#L12-L23" 
title="The pdf_08_image_layout/src/text_layout.rs module | LayoutExtJustify trait" 
target="_blank"><code>LayoutExtJustify trait</code></a> — this was first 
discussed in detail in the sixth post, in the section 
<a href="https://behainguyen.wordpress.com/2025/12/27/rust-pdfs-exploring-layout-with-pango-and-cairo/#pango-justification" 
title="Rust: PDFs — Exploring Layout with Pango and Cairo" target="_blank">On 
<code>Pango</code> Justification</a>, and was first illustrated in the accompanying module 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_03_pango/src/main_fully_justified.rs" 
title="The pdf_03_pango/src/main_fully_justified.rs module" target="_blank">
<code>pdf_03_pango/src/main_fully_justified.rs</code></a>. It has been used throughout 
later articles ever since.

⓶ The helper functions are short and should be easy to follow. 💡 Please note that the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout/src/text_layout.rs#L62-L84" 
title="The pdf_08_image_layout/src/text_layout.rs module | center_layout_block() function" 
target="_blank"><code>center_layout_block()</code></code></a> function calls 
<code>context.rel_move_to(offset_x, 0.0)</code>, whose documentation references were 
<a href="#ref-documentation">listed earlier</a>.

<a id="image-layout-mod"></a>
❻ <strong>The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout/src/image_layout.rs" 
title="The pdf_08_image_layout/src/text_layout.rs module" target="_blank">
<code>pdf_08_image_layout/src/image_layout.rs</code></a>
</strong>

This is the main focus of this article. The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro/src/image_layout.rs#L39-L111" 
title="The pdf_07_image_intro/src/image_layout.rs module | render_image_block() function" target="_blank">
<code>render_image_block()</code></a> function is no longer relevant and has been removed.

<a id="image-layout-api"></a>
The API is now the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout/src/image_layout.rs#L176-L298" 
title="The pdf_08_image_layout/src/text_layout.rs module | layout_image_block() function" target="_blank">
<code>layout_image_block()</code></code></a> function. It is fully documented.

The main helper function, 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout/src/image_layout.rs#L68-L169" 
title="The pdf_08_image_layout/src/text_layout.rs module | step_scale_image() function" target="_blank">
<code>step_scale_image()</code></code></a>, performs the progressive‑scaling 
calculation — note that it only determines the appropriate scale factor; it does not 
actually scale the image. 💡 The image is scaled only once, at the point of rendering.

Together with the <a href="#layout-algorithm">extended algorithm</a> discussion and the 
module documentation, we are not going to cover the code in detail here.

<a id="image-layout-test"></a>
💡 Please pay special attention to the tests — they cover several edge cases. Tests 
should be read in conjunction with the inline documentation.

<a id="main-mod"></a>
❼ <strong>The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout/src/main.rs" 
title="The pdf_08_image_layout/src/main.rs module" target="_blank">
<code>pdf_08_image_layout/src/main.rs</code></a>
</strong>

This module demonstrates the API function 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout/src/image_layout.rs#L176-L298" 
title="The pdf_08_image_layout/src/text_layout.rs module | layout_image_block() function" target="_blank">
<code>layout_image_block()</code></a>. We can tweak the configuration 
parameters and the <code>top_y</code> value of the first call:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">33
34
35
36
37
38
39
40
</pre></td><td class="code"><pre>    <span class="k">let</span> <span class="n">caption</span><span class="p">:</span> <span class="o">&amp;</span><span class="nb">str</span> <span class="o">=</span> <span class="s">"Cassowary, an Australia native, and “the world's most dangerous bird”.</span><span class="se">\n</span><span class="err">\</span><span class="s">
        Cassowary, chim bản địa Úc, và là “loài chim nguy hiểm nhất thế giới”."</span><span class="p">;</span>
    <span class="c">//</span> <span class="c">Define</span> <span class="c">the</span> <span class="c">input</span> <span class="c">PNG</span> <span class="c">image</span> <span class="c">file</span> <span class="c">name</span> <span class="c">(</span><span class="c">ensure</span> <span class="c">this</span> <span class="c">file</span> <span class="c">exists</span><span class="c">)</span><span class="py">.
    let</span> <span class="n">png_file_name</span> <span class="o">=</span> <span class="s">"./img/139015.png"</span><span class="p">;</span>
    <span class="k">let</span> <span class="n">image_bottom</span> <span class="o">=</span> <span class="nf">layout_image_block</span><span class="p">(</span><span class="n">png_file_name</span><span class="p">,</span> <span class="n">caption</span><span class="p">,</span> 
        <span class="c">//</span> <span class="c">A4_DEFAULT_MARGINS</span><span class="c">.top</span><span class="c">,</span> 
        <span class="mf">200.00</span><span class="p">,</span>
        <span class="o">&amp;</span><span class="n">context</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">config</span><span class="p">)</span><span class="o">?</span><span class="p">;</span>
</pre></td></tr></tbody></table></code></pre></figure>

to experiment with how the output changes. At a <code>top_y</code> of 
<code>200.00</code>, the output appears as shown in the screenshots below:

{% include image-gallery.html list=page.gallery-image-list-1 %}
<br/>

There is not enough space on the first page, so the second image block is rendered 
on the second page at the default y‑coordinate of 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout/src/page_geometry.rs#L18-L28" 
title="The pdf_08_image_layout/src/config.rs module | A4_DEFAULT_MARGINS" target="_blank">
<code>A4_DEFAULT_MARGINS.top</code></a>.

Changing <code>top_y</code> to <code>A4_DEFAULT_MARGINS.top</code> (instead of 
<code>200.00</code>, as shown in lines 38–39 above) places both image blocks on a single 
page, as illustrated in the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-2 %}
<br/>

<a id="concluding-remarks"></a>
❽ <strong>What’s Next</strong>

We conclude this article… The next main objective remains the same: enabling 
the <code>Markdown</code> parser we 
<a href="https://behainguyen.wordpress.com/2026/02/23/rust-pdfs-pango-and-cairo-layout-supporting-bold-italic-and-bold-italic-text/#concluding-remarks" 
title="Rust: PDFs — Pango and Cairo Layout — Supporting Bold, Italic, and Bold Italic Text" 
target="_blank">last discussed</a> to support image blocks, where images are specified 
using relative paths, similar to how it is done in 
<a href="https://www.latex-project.org/" title="The LaTeX Project" target="_blank">LaTeX</a>. 
And we are now ready to take this next step. We will add this feature to the parser in the 
next article.

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