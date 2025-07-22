---
layout: post
title: "rlox: A Rust Implementation of “Crafting Interpreters” – Global Variables, Assignment, and Scope"

description: I have completed Chapter 8&#58; Statements and State. The following additional statements and expressions have been implemented&#58; Stmt&#58;&#58;Expression, Stmt&#58;&#58;Print, Stmt&#58;&#58;Var, Expr&#58;&#58;Variable, Expr&#58;&#58;Assign and Stmt&#58;&#58;Block. We can now declare global variables, define scoped variables, and assign values to variables. This post discusses some implementation issues that deserve attention. 

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
---

<em>
I have completed Chapter 8: <a href="https://craftinginterpreters.com/statements-and-state.html" title="Statements and State" target="_blank">Statements and State</a>. The following additional statements and expressions have been implemented: <code>Stmt::Expression</code>, <code>Stmt::Print</code>, <code>Stmt::Var</code>, <code>Expr::Variable</code>, <code>Expr::Assign</code> and <code>Stmt::Block</code>. We can now declare global variables, define scoped variables, and assign values to variables. This post discusses some implementation issues that deserve attention.
</em>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rlox" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![144-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/07/144-feature-image.png) |
|:--:|
| *rlox: A Rust Implementation of “Crafting Interpreters” – Global Variables, Assignment, and Scope* |

<a id="repository-cloning"></a>
🚀 <strong>Note:</strong> You can download the code for this post from GitHub with:

```
git clone -b v0.3.0 https://github.com/behai-nguyen/rlox.git
```

<a id="running-the-current-cli"></a>
❶ <strong>Running the CLI Application</strong>

💥 The interactive mode is still available. However, valid expressions—such as 
<code>((4.5 / 2) * 2) == 4.50;</code>—currently produce no output. 
I'm not sure when interactive mode will be fully restored, and it’s not a current priority.

For now, Lox scripts can be run using the CLI application. For example:

```
▶️Windows: cargo run .\tests\data\variable\shadow_global.lox
▶️Ubuntu: cargo run ./tests/data/variable/shadow_global.lox
```

```
Content of shadow_global.lox:
```

```lox
var a = "global";
{
  var a = "shadow";
  print a; // expect: shadow
}
print a; // expect: global
```

For more information, please refer to 
<a href="https://github.com/behai-nguyen/rlox/blob/main/README.md#to-run" 
title="READEME.md | To Run" target="_blank">this section</a> of the 
<code>README.md</code>.

<a id="repository-layout"></a>
❷ <strong>Updated Repository Layout</strong>

<strong>Legend</strong>: <span style="font-size:1.5em;">★</span> = updated, <span style="font-size:1.5em;">☆</span> = new.

💥 Unmodified files are omitted for brevity.

```
.
├── docs
│   └── RLoxGuide.md ★
├── README.md ★
├── src
│   ├── data_type.rs ☆
│   ├── environment.rs ☆
│   ├── expr.rs ★
│   ├── interpreter.rs ★
│   ├── lib.rs ★
│   ├── lox_error_helper.rs ☆
│   ├── lox_error.rs ★
│   ├── main.rs ★
│   ├── parser.rs ★
│   ├── scanner.rs ★
│   ├── stmt.rs ★
│   └── token.rs ★
├── tests
│   ├── data/ ☆ ➜ around 11 directories & 88 files
│   ├── README.md ☆
│   ├── test_common.rs ★
│   ├── test_interpreter.rs ★
│   ├── test_parser.rs ★
│   ├── test_scanner.rs ★
│   └── test_statements_state.rs ☆
└── tool
    └── generate_ast
        └── src
            └── main.rs ★
```

<a id="author-test-scripts"></a>
❸ <strong>Catching Up on the Author's 
<a href="https://github.com/munificent/craftinginterpreters/tree/master/test/" 
title="Crafting Interpreters test scripts" target="_blank">Test Scripts</a></strong>

As noted in the 
<a href="https://behainguyen.wordpress.com/2025/06/14/rlox-a-rust-implementation-of-crafting-interpreters-scanner/#repository-layout" 
title="rlox: A Rust Implementation of “Crafting Interpreters” – Scanner" 
target="_blank">first post</a> of this project, I initially used the author's test scripts to verify the code after completing the scanner in 
<a href="https://craftinginterpreters.com/scanning.html" title="Chapter 4: Scanning" target="_blank">Chapter 4: Scanning</a>. 
However, during the next three chapters, I missed a large portion of the test scripts. There are quite a few of them, and here are some observations:

