---
layout: post
title: "rlox: A Rust Implementation of “Crafting Interpreters” – Scanner"

description: I am attempting a Rust implementation of Robert Nystrom's Lox language discussed in Crafting Interpreters. This post describes my Rust code equivalence for the Scanning chapter.

tags: 
- Rust
- Compiler
- Interpreter
- Scanner
---

<em>
I am attempting a Rust implementation of Robert Nystrom's Lox language discussed in <a href="https://craftinginterpreters.com/" title="Crafting Interpreters" target="_blank">Crafting Interpreters</a>. This post describes my Rust code equivalence for the <a href="https://craftinginterpreters.com/scanning.html" title="Scanning" target="_blank">Scanning</a> chapter. 
</em>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rlox" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![139-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/06/139-feature-image.png) |
|:--:|
| *rlox: A Rust Implementation of “Crafting Interpreters” – Scanner* |

This is the long list of existing <a href="https://github.com/munificent/craftinginterpreters/wiki/Lox-Implementations#rust" title="Lox Implementations" target="_blank">Rust Lox Implementations</a>. I downloaded and ran the first two, but I did not have a look at the code. I would like to take on this project as a challenge. If I complete it, I want it to reflect my own independent effort.

<a id="repository-cloning"></a>
🚀 <strong>Please note,</strong> code for this post can be downloaded from GitHub with:

```
git clone -b v0.1.0 https://github.com/behai-nguyen/rlox.git
```

<a id="to-run"></a>
● To run interactively, first change to the <code>rlox/</code> directory, then run the following command:

```
$ cargo run
```

Enter something like <code>var str2 = "秋の終わり";</code>, and press <code>Enter</code> — you will see the tokens printed out. Please refer to the screenshot below for an illustration.

![139-01.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/06/139-01.png)

At the moment, inputs are processed independently, meaning each new input does not retain any connection to previous inputs.

To exit, simply press <code>Enter</code> without entering anything.

● To Run with a Lox script file, first change to the <code>rlox/</code> directory, then run the following command:

```
$ cargo run ./tests/data/scanning/numbers.lox
```

If there are no errors, you will see the tokens printed out.

<a id="to-test"></a>
● To run existing tests, first change to the <code>rlox/</code> directory, then run the following command: 

```
$ cargo test
```

<a id="repository-layout"></a>
❶ Repository Layout

```
.
├── Cargo.toml
├── README.md
├── src
│   ├── lib.rs
│   ├── lox_error.rs
│   ├── main.rs
│   ├── scanner_index.rs
│   ├── scanner.rs
│   ├── token.rs
│   └── token_type.rs
└── tests
    ├── data
    │   └── scanning
    │       ├── identifiers.lox
    │       ├── keywords.lox
    │       ├── numbers.lox
    │       ├── punctuators.lox
    │       ├── README.md
    │       ├── sample.lox
    │       ├── strings.lox
    │       ├── utf8_text.lox
    │       └── whitespace.lox
    ├── test_common.rs
    └── test_scanner.rs
```

<a id="code-annotation"></a>
❷ Let's briefly describe the project.

● Identifier names follow Rust convention. In the <a href="https://craftinginterpreters.com/scanning.html" title="Scanning" target="_blank">Scanning</a> chapter, method names such as <code>scanTokens()</code>, <code>peekNext()</code> are <code>scan_tokens()</code> and <code>peek_next()</code> in Rust respectively.

● Identifier names which are keywords in Rust will simply have an underscore (<code>_</code>) suffix appended. For example, <code>match()</code> becomes <code>match_()</code>, and <code>type</code> becomes <code>type_</code>.

● The <code>src/scanner_index.rs</code> module is not in the original Java version. It implements the Java variables <code>start</code>, <code>current</code>, <code>line</code> and some additional fields to support UTF-8 text scanning and slicing; please refer to <a href="https://behainguyen.wordpress.com/2025/06/09/rust-working-with-utf-8-text/" title="Rust: Working with UTF-8 Text" target="_blank">this post</a> for a full discussion on supporting UTF-8 text slicing.

● In the <code>src/token.rs</code> module, I am not sure if we need the <code>literal</code> field in the <code>Token</code> struct in the future. I leave it for the time being.

● 💥 In the <code>src/scanner.rs</code> module, the method <code>scan_tokens()</code> returns an array (vector) of <code>Token</code>; and the <code>run()</code> function in the <code>src/main.rs</code> module consumes this array and drops it. This array is local. In the Java implementation, it is a global class variable. This implementation might change in the future.

● The <code>src/lox_error.rs</code> module is also not in the original Java version. It implements a Rust specific error struct. 

● Under <code>tests/data/scanning/</code> directory, except for <code>utf8_text.lox</code> which is mine; the <code>README.md</code> lists the original addresses of all other test data files.

● The <code>tests/test_scanner.rs</code> module implements test for each of the test data files in the <code>tests/data/scanning/</code> directory.

<a id="concluding-remarks"></a>
❸ The above points are specific to this implementation, otherwise the code adhere to <a href="https://craftinginterpreters.com/" title="Crafting Interpreters" target="_blank">Crafting Interpreters</a>, chapter <a href="https://craftinginterpreters.com/scanning.html" title="Scanning" target="_blank">Scanning</a>. 

Thank you for reading. I hope you find this post helpful. Stay safe, as always.

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
<a href="https://craftinginterpreters.com/" target="_blank">https://craftinginterpreters.com/</a>
</li>
</ul>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rlox" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>
