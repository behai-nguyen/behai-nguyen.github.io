---
layout: post
title: "rlox: A Rust Implementation of “Crafting Interpreters” – Inheritance"

description: This post covers Chapter 13 of Crafting Interpreters&#58; Inheritance. Class inheritance syntax < — Class < SuperClass — has been implemented. The final remaining syntax element, Expr&#58;&#58;Super, representing the super keyword, has also been added. In this post, we briefly discuss the new code, followed by bug fixes and test updates. 

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
- inheritance
---

<em>
This post covers Chapter 13 of <a href="https://craftinginterpreters.com/inheritance.html" title="Inheritance" target="_blank">Crafting Interpreters</a>: <strong>Inheritance</strong>. Class inheritance syntax <span style="font-weight:bold;font-size:1.5em;"><code>&lt;</code></span> — <code>Class</code> <span style="font-weight:bold;font-size:1.5em;"><code>&lt;</code></span> <code>SuperClass</code> — has been implemented. The final remaining syntax element, <code>Expr::Super</code>, representing the <code>super</code> keyword, has also been added. In this post, we briefly discuss the new code, followed by bug fixes and test updates.
</em>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rlox" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![149-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/08/149-feature-image.png) |
|:--:|
| *rlox: A Rust Implementation of “Crafting Interpreters” – Inheritance* |

<a id="repository-cloning"></a>
🚀 <strong>Note:</strong> You can download the code for this post from GitHub using:

```
git clone -b v0.6.1 https://github.com/behai-nguyen/rlox.git
```

<a id="running-the-current-cli"></a>
❶ <strong>Running the CLI Application</strong>

💥 The interactive mode is still available. However, valid expressions—such as 
<code>((4.5 / 2) * 2) == 4.50;</code>—currently produce no output. 
I'm not sure when interactive mode will be fully restored, and it's not a current priority.

For now, Lox scripts can be executed via the CLI application. For example:

<a id="running-the-current-cli-script"></a>

```
cargo run --release ./tests/data/scanning/sample.lox
```

```
Content of sample.lox:
```

```
class Doughnut {
  cook() {
    print "Fry until golden brown.";
  }
}

class BostonCream < Doughnut {
  cook() {
    super.cook();
    print "Pipe full of custard and coat with chocolate.";
  }
}

fun cooking(num) {
    var dish = BostonCream();
    print num;
    dish.cook();
}

for(var i=0; i<5; i=i+1) {
    cooking(i);
}
```

This Lox script is from 
<a href="https://github.com/fampiyush/rlox?tab=readme-ov-file#example" 
title="https://github.com/fampiyush/rlox?tab=readme-ov-file#example" target="_blank">here</a>. 
The <code>Doughnut</code> and <code>BostonCream</code> classes are from the book.
When I first explored the possibility of implementing the code in Rust, 
I downloaded and compiled this repository and ran the script. It executed successfully, 
and I was so inspired that I undertook the implementation myself. I’ve included it in the 
<a href="https://github.com/behai-nguyen/rlox/blob/main/tests/data/scanning/README.md" 
title="Scanner test script README.md" target="_blank">scanner test</a>. However, I can’t 
remember why I named it <code>sample.lox</code> instead of the original 
<code>example.lox</code>.

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
├── Cargo.toml
├── docs
│   └── RLoxGuide.md ★
├── README.md
├── src
│   ├── interpreter.rs ★
│   ├── lox_class.rs ★
│   ├── lox_error_helper.rs ★
│   ├── lox_error.rs ★
│   ├── lox_runtime_error.rs ★
│   ├── parser.rs ★
│   ├── resolver.rs ★
│   └── scanner.rs ★
└── tests
    ├── data/ ☆ ➜ some more were added
    ├── README.md ★
    ├── test_classes.rs ★
    ├── test_common.rs ★
    ├── test_inheritance.rs ☆
    ├── test_interpreter.rs ★
    ├── test_parser.rs ★
    ├── test_resolving_and_binding.rs ★
    └── test_scanner.rs ★
