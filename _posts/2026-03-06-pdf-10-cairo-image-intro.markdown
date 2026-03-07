---
layout: post
title: "Rust: PDFs — Cairo and Pango — An Introduction to Image Rendering"

description: Using the CairoGraphics library to render images onto PDFs. This article explores the basic image‑rendering functionalities provided by Cairo. The final objective is to incorporate image support into the Markdown minimum parser implemented in the previous article.

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

*Using the <a href="https://www.cairographics.org/" title="CairoGraphics" target="_blank"><code>CairoGraphics</code></a> library to render images onto PDFs. This article explores the basic image‑rendering functionalities provided by Cairo. The final objective is to incorporate image support into the <code>Markdown</code> minimum parser implemented in the <a href="https://behainguyen.wordpress.com/2026/02/23/rust-pdfs-pango-and-cairo-layout-supporting-bold-italic-and-bold-italic-text/#concluding-remarks" title="Rust: PDFs — Pango and Cairo Layout — Supporting Bold, Italic, and Bold Italic Text" target="_blank">previous article</a>.*

<h3>
🦀 <a href="https://github.com/behai-nguyen/polyglot_pdf" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![160-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/03/160-feature-image.png) |
|:--:|
| *Rust: PDFs — Cairo and Pango — An Introduction to Image Rendering* |

<a id="repository-cloning"></a>
🚀 The code for this post is in the following GitHub repository: 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro" 
title="Rust multilingual PDFs" target="_blank">pdf_07_image_intro</a>.

<a id="ref-documentation"></a>
❶ <strong>Reference Documentation</strong>

To render images, we explore the 
<a href="https://gtk-rs.org/gtk-rs-core/stable/latest/docs/cairo/" 
title="cairo-rs: Rust bindings for the Cairo library" 
target="_blank"><code>cairo-rs</code></a> crate’s 
<a href="https://gtk-rs.org/gtk-rs-core/stable/latest/docs/cairo/struct.ImageSurface.html" 
title="Struct ImageSurface" target="_blank"><code>ImageSurface</code></a> 
<code>struct</code>. Only the following 
<a href="https://gtk-rs.org/gtk-rs-core/stable/latest/docs/cairo/#fileformat-features" 
title="cairo-rs: Rust bindings for the Cairo library | Fileformat features" 
target="_blank">file formats</a> are supported: <strong>png</strong>, <strong>pdf</strong>, 
<strong>svg</strong>, and <strong>ps</strong>. For this article, we use 
<strong>png</strong> images. The function we are interested in is:

<ul>
<li style="margin-top:10px;">
<a href="https://gtk-rs.org/gtk-rs-core/stable/latest/docs/cairo/struct.ImageSurface.html#method.create_from_png" 
title="ImageSurface struct | pub fn create_from_png&lt;R: Read&gt;(stream: &mut R) -&gt; Result&lt;ImageSurface, IoError&gt;" 
target="_blank"><code>pub fn create_from_png<R: Read&gt;(stream: &mut R) -&gt; Result<ImageSurface, IoError&gt;</code></a>
</li>
</ul>

Its native 
<a href="https://www.cairographics.org/" title="CairoGraphics" 
target="_blank"><code>CairoGraphics</code></a> documentation:

<ul>
<li style="margin-top:10px;">
<a href="https://www.cairographics.org/manual/cairo-PNG-Support.html" 
title="PNG Support — Reading and writing PNG images" target="_blank">PNG Support — Reading and writing PNG images</a>
</li>
<li style="margin-top:10px;">
Under the hood, <code>create_from_png()</code> calls the native function: 
<a href="https://www.cairographics.org/manual/cairo-PNG-Support.html#cairo-image-surface-create-from-png-stream" 
title="cairo_image_surface_create_from_png_stream()" 
target="_blank"><code>cairo_image_surface_create_from_png_stream()</code></a>
</li>
</ul>

From the 
<a href="https://gtk-rs.org/gtk-rs-core/stable/latest/docs/cairo/struct.Context.html" 
title="Struct Context" target="_blank"><code>Context</code></a> <code>struct</code>, 
we will explore the following methods:  
<a href="https://gtk-rs.org/gtk-rs-core/stable/latest/docs/cairo/struct.Context.html#method.save" 
title="Context struct | pub fn save(&self) -&gt; Result&lt;(), Error&gt;" 
target="_blank"><code>pub fn save(&self) -&gt; Result&lt;(), Error&gt;</code></a>, 
<a href="https://gtk-rs.org/gtk-rs-core/stable/latest/docs/cairo/struct.Context.html#method.restore" 
title="Context struct | pub fn restore(&self) -&gt; Result&lt;(), Error&gt;" 
target="_blank"><code>pub fn restore(&self) -&gt; Result&lt;(), Error&gt;</code></a>, 
 <a href="https://gtk-rs.org/gtk-rs-core/stable/latest/docs/cairo/struct.Context.html#method.set_source_surface" 
