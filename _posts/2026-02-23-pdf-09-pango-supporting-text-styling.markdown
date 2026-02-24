---
layout: post
title: "Rust: PDFs — Pango and Cairo Layout — Supporting Bold, Italic, and Bold Italic Text"

description: Implementing support for bold, italic, and bold italic text in paragraphs. Following Markdown, these three indicators — **, *, and *** — are used. Adjacent and nested Markdown syntaxes, as well as escapes such as \* and \\, are supported. This article continues and extends the work from the eighth article. In addition to rendering all natural headers, the final PDF now styles paragraph text according to the Markdown instructions in the source text file. 

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2026/02/159-01.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2026/02/159-02.png"

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
---

Implementing support for <strong>bold</strong>, <em>italic</em>, and <strong><em>bold italic</em></strong> text in paragraphs. Following <code>Markdown</code>, <a href="https://www.markdownguide.org/basic-syntax/#emphasis" title="Markdown Guide" target="_blank">these three indicators</a> — <code>**</code>, <code>*</code>, and <code>***</code> — are used. Adjacent and nested <code>Markdown</code> syntaxes, as well as escapes such as <code>\*</code> and <code>\\</code>, are supported. This article continues and extends the work from the <a href="https://behainguyen.wordpress.com/2026/01/30/rust-pdfs-pango-and-cairo-layout-supporting-headers/" title="Rust: PDFs — Exploring Layout with Pango and Cairo" target="_blank">eighth article</a>. In addition to rendering all natural headers, the final PDF now styles paragraph text according to the <code>Markdown</code> instructions in the source text file.

<h3>
🦀 <a href="https://github.com/behai-nguyen/polyglot_pdf" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![159-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/02/159-feature-image.png) |
|:--:|
| *Rust: PDFs — Pango and Cairo Layout — Supporting Bold, Italic, and Bold Italic Text* |

<a id="repository-cloning"></a>
🚀 The code for this post is in the following GitHub repository: 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling" 
title="Rust multilingual PDFs" target="_blank">pdf_06_text_styling</a>.

💡 Please note that <code>Pango</code> also supports HTML markup. I am not taking 
that route because I prefer to retain as much control as possible over how the 
input text is processed. For the same reason, I choose not to use any of the Rust 
<code>Markdown</code> parser crates, and instead implement a minimal parser that 
provides only the required support.

<a id="the-parser"></a>
❶ <strong>The Parser</strong>

We describe the features the parser supports and some of its known limitations.
The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/inline_parser.rs#L540-L1394" 
title="The pdf_06_text_styling/src/inline_parser.rs module" target="_blank">
<code>pdf_06_text_styling/src/inline_parser.rs</code> test suite</a>, in particular 
the test 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/inline_parser.rs#L582-L653" 
title="The pdf_06_text_styling/src/inline_parser.rs module" target="_blank">
<code>Markdown</code> constants</a>, should illustrate the parser's capabilities.

Also, the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/text/essay.txt" 
title="The pdf_06_text_styling/text/essay.txt input text file" target="_blank">
<code>pdf_06_text_styling/text/essay.txt</code></a> file provides a complete 
example of the supported <code>Markdown</code>.

💡 Please note, the term <strong>marker event</strong> is used to refer to 
<strong><em>a valid opening marker followed by a valid closing marker.</em></strong>

<a id="the-parser-supported-features"></a>
⓵ <strong>Supported Features</strong>

● <strong>Adjacent marker</strong>: a sequence of marker events. 
For example, <code>— **Tưởng Vĩnh Kính**, Hồ Chí Minh Tại *Trung Quốc*, Thượng Huyền 
dịch, ***trang 339***.</code>

● <strong>Nested marker</strong>: some marker events are enclosed within an outer 
marker event. For example, <code>**Không đọc *sử* không đủ tư cách nói chuyện 
*chính trị*.**</code>

● <strong>Escaped</strong>: the character <code>\</code> signifies that the character 
following it is escaped. For example, <code>\*not bold\*</code> is interpreted 
as the literal string <code>*not bold*</code>. <code>\\Úc Đại Lợi\\</code> 
is interpreted as <code>\Úc Đại Lợi\</code>.

<a id="the-parser-known-limitations"></a>
⓶ <strong>Known Limitations</strong>

● <strong>Uneven marker indicators</strong>: the result may not be what we expect.