```

Compared to Chapter 12, Chapter 13 was somewhat a breeze. I didn’t encounter any further errors that required debugging. We briefly describe the implementation of the new code. Next, we discuss bug fixes to the 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/scanner.rs#L297-L328" 
title="The src/scanner.rs module | scan_tokens() method" target="_blank">
<code>Scanner</code></a>, 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/parser.rs#L530-L549" 
title="The src/parser.rs module | parse() method" target="_blank">
<code>Parser</code></a>, 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/resolver.rs#L58-L75" 
title="The src/resolver.rs module | resolve() method" target="_blank">
<code>Resolver</code></a>, and 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/interpreter.rs#L239-L265" 
title="The src/interpreter.rs module | interpret() method" target="_blank">
<code>Interpreter</code></a> to ensure all errors are returned, along with any partial evaluation results—particularly in the case of the <code>Interpreter</code>.
Finally, we discuss the test updates.

<a id="process-flow"></a>
<strong>❸ Process Flow: 
<code>Scanner</code>, <code>Parser</code>, <code>Resolver</code>, and <code>Interpreter</code>
</strong>

When the 
<code>Scanner</code> encounters an error, no token list is produced, so the 
<code>Parser</code> cannot and should not run.
Similarly, if the <code>Parser</code> fails, no statement list is available, and the 
<code>Resolver</code> should not run. If the <code>Resolver</code> fails, the 
<code>Interpreter</code> should not run either. While the statement list from the 
<code>Parser</code> remains available, attempting to evaluate unresolved statements 
with the <code>Interpreter</code> would be futile.

This interaction between the four components is illustrated in the flowchart below:

![scanner-parser-resolver-interpret.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/08/scanner-parser-resolver-interpret.png)

<a id="new-code"></a>
<strong>❹ New Code</strong>

Chapter 13 does not introduce any new modules. Instead, new code is added to the following existing modules.

<a id="new-code-parser"></a>
⓵ The existing <a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/parser.rs" 
title="The src/parser.rs module" target="_blank"><code>src/parser.rs</code></a>
module — Mirrors the Java version:

<ol>
<li style="margin-top:10px;">
Updated the existing 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/parser.rs#L441-L463" 
title="The src/parser.rs module | class_declaration() method" target="_blank">
<code>class_declaration()</code></a> method.
</li>

<li style="margin-top:10px;">
Updated the existing 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/parser.rs#L86-L133" 
title="The src/parser.rs module | primary() method" target="_blank">
<code>primary()</code></a> method.
</li>
</ol>	

The new code supports superclass declarations via the 
<span style="font-weight:bold;font-size:1.5em;"><code>&lt;</code></span> 
syntax, and enables access to superclass methods and properties using the <code>super</code> keyword.

<a id="new-code-resolver"></a>
⓶ The existing 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/resolver.rs" 
title="The src/resolver.rs module" target="_blank"><code>src/resolver.rs</code></a>
module — Mirrors the Java version:

<ol>
<li style="margin-top:10px;">
Updated the existing 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/resolver.rs#L267-L327" 
title="The src/resolver.rs module | visit_class_stmt() method" target="_blank">
<code>visit_class_stmt()</code></a> method — Resolves superclass references.
</li>

<li style="margin-top:10px;">
Implemented the 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/resolver.rs#L197-L219" 
title="The src/resolver.rs module | visit_super_expr() method" target="_blank">
<code>visit_super_expr()</code></a> method — Resolves the <code>super</code> keyword.
</li>
</ol>	

Additionally, for methods that return a 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/lox_runtime_error.rs#L32-L36" 
title="The src/lox_runtime_error.rs module | LoxRuntimeError enum" target="_blank">
<code>LoxRuntimeError</code></a> enum on error, we now use the 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/lox_error_helper.rs#L27-L29" 
title="The src/lox_error_helper.rs module" target="_blank">
<code>runtime_error()</code></a> helper method to construct the error.

<a id="new-code-interpreter"></a>
⓷ The existing 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/interpreter.rs" 
title="The src/interpreter.rs module" target="_blank"><code>src/interpreter.rs</code></a>
module — Mirrors the Java version:

<ol>
<li style="margin-top:10px;">
Updated the existing 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/interpreter.rs#L486-L534" 
title="The src/interpreter.rs module | visit_class_stmt() method" 
target="_blank"><code>visit_class_stmt()</code></a> method — Evaluates the superclass, 
i.e., the entity on the right-hand side of <code>&lt;</code>. For example, in <code>BostonCream &lt; Doughnut</code>, 
<code>Doughnut</code> is the superclass.
</li>

<li style="margin-top:10px;">
Implemented the 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/interpreter.rs#L412-L441" 
title="The src/interpreter.rs module | visit_super_expr() method" 
target="_blank"><code>visit_super_expr()</code></a> method — Evaluates the <code>super</code> keyword.
</li>
</ol>

The Rust code is more verbose than the Java version due to language constraints, but the implementation still closely mirrors the original.

As with the <code>Resolver</code>, methods returning a 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/lox_runtime_error.rs#L32-L36" 
title="The src/lox_runtime_error.rs module | LoxRuntimeError enum" target="_blank">
<code>LoxRuntimeError</code></a> enum now use the 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/lox_error_helper.rs#L27-L29" 
title="The src/lox_error_helper.rs module" target="_blank">
<code>runtime_error()</code></a> helper method for error construction.

<a id="new-code-lox-class"></a>
⓸ The existing 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/lox_class.rs" 
title="The src/lox_class.rs module" target="_blank"><code>src/lox_class.rs</code></a>
module — Mirrors the Java version:

<ol>
<li style="margin-top:10px;">
Added the 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/lox_class.rs#L26" 
title="The src/lox_class.rs module | superclass field" 
target="_blank"><code>superclass</code></a> field. Consequently, the 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/lox_class.rs#L31-L39" 
title="The src/lox_class.rs module | constructor method" 
target="_blank"><code>constructor</code></a> has been updated 
to accept a new <code>superclass</code> parameter.
</li>

<li style="margin-top:10px;">
The 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/lox_class.rs#L41-L48" 
title="The src/lox_class.rs module | find_method() method" 
target="_blank"><code>find_method()</code></a> method has been updated 
to search recursively in the superclass. Its return type is now an owned 
<code>Option&lt;LoxFunction&gt;</code> instead of a borrowed 
<code>Option&lt;&LoxFunction&gt;</code>.
</li>
</ol>

<a id="multiple-errors"></a>
<strong>❺ Bug Fix to Return Multiple Errors and Partial Evaluation Results</strong>

As of the Chapter 12 revision, the <code>Scanner</code>, <code>Parser</code>, 
<code>Resolver</code>, and <code>Interpreter</code> returned only the first error 
encountered—halting execution immediately. I overlooked this behavior, even while 
implementing tests using the author-provided scripts. For some reason, I ignored 
multiple errors in two scripts. This was a bug, though no debugging was required to fix it.

<a id="multiple-errors-scanner"></a>
⓵ The <code>Scanner</code> — Two bug fixes were made in the 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/scanner.rs#L297-L328" 
title="The src/scanner.rs module | scan_tokens() method" target="_blank">
<code>scan_tokens()</code></a> method:

<ol>
<li style="margin-top:10px;">
If the source text is blank, return an error immediately with the message 
<code>Source text is empty.</code> This is my own addition to handle empty input.
</li>
<li style="margin-top:10px;">
To capture and return multiple errors, we maintain a local vector of strings. 
Each time an error occurs, we push the message into the vector and continue scanning.
<p>
After scanning the full source, if the vector is empty, we return the token list. 
Otherwise, we return all error messages as a single string, separated by newline 
<span style="font-weight:bold;font-size:1.5em;"><code>\n</code></span> characters.
</p>
</li>
</ol>

<a id="multiple-errors-parser"></a>
⓶ The <code>Parser</code> — Similar to the <code>Scanner</code>, in the 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/parser.rs#L530-L549" 
title="The src/parser.rs module | parse() method" target="_blank">
<code>parse()</code></a> method, we maintain a local vector of strings. 
When a token causes an error, we push the message into the vector and continue parsing.

After processing all tokens, if the vector is empty, we return the statement list. 
Otherwise, we return all error messages as a single string, separated by newline 
<span style="font-weight:bold;font-size:1.5em;"><code>\n</code></span> characters.

<a id="multiple-errors-resolver"></a>
⓷ The <code>Resolver</code> — We apply the same approach. However, in the absence of errors, the 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/resolver.rs#L58-L75" 
title="The src/resolver.rs module | resolve() method" target="_blank">
<code>resolve()</code></a> method simply returns <code>Ok(())</code>.

<a id="multiple-errors-interpreter"></a>
⓸ The <code>Interpreter</code> — We follow the same pattern as the <code>Resolver</code>.
The 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/interpreter.rs#L239-L265" 
title="The src/interpreter.rs module | interpret() method" 
target="_blank"><code>interpret()</code></a> method now evaluates all
statements, capturing and returning both successful results and error messages.

💡 Recall that the <code>Interpreter</code> has an 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/interpreter.rs#L71" 
title="The src/interpreter.rs module | output: Box&lt;dyn Writable&gt; field" 
target="_blank"><code>output: Box&lt;dyn Writable&gt;</code></a> field, 
which writes all evaluation results to a buffer. In tests, we pass a byte stream to this field.

It is entirely reasonable to expect both successful and failed evaluations across statements. Therefore:

<ol>
<li style="margin-top:10px;">
Successful evaluations are written to <code>output</code> as usual.
</li>

<li style="margin-top:10px;">
When an error occurs:

<ul>
<li style="margin-top:10px;">
We write the error message to <code>output</code>.
</li>

<li style="margin-top:10px;">
We also push the error message to the local string vector.
</li>
</ul>
</li>
</ol>

Thus, the 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/src/interpreter.rs#L71" 
title="The src/interpreter.rs module | output: Box&lt;dyn Writable&gt; field" 
target="_blank"><code>Interpreter::output</code></a> buffer contains 
everything when errors occur, and only evaluation results when successful. 
The returned error contains only error messages. Naturally, when errors occur, 
those messages are also present in the <code>output</code> buffer.

<a id="test-updates"></a>
<strong>❻ Test Updates</strong>

● A new module, 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/tests/test_inheritance.rs" 
title="The tests/test_inheritance.rs module" target="_blank">
<code>tests/test_inheritance.rs</code></a>, 
was added. Its structure and conventions follow those of the existing test modules. 
It incorporates a relevant set of author-provided 
<a href="https://github.com/munificent/craftinginterpreters/tree/master/test/" 
title="Author-provided test scripts area" target="_blank">test scripts</a>.

● In the existing 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/tests/test_parser.rs" 
title="The tests/test_parser.rs module" target="_blank">
<code>tests/test_parser.rs</code></a> module, additional methods were 
introduced to test Chapter 13 parsing error logic:

<ol>
<li style="margin-top:10px;">
Method <a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/tests/test_parser.rs#L581-L597" 
title="The tests/test_parser.rs module | test_parser_inheritance_super_sub_class() method" target="_blank">
<code>test_parser_inheritance_super_sub_class()</code></a> and its helper 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/tests/test_parser.rs#L301-L312" 
title="The tests/test_parser.rs module | get_inheritance_super_sub_class_script_results() method" 
target="_blank"><code>get_inheritance_super_sub_class_script_results()</code></a>.
</li>

<li style="margin-top:10px;">
Method <a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/tests/test_parser.rs#L599-L617" 
title="The tests/test_parser.rs module | test_parser_inheritance_calling_superclass_method() method" target="_blank">
<code>test_parser_inheritance_calling_superclass_method()</code></a> and its helper 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/tests/test_parser.rs#L314-L337" 
title="The tests/test_parser.rs module | get_inheritance_calling_superclass_method_script_results() method" target="_blank">
<code>get_inheritance_calling_superclass_method_script_results()</code></a>.
</li>
</ol>

● Regarding the author-provided 
<a href="https://github.com/munificent/craftinginterpreters/tree/master/test/benchmark" 
title="Benchmark scripts" target="_blank">benchmark scripts</a> — These are not included in integration tests. I ran them manually and recorded the results. See 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/tests/data/benchmark/README.md" 
title="Benchmark results README" target="_blank"><code>README.md</code></a>.

The primary intention of this exercise is to demonstrate that the implementation is correct and can successfully run all author-provided test scripts.

● Regarding the 
<a href="https://github.com/munificent/craftinginterpreters/tree/master/test/" 
title="Test scripts area" target="_blank">test scripts</a> — All scripts are included except those in 
<a href="https://github.com/munificent/craftinginterpreters/tree/master/test/limit" 
title="Limit test scripts" target="_blank"><code>test/limit</code></a>.

● In the 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/tests/test_resolving_and_binding.rs" 
title="Resolving and binding tests" target="_blank"><code>tests/test_resolving_and_binding.rs</code></a> and 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/tests/test_classes.rs" 
title="Class tests" target="_blank"><code>tests/test_classes.rs</code></a> modules — Removed the <code>Error:</code> prefix from failed <code>Resolver</code> test outputs.

● Test refactoring triggered by <a href="#multiple-errors">bug fixes in point ❹</a>:

⓵ In the 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/tests/test_common.rs" 
title="Common test utilities" target="_blank"><code>tests/test_common.rs</code></a> module:

<ol>
<li style="margin-top:10px;">
The 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/tests/test_common.rs#L253-L300" 
title="assert_interpreter_result() method" target="_blank"><code>assert_interpreter_result()</code></a> method — Refactored per the 
<a href="#multiple-errors-interpreter">interpreter bug fix</a>:

<ul>
<li style="margin-top:10px;">
For both successful and failed scripts: validate all expected output entries.
</li>

<li style="margin-top:10px;">
For failed scripts: also verify that all returned error messages appear in the expected output.
</li>
</ul>
</li>

<li style="margin-top:10px;">
Similarly, the 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/tests/test_common.rs#L198-L218" 
title="assert_resolver_result() method" target="_blank"><code>assert_resolver_result()</code></a>, 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/tests/test_common.rs#L176-L196" 
title="assert_parser_result() method" target="_blank"><code>assert_parser_result()</code></a>, and 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/tests/test_common.rs#L154-L174" 
title="assert_scanner_result() method" target="_blank"><code>assert_scanner_result()</code></a> methods — Refactored to validate all expected error messages for failed scripts, per the respective bug fixes for 
<a href="#multiple-errors-resolver"><code>Resolver</code></a>, 
<a href="#multiple-errors-parser"><code>Parser</code></a>, and 
<a href="#multiple-errors-scanner"><code>Scanner</code></a>.
</li>
</ol>

⓶ In the existing 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/tests/test_parser.rs" 
title="Parser tests" target="_blank"><code>tests/test_parser.rs</code></a> module — Bug-fixed the helper method 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/tests/test_parser.rs#L155-L181" 
title="get_for_loops_script_results() method" target="_blank"><code>get_for_loops_script_results()</code></a> to include multiple error messages for 
<code>./tests/data/for/statement_condition.lox</code> and 
<code>./tests/data/for/statement_initializer.lox</code>.

⓷ In the existing 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/tests/test_scanner.rs" 
title="Scanner tests" target="_blank"><code>tests/test_scanner.rs</code></a> module — Updated the helper method 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/tests/test_scanner.rs#L663-L706" 
title="get_generic_script_results() method" target="_blank"><code>get_generic_script_results()</code></a> to include the author-provided scripts 
<code>./tests/data/empty_file.lox</code> and 
<code>./tests/data/unexpected_character.lox</code>, as well as the new script 
<code>./tests/data/scanning/multi_errors.lox</code>. I had missed the two author-provided ones until halfway through writing this post.

⓸ In the existing 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/tests/test_interpreter.rs" 
title="Interpreter tests" target="_blank"><code>tests/test_interpreter.rs</code></a> module — Added a new test method 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/tests/test_interpreter.rs#L754-L769" 
title="test_interpreter_precedence() method" target="_blank"><code>test_interpreter_precedence()</code></a> and its helper 
<a href="https://github.com/behai-nguyen/rlox/blob/b8ec375989e9b354e3beca99fb3c9680fb208538/tests/test_interpreter.rs#L720-L735" 
title="get_precedence_script_results() method" target="_blank"><code>get_precedence_script_results()</code></a> to test the author-provided script 
<code>./tests/data/precedence.lox</code>, which I had missed along with the two mentioned above.

<a id="concluding-remarks"></a>
❼ <strong>What’s Next</strong>

That wraps up Chapter 13: 
<a href="https://craftinginterpreters.com/inheritance.html" title="Inheritance" 
target="_blank">Inheritance</a>. I didn’t plan for this post to be quite this long—my apologies for its length.

There are still a few warnings about dead code, which I understand the reasons for. I’m leaving them as-is for now. I plan to do another round of refactoring across both the main code and test modules, without adding new features—so I can focus more clearly on areas I’m not fully happy with.

This post also marks the completion of Part II of the book. I’m not yet sure if I’ll take on Part III. I’m leaning toward it... but it would be a long undertaking, and I’m not committing to it in writing 😂.

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
<li>
<a href="https://www.anyrgb.com/en-clipart-23wno/download" target="_blank">https://www.anyrgb.com/en-clipart-23wno/download</a>
</li>
</ul>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rlox" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>