title="Context struct | pub fn set_source_surface(&self, surface: impl AsRef&lt;Surface&gt;, x: f64, y: f64,) -&gt; Result&lt;(), Error&gt;" 
target="_blank"><code>pub fn set_source_surface(&self, surface: impl AsRef&lt;Surface&gt;, x: f64, y: f64,) -&gt; Result&lt;(), Error&gt;</code></a>,  
<a href="https://gtk-rs.org/gtk-rs-core/stable/latest/docs/cairo/struct.Context.html#method.paint" 
title="Context struct | pub fn paint(&self) -&gt; Result&lt;(), Error&gt;" 
target="_blank"><code>pub fn paint(&self) -&gt; Result&lt;(), Error&gt;</code></a>, 
<a href="https://gtk-rs.org/gtk-rs-core/stable/latest/docs/cairo/struct.Context.html#method.translate" 
title="Context struct | pub fn translate(&self, tx: f64, ty: f64)" 
target="_blank"><code>pub fn translate(&self, tx: f64, ty: f64)</code></a>, and  
<a href="https://gtk-rs.org/gtk-rs-core/stable/latest/docs/cairo/struct.Context.html#method.scale" 
title="Context struct | pub fn scale(&self, sx: f64, sy: f64)" 
target="_blank"><code>pub fn scale(&self, sx: f64, sy: f64)</code></a>.

The <code>save()</code> and <code>restore()</code> methods are relatively 
straightforward. Their native 
<a href="https://www.cairographics.org/" title="CairoGraphics" 
target="_blank"><code>CairoGraphics</code></a> documentation:

<ul>
<li style="margin-top:10px;">
<a href="https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-save" 
title="cairo_save()" target="_blank"><code>cairo_save()</code></a>
</li>
<li style="margin-top:10px;">
<a href="https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-restore" 
title="cairo_restore()" target="_blank"><code>cairo_restore()</code></a>
</li>
</ul>

The Rust methods <code>set_source_surface()</code> and <code>paint()</code> call the 
native functions:

<ul>
<li style="margin-top:10px;">
<a href="https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-set-source-surface" 
title="cairo_set_source_surface()" target="_blank"><code>cairo_set_source_surface()</code></a>
</li>
<li style="margin-top:10px;">
<a href="https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-paint" 
title="cairo_paint()" target="_blank"><code>cairo_paint()</code></a>
</li>
</ul>

The <code>translate()</code> and <code>scale()</code> methods fall under the 
<a href="https://www.cairographics.org/manual/cairo-Transformations.html" 
title="Transformations" target="_blank">Transformations</a> category. Their native 
<a href="https://www.cairographics.org/" title="CairoGraphics" 
target="_blank"><code>CairoGraphics</code></a> documentation:

<ul>
<li style="margin-top:10px;">
<a href="https://www.cairographics.org/manual/cairo-Transformations.html#cairo-translate" 
title="cairo_translate()" target="_blank"><code>cairo_translate()</code></a>
</li>
<li style="margin-top:10px;">
<a href="https://www.cairographics.org/manual/cairo-Transformations.html#cairo-scale" 
title="cairo_scale()" target="_blank"><code>cairo_scale()</code></a>
</li>
</ul>

🙏 Please recall that we used a function from this transformations category in another 
<a href="https://behainguyen.wordpress.com/2026/01/16/rust-pdfs-text-rotation-with-cairo-and-pango/" 
title="Rust: PDFs — Text Rotation with Cairo and Pango" 
target="_blank">previous article</a>.

<a id="repository-layout"></a>
❷ <strong>Repository Layout</strong>

💡 Please note: on both Windows and Ubuntu, I’m running Rust version 
<code>rustc 1.90.0 (1159e78c4 2025-09-14)</code>.

This is once again a one‑off project—I don’t plan to update it in future development. 
I want to keep a log of progress exactly as it occurred. Future code may copy this and 
make changes to it. I’ve placed the project under the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro" 
title="Rust multilingual PDFs" target="_blank">pdf_07_image_intro</a> directory. 
The structure is:

```
.
├── Cargo.toml
├── set_env.bat
├── img
│   ├── 139015.png
│   ├── KTmCgCBjQXKLsO2JeBMVrA.png
│   └── Readme.md
└── src
    ├── image_layout.rs
    ├── main_01.rs
    ├── main_02.rs
    ├── main_03.rs
    ├── main_04.rs
    ├── main_05.rs
    ├── main_06.rs
    ├── main_07.rs
    ├── main.rs
    └── page_geometry.rs
```

<a id="repository-layout-desc"></a>
We describe some modules in the following subsections. The rest will be covered in 
the sections that follow.

<a id="page-geometry-mod"></a>
⓵ The <code>src/page_geometry.rs</code> module is copied unchanged from the immediate 
<a href="https://behainguyen.wordpress.com/2026/02/23/rust-pdfs-pango-and-cairo-layout-supporting-bold-italic-and-bold-italic-text/#concluding-remarks" 
title="Rust: PDFs — Pango and Cairo Layout — Supporting Bold, Italic, and Bold Italic Text" 
target="_blank">previous article</a>. 👉 Changing any margin value in the 
<code>A4_DEFAULT_MARGINS</code> constant will change the layout of the text in the PDF.

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
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro/set_env.bat" 
title="pdf_07_image_intro/set_env.bat file" target="_blank"><code>set_env.bat</code></a>.  
After that, <code>cargo run</code> works as expected.

