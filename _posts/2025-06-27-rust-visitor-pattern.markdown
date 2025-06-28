---
layout: post
title: "Visitor Pattern with Rust"

description: Crafting Interpreters makes use of the visitor pattern, which I’m not yet familiar with. To better understand it, I’ve attempted to implement the C# and Java examples from the Wikipedia Visitor pattern article in Rust. Short, isolated examples like these help us grasp the underlying theory more effectively. We won’t be discussing the theory of the visitor pattern in this post.

tags: 
- Rust
- Visitor
- Pattern
- Compiler
- Interpreter
---

*<a href="https://craftinginterpreters.com/" title="Crafting Interpreters" target="_blank">Crafting Interpreters</a> makes use of the <a href="https://www.google.com/search?q=visitor+pattern&sca_esv=031453346484e3fe&sxsrf=AE3TifMt1Zv09mlol6xvyuLSIe-SuQ8RVw%3A1750945325549&source=hp&ei=LU5daNi5GZjc2roPj7nA-Q0&iflsig=AOw8s4IAAAAAaF1cParYGjGJNLFkiCZUR2Fzc8uzg2FT&ved=0ahUKEwiYhJLRm4-OAxUYrlYBHY8cMN8Q4dUDCBk&uact=5&oq=visitor+pattern&gs_lp=Egdnd3Mtd2l6GgIYAyIPdmlzaXRvciBwYXR0ZXJuMgoQIxiABBgnGIoFMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIIEAAYgAQYiwMyCBAAGIAEGIsDMgUQABiABDIIEAAYgAQYiwMyCBAAGIAEGIsDSIkpUABY7iZwAngAkAEAmAGuAqABkRuqAQcwLjkuNy4xuAEDyAEA-AEBmAIToAKeHMICFBAuGIAEGJECGLEDGNEDGMcBGIoFwgILEAAYgAQYkQIYigXCAg4QLhiABBixAxiDARiKBcICCxAuGIAEGNEDGMcBwgIIEAAYgAQYsQPCAhoQLhiABBixAxjRAxjSAxiDARjHARioAxiLA8ICBBAjGCfCAhAQLhiABBhDGMcBGIoFGK8BwgINEAAYgAQYQxiKBRiLA8ICHBAuGIAEGEMYpgMYxwEYqAMYigUYiwMYjgUYrwHCAgoQABiABBhDGIoFwgIdEC4YgAQYkQIYsQMY0QMY0gMYxwEYqAMYigUYiwPCAg4QABiABBiRAhiKBRiLA8ICChAuGIAEGEMYigXCAg0QABiABBixAxhDGIoFwgIUEC4YgAQYpgMYxwEYqAMYiwMYrwHCAhMQLhiABBhDGMcBGIoFGI4FGK8BwgIWEC4YgAQYsQMY0QMYQxiDARjHARiKBcICERAuGIAEGLEDGIMBGMcBGK8BwgIUEC4YgAQYkQIYxwEYigUYjgUYrwHCAgsQLhiABBjHARivAcICDhAuGIAEGLEDGNEDGMcBwgIHECMYsQIYJ8ICChAAGIAEGLEDGArCAgcQABiABBgKwgINEC4YgAQYxwEYChivAcICExAuGIAEGLEDGIMBGMcBGAoYrwHCAgsQABiABBixAxiDAcICCxAAGIAEGLEDGIoFwgIOEC4YgAQYxwEYjgUYrwGYAwCSBwcyLjcuOS4xoAesrAGyBwcwLjcuOS4xuAeHHMIHBjItMTMuNsgHdg&sclient=gws-wiz" title="Google search: visitor pattern" target="_blank">visitor pattern</a>, which I’m not yet familiar with. To better understand it, I’ve attempted to implement the C# and Java examples from the <a href="https://en.wikipedia.org/wiki/Visitor_pattern" title="Wikipedia: Visitor pattern" target="_blank">Wikipedia Visitor pattern</a> article in Rust. Short, isolated examples like these help us grasp the underlying theory more effectively.*

*We won’t be discussing the theory of the visitor pattern in this post.*

<h3>
🦀 <a href="https://github.com/behai-nguyen/rlox" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![140-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/06/140-feature-image.png) |
|:--:|
| *Visitor Pattern with Rust* |

