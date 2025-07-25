---
layout: post
title: "rlox: A Rust Implementation of “Crafting Interpreters” – Control Flow"

description: This is Chapter 9&#58; Control Flow. The following additional statements and expressions have been implemented&#58; Stmt&#58;&#58;If, Expr&#58;&#58;Logical, and Stmt&#58;&#58;While. Lox now supports if, else, and, or, while, and for. Despite this long list of new features, the implementation remains fairly straightforward. 

tags: 
- Rust
- Compiler
- Interpreter
- Scanner
- Parser
- Evaluate
- Expressions
- Variables
- Assignment
- Scope
- if
- else
- and
- or
- while
- for
---

<em>
This is Chapter 9: <a href="https://craftinginterpreters.com/control-flow.html" title="Control Flow" target="_blank">Control Flow</a>. The following additional statements and expressions have been implemented: <code>Stmt::If</code>, <code>Expr::Logical</code>, and <code>Stmt::While</code>. Lox now supports <code>if</code>, <code>else</code>, <code>and</code>, <code>or</code>, <code>while</code>, and <code>for</code>. Despite this long list of new features, the implementation remains fairly straightforward.
</em>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rlox" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![145-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/07/145-feature-image.png) |
|:--:|
| *rlox: A Rust Implementation of “Crafting Interpreters” – Control Flow* |

<a id="repository-cloning"></a>
🚀 <strong>Note:</strong> You can download the code for this post from GitHub using:

```
git clone -b v0.4.0 https://github.com/behai-nguyen/rlox.git
```

<a id="running-the-current-cli"></a>
❶ <strong>Running the CLI Application</strong>

💥 The interactive mode is still available. However, valid expressions—such as 
<code>((4.5 / 2) * 2) == 4.50;</code>—currently produce no output. 
I'm unsure when interactive mode will be fully restored, and it's not a current priority.

For now, Lox scripts can be executed via the CLI application. For example:

```
cargo run --release ./tests/data/for/book_end_section.lox
```

```
Content of book_end_section.lox:
```

```
var a = 0;
var temp;

for (var b = 1; a < 10000; b = temp + b) {
  print a;
  temp = a;
  a = b;
}
```

This Lox script is at the end of the 
<a href="https://craftinginterpreters.com/control-flow.html#for-loops" 
title="For Loops" target="_blank">For Loops</a> section: it prints the first 21 
Fibonacci numbers.

For more details, refer to 
<a href="https://github.com/behai-nguyen/rlox/blob/main/README.md#to-run" 
title="README.md | To Run" target="_blank">this section</a> of the 
<code>README.md</code>.

<a id="repository-layout"></a>
❷ <strong>Updated Repository Layout</strong>

<strong>Legend</strong>: <span style="font-size:1.5em;">★</span> = updated, <span style="font-size:1.5em;">☆</span> = new.

💥 Files not modified are omitted for brevity.

```
.
├── docs
│   └── RLoxGuide.md ★
├── README.md ★
├── src
│   ├── ast_printer.rs ★
│   ├── interpreter.rs ★
│   ├── parser.rs ★
│   └── stmt.rs ★
├── tests
│   ├── data/ ☆ ➜ added more
│   ├── test_control_flow.rs ☆
│   └── test_parser.rs ★
└── tool
    └── generate_ast
        └── src
            └── main.rs ★
```

<a id="bug-fixed-stmt"></a>
❸ <strong>Bug Fix: <code>Stmt::If</code> Struct</strong>

In <a href="https://github.com/behai-nguyen/rlox/blob/d6f86f02c0dc0879b0071291ae5be1d06bdd2b07/src/stmt.rs" 
title="src/stmt.rs" target="_blank">stmt.rs</a>, the <code>struct If</code>
field <code>then_branch</code> was updated to <code>Box&lt;Stmt&gt;</code>: this branch is always present in an <code>if</code> statement. Consequently, the <code>new()</code> constructor was refactored. This is the updated <a href="https://github.com/behai-nguyen/rlox/blob/main/src/stmt.rs#L114-L130" 
title="src/stmt.rs" target="_blank">stmt.rs</a> module. Fixing the earlier bug also led to minor refactoring in the CLI generation tool. See 
<a href="https://github.com/behai-nguyen/rlox/blob/main/tool/generate_ast/src/main.rs#L101-L113" 
title="the tool/generate_ast/src/main.rs module" 
target="_blank">tool/generate_ast/src/main.rs</a>.

<a id="updated-parser-interpreter"></a>
❹ <strong><code>Parser</code> and <code>Interpreter</code> Updates</strong>

The new code is relatively straightforward. The Rust version closely mirrors the Java version.

