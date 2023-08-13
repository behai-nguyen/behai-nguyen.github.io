---
layout: post
title: "Rust: baby step -- a trait function which returns values of different data types."

description: Using associated type, we can have a trait function to return values of different data types for different implementations.
tags:
- Rust
- trait
- associated type
---

<em style="color:#111;">Using <code>associated type</code>, we can have a trait function to return values of different data types for different implementations.</em>

| ![078-feature-image.png](https://behainguyen.files.wordpress.com/2023/08/078-feature-image.png) |
|:--:|
| *Rust: baby step -- a trait function which returns values of different data types.* |

I would like a <code>trait</code> method to return data of <code>u32</code>,
<code>f32</code> and <code>String</code> for different implementations.
In Delphi, it would look like the below:

```pascal
type
  IExecutor = interface
  ['{5EC47E9D-4FF5-4DB4-9326-CD6324594A6E}']
    function Execute(): Variant;
```

I thought <code>Option&lt;Box&lt;dyn Any>></code> would be the return
type to use. After a while, with the compiler helps, I came up with:

```rust
use std::any::Any;

pub trait Executor {
    fn execute(&self) -> Option<Box<dyn Any>>;
}

pub struct Actor1 {}

pub struct Actor2 {}

pub struct Actor3 {}

impl Executor for Actor1 {
    fn execute(&self) -> Option<Box<dyn Any>> {
        Some(Box::new(234))
    }
}

impl Executor for Actor2 {
    fn execute(&self) -> Option<Box<dyn Any>> {
        Some(Box::new(12.04))
    }
}

impl Executor for Actor3 {
    fn execute(&self) -> Option<Box<dyn Any>> {
        Some(Box::new(String::from("Test string.")))
    }
}

fn main() {
    let actor = Actor1{};
    let result = actor.execute();
    println!("actor.execute(): {:?}", result);
    
    // TO_DO: how to 'extract' 234 to a u32 variable, please?

    let actor = Actor2{};
    let result = actor.execute();
    println!("actor.execute(): {:?}", result);

    // TO_DO: how to 'extract' 12.04 to a f32 variable, please?

    let actor = Actor3{};
    let result = actor.execute();
    println!("actor.execute(): {:?}", result);    

    // TO_DO: how to 'extract' "Test string." to a string variable, please?
}
```

It produces the following output:

```
actor.execute(): Some(Any { .. })
actor.execute(): Some(Any { .. })
actor.execute(): Some(Any { .. })
```

I tried to extract the concrete values out, but I have not been able to.
I posted to the Rust Users Community Forum to request help: 
<a href="https://users.rust-lang.org/t/how-extract-concrete-value-from-option-box-dyn-any/98296"
title="How extract concrete value from Option<Box<dyn Any>>?" 
target="_blank">How extract concrete value from Option&lt;Box&lt;dyn Any&gt;&gt;?</a>

And I was advised to use <code>associated type</code>. I did follow the advice. 
And I have been able to extract the concrete values out. The <code>main()</code> 
function is a bit long, but it is straightforward:

```rust
pub trait Executor {
    type Output;
    fn execute(&self) -> Option<Self::Output>;
}

pub struct Actor1 {}

pub struct Actor2 {}

pub struct Actor3 {}

impl Executor for Actor1 {
    type Output = u32;
    fn execute(&self) -> Option<Self::Output> {
        Some(234)
    }
}

impl Executor for Actor2 {
    type Output = f32;
    fn execute(&self) -> Option<Self::Output> {
        Some(12.04)
    }    
}

impl Executor for Actor3 {
    type Output = String;
    fn execute(&self) -> Option<Self::Output> {
        Some(String::from("Test string."))
    }    
}

fn main() {
    // Actor1.

    let actor = Actor1{};
    let result = actor.execute();
    
    let u32_value1: u32;
    if let Some(value) = result {
        u32_value1 = value;        
    }
    else {
        u32_value1 = 0;        
    }
    assert_eq!(234, u32_value1);

    //
    // We can also use mutable and initalise the variable to 0,
    // if we do not need the else block.
    //
    let mut u32_value2: u32 = 0;
    if let Some(value) = result {
        u32_value2 = value;        
    }
    assert_eq!(234, u32_value2);

    // And of course, there is also match.
    let mut u32_value3: u32 = 0;
    match result {
        Some(value) => u32_value3 = value,
        _ => println!("Actor1 failed."),
    }

    assert_eq!(234, u32_value3);

    // Actor2.

    let actor = Actor2{};
    let result = actor.execute();

    let mut f32_value: f32 = 0.0;
    match result {
        Some(value) => f32_value = value,
        _ => println!("Actor2 failed."),
    }

    assert_eq!(12.04, f32_value);

    // Actor3.

    let actor = Actor3{};
    let result = actor.execute();

    let mut str_value = String::from("");
    match result {
        Some(value) => str_value.push_str(&value),
        _ => println!("Actor3 failed."),
    }

    assert_eq!("Test string.", str_value);
}
```

<code>Associated type</code> is also covered in 
<a href="https://doc.rust-lang.org/book/" title="“the book”" target="_blank">“the book”</a>,
chapter 19, section 
<a href="https://doc.rust-lang.org/book/ch19-03-advanced-traits.html#advanced-traits"
title="Advanced Traits" target="_blank">Advanced Traits</a> -- I did go over it, but 
obviously I did not remember 😂 anything about it...

I do hope you find this post relevant. Thank you for reading and 
stay safe as always.

✿✿✿

Feature image source:

<ul>
<li>
<a href="https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper" target="_blank">https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper</a>
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
</ul>