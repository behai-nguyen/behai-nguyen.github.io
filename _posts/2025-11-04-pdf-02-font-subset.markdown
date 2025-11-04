---
layout: post
title: "Rust FFI Font Subsetting Using the HarfBuzz Text Shaping Engine"

description: Loosely speaking, font subsetting involves extracting only the characters we need from a font program, such as a TrueType .ttf file. The Arial Unicode MS font program is around 20MB. If we need only a few Vietnamese characters, we can extract and use those, resulting in a font subset of just a few kilobytes. This article focuses on font subsetting on Windows and Ubuntu as a standalone process. We begin by installing a few standalone font tools on Windows, then explore the font subsetting workflow using the HarfBuzz library.

tags:
- Rust
- FFI
- HarfBuzz
- hb-shape
- hb-subset
- Unicode
- font subset
---

*Loosely speaking, <strong>font subsetting</strong> involves extracting only the characters we need from a font program, such as a TrueType <code>.ttf</code> file. The <code>Arial Unicode MS</code> font program is around 20MB. If we need only a few Vietnamese characters, we can extract and use those, resulting in a font subset of just a few kilobytes.*

*This article focuses on <em>font subsetting</em> on Windows and Ubuntu as a standalone process. We begin by installing a few standalone font tools on Windows, then explore the font subsetting workflow using the HarfBuzz library.*

<h3>
🦀 <a href="https://github.com/behai-nguyen/polyglot_pdf" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![152-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/11/152-feature-image.png) |
|:--:|
| *Rust FFI Font Subsetting Using the HarfBuzz Text Shaping Engine* |

<a id="repository-cloning"></a>
🚀 The code for this post is in the following GitHub repository: 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/harfbuzz_font_subset" 
title="The harfbuzz_font_subset/src/main.rs module" target="_blank">
harfbuzz_font_subset</a>.

This article is a continuation of the 
<a href="https://behainguyen.wordpress.com/2025/10/28/rust-ffi-adventure-with-the-harfbuzz-text-shaping-engine/" 
title="Rust FFI “Adventure” with the HarfBuzz Text Shaping Engine" 
target="_blank">first article</a>. In this article, we also present a brand new 
standalone program, whose boilerplate code is also based on the program that 
accompanied the previously mentioned article.

<a id="win-install-birdfont"></a>
❶ <strong>Install the <code>BirdFont</code> GUI Application</strong>

You can download the installer from 
<a href="https://birdfont.org/" title="BirdFont" target="_blank">BirdFont</a>.
It is free software, and donations to the developers are welcome.

Originally, ChatGPT recommended 
<a href="https://fontforge.org/en-US/" title="FontForge" target="_blank">FontForge</a>, 
which I did install and use for a bit. However, it’s quite old, and the UI feels a bit awkward.

<a id="win-install-python-fonttools"></a>
❷ <strong>Install the Python <code>fontTools</code> Package</strong>

This is its repository: 
<a href="https://github.com/fonttools/fonttools" 
title="Python fontTools" target="_blank">https://github.com/fonttools/fonttools</a>. 
We can use it to convert a font program (such as a <code>TrueType</code> font file) 
into XML to inspect internal information that would otherwise be hidden.

💡 If you're unfamiliar with <em>Python Virtual Environments</em> or how to set one up, 
please see this post: 
<a href="https://behainguyen.wordpress.com/2022/02/15/python-virtual-environment-virtualenv-for-multiple-python-versions/" 
title="Python: Virtual Environment virtualenv for multiple Python versions."
target="_blank">Python: Virtual Environment virtualenv for multiple Python versions</a>, 
which I wrote a fair while back.

I already have a generic Python development area under <code>F:\pydev\</code>. After 
changing to the <code>F:\pydev\</code> directory, activate the virtual environment 
<code>venv</code>, then install the <code>fonttools</code> package using the following commands:

```
F:\pydev>venv\Scripts\activate
(venv) F:\pydev>pip install fonttools[ufo,lxml,woff,unicode]
```

Once completed, we can verify the installation with the following command:

```
(venv) F:\pydev>ttx --version
```

My installation reports <code>4.60.1</code>.

🐧 On Ubuntu, the installation we performed in the 
<a href="https://behainguyen.wordpress.com/2025/10/28/rust-ffi-adventure-with-the-harfbuzz-text-shaping-engine/" 
title="Rust FFI “Adventure” with the HarfBuzz Text Shaping Engine" 
target="_blank">first article</a> also installed this tool: <code>ttx --version</code> 
reports <code>4.46.0</code>.

