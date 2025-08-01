---
layout: post
title: "rlox: A Rust Implementation of “Crafting Interpreters” – Functions"

description: This post covers Chapter 10 of Crafting Interpreters&#58; Functions. The following new syntax elements have been implemented&#58; Expr&#58;&#58;Call, Stmt&#58;&#58;Function, and Stmt&#58;&#58;Return. Lox now supports fun, return, and closures. This post discusses several implementation details that deserve attention. 

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
- fun
- return
- closures
---

<em>
This post covers Chapter 10 of <a href="https://craftinginterpreters.com/functions.html" title="Functions" target="_blank">Crafting Interpreters</a>: <strong>Functions</strong>. The following new syntax elements have been implemented: <code>Expr::Call</code>, <code>Stmt::Function</code>, and <code>Stmt::Return</code>. Lox now supports <code>fun</code>, <code>return</code>, and <code>closures</code>. This post discusses several implementation details that deserve attention.
</em>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rlox" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![146-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/08/146-feature-image.png) |
|:--:|
| *rlox: A Rust Implementation of “Crafting Interpreters” – Functions* |

<a id="repository-cloning"></a>
<p>
🚀 <strong>Note:</strong> You can download the code for this post from GitHub using:
</p>

```
git clone -b v0.5.0 https://github.com/behai-nguyen/rlox.git
```

<a id="running-the-current-cli"></a>
<p>
❶ <strong>Running the CLI Application</strong>
</p>

<p>
💥 The interactive mode is still available. However, valid expressions—such as 
<code>((4.5 / 2) * 2) == 4.50;</code>—currently produce no output. 
I'm unsure when interactive mode will be fully restored, and it's not a current priority.
</p>

<p>
For now, Lox scripts can be executed via the CLI application. For example:
</p>

```
cargo run --release ./tests/data/function/book_make_counter.lox
```

```
Content of book_make_counter.lox:
```

```lox
fun makeCounter() {
  var i = 0;
  fun count() {
    i = i + 1;
    print i;
  }

  return count;
}

var counter = makeCounter();
counter(); // "1.0".
counter(); // "2.0".
```

<p>
This Lox script is at the beginning of the 
<a href="https://craftinginterpreters.com/functions.html#local-functions-and-closures" 
title="For Loops" target="_blank">Local Functions and Closures</a> section: it prints 
<code>1.0</code> and <code>2.0</code> — recall that we are 
<a href="https://behainguyen.wordpress.com/2025/07/10/rlox-a-rust-implementation-of-crafting-interpreters-abstract-syntax-tree-ast-representing-code/#scanner-factoring" 
title="rlox: A Rust Implementation of “Crafting Interpreters” – Abstract Syntax Tree (AST) – Representing Code" 
target="_blank">Normalising Number Literals</a>.
</p>

<p>
For more details, refer to 
<a href="https://github.com/behai-nguyen/rlox/blob/main/README.md#to-run" 
title="README.md | To Run" target="_blank">this section</a> of the 
<code>README.md</code>.
</p>

<a id="repository-layout"></a>
<p>
❷ <strong>Updated Repository Layout</strong>
</p>

<p>
<strong>Legend</strong>: <span style="font-size:1.5em;">★</span> = updated, <span style="font-size:1.5em;">☆</span> = new.
</p>

<p>
💥 Files not modified are omitted for brevity.
</p>

```
.
├── docs
│   └── RLoxGuide.md ★
├── README.md ★
├── src
│   ├── ast_printer.rs ★
│   ├── data_type.rs ★
│   ├── environment.rs ★
│   ├── expr.rs ★
│   ├── interpreter.rs ★
│   ├── lib.rs ★
│   ├── lox_callable.rs ☆
│   ├── lox_clock.rs ☆
│   ├── lox_function.rs ☆
│   ├── lox_return.rs ☆
│   ├── lox_runtime_error.rs ☆
│   ├── main.rs ★
│   ├── parser.rs ★
│   └── stmt.rs ★
├── tests
│   ├── data/ ☆ ➜ added more
│   ├── README.md ★
│   ├── test_common.rs ★
│   ├── test_control_flow.rs ★
│   ├── test_functions.rs ☆
│   ├── test_interpreter.rs ★
│   ├── test_parser.rs ★
│   └── test_statements_state.rs ★
└── tool
    └── generate_ast
        └── src
            └── main.rs ★
```