<ol>
<li style="margin-top:10px;">
<code>**Tưởng Vĩnh Kính***</code>: results in <code><strong>Tưởng Vĩnh Kính</strong></code>, 
followed by <code>*</code>.
</li>

<li style="margin-top:10px;">
<code>***Tưởng Vĩnh Kính**</code>: results in <code><strong>*Tưởng Vĩnh Kính</strong></code>.
</li>

<li style="margin-top:10px;">
<code>***Tưởng Vĩnh Kính*</code>: results in <code>**</code> followed by 
<code><em>Tưởng Vĩnh Kính</em></code>.
</li>
</ol>

● <strong>Bold nested inside italic</strong>: for example, <code>*-- **Sir John Seeley**, 
1885*</code> is not supported. I discovered this at the last minute; it results in 
<code><em>-- Sir John Seeley, 1885</em></code>.

To get the intended effect of <code><em>--</em> <strong>Sir John Seeley</strong><em>, 1885</em></code>, 
use adjacent marker events: <code>*--* **Sir John Seeley***, 1885*</code>.

💥 It is best to construct marker events as cleanly as possible; ambiguous 
marker events can produce unexpected results.

Some software such as 
<a href="https://code.visualstudio.com/" title="Visual Studio Code" target="_blank">Visual Studio Code</a> 
and <a href="https://markdownlivepreview.com/" 
title="Markdown Live Preview" target="_blank">https://markdownlivepreview.com/</a> 
do not suffer from these limitations. Bringing this parser up to par with such software 
is not my objective, and is beyond my capabilities as well. I only aim to support a 
subset of <code>Markdown</code> that is sufficient for creating presentable PDFs.

<a id="repository-layout"></a>
❷ <strong>Repository Layout</strong>

💡 Please note: on both Windows and Ubuntu, I’m running Rust version 
<code>rustc 1.90.0 (1159e78c4 2025-09-14)</code>.

This is once again a one‑off project—I don’t plan to update it in future development. 
I want to keep a log of progress exactly as it occurred. Future code may copy this and 
make changes to it. I’ve placed the project under the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling" 
title="Rust multilingual PDFs" target="_blank">pdf_06_text_styling</a> directory. 
The structure is:

```
.
├── Cargo.toml
├── set_env.bat
├── config
│   └── config.toml
├── src
│   ├── config.rs
│   ├── document.rs
│   ├── font_utils.rs
│   ├── inline_parser.rs
│   ├── main.rs
│   ├── main_start_01.rs
│   ├── main_start_02.rs
│   └── page_geometry.rs
├── text
│   └── essay.txt
└── .vscode
    └── launch.json
```

<a id="repository-layout-desc"></a>
We describe some modules in the following subsections. The rest will be covered in 
the sections that follow.

<a id="page-geometry-mod"></a>
⓵ The <code>src/page_geometry.rs</code> module is copied unchanged from the 
<a href="https://behainguyen.wordpress.com/2026/01/16/rust-pdfs-text-rotation-with-cairo-and-pango/" 
title="Rust: PDFs — Text Rotation with Cairo and Pango" 
target="_blank">Rust: PDFs — Text Rotation with Cairo and Pango</a> article.  
👉 Changing any margin value in the <code>A4_DEFAULT_MARGINS</code> constant will 
change the layout of the text in the PDF.

<a id="config-mod"></a>
⓶ The <code>src/config.rs</code> module is copied unchanged from the 
<a href="https://behainguyen.wordpress.com/2026/01/30/rust-pdfs-pango-and-cairo-layout-supporting-headers/" 
title="Rust: PDFs — Pango and Cairo Layout — Supporting Headers" 
target="_blank">Rust: PDFs — Pango and Cairo Layout — Supporting Headers</a> article.

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
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/set_env.bat" 
title="pdf_06_text_styling/set_env.bat file" target="_blank"><code>set_env.bat</code></a>.  
After that, <code>cargo run</code> works as expected.

<a id="pkg-config-path-env-var"></a>
⓸ 💡 In the fifth article, we discussed the 
<a href="https://behainguyen.wordpress.com/2025/12/19/rust-pdfs-build-and-install-pango-and-associated-libraries/#windows-build-install-pango" 
title="Rust: PDFs — Build and Install Pango and Associated Libraries" target="_blank">
<code>PKG_CONFIG_PATH</code></a> user environment variable. This setting applies to all 
later articles. I did not mention it again from the sixth article onward. In the 
<code>set_env.bat</code> above, I include setting this variable so that we don't forget 
it and avoid potential surprises.

