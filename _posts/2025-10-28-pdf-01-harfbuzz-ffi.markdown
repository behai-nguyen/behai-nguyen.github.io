---
layout: post
title: "Rust FFI “Adventure” with the HarfBuzz Text Shaping Engine"

description: Rust FFI, or Foreign Function Interface, is a mechanism that allows Rust code to interact with programs written in other languages, such as C and C-compatible languages. The HarfBuzz text shaping engine is written in C++. In this article, we describe how to build the HarfBuzz text shaping engine on both Windows and Ubuntu. We then demonstrate how to write simple Rust code that calls the hb_version_string() function from HarfBuzz using FFI.

tags:
- Rust
- FFI
- HarfBuzz
- hb-shape
- hb-subset
---

*Rust FFI, or <a href="https://doc.rust-lang.org/nomicon/ffi.html" title="Foreign Function Interface" target="_blank">Foreign Function Interface</a>, is a mechanism that allows Rust code to interact with programs written in other languages, such as C and C-compatible languages. The <a href="https://en.wikipedia.org/wiki/HarfBuzz" title="HarfBuzz" target="_blank">HarfBuzz</a> text shaping engine is written in C++.*

*In this article, we describe how to build the <code>HarfBuzz</code> text shaping engine on both Windows and Ubuntu. We then demonstrate how to write simple Rust code that calls the <code>hb_version_string()</code> function from <code>HarfBuzz</code> using FFI.*

<h3>
🦀 <a href="https://github.com/behai-nguyen/polyglot_pdf" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![151-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/10/151-feature-image.png) |
|:--:|
| *Rust FFI “Adventure” with the HarfBuzz Text Shaping Engine* |

I should mention that this article wasn’t the one I originally set out to write. I had been working on font subsetting, and midway through, I decided to change the location of the <code>HarfBuzz</code> build on Windows. That build was successfully completed around 02 October 2025, and my Rust font subsetting code was working on both Windows and Ubuntu. However, after making the change on 20 October 2025, the Rust subsetting code stopped working on Windows, and I haven’t been able to get it running again yet.

Since I’m not yet familiar with <code>HarfBuzz</code> and FFI, I decided to scale back the scope of my documentation and focus instead on the build process and a simple example of FFI. This article isn’t a tutorial—it's a personal record of my exploration into the subject.

💡 Most of the steps were guided by ChatGPT and Copilot. It took several iterations to get everything installed correctly and to get the Rust code working. AI-generated instructions sometimes assume the presence of certain tools or prior knowledge, which I didn’t always have. I also had to do my own reading to fully understand and apply the instructions.

<a id="installation-on-win"></a>
❶ <strong>Windows: Install Build Tools and the HarfBuzz Text Shaping Engine</strong>

There are several viable methods for building <code>HarfBuzz</code> on Windows, all of which require external build tools. Depending on the features we want our built version of <code>HarfBuzz</code> to support, we may also need to build or install additional libraries. I encountered several failed attempts during this process—it can be quite intimidating. That’s the main reason I decided to document it in this article.

<a id="win-install-meson"></a>
⓵ <strong>Install the <a href="https://mesonbuild.com/Getting-meson.html" 
title="The Meson Build Tool" target="_blank">Meson Build Tool</a></strong>

Follow the instructions in the <a href="https://mesonbuild.com/Getting-meson.html#installing-meson-and-ninja-with-the-msi-installer" 
title="Installing Meson and Ninja with the MSI installer" target="_blank">Installing Meson and Ninja with the MSI installer</a> section. Download <code>meson-1.9.1-64.msi</code> from the <a href="https://github.com/mesonbuild/meson/releases" 
title="GitHub Meson Build Releases" target="_blank">Meson releases page on GitHub</a>.

I installed it to <code>C:\Program Files\Meson\</code>. During installation, you may see warnings about updating files used by other applications, and a system restart may be required. The installation path is added to the system environment automatically, and the <code>meson</code> and <code>ninja</code> command-line tools become globally available.