<a id="pkg-config-path-env-var"></a>
⓷ 💡 In the fifth article, we discussed the 
<a href="https://behainguyen.wordpress.com/2025/12/19/rust-pdfs-build-and-install-pango-and-associated-libraries/#windows-build-install-pango" 
title="Rust: PDFs — Build and Install Pango and Associated Libraries" target="_blank">
<code>PKG_CONFIG_PATH</code></a> user environment variable. This setting applies to all 
later articles. I did not mention it again from the sixth article onward. In the 
<code>set_env.bat</code> above, I include setting this variable so that we don't forget 
it and avoid potential surprises.

<a id="cargo-file"></a>
❸ <strong>The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro/Cargo.toml" 
title="The pdf_07_image_intro/src/main_01.rs module" target="_blank">
<code>pdf_07_image_intro/Cargo.toml</code></a> File
</strong>

For the <a href="https://gtk-rs.org/gtk-rs-core/stable/latest/docs/cairo/" title="cairo-rs: 
Rust bindings for the Cairo library" target="_blank"><code>cairo-rs</code></a> crate, in 
addition to the <strong>pdf</strong> feature—which we have been enabling—the 
<strong>png</strong> feature needs to be active as well. We can either edit 
<code>Cargo.toml</code> directly to enable these features, or use the 
<code>cargo add</code> command:

```
cargo add cairo-rs --features cairo-rs/pdf,png
```

💥 Note <code>cairo-rs/pdf,png</code> — there is no space before or after the comma (,).  
Also, I am not entirely sure why the feature is named <code>cairo-rs/pdf</code> 😂.  
The order of the required features does not appear to matter. The following order also works:

```
cargo add cairo-rs --features png,cairo-rs/pdf
```

Next, we cover the image‑rendering code—the <code>main*.rs</code> modules—and, in the 
process, the <code>image_layout.rs</code> module.

<a id="image-rendering-code"></a>
❹ <strong>The Image Rendering Code</strong>

I am writing down the steps I took to understand image rendering.  
🙏 I am simply sharing my learning process — please do not treat this article as a 
tutorial.

<a id="main-01-module"></a>
<strong>⓵ The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro/src/main_01.rs" 
title="The pdf_07_image_intro/src/main_01.rs module" target="_blank">
<code>pdf_07_image_intro/src/main_01.rs</code></a> Module
</strong>