<a id="text-essay-file"></a>
⓹ The <code>text/essay.txt</code> file — copied from the 
<a href="https://behainguyen.wordpress.com/2026/01/30/rust-pdfs-pango-and-cairo-layout-supporting-headers/" 
title="Rust: PDFs — Pango and Cairo Layout — Supporting Headers" target="_blank">last article</a>,  
with <code>Markdown</code> added to text in paragraphs.

<a id="text-styling-nutshell"></a>
❸ <strong>Text Styling In a Nutshell</strong>

<a href="https://www.gtk.org/docs/architecture/pango" title="Pango Library" 
target="_blank"><code>Pango</code></a> provides a powerful and straightforward approach 
to text styling. We can summarise it as follows: <strong><em>first, apply the base font 
as usual; next, determine the byte‑range of the sub‑text you want to style, and apply 
attributes to those byte‑ranges to achieve the desired effects.</em></strong> 🦀 To get 
<strong><em>bold italic</em></strong> text, apply both bold and italic attributes to the 
same byte‑range.

We demonstrate this <code>Pango</code> approach in the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/main_start_01.rs" 
title="The pdf_06_text_styling/src/main_start_01.rs module" target="_blank">
<code>pdf_06_text_styling/src/main_start_01.rs</code></a> module. For the sake of 
simplicity, we use only single‑byte text: <code>xy, bc, de</code>. The new text‑styling 
code:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">34
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
50
51
</pre></td><td class="code"><pre>    <span class="k">let</span> <span class="n">attrs</span> <span class="o">=</span> <span class="nn">pango</span><span class="p">::</span><span class="nn">AttrList</span><span class="p">::</span><span class="nf">new</span><span class="p">();</span>
    
    <span class="k">let</span> <span class="k">mut</span> <span class="n">bold</span> <span class="o">=</span> <span class="nn">AttrInt</span><span class="p">::</span><span class="nf">new_weight</span><span class="p">(</span><span class="nn">Weight</span><span class="p">::</span><span class="n">Bold</span><span class="p">);</span> 
    <span class="n">bold</span><span class="nf">.set_start_index</span><span class="p">(</span><span class="mi">0</span><span class="p">);</span> 
    <span class="n">bold</span><span class="nf">.set_end_index</span><span class="p">(</span><span class="mi">9</span><span class="p">);</span> 
    <span class="n">attrs</span><span class="nf">.insert</span><span class="p">(</span><span class="n">bold</span><span class="p">);</span>

    <span class="k">let</span> <span class="k">mut</span> <span class="n">italic</span> <span class="o">=</span> <span class="nn">AttrInt</span><span class="p">::</span><span class="nf">new_style</span><span class="p">(</span><span class="nn">Style</span><span class="p">::</span><span class="n">Italic</span><span class="p">);</span>
    <span class="n">italic</span><span class="nf">.set_start_index</span><span class="p">(</span><span class="mi">4</span><span class="p">);</span>
    <span class="n">italic</span><span class="nf">.set_end_index</span><span class="p">(</span><span class="mi">5</span><span class="p">);</span>
    <span class="n">attrs</span><span class="nf">.insert</span><span class="p">(</span><span class="n">italic</span><span class="p">);</span>

    <span class="k">let</span> <span class="k">mut</span> <span class="n">italic</span> <span class="o">=</span> <span class="nn">AttrInt</span><span class="p">::</span><span class="nf">new_style</span><span class="p">(</span><span class="nn">Style</span><span class="p">::</span><span class="n">Italic</span><span class="p">);</span>
    <span class="n">italic</span><span class="nf">.set_start_index</span><span class="p">(</span><span class="mi">8</span><span class="p">);</span>
    <span class="n">italic</span><span class="nf">.set_end_index</span><span class="p">(</span><span class="mi">9</span><span class="p">);</span>
    <span class="n">attrs</span><span class="nf">.insert</span><span class="p">(</span><span class="n">italic</span><span class="p">);</span>

    <span class="n">layout</span><span class="nf">.set_attributes</span><span class="p">(</span><span class="nf">Some</span><span class="p">(</span><span class="o">&amp;</span><span class="n">attrs</span><span class="p">));</span>
</pre></td></tr></tbody></table></code></pre></figure>