<a id="win-install-llvm"></a>
⓶ <strong>Install <a href="https://en.wikipedia.org/wiki/LLVM" title="LLVM" target="_blank">LLVM</a></strong>

<code>LLVM</code> is a collection of compiler and toolchain technologies. For more information, see 
<a href="https://llvm.org/" title="The LLVM Compiler Infrastructure" target="_blank">
The LLVM Compiler Infrastructure</a> and the 
<a href="https://en.wikipedia.org/wiki/LLVM" title="LLVM" target="_blank">Wikipedia article on LLVM</a>.

We’ll be using the <a href="https://docs.rs/bindgen/latest/bindgen/" title="Crate bindgen" 
target="_blank">bindgen</a> crate to generate Rust bindings for the <code>HarfBuzz</code> 
library. This crate requires the <code>LLVM</code> toolchain to function.

Download the latest installer from the 
<a href="https://github.com/llvm/llvm-project/releases" title="LLVM GitHub Repository" 
target="_blank">LLVM GitHub releases page</a>, and run it. I downloaded 
<code>LLVM-21.1.2-win64.exe</code>. During installation, select the option 
<code>Add LLVM to the system PATH for all users</code>, and accept the default 
installation directory <code>C:\Program Files\LLVM</code>.

💡 <strong>Important</strong> 💥 The following steps rely on an up-to-date installation of 
<strong><code>Visual Studio 2022</code></strong> on Windows. I haven’t tested this with later versions of 
<code>Visual Studio</code>, so I can’t comment on compatibility beyond 2022.

To access the 64-bit <code>Developer Command Prompt for Visual Studio 2022</code> (or for your installed version), 
open a <code>Windows Terminal</code> session, launch a new <code>Command Prompt</code>, and run the following batch file:

```
"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
```

You should see output similar to the following—note the <code>x64</code> architecture:

```
**********************************************************************
** Visual Studio 2022 Developer Command Prompt v17.14.18
** Copyright (c) 2025 Microsoft Corporation
**********************************************************************
[vcvarsall.bat] Environment initialized for: 'x64'
```

Running <code>where cl.exe</code>, <code>where cmake.exe</code>, and 
<code>where dumpbin.exe</code> should report the following paths:

<ol>
<li style="margin-top:10px;">
<code>C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\bin\Hostx64\x64\cl.exe</code>
</li>
<li style="margin-top:10px;">
<code>C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe</code>
</li>
<li style="margin-top:10px;">
<code>C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\bin\Hostx64\x64\dumpbin.exe</code>
</li>
</ol>	

While the paths for <code>cl.exe</code> and <code>dumpbin.exe</code> clearly indicate <code>x64</code>, 
the directory for <code>cmake.exe</code> does not. To confirm that <code>cmake.exe</code> is also a 64-bit CLI, 
run the following command:

```
dumpbin /headers "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe" | find "machine"
```

The output should include <code>8664 machine (x64)</code>, confirming that it is a 64-bit executable.

<a id="win-install-vcpkg"></a>
⓷ <strong>Install <code>vcpkg</code></strong>

<code>vcpkg</code> is a C/C++ dependency manager from Microsoft that supports all platforms, build systems, and workflows. References:

<ol>
<li style="margin-top:10px;">
<a href="https://vcpkg.io/en/" title="vcpkg" target="_blank">https://vcpkg.io/en/</a>
</li>
<li style="margin-top:10px;">
<a href="https://github.com/microsoft/vcpkg" title="vcpkg GitHub repository" target="_blank">https://github.com/microsoft/vcpkg</a>
</li>
</ol>

I followed this Microsoft article: 
<a href="https://learn.microsoft.com/en-us/vcpkg/get_started/get-started?pivots=shell-powershell" 
title="Tutorial: Install and use packages with CMake" target="_blank">Tutorial: Install and use packages with CMake</a> 
to install <code>vcpkg</code> to <code>C:\PF\</code>. After changing to the <code>C:\PF\</code> directory, run the following command:

