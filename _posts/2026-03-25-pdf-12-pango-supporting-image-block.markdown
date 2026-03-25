---
layout: post
title: "Rust: PDFs — Pango and Cairo Layout — Supporting Image Blocks"

description: This article focuses on enabling the Markdown parser we last discussed to support image blocks, where images are specified using relative paths. Only the basic ![caption](relative/path/to/image.png) image‑block syntax is supported. 

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2026/03/162-01-a.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2026/03/162-01-b.png"

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
This article focuses on enabling the <code>Markdown</code> parser we <a href="https://behainguyen.wordpress.com/2026/02/23/rust-pdfs-pango-and-cairo-layout-supporting-bold-italic-and-bold-italic-text/#concluding-remarks" title="Rust: PDFs — Pango and Cairo Layout — Supporting Bold, Italic, and Bold Italic Text" target="_blank">last discussed</a> to support image blocks, where images are specified using relative paths. Only the basic <code>![caption](relative/path/to/image.png)</code> image‑block syntax is supported.
</em>

<h3>
🦀 <a href="https://github.com/behai-nguyen/polyglot_pdf" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![162-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/03/162-feature-image.png) |
|:--:|
| *Rust: PDFs — Pango and Cairo Layout — Supporting Image Blocks* |

<a id="repository-cloning"></a>
🚀 The code for this post is in the following GitHub repository: 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block" 
title="Rust multilingual PDFs" target="_blank">pdf_09_image_block</a>.

<a id="repository-layout"></a>
❶ <strong>Repository Layout</strong>

💡 Please note: on both Windows and Ubuntu, I’m running Rust version 
<code>rustc 1.90.0 (1159e78c4 2025-09-14)</code>.

This is once again a one‑off project — I don’t plan to update it in future development. 
I want to keep a log of progress exactly as it occurred. Future code may copy this and 
make changes to it. I’ve placed the project under the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block" 
title="Rust multilingual PDFs" target="_blank">pdf_09_image_block</a> directory. 
The structure is:

```
.
├── Cargo.toml
├── set_env.bat
├── config
│   └── config.toml
├── img
│   ├── Readme.md
│   └── unscalable.png
├── src
│   ├── config.rs
│   ├── document.rs
│   ├── font_utils.rs
│   ├── image_block_parser.rs
│   ├── image_layout.rs
│   ├── inline_parser.rs
│   ├── main.rs
│   ├── page_geometry.rs
│   └── text_layout.rs
├── text
│   ├── essay.txt
│   └── img
│     ├── ho-chi-minh-fontainebleau-19460914.png
│     └── ho-chi-minh-marius-moutet-19460914.png
└── .vscode
  └── launch.json
```

<a id="repository-layout-desc"></a>
We describe some entries in the following subsections. The rest will be covered in 
the sections that follow.

<a id="page-geometry-mod"></a>
⓵ The <code>src/page_geometry.rs</code> module is copied unchanged from 
<a href="https://behainguyen.wordpress.com/2026/03/15/rust-pdfs-cairo-and-pango-image-block-layout/" 
title="Rust: PDFs — Cairo and Pango — Image Block Layout" 
target="_blank">the eleventh</a> article. 👉 Changing any margin value in the 
<code>A4_DEFAULT_MARGINS</code> constant will change the layout of the text in the PDF. 
This module has remained unmodified for several articles.

<a id="font-utils-mod"></a>
⓶ The <code>src/font_utils.rs</code>, <code>src/text_layout.rs</code>, and 
<code>src/config.rs</code> modules are also copied unchanged from 
<a href="https://behainguyen.wordpress.com/2026/03/15/rust-pdfs-cairo-and-pango-image-block-layout/" 
title="Rust: PDFs — Cairo and Pango — Image Block Layout"
target="_blank">the eleventh</a> article.