<p>
The introduction of 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/src/lox_callable.rs" 
title="src/lox_callable.rs" target="_blank">the <code>LoxCallable</code> trait</a> and 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/src/lox_function.rs" 
title="src/lox_function.rs" target="_blank">the <code>LoxFunction</code> struct</a> 
prompted substantial refactoring of the existing code. We begin by discussing these changes.
</p>

<a id="loxcallable-driven-refactoring"></a>
<p>
❸ <strong><code>LoxCallable</code> and Its Driven Refactorings</strong>
</p>

<p>
In the Java implementation, the first line of the 
<a href="https://github.com/munificent/craftinginterpreters/blob/1610d284827d92963629636d7340b18124ced202/java/com/craftinginterpreters/lox/Interpreter.java#L339" 
title="visitCallExpr() method" target="_blank">visitCallExpr()</a> method reads 
<code>Object callee = evaluate(expr.callee);</code>. Later, it checks 
<a href="https://github.com/munificent/craftinginterpreters/blob/1610d284827d92963629636d7340b18124ced202/java/com/craftinginterpreters/lox/Interpreter.java#L347" 
title="visitCallExpr() method" target="_blank"><code>if (!(callee instanceof LoxCallable))</code></a>. 
This implies that <code>evaluate()</code> may return a <code>LoxCallable</code> object, 
alongside other 
<a href="https://github.com/behai-nguyen/rlox/blob/main/docs/RLoxGuide.md#data-types" 
title="Lox Guide" target="_blank">supported data types</a>.
</p>

<p>
In rlox, the 
<a href="https://github.com/behai-nguyen/rlox/blob/d6f86f02c0dc0879b0071291ae5be1d06bdd2b07/src/interpreter.rs#L50-L52" 
title="evaluate() method" target="_blank">evaluate()</a> method returns 
<code>Result&lt;Value, LoxError&gt;</code>, where <code>Value</code> is an enum of 
<a href="https://github.com/behai-nguyen/rlox/blob/d6f86f02c0dc0879b0071291ae5be1d06bdd2b07/src/data_type.rs#L7-L15" 
title="supported data types" target="_blank">supported types</a>. 
To support callable objects, the <code>LoxCallable</code> trait must be added as a variant of 
<code>Value</code>: 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/src/data_type.rs#L18" 
title="Value::LoxCallable variant" target="_blank"><code>
LoxCallable(Box&lt;dyn LoxCallable&gt;)</code></a>.
</p>

<p>
Rust trait objects do not automatically implement <code>Clone</code> or <code>PartialEq</code>. 
While this limitation isn't prominently documented in one place, the following resources and 
compiler guidance confirm it:
</p>

<ol>
<li style="margin-top:10px;">
<a href="https://doc.rust-lang.org/reference/types/trait-object.html" 
title="Trait objects" target="_blank">Trait objects</a>
</li>

<li style="margin-top:10px;">
<a href="https://doc.rust-lang.org/book/ch17-02-trait-objects.html" 
title="Using Trait Objects That Allow for Values of Different Types" 
target="_blank">Using Trait Objects That Allow for Values of Different Types</a>
</li>

<li style="margin-top:10px;">
<a href="https://doc.rust-lang.org/std/clone/trait.Clone.html" 
title="Trait Clone" target="_blank">Trait Clone</a>
</li>

<li style="margin-top:10px;">
<a href="https://doc.rust-lang.org/std/cmp/trait.PartialEq.html" 
title="Trait PartialEq" target="_blank">Trait PartialEq</a>
</li>

<li style="margin-top:10px;">
<a href="https://doc.rust-lang.org/reference/items/traits.html#object-safety" 
title="Traits Dyn compatibility" target="_blank">Traits Dyn compatibility</a>
</li>
</ol>

<p>
As a result, once <code>LoxCallable(Box&lt;dyn LoxCallable&gt;)</code> was added to 
<code>Value</code>, the enum could no longer derive <code>Debug</code>, <code>Clone</code>, 
and <code>PartialEq</code> automatically. Only 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/src/data_type.rs#L12" 
title="Debug derive" target="_blank"><code>#[derive(Debug)]</code></a> remains, 
while explicit implementations of 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/src/data_type.rs#L23-L50" 
title="Manual Clone and PartialEq" target="_blank"><code>Clone</code> and <code>PartialEq</code></a> 
replace the previous derive.
</p>