<p>
<strong>For each of the C# and Java examples,</strong> we will first present an equivalent 
Rust implementation using <code>enum</code>, followed by an alternative approach using 
<code>trait</code>s. We will also extend the original examples by introducing additional 
components to demonstrate that our Rust code behaves as intended.
</p>

<a id="c-sharp-example"></a>
<p>
❶ <strong>Implementing the <a href="https://en.wikipedia.org/wiki/Visitor_pattern" 
title="Wikipedia: Visitor pattern C# example" target="_blank">C# Example</a> 
in Rust</strong>
</p>

<a id="c-sharp-example-enum"></a>
<!-- Master file: src\c_sharp-02.rs -->
<p>
⓵ <strong>Rust <code>enum</code> Implementation</strong>
</p>

<p>
In this implementation, we use an <code>enum</code> to represent each of the expression 
types: <code>Literal</code> and <code>Addition</code>. The complete code is listed below:
</p>

```rust
// Define enum
pub enum Expression {
    Literal(Literal),
    Addition(Addition)
}

// Visitor Trait
pub trait Visitor<T> {
    fn visit_literal_expression(&self, expression: &Expression) -> T;
    fn visit_addition_expression(&self, expression: &Expression) -> T;
}

pub struct Literal {
    value: f32,
}

impl Literal {
    pub fn new(value: f32) -> Self {
        Literal { value }
    }

    pub fn get_value(&self) -> f32 {
        self.value
    }
}

pub struct Addition {
    pub left: Box<Expression>,
    pub right: Box<Expression>,
}

impl Addition {
    pub fn new(left: Expression, right: Expression) -> Self {
        Addition { 
            left: Box::new(left),
            right: Box::new(right),
        }
    }

    pub fn get_value(&self) -> f32 {
        self.left.get_value() + self.right.get_value()
    }    
}

// Implement accept() for Expression
impl Expression {
    pub fn accept<T>(&self, visitor: &dyn Visitor<T>) -> T {
        match self {
            Expression::Literal(_) => visitor.visit_literal_expression(self),
            Expression::Addition(_) => visitor.visit_addition_expression(self),
        }
    }

    pub fn get_value(&self) -> f32 {
        match self {
            Expression::Literal(lit) => lit.get_value(),
            Expression::Addition(add) => add.get_value(),
        }
    }
}

pub struct ExpressionPrintingVisitor;

impl Visitor<()> for ExpressionPrintingVisitor {
    fn visit_literal_expression(&self, expression: &Expression) -> () {
        if let Expression::Literal(lit) = expression {
            println!("{}", lit.get_value());
        }
    }

    fn visit_addition_expression(&self, expression: &Expression) -> () {
        if let Expression::Addition(add) = expression {
            let left_val = add.left.get_value();
            let right_val = add.right.get_value();
            let sum = add.get_value();
            println!("{} + {} = {}", left_val, right_val, sum);
        }
    }
}

fn main() {
    let visitor = ExpressionPrintingVisitor;

    // Emulate 1 + 2 + 3
    let expr = Expression::Addition(Addition::new(
        Expression::Addition(Addition::new(
            Expression::Literal(Literal::new(1.0)),
            Expression::Literal(Literal::new(2.0)),
        )),
        Expression::Literal(Literal::new(3.0)),
    ));
    
    expr.accept(&visitor);
}
```

<p>
The output is <code>3 + 3 = 6</code> as expected. You can run this code in 
<a href="https://play.rust-lang.org/?version=stable&mode=debug&edition=2024&gist=8dc3a0f790c1ee8bfaa33b577f5baf23" 
title="Rust Playground" target="_blank">Rust Playground</a> to see the result.
</p>

<p>
🦀 To emulate the following expression: <code>(1 + 2) + (3 + 10)</code>:
</p>

```rust
fn main() {
    let visitor = ExpressionPrintingVisitor;

    // (1 + 2) + (3 + 10)
    let expr = Expression::Addition(Addition::new(
        Expression::Addition(Addition::new(
            Expression::Literal(Literal::new(1.0)),
            Expression::Literal(Literal::new(2.0)),
        )),
        Expression::Addition(Addition::new(
            Expression::Literal(Literal::new(3.0)),
            Expression::Literal(Literal::new(10.0)),
        )),
    ));

    expr.accept(&visitor);
}
```

<p>
Run it in 
<a href="https://play.rust-lang.org/?version=stable&mode=debug&edition=2024&gist=f3999070c72bba74e5dbd5e00b3b2fb2" 
title="Rust Playground" target="_blank">Rust Playground</a> to see the output <code>3 + 13 = 16</code>. 
</p>