🪟 On Windows, I can run it as follows:

```
(venv) F:\pydev>ttx path\to\font\program\font_file.ttf
```

🐧 On Ubuntu, the CLI syntax is the same.

The resulting <code>path\to\font\program\font_file.ttx</code> is an XML file that 
lists the internal structure of the <code>.ttf</code> font program.

<a id="win-install-harfbuzz-cli"></a>
❸ <strong>Optionally Install <code>HarfBuzz</code> CLI Tools</strong>

Recall that the build we performed in the 
<a href="https://behainguyen.wordpress.com/2025/10/28/rust-ffi-adventure-with-the-harfbuzz-text-shaping-engine/" 
title="Rust FFI “Adventure” with the HarfBuzz Text Shaping Engine" 
target="_blank">first article</a> also produced some CLI tools for 
<a href="https://behainguyen.wordpress.com/2025/10/28/rust-ffi-adventure-with-the-harfbuzz-text-shaping-engine/#win-libs-clis" 
title="Rust FFI “Adventure” with the HarfBuzz Text Shaping Engine" 
target="_blank">Windows</a> and 
<a href="https://behainguyen.wordpress.com/2025/10/28/rust-ffi-adventure-with-the-harfbuzz-text-shaping-engine/#ubuntu-libs-clis" 
title="Rust FFI “Adventure” with the HarfBuzz Text Shaping Engine" 
target="_blank">Ubuntu</a>. 

If desired, we can download a prebuilt version of these CLI tools from 
<a href="https://sourceforge.net/projects/harfbuzz.mirror/" title="HarfBuzz CLIs"
target="_blank">https://sourceforge.net/projects/harfbuzz.mirror/</a>. I downloaded 
<code>harfbuzz-win64-12.1.0.zip</code> and extracted its contents to 
<code>C:\PF\harfbuzz-win64\</code>. I believe this build is provided by the author of HarfBuzz.

<a id="font-programs-used"></a>
❹ <strong>Font Programs Used In This Article</strong>

🪟 On Windows, we use the standard <code>Arial Unicode MS</code> font, located at 
<code>C:/Windows/Fonts/arialuni.ttf</code>. 🐧 On Ubuntu, I downloaded 
<code>Noto_Sans_SC</code>, <code>Noto_Sans_TC,Noto_Serif_TC.zip</code> 
from 
<a href="https://fonts.google.com/selection" title="Google Fonts" 
target="_blank">Google Fonts</a>, and extracted the contents to 
<code>/home/behai/Noto_Sans_TC</code>. The font program we are using is 
<code>NotoSansTC-Regular.ttf</code>.

To keep things simple, we will refer to these fonts using absolute paths. 

<a id="hb-shape-hb-subset"></a>
❺ <strong>The <code>hb-shape</code> and <code>hb-subset</code> CLIs</strong>

💡 Please note: based on the build and installation process discussed in the 
<a href="https://behainguyen.wordpress.com/2025/10/28/rust-ffi-adventure-with-the-harfbuzz-text-shaping-engine/" 
title="Rust FFI “Adventure” with the HarfBuzz Text Shaping Engine" 
target="_blank">first article</a>, 🪟 on Windows, before running these CLIs we 
need to set the library paths once per terminal session:

```
set PATH=C:\PF\harfbuzz\build\src\;%PATH%
set PATH=C:\PF\vcpkg\installed\x64-windows\bin\;%PATH%
```

<a id="glyph-id"></a>
A <a href="https://www.google.com/search?q=what+is+harfbuzz+glyph+id&sca_esv=026ce982ac60e96f&biw=1440&bih=697&sxsrf=AE3TifOfZMciZg_MN_puL01vM99FE2AiNA%3A1762042673992&ei=MaMGaf2jPMCc4-EPzeObgAM&ved=0ahUKEwi9gKa9mNKQAxVAzjgGHc3xBjAQ4dUDCBE&uact=5&oq=what+is+harfbuzz+glyph+id&gs_lp=Egxnd3Mtd2l6LXNlcnAiGXdoYXQgaXMgaGFyZmJ1enogZ2x5cGggaWQyBRAhGKABMgUQIRigAUiYS1C5HlinSHABeAGQAQCYAd8BoAGFG6oBBjAuMjAuMbgBA8gBAPgBAZgCCKACkAnCAgoQABiwAxjWBBhHwgIIECEYoAEYwwTCAgoQIRigARjDBBgKmAMAiAYBkAYCkgcDMS43oAfASbIHAzAuN7gHhAnCBwUwLjQuNMgHGA&sclient=gws-wiz-serp" 
title="what is harfbuzz glyph id" target="_blank">glyph ID</a> is an unsigned integer 
used by a font program to represent a specific visual shape of a character—for example, 
<code>Ề</code>. The same character can have different glyph IDs in different font programs.