<p>
To make the 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/src/lox_callable.rs" 
title="LoxCallable trait" target="_blank"><code>LoxCallable</code> trait</a> 
usable as a trait object, we need helper traits that enable 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/src/lox_callable.rs#L15-L46" 
title="CloneLoxCallable and PartialEqLoxCallable" target="_blank">cloning and comparison</a>. 
The trait is defined as follows:
</p>

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">48
49
50
51
52
53
</pre></td><td class="code"><pre><span class="k">pub</span> <span class="k">trait</span> <span class="n">LoxCallable</span><span class="p">:</span> <span class="n">Debug</span> <span class="o">+</span> <span class="n">CloneLoxCallable</span> <span class="o">+</span> <span class="n">PartialEqLoxCallable</span> <span class="p">{</span>
    <span class="k">fn</span> <span class="nf">arity</span><span class="p">(</span><span class="o">&amp;</span><span class="k">self</span><span class="p">)</span> <span class="k">-&gt;</span> <span class="nb">usize</span><span class="p">;</span>
    <span class="k">fn</span> <span class="nf">call</span><span class="p">(</span><span class="o">&amp;</span><span class="k">self</span><span class="p">,</span> <span class="n">interpreter</span><span class="p">:</span> <span class="o">&amp;</span><span class="k">mut</span> <span class="n">Interpreter</span><span class="p">,</span> <span class="n">arguments</span><span class="p">:</span> <span class="nb">Vec</span><span class="o">&lt;</span><span class="n">Value</span><span class="o">&gt;</span><span class="p">)</span> <span class="k">-&gt;</span> <span class="n">Result</span><span class="o">&lt;</span><span class="n">Value</span><span class="p">,</span> <span class="n">LoxRuntimeError</span><span class="o">&gt;</span><span class="p">;</span>
    <span class="k">fn</span> <span class="nf">as_any</span><span class="p">(</span><span class="o">&amp;</span><span class="k">self</span><span class="p">)</span> <span class="k">-&gt;</span> <span class="o">&amp;</span><span class="n">dyn</span> <span class="n">Any</span><span class="p">;</span>
    <span class="k">fn</span> <span class="nf">to_string</span><span class="p">(</span><span class="o">&amp;</span><span class="k">self</span><span class="p">)</span> <span class="k">-&gt;</span> <span class="nb">String</span><span class="p">;</span>
<span class="p">}</span>
</pre></td></tr></tbody></table></code></pre></figure>

<p>
💥 We discuss <code>LoxRuntimeError</code> in a 
<a href="#loxruntimeerror">later section</a>.
</p>

<p>
The <code>as_any()</code> method enables downcasting to recover the concrete type, 
as described in 
<a href="#loxfunction-driven-refactoring"><code>LoxFunction</code> and Its Driven Refactorings</a>. 
Note the explicit <code>PartialEq</code> implementation:
</p>

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">55
56
57
58
59
</pre></td><td class="code"><pre><span class="k">impl</span> <span class="n">PartialEq</span> <span class="k">for</span> <span class="nb">Box</span><span class="o">&lt;</span><span class="n">dyn</span> <span class="n">LoxCallable</span><span class="o">&gt;</span> <span class="p">{</span>
    <span class="k">fn</span> <span class="nf">eq</span><span class="p">(</span><span class="o">&amp;</span><span class="k">self</span><span class="p">,</span> <span class="n">other</span><span class="p">:</span> <span class="o">&amp;</span><span class="n">Self</span><span class="p">)</span> <span class="k">-&gt;</span> <span class="nb">bool</span> <span class="p">{</span>
        <span class="p">(</span><span class="o">**</span><span class="k">self</span><span class="p">)</span><span class="nf">.equals_callable</span><span class="p">(</span><span class="o">&amp;**</span><span class="n">other</span><span class="p">)</span>
    <span class="p">}</span>
<span class="p">}</span>
</pre></td></tr></tbody></table></code></pre></figure>

<p>
Unlike <code>Clone</code>, which operates on a single value and can delegate via 
<code>clone_box()</code>, <code>PartialEq</code> requires comparing two trait objects. 
Since Rust cannot infer the concrete types behind <code>Box&lt;dyn LoxCallable&gt;</code>, 
we must provide an explicit implementation. Even with <code>PartialEqLoxCallable</code> 
as a helper, the runtime lacks the type information needed to resolve <code>==</code> 
automatically.
</p>

