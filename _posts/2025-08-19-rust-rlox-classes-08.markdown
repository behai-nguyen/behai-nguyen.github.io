---
layout: post
title: "rlox: A Rust Implementation of “Crafting Interpreters” – Classes"

description: This post covers Chapter 12 of Crafting Interpreters&#58; Classes. The following new syntax elements have been implemented&#58; Stmt&#58;&#58;Class, Expr&#58;&#58;Get, Expr&#58;&#58;Set, and Expr&#58;&#58;This. Lox now supports class, this, and init. While implementing this chapter, I encountered two stack overflow bugs and several cases where author-provided test scripts produced incorrect results. This post discusses those issues in detail. 

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
- class
- this
- init
---

<em>
This post covers Chapter 12 of <a href="https://craftinginterpreters.com/classes.html" title="Classes" target="_blank">Crafting Interpreters</a>: <strong>Classes</strong>. The following new syntax elements have been implemented: <code>Stmt::Class</code>, <code>Expr::Get</code>, <code>Expr::Set</code>, and <code>Expr::This</code>. Lox now supports <code>class</code>, <code>this</code>, and <code>init</code>. While implementing this chapter, I encountered two stack overflow bugs and several cases where author-provided test scripts produced incorrect results. This post discusses those issues in detail.
</em>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rlox" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![148-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/08/148-feature-image.png) |
|:--:|
| *rlox: A Rust Implementation of “Crafting Interpreters” – Classes* |

<a id="repository-cloning"></a>
🚀 <strong>Note:</strong> You can download the code for this post from GitHub using:

```
git clone -b v0.6.0 https://github.com/behai-nguyen/rlox.git
```

<a id="running-the-current-cli"></a>
❶ <strong>Running the CLI Application</strong>

💥 The interactive mode is still available. However, valid expressions—such as 
<code>((4.5 / 2) * 2) == 4.50;</code>—currently produce no output. 
I'm not sure when interactive mode will be fully restored, and it's not a current priority.

For now, Lox scripts can be executed via the CLI application. For example:

<a id="running-the-current-cli-script"></a>

```
cargo run --release ./tests/data/constructor/call_init_explicitly.lox
```

```
Content of call_init_explicitly.lox:
```

```
class Foo {
  init(arg) {
    print "Foo.init(" + arg + ")";
    this.field = "init";
  }
}

var foo = Foo("one"); // expect: Foo.init(one)
foo.field = "field";

var foo2 = foo.init("two"); // expect: Foo.init(two)
print foo2; // expect: Foo instance

// Make sure init() doesn't create a fresh instance.
print foo.field; // expect: init
```

This Lox script is an author provided one, it can be found 
<a href="https://github.com/munificent/craftinginterpreters/tree/master/test/constructor/call_init_explicitly.lox" 
title="Author provided test/constructor/call_init_explicitly.lox" target="_blank">here</a>. 
The output of this Lox script should be as noted: <code>Foo.init(one)</code>, 
<code>Foo.init(two)</code>, <code>Foo instance</code>, and <code>init</code>.

For more details on the Lox language, refer to 
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
│   ├── environment.rs ★
│   ├── interpreter.rs ★
│   ├── lib.rs ★
│   ├── lox_callable.rs ★
│   ├── lox_class.rs ☆
│   ├── lox_clock.rs ★
│   ├── lox_error_helper.rs ★
│   ├── lox_error.rs ★
│   ├── lox_function.rs ★
│   ├── lox_instance.rs ☆
│   ├── lox_return.rs ★
│   ├── main.rs ★
│   ├── parser.rs ★
│   ├── resolver.rs ★
│   └── value.rs ★ ➜ formerly data_type.rs
└── tests
    ├── data/ ☆ ➜ a lot more were added
    ├── README.md ★
    ├── test_classes.rs ☆
    ├── test_interpreter.rs ★
    └── test_parser.rs ★