💡 Please note: the index parameters passed to 
<a href="https://docs.rs/pango/latest/pango/struct.AttrInt.html#method.set_start_index" 
title="Struct AttrInt | pub fn set_start_index(&mut self, index: u32)" 
target="_blank">AttrInt::set_start_index()</a> and 
<a href="https://docs.rs/pango/latest/pango/struct.AttrInt.html#method.set_end_index" 
title="Struct AttrInt | pub fn set_end_index(&mut self, index: u32)" 
target="_blank">AttrInt::set_end_index()</a> are byte indices, not character indices. 
UTF‑8 characters may span multiple bytes.

In the code above:

<ul>
<li style="margin-top:10px;">
<strong>Bold</strong> is applied to the entire text, from <code>x</code> to <code>e</code>, 
inclusive.
</li>
<li style="margin-top:10px;">
<em>Italic</em> is applied to <code><em>bc</em></code> and <code><em>de</em></code>.  
Because bold already applies to the whole string, these segments become 
<strong><em>bold italic</em></strong>:  
<strong><em><code>bc</code></em></strong> and <strong><em><code>de</code></em></strong>.
</li>
</ul>

The parser identifies these byte‑ranges automatically based on the positions of the 
marker events. Next, we look at the parser from an overview perspective.

<a id="parser-overview"></a>
❹ <strong>Overview of the Parser</strong>

The parser lives in the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/inline_parser.rs" 
title="The pdf_06_text_styling/src/inline_parser.rs module" target="_blank">
<code>pdf_06_text_styling/src/inline_parser.rs</code></a> module. Its API is simple:

```rust
pub fn parse_inline(markdown_text: &str) -> InlineParseResult
```

<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/inline_parser.rs#L103-L115" 
title="The pdf_06_text_styling/src/inline_parser.rs module | InlineParseResult struct" target="_blank">
<code>InlineParseResult</code></a> encapsulates the result of parsing a single line 
(paragraph) of <code>Markdown</code> text. It exposes two pieces of data.

The first field is <code>text: String</code>. This is the text with all marker indicators 
(i.e. <code>*</code>) removed. Escaped asterisks are still represented by the 3‑byte 
character <code>\u{E000}</code>. Call the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/inline_parser.rs#L132-L135" 
title="The pdf_06_text_styling/src/inline_parser.rs module | reserve_asterisk() function" 
target="_blank"><code>reserve_asterisk()</code></a> function on this text to restore 
escaped <code>*</code> characters before giving it to <code>Pango</code>.

The second field is <code>spans: Vec&lt;Span&gt;</code>. This is the definition of the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/document.rs#L13-L49" 
title="The pdf_06_text_styling/src/document.rs module | Span struct" 
target="_blank"><code>Span</code></a> <code>struct</code>. Each <code>Span</code> 
represents a byte‑range—<a href="#text-styling-nutshell">as discussed earlier</a>—of a slice 
in <code>text</code> and its associated style. Recall that <code>***bold italic***</code> 
produces two <code>Span</code>s: one for <strong>bold italic</strong> and one for 
<em>bold italic</em>, resulting in <strong><em>bold italic</em></strong>.

Stripping out all inline documentation and test‑related code, the actual parser is fewer 
than 300 lines. Given the amount of inline documentation, we will not discuss the parser 
code in detail here. The documentation and the test methods should be sufficient to guide 
your understanding of the implementation.

<a id="simple-parser-example"></a>
❺ <strong>A Simple Example On Using the Parser</strong>

We now look at a simple example of how to apply the parser. The code is intentionally 
minimal: it parses a single line of <code>Markdown</code> text and writes it to a PDF. 
It assumes that the final clean text fits on a single line, so no measurement or layout 
logic is required.

This example is the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/main_start_02.rs" 
title="The pdf_06_text_styling/src/main_start_02.rs module" target="_blank">
<code>pdf_06_text_styling/src/main_start_02.rs</code></a> module, which is a 
refactored version of the earlier 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/main_start_01.rs" 
title="The pdf_06_text_styling/src/main_start_01.rs module" target="_blank">
<code>pdf_06_text_styling/src/main_start_01.rs</code></a> example:

● <a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/main_start_02.rs#L22-L64" 
title="The pdf_06_text_styling/src/main_start_02.rs module | create_font_attrs() function" target="_blank">
<code>create_font_attrs()</code></a>: a generic method that creates the styling 
attributes for the text. It is based on the code shown in a 
<a href="#text-styling-nutshell">previous discussion</a>.