<a id="loxfunction-driven-refactoring"></a>
<p>
❹ <strong><code>LoxFunction</code> and Its Driven Refactorings</strong>
</p>

<p>
⓵ <strong>Refactoring <code>Interpreter</code>'s Output Destinations</strong>
</p>

<a id="loxfunction-driven-refactoring-interpreter-output-destination"></a>
<p>
In a previous post, we discussed the <code>Interpreter</code>'s 
<a href="https://behainguyen.wordpress.com/2025/07/22/rlox-a-rust-implementation-of-crafting-interpreters-global-variables-assignment-and-scope/#interpreter-refactoring" 
title="rlox: A Rust Implementation of “Crafting Interpreters” – Global Variables, Assignment, and Scope" 
target="_blank">output destinations</a> in detail. Consider the following Lox script from Chapter 10, 
featured in the 
<a href="https://craftinginterpreters.com/functions.html#local-functions-and-closures" 
title="Functions | Local Functions and Closures" target="_blank">Local Functions and Closures</a> section:
</p>


```lox
fun makeCounter() {
  var i = 0;
  fun count() {
    i = i + 1;
    print i;
  }

  return count;
}

var counter = makeCounter();
counter(); // "1".
counter(); // "2".
```

<p>
<code>LoxFunction</code> enables the <code>Interpreter</code> to invoke functions like 
<code>makeCounter()</code> and <code>count()</code> in the script above. The <code>print</code> 
statement inside <code>count()</code> is executed via the 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/src/interpreter.rs#L389-L398" 
title="visit_print_stmt() method" target="_blank"><code>visit_print_stmt()</code></a> method. 
This means <code>LoxFunction</code> must have access to the <code>Interpreter</code>'s output 
destination.
</p>

<p>
After experimentation, it became clear that the <code>Interpreter</code>'s 
<code>output</code> field should be a trait object implementing the 
<a href="https://doc.rust-lang.org/std/io/trait.Write.html" 
title="Trait Write" target="_blank"><code>Write</code> trait</a>:
</p>

<ul>
<li style="margin-top:10px;">
We introduced a new 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/src/interpreter.rs#L34-L64" 
title="Writable trait" target="_blank"><code>Writable</code> trait</a> for type erasure.
</li>

<li style="margin-top:10px;">
The <code>Interpreter</code>'s <code>output</code> field was updated to 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/src/interpreter.rs#L67" 
title="Interpreter output field" target="_blank"><code>Box&lt;dyn Writable&gt;</code></a>. 
Methods using <code>output</code> remain unchanged.
</li>
</ul>

<p>
The <code>call()</code> method of 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/src/lox_function.rs#L37-L56" 
title="call() method" target="_blank"><code>LoxFunction</code></a> receives a mutable 
reference to the <code>Interpreter</code> and delegates execution to its methods. 
As a result, <code>call()</code> does not need direct access to the output destination.
</p>

<a id="loxfunction-driven-refactoring-test-helper-methods"></a>
<p>
⓶ <strong>Refactoring Test Helper Methods</strong>
</p>

<p>
The change to the <code>Interpreter</code>'s <code>output</code> field required updates to 
the <a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/tests/test_common.rs" 
title="test_common.rs module" target="_blank"><code>tests/test_common.rs</code></a> module:
</p>

<ol>
<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/tests/test_common.rs#L194-L210" 
title="extract_output_lines() method" target="_blank"><code>extract_output_lines()</code></a> — 
We downcast the <code>Interpreter</code>'s <code>output</code> trait object to retrieve the 
<code>Cursor&lt;Vec&lt;u8&gt;&gt;</code> byte stream. The rest of the method remains unchanged.
</li>

<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/tests/test_common.rs#L179-L182" 
title="make_interpreter() method" target="_blank"><code>make_interpreter()</code></a> — 
Removed generics; the parameter is now <code>writer: impl Writable + 'static</code>.
</li>

<li style="margin-top:10px;">
Added helper methods: 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/tests/test_common.rs#L184-L187" 
title="make_interpreter_stdout()" target="_blank"><code>make_interpreter_stdout()</code></a> and 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/tests/test_common.rs#L189-L192" 
title="make_interpreter_byte_stream()" target="_blank"><code>make_interpreter_byte_stream()</code></a>.
</li>

