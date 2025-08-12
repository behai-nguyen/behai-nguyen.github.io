---
layout: post
title: "rlox: A Rust Implementation of “Crafting Interpreters” – Resolving and Binding"

description: This post covers Chapter 11 of Crafting Interpreters&#58; Resolving and Binding. No new syntax elements are introduced in this chapter. Instead, Chapter 11 serves as a kind of patch to Chapter 10&#58; it ensures that variables are resolved within their correct closures. The code for this chapter is relatively straightforward, but I made a mistake that introduced a subtle bug—one that took me a long time to diagnose and finally fix. 

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
- resolver
- resolving
- binding
---

<em>
This post covers Chapter 11 of <a href="https://craftinginterpreters.com/resolving-and-binding.html" title="Resolving and Binding" target="_blank">Crafting Interpreters</a>: <strong>Resolving and Binding</strong>. No new syntax elements are introduced in this chapter. Instead, Chapter 11 serves as a kind of patch to Chapter 10: it ensures that variables are resolved within their correct <code>closures</code>. The code for this chapter is relatively straightforward, but I made a mistake that introduced a subtle bug—one that took me a long time to diagnose and finally fix.
</em>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rlox" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![147-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/08/147-feature-image.png) |
|:--:|
| *rlox: A Rust Implementation of “Crafting Interpreters” – Resolving and Binding* |

<a id="repository-cloning"></a>
🚀 <strong>Note:</strong> You can download the code for this post from GitHub using:

```
git clone -b v0.5.1 https://github.com/behai-nguyen/rlox.git
```

<a id="running-the-current-cli"></a>
❶ <strong>Running the CLI Application</strong>

💥 The interactive mode is still available. However, valid expressions—such as 
<code>((4.5 / 2) * 2) == 4.50;</code>—currently produce no output. 
I'm not sure when interactive mode will be fully restored, and it's not a current priority.

For now, Lox scripts can be executed via the CLI application. For example:

<a id="running-the-current-cli-script"></a>
```
cargo run --release ./tests/data/closure/book_fun_in_closure.lox
```

```
Content of book_fun_in_closure.lox:
```

```lox
var a = "global";
{
  fun showA() {
    print a;
  }

  showA();
  var a = "block";
  showA();
}
```

This Lox script appears at the end of the 
<a href="https://craftinginterpreters.com/resolving-and-binding.html#static-scope" 
title="Static Scope" target="_blank">Static Scope</a> section. What do you think 
it prints?

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
│   └── RLoxGuide.md ★
├── README.md ★
├── src
│   ├── ast_printer.rs ★
│   ├── environment.rs ★
│   ├── expr.rs ★
│   ├── interpreter.rs ★
│   ├── lib.rs ★
│   ├── lox_error_helper.rs ★
│   ├── lox_function.rs ★
│   ├── main.rs ★
│   ├── parser.rs ★
│   ├── resolver.rs ☆
│   ├── stmt.rs ★
│   ├── token.rs ★
│   └── token_type.rs ★
├── tests
│   ├── data/ ☆ ➜ only a few added
│   ├── README.md ★
│   ├── test_common.rs ★
│   ├── test_control_flow.rs ★
│   ├── test_functions.rs ★
│   ├── test_interpreter.rs ★
│   ├── test_parser.rs ★
│   ├── test_resolving_and_binding.rs ☆
│   ├── test_scanner.rs ★
│   └── test_statements_state.rs ★
└── tool
    └── generate_ast
        └── src
            └── main.rs ★