```
git clone https://github.com/microsoft/vcpkg.git
```

This repository is approximately 118MB in size. Then:

```
cd vcpkg
```

The current working directory should now be <code>C:\PF\vcpkg\</code>. Then run:

```
.\bootstrap-vcpkg.bat
```

<a id="win-install-freetype"></a>
⓸ <strong>Install the FreeType Text Rendering Engine</strong>

References:

<ul>
<li style="margin-top:10px;">
<a href="https://freetype.org/" title="The FreeType Project" target="_blank">The FreeType Project</a>
</li>
<li style="margin-top:10px;">
<a href="https://en.wikipedia.org/wiki/FreeType" title="FreeType on Wikipedia" target="_blank">FreeType on Wikipedia</a>
</li>
</ul>

This is a system-wide installation. Change to the <code>C:\PF\vcpkg\</code> directory, then run the following command:

```
vcpkg install freetype:x64-windows
```

The installation may take several minutes and produce a long output. I was able to install it successfully on the first attempt. After installation, you should see the following:

<ul>
<li style="margin-top:10px;">
<code>C:\PF\vcpkg\installed\x64-windows\include\freetype</code>
</li>
<li style="margin-top:10px;">
<code>C:\PF\vcpkg\installed\x64-windows\lib\freetype.lib</code>
</li>
<li style="margin-top:10px;">
<code>C:\PF\vcpkg\buildtrees\freetype\x64-windows-rel\freetype.dll</code>
</li>
</ul>

To confirm that <code>freetype.dll</code> is a 64-bit binary, run:

```
dumpbin /headers "C:\PF\vcpkg\buildtrees\freetype\x64-windows-rel\freetype.dll" | find "machine"
```

The output should include <code>8664 machine (x64)</code>.

<a id="win-install-pkgconf"></a>
⓹ <strong>Install <code>pkgconf</code> into the <a href="#win-install-vcpkg">vcpkg</a> Tree</strong>

Reference: <a href="https://vcpkgx.com/details.html?package=pkgconf" 
title="vcpkgx" target="_blank">https://vcpkgx.com/details.html?package=pkgconf</a>. 
The <a href="#win-install-meson">Meson</a> build tool requires this utility to locate the 
<a href="#win-install-freetype">FreeType</a> library.

Change to the <code>C:\PF\vcpkg\</code> directory, then run the following command:

```
vcpkg install pkgconf:x64-windows
```

The installation should complete quickly. Afterward, you should see the following:

<ul>
<li style="margin-top:10px;">
<code>C:\PF\vcpkg\installed\x64-windows\tools\pkgconf\pkgconf.exe</code>: 
This is a 64-bit CLI. You can verify its architecture using <code>dumpbin</code>.
</li>
<li style="margin-top:10px;">
<code>C:\PF\vcpkg\installed\x64-windows\lib\pkgconfig\freetype2.pc</code>
</li>
</ul>

To confirm that <code>pkgconf</code> can detect the FreeType version, run the following command:

```
set PKG_CONFIG_PATH=C:\PF\vcpkg\installed\x64-windows\lib\pkgconfig
C:\PF\vcpkg\installed\x64-windows\tools\pkgconf\pkgconf.exe --modversion freetype2
```

This should report <code>26.2.20</code>.

<a id="win-install-glib"></a>
⓺ <strong>Install the <code>GLib</code> Library</strong>

References:

<ul>
<li style="margin-top:10px;">
<a href="https://docs.gtk.org/glib/" title="GLib" target="_blank">https://docs.gtk.org/glib/</a>
</li>
<li style="margin-top:10px;">
<a href="https://harfbuzz.github.io/integration.html#integration-glib" 
title="GNOME integration, GLib, and GObject" target="_blank">Harfbuzz GLib Integration</a>
</li>
<li style="margin-top:10px;">
<a href="https://en.wikipedia.org/wiki/GLib" title="GLib on Wikipedia" target="_blank">GLib on Wikipedia</a>
</li>
</ul>

