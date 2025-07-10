---
layout: post
title: "rlox: A Rust Implementation of “Crafting Interpreters” – Abstract Syntax Tree (AST) – Representing Code"

description: The primary focus of this post is Chapter 5&#58; Representing Code, in which the author introduces an independent tool to generate ASTs for both expressions and statements, followed by a printer for displaying the AST. This post briefly discusses my Rust implementation of both tools. 

tags: 
- Rust
- Compiler
- Interpreter
- Scanner
- Abstract Syntax Tree
- AST
---

<em>
The primary focus of this post is Chapter 5: <a href="https://craftinginterpreters.com/representing-code.html" title="Representing Code" target="_blank">Representing Code</a>, in which the author introduces an independent tool to generate ASTs for both expressions and statements, followed by a printer for displaying the AST. This post briefly discusses my Rust implementation of both tools.
</em>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rlox" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![142-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/07/142-feature-image.png) |
|:--:|
| *rlox: A Rust Implementation of “Crafting Interpreters” – Abstract Syntax Tree (AST) – Representing Code* |

I’ve already completed Chapter 6, 
<a href="https://craftinginterpreters.com/parsing-expressions.html" 
title="Parsing Expressions" target="_blank">Parsing Expressions</a>. 
While working on that chapter, I discovered my earlier implementation of the Rust scanner wasn’t fully correct, so I made several changes. Let’s cover those first.

<a id="repository-cloning"></a>
🚀 <strong>Please note,</strong> code for this post can be downloaded from GitHub with:

```
git clone -b v0.1.1 https://github.com/behai-nguyen/rlox.git
```

<a id="scanner-factoring"></a>
❶ <strong>Scanner Refactoring</strong>

⓵ <strong>Using the <code>Token::literal</code> Field</strong>

In the previous revision, I didn’t fully understand the purpose of this field as defined in 
<a href="https://github.com/behai-nguyen/rlox/blob/9447de676e709a100ef05af5d48c7bf9d6598b15/src/token.rs#L13-L15" 
title="src/token.rs" target="_blank">src/token.rs</a>. 
I’ve since refactored the code to properly store literal values in this field. The main changes are:

<ol>
<li style="margin-top:10px;">
Enums <code>TokenType::String</code> and <code>TokenType::Number</code> no longer carry variants.
<a href="https://github.com/behai-nguyen/rlox/blob/a4abe5c35e7f075ecf6eed00d458113054b6d5cf/src/token_type.rs#L35-L36" 
title="src/token_type.rs" target="_blank">Reference</a>.
</li>

<li style="margin-top:10px;">
Introduced a new <code>LiteralValue</code> 
enum to represent the literal types supported by Lox. This is now used for <code>Token::literal</code>. 
<a href="https://github.com/behai-nguyen/rlox/blob/a4abe5c35e7f075ecf6eed00d458113054b6d5cf/src/token.rs#L10-L22" 
title="src/token.rs" target="_blank">Reference</a>.
</li>

<li style="margin-top:10px;">
Literal values are now assigned correctly in the 
<a href="https://github.com/behai-nguyen/rlox/blob/a4abe5c35e7f075ecf6eed00d458113054b6d5cf/src/scanner.rs#L166-L167" 
title="src/scanner.rs number() method" target="_blank">number()</a> and 
<a href="https://github.com/behai-nguyen/rlox/blob/a4abe5c35e7f075ecf6eed00d458113054b6d5cf/src/scanner.rs#L124-L125" 
title="src/scanner.rs string() method" target="_blank">string()</a> methods.
</li>
</ol>

⓶ <strong>Normalising Number Literals</strong>

Lox only supports floating-point numbers. The scanner has been updated to normalise 
numeric input to <code>f64</code>, appending <code>.0</code> where needed. 
<a href="https://github.com/behai-nguyen/rlox/blob/a4abe5c35e7f075ecf6eed00d458113054b6d5cf/src/scanner.rs#L149-L154" 
title="src/scanner.rs number() method" target="_blank">See this logic</a>.

⓷ <strong>Other Refactorings</strong>

This includes improved code annotations and method renaming 
(e.g., <code>match_()</code> is now <code>`match_char()</code>`). 
<a href="https://github.com/behai-nguyen/rlox/blob/a4abe5c35e7f075ecf6eed00d458113054b6d5cf/src/scanner.rs#L51" 
title="src/scanner.rs match_char() method" target="_blank">Reference</a>.

⓸ <strong>Updated Scanner Tests</strong>