```

<a id="resolver-driven-refactoring"></a>
❸ <strong>
<code><a href="https://doc.rust-lang.org/std/collections/struct.HashMap.html"
title="Struct HashMap" target="_blank">HashMap</a></code>, Pointer Identity, 
and Their Driven Refactorings
</strong>

<a id="resolver-driven-refactoring-new-code"></a>
The code in Chapter 11 is fairly straightforward. However, the new logic in the 
<code>Interpreter</code> module deserves some discussion. For storing resolved 
variables, the author uses a 
<a href="https://github.com/munificent/craftinginterpreters/blob/1610d284827d92963629636d7340b18124ced202/java/com/craftinginterpreters/lox/Interpreter.java#L32" 
title="Resolving and Binding locals" target="_blank">HashMap</a> in Java:

<figure class="highlight"><pre><code class="language-java" data-lang="java"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">32
</pre></td><td class="code"><pre>  <span class="kd">private</span> <span class="kd">final</span> <span class="nc">Map</span><span class="o">&lt;</span><span class="nc">Expr</span><span class="o">,</span> <span class="nc">Integer</span><span class="o">&gt;</span> <span class="n">locals</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">HashMap</span><span class="o">&lt;&gt;();</span>
</pre></td></tr></tbody></table></code></pre></figure>

In the 
<a href="https://github.com/munificent/craftinginterpreters/blob/1610d284827d92963629636d7340b18124ced202/java/com/craftinginterpreters/lox/Interpreter.java#L87-L89" 
title="resolve() method" target="_blank">resolve()</a> method, the visited expression 
is stored along with the number of scopes between the variable’s declaration and the 
current scope. See the 
<a href="https://craftinginterpreters.com/resolving-and-binding.html#interpreting-resolved-variables" 
title="Interpreting Resolved Variables" target="_blank">reference</a>:

<figure class="highlight"><pre><code class="language-java" data-lang="java"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">87
88
89
</pre></td><td class="code"><pre>  <span class="kt">void</span> <span class="nf">resolve</span><span class="o">(</span><span class="nc">Expr</span> <span class="n">expr</span><span class="o">,</span> <span class="kt">int</span> <span class="n">depth</span><span class="o">)</span> <span class="o">{</span>
    <span class="n">locals</span><span class="o">.</span><span class="na">put</span><span class="o">(</span><span class="n">expr</span><span class="o">,</span> <span class="n">depth</span><span class="o">);</span>
  <span class="o">}</span>
</pre></td></tr></tbody></table></code></pre></figure>

Later, when accessing a resolved variable, the 
<a href="https://github.com/munificent/craftinginterpreters/blob/1610d284827d92963629636d7340b18124ced202/java/com/craftinginterpreters/lox/Interpreter.java#L482-L489" 
title="lookUpVariable() method" target="_blank">lookUpVariable()</a> method uses the 
stored depth to retrieve the correct binding:

<figure class="highlight"><pre><code class="language-java" data-lang="java"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">482
483
484
485
486
487
488
489
</pre></td><td class="code"><pre>  <span class="kd">private</span> <span class="nc">Object</span> <span class="nf">lookUpVariable</span><span class="o">(</span><span class="nc">Token</span> <span class="n">name</span><span class="o">,</span> <span class="nc">Expr</span> <span class="n">expr</span><span class="o">)</span> <span class="o">{</span>
    <span class="nc">Integer</span> <span class="n">distance</span> <span class="o">=</span> <span class="n">locals</span><span class="o">.</span><span class="na">get</span><span class="o">(</span><span class="n">expr</span><span class="o">);</span>
    <span class="k">if</span> <span class="o">(</span><span class="n">distance</span> <span class="o">!=</span> <span class="kc">null</span><span class="o">)</span> <span class="o">{</span>
      <span class="k">return</span> <span class="n">environment</span><span class="o">.</span><span class="na">getAt</span><span class="o">(</span><span class="n">distance</span><span class="o">,</span> <span class="n">name</span><span class="o">.</span><span class="na">lexeme</span><span class="o">);</span>
    <span class="o">}</span> <span class="k">else</span> <span class="o">{</span>
      <span class="k">return</span> <span class="n">globals</span><span class="o">.</span><span class="na">get</span><span class="o">(</span><span class="n">name</span><span class="o">);</span>
    <span class="o">}</span>
  <span class="o">}</span>
</pre></td></tr></tbody></table></code></pre></figure>

It’s clear that both methods operate on the actual 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/expr.rs#L317" 
title="the expr.rs module" target="_blank"><code>Expr</code> enum</a>, rather 
than on the variant structs associated with each enum. The Rust equivalent of Java’s 
<code>HashMap</code> is also 
<a href="https://doc.rust-lang.org/std/collections/struct.HashMap.html"
title="Struct HashMap" target="_blank"><code>HashMap</code></a>.

<a id="resolver-driven-refactoring-rc-pointer"></a>
⓵ <strong>The <code>
<a href="https://doc.rust-lang.org/book/ch15-04-rc.html" 
title="Rc&lt;T&gt;, the Reference Counted Smart Pointer" target="_blank">Rc&lt;T&gt;</a> 
</code> Pointer</strong>

I ran into some issues with the new code. After several iterations, it became clear that 
<a href="https://doc.rust-lang.org/book/ch15-04-rc.html" 
title="Rc&lt;T&gt;, the Reference Counted Smart Pointer" target="_blank">Rc&lt;T&gt;</a> 
was the correct pointer type to use for the 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/expr.rs#L317" 
title="the expr.rs module" target="_blank"><code>Expr</code></a> and 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/stmt.rs#L241" 
title="the stmt.rs module" target="_blank"><code>Stmt</code></a> enums—rather than 
<a href="https://doc.rust-lang.org/book/ch15-01-box.html" 
title="Using Box&lt;T&gt; to Point to Data on the Heap" target="_blank">Box&lt;T&gt;</a>.

<code>Rc&lt;T&gt;</code> implements 
<a href="https://doc.rust-lang.org/std/cmp/trait.PartialEq.html" 
title="Trait PartialEq" target="_blank">PartialEq</a>, 
<a href="https://doc.rust-lang.org/std/cmp/trait.Eq.html" 
title="Trait Eq" target="_blank">Eq</a>, and 
<a href="https://doc.rust-lang.org/std/hash/trait.Hash.html" 
title="Trait Hash" target="_blank">Hash</a> by delegating to <code>T</code>.
This means two <code>Rc&lt;T&gt;</code> instances are considered equal if their inner 
<code>T</code> values are equal. However, since variables being resolved may have the 
same name, comparing by value isn't sufficient. We need pointer identity instead—that is, 
the <code>HashMap</code> should key off the pointer addresses.

For this reason, the <code>Interpreter</code>'s 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/interpreter.rs#L72" 
title="the locals field" target="_blank"><code>locals</code></a> field uses raw 
pointer keys:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">72
</pre></td><td class="code"><pre>    <span class="n">locals</span><span class="p">:</span> <span class="n">HashMap</span><span class="o">&lt;*</span><span class="k">const</span> <span class="n">Expr</span><span class="p">,</span> <span class="nb">usize</span><span class="o">&gt;</span><span class="p">,</span>
</pre></td></tr></tbody></table></code></pre></figure>

And in the <code>Interpreter</code>'s 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/interpreter.rs#L137-L140" 
title="the src/interpreter.rs module resolve() method" target="_blank"> 
<code>resolve()</code></a> method, we use the pointer address via 
<a href="https://doc.rust-lang.org/std/rc/struct.Rc.html#method.as_ptr" 
title="pub fn as_ptr(this: &Rc&lt;T&gt;) -&gt; *const T" 
target="_blank"><code>Rc::as_ptr()</code></a>:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">137
138
139
140
</pre></td><td class="code"><pre>    <span class="k">pub</span> <span class="k">fn</span> <span class="nf">resolve</span><span class="p">(</span><span class="o">&amp;</span><span class="k">mut</span> <span class="k">self</span><span class="p">,</span> <span class="n">expr</span><span class="p">:</span> <span class="nb">Rc</span><span class="o">&lt;</span><span class="n">Expr</span><span class="o">&gt;</span><span class="p">,</span> <span class="n">depth</span><span class="p">:</span> <span class="nb">usize</span><span class="p">)</span> <span class="p">{</span>
        <span class="c">// Pointer identity, using pointer address: Rc::as_ptr(&amp;expr).</span>
        <span class="k">self</span><span class="py">.locals</span><span class="nf">.insert</span><span class="p">(</span><span class="nn">Rc</span><span class="p">::</span><span class="nf">as_ptr</span><span class="p">(</span><span class="o">&amp;</span><span class="n">expr</span><span class="p">),</span> <span class="n">depth</span><span class="p">);</span>
    <span class="p">}</span>
</pre></td></tr></tbody></table></code></pre></figure>

Similarly, the <code>Interpreter</code>'s 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/interpreter.rs#L142-L149" 
title="the src/interpreter.rs module look_up_variable() method" target="_blank"> 
<code>look_up_variable()</code></a> method:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">142
143
144
145
146
147
148
149
</pre></td><td class="code"><pre>    <span class="k">fn</span> <span class="nf">look_up_variable</span><span class="p">(</span><span class="o">&amp;</span><span class="k">self</span><span class="p">,</span> <span class="n">name</span><span class="p">:</span> <span class="o">&amp;</span><span class="n">Token</span><span class="p">,</span> <span class="n">expr</span><span class="p">:</span> <span class="nb">Rc</span><span class="o">&lt;</span><span class="n">Expr</span><span class="o">&gt;</span><span class="p">)</span> <span class="k">-&gt;</span> <span class="n">Result</span><span class="o">&lt;</span><span class="n">Value</span><span class="p">,</span> <span class="n">LoxError</span><span class="o">&gt;</span> <span class="p">{</span>
        <span class="c">// Pointer identity, using pointer address: &amp;Rc::as_ptr(&amp;expr).</span>
        <span class="k">if</span> <span class="k">let</span> <span class="nf">Some</span><span class="p">(</span><span class="o">&amp;</span><span class="n">distance</span><span class="p">)</span> <span class="o">=</span> <span class="k">self</span><span class="py">.locals</span><span class="nf">.get</span><span class="p">(</span><span class="o">&amp;</span><span class="nn">Rc</span><span class="p">::</span><span class="nf">as_ptr</span><span class="p">(</span><span class="o">&amp;</span><span class="n">expr</span><span class="p">))</span> <span class="p">{</span>
            <span class="nn">Environment</span><span class="p">::</span><span class="nf">get_at</span><span class="p">(</span><span class="o">&amp;</span><span class="k">self</span><span class="py">.environment</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="n">distance</span><span class="p">)</span>
        <span class="p">}</span> <span class="k">else</span> <span class="p">{</span>             
            <span class="k">self</span><span class="py">.globals</span><span class="nf">.borrow</span><span class="p">()</span><span class="nf">.get</span><span class="p">(</span><span class="n">name</span><span class="p">)</span>
        <span class="p">}</span>
    <span class="p">}</span>
</pre></td></tr></tbody></table></code></pre></figure>

💥 It's essential that the <code>Rc&lt;Expr&gt;</code> instance passed to 
<code>Interpreter::resolve()</code> is the same one later passed to 
<code>Interpreter::look_up_variable()</code>. We must not create a new instance using 
<a href="https://doc.rust-lang.org/std/rc/struct.Rc.html#method.new" 
title="pub fn new(value: T) -&gt; Rc&lt;T&gt;" target="_blank"><code>Rc::new()</code></a> 
in between. <strong>This was the trap I fell into—in transitional code, I created a new 
instance for the later method without realising it.</strong>

To arrive at the correct implementation, the existing code had to be refactored 
significantly. <code>Rc&lt;Expr&gt;</code> and <code>Rc&lt;Stmt&gt;</code> instances 
should be created only once. These refactorings are described in the next sections.

Before we move on, note that 
<a href="https://doc.rust-lang.org/std/rc/struct.Rc.html#method.clone" 
title="fn clone(&self) -&gt; Rc&lt;T&gt;" target="_blank"><code>Rc::clone()</code></a> 
increases the reference count but does not change the pointer address. This means we can 
safely clone an <code>Rc&lt;Expr&gt;</code> instance using either 
<code>Rc::clone(&expr)</code> or <code>expr.clone()</code>.

<a id="resolver-driven-refactoring-token-and-type"></a>
⓶ <strong>The 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/token_type.rs" 
title="the src/token_type.rs module" target="_blank"><code>src/token_type.rs</code></a> 
and 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/token.rs" 
title="the src/token.rs module" target="_blank"><code>src/token.rs</code></a> 
Modules</strong>

● All relevant <code>struct</code>s and <code>enum</code>s must implement the 
<a href="https://doc.rust-lang.org/std/cmp/trait.Eq.html" 
title="Trait Eq" target="_blank">Eq</a> and 
<a href="https://doc.rust-lang.org/std/hash/trait.Hash.html" 
title="Trait Hash" target="_blank">Hash</a> traits.

● In the <code>src/token_type.rs</code> module, for the <code>TokenType</code> enum, 
simply add <code>Eq</code> and <code>Hash</code> to the existing 
<code>#[derive(...)]</code> attribute.

● In the <code>src/token.rs</code> module:

<ol>
<li style="margin-top:10px;">
The <code>LiteralValue</code> enum includes a <code>Number(f64)</code> variant. 
Since <code>f64</code> does not implement <code>Hash</code> by default—due to 
NaNs and rounding behavior—you must manually implement <code>Hash</code> for 
<code>LiteralValue</code>. This can be done by converting the <code>f64</code> 
to a bit pattern using 
<a href="https://doc.rust-lang.org/std/primitive.f64.html#method.to_bits"  
title="pub const fn to_bits(self) -&gt; u64" target="_blank"><code>to_bits()</code></a>, 
which yields a <code>u64</code> that does implement <code>Hash</code>: 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/token.rs#L72-L92" 
title="the src/token.rs module" target="_blank">please see the implementation</a>.
</li>

<li style="margin-top:10px;">
The <code>Eq</code> trait is a marker trait—it defines no methods or associated types. 
Its 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/token.rs#L94" 
title="the src/token.rs module" target="_blank">implementation is simple</a>.
</li>

<li style="margin-top:10px;">
Once <code>LiteralValue</code> implements both <code>Hash</code> and <code>Eq</code>, 
you can then add <code>Eq</code> and <code>Hash</code> to the 
<code>#[derive(...)]</code> attribute of the <code>Token</code> struct: 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/token.rs#L19-L25" 
title="the src/token.rs module" target="_blank">please see</a>.
</li>

<li style="margin-top:10px;">
Also, all <code>get_</code> prefixes were removed from getter methods to comply 
with idiomatic Rust naming conventions.
</li>
</ol>

<a id="resolver-driven-refactoring-expr-and-stmt"></a>
⓷ <strong>The 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/expr.rs" 
title="the src/expr.rs module" target="_blank"><code>src/expr.rs</code></a> 
and 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/stmt.rs" 
title="the src/stmt.rs module" target="_blank"><code>src/stmt.rs</code></a> 
Modules</strong>

● As mentioned at the outset, the 
<a href="https://doc.rust-lang.org/book/ch15-04-rc.html" 
title="Rc&lt;T&gt;, the Reference Counted Smart Pointer" target="_blank">Rc&lt;T&gt;</a> 
smart pointer has replaced the 
<a href="https://doc.rust-lang.org/book/ch15-01-box.html" 
title="Using Box&lt;T&gt; to Point to Data on the Heap" target="_blank">Box&lt;T&gt;</a> 
pointer. This enables shared ownership and identity preservation across the AST.

● All <code>enum</code>s and variant <code>struct</code>s now implement the 
<a href="https://doc.rust-lang.org/std/cmp/trait.Eq.html" 
title="Trait Eq" target="_blank">Eq</a> and 
<a href="https://doc.rust-lang.org/std/hash/trait.Hash.html" 
title="Trait Hash" target="_blank">Hash</a> traits.

● 💡 Crucially, all <code>Visitor&lt;T&gt;</code>'s <code>visit_*</code> methods 
now receive the outer <code>enum</code> type directly—i.e., <code>Rc&lt;Expr&gt;</code> 
and <code>Rc&lt;Stmt&gt;</code>—rather than the inner variant <code>struct</code>.

● 💡 Equally important, the <code>accept()</code> and <code>accept_ref()</code> methods 
have been updated to take <code>Rc&lt;Expr&gt;</code> and <code>Rc&lt;Stmt&gt;</code> 
as parameters, replacing <code>&mut self</code> and <code>&self</code>. For example:

```rust
impl Expr {
    pub fn accept<T>(expr: Rc<Expr>, visitor: &mut dyn Visitor<T>) -> Result<T, LoxRuntimeError> {
	...
	}