Change to the <code>C:\PF\vcpkg\</code> directory and run the following command:

```
vcpkg install glib:x64-windows
```

On my <code>Intel(R) Core(TM) i7-7700 CPU @ 3.6GHz</code> with 16GB RAM, 4 cores, and 8 logical processors, 
the installation took 44 minutes to complete.

While still in the <code>C:\PF\vcpkg\</code> directory, run the following command:

```
dir /s *glib*.dll
```

I counted 8 copies across 8 different subdirectories. I'm not entirely sure which one is used by the 
<a href="#win-install-harfbuzz">HarfBuzz build (install) process</a>.

<a id="win-install-harfbuzz"></a>
⓻ <strong>Build (Install) the HarfBuzz Text Shaping Engine</strong>

References:

<ul>
<li style="margin-top:10px;">
<a href="https://github.com/harfbuzz/harfbuzz" title="The HarfBuzz text shaping engine" target="_blank">GitHub repository</a>
</li>
<li style="margin-top:10px;">
<a href="https://en.wikipedia.org/wiki/HarfBuzz" title="HarfBuzz" target="_blank">HarfBuzz on Wikipedia</a>
</li>
</ul>

Change to the <code>C:\PF\</code> directory and clone the <code>HarfBuzz</code> repository:

```
git clone https://github.com/harfbuzz/harfbuzz.git
```

The repository is approximately 206MB. I encountered several failed builds—meaning the Rust code didn’t compile correctly. The command sequence below is what worked for me:

```
cd harfbuzz
```

Now in the <code>C:\PF\harfbuzz\</code> directory, run the following commands:

```
set PKG_CONFIG=C:\PF\vcpkg\installed\x64-windows\tools\pkgconf\pkgconf.exe
set PKG_CONFIG_PATH=C:\PF\vcpkg\installed\x64-windows\lib\pkgconfig
meson setup build --wipe --buildtype=release -Ddefault_library=shared -Dfreetype=enabled -Dglib=enabled -Dutilities=enabled
meson compile -C build
```

The last part of the <code>meson setup build...</code> command:

```
harfbuzz 12.1.0

  Directories
    prefix                    : c:/
    bindir                    : bin
    libdir                    : lib
    includedir                : include
    datadir                   : share
    cmakepackagedir           : lib/cmake

  Unicode callbacks (you want at least one)
    Builtin                   : YES
    Glib                      : YES
    ICU                       : NO

  Font callbacks (the more the merrier)
    Builtin                   : YES
    FreeType                  : YES
    Fontations                : NO

  Dependencies used for command-line utilities
    Cairo                     : NO
    Chafa                     : NO

  Additional shapers
    Graphite2                 : NO
    WebAssembly (experimental): NO

  Platform / other shapers (not normally needed)
    CoreText                  : NO
    DirectWrite               : NO
    GDI/Uniscribe             : NO
    HarfRust                  : NO
    kbts                      : NO

  Other features
    Utilities                 : YES
    Documentation             : NO
    GObject bindings          : YES
    Cairo integration         : NO
    Introspection             : NO
    Experimental APIs         : NO

  Testing
    Tests                     : YES
    Benchmark                 : NO

  User defined options
    buildtype                 : release
    default_library           : shared
    freetype                  : enabled
    glib                      : enabled
    utilities                 : enabled

Found ninja-1.12.1 at "C:\Program Files\Meson\ninja.EXE"
```

The output of the <code>meson compile -C build</code> command:

```
INFO: autodetecting backend as ninja
INFO: calculating backend command to run: "C:\Program Files\Meson\ninja.EXE" -C C:/PF/harfbuzz/build
ninja: Entering directory `C:/PF/harfbuzz/build'
[62/258] Linking target src/harfbuzz.dll
   Creating library src\harfbuzz.lib and object src\harfbuzz.exp
[83/258] Linking target src/harfbuzz-gobject.dll
   Creating library src\harfbuzz-gobject.lib and object src\harfbuzz-gobject.exp