<ol>
<li style="margin-top:10px;">
They are not organised by chapter.
</li>

<li style="margin-top:10px;">
Within each subdirectory, scripts can apply to multiple chapters.
</li>

<li style="margin-top:10px;">
Each script needs to be examined individually, and we must use our own judgment to assess its suitability for the current stage of implementation.
</li>
</ol>

While working through Chapter 8: <a href="https://craftinginterpreters.com/statements-and-state.html" 
title="Statements and State" target="_blank">Statements and State</a>, 
I realised I had missed many scripts that should have been used in Chapter 4, 
Chapter 6: <a href="https://craftinginterpreters.com/parsing-expressions.html" 
title="Parsing Expressions" target="_blank">Parsing Expressions</a>, and Chapter 7: <a href="https://craftinginterpreters.com/evaluating-expressions.html" title="Evaluating Expressions" target="_blank">Evaluating Expressions</a>.

I retrofitted tests for around 70 scripts. Please refer to the 
<a href="https://github.com/behai-nguyen/rlox/tree/main/tests/data/" 
title="tests/data/ area" target="_blank">tests/data/ area</a> directory in the repository: 

<ol>
<li style="margin-top:10px;">
For each subdirectory, only the scripts actually used are checked in.
</li>
<li style="margin-top:10px;">
Each subdirectory contains a short <code>README.md</code> file that lists which scripts are used by which test modules.
</li>
</ol>

As a result, the following test modules have been updated:

<ol>
<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/6fc7af72399e30baad3ebd5ae020441ebc5a328f/tests/test_common.rs" 
title="the tests/test_common.rs module" target="_blank">tests/test_common.rs</a> — Writing a test method for every script would be overwhelming due to the large number of scripts. This helper module includes new types and utility methods to facilitate semi-automatic testing. The additions are straightforward and should be mostly self-explanatory. Some of them are discussed in later sections.
</li>
<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/6fc7af72399e30baad3ebd5ae020441ebc5a328f/tests/test_scanner.rs" 
title="the tests/test_scanner.rs module" target="_blank">tests/test_scanner.rs</a> — A single new method, 
<a href="https://github.com/behai-nguyen/rlox/blob/6fc7af72399e30baad3ebd5ae020441ebc5a328f/tests/test_scanner.rs#L674-L685" 
title="the test_scanner_generics() method" target="_blank">test_scanner_generics() method</a>, 
has been added. It uses just one script, but still follows the semi-automatic approach. This module may be the easiest place to start examining the new testing logic.
</li>
<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/6fc7af72399e30baad3ebd5ae020441ebc5a328f/tests/test_parser.rs" 
title="the tests/test_parser.rs module" target="_blank">tests/test_parser.rs</a> — 
<a href="https://github.com/behai-nguyen/rlox/blob/6fc7af72399e30baad3ebd5ae020441ebc5a328f/tests/test_parser.rs#L193-L238" 
title="the new test methods" target="_blank">Three new test methods</a> have been added.
</li>

<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/6fc7af72399e30baad3ebd5ae020441ebc5a328f/tests/test_interpreter.rs" 
title="the tests/test_interpreter.rs module" target="_blank">tests/test_interpreter.rs</a> 
 — A single new method, 
<a href="https://github.com/behai-nguyen/rlox/blob/6fc7af72399e30baad3ebd5ae020441ebc5a328f/tests/test_interpreter.rs#L720-L734" 
title="the test_interpreter_expr() method" target="_blank">test_interpreter_expr() method</a>, 
has been added, but it covers quite a few scripts.
</li>
</ol>

💥 I assume that by the end of Part II of the book, I should have tests that exercise all of the author's scripts. Otherwise, the test suite would be incomplete.

<a id="interpreter-refactoring"></a>
❹ <strong><code>Interpreter</code> Refactoring</strong>

The implementation of the <code>Interpreter</code> struct is responsible for producing output. 
During testing, we often need to capture this output—sometimes spanning multiple 
lines—in order to compare it against the expected results. I prefer not to use any 
third-party crate, and at the same time, I don't want the <code>Interpreter</code> to behave 
like a fully featured writer.

