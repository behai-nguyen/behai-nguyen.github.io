---
layout: post
title: "rlox: A Rust Implementation of “Crafting Interpreters” – Parsing and Evaluating Expressions"

description: In this post, I briefly describe the implementation of the code in Chapter 6&#58; Parsing Expressions, and Chapter 7&#58; Evaluating Expressions. 

tags: 
- Rust
- Compiler
- Interpreter
- Scanner
- Parser
- Evaluate
- Expressions
---

<em>
In this post, I briefly describe the implementation of the code in Chapter 6: <a href="https://craftinginterpreters.com/parsing-expressions.html" title="Parsing Expressions" target="_blank">Parsing Expressions</a>, and Chapter 7: <a href="https://craftinginterpreters.com/evaluating-expressions.html" title="Evaluating Expressions" target="_blank">Evaluating Expressions</a>.
</em>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rlox" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![143-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/07/143-feature-image.png) |
|:--:|
| *rlox: A Rust Implementation of “Crafting Interpreters” – Parsing and Evaluating Expressions* |

<a id="repository-cloning"></a>
🚀 <strong>Please note,</strong> code for this post can be downloaded from GitHub with:

```
git clone -b v0.2.0 https://github.com/behai-nguyen/rlox.git
```

<a id="running-the-current-cli"></a>
❶ <strong>Running the CLI Application</strong>

To run the CLI application, use the following command:

```
$ cargo run --release
```

Enter a valid expression such as <code>((4.5 / 2) * 2) == 4.50</code>.
This should produce the following output:

```
Expression: (== (group (* (group (/ 4.5 2.0)) 2.0)) 4.5)
Evaluated to: true
```

<ul>
<li style="margin-top:10px;">
<strong>Expression</strong>: Output of the 
<a href="https://github.com/behai-nguyen/rlox/blob/fb0359b66de2d84ae92ae3c1154b60c889d5d059/src/parser.rs" 
title="the src/parser.rs module" target="_blank">src/parser.rs</a> 
module.
</li>
<li style="margin-top:10px;">
<strong>Evaluated to</strong>: Output of the 
<a href="https://github.com/behai-nguyen/rlox/blob/fb0359b66de2d84ae92ae3c1154b60c889d5d059/src/interpreter.rs" 
title="the src/interpreter.rs module" target="_blank">src/interpreter.rs</a>
module. 
</li>
</ul>

🚀 At this point, the CLI application is capable as a basic arithmetic calculator 
which supports addition, subtraction, multiplication and division.

Please also refer to 
<a href="https://github.com/behai-nguyen/rlox/blob/main/README.md#to-run" 
title="READEME.md | To Run" target="_blank">this section</a> of the 
<code>README.md</code> for more information.

<a id="repository-layout"></a>
❷ <strong>Updated Repository Layout</strong>

<strong>Legend</strong>: <span style="font-size:1.5em;">★</span> = updated, <span style="font-size:1.5em;">☆</span> = new.

💥 Unmodified files are omitted for brevity.

```
.
├── docs
│   └── RLoxGuide.md ☆
├── README.md
├── src
│   ├── ast_printer.rs ★
│   ├── expr.rs ★
│   ├── interpreter.rs ☆
│   ├── lib.rs ★
│   ├── main.rs ★
│   ├── parser.rs ☆
│   └── stmt.rs ★
├── tests
│   ├── data
│   │   └── expressions ☆
│   │       ├── evaluate.lox
│   │       ├── parse-02.lox
│   │       ├── parse-03.lox
│   │       ├── parse.lox
│   │       └── README.md
│   ├── test_common.rs ★
│   ├── test_interpreter.rs ☆
│   └── test_parser.rs ☆
└── tool
    └── generate_ast
        └── src
            └── main.rs ★
```

As the 
<a href="https://github.com/behai-nguyen/rlox/blob/fb0359b66de2d84ae92ae3c1154b60c889d5d059/src/interpreter.rs" 
title="the src/interpreter.rs module" target="_blank">src/interpreter.rs</a> 
module was being developed, I have found that it would be more efficient 
to propagate the error up until the <code>main()</code> function. This is 
not unexpected, as stated toward the end of 
<a href="https://behainguyen.wordpress.com/2025/07/10/rlox-a-rust-implementation-of-crafting-interpreters-abstract-syntax-tree-ast-representing-code/#generate-ast" 
title="rlox: A Rust Implementation of “Crafting Interpreters” – Abstract Syntax Tree (AST) – Representing Code" 
target="_blank">this section</a> in a 
<a href="https://behainguyen.wordpress.com/2025/07/10/rlox-a-rust-implementation-of-crafting-interpreters-abstract-syntax-tree-ast-representing-code/" 
title="rlox: A Rust Implementation of “Crafting Interpreters” – Abstract Syntax Tree (AST) – Representing Code" 
target="_blank">previous post</a>. Let's cover those first.

