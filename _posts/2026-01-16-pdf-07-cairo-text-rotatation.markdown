---
layout: post
title: "Rust: PDFs — Text Rotation with Cairo and Pango"

description: My fascination with Pango and CairoGraphics has led me to explore text rotation. I find it very interesting. It becomes straightforward once we understand a few key ideas. In this article, we focus on ±90° rotation for left‑to‑right text only. 

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
---

*My fascination with <a href="https://www.gtk.org/docs/architecture/pango" title="Pango Library" target="_blank"><code>Pango</code></a> and <a href="https://www.cairographics.org/" title="CairoGraphics" target="_blank"><code>CairoGraphics</code></a> has led me to explore text rotation. I find it very interesting. It becomes straightforward once we understand a few key ideas. In this article, we focus on ±90° rotation for left‑to‑right text only.*

<h3>
🦀 <a href="https://github.com/behai-nguyen/polyglot_pdf" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![157-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/01/157-feature-image.png) |
|:--:|
| *Rust: PDFs — Text Rotation with Cairo and Pango* |

<a id="repository-cloning"></a>
🚀 The code for this post is in the following GitHub repository: 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_04_text_rotation" 
title="Rust multilingual PDFs" target="_blank">pdf_04_text_rotation</a>.

<a id="cairo-coordinates-recap"></a>
❶ <strong><code>Cairo</code> Coordinates Recap</strong>

Recall from our previous discussion, 
<a href="https://behainguyen.wordpress.com/2025/12/27/rust-pdfs-exploring-layout-with-pango-and-cairo/#cairo-units-and-coordinates" 
title="Rust: PDFs — Exploring Layout with Pango and Cairo" 
target="_blank"><code>Cairo</code> Units and Coordinates</a> — that 
<code>Cairo</code>’s effective coordinate system (when used with <code>PangoCairo</code>) 
is <code>top‑left</code>. We can visualise it as illustrated below:

<p><img src="https://behainguyen.wordpress.com/wp-content/uploads/2026/01/157-01-cairo-coordinates.png" alt="157-01-cairo-coordinates.png" width="327" height="194"></p>

For Latin‑based writing systems, as well as scripts such as Khmer, Lao, and Thai, 
text flows horizontally from <code>0</code> toward <code>X+</code>, and vertically 
from <code>0</code> toward <code>Y+</code>.

<a id="cairo-text-rotation"></a>
❷ <strong><a href="https://www.cairographics.org/" title="CairoGraphics" 
target="_blank"><code>Cairo</code></a> Text Rotation</strong>

We perform text rotation through <code>Cairo</code>. We rotate the 
<a href="https://gtk-rs.org/gtk-rs-core/stable/latest/docs/cairo/struct.Context.html" 
title="Struct Context" target="_blank"><code>cairo::Context</code></a>, then draw the 
text using 
<a href="https://gtk-rs.org/gtk-rs-core/stable/latest/docs/pangocairo/functions/fn.show_layout.html" 
title="pangocairo::functions::show_layout" target="_blank">
<code>pangocairo::functions::show_layout()</code></a> — the same function we used in the 
<a href="https://behainguyen.wordpress.com/2025/12/27/rust-pdfs-exploring-layout-with-pango-and-cairo/" 
title="Rust: PDFs — Exploring Layout with Pango and Cairo" target="_blank">previous article</a>.

The official 
<a href="https://gtk-rs.org/gtk-rs-core/stable/latest/docs/cairo/struct.Context.html" 
title="Struct Context" target="_blank"><code>cairo::Context</code></a> method 
<a href="https://gtk-rs.org/gtk-rs-core/stable/latest/docs/cairo/struct.Context.html#method.rotate" 
title="pub fn rotate(&self, angle: f64)" target="_blank">pub fn rotate(&self, angle: f64)</a> 
has no documentation. In the underlying <code>Cairo</code> C library, the corresponding 
<a href="https://www.cairographics.org/manual/cairo-Transformations.html#cairo-rotate" 
title="cairo_rotate()" target="_blank"><code>cairo_rotate()</code></a> function belongs to 
the <a href="https://www.cairographics.org/manual/cairo-Transformations.html" 
title="Transformations" target="_blank">Transformations</a> category, described as 
<em>“Transformations — Manipulating the current transformation matrix”</em>.