<li style="margin-top:10px;">
In other methods — The parameter 
<code>interpreter: &Interpreter&lt;Cursor&lt;Vec&lt;u8&gt;&gt;&gt;</code> is now simply 
<code>interpreter: &Interpreter</code>.
</li>
</ol>

<a id="loxreturn-and-loxruntimeerror"></a>
<p>
❺ <strong><code>LoxReturn</code> and the <code>LoxRuntimeError</code> Enum</strong>
</p>

<p>
The original Java implementation uses the language’s exception mechanism to handle 
<code>return</code> statements. The author defines a custom unchecked exception to signal 
early exits from Lox functions, and Java’s <code>try/catch</code> makes this approach seamless. 
In Rust, we achieve the same effect using <strong>control flow via <code>Result</code> and early returns</strong>.
</p>

<a id="loxreturn"></a>
<p>
⓵ <strong><code>LoxReturn</code></strong>
</p>

<p>
Unlike the Java version, 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/src/lox_return.rs" 
title="LoxReturn module" target="_blank"><code>LoxReturn</code></a> in Rust 
is simply a value holder. The <code>Interpreter</code> short-circuits execution by returning 
<code>LoxReturn</code> through a <code>Result</code>, allowing it to propagate up the call stack.
</p>

<a id="loxruntimeerror"></a>
<p>
⓶ <strong><code>LoxRuntimeError</code> Enum</strong>
</p>

<p>
Here is the original Java <code>visitReturnStmt()</code> method:
</p>

```java
  @Override
  public Void visitReturnStmt(Stmt.Return stmt) {
    Object value = null;
    if (stmt.value != null) value = evaluate(stmt.value);

    throw new Return(value);
  }
```

<p>
As the author explains, Java exceptions are used to implement Lox’s <code>return</code> behavior. 
In Rust, we use <code>Result</code> and early returns to simulate this control flow. 
Here is the equivalent Rust implementation:
</p>

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">400
401
402
403
404
405
406
407
408
</pre></td><td class="code"><pre>    <span class="k">fn</span> <span class="nf">visit_return_stmt</span><span class="p">(</span><span class="o">&amp;</span><span class="k">mut</span> <span class="k">self</span><span class="p">,</span> <span class="n">stmt</span><span class="p">:</span> <span class="o">&amp;</span><span class="n">Return</span><span class="p">)</span> <span class="k">-&gt;</span> <span class="n">Result</span><span class="o">&lt;</span><span class="p">(),</span> <span class="n">LoxRuntimeError</span><span class="o">&gt;</span> <span class="p">{</span>
        <span class="k">let</span> <span class="n">value</span> <span class="o">=</span> <span class="k">if</span> <span class="k">let</span> <span class="nf">Some</span><span class="p">(</span><span class="n">expr</span><span class="p">)</span> <span class="o">=</span> <span class="o">&amp;</span><span class="n">stmt</span><span class="nf">.get_value</span><span class="p">()</span> <span class="p">{</span>
            <span class="k">self</span><span class="nf">.evaluate</span><span class="p">(</span><span class="n">expr</span><span class="p">)</span><span class="o">?</span>
        <span class="p">}</span> <span class="k">else</span> <span class="p">{</span>
            <span class="nn">Value</span><span class="p">::</span><span class="nb">Nil</span>
        <span class="p">};</span>

        <span class="nf">Err</span><span class="p">(</span><span class="nn">LoxRuntimeError</span><span class="p">::</span><span class="nf">Return</span><span class="p">(</span><span class="n">LoxReturn</span> <span class="p">{</span> <span class="n">value</span> <span class="p">}))</span>
    <span class="p">}</span>
</pre></td></tr></tbody></table></code></pre></figure>

<p>
Previously, all <code>expr::Visitor</code> methods returned 
<a href="https://github.com/behai-nguyen/rlox/blob/d6f86f02c0dc0879b0071291ae5be1d06bdd2b07/src/interpreter.rs#L141-L257"
title="expr::Visitor implementation" target="_blank"><code>Result&lt;Value, LoxError&gt;</code></a>, 
and <code>stmt::Visitor</code> methods returned 
<a href="https://github.com/behai-nguyen/rlox/blob/d6f86f02c0dc0879b0071291ae5be1d06bdd2b07/src/interpreter.rs#L259-L329" 
title="stmt::Visitor implementation" target="_blank"><code>Result&lt;(), LoxError&gt;</code></a>. 
An <code>Err(LoxError)</code> indicated a runtime error.
</p>