[142/258] Compiling C object test/api/test-style.exe.p/test-style.c.obj
../test/api/test-style.c(175): warning C4305: 'function': truncation from 'double' to 'float'
[163/258] Compiling C object test/api/test-unicode.exe.p/test-unicode.c.obj
../test/api/test-unicode.c(614): warning C4068: unknown pragma 'GCC'
../test/api/test-unicode.c(615): warning C4068: unknown pragma 'GCC'
../test/api/test-unicode.c(623): warning C4068: unknown pragma 'GCC'
[166/258] Compiling C++ object test/fuzzing/hb-set-fuzzer.exe.p/hb-set-fuzzer.cc.obj
../test/fuzzing/hb-set-fuzzer.cc(49): warning C4068: unknown pragma 'GCC'
../test/fuzzing/hb-set-fuzzer.cc(50): warning C4068: unknown pragma 'GCC'
../test/fuzzing/hb-set-fuzzer.cc(52): warning C4068: unknown pragma 'GCC'
[207/258] Linking target src/harfbuzz-subset.dll
   Creating library src\harfbuzz-subset.lib and object src\harfbuzz-subset.exp
[258/258] Linking target test/threads/hb-subset-threads.exe
```

<a id="win-libs-clis"></a>
After a successful build, you should see the following files:

<ul>
<li style="margin-top:10px;">
<code>C:\PF\harfbuzz\build\src\harfbuzz.dll</code>
</li>
<li style="margin-top:10px;">
<code>C:\PF\harfbuzz\build\src\harfbuzz-subset.dll</code>
</li>
<li style="margin-top:10px;">
<code>C:\PF\harfbuzz\build\util\</code>: This directory should contain:

<ul>
<li style="margin-top:10px;">
<code>hb-info.exe</code>
</li>
<li style="margin-top:10px;">
<code>hb-info.exe.p</code>
</li>
<li style="margin-top:10px;">
<code>hb-shape.exe</code>
</li>
<li style="margin-top:10px;">
<code>hb-shape.exe.p</code>
</li>
<li style="margin-top:10px;">
<code>hb-subset.exe</code>
</li>
<li style="margin-top:10px;">
<code>hb-subset.exe.p</code>
</li>
</ul>
</li>
</ul>

To verify that these binaries are 64-bit, run the following commands. Each should report <code>8664 machine (x64)</code>:

```
dumpbin /headers C:\PF\harfbuzz\build\src\harfbuzz.dll | find "machine"
dumpbin /headers C:\PF\harfbuzz\build\src\harfbuzz-subset.dll | find "machine"
dumpbin /headers C:\PF\harfbuzz\build\util\hb-info.exe | find "machine"
dumpbin /headers C:\PF\harfbuzz\build\util\hb-shape.exe | find "machine"
dumpbin /headers C:\PF\harfbuzz\build\util\hb-subset.exe | find "machine"
```

<a id="installation-on-ubuntu"></a>
❷ <strong>Ubuntu: Install Build Tools and the HarfBuzz Text Shaping Engine</strong>

On Ubuntu, the process is surprisingly straightforward. The instructions provided by AI didn’t work out of the box. Based on those suggestions, I did some research and was able to get everything built and installed successfully on the fourth or fifth attempt.

I followed the instructions in this 
<a href="https://github.com/harfbuzz/harfbuzz/blob/main/BUILD.md" 
title="Building HarfBuzz" target="_blank">build guide</a>. Make sure to update your Ubuntu system if it’s outdated. Then install the required build tools with:

```
$ sudo apt-get install meson pkg-config ragel gtk-doc-tools gcc g++ libfreetype6-dev libglib2.0-dev libcairo2-dev
```

From the user home directory <code>/home/behai</code>, clone the <code>HarfBuzz</code> repository:

```
$ git clone https://github.com/harfbuzz/harfbuzz
```

Change into the newly created <code>harfbuzz/</code> subdirectory:

```
$ cd harfbuzz/
```

Now in <code>/home/behai/harfbuzz</code>, build <code>HarfBuzz</code> with:

```
$ meson build && ninja -C build && meson test -C build
```

At completion, <code>meson</code> reports the locations of the build log and the test log.

To install the build artifacts:

```
$ sudo meson install -C build
```

The output is lengthy, and at completion, it also reports the location of the installation log.

<a id="ubuntu-libs-clis"></a>
And that’s about it! You should now have the following:

<ul>
<li style="margin-top:10px;">
<code>/usr/local/lib/x86_64-linux-gnu/</code>, which contains:
<ul>
<li style="margin-top:10px;">
<code>libharfbuzz.so</code>: Equivalent to Windows <code>harfbuzz.dll</code>.
</li>
<li style="margin-top:10px;">
<code>libharfbuzz-subset.so</code>: Equivalent to Windows <code>harfbuzz-subset.dll</code>.
</li>
<li style="margin-top:10px;">
Other related shared libraries.
</li>
</ul>
</li>
<li style="margin-top:10px;">
<code>/usr/local/bin/</code>, which includes:
<ul>
<li style="margin-top:10px;">
<code>hb-info</code>
</li>
<li style="margin-top:10px;">
<code>hb-shape</code>
</li>
<li style="margin-top:10px;">
<code>hb-subset</code>
</li>
<li style="margin-top:10px;">
<code>hb-view</code>
</li>
</ul>
</li>
</ul>

<a id="rust-ffi"></a>
❸ <strong>A Rust FFI That Calls <code>HarfBuzz</code>'s 
<code>hb_version_string()</code> Function</strong>

💡 Please note: on both Windows and Ubuntu, I’m running Rust version 
<code>rustc 1.90.0 (1159e78c4 2025-09-14)</code>.

Since this is just an exploratory one-off project, I don’t plan to extend it further in future development—although future code will likely follow the same approach. I’ve placed the project under the <code>harfbuzz_ffi</code> directory. The structure is simple:

```
.
├── Cargo.toml
├── build.rs
└── src
    └── main.rs