<a id="c-sharp-example-trait"></a>
<!-- Master file: src\c_sharp-03.rs -->
<p>
⓶ <strong>Rust <code>trait</code> Implementation</strong>
</p>

<p>
We can't simply turn the <code>Expression</code> enum into a <code>trait</code> 
and use it as <a href="#c-sharp-example-enum">shown previously</a>, since the 
<code>accept</code> method involves generic type parameters. As a result, 
<code>Expression</code> cannot be used as a trait object. For example:
</p>

```rust
pub struct Addition {
    pub left: Box<dyn Expression>,
    pub right: Box<dyn Expression>,
}
```

<p>
would result in <a href="https://doc.rust-lang.org/error_codes/E0038.html" 
title="Error code E0038" target="_blank">E0038</a>. Instead, we define another trait 
that owns the <code>accept</code> method. The complete code is listed below: 
</p>

```rust
pub trait ExpressionVisitor {
    fn visit_literal(&self, literal: &Literal);
    fn visit_addition(&self, addition: &Addition);
}

pub trait ExpressionBase {
    fn accept(&self, visitor: &dyn ExpressionVisitor);
    fn get_value(&self) -> f32;
}

pub struct Literal {
    value: f32,
}

impl Literal {
    pub fn new(value: f32) -> Self {
        Literal { value }
    }

    pub fn get_value(&self) -> f32 {
        self.value
    }
}

impl ExpressionBase for Literal {
    fn accept(&self, visitor: &dyn ExpressionVisitor) {
        visitor.visit_literal(self);
    }

    fn get_value(&self) -> f32 {
        self.get_value()
    }
}

pub struct Addition {
    left: Box<dyn ExpressionBase>,
    right: Box<dyn ExpressionBase>,
}

impl Addition {
    pub fn new(left: Box<dyn ExpressionBase>, right: Box<dyn ExpressionBase>) -> Self {
        Addition { left, right }
    }

    pub fn get_value(&self) -> f32 {
        self.left.get_value() + self.right.get_value()
    }
}

impl ExpressionBase for Addition {
    fn accept(&self, visitor: &dyn ExpressionVisitor) {
        visitor.visit_addition(self);
    }

    fn get_value(&self) -> f32 {
        self.get_value()
    }
}

pub struct ExpressionPrintingVisitor;

impl ExpressionVisitor for ExpressionPrintingVisitor {
    fn visit_literal(&self, literal: &Literal) {
        println!("{}", literal.get_value());
    }

    fn visit_addition(&self, addition: &Addition) {
        let left = addition.left.get_value();
        let right = addition.right.get_value();
        let sum = addition.get_value();
        println!("{} + {} = {}", left, right, sum);
    }
}

fn main() {
    let visitor = ExpressionPrintingVisitor;

    // Emulate 1 + 2 + 3
    let expr: Box<dyn ExpressionBase> = Box::new(Addition::new(
        Box::new(Addition::new(
            Box::new(Literal::new(1.0)),
            Box::new(Literal::new(2.0)),
        )),
        Box::new(Literal::new(3.0)),
    ));

    expr.accept(&visitor);

    // Emulate (1 + 2) + (3 + 10)
    let expr: Box<dyn ExpressionBase> = Box::new(Addition::new(
        Box::new(Addition::new(
            Box::new(Literal::new(1.0)),
            Box::new(Literal::new(2.0)),
        )),
        Box::new(Addition::new(
            Box::new(Literal::new(3.0)),
            Box::new(Literal::new(10.0)),
        )),
    ));

    expr.accept(&visitor);    
}
```

<p>
Run it in 
<a href="https://play.rust-lang.org/?version=stable&mode=debug&edition=2024&gist=46ff0556cfc903f7572e903a11f4bf0e" 
title="Rust Playground" target="_blank">Rust Playground</a>. The expected output is:
</p>

```
3 + 3 = 6
3 + 13 = 16
```

<a id="c-sharp-example-trait-with-subtraction"></a>
<!-- Master file: src\c_sharp-04.rs -->
<p>
⓷ <strong>Rust <code>trait</code> Implementation with a <code>Subtraction</code> Expression</strong>
</p>

<p>
The <code>Subtraction</code> expression type closely resembles <code>Addition</code>. 
The complete code is below:
</p>