<a id="expr-stmt-factoring"></a>
❸ <strong>Expressions and Statements Refactoring</strong>

In both modules 
<a href="https://github.com/behai-nguyen/rlox/blob/fb0359b66de2d84ae92ae3c1154b60c889d5d059/src/expr.rs#L343-L360" 
title="src/expr.rs" target="_blank">expr.rs</a>; and 
<a href="https://github.com/behai-nguyen/rlox/blob/fb0359b66de2d84ae92ae3c1154b60c889d5d059/src/stmt.rs#L261-L275" 
title="src/stmt.rs" target="_blank">stmt.rs</a>, all 
<code>Visitor&lt;T&gt;</code> trait's <code>visit_()*</code> and enum's 
<code>accept()</code> methods now return <code>Result&lt;T, LoxError&gt;</code>. 
This led to the following changes:

<ol>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2025/07/10/rlox-a-rust-implementation-of-crafting-interpreters-abstract-syntax-tree-ast-representing-code/#generate-ast" 
title="rlox: A Rust Implementation of “Crafting Interpreters” – Abstract Syntax Tree (AST) – Representing Code" 
target="_blank">As discussed</a>, both <code>expr.rs</code> and <code>stmt.rs</code> 
are generated by a standalone tool. The relevant parts of this tool have been updated 
to produce the desired output. 
<a href="https://github.com/behai-nguyen/rlox/blob/main/tool/generate_ast/src/main.rs#L158-L166" 
title="the tool/generate_ast/src/main.rs module"
target="_blank">Reference</a>.
</li>

<li style="margin-top:10px;">
Most of the methods in the 
<a href="https://github.com/behai-nguyen/rlox/blob/main/src/ast_printer.rs" 
title="the src/ast_printer.rs module" 
target="_blank">src/ast_printer.rs</a> module had to be refactored 
in response to the above changes.
</li>
</ol>	

<a id="parsing-expressions"></a>
❹ <strong>Parsing Expressions</strong>

This is <a href="https://craftinginterpreters.com/parsing-expressions.html"
title="Parsing Expressions" target="_blank">Chapter 6</a>. I have completed 
the parsing code in this chapter only:

<ol>
<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/fb0359b66de2d84ae92ae3c1154b60c889d5d059/src/parser.rs"
title="The src/parser.rs module" target="_blank">src/parser.rs</a>: 
The parser code. 
</li>

<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/fb0359b66de2d84ae92ae3c1154b60c889d5d059/tests/test_parser.rs" 
title="The tests/test_parser.rs module" target="_blank">tests/test_parser.rs</a>:
Tests for the parser module.
</li>
</ol>

The parser has been wired in the 
<a href="https://github.com/behai-nguyen/rlox/blob/fb0359b66de2d84ae92ae3c1154b60c889d5d059/src/main.rs#L38-L42" 
title="The src/main.rs module" target="_blank">src/main.rs</a> module,
it takes in a list of tokens, which is produced by the scanner. 
If parsing succeeds, we first call 
<a href="https://github.com/behai-nguyen/rlox/blob/fb0359b66de2d84ae92ae3c1154b60c889d5d059/src/ast_printer.rs" 
title="The src/ast_printer.rs module" target="_blank">src/ast_printer.rs</a> 
to display the resulting expression. Then passing the expression to the 
<a href="https://github.com/behai-nguyen/rlox/blob/fb0359b66de2d84ae92ae3c1154b60c889d5d059/src/interpreter.rs" 
title="The src/interpreter.rs module" target="_blank">src/interpreter.rs</a> 
module 
<a href="https://github.com/behai-nguyen/rlox/blob/fb0359b66de2d84ae92ae3c1154b60c889d5d059/src/main.rs#L44-L48" 
title="The src/main.rs module" target="_blank">to evaluate</a>.

<a id="evaluating-expressions"></a>
❺ <strong>Evaluating Expressions</strong>

And this is <a href="https://craftinginterpreters.com/evaluating-expressions.html"
title="Evaluating Expressions" target="_blank">Chapter 7</a>. The following 
expressions are implemented (evaluated): <code>Expr::Binary</code>, 
<code>Expr::Grouping</code>, <code>Expr::Literal</code> and <code>Expr::Unary</code>. 