<a id="interpreter-actual-refactoring"></a>
Instead, we want the caller to specify the desired output destination. 
These “destinations” are objects that implement the 
<a href="https://doc.rust-lang.org/std/io/trait.Write.html" title="Trait Write" target="_blank">Write trait</a>.
The <code>Interpreter</code> simply delegates output writing to the specified destination. 
Relevant changes in the 
<a href="https://github.com/behai-nguyen/rlox/blob/6fc7af72399e30baad3ebd5ae020441ebc5a328f/src/interpreter.rs" 
title="the src/interpreter.rs module" target="_blank">src/interpreter.rs</a> module:

⓵ <strong>Refactoring the <code>Interpreter</code> Struct</strong>

```rust
...
pub struct Interpreter<W: Write> {
    output: W,
}

impl<W: Write> Interpreter<W> {
    pub fn new(output: W) -> Self {
        Interpreter { 
            output,
        }
    }

    pub fn get_output(&self) -> &W {
        &self.output
    }

    fn write_output(&mut self, value: &str) {
        writeln!(self.output, "{}", value).expect("Failed to write output");
    }
	...
}	
```

⓶ <strong>New Implementation of the <code>Stmt::Print</code> Statement</strong>

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">281
282
283
284
285
286
287
288
289
290
</pre></td><td class="code"><pre>    <span class="k">fn</span> <span class="nf">visit_print_stmt</span><span class="p">(</span><span class="o">&amp;</span><span class="k">mut</span> <span class="k">self</span><span class="p">,</span> <span class="n">stmt</span><span class="p">:</span> <span class="o">&amp;</span><span class="n">Print</span><span class="p">)</span> <span class="k">-&gt;</span> <span class="n">Result</span><span class="o">&lt;</span><span class="p">(),</span> <span class="n">LoxError</span><span class="o">&gt;</span> <span class="p">{</span>
        <span class="k">let</span> <span class="n">value</span><span class="p">:</span> <span class="n">Value</span> <span class="o">=</span> <span class="k">self</span><span class="nf">.evaluate</span><span class="p">(</span><span class="n">stmt</span><span class="nf">.get_expression</span><span class="p">())</span><span class="o">?</span><span class="p">;</span>

        <span class="c">// Note from the author in the original Java version:</span>
        <span class="c">//     Before discarding the expression’s value, we convert it to a </span>
        <span class="c">//     string using the stringify() method we introduced in the last </span>
        <span class="c">//     chapter and then dump it to stdout.</span>
        <span class="k">self</span><span class="nf">.write_output</span><span class="p">(</span><span class="o">&amp;</span><span class="k">self</span><span class="nf">.stringify</span><span class="p">(</span><span class="o">&amp;</span><span class="n">value</span><span class="p">));</span>
        <span class="nf">Ok</span><span class="p">(())</span>
    <span class="p">}</span>
</pre></td></tr></tbody></table></code></pre></figure>

<a id="interpreter-actual-refactoring-mut-self"></a>
💥 Note that the first parameter — <code>&mut self</code> — must now be mutable, which is a significant refactoring that will be discussed further in the <a href="#expr-stmt-factoring">Expressions and Statements</a> section.

<a id="interpreter-factoring-in-main"></a>
⓷ <strong>Using the <code>Interpreter</code> in the CLI Application — Writing to Standard Output</strong>

In the CLI application, the 
<a href="https://github.com/behai-nguyen/rlox/blob/6fc7af72399e30baad3ebd5ae020441ebc5a328f/src/main.rs#L37" 
title="the src/main.rs module" target="_blank">src/main.rs <code>run()</code></a> 
method passes <code>io::stdout()</code> as the output destination:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">37
</pre></td><td class="code"><pre><span class="k">let</span> <span class="k">mut</span> <span class="n">interpreter</span> <span class="o">=</span> <span class="nn">Interpreter</span><span class="p">::</span><span class="nf">new</span><span class="p">(</span><span class="nn">io</span><span class="p">::</span><span class="nf">stdout</span><span class="p">());</span>
</pre></td></tr></tbody></table></code></pre></figure>