```

The code for Chapter 12 initially appeared straightforward. However, testing it 
against the relevant scripts from the author's 
<a href="https://github.com/munificent/craftinginterpreters/tree/master/test/" 
title="Crafting Interpreters test suite" target="_blank">Crafting Interpreters test suite</a> 
revealed some existing flaws in my earlier implementation, as well as mistakes introduced 
during development. Working through these issues deepened my understanding of Rust, 
particularly around ownership, pointer identity, and trait object behavior. 
This post explores those challenges in detail.

<a id="derive-debug-stack-overflow"></a>
❶ <strong><code>#[derive(Debug)]</code> Can Potentially Cause Stack Overflow</strong> 

Consider the following Chapter 11 code:

<ol>
<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/lox_function.rs#L20-L24" 
title="The src/lox_function.rs | pub struct LoxFunction" 
target="_blank"><code>pub struct LoxFunction</code></a> — The <code>LoxFunction</code> 
struct implemented <code>Debug</code> via the <code>#[derive(Debug, Clone, PartialEq)]</code> attribute.
</li>

<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/data_type.rs#L12-L19" 
title="The src/data_type.rs module | Value enum" 
target="_blank"><code>DataType</code> aka <code>Value</code> enum</a> — The 
<code>Value::LoxCallable</code> variant was defined as <code>Box&lt;dyn LoxCallable&gt;</code>.
</li>
</ol>

These were still in place while I was converting code for Chapter 12. I needed 
to do some debug logging and happened to add a debug print inside the 
<code>Interpreter</code>'s
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/interpreter.rs#L310-L333" 
title="The src/interpreter.rs module | visit_call_expr() method" 
target="_blank"><code>visit_call_expr()</code></a> method, like so:

```rust
    fn visit_call_expr(&mut self, expr: Rc<Expr>) -> Result<Value, LoxRuntimeError> {
        let call = unwrap_expr!(expr, Call);

        let callee: Value = self.evaluate(Rc::clone(call.callee()))?;

        println!("Interpreter::visit_call_expr() callee {:?}", callee);
        ...
    }