The text we are using for font subsetting throughout this article is 
<em>“Kỷ độ Long Tuyền đới nguyệt ma. 幾度龍泉戴月磨。”</em> — a single verse in Vietnamese 
and Chinese from a poem by General Đặng Dung of the Later Trần Dynasty, shortly 
before the general took his own life in 1413, rather than be executed by his 
Ming-Chinese captors. This verse means <em>“Countless times I have sharpened my 
battle sword under the moonlight.”</em>

<a id="hb-shape"></a>
⓵ <strong>The <code>hb-shape</code> CLI</strong>

The <code>hb-shape</code> CLI is a shaping diagnostics tool. Among its many options, 
we can use it to obtain the glyph IDs for a given text and font program.

🪟 -- In its simplest form:

```
C:\PF\harfbuzz\build\util\hb-shape.exe ^
C:\Windows\Fonts\arialuni.ttf ^
"Kỷ độ Long Tuyền đới nguyệt ma. 幾度龍泉戴月磨。"
```

The output looks like:

```
[gid46=0+1366|gid2985=1+1024|gid3=2+569|gid211=3+1139^
|gid2955=4+1139|gid3=5+569|gid47=6+1139|gid82=7+1139|^
gid81=8+1139|gid74=9+1139|gid3=10+569|gid55=11+1251|^
gid88=12+1139|gid92=13+1024|gid2931=14+1139|gid81=^
15+1139|gid3=16+569|gid211=17+1139|gid2957=18+1139|^
gid76=19+455|gid3=20+569|gid81=21+1139|gid74=22+1139|^
gid88=23+1139|gid92=24+1024|gid2937=25+1139|gid87=^
26+569|gid3=27+569|gid80=28+1706|gid68=29+1139|gid17^
=30+569|gid3=31+569|^gid12557=32+2048|gid12597=33+2048^
|gid29212=34+2048|^gid16216=35+2048|gid13507=36+2048|^
gid14743=37+2048|gid19319=38+2048|gid4589=39+2048]
```

💡 <strong>Note:</strong> if we run the above command multiple times, 
we are not guaranteed to get the glyph list in the same order each time.

We can feed the unique <code>gid</code>s—<code>46</code>, <code>2985</code>, … <code>4589</code>—
into <code>hb-subset</code> to create a font subset program if we choose to.

To get CLI options for <code>hb-shape</code>, we can run:

```
C:\PF\harfbuzz\build\util\hb-shape.exe --help
```

To get just the glyph IDs for the text:

```
C:\PF\harfbuzz\build\util\hb-shape.exe --no-glyph-names^ 
--no-positions --no-clusters C:\Windows\Fonts\arialuni.ttf^ 
"Kỷ độ Long Tuyền đới nguyệt ma. 幾度龍泉戴月磨。"
```

The output is now simplified to:

```
[46|2985|3|211|2955|3|47|82|81|74|3|55|88|92|2931|^
81|3|211|2957|76|^3|81|74|88|92|2937|87|3|80|68|17|^
3|12557|12597|29212|16216|13507|14743|19319|4589]
```

🐧 -- Using a different font program, we get different glyph IDs:

```
$ hb-shape /home/behai/Noto_Sans_TC/NotoSansTC-Regular.ttf^ 
"Kỷ độ Long Tuyền đới nguyệt ma. 幾度龍泉戴月磨。"
```

Output:

```
[gid44=0+621|gid460=1+521|gid1=2+224|gid194=3+620|^
gid430=4+606|gid1=5+224|gid45=6+527|gid80=7+606|gid79^
=8+610|gid72=9+564|gid1=10+224|gid53=11+544|gid86=^
12+607|gid90=13+514|gid406=14+554|gid79=15+610|gid1^
=16+224|gid194=17+620|gid432=18+606|gid74=19+275|^
gid1=20+224|gid79=21+610|gid72=22+564|gid86=23+607|^
gid90=24+514|gid412=25+540|gid85=26+377|gid1=27+224|^
gid78=28+926|gid66=29+563|gid15=30+278|gid1=31+224|^
gid5794=32+1000|gid5822=33+1000|gid17998=34+1000|^
gid8575=35+1000|gid6506=36+1000|gid7442=37+1000|^
gid11001=38+1000|gid20341=39+1000]
```