All output is written directly to the terminal.

<a id="interpreter-factoring-and-tests"></a>
⓸ <strong>Using the <code>Interpreter</code> in Tests — Writing to a Byte Stream</strong>

The <code>tests/test_common.rs</code> module defines the public function 
<a href="https://github.com/behai-nguyen/rlox/blob/6fc7af72399e30baad3ebd5ae020441ebc5a328f/tests/test_common.rs#L179-L181" 
title="the tests/test_common.rs module make_interpreter() function" 
target="_blank">make_interpreter()</a>:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">179
180
181
</pre></td><td class="code"><pre><span class="k">pub</span> <span class="k">fn</span> <span class="n">make_interpreter</span><span class="o">&lt;</span><span class="n">W</span><span class="p">:</span> <span class="nn">std</span><span class="p">::</span><span class="nn">io</span><span class="p">::</span><span class="n">Write</span><span class="o">&gt;</span><span class="p">(</span><span class="n">writer</span><span class="p">:</span> <span class="n">W</span><span class="p">)</span> <span class="k">-&gt;</span> <span class="n">Interpreter</span><span class="o">&lt;</span><span class="n">W</span><span class="o">&gt;</span> <span class="p">{</span>
    <span class="nn">Interpreter</span><span class="p">::</span><span class="nf">new</span><span class="p">(</span><span class="n">writer</span><span class="p">)</span>
<span class="p">}</span>
</pre></td></tr></tbody></table></code></pre></figure>

In the existing 
<a href="https://github.com/behai-nguyen/rlox/blob/6fc7af72399e30baad3ebd5ae020441ebc5a328f/tests/test_interpreter.rs" 
title="the tests/test_interpreter.rs module" target="_blank">tests/test_interpreter.rs</a>
and new 
<a href="https://github.com/behai-nguyen/rlox/blob/6fc7af72399e30baad3ebd5ae020441ebc5a328f/tests/test_statements_state.rs" 
title="the tests/test_interpreter.rs module" target="_blank">tests/test_statements_state.rs</a>
modules, an <code>Interpreter</code> instance is created with a byte stream as the output destination:

```rust
let mut interpreter = make_interpreter(Cursor::new(Vec::new()));
```

After execution, the output can be extracted as a list of strings using the 
<a href="https://github.com/behai-nguyen/rlox/blob/6fc7af72399e30baad3ebd5ae020441ebc5a328f/tests/test_common.rs#L184-L190" 
title="the tests/test_common.rs module extract_output_lines() function" 
target="_blank">extract_output_lines()</a> 
function in <code>tests/test_common.rs</code>:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">184
185
186
187
188
189
190
</pre></td><td class="code"><pre><span class="k">pub</span> <span class="k">fn</span> <span class="nf">extract_output_lines</span><span class="p">(</span><span class="n">interpreter</span><span class="p">:</span> <span class="o">&amp;</span><span class="n">Interpreter</span><span class="o">&lt;</span><span class="n">Cursor</span><span class="o">&lt;</span><span class="nb">Vec</span><span class="o">&lt;</span><span class="nb">u8</span><span class="o">&gt;&gt;&gt;</span><span class="p">)</span> <span class="k">-&gt;</span> <span class="nb">Vec</span><span class="o">&lt;</span><span class="nb">String</span><span class="o">&gt;</span> <span class="p">{</span>
    <span class="k">let</span> <span class="n">output</span> <span class="o">=</span> <span class="n">interpreter</span><span class="nf">.get_output</span><span class="p">()</span><span class="nf">.clone</span><span class="p">()</span><span class="nf">.into_inner</span><span class="p">();</span>
    <span class="nn">String</span><span class="p">::</span><span class="nf">from_utf8</span><span class="p">(</span><span class="n">output</span><span class="p">)</span><span class="nf">.unwrap</span><span class="p">()</span>
        <span class="nf">.lines</span><span class="p">()</span>
        <span class="nf">.map</span><span class="p">(|</span><span class="n">line</span><span class="p">|</span> <span class="n">line</span><span class="nf">.to_string</span><span class="p">())</span>
        <span class="nf">.collect</span><span class="p">()</span>
<span class="p">}</span>
</pre></td></tr></tbody></table></code></pre></figure>