● And in the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/main_start_02.rs#L66-L110" 
title="The pdf_06_text_styling/src/main_start_02.rs module | main() function" target="_blank">
<code>main()</code></a> function:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">84
85
86
87
88
89
90
91
92
93
94
95
96
97
</pre></td><td class="code"><pre>    <span class="k">let</span> <span class="n">markdown_text</span> <span class="o">=</span> <span class="s">r"**Không đọc *sử* không đủ tư cách nói chuyện *chính trị*.** \*"</span><span class="p">;</span>
    <span class="c">//</span> <span class="c">let</span> <span class="c">markdown_text</span> <span class="c">=</span> <span class="c">"***Không đọc sử không đủ tư cách nói chuyện chính trị.***"</span><span class="c">;</span>
    <span class="c">//</span> <span class="c">let</span> <span class="c">markdown_text</span> <span class="c">=</span> <span class="c">"( **Chính Ðạo, *Việt Nam Niên Biểu*, *Tập 1A***, trang 347 )"</span><span class="c">;</span>

    <span class="k">let</span> <span class="n">res</span> <span class="o">=</span> <span class="nf">parse_inline</span><span class="p">(</span><span class="n">markdown_text</span><span class="p">);</span>

    <span class="k">let</span> <span class="n">attrs</span> <span class="o">=</span> <span class="nn">pango</span><span class="p">::</span><span class="nn">AttrList</span><span class="p">::</span><span class="nf">new</span><span class="p">();</span>
    <span class="k">for</span> <span class="n">span</span> <span class="n">in</span> <span class="n">res</span><span class="nf">.spans</span><span class="p">()</span> <span class="p">{</span>
        <span class="k">for</span> <span class="n">attr</span> <span class="n">in</span> <span class="nf">create_font_attrs</span><span class="p">(</span><span class="n">span</span><span class="p">)</span> <span class="p">{</span>
            <span class="n">attrs</span><span class="nf">.insert</span><span class="p">(</span><span class="n">attr</span><span class="p">);</span>
        <span class="p">}</span>
    <span class="p">}</span>
    <span class="n">layout</span><span class="nf">.set_attributes</span><span class="p">(</span><span class="nf">Some</span><span class="p">(</span><span class="o">&amp;</span><span class="n">attrs</span><span class="p">));</span>
    <span class="n">layout</span><span class="nf">.set_text</span><span class="p">(</span><span class="o">&amp;</span><span class="nf">reserve_asterisk</span><span class="p">(</span><span class="n">res</span><span class="nf">.text</span><span class="p">()));</span>
</pre></td></tr></tbody></table></code></pre></figure>

<ul>
<li style="margin-top:10px;">
Calls <code>parse_inline()</code> to parse the <code>Markdown</code> text.
</li>
<li style="margin-top:10px;">
Uses the resulting <code>Span</code>s to create the appropriate styles for each 
byte‑range, and applies those styles.
</li>

<li style="margin-top:10px;">
Calls <code>reserve_asterisk()</code> on the resulting clean text to restore any 
escaped asterisks, then gives <code>Pango</code> this final text to render using the 
selected font and applied styles.
</li>
</ul>

Before we discuss the final main code, let's briefly cover the auxiliary modules.

<a id="the-auxiliary-modules"></a>
❻ <strong>The Auxiliary Modules</strong>

<a id="document-mod"></a>
⓵ The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/document.rs" 
title="The pdf_06_text_styling/src/document.rs module" target="_blank">
<code>pdf_06_text_styling/src/document.rs</code></a> module — copied from the 
<a href="https://behainguyen.wordpress.com/2026/01/30/rust-pdfs-pango-and-cairo-layout-supporting-headers/" 
title="Rust: PDFs — Pango and Cairo Layout — Supporting Headers" 
target="_blank">Rust: PDFs — Pango and Cairo Layout — Supporting Headers</a> 
article, with some refactorings:

<ul>
<a id="document-mod-span"></a>
<li style="margin-top:10px;">
Added 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/document.rs#L5-L49" 
title="The pdf_06_text_styling/src/document.rs module | enum SpanStyle and struct Span" target="_blank">
<code>enum SpanStyle</code> and <code>struct Span</code></a> — we covered these in the 
<a href="#parser-overview">Overview of the Parser</a> and 
<a href="#simple-parser-example">A Simple Example On Using the Parser</a> sections.
</li>