And:

```
$ hb-shape /home/behai/Noto_Sans_TC/NotoSansTC-Regular.ttf^ 
--no-glyph-names --no-positions --no-clusters^ 
"Kỷ độ Long Tuyền đới nguyệt ma. 幾度龍泉戴月磨。"
```

gives:

```
[44|460|1|194|430|1|45|80|79|72|1|53|86|90|406|79|^
1|194|432|74|1|79|72|86|90|412|85|1|78|66|15|1|5794|^
5822|17998|8575|6506|7442|11001|20341]
```

<a id="hb-subset"></a>
⓶ <strong>The <code>hb-subset</code> CLI</strong>

The <code>hb-subset</code> CLI extracts only the characters we need from a font 
program. We can either provide the text directly or supply a unique list of glyph IDs 
that represent the text.

🪟 -- Let's take a look at glyph ID input. I’m using the list above, which 
contains duplicates:

```
C:\PF\harfbuzz\build\util\hb-subset.exe --glyphs=46,^
2985,3,211,2955,3,47,82,81,74,3,55,88,92,2931,81,3,^
211,2957,76,3,81,74,88,92,2937,87,3,80,68,17,3,^
12557,12597,29212,16216,13507,14743,19319,4589^ 
C:/Windows/Fonts/arialuni.ttf --output-file=subset.ttf
```

The screenshot below shows <code>subset.ttf</code> as viewed in 
<a href="#win-install-birdfont">BirdFont</a>:

| ![152-windows-font-subset.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/11/152-windows-font-subset.png) |
|:--:|
| Windows |

🐧 -- Now let’s look at text input:

```
$ hb-subset /home/behai/Noto_Sans_TC/NotoSansTC-Regular.ttf^ 
--text="Kỷ độ Long Tuyền đới nguyệt ma. 幾度龍泉戴月磨。"^ 
--output-file=subset.ttf
```

The screenshot below shows <code>subset.ttf</code> as viewed in 
<a href="#win-install-birdfont">BirdFont</a>:

| ![152-ubuntu-font-subset.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/11/152-ubuntu-font-subset.png) |
|:--:|
| Ubuntu |

<a id="rust-harfbuzz-subsetting"></a>
❻ <strong>A Rust FFI Font Subsetting Using <code>HarfBuzz</code>’s Functions</strong>

We are replicating the subsetting functionality of the <code>hb-subset</code> CLI 
using Rust FFI to call into <code>HarfBuzz</code>’s functions. The structure 
of this program is quite similar to the 
<a href="https://behainguyen.wordpress.com/2025/10/28/rust-ffi-adventure-with-the-harfbuzz-text-shaping-engine/#rust-ffi" 
title="Rust FFI “Adventure” with the HarfBuzz Text Shaping Engine" target="_blank">
<code>HarfBuzz</code>’s <code>hb_version_string()</code> program discussed in the 
first article</a> — in this one, we’re simply calling more of <code>HarfBuzz</code>’s functions.
🦀 This program is also a one-off standalone; we’ll use the illustrated code to develop 
future programs, but we won’t be making changes to it.

We note the following:

⓵ In <a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/harfbuzz_font_subset/build.rs#L55" 
title="The harfbuzz_font_subset/build.rs module" target="_blank"><code>
harfbuzz_font_subset/build.rs</code></a>: Added <code>hb-subset.h</code>. 
The compiler will generate a new <code>bindings.rs</code> module, which will 
include the required <code>HarfBuzz</code> subset functions.

⓶ In <a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/harfbuzz_font_subset/src/main.rs" 
title="The harfbuzz_font_subset/src/main.rs module" target="_blank"><code>
harfbuzz_font_subset/src/main.rs</code></a>:

● <a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/harfbuzz_font_subset/src/main.rs#L11-L23" 
title="The harfbuzz_font_subset/src/main.rs module" target="_blank">Lines 11–23</a>: 
We import the functions needed for subsetting.

● <a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/harfbuzz_font_subset/src/main.rs#L53-L55" 
title="The harfbuzz_font_subset/src/main.rs module" target="_blank">Lines 53–55</a>: 
We use character Unicode values, effectively subsetting based on the actual text.
The text is hardcoded for simplicity.