All tests in 
<a href="https://github.com/behai-nguyen/rlox/blob/a4abe5c35e7f075ecf6eed00d458113054b6d5cf/tests/test_scanner.rs"
title="tests/test_scanner.rs" target="_blank">tests/test_scanner.rs</a> 
now validate <code>Token::literal</code> values.

<a id="repository-layout"></a>
❷ <strong>Updated Repository Layout</strong>

<strong>Legend</strong>: <span style="font-size:1.5em;">★</span> = updated, <span style="font-size:1.5em;">☆</span> = new.

```
.
├── Cargo.toml
├── README.md ★
├── src
│   ├── ast_printer.rs ☆
│   ├── expr.rs ☆
│   ├── lib.rs ★
│   ├── lox_error.rs
│   ├── main.rs ★
│   ├── scanner_index.rs
│   ├── scanner.rs ★
│   ├── stmt.rs ☆
│   ├── token.rs ★
│   └── token_type.rs ★
├── tests
│   ├── data/ -- unchanged.
│   ├── test_common.rs ★
│   └── test_scanner.rs ★
└── tool ☆
    └── generate_ast
        ├── Cargo.toml
        └── src
            └── main.rs
```

<a id="generate-ast"></a>
❸ <strong>Generate AST Tool</strong>

This tool generates the modules 
<a href="https://github.com/behai-nguyen/rlox/blob/a4abe5c35e7f075ecf6eed00d458113054b6d5cf/src/expr.rs" 
title="src/expr.rs" target="_blank">expr.rs</a> and 
<a href="https://github.com/behai-nguyen/rlox/blob/a4abe5c35e7f075ecf6eed00d458113054b6d5cf/src/stmt.rs" 
title="src/stmt.rs" target="_blank">stmt.rs</a>, 
both based on the 
<a href="https://en.wikipedia.org/wiki/Visitor_pattern" 
title="Wikipedia: Visitor pattern" target="_blank">Visitor Pattern</a>.
For a Rust-specific take on this pattern, check out my write-up: 
<a href="https://behainguyen.wordpress.com/2025/06/28/visitor-pattern-with-rust/" 
title="Visitor Pattern with Rust" target="_blank">Visitor Pattern with Rust</a>.

The tool is fully self-contained and uses only standard Rust libraries. 
My implementation closely follows 
<a href="https://github.com/munificent/craftinginterpreters/blob/master/java/com/craftinginterpreters/tool/GenerateAst.java"
title="tool/GenerateAst.java" target="_blank">tool/GenerateAst.java</a> 
from the author’s GitHub repo. Since Rust differs significantly from Java, the Rust version is naturally longer and includes Rust-specific adjustments, which I’ve clearly annotated in the code.

To run the generator:

```
▶️Windows: > cargo run C:\xxxxx\behai
▶️Ubuntu: $ cargo run /home/behai/tmp
```

<strong>Sample output:</strong>

| ![142-01.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/07/142-01.png) |
|:--:|
| *Execution Screenshot* |

| ![142-02.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/07/142-02.png) |
|:--:|
| *Generated Files* |

The generated modules compile successfully, all tests pass, and the parser works correctly. That said, I’m prepared to revisit and refactor this tool as future chapters uncover new requirements.

<a id="ast-printer"></a>
❹ <strong>AST Printer</strong>

Following the same pattern, I implemented a complete printer based on the author’s 
<a href="https://github.com/munificent/craftinginterpreters/blob/master/java/com/craftinginterpreters/lox/AstPrinter.java"
title="lox/AstPrinter.java" target="_blank">lox/AstPrinter.java</a>. 
My version doesn’t have a standalone <code>main</code> function, but I’ve adapted the book’s example 
into a unit test. Like the AST generator, I may revisit this module as I progress—mainly to fix bugs or correct misunderstandings that emerge while integrating it into later chapters.

<a id="concluding-remarks"></a>
❺ <strong>What’s Next</strong>

Though <a href="https://craftinginterpreters.com/parsing-expressions.html" 
title="Parsing Expressions" target="_blank">Chapter 6</a> is already complete, I’ll hold off discussing it in detail until I’ve finished Chapter 7. I believe that will allow for a more insightful and connected explanation of how expression parsing integrates with statement parsing and evaluation.

You might notice some warnings about dead code—these are expected, as some generated types and methods will only be used in future chapters. I’m happy to ignore them for now.

Thank you for reading! I hope this post helps others following the same journey. As always—stay curious, stay safe 🦊

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