The code excerpt below is the image‑rendering logic, written to be as simple as possible:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
</pre></td><td class="code"><pre>    <span class="k">let</span> <span class="n">surface</span> <span class="o">=</span> <span class="nn">PdfSurface</span><span class="p">::</span><span class="nf">new</span><span class="p">(</span><span class="nf">a4_default_content_width</span><span class="p">(),</span> 
        <span class="nf">a4_default_content_height</span><span class="p">(),</span> <span class="n">pdf_file_name</span><span class="p">)</span><span class="o">?</span><span class="p">;</span>

    <span class="k">let</span> <span class="n">context</span> <span class="o">=</span> <span class="nn">Context</span><span class="p">::</span><span class="nf">new</span><span class="p">(</span><span class="o">&amp;</span><span class="n">surface</span><span class="p">)</span><span class="o">?</span><span class="p">;</span>

    <span class="c">//</span> <span class="c">Reserve</span> <span class="c">the</span> <span class="c">entire</span> <span class="c">context</span><span class="c">. Painting</span> <span class="c">an</span> <span class="c">image</span> <span class="c">will</span> <span class="c">alter</span> <span class="c">some</span> <span class="c">context</span> <span class="c">information</span><span class="py">.
    context</span><span class="nf">.save</span><span class="p">()</span><span class="nf">.expect</span><span class="p">(</span><span class="s">"Failed to save cairo context"</span><span class="p">);</span>

    <span class="c">//</span> <span class="c">Define</span> <span class="c">the</span> <span class="c">input</span> <span class="c">PNG</span> <span class="c">image</span> <span class="c">file</span> <span class="c">name</span> <span class="c">(</span><span class="c">ensure</span> <span class="c">this</span> <span class="c">file</span> <span class="c">exists</span><span class="c">)</span><span class="py">.
    let</span> <span class="n">png_file_name</span> <span class="o">=</span> <span class="s">"./img/139015.png"</span><span class="p">;</span> 
    <span class="o">//</span> <span class="c">Load</span> <span class="c">the</span> <span class="c">PNG</span> <span class="c">image</span> <span class="c">into</span> <span class="c">an</span> <span class="c">ImageSurface</span><span class="c">.</span>
    <span class="o">//</span> <span class="c">The</span> <span class="c">cairo</span> <span class="c">library</span> <span class="c">provides</span> <span class="c">a</span> <span class="c">function</span> <span class="c">for</span> <span class="c">this</span><span class="c">,</span> <span class="c">accessible</span> <span class="c">via</span> <span class="c">the</span> <span class="c">Rust</span> <span class="c">bindings</span><span class="py">.
    let</span> <span class="k">mut</span> <span class="n">img_file</span> <span class="o">=</span> <span class="nn">File</span><span class="p">::</span><span class="nf">open</span><span class="p">(</span><span class="n">png_file_name</span><span class="p">)</span><span class="o">?</span><span class="p">;</span>
    <span class="k">let</span> <span class="n">image_surface</span> <span class="o">=</span> <span class="nn">ImageSurface</span><span class="p">::</span><span class="nf">create_from_png</span><span class="p">(</span><span class="o">&amp;</span><span class="k">mut</span> <span class="n">img_file</span><span class="p">)</span>
        <span class="nf">.map_err</span><span class="p">(|</span><span class="n">e</span><span class="p">|</span> <span class="nd">format!</span><span class="p">(</span><span class="s">"Failed to create image surface from PNG: {}"</span><span class="p">,</span> <span class="n">e</span><span class="p">))</span><span class="o">?</span><span class="p">;</span>

    <span class="c">//</span> <span class="c">Draw</span> <span class="c">the</span> <span class="c">Image</span> <span class="c">onto</span> <span class="c">the</span> <span class="c">PDF</span> <span class="c">Surface</span><span class="c">:</span>
    <span class="c">//</span> <span class="c">Set</span> <span class="c">the</span> <span class="c">image</span> <span class="c">surface</span> <span class="c">as</span> <span class="c">the</span> <span class="c">source</span> <span class="c">pattern</span> <span class="c">for</span> <span class="c">drawing</span>
    <span class="c">//</span> <span class="c">Draw</span> <span class="c">at</span> <span class="c">position</span> <span class="c">(</span><span class="c">A4_DEFAULT_MARGINS</span><span class="c">.left</span><span class="c">,</span> <span class="c">A4_DEFAULT_MARGINS</span><span class="c">.top</span><span class="c">)</span><span class="py">.
    context</span><span class="nf">.set_source_surface</span><span class="p">(</span><span class="o">&amp;</span><span class="n">image_surface</span><span class="p">,</span> <span class="n">A4_DEFAULT_MARGINS</span><span class="py">.left</span><span class="p">,</span> <span class="n">A4_DEFAULT_MARGINS</span><span class="py">.top</span><span class="p">)</span><span class="o">?</span><span class="p">;</span>

    <span class="c">//</span> <span class="c">Paint</span> <span class="c">the</span> <span class="c">source</span> <span class="c">surface</span> <span class="c">onto</span> <span class="c">the</span> <span class="c">current</span> <span class="c">target</span> <span class="nf">surface</span> <span class="c">(</span><span class="c">the</span> <span class="c">PDF</span> <span class="c">surface</span><span class="c">)</span><span class="py">.
    context</span><span class="nf">.paint</span><span class="p">()</span><span class="o">?</span><span class="p">;</span>

    <span class="c">//</span> <span class="c">Restore</span> <span class="c">the</span> <span class="c">original</span> <span class="c">context</span><span class="py">.
    context</span><span class="nf">.restore</span><span class="p">()</span><span class="nf">.expect</span><span class="p">(</span><span class="s">"Failed to restore cairo context"</span><span class="p">);</span>
</pre></td></tr></tbody></table></code></pre></figure>

The code should be self‑explanatory. These are the essential calls required to render 
an image. The next part of the code — the text rendering — should already be familiar.

💡 Disable <code>context.save()</code> and <code>context.restore()</code>, then build and run 
the module. The text <code>Hello, Cairo PDF with PNG!</code> will no longer be visible. 
Now enable line 61:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">61
</pre></td><td class="code"><pre><span class="o">//</span> <span class="c">context</span><span class="c">.set_source_rgb</span><span class="c">(</span><span class="c">1.0</span><span class="c">,</span> <span class="c">0.0</span><span class="c">,</span> <span class="c">0.0</span><span class="c">);</span> <span class="c">//</span> <span class="c">or</span> <span class="c">any</span> <span class="c">color</span><span class="c">...</span>
</pre></td></tr></tbody></table></code></pre></figure>

The text <span style="color:red;"><code>Hello, Cairo PDF with PNG!</code></span> appears in 
<span style="color:red;"><strong>red</strong></span>. Image rendering alters the context 
state, so using <code>context.save()</code> and <code>context.restore()</code> is the 
recommended approach to preserve context information.

💥 The most important thing to notice in the PDF output is that only part of the image 
fills the entire page. See the screenshot below:

![160-01.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/03/160-01.png)

This is intentional and expected, because we already knew the image is much larger than 
the effective page area. We need to scale the image to fit the page. Let’s look at the 
next module, where we do exactly that.

<a id="main-02-module"></a>
<strong>⓶ The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro/src/main_02.rs" 
title="The pdf_07_image_intro/src/main_02.rs module" target="_blank">
<code>pdf_07_image_intro/src/main_02.rs</code></a> Module
</strong>