```rust
pub trait ExpressionVisitor {
    fn visit_literal(&self, literal: &Literal);
    fn visit_addition(&self, addition: &Addition);
    fn visit_subtraction(&self, subtraction: &Subtraction);
}

pub trait ExpressionBase {
    fn accept(&self, visitor: &dyn ExpressionVisitor);
    fn get_value(&self) -> f32;
}

pub struct Literal {
    value: f32,
}

impl Literal {
    pub fn new(value: f32) -> Self {
        Literal { value }
    }

    pub fn get_value(&self) -> f32 {
        self.value
    }
}

impl ExpressionBase for Literal {
    fn accept(&self, visitor: &dyn ExpressionVisitor) {
        visitor.visit_literal(self);
    }

    fn get_value(&self) -> f32 {
        self.get_value()
    }
}

pub struct Addition {
    left: Box<dyn ExpressionBase>,
    right: Box<dyn ExpressionBase>,
}

impl Addition {
    pub fn new(left: Box<dyn ExpressionBase>, right: Box<dyn ExpressionBase>) -> Self {
        Addition { left, right }
    }

    pub fn get_value(&self) -> f32 {
        self.left.get_value() + self.right.get_value()
    }
}

impl ExpressionBase for Addition {
    fn accept(&self, visitor: &dyn ExpressionVisitor) {
        visitor.visit_addition(self);
    }

    fn get_value(&self) -> f32 {
        self.get_value()
    }
}

pub struct Subtraction {
    left: Box<dyn ExpressionBase>,
    right: Box<dyn ExpressionBase>,
}

impl Subtraction {
    pub fn new(left: Box<dyn ExpressionBase>, right: Box<dyn ExpressionBase>) -> Self {
        Subtraction { left, right }
    }

    pub fn get_value(&self) -> f32 {
        self.left.get_value() - self.right.get_value()
    }
}

impl ExpressionBase for Subtraction {
    fn accept(&self, visitor: &dyn ExpressionVisitor) {
        visitor.visit_subtraction(self);
    }

    fn get_value(&self) -> f32 {
        self.get_value()
    }
}

pub struct ExpressionPrintingVisitor;

impl ExpressionVisitor for ExpressionPrintingVisitor {
    fn visit_literal(&self, literal: &Literal) {
        println!("{}", literal.get_value());
    }

    fn visit_addition(&self, addition: &Addition) {
        let left = addition.left.get_value();
        let right = addition.right.get_value();
        let sum = addition.get_value();
        println!("{} + {} = {}", left, right, sum);
    }

    fn visit_subtraction(&self, subtraction: &Subtraction) {
        let left = subtraction.left.get_value();
        let right = subtraction.right.get_value();
        let difference = subtraction.get_value();
        println!("{} - {} = {}", left, right, difference);
    }
}

fn main() {
    let visitor = ExpressionPrintingVisitor;

    // Emulate (1 + 2) + 3
    let expr: Box<dyn ExpressionBase> = Box::new(Addition::new(
        Box::new(Addition::new(
            Box::new(Literal::new(1.0)),
            Box::new(Literal::new(2.0)),
        )),
        Box::new(Literal::new(3.0)),
    ));

    expr.accept(&visitor);

    // Emulate 1 - 2 = -1
    let expr: Box<dyn ExpressionBase> = Box::new(Subtraction::new(
        Box::new(Literal::new(1.0)),
        Box::new(Literal::new(2.0))
    ));

    expr.accept(&visitor);

    // Emulate (1 - 2) + 8 = 7
    let expr: Box<dyn ExpressionBase> = Box::new(Addition::new(
        Box::new(Subtraction::new(
            Box::new(Literal::new(1.0)),
            Box::new(Literal::new(2.0))
        )),
        Box::new(Literal::new(8.0))
    ));

    expr.accept(&visitor);
}
```

<p>
Running it in 
<a href="https://play.rust-lang.org/?version=stable&mode=debug&edition=2024&gist=aa1afa92103209bb67d739fa6630b59d" 
title="Rust Playground" target="_blank">Rust Playground</a> gives this output:
</p>

```
3 + 3 = 6
1 - 2 = -1
-1 + 8 = 7
```

<a id="java-example"></a>
<p>
❷ <strong>Implementing the <a href="https://en.wikipedia.org/wiki/Visitor_pattern" 
title="Wikipedia: Visitor pattern Java example" target="_blank">Java Example</a> 
in Rust</strong>
</p>