<a id="expr-stmt-factoring"></a>
❺ <strong>Expressions and Statements Refactoring</strong>

Enabling output delegation requires the <code>Interpreter</code> instance to be mutable, 
<a href="#interpreter-actual-factoring-mut-self">as discussed earlier</a>. 
This, in turn, necessitates the following changes in the implementation of expressions and statements:

<ol>
<li style="margin-top:10px;">
The first parameter of the <code>Visitor&lt;T&gt;</code> trait's <code>visit_()*</code> 
methods must now be mutable — <code>&mut self</code> — in both the 
<a href="https://github.com/behai-nguyen/rlox/blob/6fc7af72399e30baad3ebd5ae020441ebc5a328f/src/expr.rs#L343-L356" 
title="src/expr.rs" target="_blank">expr.rs</a> and 
<a href="https://github.com/behai-nguyen/rlox/blob/6fc7af72399e30baad3ebd5ae020441ebc5a328f/src/stmt.rs#L261-L271" 
title="src/stmt.rs" target="_blank">stmt.rs</a> modules.
</li>

<li style="margin-top:10px;">
The <code>accept()</code> method for both <code>Expr</code> and <code>Stmt</code> 
now requires both parameters to be mutable. This led to the introduction of 
<code>accept_ref()</code>, where <code>&self</code> is not mutable. 
Callers can invoke the appropriate method depending on the context. 
See the changes in 
<a href="https://github.com/behai-nguyen/rlox/blob/6fc7af72399e30baad3ebd5ae020441ebc5a328f/src/expr.rs#L359-L393" 
title="src/expr.rs" target="_blank">expr.rs</a> and 
<a href="https://github.com/behai-nguyen/rlox/blob/6fc7af72399e30baad3ebd5ae020441ebc5a328f/src/stmt.rs#L274-L302" 
title="src/stmt.rs" target="_blank">stmt.rs</a>.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2025/07/10/rlox-a-rust-implementation-of-crafting-interpreters-abstract-syntax-tree-ast-representing-code/#generate-ast" 
title="rlox: A Rust Implementation of “Crafting Interpreters” – Abstract Syntax Tree (AST) – Representing Code" 
target="_blank">As previously discussed</a>, both <code>expr.rs</code> and <code>stmt.rs</code> 
are generated by a standalone tool. The relevant parts of this tool have been updated to produce the desired changes. 
<a href="https://github.com/behai-nguyen/rlox/blob/6fc7af72399e30baad3ebd5ae020441ebc5a328f/tool/generate_ast/src/main.rs" 
title="the tool/generate_ast/src/main.rs module" target="_blank">Reference</a>.
</li>
</ol>	

<a id="the-environment"></a>
❻ <strong><code>Environment</code> Implementation, Usage, and Unit Tests</strong>

<a id="the-environment-issue"></a>
⓵ <strong>Multiple Ownership and Mutability</strong>

The initial part of the implementation—up to the 
<a href="https://craftinginterpreters.com/statements-and-state.html#assignment-semantics" 
title="Assignment semantics" target="_blank">Assignment Semantics</a> 
section—is straightforward and consists mainly of struct definitions. 
However, starting from the 
<a href="https://craftinginterpreters.com/statements-and-state.html#scope" 
title="Scope" target="_blank">Scope</a> section, particularly 
<a href="https://craftinginterpreters.com/statements-and-state.html#nesting-and-shadowing" 
title="Nesting and shadowing" target="_blank">Nesting and Shadowing</a>, 
the <code>Environment</code> becomes a 
<a href="https://en.wikipedia.org/wiki/Parent_pointer_tree" 
title="Parent pointer tree" target="_blank">Parent pointer tree</a>. 
At this point, managing ownership of the global <code>Environment</code> instance—
held by the <code>Interpreter</code>—becomes more complex: we require both multiple ownership and interior mutability.

To address this, <a href="https://doc.rust-lang.org/std/rc/struct.Rc.html" title="Struct Rc" target="_blank">Rc&lt;T&gt;</a> and 
<a href="https://doc.rust-lang.org/std/cell/struct.RefCell.html" title="Struct RefCell" target="_blank">RefCell&lt;T&gt;</a>
are used to manage <code>Environment</code> instances. For more information, see the relevant sections of <em>The Book</em>:

<ul>
<li style="margin-top:10px;">
<a href="https://doc.rust-lang.org/book/ch15-04-rc.html" 
title="Rc<T>, the Reference Counted Smart Pointer" 
target="_blank"><code>Rc&lt;T&gt;</code>, the Reference Counted Smart Pointer</a>
</li>

<li style="margin-top:10px;">
<a href="https://doc.rust-lang.org/book/ch15-05-interior-mutability.html" 
title="RefCell<T> and the Interior Mutability Pattern"
target="_blank"><code>RefCell&lt;T&gt;</code> and the Interior Mutability Pattern</a>
</li>

<li style="margin-top:10px;">
<a href="https://doc.rust-lang.org/book/ch15-05-interior-mutability.html#allowing-multiple-owners-of-mutable-data-with-rct-and-refcellt" 
title="Allowing Multiple Owners of Mutable Data with Rc<T> and RefCell<T>" 
target="_blank">Allowing Multiple Owners of Mutable Data with <code>Rc&lt;T&gt;</code> and <code>RefCell&lt;T&gt;</code></a>
</li>
</ul>

<a id="the-environment-impl-overview"></a>
⓶ <strong>Implementation Overview</strong>

The full implementation can be found in 
<a href="https://github.com/behai-nguyen/rlox/blob/6fc7af72399e30baad3ebd5ae020441ebc5a328f/src/environment.rs" 
title="the src/environment.rs module" target="_blank">src/environment.rs</a>
module. Here's the struct declaration and constructors: 

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">30
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
50
51
52
53
54
55
83
</pre></td><td class="code"><pre><span class="k">pub</span> <span class="k">type</span> <span class="n">EnvironmentRef</span> <span class="o">=</span> <span class="nb">Rc</span><span class="o">&lt;</span><span class="n">RefCell</span><span class="o">&lt;</span><span class="n">Environment</span><span class="o">&gt;&gt;</span><span class="p">;</span>

<span class="k">pub</span> <span class="k">struct</span> <span class="n">Environment</span> <span class="p">{</span>
    <span class="n">values</span><span class="p">:</span> <span class="n">ValuesMap</span><span class="p">,</span>
    <span class="n">enclosing</span><span class="p">:</span> <span class="nb">Option</span><span class="o">&lt;</span><span class="n">EnvironmentRef</span><span class="o">&gt;</span><span class="p">,</span>
<span class="p">}</span>

<span class="k">impl</span> <span class="n">Environment</span> <span class="p">{</span>
    <span class="c">// https://craftinginterpreters.com/statements-and-state.html#nesting-and-shadowing</span>
    <span class="c">// The global scope’s environment.</span>
    <span class="k">pub</span> <span class="k">fn</span> <span class="nf">new</span><span class="p">()</span> <span class="k">-&gt;</span> <span class="n">Self</span> <span class="p">{</span>
        <span class="n">Environment</span> <span class="p">{</span>
            <span class="n">values</span><span class="p">:</span> <span class="nn">HashMap</span><span class="p">::</span><span class="nf">new</span><span class="p">(),</span>
            <span class="n">enclosing</span><span class="p">:</span> <span class="nb">None</span><span class="p">,</span>
        <span class="p">}</span>
    <span class="p">}</span>

    <span class="c">// https://craftinginterpreters.com/statements-and-state.html#nesting-and-shadowing</span>
    <span class="c">// Creates a new local scope nested inside the given outer one.</span>
    <span class="k">pub</span> <span class="k">fn</span> <span class="nf">new_local_scope</span><span class="p">(</span><span class="n">enclosing</span><span class="p">:</span> <span class="n">EnvironmentRef</span><span class="p">)</span> <span class="k">-&gt;</span> <span class="n">Self</span> <span class="p">{</span>
        <span class="n">Environment</span> <span class="p">{</span>
            <span class="n">values</span><span class="p">:</span> <span class="nn">HashMap</span><span class="p">::</span><span class="nf">new</span><span class="p">(),</span>
            <span class="n">enclosing</span><span class="p">:</span> <span class="nf">Some</span><span class="p">(</span><span class="n">enclosing</span><span class="p">),</span>
        <span class="p">}</span>
    <span class="p">}</span>
    <span class="o">...</span>
<span class="p">}</span>
</pre></td></tr></tbody></table></code></pre></figure>