To keep the code focused, this module does not render any text.  
First, we introduce a helper function:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">19
20
21
</pre></td><td class="code"><pre><span class="k">fn</span> <span class="nf">get_scaling_factor</span><span class="p">(</span><span class="n">img_surface</span><span class="p">:</span> <span class="o">&amp;</span><span class="n">ImageSurface</span><span class="p">)</span> <span class="k">-&gt;</span> <span class="nb">f64</span> <span class="p">{</span>
    <span class="nf">a4_default_content_width</span><span class="p">()</span> <span class="o">/</span> <span class="n">img_surface</span><span class="nf">.width</span><span class="p">()</span> <span class="k">as</span> <span class="nb">f64</span>
<span class="p">}</span>
</pre></td></tr></tbody></table></code></pre></figure>

The scaling factor ensures the image fits within  
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro/src/page_geometry.rs#L30-L32" 
title="The pdf_07_image_intro/src/page_geometry.rs module | a4_default_content_width() function" target="_blank">
<code>a4_default_content_width()</code></a>.  
It may scale the image up or down depending on its width.  
In all cases, the image is resized so that its width matches 
<code>a4_default_content_width()</code>.

There are two changes and some new code related specifically to scaling.  
The first change is:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">30
</pre></td><td class="code"><pre>    <span class="k">let</span> <span class="n">surface</span> <span class="o">=</span> <span class="nn">PdfSurface</span><span class="p">::</span><span class="nf">new</span><span class="p">(</span><span class="n">A4</span><span class="py">.width</span><span class="p">,</span> <span class="n">A4</span><span class="py">.height</span><span class="p">,</span> <span class="n">pdf_file_name</span><span class="p">)</span><span class="o">?</span><span class="p">;</span>
</pre></td></tr></tbody></table></code></pre></figure>

Note that the first two parameters are now <code>A4.width</code> and 
<code>A4.height</code>, instead of <code>a4_default_content_width()</code> and 
<code>a4_default_content_height()</code>.

🦀 I cannot offer a concise explanation for why this is required.  
Even though the image width is scaled to <code>a4_default_content_width()</code>,  
when rendered at  
<code>(A4_DEFAULT_MARGINS.left, A4_DEFAULT_MARGINS.top)</code>,  
it extends all the way to the right edge — the right margin disappears.  
I suspect this is related to how scaling affects the coordinate system.  
Using <code>A4.width</code> resolves the issue.

The second part is the following new and modified code:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">45
46
47
48
49
50
51
52
53
54
55
56
</pre></td><td class="code"><pre>    <span class="k">let</span> <span class="n">scale_factor</span> <span class="o">=</span> <span class="nf">get_scaling_factor</span><span class="p">(</span><span class="o">&amp;</span><span class="n">image_surface</span><span class="p">);</span>

    <span class="c">//</span> <span class="c">Move</span> <span class="c">to</span> <span class="c">the</span> <span class="c">top</span><span class="c">-</span><span class="c">left</span> <span class="c">content</span> <span class="c">area</span> <span class="c">(</span><span class="c">unscaled</span><span class="p">)</span>
    <span class="n">context</span><span class="nf">.translate</span><span class="p">(</span><span class="n">A4_DEFAULT_MARGINS</span><span class="py">.left</span><span class="p">,</span> <span class="n">A4_DEFAULT_MARGINS</span><span class="py">.top</span><span class="p">);</span>

    <span class="c">//</span> <span class="c">Apply</span> <span class="c">scale</span> <span class="n">transformation</span>
    <span class="n">context</span><span class="nf">.scale</span><span class="p">(</span><span class="n">scale_factor</span><span class="p">,</span> <span class="n">scale_factor</span><span class="p">);</span> 

    <span class="c">//</span> <span class="c">Draw</span> <span class="c">the</span> <span class="c">Image</span> <span class="c">onto</span> <span class="c">the</span> <span class="c">PDF</span> <span class="c">Surface</span><span class="c">:</span>
    <span class="c">//</span> <span class="c">Set</span> <span class="c">the</span> <span class="c">image</span> <span class="c">surface</span> <span class="c">as</span> <span class="c">the</span> <span class="c">source</span> <span class="c">pattern</span> <span class="c">for</span> <span class="c">drawing</span>
    <span class="c">//</span> <span class="c">Draw</span> <span class="c">the</span> <span class="c">image</span> <span class="c">at</span> <span class="c">(</span><span class="c">0</span><span class="c">,</span> <span class="c">0</span><span class="c">)</span> <span class="c">in</span> <span class="c">scaled</span> <span class="c">coordinates</span><span class="py">.
    context</span><span class="nf">.set_source_surface</span><span class="p">(</span><span class="o">&amp;</span><span class="n">image_surface</span><span class="p">,</span> <span class="mf">0.0</span><span class="p">,</span> <span class="mf">0.0</span><span class="p">)</span><span class="o">?</span><span class="p">;</span>
</pre></td></tr></tbody></table></code></pre></figure>