<a id="document-mod-block"></a>
<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/document.rs#L82-L90" 
title="The pdf_06_text_styling/src/document.rs module | struct Block" target="_blank">
<code>struct Block</code></a> — in the <code>Paragraph</code> variant, a new field 
<code>spans: Vec&lt;Span&gt;</code> has been added, which we will discuss in a 
<a href="#main-mod-parse_blocks">later section</a>.
</li>

<a id="document-mod-positioned-block"></a>
<li style="margin-top:10px;">
Removed <code>line_height</code> from 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/document.rs#L92-L105" 
title="The pdf_06_text_styling/src/document.rs module | struct PositionedBlock" target="_blank">
<code>struct PositionedBlock</code></a> — we will discuss this in a 
<a href="#main-mod-prepared-block">later section</a>.
</li>
</ul>

<a id="font-utils-mod"></a>
⓶ The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/font_utils.rs" 
title="The pdf_06_text_styling/src/font_utils.rs module" target="_blank">
<code>pdf_06_text_styling/src/font_utils.rs</code></a> module — the code here is 
not new:

<ul>
<li style="margin-top:10px;">
The 
<a href="https://behainguyen.wordpress.com/2026/01/30/rust-pdfs-pango-and-cairo-layout-supporting-headers/" 
title="Rust: PDFs — Pango and Cairo Layout — Supporting Headers" 
target="_blank">previous article</a>’s 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header/src/main.rs#L49-L75" 
title="The pdf_05_header/src/main.rs module | to_pango_description() method" 
target="_blank"><code>to_pango_description()</code></a> function is copied over.
</li>
<li style="margin-top:10px;">
The <code>create_font_attrs()</code> function discussed in 
<a href="#simple-parser-example">A Simple Example On Using the Parser</a>.
</li>
</ul>

We have now covered all the groundwork. Next, we discuss integrating the parser 
into the PDF creation process.

<a id="the-main-code"></a>
❼ <strong>The Main Code</strong>

The final module, 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/main.rs" 
title="The pdf_06_text_styling/src/main.rs module" target="_blank">
<code>pdf_06_text_styling/src/main.rs</code></a>, is a copy of the 
<a href="https://behainguyen.wordpress.com/2026/01/30/rust-pdfs-pango-and-cairo-layout-supporting-headers/" 
title="Rust: PDFs — Pango and Cairo Layout — Supporting Headers" 
target="_blank">previous article</a>’s 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header/src/main.rs" 
title="The pdf_05_header/src/main.rs module" target="_blank">
<code>pdf_05_header/src/main.rs</code></a> module, with some refactoring. We discuss 
those changes in the sections that follow.

<a id="main-mod-parse_blocks"></a>
● The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/main.rs#L116-L137" 
title="The pdf_06_text_styling/src/main.rs module | function parse_blocks_from_file()" target="_blank">
<code>parse_blocks_from_file()</code></a> function — for paragraph text, we 
now assume it is <code>Markdown</code> and parse it accordingly:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">130
131
132
133
</pre></td><td class="code"><pre>	<span class="p">}</span> <span class="k">else</span> <span class="p">{</span>
		<span class="k">let</span> <span class="n">InlineParseResult</span> <span class="p">{</span> <span class="n">text</span><span class="p">,</span> <span class="n">spans</span> <span class="p">}</span> <span class="o">=</span> <span class="nf">parse_inline</span><span class="p">(</span><span class="o">&amp;</span><span class="n">line</span><span class="p">);</span>
		<span class="n">blocks</span><span class="nf">.push</span><span class="p">(</span><span class="nn">Block</span><span class="p">::</span><span class="n">Paragraph</span> <span class="p">{</span> <span class="n">text</span><span class="p">,</span> <span class="n">spans</span> <span class="p">});</span>
	<span class="p">}</span>
</pre></td></tr></tbody></table></code></pre></figure>

We discussed <code>spans</code> in a <a href="#document-mod-block">previous section</a>. 
With this information available, we now have all the data required for measuring and 
pagination.

<a id="main-mod-prepare-layout-text"></a>
● The new 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/main.rs#L162-L180" 
title="The pdf_06_text_styling/src/main.rs module | prepare_layout_text() function" target="_blank">
<code>prepare_layout_text()</code></a> function replaces the previous 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header/src/main.rs#L151-L156" 
title="The pdf_05_header/src/main.rs module | block_text() function" target="_blank">
<code>block_text()</code></a> function. The code in this new function follows the 
approach we have already discussed, and should be self‑explanatory.