```

Let’s list the contents of each file and walk through them.

```
Content of Cargo.toml:
```

```toml
[package]
name = "harfbuzz_ffi" 
version = "0.1.0"
edition = "2024"

[dependencies]
libc = "0.2.177"

[build-dependencies]
bindgen = "0.72.1"
```

Both <code>libc</code> and <code>bindgen</code> make Rust FFI possible. References:

<ul>
<li style="margin-top:10px;">
<a href="https://docs.rs/libc/latest/libc/"
title="Crate libc" target="_blank">libc crate</a>
</li>
<li style="margin-top:10px;">
<a href="https://rust-lang.github.io/rust-bindgen/introduction.html" 
title="The bindgen User Guide" target="_blank">The bindgen User Guide</a>
</li>
<li style="margin-top:10px;">
<a href="https://github.com/fitzgen/bindgen-tutorial-bzip2-sys" 
title="bindgen-tutorial-bzip2-sys" target="_blank">Bindgen Tutorial</a>, which links to this 
<a href="https://fitzgen.com/2016/12/14/using-libbindgen-in-build-rs.html" 
title="Generating Rust FFI Bindings to C/C++ Libraries at cargo build time in build.rs with bindgen" 
target="_blank">full tutorial</a>. I followed it in full.
</li>
<li style="margin-top:10px;">
<a href="https://docs.rs/bindgen/latest/bindgen/" title="Crate bindgen" target="_blank">bindgen crate</a>
</li>
</ul>

```
Content of build.rs:
```

```rust
use std::env;
use std::path::PathBuf;
use std::process::Command;