The call to <code>context.translate()</code> must come before 
<code>context.scale()</code> — that is simply how <code>Cairo</code>’s transformation 
stack works.  As a reminder from a  
<a href="https://behainguyen.wordpress.com/2025/12/27/rust-pdfs-exploring-layout-with-pango-and-cairo/#cairo-units-and-coordinates" 
title="Rust: PDFs — Exploring Layout with Pango and Cairo" target="_blank">previous article</a>,  
<code>Cairo</code>’s effective coordinate system (when used with <code>PangoCairo</code>) is 
<code>top‑left</code>.

● The method <code>context.translate(tx, ty)</code> does the following:

<ul>
<li style="margin-top:10px;">
It treats the point <code>(tx, ty)</code> as if it were <code>(0, 0)</code>.  
The <em>origin</em> moves to <code>(tx, ty)</code>.
</li>

<li style="margin-top:10px;">
It does <strong>not</strong> move the drawing — it moves <strong>the coordinate system</strong>.
</li>

<li style="margin-top:10px;">
All subsequent drawing commands are interpreted <strong>relative to the new origin</strong>.
</li>

<li style="margin-top:10px;">
The underlying surface (PDF or image) does not change its coordinate system.
</li>

<li style="margin-top:10px;">
Only the user’s <em>view</em> of the coordinate system changes.
</li>
</ul>

● The call <code>context.scale(sx, sy)</code> scales the <strong>coordinate system</strong>.

● <code>context.set_source_surface(&image_surface, 0.0, 0.0)</code> draws the image  
at <code>(0, 0)</code> in the scaled coordinate space.

The generated PDF is shown in the screenshot below:

![160-02.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/03/160-02.png)

<a id="main-03-module"></a>
<strong>⓷ The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro/src/main_03.rs" 
title="The pdf_07_image_intro/src/main_03.rs module" target="_blank">
<code>pdf_07_image_intro/src/main_03.rs</code></a> Module
</strong>

Similar to <a href="#main-02-module"><code>main_02.rs</code></a>, this module experiments 
with avoiding <code>context.translate(tx, ty)</code> and instead using an 
<code>original_factor</code> of <code>1.0 / scale_factor</code> as compensation.  
The result is the same, but this is not an appropriate approach. 🙏 Please also read the 
inline documentation.

<a id="image-layout-module"></a>
<strong>⓸ The Shared Auxiliary Module 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro/src/image_layout.rs" 
title="The pdf_07_image_intro/src/image_layout.rs module" target="_blank">
<code>pdf_07_image_intro/src/image_layout.rs</code></a>
</strong>

The image‑rendering code from <a href="#main-02-module"><code>main_02.rs</code></a> 
has been refactored into this module. The public 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro/src/image_layout.rs#L39-L111" 
title="The pdf_07_image_intro/src/image_layout.rs module | render_image_block() function" target="_blank">
<code>render_image_block()</code></a> function is now responsible for rendering 
images. 🦀 Please note the new parameters <code>reduction_factor: f64</code> and 
<code>centre_aligned: bool</code> — these can be considered new features that were not 
part of the original implementation. This function is fully documented; please refer to 
its documentation.

<a id="main-04-module"></a>
<strong>⓹ The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro/src/main_04.rs" 
title="The pdf_07_image_intro/src/main_04.rs module" target="_blank">
<code>pdf_07_image_intro/src/main_04.rs</code></a> Module
</strong>

This module demonstrates placing text immediately below an image using the <code>y</code> 
coordinate returned from the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro/src/image_layout.rs#L39-L111" 
title="The pdf_07_image_intro/src/image_layout.rs module | render_image_block() function" target="_blank">
<code>render_image_block()</code></a> function. In the module documentation, I note 
that <em>I ACCIDENTALLY get a visually nice vertical gap between the image bottom and the 
first line of text.</em>

💡 During the study process, I encountered several issues with placing text below an image.  
I eventually resolved them, and the following sections explore the different solutions.  
I refactored <code>render_image_block()</code> near the end of this process, and it turns 
out that its returned value can be used directly as the <code>y</code> coordinate for the 
first line of text.