The <code>enclosing</code> field represents the parent environment. If there is no 
parent (i.e. global scope), it is set to <code>None</code>, which is why its type 
is <code>Option&lt;EnvironmentRef&gt;</code>. The <code>new_local_scope()</code> 
constructor is used inside <code>Interpreter</code> to create nested environments 
for block scopes.

<a id="the-environment-usage"></a>
⓷ <strong>Usage</strong>

The <code>Environment</code> is used in 
<a href="https://github.com/behai-nguyen/rlox/blob/6fc7af72399e30baad3ebd5ae020441ebc5a328f/src/interpreter.rs#L31-L40" 
title="the src/interpreter.rs module" target="_blank">src/interpreter.rs</a>:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">28
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
</pre></td><td class="code"><pre><span class="k">pub</span> <span class="k">struct</span> <span class="n">Interpreter</span><span class="o">&lt;</span><span class="n">W</span><span class="p">:</span> <span class="n">Write</span><span class="o">&gt;</span> <span class="p">{</span>
    <span class="n">output</span><span class="p">:</span> <span class="n">W</span><span class="p">,</span>
    <span class="c">// The variable global scope.</span>
    <span class="n">environment</span><span class="p">:</span> <span class="n">EnvironmentRef</span><span class="p">,</span>
<span class="p">}</span>