<a id="java-example-enum"></a>
<!-- Master file: src\java_car-02.rs -->
<p>
⓵ <strong>Rust <code>enum</code> Implementation</strong>
</p>

<p>
In this version, we treat <code>Car</code> as just another <code>CarElement</code> 
and visit it like any other part. The complete code is listed below:
</p>

```rust
#[derive(Clone)]
pub struct Wheel {
    name: String,
}

impl Wheel {
    pub fn new(name: &str) -> Self {
        Wheel { name: name.to_string() }
    }

    pub fn get_name(&self) -> &str {
        self.name.as_str()
    }
}

#[derive(Clone)]
pub struct Body;

#[derive(Clone)]
pub struct Engine;

#[derive(Clone)]
pub struct Car {
    elements: Vec<Box<CarElement>>,
}

impl Car {
    pub fn new() -> Self {
        let mut car = Car {
            elements: vec![
                Box::new(CarElement::Wheel(Wheel::new("front left"))),
                Box::new(CarElement::Wheel(Wheel::new("front right"))),
                Box::new(CarElement::Wheel(Wheel::new("back left"))),
                Box::new(CarElement::Wheel(Wheel::new("back right"))),
                Box::new(CarElement::Body(Body {})),
                Box::new(CarElement::Engine(Engine {})),
            ]
        };

        // Add the car itself as a CarElement
        car.elements.push(Box::new(CarElement::Car(car.clone())));
        car
    }

    pub fn accept(&self, visitor: &dyn CarElementVisitor) {
        for element in &self.elements {
            element.accept(visitor);
        }
        visitor.visit_car(self);
    }

    pub fn get_elements(&self) -> &Vec<Box<CarElement>> {
        &self.elements
    }
}

// Define enum. 
#[derive(Clone)]
pub enum CarElement {
    Wheel(Wheel),
    Body(Body),
    Engine(Engine),
    Car(Car),
}

// CarElementVisitor Trait
pub trait CarElementVisitor {
    fn visit_body(&self, body: &Body);
    fn visit_car(&self, car: &Car);
    fn visit_engine(&self, engine: &Engine);
    fn visit_wheel(&self, wheel: &Wheel);
}

// Implement accept() for CarElement
impl CarElement {
    pub fn accept(&self, visitor: &dyn CarElementVisitor) {
        match self {
            CarElement::Body(body) => visitor.visit_body(body),
            CarElement::Car(car) => visitor.visit_car(car),
            CarElement::Engine(engine) => visitor.visit_engine(engine),
            CarElement::Wheel(wheel) => visitor.visit_wheel(wheel),
        }
    }
}

pub struct CarElementDoVisitor;

impl CarElementVisitor for CarElementDoVisitor {
    fn visit_body(&self, _: &Body) {
        println!("Moving my body");
    }

    fn visit_car(&self, _: &Car) {
        println!("Starting my car");
    }

    fn visit_engine(&self, _: &Engine) {
        println!("Starting my engine");
    }

    fn visit_wheel(&self, wheel: &Wheel) {
        println!("Kicking my {} wheel", wheel.get_name());
    }
}

pub struct CarElementPrintVisitor;

impl CarElementVisitor for CarElementPrintVisitor {
    fn visit_body(&self, _: &Body) {
        println!("Visiting body");
    }

    fn visit_car(&self, _: &Car) {
        println!("Visiting car");
    }

    fn visit_engine(&self, _: &Engine) {
        println!("Visiting engine");
    }

    fn visit_wheel(&self, wheel: &Wheel) {
        println!("Visiting {} wheel", wheel.get_name());
    }    
}

fn main() {
    let print_visitor = CarElementPrintVisitor;
    let do_visitor = CarElementDoVisitor;

    let car = Car::new();

    for element in car.get_elements() {
        element.accept(&print_visitor);
    }

    for element in car.get_elements() {
        element.accept(&do_visitor);
    }
}
```

<p>
Run it in 
<a href="https://play.rust-lang.org/?version=stable&mode=debug&edition=2024&gist=384eef097922bb7b408c0f62912166b3" 
title="Rust Playground" target="_blank">Rust Playground</a> and observe that the output 
matches the <a href="https://en.wikipedia.org/wiki/Visitor_pattern" 
title="Wikipedia: Visitor pattern Java example" target="_blank">Java example</a> 
on Wikipedia:
</p>