<a id="main-mod-prev-measuring"></a>
● The previous 
<a href="https://behainguyen.wordpress.com/2026/01/30/rust-pdfs-pango-and-cairo-layout-supporting-headers/#main-mod-measure_block" 
title="Rust: PDFs — Pango and Cairo Layout — Supporting Headers" target="_blank">
<code>measure_block()</code></a> and 
<a href="https://behainguyen.wordpress.com/2026/01/30/rust-pdfs-pango-and-cairo-layout-supporting-headers/#main-mod-output-positioned-block" 
title="Rust: PDFs — Pango and Cairo Layout — Supporting Headers" 
target="_blank"><code>output_positioned_block()</code></a> functions repeatedly create 
<code>pango::Layout</code> objects, set the font, and set the text in order to measure 
line heights, perform pagination, and finally render the output. In this article, we 
prepare everything once and cache it. The two methods mentioned above then use this 
cached data to perform their work, rather than recalculating everything on the fly. 
We discuss this caching implementation next.

<a id="main-mod-prepared"></a>
● The caching mechanism is made possible by the new 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/main.rs#L46-L61" 
title="The pdf_06_text_styling/src/main.rs module | struct PreparedBlock" target="_blank">
<code>struct PreparedBlock</code></a> and the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/main.rs#L182-L216" 
title="The pdf_06_text_styling/src/main.rs module | prepare_blocks() function" target="_blank">
<code>prepare_blocks()</code></a> function, which returns a vector of 
<code>PreparedBlock</code>.

<ol>
<a id="main-mod-prepared-block"></a>
<li style="margin-top:10px;">
<code>PreparedBlock</code> — this <code>struct</code> represents a 
<code>Pango</code>-ready‑to‑render version of the semantic 
<a href="#document-mod-block">Block</a>. The <code>layout</code> field contains 
complete layout data: individual lines derived from the 
<code>Block::Paragraph</code>’s <code>text</code> field that fit within the page width, 
right‑justified, and with font family, font size, and styling attributes already applied.
The <code>Block::Paragraph</code>’s <code>line_heights</code> vector stores the height of 
each individual line. Styling can cause line heights to vary, which is why we removed the 
<code>line_height</code> field from <code>struct PositionedBlock</code>, as 
<a href="#document-mod-positioned-block">previously discussed</a>.
</li>

<a id="main-mod-prepared-function"></a>
<li style="margin-top:10px;">
The new 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/main.rs#L182-L216" 
title="The pdf_06_text_styling/src/main.rs module | prepare_blocks() function" target="_blank">
<code>prepare_blocks()</code></a> function is a simplified version of the earlier 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_05_header/src/main.rs" 
title="The pdf_05_header/src/main.rs module | measure_block() function" 
target="_blank"><code>measure_block()</code></a> function. For each semantic 
<a href="#document-mod-block">Block</a>, it computes a <code>Pango</code>-ready 
<a href="#main-mod-prepared-block"><code>PreparedBlock</code></a> and finally returns a 
vector of <code>PreparedBlock</code>.
</li>
</ol>

It follows naturally that the total number of <code>PreparedBlock</code>s should always 
match the number of <code>Block</code>s, while there may be more 
<code>PositionedBlock</code>s.

● The new 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/main.rs#L218-L260" 
title="The pdf_06_text_styling/src/main.rs module | measure_block() function" target="_blank">
<code>measure_block()</code></a> function now receives, as its parameter, a 
reference to the vector of <code>PreparedBlock</code> returned by the 
<a href="#main-mod-prepared-function">prepare_blocks()</a> function. It performs its 
measurements based on this vector.

● The new 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/main.rs#L262-L279" 
title="The pdf_06_text_styling/src/main.rs module | output_positioned_block() function" target="_blank">
<code>output_positioned_block()</code></a> function now receives a reference 
to a <code>PreparedBlock</code>. The overall flow of the code remains largely unchanged.

The screenshots below show some PDF pages generated on 🐧 Ubuntu:

{% include image-gallery.html list=page.gallery-image-list %}
<br/>

<a id="concluding-remarks"></a>
❽ <strong>What’s Next</strong>

Implementing the parser took a while, but it was satisfying to see it completed. 
The next feature I would like to support is images with captions, where images are 
specified using relative paths, similar to how it is done in 
<a href="https://www.latex-project.org/" 
title="The LaTeX Project" target="_blank">LaTeX</a>.

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