I am reproducing the official <code>cairo_rotate()</code> documentation below:

<a id="cairo-rotate-doc"></a>
<div style="border:1px solid black; padding:1em;">
<a href="https://www.cairographics.org/manual/cairo-Transformations.html#cairo-rotate" 
title="cairo_rotate()" target="_blank"><code>cairo_rotate()</code></a>

<figure class="highlight"><pre><code class="language-c" data-lang="c"><span class="kt">void</span>
<span class="nf">cairo_rotate</span> <span class="p">(</span><span class="n">cairo_t</span> <span class="o">*</span><span class="n">cr</span><span class="p">,</span>
              <span class="kt">double</span> <span class="n">angle</span><span class="p">);</span></code></pre></figure>

Modifies the current transformation matrix (CTM) by rotating the user-space axes by angle radians. The rotation of the axes takes places after any existing transformation of user space. The rotation direction for positive angles is from the positive X axis toward the positive Y axis.

<p><strong>Parameters</strong></p>

<span style="padding-left:1em;"><code>cr</code>: a cairo context</span>

<span style="padding-left:1em;"><code>angle</code>: angle (in radians) by which the user-space axes will be rotated</span>

Since: <a href="https://www.cairographics.org/manual/api-index-1-0.html#api-index-1.0" 
title="Index of new symbols in 1.0" target="_blank">1.0</a>
</div><br>

💡 Please note: the <code>angle</code> parameter to <code>cairo_rotate()</code> is in 
<a href="https://en.wikipedia.org/wiki/Radian" title="Wikipedia Radian" target="_blank">radians</a>.  
Briefly, <code>360° = 2π radians</code> and <code>180° = π radians</code>.  
To convert degrees to radians, <code>multiply degrees by π/180</code>.  
To convert radians to degrees, <code>multiply radians by 180/π</code>. For example:

<ul>
<li style="margin-top:10px;">90° → radians: 90 × (π / 180) = 1.57 radians</li>
<li style="margin-top:10px;">1.57 radians → degrees: 1.57 × (180 / π) = 90°</li>
</ul>

I did high school in Vietnam back in the 1980s… 
<a href="https://en.wikipedia.org/wiki/Radian" title="Wikipedia Radian" target="_blank">radians</a> 
felt foreign 😂 and suggested nothing. I have since confirmed that they are taught — and 
called <em>radian</em> — but I remember none of it. Degrees make far more sense to me, 
both visually and intuitively.

🦀 In Rust, converting 90° to radians is simple:  
<code>90.0_f64.to_radians()</code> or <code>90.0_f32.to_radians()</code>.  
Next, we will look at some Rust code that performs text rotation.

<a id="repository-layout"></a>
❸ <strong>Repository Layout</strong>

💡 Please note: on both Windows and Ubuntu, I’m running Rust version 
<code>rustc 1.90.0 (1159e78c4 2025-09-14)</code>.

This is once again a one‑off project—I don’t plan to update it in future development. 
I want to keep a log of progress exactly as it occurred. Future code may copy this and 
make changes to it. I’ve placed the project under the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_04_text_rotation" 
title="Rust multilingual PDFs" target="_blank">pdf_04_text_rotation</a> directory. 
The structure is:

```
.
├── Cargo.toml
├── set_env.bat
└── src
    ├── main_01.rs
    ├── main_02.rs
    ├── main_03.rs
    ├── main_04.rs
    ├── main_05.rs
    ├── main.rs
    └── page_geometry.rs
```

<a id="repository-layout-desc"></a>
All <code>main*.rs</code> modules under <code>src/</code> are self‑contained 
Rust programs written in the listed order to help me understand text rotation.  
We discuss these modules in the listed order.

The <code>src/page_geometry.rs</code> module is copied unchanged from the 
<a href="https://behainguyen.wordpress.com/2025/12/27/rust-pdfs-exploring-layout-with-pango-and-cairo/#repository-layout-desc" 
title="Rust: PDFs — Exploring Layout with Pango and Cairo" 
target="_blank">last article</a>.  
👉 Changing any margin value in the <code>A4_DEFAULT_MARGINS</code> constant will 
change the layout of the text in the PDF.