```
Visiting front left wheel
Visiting front right wheel
Visiting back left wheel
Visiting back right wheel
Visiting body
Visiting engine
Visiting car
Kicking my front left wheel
Kicking my front right wheel
Kicking my back left wheel
Kicking my back right wheel
Moving my body
Starting my engine
Starting my car
```

<a id="java-example-trait"></a>
<!-- Master file: src\c_sharp-03.rs -->
<p>
⓶ <strong>Rust <code>trait</code> Implementation</strong>
</p>

<p>
Since the <code>accept</code> method doesn't have generic parameters, the trait-based 
implementation mirrors the earlier enum version. The complete code:
</p>

```rust
pub trait CarElementVisitor {
    fn visit_wheel(&self, wheel: &Wheel);
    fn visit_body(&self, body: &Body);
    fn visit_engine(&self, engine: &Engine);
    fn visit_car(&self, car: &Car);
}

pub trait CarElement {
    fn accept(&self, visitor: &dyn CarElementVisitor);
}

pub struct Wheel {
    name: String,
}

impl Wheel {
    pub fn new(name: &str) -> Self {
        Wheel { name: name.to_string() }
    }

    pub fn get_name(&self) -> &str {
        &self.name
    }
}

impl CarElement for Wheel {
    fn accept(&self, visitor: &dyn CarElementVisitor) {
        visitor.visit_wheel(self);
    }
}

pub struct Body;

impl CarElement for Body {
    fn accept(&self, visitor: &dyn CarElementVisitor) {
        visitor.visit_body(self);
    }
}

pub struct Engine;

impl CarElement for Engine {
    fn accept(&self, visitor: &dyn CarElementVisitor) {
        visitor.visit_engine(self);
    }
}

pub struct Car {
    elements: Vec<Box<dyn CarElement>>,
}

impl Car {
    pub fn new() -> Self {
        Car {
            elements: vec![
                Box::new(Wheel::new("front left")),
                Box::new(Wheel::new("front right")),
                Box::new(Wheel::new("back left")),
                Box::new(Wheel::new("back right")),
                Box::new(Body),
                Box::new(Engine),
            ],
        }
    }
}

impl CarElement for Car {
    fn accept(&self, visitor: &dyn CarElementVisitor) {
        for element in &self.elements {
            element.accept(visitor);
        }
        visitor.visit_car(self);
    }
}

pub struct CarElementPrintVisitor;

impl CarElementVisitor for CarElementPrintVisitor {
    fn visit_wheel(&self, wheel: &Wheel) {
        println!("Visiting {} wheel", wheel.get_name());
    }

    fn visit_body(&self, _: &Body) {
        println!("Visiting body");
    }

    fn visit_engine(&self, _: &Engine) {
        println!("Visiting engine");
    }

    fn visit_car(&self, _: &Car) {
        println!("Visiting car");
    }
}

pub struct CarElementDoVisitor;

impl CarElementVisitor for CarElementDoVisitor {
    fn visit_body(&self, _: &Body) {
        println!("Moving my body");
    }

    fn visit_car(&self, _: &Car) {
        println!("Starting my car");
    }

    fn visit_engine(&self, _: &Engine) {
        println!("Starting my engine");
    }

    fn visit_wheel(&self, wheel: &Wheel) {
        println!("Kicking my {} wheel", wheel.get_name());
    }
}

fn main() {
    let car = Car::new();

    let print_visitor = CarElementPrintVisitor;
    let do_visitor = CarElementDoVisitor;

    car.accept(&print_visitor);
    car.accept(&do_visitor);
}
```

<p>
The output should be identical—see it in 
<a href="https://play.rust-lang.org/?version=stable&mode=debug&edition=2024&gist=3ef5ad48f71cac9abe7d2afe26aa94be" 
title="Rust Playground" target="_blank">Rust Playground</a>.
</p>

<a id="java-example-trait-with-dashboard"></a>
<!-- Master file: src\java_car-05.rs -->
<p>
⓷ <strong>Rust <code>trait</code> Implementation with a <code>Dashboard</code> Element</strong>
</p>

<p>
For illustration, <code>Dashboard</code> will contain five fields. We also implement the 
<a href="https://doc.rust-lang.org/std/fmt/trait.Display.html" title="Trait Display" 
target="_blank">Display trait</a> to make the visit output more idiomatic.
</p>