<span class="k">impl</span><span class="o">&lt;</span><span class="n">W</span><span class="p">:</span> <span class="n">Write</span><span class="o">&gt;</span> <span class="n">Interpreter</span><span class="o">&lt;</span><span class="n">W</span><span class="o">&gt;</span> <span class="p">{</span>
    <span class="k">pub</span> <span class="k">fn</span> <span class="nf">new</span><span class="p">(</span><span class="n">output</span><span class="p">:</span> <span class="n">W</span><span class="p">)</span> <span class="k">-&gt;</span> <span class="n">Self</span> <span class="p">{</span>
        <span class="n">Interpreter</span> <span class="p">{</span> 
            <span class="n">output</span><span class="p">,</span>
            <span class="n">environment</span><span class="p">:</span> <span class="nn">Rc</span><span class="p">::</span><span class="nf">new</span><span class="p">(</span><span class="nn">RefCell</span><span class="p">::</span><span class="nf">new</span><span class="p">(</span><span class="nn">Environment</span><span class="p">::</span><span class="nf">new</span><span class="p">())),</span>
        <span class="p">}</span>
    <span class="p">}</span>
    <span class="o">...</span>
</pre></td></tr></tbody></table></code></pre></figure>

The <code>Interpreter</code> initialises the global environment. When 
encountering a <code>Stmt::Block</code>, it creates a new environment for the block scope:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">253
254
255
256
257
258
259
260
261
262
263
</pre></td><td class="code"><pre><span class="k">impl</span><span class="o">&lt;</span><span class="n">W</span><span class="p">:</span> <span class="n">Write</span><span class="o">&gt;</span> <span class="nn">stmt</span><span class="p">::</span><span class="n">Visitor</span><span class="o">&lt;</span><span class="p">()</span><span class="o">&gt;</span> <span class="k">for</span> <span class="n">Interpreter</span><span class="o">&lt;</span><span class="n">W</span><span class="o">&gt;</span> <span class="p">{</span>
    <span class="k">fn</span> <span class="nf">visit_block_stmt</span><span class="p">(</span><span class="o">&amp;</span><span class="k">mut</span> <span class="k">self</span><span class="p">,</span> <span class="n">stmt</span><span class="p">:</span> <span class="o">&amp;</span><span class="n">Block</span><span class="p">)</span> <span class="k">-&gt;</span> <span class="n">Result</span><span class="o">&lt;</span><span class="p">(),</span> <span class="n">LoxError</span><span class="o">&gt;</span> <span class="p">{</span>
        
        <span class="k">let</span> <span class="n">new_env</span> <span class="o">=</span> <span class="nn">Rc</span><span class="p">::</span><span class="nf">new</span><span class="p">(</span><span class="nn">RefCell</span><span class="p">::</span><span class="nf">new</span><span class="p">(</span>
            <span class="nn">Environment</span><span class="p">::</span><span class="nf">new_local_scope</span><span class="p">(</span><span class="nn">Rc</span><span class="p">::</span><span class="nf">clone</span><span class="p">(</span><span class="o">&amp;</span><span class="k">self</span><span class="py">.environment</span><span class="p">))</span>
        <span class="p">));</span>
        <span class="k">self</span><span class="nf">.execute_block</span><span class="p">(</span><span class="n">stmt</span><span class="nf">.get_statements</span><span class="p">(),</span> <span class="n">new_env</span><span class="p">)</span><span class="o">?</span><span class="p">;</span>

        <span class="nf">Ok</span><span class="p">(())</span>
    <span class="p">}</span>
    <span class="o">...</span>
</pre></td></tr></tbody></table></code></pre></figure>

Replacing and restoring the environment is implemented as:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
</pre></td><td class="code"><pre>    <span class="c">// See: https://craftinginterpreters.com/statements-and-state.html#scope</span>
    <span class="k">pub</span> <span class="k">fn</span> <span class="nf">execute_block</span><span class="p">(</span><span class="o">&amp;</span><span class="k">mut</span> <span class="k">self</span><span class="p">,</span> <span class="n">statements</span><span class="p">:</span> <span class="o">&amp;</span><span class="p">[</span><span class="n">Stmt</span><span class="p">],</span> 
        <span class="n">new_env</span><span class="p">:</span> <span class="n">EnvironmentRef</span><span class="p">)</span> <span class="k">-&gt;</span> <span class="n">Result</span><span class="o">&lt;</span><span class="p">(),</span> <span class="n">LoxError</span><span class="o">&gt;</span> <span class="p">{</span>
        <span class="k">let</span> <span class="n">previous</span> <span class="o">=</span> <span class="nn">std</span><span class="p">::</span><span class="nn">mem</span><span class="p">::</span><span class="nf">replace</span><span class="p">(</span><span class="o">&amp;</span><span class="k">mut</span> <span class="k">self</span><span class="py">.environment</span><span class="p">,</span> <span class="n">new_env</span><span class="p">);</span>

        <span class="k">let</span> <span class="n">result</span> <span class="o">=</span> <span class="p">(||</span> <span class="p">{</span>
            <span class="k">for</span> <span class="n">stmt</span> <span class="n">in</span> <span class="n">statements</span> <span class="p">{</span>
                <span class="k">self</span><span class="nf">.execute</span><span class="p">(</span><span class="n">stmt</span><span class="p">)</span><span class="o">?</span><span class="p">;</span>
            <span class="p">}</span>
            <span class="nf">Ok</span><span class="p">(())</span>
        <span class="p">})();</span>

        <span class="k">self</span><span class="py">.environment</span> <span class="o">=</span> <span class="n">previous</span><span class="p">;</span>
        <span class="n">result</span>
    <span class="p">}</span>
	<span class="o">...</span>
</pre></td></tr></tbody></table></code></pre></figure>

<a href="https://doc.rust-lang.org/std/mem/fn.replace.html" 
title="std::mem Function replace" target="_blank">std::mem::replace()</a> safely 
swaps the current environment. If <code>self.execute(stmt)</code> returns an error, 
the closure immediately returns <code>Err(...)</code>, otherwise it returns <code>Ok(())</code>. 
In both cases, the <code>previous</code> environment is restored, ensuring 
<code>self.environment = previous;</code> is always executed—effectively mimicking a 
<code>try...finally</code> construct.

<a id="the-environment-unit-test"></a>
⓸ <strong>Unit Tests</strong>

There is a 
<a href="https://github.com/behai-nguyen/rlox/blob/6fc7af72399e30baad3ebd5ae020441ebc5a328f/src/environment.rs#L88-L246" 
title="the src/environment.rs module" target="_blank">comprehensive set of unit tests</a> 
for this module. To run them, use: 

```
cargo test environment::tests
```

<a id="concluding-remarks"></a>
❼ <strong>What’s Next</strong>

I apologise that this post is a bit long. I feel the need to document the problems encountered during development to explain the rationale behind the code. There are still five more chapters to go until Part II is complete. At this point, I’m a little more certain that I’m going to see this project through to the end of Part II.

There are still warnings about dead code—these I’m happy to ignore for now.

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