<a id="font-utils-mod"></a>
⓷ The <code>src/config.rs</code> module and its associated 
<code>config/config.toml</code> file are also copied unchanged from 
<a href="https://behainguyen.wordpress.com/2026/03/15/rust-pdfs-cairo-and-pango-image-block-layout/" 
title="Rust: PDFs — Cairo and Pango — Image Block Layout" 
target="_blank">the eleventh</a> article. They were first introduced in 
<a href="https://behainguyen.wordpress.com/2026/01/30/rust-pdfs-pango-and-cairo-layout-supporting-headers/#the-main-code-config" 
title="Rust: PDFs — Pango and Cairo Layout — Supporting Headers | Font Configuration" 
target="_blank">the eighth</a> article, with 
<a href="https://behainguyen.wordpress.com/2026/03/15/rust-pdfs-cairo-and-pango-image-block-layout/#configuration-updates" 
title="Rust: PDFs — Cairo and Pango — Image Block Layout | Configuration Updates" 
target="_blank">significant additions</a> made in the eleventh.

<a id="inline_parser-mod"></a>
⓸ The <code>src/inline_parser.rs</code> module is copied unchanged from 
<a href="https://behainguyen.wordpress.com/2026/02/23/rust-pdfs-pango-and-cairo-layout-supporting-bold-italic-and-bold-italic-text/" 
title="Rust: PDFs — Pango and Cairo Layout — Supporting Bold, Italic, and Bold Italic Text" 
target="_blank">the ninth</a> article, where it was first introduced.

<a id="path-env-var"></a>
⓹ 💡 The code requires the <code>Pango</code>, <code>HarfBuzz</code>, <code>Cairo</code>, 
etc. libraries. 🐧 On Ubuntu, all required libraries are globally recognised. 🪟 On Windows, 
I haven’t added the paths for the libraries’ DLLs to the <code>PATH</code> environment 
variable. In each new Windows terminal session, I run the following once:

```
set PATH=C:\PF\harfbuzz\dist\bin\;%PATH%
set PATH=C:\PF\vcpkg\installed\x64-windows\bin\;%PATH%
set PATH=C:\PF\pango\dist\bin;C:\PF\cairo-1.18.4\dist\bin;C:\PF\fribidi\dist\bin;%PATH%
```

Alternatively, you can simply run 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/set_env.bat" 
title="pdf_09_image_block/set_env.bat file" target="_blank"><code>set_env.bat</code></a>. 
After that, <code>cargo run</code> works as expected.

<a id="pkg-config-path-env-var"></a>
⓺ 💡 In the fifth article, we discussed the 
<a href="https://behainguyen.wordpress.com/2025/12/19/rust-pdfs-build-and-install-pango-and-associated-libraries/#windows-build-install-pango" 
title="Rust: PDFs — Build and Install Pango and Associated Libraries" target="_blank">
<code>PKG_CONFIG_PATH</code></a> user environment variable. This setting applies to all 
later articles. I did not mention it again from the sixth article onward. In the 
<code>set_env.bat</code> above, I include setting this variable so that we don't forget 
it and avoid potential surprises.

<a id="document-mod"></a>
❷ <strong>The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/src/document.rs" 
title="The pdf_09_image_block/src/document.rs module" target="_blank">
<code>pdf_09_image_block/src/document.rs</code></a> Module
</strong>

This module is copied from 
<a href="https://behainguyen.wordpress.com/2026/03/15/rust-pdfs-cairo-and-pango-image-block-layout/" 
title="Rust: PDFs — Cairo and Pango — Image Block Layout" 
target="_blank">the eleventh</a> article; it was first introduced in 
<a href="https://behainguyen.wordpress.com/2026/01/30/rust-pdfs-pango-and-cairo-layout-supporting-headers/" 
title="Rust: PDFs — Pango and Cairo Layout — Supporting Headers | Font Configuration" 
target="_blank">the eighth</a>. This iteration makes several significant refactorings 
necessary to support image blocks:

<a id="document-block-enum"></a>
⓵ <a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/src/document.rs#L86-L98" 
title="The pdf_09_image_block/src/document.rs module | Block enum" target="_blank">
<code>Block enum</code></a> — it has been extended to support image blocks. At 
this stage, it should be self‑explanatory; we will encounter it again in a 
<a href="#parse-blocks-from-file-func">later section</a>.

<a id="document-image-block-layout-info-struct"></a>
⓶ <a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/src/document.rs#L100-L131" 
title="The pdf_09_image_block/src/document.rs module | ImageBlockLayoutInfo struct" target="_blank">
<code>ImageBlockLayoutInfo struct</code></a> — this <code>struct</code> was 
first introduced in the eleventh article’s 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout/src/image_layout.rs#L27-L45" 
title="The pdf_08_image_layout/src/image_layout.rs | ImageBlockLayoutInfo struct" target="_blank">
<code>src/image_layout.rs</code></a> module. Its implementation has been extended in 
this article.