<p>
<code>Dashboard</code> is now a component of <code>Car</code>, so instantiating 
a car includes a dashboard. Full code:
</p>

```rust
use std::fmt;

pub trait CarElementVisitor {
    fn visit_wheel(&self, wheel: &Wheel);
    fn visit_body(&self, body: &Body);
    fn visit_engine(&self, engine: &Engine);
    fn visit_car(&self, car: &Car);
    fn visit_dashboard(&self, dashboard: &Dashboard);
}

pub trait CarElement {
    fn accept(&self, visitor: &dyn CarElementVisitor);
}

pub struct Wheel {
    name: String,
}

impl Wheel {
    pub fn new(name: &str) -> Self {
        Wheel { name: name.to_string() }
    }

    pub fn get_name(&self) -> &str {
        &self.name
    }
}

impl CarElement for Wheel {
    fn accept(&self, visitor: &dyn CarElementVisitor) {
        visitor.visit_wheel(self);
    }
}

pub struct Body;

impl CarElement for Body {
    fn accept(&self, visitor: &dyn CarElementVisitor) {
        visitor.visit_body(self);
    }
}

pub struct Engine;

impl CarElement for Engine {
    fn accept(&self, visitor: &dyn CarElementVisitor) {
        visitor.visit_engine(self);
    }
}

pub struct Dashboard {
    screen_size_in_inches: f32,
    has_navigation: bool,
    display_type: String,
    num_buttons: u8,
    language: Option<String>,
}

impl fmt::Display for Dashboard {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let language = self.language.as_deref().unwrap_or("not specified");

        write!(f, 
            "Screen Size: {}\", GPS: {}, Display Type: {}, Number of Buttons: {}, Language: {}",
            self.screen_size_in_inches,
            self.has_navigation,
            self.display_type,
            self.num_buttons,
            language
        )        
    }
}

impl Dashboard {
    pub fn new(screen_size_in_inches: f32, 
        has_navigation: bool, 
        display_type: &str,
        num_buttons: u8,
        language: Option<String>,
    ) -> Self {
        Dashboard {
            screen_size_in_inches,
            has_navigation,
            display_type: display_type.to_string(),
            num_buttons,
            language,
        }
    }
}

impl CarElement for Dashboard {
    fn accept(&self, visitor: &dyn CarElementVisitor) {
        visitor.visit_dashboard(self);
    }
}

pub struct Car {
    elements: Vec<Box<dyn CarElement>>,
}

impl Car {
    pub fn new() -> Self {
        Car {
            elements: vec![
                Box::new(Wheel::new("front left")),
                Box::new(Wheel::new("front right")),
                Box::new(Wheel::new("back left")),
                Box::new(Wheel::new("back right")),
                Box::new(Body),
                Box::new(Engine),
                Box::new(Dashboard::new(12.00,
                    false, "OLED", 6, Some(String::from("English")))),
            ],
        }
    }
}

impl CarElement for Car {
    fn accept(&self, visitor: &dyn CarElementVisitor) {
        for element in &self.elements {
            element.accept(visitor);
        }
        visitor.visit_car(self);
    }
}

pub struct CarElementPrintVisitor;

impl CarElementVisitor for CarElementPrintVisitor {
    fn visit_wheel(&self, wheel: &Wheel) {
        println!("Visiting {} wheel", wheel.get_name());
    }

    fn visit_body(&self, _: &Body) {
        println!("Visiting body");
    }

    fn visit_engine(&self, _: &Engine) {
        println!("Visiting engine");
    }

    fn visit_car(&self, _: &Car) {
        println!("Visiting car");
    }

    fn visit_dashboard(&self, dashboard: &Dashboard) {
        println!("Visiting dashboard: {}", dashboard);
    }
}

pub struct CarElementDoVisitor;

impl CarElementVisitor for CarElementDoVisitor {
    fn visit_body(&self, _: &Body) {
        println!("Moving my body");
    }

    fn visit_car(&self, _: &Car) {
        println!("Starting my car");
    }

    fn visit_engine(&self, _: &Engine) {
        println!("Starting my engine");
    }

    fn visit_wheel(&self, wheel: &Wheel) {
        println!("Kicking my {} wheel", wheel.get_name());
    }

    fn visit_dashboard(&self, dashboard: &Dashboard) {
        println!("Navigating using dashboard: {}", dashboard);
    }
}

fn main() {
    let car = Car::new();

    let print_visitor = CarElementPrintVisitor;
    let do_visitor = CarElementDoVisitor;

    car.accept(&print_visitor);
    car.accept(&do_visitor);
}
```