<a id="path-env-var"></a>
💡 The code requires the <code>Pango</code>, <code>HarfBuzz</code>, <code>Cairo</code>, 
etc. libraries. 🐧 On Ubuntu, all required libraries are globally recognised. 🪟 On Windows, 
I haven’t added the paths for the libraries’ DLLs to the <code>PATH</code> environment 
variable. In each new Windows terminal session, I run the following once:

```
set PATH=C:\PF\harfbuzz\dist\bin\;%PATH%
set PATH=C:\PF\vcpkg\installed\x64-windows\bin\;%PATH%
set PATH=C:\PF\pango\dist\bin;C:\PF\cairo-1.18.4\dist\bin;C:\PF\fribidi\dist\bin;%PATH%
```

Alternatively, you can simply run 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_02/set_env.bat" 
title="pdf_02/set_env.bat file" target="_blank"><code>set_env.bat</code></a>.  
After that, <code>cargo run</code> works as expected.

<a id="rust-study-code"></a>
❹ <strong>Text Rotation Study Code</strong>

In this section, we look at several small study programs. Our focus is on ±90° text rotation.

<a id="90-degrees-rotation"></a>
⓵ <strong>90° Rotation</strong>

<a id="90-degrees-rotation-1"></a>
We start with the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_04_text_rotation/src/main_01.rs" 
title="The pdf_04_text_rotation/src/main_01.rs module" target="_blank">
<code>pdf_04_text_rotation/src/main_01.rs</code></a> module — most of the 
code should already be familiar. The only new line is line 45:  
<code>context.rotate(90.0_f64.to_radians());</code>

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">36
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
50
</pre></td><td class="code"><pre>    <span class="n">layout</span><span class="nf">.set_text</span><span class="p">(</span><span class="s">"Kỷ độ Long Tuyền đới nguyệt ma"</span><span class="p">);</span>

    <span class="c">//</span> <span class="c">Save</span> <span class="c">the</span> <span class="c">current</span> <span class="c">state</span>
    <span class="n">context</span><span class="nf">.save</span><span class="p">()</span><span class="o">?</span><span class="p">;</span>

    <span class="n">context</span><span class="nf">.move_to</span><span class="p">(</span><span class="n">A4_DEFAULT_MARGINS</span><span class="py">.left</span><span class="p">,</span> <span class="n">A4_DEFAULT_MARGINS</span><span class="py">.top</span><span class="p">);</span>

    <span class="c">//</span> <span class="c">Both</span> <span class="c">produce</span> <span class="c">the</span> <span class="c">same</span> <span class="c">result</span><span class="c">.</span>
    <span class="c">//</span> <span class="c">context</span><span class="c">.rotate</span><span class="c">(</span><span class="c">90.0</span> <span class="c">*</span> <span class="c">PI</span> <span class="c">/</span> <span class="c">180.0</span><span class="c">);</span>
    <span class="n">context</span><span class="nf">.rotate</span><span class="p">(</span><span class="mf">90.0_f64</span><span class="nf">.to_radians</span><span class="p">());</span>

    <span class="nf">show_layout</span><span class="p">(</span><span class="o">&amp;</span><span class="n">context</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">layout</span><span class="p">);</span>

    <span class="o">//</span> <span class="c">Restore</span> <span class="c">the</span> <span class="c">context</span> <span class="c">to</span> <span class="c">the</span> <span class="c">original</span> <span class="c">matrix</span> <span class="c">state</span> <span class="c">for</span> <span class="c">subsequent</span> <span class="c">drawing</span> <span class="c">operations</span>
    <span class="n">context</span><span class="nf">.restore</span><span class="p">()</span><span class="o">?</span><span class="p">;</span>
</pre></td></tr></tbody></table></code></pre></figure>

When I first began studying text rotation, I assumed that before calling 
<a href="https://www.cairographics.org/manual/cairo-Transformations.html#cairo-rotate" 
title="cairo_rotate()" target="_blank"><code>cairo_rotate()</code></a>, we would need to 
call <a href="https://www.cairographics.org/manual/cairo-Transformations.html#cairo-translate" 
title="cairo_translate()" target="_blank"><code>cairo_translate()</code></a>.  
However, <a href="https://www.cairographics.org/manual/cairo-Paths.html#cairo-move-to" 
title="cairo_move_to()" target="_blank"><code>cairo_move_to()</code></a> is sufficient.

The output it produces is shown below:

![157-02-rotate-plus-90-degrees.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/01/157-02-rotate-plus-90-degrees.png)

In this output, both <code>A4_DEFAULT_MARGINS.top</code> and 
<code>A4_DEFAULT_MARGINS.left</code> are set to <code>57.0</code> PostScript points.  
However, visually, the left margin appears smaller than the top margin.  
According to the <a href="#cairo-rotate-doc">documentation</a>:

> The rotation direction for positive angles is from the positive X axis toward the positive Y axis.

This means that after rotation, <code>X+</code> now points <strong>down</strong>, and 
<code>Y+</code> now points <strong>left</strong>.  
It follows that the rotated user‑space <code>X</code> origin effectively becomes  
<code>A4_DEFAULT_MARGINS.left</code> − <code>line height</code>.  
If we compensate the <code>X</code> origin by one <code>line height</code> (in PostScript 
points), the visual origin aligns correctly with the intended 
<code>A4_DEFAULT_MARGINS.left</code>.

<a id="90-degrees-rotation-2"></a>
We implement the above compensation in 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_04_text_rotation/src/main_02.rs" 
title="The pdf_04_text_rotation/src/main_02.rs module" target="_blank">
<code>pdf_04_text_rotation/src/main_02.rs</code></a>. We added lines 
<code>38–39</code> and updated line <code>44</code>:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">36
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
50
51
52
53
</pre></td><td class="code"><pre>    <span class="n">layout</span><span class="nf">.set_text</span><span class="p">(</span><span class="s">"Kỷ độ Long Tuyền đới nguyệt ma"</span><span class="p">);</span>

    <span class="k">let</span> <span class="p">(</span><span class="mi">_</span><span class="p">,</span> <span class="n">logical</span><span class="p">)</span> <span class="o">=</span> <span class="n">layout</span><span class="nf">.extents</span><span class="p">();</span>
    <span class="k">let</span> <span class="n">line_height</span> <span class="o">=</span> <span class="n">logical</span><span class="nf">.height</span><span class="p">()</span> <span class="k">as</span> <span class="nb">f64</span> <span class="o">/</span> <span class="nn">pango</span><span class="p">::</span><span class="n">SCALE</span> <span class="k">as</span> <span class="nb">f64</span><span class="p">;</span>

    <span class="c">//</span> <span class="c">Save</span> <span class="c">the</span> <span class="c">current</span> <span class="c">state</span>
    <span class="n">context</span><span class="nf">.save</span><span class="p">()</span><span class="o">?</span><span class="p">;</span>

    <span class="n">context</span><span class="nf">.move_to</span><span class="p">(</span><span class="n">A4_DEFAULT_MARGINS</span><span class="py">.left</span> <span class="o">+</span> <span class="n">line_height</span><span class="p">,</span> <span class="n">A4_DEFAULT_MARGINS</span><span class="py">.top</span><span class="p">);</span>

    <span class="c">//</span> <span class="c">Both</span> <span class="c">produce</span> <span class="c">the</span> <span class="c">same</span> <span class="c">result</span><span class="c">.</span>
    <span class="c">//</span> <span class="c">context</span><span class="c">.rotate</span><span class="c">(</span><span class="c">90.0</span> <span class="c">*</span> <span class="c">PI</span> <span class="c">/</span> <span class="c">180.0</span><span class="c">);</span>
    <span class="n">context</span><span class="nf">.rotate</span><span class="p">(</span><span class="mf">90.0_f64</span><span class="nf">.to_radians</span><span class="p">());</span>

    <span class="nf">show_layout</span><span class="p">(</span><span class="o">&amp;</span><span class="n">context</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">layout</span><span class="p">);</span>

    <span class="c">//</span> <span class="c">Restore</span> <span class="c">the</span> <span class="c">context</span> <span class="c">to</span> <span class="c">the</span> <span class="c">original</span> <span class="c">matrix</span> <span class="c">state</span> <span class="c">for</span> <span class="c">subsequent</span> <span class="c">drawing</span> <span class="c">operations</span>
    <span class="n">context</span><span class="nf">.restore</span><span class="p">()</span><span class="o">?</span><span class="p">;</span>
</pre></td></tr></tbody></table></code></pre></figure>

The new code is not conceptually new—we have used these calls in previous articles. 
The user‑space axes are rotated, but the text itself is not; it retains the same metrics 
it would have in the default user‑space orientation. The output is now:

![157-03-rotate-plus-90-degrees.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/01/157-03-rotate-plus-90-degrees.png)

<a id="90-degrees-rotation-3"></a>
Both margin look visually identical. But let's verify that by printing the same line 
of text just below the rotated text, at the same <code>X</code> coordinate. 

In the <a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_04_text_rotation/src/main_03.rs" 
title="The pdf_04_text_rotation/src/main_03.rs module" target="_blank">
<code>pdf_04_text_rotation/src/main_03.rs</code></a> module:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">36
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
50
51
52
53
54
55
56
57
</pre></td><td class="code"><pre>    <span class="n">layout</span><span class="nf">.set_text</span><span class="p">(</span><span class="s">"Kỷ độ Long Tuyền đới nguyệt ma"</span><span class="p">);</span>

    <span class="k">let</span> <span class="p">(</span><span class="mi">_</span><span class="p">,</span> <span class="n">logical</span><span class="p">)</span> <span class="o">=</span> <span class="n">layout</span><span class="nf">.extents</span><span class="p">();</span>
    <span class="k">let</span> <span class="n">line_height</span> <span class="o">=</span> <span class="n">logical</span><span class="nf">.height</span><span class="p">()</span> <span class="k">as</span> <span class="nb">f64</span> <span class="o">/</span> <span class="nn">pango</span><span class="p">::</span><span class="n">SCALE</span> <span class="k">as</span> <span class="nb">f64</span><span class="p">;</span>
    <span class="k">let</span> <span class="n">line_width</span> <span class="o">=</span> <span class="n">logical</span><span class="nf">.width</span><span class="p">()</span> <span class="k">as</span> <span class="nb">f64</span> <span class="o">/</span> <span class="nn">pango</span><span class="p">::</span><span class="n">SCALE</span> <span class="k">as</span> <span class="nb">f64</span><span class="p">;</span>

    <span class="c">//</span> <span class="c">Save</span> <span class="c">the</span> <span class="c">current</span> <span class="c">state</span>
    <span class="n">context</span><span class="nf">.save</span><span class="p">()</span><span class="o">?</span><span class="p">;</span>

    <span class="n">context</span><span class="nf">.move_to</span><span class="p">(</span><span class="n">A4_DEFAULT_MARGINS</span><span class="py">.left</span> <span class="o">+</span> <span class="n">line_height</span><span class="p">,</span> <span class="n">A4_DEFAULT_MARGINS</span><span class="py">.top</span><span class="p">);</span>

    <span class="c">//</span> <span class="c">Both</span> <span class="c">produce</span> <span class="c">the</span> <span class="c">same</span> <span class="c">result</span><span class="c">.</span>
    <span class="c">//</span> <span class="c">context</span><span class="c">.rotate</span><span class="c">(</span><span class="c">90.0</span> <span class="c">*</span> <span class="c">PI</span> <span class="c">/</span> <span class="c">180.0</span><span class="c">);</span>
    <span class="n">context</span><span class="nf">.rotate</span><span class="p">(</span><span class="mf">90.0_f64</span><span class="nf">.to_radians</span><span class="p">());</span>

    <span class="nf">show_layout</span><span class="p">(</span><span class="o">&amp;</span><span class="n">context</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">layout</span><span class="p">);</span>

    <span class="c">//</span> <span class="c">Restore</span> <span class="c">the</span> <span class="c">context</span> <span class="c">to</span> <span class="c">the</span> <span class="c">original</span> <span class="c">matrix</span> <span class="c">state</span> <span class="c">for</span> <span class="c">subsequent</span> <span class="c">drawing</span> <span class="c">operations</span>
    <span class="n">context</span><span class="nf">.restore</span><span class="p">()</span><span class="o">?</span><span class="p">;</span>

    <span class="n">context</span><span class="nf">.move_to</span><span class="p">(</span><span class="n">A4_DEFAULT_MARGINS</span><span class="py">.left</span><span class="p">,</span> <span class="n">A4_DEFAULT_MARGINS</span><span class="py">.top</span> <span class="o">+</span> <span class="n">line_width</span><span class="p">);</span>
    <span class="nf">show_layout</span><span class="p">(</span><span class="o">&amp;</span><span class="n">context</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">layout</span><span class="p">);</span>
</pre></td></tr></tbody></table></code></pre></figure>

We added line <code>40</code> — and after restore the original user-space in line 54 
<code>context.restore()?;</code> — we added lines <code>56-57</code>: 
<code>A4_DEFAULT_MARGINS.top + line_width</code> gives the <code>Y</code> coordinate 
<em>just below the rotated text</em>. The text is rotated vertically, <code>line_width</code> 
can be treated as logical height since the rotated text actually occupies 
<code>line_width</code> PostScript points veritically. The output looks like: 

![157-04-rotate-plus-90-degrees.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/01/157-04-rotate-plus-90-degrees.png)

The compensation we <a href="#90-degrees-rotation-2">have implemented</a> appears 
to be correct.

<a id="minus-90-degrees-rotation"></a>
⓶ <strong>-90° Rotation</strong>

The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_04_text_rotation/src/main_04.rs" 
title="The pdf_04_text_rotation/src/main_04.rs module" target="_blank">
<code>pdf_04_text_rotation/src/main_04.rs</code></a> module implements 
-90° rotation. It is a copy of 
<a href="#90-degrees-rotation-1"><code>pdf_04_text_rotation/src/main_01.rs</code></a> 
with only a single modification — the angle is negative, updating line 45 to:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">43
44
45
</pre></td><td class="code"><pre>    <span class="c">//</span> <span class="c">Both</span> <span class="c">produce</span> <span class="c">the</span> <span class="c">same</span> <span class="c">result</span><span class="c">.</span>
    <span class="c">//</span> <span class="c">context</span><span class="c">.rotate</span><span class="c">(</span><span class="c">-</span><span class="c">90.0</span> <span class="c">*</span> <span class="c">PI</span> <span class="c">/</span> <span class="c">180.0</span><span class="c">);</span>
    <span class="n">context</span><span class="nf">.rotate</span><span class="p">(</span><span class="o">-</span><span class="mf">90.0_f64</span><span class="nf">.to_radians</span><span class="p">());</span>
</pre></td></tr></tbody></table></code></pre></figure>

The PDF looks like the screenshot below:

![157-05-rotate-minus-90-degrees.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/01/157-05-rotate-minus-90-degrees.png)

The <code>X</code> coordinate visually appears correct at <code>A4_DEFAULT_MARGINS.left</code>. 
However, because the user‑space axes rotate upward with a negative angle, the text is clipped.  
To position the “top” of the text at the <code>A4_DEFAULT_MARGINS.top</code> 
<code>Y</code> coordinate, we must compensate by  
<code>A4_DEFAULT_MARGINS.top + line_width</code>, similar to a 
<a href="#90-degrees-rotation-3">previous discussion</a>.

<a id="minus-90-degrees-rotation-2"></a>
The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_04_text_rotation/src/main_05.rs" 
title="The pdf_04_text_rotation/src/main_05.rs module" target="_blank">
<code>pdf_04_text_rotation/src/main_05.rs</code></a> module implements this 
compensation. We added lines <code>38–39</code> and updated line <code>44</code>:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">36
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
50
51
52
53
</pre></td><td class="code"><pre>    <span class="n">layout</span><span class="nf">.set_text</span><span class="p">(</span><span class="s">"Kỷ độ Long Tuyền đới nguyệt ma"</span><span class="p">);</span>

    <span class="k">let</span> <span class="p">(</span><span class="mi">_</span><span class="p">,</span> <span class="n">logical</span><span class="p">)</span> <span class="o">=</span> <span class="n">layout</span><span class="nf">.extents</span><span class="p">();</span>
    <span class="k">let</span> <span class="n">line_width</span> <span class="o">=</span> <span class="n">logical</span><span class="nf">.width</span><span class="p">()</span> <span class="k">as</span> <span class="nb">f64</span> <span class="o">/</span> <span class="nn">pango</span><span class="p">::</span><span class="n">SCALE</span> <span class="k">as</span> <span class="nb">f64</span><span class="p">;</span>

    <span class="c">//</span> <span class="c">Save</span> <span class="c">the</span> <span class="c">current</span> <span class="c">state</span>
    <span class="n">context</span><span class="nf">.save</span><span class="p">()</span><span class="o">?</span><span class="p">;</span>

    <span class="n">context</span><span class="nf">.move_to</span><span class="p">(</span><span class="n">A4_DEFAULT_MARGINS</span><span class="py">.left</span><span class="p">,</span> <span class="n">A4_DEFAULT_MARGINS</span><span class="py">.top</span> <span class="o">+</span> <span class="n">line_width</span><span class="p">);</span>

    <span class="c">//</span> <span class="c">Both</span> <span class="c">produce</span> <span class="c">the</span> <span class="c">same</span> <span class="c">result</span><span class="c">.</span>
    <span class="c">//</span> <span class="c">context</span><span class="c">.rotate</span><span class="c">(</span><span class="c">-</span><span class="c">90.0</span> <span class="c">*</span> <span class="c">PI</span> <span class="c">/</span> <span class="c">180.0</span><span class="c">);</span>
    <span class="n">context</span><span class="nf">.rotate</span><span class="p">(</span><span class="o">-</span><span class="mf">90.0_f64</span><span class="nf">.to_radians</span><span class="p">());</span>

    <span class="nf">show_layout</span><span class="p">(</span><span class="o">&amp;</span><span class="n">context</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">layout</span><span class="p">);</span>

    <span class="c">//</span> <span class="c">Restore</span> <span class="c">the</span> <span class="c">context</span> <span class="c">to</span> <span class="c">the</span> <span class="c">original</span> <span class="c">matrix</span> <span class="c">state</span> <span class="k">for</span> <span class="c">subsequent</span> <span class="c">drawing</span> <span class="c">operations</span>
    <span class="n">context</span><span class="nf">.restore</span><span class="p">()</span><span class="o">?</span><span class="p">;</span>
</pre></td></tr></tbody></table></code></pre></figure>

There is no new logic here. The output PDF looks like the screenshot below; visually, 
both margins now align with <code>A4_DEFAULT_MARGINS.left</code> and 
<code>A4_DEFAULT_MARGINS.top</code>:

![157-06-rotate-minus-90-degrees.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/01/157-06-rotate-minus-90-degrees.png)

<a id="variant-degrees-rotation"></a>
⓷ <strong>Angles Other Than ±90°</strong>

As a final example, we look at rotating by angles other than ±90°. The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_04_text_rotation/src/main.rs" 
title="The pdf_04_text_rotation/src/main.rs module" target="_blank">
<code>pdf_04_text_rotation/src/main.rs</code></a> module rotates the 
user‑space axes in 10° steps until reaching 360°:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">47
48
49
50
51
</pre></td><td class="code"><pre>    <span class="k">for</span> <span class="n">degree</span> <span class="nf">in</span> <span class="p">(</span><span class="mi">10</span><span class="o">..</span><span class="mi">370</span><span class="p">)</span><span class="nf">.step_by</span><span class="p">(</span><span class="mi">10</span><span class="p">)</span> <span class="p">{</span>
        <span class="n">context</span><span class="nf">.rotate</span><span class="p">((</span><span class="n">degree</span> <span class="k">as</span> <span class="nb">f64</span><span class="p">)</span><span class="nf">.to_radians</span><span class="p">());</span>
        <span class="nf">show_layout</span><span class="p">(</span><span class="o">&amp;</span><span class="n">context</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">layout</span><span class="p">);</span>
        <span class="n">context</span><span class="nf">.set_matrix</span><span class="p">(</span><span class="nn">cairo</span><span class="p">::</span><span class="nn">Matrix</span><span class="p">::</span><span class="nf">identity</span><span class="p">());</span>
    <span class="p">}</span>
</pre></td></tr></tbody></table></code></pre></figure>

Because <code>Cairo</code> transformations are cumulative, we must call 
<code>context.set_matrix()</code> to reset the transformation matrix after each draw.  
Instead of <code>context.set_matrix()</code>, we can use <code>context.save()?;</code> 
and <code>context.restore()?;</code>, as shown in the snippet below.  
Please refer to the module for full details:

```rust
        context.save()?;
        context.rotate((degree as f64).to_radians());
        show_layout(&context, &layout);
        context.restore()?;
```

Its output is shown in the screenshot below:

![157-07-rotate-variant-degrees.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/01/157-07-rotate-variant-degrees.png)

<a id="90-degrees-rotation-doc-revisited"></a>
❺ <strong>The ±90° Rotation and <code>cairo-rotate()</code>'s Documentation Revisited</strong>

The <code>cairo-rotate()</code> <a href="#cairo-rotate-doc">documentation</a> states:

> Modifies the current transformation matrix (CTM) by rotating the user-space axes by angle radians. The rotation of the axes takes places after any existing transformation of user space. The rotation direction for positive angles is from the positive X axis toward the positive Y axis.

It took me a while to fully understand the above paragraph, even though through 
trial and error I did get the ±90° rotations working. We have already seen how the 
code behaves; now let’s unpack this visually to cement our understanding of this 
transformation function.

<a id="normal-user-space-axes"></a>
The image below illustrates how <code>Cairo</code> draws text in the default 
user‑space axes:

<!--
| ![157-08-cairo-normal-text.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/01/157-08-cairo-normal-text.png) |
|:--:|
| Cairo Text in Default User-Space Axes |
-->
<table>
  <thead>
    <tr>
      <th style="text-align: center"><img src="https://behainguyen.wordpress.com/wp-content/uploads/2026/01/157-08-cairo-normal-text.png" alt="Cairo Text in Default User-Space Axes" width="335" height="205"></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center">Cairo Text in Default User-Space Axes</td>
    </tr>
  </tbody>
</table>

The text simply flows toward <code>X+</code> for left‑to‑right text.

<a id="90-degrees-rotated-user-space-axes"></a>
<em>“The rotation direction for positive angles is from the positive X axis toward the positive Y axis.”</em>  
For a +90° rotation, <code>X+</code> points <strong>down</strong> and 
<code>Y+</code> points <strong>left</strong>. That is:

<!--
| ![157-09-cairo-rotated-text-plus-90-degrees.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/01/157-09-cairo-rotated-text-plus-90-degrees.png) |
|:--:|
| Cairo Text in +90° Rotated User-Space Axes |
-->
<table>
  <thead>
    <tr>
      <th style="text-align: center"><img src="https://behainguyen.wordpress.com/wp-content/uploads/2026/01/157-09-cairo-rotated-text-plus-90-degrees.png" alt="Cairo Text in +90° Rotated User-Space Axes" width="205" height="335"></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center">Cairo Text in +90° Rotated User-Space Axes</td>
    </tr>
  </tbody>
</table>

<a id="minus-90-degrees-rotated-user-space-axes"></a>
For a -90° rotation, <code>X+</code> points <strong>up</strong> and 
<code>Y+</code> points <strong>right</strong>. That is:

<!--
| ![157-10-cairo-rotated-text-minus-90-degrees.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/01/157-10-cairo-rotated-text-minus-90-degrees.png) |
|:--:|
| Cairo Text in -90° Rotated User-Space Axes |
-->
<table>
  <thead>
    <tr>
      <th style="text-align: center"><img src="https://behainguyen.wordpress.com/wp-content/uploads/2026/01/157-10-cairo-rotated-text-minus-90-degrees.png" alt="Cairo Text in -90° Rotated User-Space Axes" width="205" height="335"></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center">Cairo Text in -90° Rotated User-Space Axes</td>
    </tr>
  </tbody>
</table>

💡 The key point is that the <strong>user‑space axes</strong> are rotated — not the text.  
Following the directions of <code>X+</code> and <code>Y+</code> is the key to 
understanding why the text appears rotated the way it does.  
I initially tried to reason about this in terms of <em>“clockwise”</em> and 
<em>“counter‑clockwise”</em>, but that approach failed; it does not map cleanly to 
how <code>Cairo</code> rotates the coordinate system.

<a id="concluding-remarks"></a>
❻ <strong>What’s Next</strong>

It was fun exploring this functionality. I also looked briefly into image rotation, 
though not as deeply as text rotation. I may study image rotation further and share 
my findings in another article.

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