The function <code>render_image_block()</code> is now responsible for rendering images:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">49
50
51
52
</pre></td><td class="code"><pre>    <span class="c">//</span> <span class="c">Define</span> <span class="c">the</span> <span class="c">input</span> <span class="c">PNG</span> <span class="c">image</span> <span class="c">file</span> <span class="c">name</span> <span class="c">(</span><span class="c">ensure</span> <span class="c">this</span> <span class="c">file</span> <span class="c">exists</span><span class="c">)</span><span class="py">.
    let</span> <span class="n">png_file_name</span> <span class="o">=</span> <span class="s">"./img/139015.png"</span><span class="p">;</span>
    <span class="k">let</span> <span class="n">image_bottom</span> <span class="o">=</span> <span class="nf">render_image_block</span><span class="p">(</span><span class="n">png_file_name</span><span class="p">,</span> 
        <span class="mf">1.0</span><span class="p">,</span> <span class="k">false</span><span class="p">,</span> <span class="n">A4_DEFAULT_MARGINS</span><span class="py">.top</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">context</span><span class="p">)</span><span class="o">?</span><span class="p">;</span>
</pre></td></tr></tbody></table></code></pre></figure>

The helper function <code>layout_ink_metrics()</code> is not new — we have used this code 
in previous articles to obtain layout line heights. The rest of the code is also familiar 
and should be self‑explanatory.

🦀 <em>I plan to use this approach later on to render an image and its caption as a 
single unit.</em>

The generated PDF is shown in the screenshot below:

![160-03.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/03/160-03.png)

<a id="main-05-module"></a>
<strong>⓺ The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro/src/main_05.rs" 
title="The pdf_07_image_intro/src/main_05.rs module" target="_blank">
<code>pdf_07_image_intro/src/main_05.rs</code></a> Module
</strong>

This is a retrospective module, written based on 
<a href="#main-04-module"><code>main_04.rs</code></a> above.  
I aim to demonstrate how I lost the vertical space:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">62
63
64
65
66
</pre></td><td class="code"><pre>    <span class="c">//</span> <span class="c">Text</span> <span class="c">ink</span> <span class="c">metrics</span><span class="nf">.
    let</span> <span class="p">(</span><span class="n">y_bearing</span><span class="p">,</span> <span class="n">height</span><span class="p">)</span> <span class="o">=</span> <span class="nf">layout_ink_metrics</span><span class="p">(</span><span class="o">&amp;</span><span class="n">layout</span><span class="p">);</span>

    <span class="c">//</span> <span class="c">Text</span> <span class="c">appears</span> <span class="c">below</span> <span class="c">the</span> <span class="c">image</span><span class="py">.
    let</span> <span class="n">baseline_y</span> <span class="o">=</span> <span class="n">image_bottom</span> <span class="o">-</span> <span class="n">y_bearing</span><span class="p">;</span>
</pre></td></tr></tbody></table></code></pre></figure>

Please note <code>image_bottom - y_bearing</code> — this is the cause of the problem.

<a id="main-06-module"></a>
<strong>⓻ The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro/src/main_06.rs" 
title="The pdf_07_image_intro/src/main_06.rs module" target="_blank">
<code>pdf_07_image_intro/src/main_06.rs</code></a> Module
</strong>

This module demonstrates one of the solutions I was given to address the problem shown in 
<a href="#main-05-module"><code>main_05.rs</code></a>. The main focus of this module is:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">60
61
62
63
64
65
66
67
68
</pre></td><td class="code"><pre>    <span class="c">//</span> <span class="c">Setting</span> <span class="c">a</span> <span class="c">natural</span> <span class="c">vertical</span> <span class="c">space</span> <span class="c">between</span> <span class="c">the</span> <span class="c">image</span> <span class="c">and</span> <span class="c">the</span> <span class="c">text</span> <span class="c">line</span><span class="py">.
    let</span> <span class="n">metrics</span> <span class="o">=</span> <span class="n">context</span><span class="nf">.font_extents</span><span class="p">()</span><span class="o">?</span><span class="p">;</span>
    <span class="k">let</span> <span class="n">ascent</span> <span class="o">=</span> <span class="n">metrics</span><span class="nf">.ascent</span><span class="p">()</span> <span class="k">as</span> <span class="nb">f64</span> <span class="o">/</span> <span class="nn">pango</span><span class="p">::</span><span class="n">SCALE</span> <span class="k">as</span> <span class="nb">f64</span><span class="p">;</span>
    <span class="c">//</span> <span class="c">let</span> <span class="c">descent</span> <span class="c">=</span> <span class="c">metrics</span><span class="c">.descent</span><span class="c">()</span> <span class="c">as</span> <span class="c">f64</span> <span class="c">/</span> <span class="c">pango</span><span class="c">::</span><span class="c">SCALE</span> <span class="c">as</span> <span class="c">f64</span><span class="p">;</span>

    <span class="k">let</span> <span class="n">y_bearing_equiv</span> <span class="o">=</span> <span class="o">-</span><span class="n">ascent</span><span class="p">;</span>

    <span class="c">//</span> <span class="c">Text</span> <span class="c">appears</span> <span class="c">below</span> <span class="c">the</span> <span class="c">image</span><span class="py">.
    let</span> <span class="n">baseline_y</span> <span class="o">=</span> <span class="n">image_bottom</span> <span class="o">-</span> <span class="n">y_bearing_equiv</span><span class="p">;</span>
</pre></td></tr></tbody></table></code></pre></figure>

The final result is essentially identical to 
<a href="#main-04-module"><code>main_04.rs</code></a>.

<a id="main-07-module"></a>
<strong>⓼ The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro/src/main_07.rs" 
title="The pdf_07_image_intro/src/main_07.rs module" target="_blank">
<code>pdf_07_image_intro/src/main_07.rs</code></a> Module
</strong>

This module demonstrates another solution I was given to address the problem shown in 
<a href="#main-05-module"><code>main_05.rs</code></a>. The main focus of this module is:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">60
61
62
63
64
65
66
67
68
</pre></td><td class="code"><pre>    <span class="c">//</span> <span class="c">Setting</span> <span class="c">a</span> <span class="c">natural</span> <span class="c">vertical</span> <span class="c">space</span> <span class="c">between</span> <span class="c">the</span> <span class="c">image</span> <span class="c">and</span> <span class="c">the</span> <span class="c">text</span> <span class="c">line</span><span class="p">,</span> <span class="c">using</span> <span class="c">`</span><span class="c">Pango</span><span class="c">`</span><span class="py">.
    let</span> <span class="n">ctx</span> <span class="o">=</span> <span class="n">layout</span><span class="nf">.context</span><span class="p">();</span>
    <span class="k">let</span> <span class="n">metrics</span> <span class="o">=</span> <span class="n">ctx</span><span class="nf">.metrics</span><span class="p">(</span><span class="nf">Some</span><span class="p">(</span><span class="o">&amp;</span><span class="n">desc</span><span class="p">),</span> <span class="nb">None</span><span class="p">);</span>

    <span class="k">let</span> <span class="n">ascent</span> <span class="o">=</span> <span class="n">metrics</span><span class="nf">.ascent</span><span class="p">()</span> <span class="k">as</span> <span class="nb">f64</span> <span class="o">/</span> <span class="nn">pango</span><span class="p">::</span><span class="n">SCALE</span> <span class="k">as</span> <span class="nb">f64</span><span class="p">;</span>
    <span class="c">//</span> <span class="c">let</span> <span class="c">descent</span> <span class="c">=</span> <span class="c">metrics</span><span class="c">.descent</span><span class="c">()</span> <span class="c">as</span> <span class="c">f64</span> <span class="c">/</span> <span class="c">pango</span><span class="c">::</span><span class="c">SCALE</span> <span class="c">as</span> <span class="c">f64</span><span class="p">;</span>

    <span class="c">//</span> <span class="c">Text</span> <span class="c">appears</span> <span class="c">below</span> <span class="c">the</span> <span class="c">image</span><span class="py">.
    let</span> <span class="n">baseline_y</span> <span class="o">=</span> <span class="n">image_bottom</span> <span class="o">+</span> <span class="n">ascent</span><span class="p">;</span>
</pre></td></tr></tbody></table></code></pre></figure>

The final result is essentially identical to 
<a href="#main-04-module"><code>main_04.rs</code></a>.

<a id="main-module"></a>
<strong>⓽ The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro/src/main.rs" 
title="The pdf_07_image_intro/src/main.rs module" target="_blank">
<code>pdf_07_image_intro/src/main.rs</code></a> Module
</strong>

In this final demo, we exercise the two new parameters 
<code>reduction_factor: f64</code> and <code>centre_aligned: bool</code> 
of the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro/src/image_layout.rs#L39-L111" 
title="The pdf_07_image_intro/src/image_layout.rs module | render_image_block() function" target="_blank">
<code>render_image_block()</code></a> function.

For both images, we apply a <code>reduction_factor</code> of <code>0.75</code>, 
small enough to fit everything onto a single page. For the first image, 
<code>centre_aligned</code> is <code>true</code>, centring the image within 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro/src/page_geometry.rs#L30-L32" 
title="The pdf_07_image_intro/src/page_geometry.rs module | a4_default_content_width() function" target="_blank">
<code>a4_default_content_width()</code></a>.  
For the second image, <code>centre_aligned</code> is <code>false</code>, so it defaults 
to left‑justified.

For each text <code>y</code> coordinate, we simply use the returned value from 
<code>render_image_block()</code>, as demonstrated in the 
<a href="#main-04-module"><code>main_04.rs</code></a> module discussed above.

The generated PDF is shown in the screenshot below:

![160-04.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/03/160-04.png)

We could certainly make the layout much nicer… but that is a task for another day.

<a id="concluding-remarks"></a>
❺ <strong>What’s Next</strong>

I do apologise that this article is a bit long — I did not intend for it to grow this much. 
The next main objective remains the same: enabling the <code>Markdown</code> parser we 
<a href="https://behainguyen.wordpress.com/2026/02/23/rust-pdfs-pango-and-cairo-layout-supporting-bold-italic-and-bold-italic-text/#concluding-remarks" 
title="Rust: PDFs — Pango and Cairo Layout — Supporting Bold, Italic, and Bold Italic Text" 
target="_blank">last discussed</a> to support images with captions, where images are 
specified using relative paths, similar to how it is done in 
<a href="https://www.latex-project.org/" title="The LaTeX Project" target="_blank">LaTeX</a>. 
But we are not quite there yet. In the next iteration, we will extend the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_07_image_intro/src/image_layout.rs#L39-L111" 
title="The pdf_07_image_intro/src/image_layout.rs module | render_image_block() function" target="_blank">
<code>render_image_block()</code></a> function to support rendering an image and its 
caption as a single image block, and give the extended version some essential intelligence, 
such as ensuring the image block can be rendered properly within the available effective 
height.

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