<p>
With the introduction of <code>LoxReturn</code>, some <code>visit_*</code> methods now return 
one of three outcomes: <code>Ok(T)</code>, <code>Err(LoxError)</code>, or an early 
<code>LoxReturn</code>. The 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/src/lox_runtime_error.rs" 
title="LoxRuntimeError module" target="_blank"><code>LoxRuntimeError</code></a> enum 
encapsulates the latter two.
</p>

<p>
In <code>LoxFunction</code>'s 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/src/lox_function.rs#L37-L56" 
title="call() method" target="_blank"><code>call()</code></a> method:
</p>

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">47
48
49
50
51
52
53
54
55
</pre></td><td class="code"><pre>        <span class="k">return</span> <span class="k">match</span> <span class="n">interpreter</span><span class="nf">.execute_block</span><span class="p">(</span><span class="o">&amp;</span><span class="k">self</span><span class="py">.declaration</span><span class="nf">.get_body</span><span class="p">(),</span> <span class="n">environment</span><span class="p">)</span> <span class="p">{</span>
            <span class="nf">Err</span><span class="p">(</span><span class="nn">LoxRuntimeError</span><span class="p">::</span><span class="nf">Return</span><span class="p">(</span><span class="n">ret</span><span class="p">))</span> <span class="k">=&gt;</span> <span class="p">{</span>
                <span class="nf">Ok</span><span class="p">(</span><span class="n">ret</span><span class="py">.value</span><span class="p">)</span>
            <span class="p">}</span>
            <span class="nf">Err</span><span class="p">(</span><span class="nn">LoxRuntimeError</span><span class="p">::</span><span class="nf">Error</span><span class="p">(</span><span class="n">err</span><span class="p">))</span> <span class="k">=&gt;</span> <span class="nf">Err</span><span class="p">(</span><span class="nn">LoxRuntimeError</span><span class="p">::</span><span class="nf">Error</span><span class="p">(</span><span class="n">err</span><span class="p">)),</span>
            <span class="nf">Ok</span><span class="p">(</span><span class="mi">_</span><span class="p">)</span> <span class="k">=&gt;</span> <span class="p">{</span>
                <span class="nf">Ok</span><span class="p">(</span><span class="nn">Value</span><span class="p">::</span><span class="nb">Nil</span><span class="p">)</span>
            <span class="p">}</span>
        <span class="p">}</span>
</pre></td></tr></tbody></table></code></pre></figure>

<p>
✔️ A <code>LoxReturn</code> is translated into an <code>Ok(T)</code>, representing the 
function’s return value. The following <code>Interpreter</code> methods are relevant:
</p>

<ul>
<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/src/interpreter.rs#L264-L289" 
title="visit_call_expr() method" target="_blank"><code>visit_call_expr()</code></a> — 
Note: <code>Ok(func.call(self, arguments)?)</code>.
</li>

<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/src/interpreter.rs#L369-L376" 
title="visit_function_stmt() method" target="_blank"><code>visit_function_stmt()</code></a> — 
Converts a function declaration into a runtime representation and stores it in the current environment.
</li>

<li style="margin-top:10px;">   
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/src/interpreter.rs#L400-L408" 
title="visit_return_stmt() method" target="_blank"><code>visit_return_stmt()</code></a> — 
Note: <code>Err(LoxRuntimeError::Return(...))</code>.
</li>
</ul>

<a id="expr-stmt-factoring"></a>
<p>
⓷ <strong>Expressions and Statements Refactoring</strong>
</p>

<p>
As shown above, <code>LoxRuntimeError</code> replaces <code>LoxError</code> in 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/src/expr.rs" 
title="expr.rs" target="_blank"><code>expr.rs</code></a> and 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/src/stmt.rs" 
title="stmt.rs" target="_blank"><code>stmt.rs</code></a>. 
<a href="https://behainguyen.wordpress.com/2025/07/10/rlox-a-rust-implementation-of-crafting-interpreters-abstract-syntax-tree-ast-representing-code/#generate-ast" 
title="AST generation post" target="_blank">As discussed previously</a>, these modules are 
generated by 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/tool/generate_ast/src/main.rs" 
title="AST generator" target="_blank"><code>tool/generate_ast/src/main.rs</code></a>. 
The updates were simple textual replacements:
</p>

<ol>
<li style="margin-top:10px;">
<code>use super::lox_runtime_error::LoxRuntimeError;</code> replaced 
<code>use super::lox_error::LoxError;</code>
</li>