    pub fn accept_ref<T>(expr: Rc<Expr>, visitor: &mut dyn Visitor<T>) -> Result<T, LoxRuntimeError> {
	...
    }
}
```

and

```rust
impl Stmt {
    pub fn accept<T>(stmt: Rc<Stmt>, visitor: &mut dyn Visitor<T>) -> Result<T, LoxRuntimeError> {
	...
    }

    pub fn accept_ref<T>(stmt: Rc<Stmt>, visitor: &mut dyn Visitor<T>) -> Result<T, LoxRuntimeError> {
	...
    }
}
```

This refactoring ensures that the original <code>Rc&lt;Expr&gt;</code> and 
<code>Rc&lt;Stmt&gt;</code> instances are passed around without altering their pointer identity.

● <a href="https://behainguyen.wordpress.com/2025/07/10/rlox-a-rust-implementation-of-crafting-interpreters-abstract-syntax-tree-ast-representing-code/#generate-ast" 
title="AST generation post" target="_blank">As discussed previously</a>, these modules are 
generated by 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/tool/generate_ast/src/main.rs" 
title="AST generator" target="_blank"><code>tool/generate_ast/src/main.rs</code></a>. 
This generator has been updated accordingly, and the helper function 
<code>get_constructor_overrides()</code> was removed.

● Also, all <code>get_</code> prefixes were removed from getter methods to comply 
with idiomatic Rust naming conventions.

<a id="resolver-driven-refactoring-parser"></a>
⓸ <strong>The 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/parser.rs" 
title="the src/parser.rs module" target="_blank"><code>src/parser.rs</code></a> 
Module</strong>

This is the starting point: the <code>Parser</code> is responsible for creating all 
<code>Expr</code> and <code>Stmt</code> instances. The refactoring is straightforward:

<ul>
<li style="margin-top:10px;">
Methods that previously returned <code>Result&lt;Expr, LoxError&gt;</code> now return 
<code>Result&lt;Rc&lt;Expr&gt;, LoxError&gt;</code>.
</li>
<li style="margin-top:10px;">
Methods that previously returned <code>Result&lt;Stmt, LoxError&gt;</code> now return 
<code>Result&lt;Rc&lt;Stmt&gt;, LoxError&gt;</code>.
</li>
<li style="margin-top:10px;">
The public 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/parser.rs#L480-L487" 
title="the src/parser.rs module parse() method" target="_blank"><code>parse()</code></a> 
method now returns <code>Result&lt;Vec&lt;Rc&lt;Stmt&gt;&gt;, LoxError&gt;</code>.
</li>
</ul>

<a id="resolver-driven-refactoring-interpreter"></a>
⓹ <strong>The 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/interpreter.rs" 
title="the src/interpreter.rs module" target="_blank"><code>src/interpreter.rs</code></a> 
Module</strong>

<ul>
<li style="margin-top:10px;">
The public 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/interpreter.rs#L232-L238" 
title="the src/interpreter.rs module interpret() method" target="_blank">
<code>interpret()</code></a> method now takes a reference to a list of 
<code>Rc&lt;Stmt&gt;</code>: <code>&Vec&lt;Rc&lt;Stmt&gt;&gt;</code>.
</li>

<li style="margin-top:10px;">
This change propagates through to other helper methods and visitor implementations.
</li>
</ul>

<a id="resolver-driven-refactoring-test-area"></a>
⓺ <strong>The Test Area</strong>

Changes to public methods in the main modules required minor updates across all 
existing test modules. These changes should be self-explanatory.

<a id="the-resolver"></a>
❹ <strong>The New Code: the 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/resolver.rs" 
title="the src/resolver.rs module" target="_blank"><code>Resolver</code></a></strong>

<a id="the-resolver-impl-detail"></a>
⓵ <strong>Some Implementation Details</strong>

The implementation closely mirrors the author's original Java version. Here are a few 
noteworthy details:

<ul>
<li style="margin-top:10px;">
The <code>scopes</code> field is implemented as 
<code>Vec&lt;HashMap&lt;String, bool&gt;&gt;</code>, representing a stack of lexical scopes.
</li>

<li style="margin-top:10px;">
Instances of <code>Rc&lt;Expr&gt;</code> and <code>Rc&lt;Stmt&gt;</code> passed to the 
<code>Resolver</code> must be the exact same ones passed to the 
<code>Interpreter</code>. Creating new <code>Rc</code> wrappers around existing 
<code>Expr</code> or <code>Stmt</code> objects will break resolution, as pointer identity 
is used to track bindings.
</li>
</ul>

<a id="the-resolver-incorporated"></a>
⓶ <strong>Incorporating the 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/resolver.rs" 
title="the src/resolver.rs module" target="_blank"><code>Resolver</code></a></strong>

As described 
<a href="https://craftinginterpreters.com/resolving-and-binding.html#running-the-resolver"
title="Running the resolver" target="_blank">in the book</a>, the 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/parser.rs#L480-L487" 
title="the src/parser.rs module" target="_blank"><code>Parser</code></a> 
returns a list of statements: <code>Vec&lt;Rc&lt;Stmt&gt;&gt;</code>. This list is first 
passed to the <code>Resolver</code>. If resolution succeeds, it is then passed to the 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/interpreter.rs#L232-L238" 
title="the src/interpreter.rs module" target="_blank"><code>Interpreter</code></a>:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">51
52
53
54
55
56
57
58
59
</pre></td><td class="code"><pre>	<span class="k">match</span> <span class="n">resolver</span><span class="nf">.resolve</span><span class="p">(</span><span class="o">&amp;</span><span class="n">statements</span><span class="p">)</span> <span class="p">{</span>
	  <span class="nf">Err</span><span class="p">(</span><span class="n">err</span><span class="p">)</span> <span class="k">=&gt;</span> <span class="nd">println!</span><span class="p">(</span><span class="s">"Resolve error: {}"</span><span class="p">,</span> <span class="n">err</span><span class="p">),</span>
		<span class="nf">Ok</span><span class="p">(</span><span class="mi">_</span><span class="p">)</span> <span class="k">=&gt;</span> <span class="p">{</span>
			<span class="k">match</span> <span class="n">interpreter</span><span class="nf">.interpret</span><span class="p">(</span><span class="o">&amp;</span><span class="n">statements</span><span class="p">)</span> <span class="p">{</span>
				<span class="nf">Err</span><span class="p">(</span><span class="n">err</span><span class="p">)</span> <span class="k">=&gt;</span> <span class="nd">println!</span><span class="p">(</span><span class="s">"Evaluation error: {}"</span><span class="p">,</span> <span class="n">err</span><span class="p">),</span>
				<span class="nf">Ok</span><span class="p">(</span><span class="mi">_</span><span class="p">)</span> <span class="k">=&gt;</span> <span class="p">(),</span>
			<span class="p">}</span>
		<span class="p">}</span>
	<span class="p">}</span>
</pre></td></tr></tbody></table></code></pre></figure>

See the full 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/main.rs#L38-L70" 
title="the src/main.rs module" target="_blank"><code>run()</code></a> method.

<a id="test-updates"></a>
❺ <strong>Test Updates</strong>

● A new module, 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/tests/test_resolving_and_binding.rs" 
title="test_resolving_and_binding.rs module" target="_blank"><code>tests/test_resolving_and_binding.rs</code></a>, 
was added. Its structure and conventions follow those of the existing test modules.

● 💥 After incorporating the 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/resolver.rs" 
title="the src/resolver.rs module" target="_blank"><code>Resolver</code></a>, 
many test scripts in the previously introduced 
<a href="https://github.com/behai-nguyen/rlox/blob/b4e3136c52bf8c0fa44d2a45cb7c7abe6a6c9ec0/tests/test_functions.rs" 
title="test_functions.rs module" target="_blank"><code>tests/test_functions.rs</code></a> 
module began failing. These scripts were migrated to the new 
<code>tests/test_resolving_and_binding.rs</code> module to reflect their dependency on resolution.

● 👉 What do you think is the output of the script introduced 
<a href="#running-the-current-cli-script">at the beginning</a> of this article?

● Only a handful of test scripts from the author's 
<a href="https://github.com/munificent/craftinginterpreters/tree/master/test/" 
title="Crafting Interpreters test suite" target="_blank">Crafting Interpreters test suite</a> 
have been incorporated to test the code of this chapter.

<a id="concluding-remarks"></a>
❻ <strong>What’s Next</strong>

That wraps up Chapter 11: 
<a href="https://craftinginterpreters.com/resolving-and-binding.html" 
title="Resolving and Binding" target="_blank">Resolving and Binding</a>.
There are still a few warnings about dead code, which I’m okay with for now. 
Two chapters remain in Part II, and I’m aiming to complete them during August 2025.

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
<a href="https://craftinginterpreters.com/" target="_blank">https://craftinginterpreters.com/</a>
</li>
</ul>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rlox" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>