fn main() {
    // println!("cargo:rustc-link-lib=dylib=harfbuzz");
    // println!("cargo:rustc-link-lib=static=harfbuzz");
    println!("cargo:rustc-link-lib=harfbuzz");

    // C:\PF\harfbuzz\src\[*.h, hb.h]
    // /usr/local/include/harfbuzz/[*.h, hb.h]    
    // C:\PF\harfbuzz\build\src\harfbuzz.lib
    // /usr/local/lib/x86_64-linux-gnu/libharfbuzz.so.0
    let (hb_include, lib_search) = if cfg!(target_os = "windows") {
        (
            "C:/PF/harfbuzz/src/",
            "C:/PF/harfbuzz/build/src/",
        )        
    } else {
        (
            "/usr/local/include/harfbuzz/",
            "/usr/local/lib/x86_64-linux-gnu/",
        )
    };

    println!("cargo:rustc-link-search=native={}", lib_search);

    // Windows vs Linux include paths
    let mut clang_args = Vec::new();

    // Try to auto-detect GCC’s include path on Unix-like systems
    // Handle the problem:
    // /usr/local/include/harfbuzz/hb-common.h:68:10: fatal error: 'stddef.h' file not found
    if cfg!(not(target_os = "windows")) {
        if let Ok(output) = Command::new("gcc").arg("-print-file-name=include").output() {
            if output.status.success() {
                if let Ok(path) = String::from_utf8(output.stdout) {
                    let trimmed = path.trim();
                    clang_args.push(format!("-I{}", trimmed));
                }
            }
        }
    }

    // Add the HarfBuzz include and common system paths
    clang_args.push(format!("-I{}", hb_include));
    clang_args.push("-I/usr/include".to_string());

    let bindings = bindgen::Builder::default()
        .clang_args(clang_args)
        .header(format!("{}/hb.h", hb_include))        
        .generate()
        .expect("Unable to generate bindings");    

    let out_path = PathBuf::from(env::var("OUT_DIR").unwrap());
    bindings
        .write_to_file(out_path.join("bindings.rs"))
        .expect("Couldn't write bindings!");
}
```

Most of the <code>build.rs</code> logic is discussed in the tutorial above. 
Note that the <code>.clang_args()</code> call in 
<code>bindgen::Builder::default().clang_args([...])</code> requires 
<a href="#win-install-llvm">LLVM</a>.

```
Content of src/main.rs:
```

```rust
use std::ffi::CStr;

#[allow(non_camel_case_types, non_snake_case, non_upper_case_globals)]
mod hb {
    include!(concat!(env!("OUT_DIR"), "/bindings.rs"));
}

#[link(name = "harfbuzz")]
unsafe extern "C" {
    pub fn hb_version_string() -> *const std::os::raw::c_char;
}

fn main() {
    unsafe {
        let version_ptr = hb::hb_version_string();
        let version = CStr::from_ptr(version_ptr);
        println!("HarfBuzz version: {}", version.to_str().unwrap());
    }
}
```

<code>src/main.rs</code> is also covered in the tutorial mentioned above.

Please note that <code>cargo build</code> produces over 1,000 warnings, mostly related to mixed-case constant names. These can be suppressed, but it’s not necessary for this project.

On Ubuntu, all required libraries are globally recognized. On Windows, I haven’t added the paths for <code>harfbuzz.dll</code> and its dependencies to the <code>PATH</code> environment variable. So in each new Windows terminal session, I run the following once:

```
set PATH=C:\PF\harfbuzz\build\src\;%PATH%
set PATH=C:\PF\vcpkg\installed\x64-windows\bin\;%PATH%
```

After that, <code>cargo run</code> works as expected. The screenshots below show the result of running the Rust FFI code on both Windows and Ubuntu:

| ![151-windows-run.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/10/151-windows-run.png) |
|:--:|
| *Windows* |

| ![151-ubuntu-run.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/10/151-ubuntu-run.png) |
|:--:|
| *Ubuntu* |

<a id="concluding-remarks"></a>
❹ <strong>What’s Next</strong>

For me, it’s back to troubleshooting font subsetting on Windows. If I can’t resolve the issue, I’ll settle for calling the <code>hb-subset</code> CLI on both Windows and Ubuntu. Even though everything works fine on Ubuntu, I’d prefer a single, unified code path. I’ll document that process as well.

Thanks for reading! I hope this post helps others on a similar journey.  
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