<li style="margin-top:10px;">
All instances of <code>LoxError</code> were replaced with <code>LoxRuntimeError</code>
</li>
</ol>

<a id="test-updates"></a>
<p>
❻ <strong>Test Updates</strong>
</p>

<p>
<p>
The refactorings described in 
<a href="#loxfunction-driven-refactoring-test-helper-methods">Refactoring Test Helper Methods</a> 
led to several minor updates across existing test modules. These changes are straightforward 
and will not be detailed here.
</p>

<p>
Additional test scripts from the author's 
<a href="https://github.com/munificent/craftinginterpreters/tree/master/test/" 
title="Crafting Interpreters test suite" target="_blank">Crafting Interpreters test suite</a> 
have been incorporated. These were used to expand both existing test methods and introduce new ones.
</p>

<p>
A new module, 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/tests/test_functions.rs" 
title="test_functions.rs module" target="_blank"><code>tests/test_functions.rs</code></a>, 
was added. Its implementation follows the same structure and conventions as the existing test modules.
</p>

<a id="author-benchmarking-scripts"></a>
❼ <strong>The Author's Benchmark Test Scripts</strong>

<p>
These benchmark scripts invoke the native <code>clock()</code> function, 
implemented in the 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/src/lox_clock.rs" 
title="lox_clock.rs" target="_blank"><code>lox_clock.rs</code></a> module. 
The reported results are in seconds.
</p>

<p>
In the author's 
<a href="https://github.com/munificent/craftinginterpreters/tree/master/test/benchmark/" 
title="test/benchmark/" target="_blank">test/benchmark/</a> directory, several benchmark scripts 
are provided. The current implementation supports running the following three scripts via the CLI application:
</p>

<p>
⓵ <a href="https://github.com/munificent/craftinginterpreters/tree/master/test/benchmark/equality.lox" 
title="test/benchmark/equality.lox test script" target="_blank">test/benchmark/equality.lox</a>
</p>

<div class="language-plaintext highlighter-rouge">
<div class="highlight"><pre class="highlight">
<code>cargo run ./tests/data/benchmark/equality.lox
</code></pre></div></div>

<p>
Output:
</p>

<div class="language-plaintext highlighter-rouge">
<div class="highlight"><pre class="highlight">
<code>loop
41.23750400543213
elapsed
51.01371693611145
equals
9.776212930679321
</code></pre></div></div>

<p>
⓶ <a href="https://github.com/munificent/craftinginterpreters/tree/master/test/benchmark/fib.lox" 
title="test/benchmark/fib.lox test script" target="_blank">test/benchmark/fib.lox</a>
</p>

<div class="language-plaintext highlighter-rouge">
<div class="highlight"><pre class="highlight">
<code>cargo run ./tests/data/benchmark/fib.lox
</code></pre></div></div>

<p>
Output:
</p>

<div class="language-plaintext highlighter-rouge">
<div class="highlight"><pre class="highlight">
<code>true
291.4927499294281
</code></pre></div></div>

<p>
⓷ <a href="https://github.com/munificent/craftinginterpreters/tree/master/test/benchmark/string_equality.lox" 
title="test/benchmark/string_equality.lox test script" target="_blank">test/benchmark/string_equality.lox</a>
</p>

<div class="language-plaintext highlighter-rouge">
<div class="highlight"><pre class="highlight">
<code>cargo run ./tests/data/benchmark/string_equality.lox
</code></pre></div></div>

<p>
Output:
</p>

<div class="language-plaintext highlighter-rouge">
<div class="highlight"><pre class="highlight">
<code>loop
59.191839933395386
elapsed
63.91852593421936
equals
4.726686000823975
</code></pre></div></div>
	
<a id="concluding-remarks"></a>
<p>
❽ <strong>What’s Next</strong>
</p>

<p>
That wraps up Chapter 10: 
<a href="https://craftinginterpreters.com/functions.html" 
title="Functions" target="_blank">Functions</a>—and the implementation discussion that came with it. 
There are still some warnings about dead code, which I’m okay with for now. 
With three more chapters remaining in Part II, I don’t plan on giving up at this stage.
</p>

<p>
Thanks for reading! I hope this post helps others on the same journey. 
As always—stay curious, stay safe 🦊
</p>

<p>✿✿✿</p>

<p>
Feature image sources:
</p>

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