<ol>
<li style="margin-top:10px;">
In the 
<a href="https://github.com/behai-nguyen/rlox/blob/d6f86f02c0dc0879b0071291ae5be1d06bdd2b07/src/parser.rs" 
title="the src/parser.rs module" target="_blank">src/parser.rs</a> module, 
the following methods were added:

<ul>
<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/d6f86f02c0dc0879b0071291ae5be1d06bdd2b07/src/parser.rs#L241-L255" 
title="the src/parser.rs module if_statement() method" target="_blank">if_statement()</a>
</li>

<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/d6f86f02c0dc0879b0071291ae5be1d06bdd2b07/src/parser.rs#L173-L183" 
title="the src/parser.rs module and() method" target="_blank">and()</a>
</li>

<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/d6f86f02c0dc0879b0071291ae5be1d06bdd2b07/src/parser.rs#L185-L195" 
title="the src/parser.rs module or() method" target="_blank">or()</a>
</li>

<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/d6f86f02c0dc0879b0071291ae5be1d06bdd2b07/src/parser.rs#L278-L285" 
title="the src/parser.rs module while_statement() method" target="_blank">while_statement()</a>
</li>

<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/d6f86f02c0dc0879b0071291ae5be1d06bdd2b07/src/parser.rs#L287-L331" 
title="the src/parser.rs module for_statement() method" target="_blank">for_statement()</a>
</li>
</ul>

The following methods were updated:

<ul>
<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/d6f86f02c0dc0879b0071291ae5be1d06bdd2b07/src/parser.rs#L381-L395" 
title="the src/parser.rs module statement() method" target="_blank">statement()</a>
</li>

<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/d6f86f02c0dc0879b0071291ae5be1d06bdd2b07/src/parser.rs#L360-L379" 
title="the src/parser.rs module assignment() method" target="_blank">assignment()</a>
</li>
</ul>

</li>

<li style="margin-top:10px;">
In the 
<a href="https://github.com/behai-nguyen/rlox/blob/d6f86f02c0dc0879b0071291ae5be1d06bdd2b07/src/interpreter.rs" 
title="the src/interpreter.rs module" target="_blank">src/interpreter.rs</a> 
module, the following methods were added:

<ul>
<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/d6f86f02c0dc0879b0071291ae5be1d06bdd2b07/src/interpreter.rs#L283-L292" 
title="the src/interpreter.rs module visit_if_stmt() method" target="_blank">visit_if_stmt()</a> 
</li>

<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/d6f86f02c0dc0879b0071291ae5be1d06bdd2b07/src/interpreter.rs#L218-L226" 
title="the src/interpreter.rs module visit_logical_expr() method" target="_blank">visit_logical_expr()</a> 
</li>

<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/d6f86f02c0dc0879b0071291ae5be1d06bdd2b07/src/interpreter.rs#L321-L328" 
title="the src/interpreter.rs module visit_while_stmt() method" target="_blank">visit_while_stmt()</a> 
</li>
</ul>

<p>
Note: <code>for</code> loops are desugared into <code>while</code> loops, so no separate code for <code>for</code> loops was added to the <code>Interpreter</code>.
</p>
</li>
</ol>

<a id="new-and-updated-tests"></a>
❺ <strong>New and Updated Tests</strong>

Additional tests based on the author's 
<a href="https://github.com/munificent/craftinginterpreters/tree/master/test/" 
title="Crafting Interpreters test scripts" target="_blank">test scripts</a> 
were incorporated:

<ol>
<li style="margin-top:10px;">
A new 
<a href="https://github.com/behai-nguyen/rlox/blob/d6f86f02c0dc0879b0071291ae5be1d06bdd2b07/tests/test_control_flow.rs" 
title="the tests/test_control_flow.rs module" target="_blank">tests/test_control_flow.rs</a> 
module was added.
</li>

<li style="margin-top:10px;">
The existing 
<a href="https://github.com/behai-nguyen/rlox/blob/d6f86f02c0dc0879b0071291ae5be1d06bdd2b07/tests/test_parser.rs" 
title="the tests/test_parser.rs module" target="_blank">tests/test_parser.rs</a> 
module was updated with 
<a href="https://github.com/behai-nguyen/rlox/blob/d6f86f02c0dc0879b0071291ae5be1d06bdd2b07/tests/test_parser.rs#L298-L344" 
title="the new test methods" target="_blank">three new test methods</a>.
</li>
</ol>

<a id="concluding-remarks"></a>
❻ <strong>What’s Next</strong>

That wraps up this post. There are still some warnings about dead code—which I’m okay with for now.

Thanks for reading! I hope this post supports others on the same journey. As always—stay curious, stay safe 🦊

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