<a id="document-image-block-measured-info-struct"></a>
⓷ <a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/src/document.rs#L133-L195" 
title="The pdf_09_image_block/src/document.rs module | ImageBlockMeasuredInfo struct" target="_blank">
<code>ImageBlockMeasuredInfo struct</code></a> — this is a new <code>struct</code>, 
whose usage will be discussed in a <a href="#image-layout-mod">later section</a>.

<a id="document-positioned-block-enum"></a>
⓸ <a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/src/document.rs#L197-L260" 
title="The pdf_09_image_block/src/document.rs module | PositionedBlock enum" target="_blank">
<code>PositionedBlock enum</code></a> — the original <code>struct</code> has been 
refactored into an <code>enum</code> to support image blocks. At this stage, it should be 
self‑explanatory; we will encounter it again in a 
<a href="#measure-block-func">later section</a>.

<a id="image-layout-mod"></a>
❸ <strong>The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/src/image_layout.rs" 
title="The pdf_09_image_block/src/image_layout.rs module" target="_blank">
<code>pdf_09_image_block/src/image_layout.rs</code></a> Module
</strong>

In the last — eleventh — article, we discussed the 
<a href="https://behainguyen.wordpress.com/2026/03/15/rust-pdfs-cairo-and-pango-image-block-layout/#layout-algorithm" 
title="Rust: PDFs — Cairo and Pango — Image Block Layout | The Image Block Layout Algorithm" 
target="_blank">image block layout algorithm</a>, and the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_08_image_layout/src/image_layout.rs#L176-L298" 
title="The pdf_08_image_layout/src/image_layout.rs module | layout_image_block() function" target="_blank">
<code>layout_image_block()</code></a> function implements that algorithm. 
This function — by itself — is not suitable for integration into the PDF generation 
pipeline. It has therefore been refactored into two functions:

<a id="image-layout-measure-image-block-fn"></a>
⓵ <a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/src/image_layout.rs#L152-L238" 
title="The pdf_09_image_block/src/image_layout.rs module | measure_image_block() function" target="_blank">
<code>measure_image_block()</code></a> — this function effectively implements the 
<a href="https://behainguyen.wordpress.com/2026/03/15/rust-pdfs-cairo-and-pango-image-block-layout/#layout-algorithm" 
title="Rust: PDFs — Cairo and Pango — Image Block Layout | The Image Block Layout Algorithm" 
target="_blank">algorithm</a>, but no longer renders images or captions. Instead, on 
success, it returns the information required for pagination and later rendering of the 
image block — the <code>ImageBlockMeasuredInfo</code> struct that was 
<a href="#image-block-measured-info-struct">previously mentioned</a>. 
It is a simplified version of <code>layout_image_block()</code>, and we will not cover it 
in detail.

🦀 The tests have been rewritten accordingly for this function. The image 
<code>img/unscalable.png</code> is not strictly required for the tests; it is included 
in the codebase for completeness.

<a id="image-layout-render-image-block-fn"></a>
⓶ <a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/src/image_layout.rs#L240-L297" 
title="The pdf_09_image_block/src/image_layout.rs module | render_image_block() function" target="_blank">
<code>render_image_block()</code></a> — this is also a refactored and simplified 
version of <code>layout_image_block()</code>. It is responsible solely for rendering the 
image block. It has no intelligence: it simply renders the loaded PNG based on the 
information it is given. There is no test for this method.

<a id="image-block-parser-mod"></a>
❹ <strong>The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/src/image_block_parser.rs" 
title="The pdf_09_image_block/src/image_block_parser.rs module" target="_blank">
<code>pdf_09_image_block/src/image_block_parser.rs</code></a> Module
</strong>

This module is the parser for image‑block text. As mentioned in the introduction, 
only the basic syntax <code>![caption](relative/path/to/image.png)</code> is supported.

🦀 The API is the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/src/image_block_parser.rs#L154-L159" 
title="The pdf_09_image_block/src/image_block_parser.rs module | parse_image_block() function" target="_blank">
<code>parse_image_block()</code></a> function. The comprehensive test suite 
illustrates how to call this API and demonstrates invalid edge cases.