● Note the lack of error handling — this is intentional to keep the code simple for 
illustration purposes.

● <a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/harfbuzz_font_subset/src/main.rs#L65-L72" 
title="The harfbuzz_font_subset/src/main.rs module" target="_blank">Lines 65–72</a>: 

```rust
    let result = slice.to_vec();

    unsafe { hb_blob_destroy(blob) };
    unsafe { hb_face_destroy(subset_face) };
    unsafe { hb_subset_input_destroy(input) };
    unsafe { hb_face_destroy(face) };

    fs::write(output_font_file, result).unwrap();
```

🙏 I purposely access <code>result</code> last, after freeing all 
<code>HarfBuzz</code>-allocated memory. This ensures that the call to 
<code>slice.to_vec()</code> produces memory owned by Rust, rather than still 
managed by <code>HarfBuzz</code>.

🐧 On Ubuntu, all required libraries are globally recognized. 🪟 On Windows, I haven’t added the paths for <code>harfbuzz.dll</code>, <code>harfbuzz-subset.dll</code>, and their dependencies to the <code>PATH</code> environment variable. So in each new Windows terminal session, I run the following once:

```
set PATH=C:\PF\harfbuzz\build\src\;%PATH%
set PATH=C:\PF\vcpkg\installed\x64-windows\bin\;%PATH%
```

After that, <code>cargo run</code> works as expected.

Viewing <code>win_subset.ttf</code> and <code>linux_subset.ttf</code> in 
<a href="#win-install-birdfont">BirdFont</a> should show the same results as 
the font subset files created by the <a href="#hb-subset"><code>hb-subset</code></a>
CLI.

💡 <strong>Subset Using Glyph IDs</strong>

For an illustration of how to subset using glyph IDs, please refer to 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/harfbuzz_font_subset/src/main_glyph.rs" 
title="The harfbuzz_font_subset/src/main.rs module" target="_blank">
<code>harfbuzz_font_subset/src/main_glyph.rs</code></a> — rename it to 
<code>main.rs</code> to build and run. It uses the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/harfbuzz_font_subset/src/glyph.rs" 
title="The harfbuzz_font_subset/src/main.rs module" target="_blank">
<code>harfbuzz_font_subset/src/glyph.rs</code></a> module.

<a id="other-crates"></a>
❼ <strong>Other Crates</strong>

I’m aware of other Rust crates related to <code>HarfBuzz</code>, notably the 
<a href="https://crates.io/crates/hb-subset" title="Crate hb-subset" 
target="_blank">hb-subset</a> crate. In fact, my initial attempt at subsetting 
was through this crate. However, it is outdated, so I chose the FFI route rather than 
patching the crate.

<a id="concluding-remarks"></a>
❽ <strong>What’s Next</strong>

That wraps up the font subsetting illustration process. There are still more than 1,300 
warnings, but I’m not too worried about them. In the next instalment, we’ll extend 
the code in the 
<a href="https://github.com/behai-nguyen/polyglot_pdf/blob/main/harfbuzz_font_subset/src/main.rs" 
title="The harfbuzz_font_subset/src/main.rs module" target="_blank"><code>
harfbuzz_font_subset/src/main.rs</code></a> module into a generic function:

```rust
pub fn get_font_subset(input_font_file: &str, 
    face_index: u32, 
    text: &str
) -> Result<Vec<u8>, String>
```

to perform font subsetting generically, as part of a polyglot (multilingual) PDF creation 
workflow using the 
<a href="https://crates.io/crates/lopdf" title="Crate lopdf" target="_blank">lopdf</a> crate.

Thanks for reading! I hope this post helps others on the same journey.  
As always—stay curious, stay safe 🦊

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
<a href="https://www.rust-lang.org/" target="_blank">https://www.rust-lang.org/</a>
</li>
<li>
<a href="https://www.pngitem.com/download/ibmJoR_rust-language-hd-png-download/" target="_blank">https://www.pngitem.com/download/ibmJoR_rust-language-hd-png-download/</a>
</li>
<li>
<a href="https://ur.wikipedia.org/wiki/%D9%81%D8%A7%D8%A6%D9%84:HarfBuzz.svg" target="_blank">https://ur.wikipedia.org/wiki/%D9%81%D8%A7%D8%A6%D9%84:HarfBuzz.svg</a>
</li>
</ul>

<h3>
🦀 <a href="https://github.com/behai-nguyen/polyglot_pdf" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>