<p>
Run it in 
<a href="https://play.rust-lang.org/?version=stable&mode=debug&edition=2024&gist=ddf95436b30c6e7fde90749f02d891d9" 
title="Rust Playground" target="_blank">Rust Playground</a>. You should see:
</p>

```
Visiting front left wheel
Visiting front right wheel
Visiting back left wheel
Visiting back right wheel
Visiting body
Visiting engine
Visiting dashboard: Screen Size: 12", GPS: false, Display Type: OLED, Number of Buttons: 6, Language: English
Visiting car
Kicking my front left wheel
Kicking my front right wheel
Kicking my back left wheel
Kicking my back right wheel
Moving my body
Starting my engine
Navigating using dashboard: Screen Size: 12", GPS: false, Display Type: OLED, Number of Buttons: 6, Language: English
Starting my car
```

<a id="concluding-remarks"></a>
<p>
❸ As stated at the outset, this post documents my personal journey toward understanding the 
<a href="https://www.google.com/search?q=visitor+pattern&sca_esv=031453346484e3fe&sxsrf=AE3TifMt1Zv09mlol6xvyuLSIe-SuQ8RVw%3A1750945325549&source=hp&ei=LU5daNi5GZjc2roPj7nA-Q0&iflsig=AOw8s4IAAAAAaF1cParYGjGJNLFkiCZUR2Fzc8uzg2FT&ved=0ahUKEwiYhJLRm4-OAxUYrlYBHY8cMN8Q4dUDCBk&uact=5&oq=visitor+pattern&gs_lp=Egdnd3Mtd2l6GgIYAyIPdmlzaXRvciBwYXR0ZXJuMgoQIxiABBgnGIoFMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIIEAAYgAQYiwMyCBAAGIAEGIsDMgUQABiABDIIEAAYgAQYiwMyCBAAGIAEGIsDSIkpUABY7iZwAngAkAEAmAGuAqABkRuqAQcwLjkuNy4xuAEDyAEA-AEBmAIToAKeHMICFBAuGIAEGJECGLEDGNEDGMcBGIoFwgILEAAYgAQYkQIYigXCAg4QLhiABBixAxiDARiKBcICCxAuGIAEGNEDGMcBwgIIEAAYgAQYsQPCAhoQLhiABBixAxjRAxjSAxiDARjHARioAxiLA8ICBBAjGCfCAhAQLhiABBhDGMcBGIoFGK8BwgINEAAYgAQYQxiKBRiLA8ICHBAuGIAEGEMYpgMYxwEYqAMYigUYiwMYjgUYrwHCAgoQABiABBhDGIoFwgIdEC4YgAQYkQIYsQMY0QMY0gMYxwEYqAMYigUYiwPCAg4QABiABBiRAhiKBRiLA8ICChAuGIAEGEMYigXCAg0QABiABBixAxhDGIoFwgIUEC4YgAQYpgMYxwEYqAMYiwMYrwHCAhMQLhiABBhDGMcBGIoFGI4FGK8BwgIWEC4YgAQYsQMY0QMYQxiDARjHARiKBcICERAuGIAEGLEDGIMBGMcBGK8BwgIUEC4YgAQYkQIYxwEYigUYjgUYrwHCAgsQLhiABBjHARivAcICDhAuGIAEGLEDGNEDGMcBwgIHECMYsQIYJ8ICChAAGIAEGLEDGArCAgcQABiABBgKwgINEC4YgAQYxwEYChivAcICExAuGIAEGLEDGIMBGMcBGAoYrwHCAgsQABiABBixAxiDAcICCxAAGIAEGLEDGIoFwgIOEC4YgAQYxwEYjgUYrwGYAwCSBwcyLjcuOS4xoAesrAGyBwcwLjcuOS4xuAeHHMIHBjItMTMuNsgHdg&sclient=gws-wiz" 
title="Google search: visitor pattern" target="_blank">visitor pattern</a>. 
It is not meant to be a tutorial.
</p>

<p>
Thank you for reading. I hope you find this post helpful. Stay safe, as always.
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
<a href="https://www.wannapik.com/vectors/21725" target="_blank">https://www.wannapik.com/vectors/21725</a>
</li>
</ul>

<h3>
🦀 <a href="https://github.com/behai-nguyen/rlox" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>