The code itself is less than 130 lines and is fully documented. Let's reprint the 
assumptions and limitations from the module documentation.

<a id="image-block-parser-assumptions"></a>
⓵ <strong>Assumptions</strong>

<ol>
<li style="margin-top:10px;">
The image‑block text must be at least <code>![](relative/path/to/image.png)</code>.
</li>

<li style="margin-top:10px;">
The image‑block text represents only a single image block.
</li>
</ol>

<a id="image-block-parser-limitations"></a>
⓶ <strong>Limitations</strong>

<ol>
<li style="margin-top:10px;">
Captions containing <code>]</code> or <code>[</code> are not supported. 
For example, <code>![A caption with \]](path)</code> will be treated as invalid.
</li>

<li style="margin-top:10px;">
Paths containing <code>)</code> are not supported. 
For example, <code>![caption](path_(1).png)</code> will result in an invalid path, 
because the parser stops at the first <code>)</code>.
</li>

<li style="margin-top:10px;">
Multiple image blocks on one line are not supported. 
The parser handles only one image block per line.
</li>
</ol>

<a id="essay-text-file"></a>
❺ <strong>The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/text/essay.txt" 
title="The pdf_09_image_block/text/essay.txt file" target="_blank">
<code>pdf_09_image_block/text/essay.txt</code></a> and Associated Image Files 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/text/img/" 
title="The pdf_09_image_block/text/img/ files" target="_blank">
<code>pdf_09_image_block/text/img/*.*</code></a>
</strong>

The <code>pdf_09_image_block/text/essay.txt</code> file is copied from 
<a href="https://behainguyen.wordpress.com/2026/02/23/rust-pdfs-pango-and-cairo-layout-supporting-bold-italic-and-bold-italic-text/" 
title="Rust: PDFs — Pango and Cairo Layout — Supporting Bold, Italic, and Bold Italic Text" 
target="_blank">the ninth</a> article. Two modifications were made:

<ol>
<li style="margin-top:10px;">
Removed an extra marker <code>**</code>, which would otherwise appear as a literal 
string in the final PDF.
</li>

<li style="margin-top:10px;">
Added two image‑block texts, one for each of the images under <code>text/img/</code>.
</li>
</ol>

<a id="main-mod"></a>
❻ <strong>The 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/src/main.rs" 
title="The pdf_09_image_block/src/main.rs module" target="_blank">
<code>pdf_09_image_block/src/main.rs</code></a> Module
</strong>

🙏 Before proceeding with this module, it is beneficial to review the 
<a href="#document-mod">discussion</a> on the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/src/document.rs" 
title="The pdf_09_image_block/src/document.rs module" target="_blank">
<code>pdf_09_image_block/src/document.rs</code></a>.

This module brings everything together, just as in previous iterations, and is therefore 
the most complicated one. It is originally copied from the 
<a href="https://behainguyen.wordpress.com/2026/02/23/rust-pdfs-pango-and-cairo-layout-supporting-bold-italic-and-bold-italic-text/" 
title="Rust: PDFs — Pango and Cairo Layout — Supporting Bold, Italic, and Bold Italic Text" 
target="_blank">ninth</a> article, specifically from the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/main.rs" 
title="The pdf_06_text_styling/src/main.rs module" 
target="_blank"><code>pdf_06_text_styling/src/main.rs</code></a> module. 
Let’s discuss the refactorings carried out on it.

<a id="prepared-block-enum"></a>
⓵ <a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/src/main.rs#L54-L78" 
title="The pdf_09_image_block/src/main.rs module | PreparedBlock enum" target="_blank">
<code>PreparedBlock enum</code></a> — the original <code>struct</code> has been 
refactored into an <code>enum</code> to support image blocks.

<a id="parse-blocks-from-file-func"></a>
⓶ The next function requiring refactoring is 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/src/main.rs#L130-L181" 
title="The pdf_09_image_block/src/main.rs module | parse_blocks_from_file() function" target="_blank">
<code>parse_blocks_from_file()</code></a> — this function reads the text file and 
turns each line into its corresponding 
<a href="#document-block-enum"><code>Block enum</code></a> representation. 
It now also detects image‑block text via the new helper 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/src/main.rs#L121-L128" 
title="The pdf_09_image_block/src/main.rs module | detect_image_block_text() function" target="_blank">
<code>detect_image_block_text()</code></a> function, then invokes the 
<a href="#image-block-parser-mod"><code>parse_image_block()</code></a> API to parse the 
text. If the syntax is invalid, the image‑block text is treated as a normal paragraph. 
Otherwise, a <a href="#document-block-enum"><code>Block::Image</code></a> is created. 
In either case, a <code>Block enum</code> representation of the line is produced and 
stored in the returned vector. 

<a id="create-layout-for-block-func"></a>
⓷ The new, more unified function 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/src/main.rs#L209-L248" 
title="The pdf_09_image_block/src/main.rs module | create_layout_for_block() function" target="_blank">
<code>create_layout_for_block()</code></a> replaces the previous 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_06_text_styling/src/main.rs#L162-L180" 
title="The pdf_06_text_styling/src/main.rs module | prepare_layout_text() function" 
target="_blank"><code>prepare_layout_text()</code></a> function.

<a id="prepare-blocks-func"></a>
⓸ The next function that has been extended is 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/src/main.rs#L250-L291" 
title="The pdf_09_image_block/src/main.rs module | prepare_blocks() function" target="_blank">
<code>prepare_blocks()</code></a> — it converts each 
<a href="#document-block-enum"><code>Block enum</code></a> into its corresponding 
<a href="#prepared-block-enum"><code>PreparedBlock enum</code></a> variant. 
🙏 In the new <code>PreparedBlock::Image</code> arm, it prepares and caches both the 
ready‑to‑render image caption and the image PNG stream as a 
<a href="https://docs.rs/pango/latest/pango/struct.Layout.html" 
title="Struct Layout" target="_blank"><code>pango::Layout</code></a> and a 
<a href="https://docs.rs/cairo-rs/latest/cairo/struct.ImageSurface.html" 
title="Struct ImageSurface" target="_blank"><code>cairo::ImageSurface</code></a>, 
respectively. 🦀 The <code>cairo::ImageSurface</code> provides both the PNG’s physical width and 
height — values required for step‑scaling.

<a id="measure-block-func"></a>
⓹ The next function in the pipeline is 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/src/main.rs#L293-L382" 
title="The pdf_09_image_block/src/main.rs module | measure_block() function" target="_blank">
<code>measure_block()</code></a> — in the new <code>PreparedBlock::Image</code> 
arm, it first calls 
<a href="#image-layout-measure-image-block-fn"><code>measure_image_block()</code></a> 
to perform step‑scaling and collect pagination, positioning, and measurement 
information. Using the data returned from <code>measure_image_block()</code>, it then 
creates and stores a 
<a href="#document-positioned-block-enum"><code>PositionedBlock::Image</code></a> 
in the returned vector. Finally, it updates the positioning and pagination for the 
next block, mirroring the existing <code>PositionedBlock::Text</code> arm.

<a id="output-positioned-block-func"></a>
⓺ The final function in the chain is 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/pdf_09_image_block/src/main.rs#L384-L413" 
title="The pdf_09_image_block/src/main.rs module | output_positioned_block() function" target="_blank">
<code>output_positioned_block()</code></a> — following the same pattern, a new 
<a href="#document-positioned-block-enum"><code>PositionedBlock::Image</code></a> arm 
was added to render in‑memory image blocks. This new arm is very simple: it gathers all 
cached information and passes it to 
<a href="#image-layout-render-image-block-fn">render_image_block()</a> to render the 
image and its caption.

With the addition of the two image blocks, the total number of pages is now 36 
(thirty‑six), an increase of 1 (one) page. The screenshots below show the two pages 
containing image blocks:

{% include image-gallery.html list=page.gallery-image-list %}
<br/>

We are using exactly the same configuration on both Ubuntu 🐧 and Windows 10 🪟, 
resulting in identical final PDF output on both platforms.

<a id="concluding-remarks"></a>
❼ <strong>What’s Next</strong>

That is all for this article… I am glad I decided to write the image‑block parser 
rather than rely on regular expressions — I genuinely enjoyed implementing it. 
There are still several features I would like to support. For example, lists — both 
bullet points and numbered — which I understand can be a challenging feature to 
implement. Another example is correctly recognising and rendering URLs so that they 
become clickable links within the PDF.

At the moment, I am not sure which one I will tackle next…

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