```

The variable <code>callee</code> was a <code>Value::LoxCallable(Box&lt;dyn LoxCallable&gt;)</code>,
whose concrete type was <code>LoxFunction</code>. The <code>LoxFunction</code>'s 
<code>closure</code> was an 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/environment.rs#L30-L36" 
title="The src/environment.rs module | Environment struct" 
target="_blank"><code>Environment</code></a>, and its <code>enclosing</code> field 
was also an <code>Environment</code>.

In other words, <code>Environment</code> is a recursive structure. This recursive 
nesting caused the debug print to explode and eventually led to a stack overflow 
when the <code>Interpreter</code> tried to clone or traverse it. The 
<code>println!</code> statement above produced between 240K and 320K of repeated AST 
text before crashing.

💡 The solution was to override <code>Debug</code> for <code>LoxFunction</code> 
to <strong>avoid printing the full closure</strong>:

<ol>
<li style="margin-top:10px;">
Removed the <code>#[derive(Debug)]</code> attribute from 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/lox_function.rs#L20-L24" 
title="The src/lox_function.rs | pub struct LoxFunction" 
target="_blank"><code>pub struct LoxFunction</code></a>.
</li>

<li style="margin-top:10px;">
Manually implemented <code>std::fmt::Debug</code> for 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/lox_function.rs#L39-L43" 
title="The src/lox_function.rs | pub struct LoxFunction" 
target="_blank"><code>pub struct LoxFunction</code></a>.
</li>
</ol>

<a id="partialeq-trait-object-stack-overflow"></a>
<strong>❷ <code>PartialEq</code> on <code>Box&lt;dyn LoxCallable&gt;</code> Can Potentially Cause Stack Overflow</strong>

This stack overflow occurred when the codebase was still largely in the same state as the 
<a href="#derive-debug-stack-overflow">first stack overflow</a>. That is:

<ol>
<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/lox_function.rs#L20-L24" 
title="The src/lox_function.rs | pub struct LoxFunction" 
target="_blank"><code>pub struct LoxFunction</code></a> — The <code>LoxFunction</code> 
struct derived <code>PartialEq</code> via <code>#[derive(Debug, Clone, PartialEq)]</code>.
</li>

<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/data_type.rs#L12-L19" 
title="The src/data_type.rs module | Value enum" 
target="_blank"><code>DataType</code> aka <code>Value</code> enum</a> — The 
<code>Value::LoxCallable</code> variant was still defined as <code>Box&lt;dyn LoxCallable&gt;</code>.
</li>

<li style="margin-top:10px;">
In the manual 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/data_type.rs#L37-L50" 
title="The src/data_type.rs module | Value enum impl PartialEq" target="_blank">
<code>PartialEq</code> implementation for <code>Value</code></a>, the comparison for 
<code>Value::LoxCallable</code> was written as 
<code>(DataType::LoxCallable(a), DataType::LoxCallable(b)) => a == b,</code> 🤬.
</li>

<li style="margin-top:10px;">
The variables involved in the comparison were <code>Value::LoxCallable(Box&lt;dyn LoxCallable&gt;)</code>,
whose concrete type was <code>LoxFunction</code>.
</li>
</ol>

<code>Box&lt;dyn LoxCallable&gt;</code> doesn’t support <code>PartialEq</code> out of the box. 
So when Rust attempts to evaluate the equality comparison, it will:

<ol>
<li style="margin-top:10px;">
Try to resolve <code>PartialEq</code> for the trait object.
</li>

<li style="margin-top:10px;">
Since <code>PartialEq</code> was derived on <code>LoxFunction</code>, it will compare <strong>all fields</strong>.
</li>

<li style="margin-top:10px;">
That includes the <code>closure</code> field, which is an <code>Environment</code>.
</li>

<li style="margin-top:10px;">
<code>Environment</code> can contain values that include functions, which contain environments, and so on. 
This leads to infinite recursion and ultimately a stack overflow.
</li>
</ol>

💡 The solution involved two key fixes:

⓵ <strong>Compare the data pointer only</strong>—check <strong>identity</strong>, not equality. 
Replace the offending line 
<code>(DataType::LoxCallable(a), DataType::LoxCallable(b)) => a == b,</code> with:

<figure class="highlight"><pre><code class="language-rust" data-lang="rust"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">61
62
</pre></td><td class="code"><pre>	<span class="p">(</span><span class="nn">Value</span><span class="p">::</span><span class="nf">LoxCallable</span><span class="p">(</span><span class="n">a</span><span class="p">),</span> <span class="nn">Value</span><span class="p">::</span><span class="nf">LoxCallable</span><span class="p">(</span><span class="n">b</span><span class="p">))</span> <span class="k">=&gt;</span>
		<span class="nn">std</span><span class="p">::</span><span class="nn">ptr</span><span class="p">::</span><span class="nf">eq</span><span class="p">(</span><span class="n">a</span><span class="nf">.as_ref</span><span class="p">(),</span> <span class="n">b</span><span class="nf">.as_ref</span><span class="p">()),</span>
</pre></td></tr></tbody></table></code></pre></figure>

See the full updated 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/value.rs#L51-L67" 
title="The src/value.rs module | Value enum impl PartialEq" target="_blank">
<code>impl PartialEq for Value</code></a>.

⓶ <strong>Manually implement 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/lox_function.rs#L45-L59" 
title="The src/lox_function.rs | impl PartialEq for LoxFunction" 
target="_blank"><code>PartialEq</code> for <code>LoxFunction</code></a></strong>. 
This gives you full control over the equality logic: compare <code>closure</code> by identity, 
and <code>declaration</code> by value.

<a id="box-dyn-loxcallable"></a>

<strong>❸ <code>Box&lt;dyn LoxCallable&gt;</code> Breaks Pointer Identity</strong>

When I ran the author-provided test script 
<a href="https://github.com/munificent/craftinginterpreters/tree/master/test/operator/equals_method.lox" 
title="test/operator/equals_method.lox" target="_blank">test/operator/equals_method.lox</a>, 
which contains the following:

```
// Bound methods have identity equality.
class Foo {
  method() {}
}

var foo = Foo();
var fooMethod = foo.method;

// Same bound method.
print fooMethod == fooMethod; // expect: true