🦀 Please recall that the Lox language supports only the following data types:

<ol>
<li style="margin-top:10px;">
<code>Number</code>: <code>f64</code> in Rust. E.g. <code>1.05</code>.
</li>

<li style="margin-top:10px;">
<code>String</code>: <code>String</code> in Rust. E.g. <code>abcd</code>.
</li>

<li style="margin-top:10px;">
<code>Boolean</code>: <code>bool</code> in Rust. E.g. <code>true</code> or <code>false</code>.
</li>

<li style="margin-top:10px;">
<code>Nil</code>: Expressed as <code>nil</code> without quotations.
</li>
</ol>

Expressions are evaluated to values of one of the above data types.

And I have also completed only the code for this chapter:

<ol>
<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/fb0359b66de2d84ae92ae3c1154b60c889d5d059/src/interpreter.rs" 
title="The src/interpreter.rs module" target="_blank">src/interpreter.rs</a>:
The interpreter code. 
</li>

<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/rlox/blob/fb0359b66de2d84ae92ae3c1154b60c889d5d059/tests/test_interpreter.rs" 
title="The tests/test_interpreter.rs module" target="_blank">tests/test_interpreter.rs</a>:
Exhaustive tests for the interpreter module.
</li>
</ol>

For the <code>Expr::Grouping</code> enum, the corresponding 
<a href="https://github.com/behai-nguyen/rlox/blob/fb0359b66de2d84ae92ae3c1154b60c889d5d059/src/interpreter.rs#L223-L225" 
title="The src/interpreter.rs module | visit_grouping_expr()" 
target="_blank">visit_grouping_expr()</a> method doesn’t <em>compute</em> 
anything itself, it traverses the AST to perform recursive evaluation of grouped 
sub-expressions: I have not written any test for this expression.

With regard to the <code>Expr::Literal</code> enum, whose corresponding 
<a href="https://github.com/behai-nguyen/rlox/blob/fb0359b66de2d84ae92ae3c1154b60c889d5d059/src/interpreter.rs#L227-L234" 
title="The src/interpreter.rs module | visit_literal_expr()" 
target="_blank">visit_literal_expr()</a> method, does not have to implement 
any operator, it just returns the underlying literal value. Whereas:

<ol>
<li style="margin-top:10px;">
<code>Expr::Binary</code> implements the following operator <code>&gt;</code>, 
<code>&gt;=</code>, <code>&lt;</code>, <code>&lt;=</code>, <code>!=</code>, 
<code>==</code>, <code>+</code>, <code>-</code>, <code>*</code>, and <code>/</code> 
via method 
<a href="https://github.com/behai-nguyen/rlox/blob/fb0359b66de2d84ae92ae3c1154b60c889d5d059/src/interpreter.rs#L167-L213" 
title="The src/interpreter.rs module | visit_literal_expr()" 
target="_blank">visit_binary_expr()</a>.
</li>

<li style="margin-top:10px;">
<code>Expr::Unary</code> implements <code>!</code> and <code>-</code> 
via method 
<a href="https://github.com/behai-nguyen/rlox/blob/fb0359b66de2d84ae92ae3c1154b60c889d5d059/src/interpreter.rs#L252-L264" 
title="The src/interpreter.rs module | visit_literal_expr()" 
target="_blank">visit_unary_expr()</a>.
</li>
</ol>

Please refer to the <strong>RLox Language Guide</strong>'s
<a href="https://github.com/behai-nguyen/rlox/blob/main/docs/RLoxGuide.md#expressions-and-operators" 
title="RLox Language Guide | Expressions and Operators" target="_blank">Expressions and 
Operators</a> for more detail.

The 
<a href="https://github.com/behai-nguyen/rlox/blob/fb0359b66de2d84ae92ae3c1154b60c889d5d059/tests/test_interpreter.rs" 
title="The tests/test_interpreter.rs module" target="_blank">interpreter test module</a> 
includes exhaustive tests for all <code>Expr::Literal</code> data types, all 
<code>Expr::Binary</code> and <code>Expr::Unary</code> operators.

<a id="concluding-remarks"></a>
❻ <strong>What’s Next</strong>

There is still a long journey ahead... I’m studying each chapter in turn, implementing the code and documenting my progress as I go.

There are still warnings about dead code—these, I’m happy to ignore them for now.

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