// Different closurizations.
print foo.method == foo.method; // expect: false
```

💥 I got <code>false</code> and <code>false</code> instead of the expected <code>true</code> and 
<code>false</code>.

The 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/data_type.rs#L23-L35" 
title="The src/data_type.rs module | Value enum Clone impl" 
target="_blank">manual <code>Clone</code> implementation for <code>DataType</code></a> 
correctly cloned <code>Box&lt;dyn LoxCallable&gt;</code> using:
<code>DataType::LoxCallable(callable) => DataType::LoxCallable(callable.clone_box())</code>.
However, this creates a <strong>new boxed object</strong>, which breaks pointer identity.

💡 The fix is to use <code>Rc&lt;dyn LoxCallable&gt;</code> instead of 
<code>Box&lt;dyn LoxCallable&gt;</code>. Since 
<a href="https://doc.rust-lang.org/std/rc/struct.Rc.html#method.clone" 
title="fn clone(&self) -&gt; Rc&lt;T, A&gt;" target="_blank"><code>Rc::clone()</code></a> 
preserves pointer identity, this change ensures correct behavior. See the refactored 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/value.rs#L24-L34" 
title="The src/value.rs module | pub enum Value" target="_blank">
<code>pub enum Value</code></a>.

With <code>Rc&lt;dyn LoxCallable&gt;</code>, we can safely derive <code>Clone</code> 
using <code>#[derive(Clone)]</code>, eliminating the need for a manual implementation.

After this change, the test script now produces the correct result.

<a id="lox-instance-get-interpreter-visit-get-expr"></a>
<strong>❹ The New 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/lox_instance.rs#L37-L52" 
title="The src/lox_instance.rs module | get()" target="_blank">
<code>LoxInstance::get()</code></a> and 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/interpreter.rs#L342-L351" 
title="The src/interpreter.rs module | visit_get_expr()" target="_blank">
<code>Interpreter::visit_get_expr()</code></a> Methods</strong>

The 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/lox_instance.rs" 
title="The src/lox_instance.rs module" target="_blank">
<code>src/lox_instance.rs</code></a> is a new module introduced in 
Chapter 12. It defines and implements the <code>LoxInstance</code> struct, 
which is also added as a variant of 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/value.rs#L24-L34" 
title="The src/value.rs module | pub enum Value" target="_blank">
<code>pub enum Value</code></a>: 
<code>LoxInstance(Rc&lt;RefCell&lt;LoxInstance&gt;&gt;)</code>.

At this stage of development, I ran the author-provided script referenced in 
<a href="#running-the-current-cli">the beginning</a> and got the wrong output:
<code>Foo.init(one)</code>, <code>Foo.init(two)</code>, <code>Foo instance</code>, 
and <code>field</code>. 💥 The last entry should have been <code>init</code>.

After several debugging iterations, I discovered the issue: in 
<code>Interpreter::visit_get_expr()</code>, I passed a <code>&LoxInstance</code> 
to <code>LoxInstance::get()</code>. That method then created a new 
<code>Rc&lt;RefCell&lt;LoxInstance&gt;&gt;</code> from the borrowed reference, 
which broke pointer identity.

However, <code>Interpreter::visit_get_expr()</code> already had access to the original 
<code>Rc&lt;RefCell&lt;LoxInstance&gt;&gt;</code>. I should have passed that directly to 
<code>LoxInstance::get()</code> instead of a reference. Then, inside 
<code>LoxInstance::get()</code>, I could simply clone it using 
<a href="https://doc.rust-lang.org/std/rc/struct.Rc.html#method.clone" 
title="fn clone(&self) -&gt; Rc&lt;T, A&gt;" target="_blank"><code>Rc::clone()</code></a>, 
which preserves pointer identity.

This fix allows the script — 
<a href="https://github.com/munificent/craftinginterpreters/tree/master/test/constructor/call_init_explicitly.lox" 
title="Author provided test/constructor/call_init_explicitly.lox" target="_blank">
test/constructor/call_init_explicitly.lox</a> — to run correctly.

<a id="other-side-effect-refactorings"></a>
<strong>❺ Other Side-Effect Refactorings</strong>

By <em>side-effect</em>, I mean refactorings triggered by bug fixes in existing code or by the introduction of new code.

<a id="other-side-effect-refactorings-value-mod"></a>
⓵ With the addition of the two 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/value.rs#L32-L33" 
title="The src/value.rs module | Value enum variants" target="_blank">
<code>LoxCallable</code> and <code>LoxInstance</code></a> variants to the <code>Value</code> enum, 
the former 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/data_type.rs#L12-L19" 
title="The src/data_type.rs module" target="_blank"><code>src/data_type.rs</code></a> module 
was renamed to 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/value.rs" 
title="The src/value.rs module | Value enum variants" target="_blank">
<code>src/value.rs</code></a>. The enum is now named <code>Value</code>; 
<code>DataType</code> has been removed.

<a id="other-side-effect-refactorings-lox-callable-mod"></a>
⓶ As discussed in 
<a href="#box-dyn-loxcallable">❸</a>, we replaced 
<code>Box&lt;dyn LoxCallable&gt;</code> with <code>Rc&lt;dyn LoxCallable&gt;</code> in the 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/lox_callable.rs" 
title="The src/lox_callable.rs module" target="_blank">
<code>src/lox_callable.rs</code></a> module. This change allowed us to simplify the module 
down to a trait declaration. We also removed the <code>to_string()</code> method in favor of 
<code>Display</code>. That means any concrete type implementing the <code>LoxCallable</code> trait 
must also implement <code>Display</code>. See:

<ol>
<li style="margin-top:10px;">
The existing 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/lox_clock.rs#L39-L43" 
title="The src/lox_clock.rs module" target="_blank"><code>src/lox_clock.rs</code></a>.
</li>

<li style="margin-top:10px;">
The existing  
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/lox_function.rs#L110-L114" 
title="The src/lox_function.rs module" target="_blank"><code>src/lox_function.rs</code></a>.
</li>

<li style="margin-top:10px;">
The new 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/lox_class.rs#L42-L46" 
title="The src/lox_class.rs module" target="_blank"><code>src/lox_class.rs</code></a>.
</li>
</ol>

<a id="other-side-effect-refactorings-environment-mod"></a>
⓷ Up to Chapter 11, the <code>src/environment.rs</code> module’s 
<a href="https://github.com/behai-nguyen/rlox/blob/0bd1e34b06a1503df7b18ecf00bcfb9fb4f07ff9/src/environment.rs#L88-L105" 
title="The src/environment.rs module | ancestor() and get_at() methods" 
target="_blank"><code>ancestor()</code> and <code>get_at()</code></a> methods 
included a <code>name: &Token</code> parameter. However, the original Java methods 
<a href="https://github.com/munificent/craftinginterpreters/blob/1610d284827d92963629636d7340b18124ced202/java/com/craftinginterpreters/lox/Environment.java#L61-L73" 
title="ancestor() method" target="_blank">do not</a>.

I’ve been reading and coding chapter by chapter without looking ahead, so I didn’t initially understand 
why <code>getAt()</code> lacked a <code>Token name</code> in the Java version. In Chapter 12, 
<code>getAt()</code> is called in 
<a href="https://github.com/munificent/craftinginterpreters/blob/1610d284827d92963629636d7340b18124ced202/java/com/craftinginterpreters/lox/LoxFunction.java#L78-L86" 
title="The LoxFunction.java module" target="_blank"><code>LoxFunction.java</code></a> 
without a <code>Token name</code>, which isn’t available at that point in the code anyway.

To match the Java version, I refactored the 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/environment.rs" 
title="The src/environment.rs module" target="_blank"><code>src/environment.rs</code></a> module. This involved:

<ol>
<li style="margin-top:10px;">
Adding a new 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/environment.rs#L71-L73" 
title="The src/environment.rs module | get_by_name() method" target="_blank"><code>get_by_name()</code></a> 
helper method.
</li>

<li style="margin-top:10px;">
Removing the <code>name: &Token</code> parameter from both 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/environment.rs#L95-L111" 
title="The src/environment.rs module | ancestor() method" target="_blank"><code>ancestor()</code></a> 
and 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/environment.rs#L113-L121" 
title="The src/environment.rs module | get_at() method" target="_blank"><code>get_at()</code></a>.
</li>
</ol>

The original purpose of the <code>name: &Token</code> parameter was to provide error context, 
specifically line numbers. But <code>get_at()</code> is only used for <strong>internally resolved variables</strong>. 
By the time it’s called in the <code>Interpreter</code>, resolution has already guaranteed the variable exists, 
so <strong>error context isn’t needed</strong>. If it fails, it’s a bug in the <code>Interpreter</code>, not user code. 
So the <code>name: &Token</code> was unnecessary.

<a id="new-code"></a>
<strong>❻ New Code</strong>

Apart from the 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/lox_instance.rs" 
title="The src/lox_instance.rs module" target="_blank">
<code>src/lox_instance.rs</code></a> module, which we discussed 
<a href="#lox-instance-get-interpreter-visit-get-expr">above</a>, the other code additions 
are fairly straightforward and closely mirror the Java version from the book.

<a id="new-code-lox-class"></a>
⓵ The new 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/lox_class.rs" 
title="The src/lox_class.rs module" target="_blank"> 
<code>src/lox_class.rs</code></a> module — Mirrors the Java version, 
though the 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/lox_class.rs#L57-L67" 
title="The src/lox_class.rs module | call() method" target="_blank"> 
<code>call()</code></a> method in Rust is particularly interesting.

<a id="new-code-parser-updates"></a>
⓶ The existing 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/parser.rs" 
title="The src/parser.rs module" target="_blank">
<code>src/parser.rs</code></a> module — Mirrors the Java version:

<ol>
<li style="margin-top:10px;">
Added a new 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/parser.rs#L434-L450" 
title="The src/parser.rs module | class_declaration() method" target="_blank">
<code>class_declaration()</code></a> method.
</li>

<li style="margin-top:10px;">
Updated the existing 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/parser.rs#L254-L272" 
title="The src/parser.rs module | declaration() method" target="_blank">
<code>declaration()</code></a> method to invoke <code>class_declaration()</code>.
</li>

<li style="margin-top:10px;">
Updated the existing methods 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/parser.rs#L159-L174" 
title="The src/parser.rs module | call() method" target="_blank">
<code>call()</code></a>, 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/parser.rs#L472-L491" 
title="The src/parser.rs module | assignment() method" target="_blank">
<code>assignment()</code></a>, and 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/parser.rs#L86-L126" 
title="The src/parser.rs module | primary() method" target="_blank">
<code>primary()</code></a> as per Chapter 12.
</li>
</ol>	

<a id="new-code-resolver-updates"></a>
⓷ Implemented the following methods in the existing 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/resolver.rs" 
title="The src/resolver.rs module" target="_blank">
<code>src/resolver.rs</code></a> module, as described in Chapter 12 — 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/resolver.rs#L236-L267" 
title="The src/resolver.rs module | visit_class_stmt() method" target="_blank">
<code>visit_class_stmt()</code></a>, 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/resolver.rs#L149-L153" 
title="The src/resolver.rs module | visit_get_expr() method" target="_blank">
<code>visit_get_expr()</code></a>, 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/resolver.rs#L174-L181" 
title="The src/resolver.rs module | visit_set_expr() method" target="_blank">
<code>visit_set_expr()</code></a>, and 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/resolver.rs#L187-L200" 
title="The src/resolver.rs module | visit_this_expr() method" target="_blank">
<code>visit_this_expr()</code></a>.

<a id="new-code-interpreter-updates"></a>
⓸ Updated the existing 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/interpreter.rs" 
title="The src/interpreter.rs module" target="_blank">
<code>src/interpreter.rs</code></a> module:

<ol>
<li style="margin-top:10px;">
Implemented the following methods as per Chapter 12: 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/interpreter.rs#L444-L462" 
title="The src/interpreter.rs module | visit_class_stmt() method" target="_blank">
<code>visit_class_stmt()</code></a>, 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/interpreter.rs#L342-L351" 
title="The src/interpreter.rs module | visit_get_expr() method" target="_blank">
<code>visit_get_expr()</code></a>, 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/interpreter.rs#L381-L395" 
title="The src/interpreter.rs module | visit_set_expr() method" target="_blank">
<code>visit_set_expr()</code></a>, and 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/interpreter.rs#L401-L406" 
title="The src/interpreter.rs module | visit_this_expr() method" target="_blank">
<code>visit_this_expr()</code></a>.
</li>

<li style="margin-top:10px;">
Updated the existing methods 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/interpreter.rs#L172-L182" 
title="The src/interpreter.rs module | is_truthy() method" target="_blank">
<code>is_truthy()</code></a> and 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/interpreter.rs#L214-L225" 
title="The src/interpreter.rs module | stringify() method" target="_blank">
<code>stringify()</code></a> to handle the new 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/value.rs#L33" 
title="The src/value.rs module | Value enum impl PartialEq" target="_blank">
<code>Value::LoxInstance(Rc&lt;RefCell&lt;LoxInstance&gt;&gt;)</code></a> enum variant.
</li>

<li style="margin-top:10px;">
Updated the existing 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/interpreter.rs#L147-L154" 
title="The src/interpreter.rs module | look_up_variable() method" target="_blank">
<code>look_up_variable()</code></a> method — In response to the 
<code>Environment::get_at()</code> signature refactoring 
<a href="#other-side-effect-refactorings-environment-mod">discussed earlier</a>.
</li>
</ol>

<a id="test-updates"></a>
<strong>❼ Test Updates</strong>

● A new module, 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/tests/test_classes.rs" 
title="tests/test_classes.rs" target="_blank"><code>tests/test_classes.rs</code></a>, 
was added. Its structure and conventions follow those of the existing test modules. 
It incorporates a relevant set of author-provided 
<a href="https://github.com/munificent/craftinginterpreters/tree/master/test/" 
title="Author provided test scripts area" target="_blank">test scripts</a>.

● In the existing module 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/tests/test_parser.rs" 
title="The tests/test_parser.rs module" target="_blank"><code>tests/test_parser.rs</code></a>, 
additional methods were introduced to test Chapter 12 parsing error logic:

<ol>
<li style="margin-top:10px;">
Method 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/tests/test_parser.rs#L485-L501" 
title="The tests/test_parser.rs module | test_parser_classes_field_and_property() method" 
target="_blank"><code>test_parser_classes_field_and_property()</code></a>  
and its helper  
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/tests/test_parser.rs#L248-L264" 
title="The tests/test_parser.rs module | get_classes_field_and_property_script_results() method" 
target="_blank"><code>get_classes_field_and_property_script_results()</code></a>.
</li>

<li style="margin-top:10px;">
Method 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/tests/test_parser.rs#L503-L519" 
title="The tests/test_parser.rs module | test_parser_classes_methods_on_classes() method" 
target="_blank"><code>test_parser_classes_methods_on_classes()</code></a>  
and its helper  
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/tests/test_parser.rs#L266-L282" 
title="The tests/test_parser.rs module | get_classes_methods_on_classes_script_results() method" 
target="_blank"><code>get_classes_methods_on_classes_script_results()</code></a>.
</li>

<li style="margin-top:10px;">
Method 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/tests/test_parser.rs#L521-L537" 
title="The tests/test_parser.rs module | test_parser_classes_this() method" target="_blank">
<code>test_parser_classes_this()</code></a>  
and its helper  
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/tests/test_parser.rs#L284-L295" 
title="The tests/test_parser.rs module | get_classes_this_script_results() method" target="_blank">
<code>get_classes_this_script_results()</code></a>.
</li>
</ol>	

● The update to the existing 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/tests/test_interpreter.rs" 
title="The tests/test_interpreter.rs module" target="_blank">
<code>tests/test_interpreter.rs</code></a> module was minor: a few adjustments 
were made in response to the removal of the <code>get_</code> prefix from 
getter methods in the 
<a href="https://github.com/behai-nguyen/rlox/blob/78b5ee77bece6e22d06c29b89a90208f30ad4e6b/src/lox_error.rs" 
title="The src/lox_error.rs module" target="_blank">
<code>src/lox_error.rs</code></a> module.

<a id="concluding-remarks"></a>
❽ <strong>What’s Next</strong>

That wraps up Chapter 12: 
<a href="https://craftinginterpreters.com/classes.html" 
title="Classes" target="_blank">Classes</a>. I apologise if this post feels a bit long, 
but I believe it's important to document everything thoroughly for my future self—especially 
after encountering so many bugs in this chapter. I'm still not entirely satisfied with the code; 
there’s room for improvement, and I may revisit it for refactoring later on.  

There are still a few warnings about dead code, which I’m okay with for now.  
Only one chapter remains in Part II, and about 10 days left until the end of August 2025.  
Hopefully, I’ll be able to complete it by then.

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
