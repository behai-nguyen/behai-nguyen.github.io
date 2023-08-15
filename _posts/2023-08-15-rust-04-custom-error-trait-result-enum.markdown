---
layout: post
title: "Rust: baby step -- using our own Error trait in Result enum."

description: Implementing our own custom Error trait to use in Result enum.
tags:
- Rust
- Error trait
- Result enum
---

<em style="color:#111;">Implementing our own custom <code>Error trait</code> to use in <code>Result enum</code>.</em>

| ![079-feature-image.png](https://behainguyen.files.wordpress.com/2023/08/079-feature-image.png) |
|:--:|
| *Rust: baby step -- using our own Error trait in Result enum.* |

In languages such as Delphi and Python, we can define our own 
exceptions, and raise them when we need to. Similarly, in Rust, 
we can define our own custom <code>Error traits</code> to use 
in <code>Result&lt;T, E&gt;</code>.

The primary sources of references for this post are 
<a href="https://doc.rust-lang.org/std/"
title="The Rust Standard Library" target="_blank">The Rust Standard Library</a>
and chapter 
<a href="https://doc.rust-lang.org/book/ch09-00-error-handling.html"
title="Error Handling" target="_blank">Error Handling</a> from 
<a href="https://doc.rust-lang.org/book/" title="“the book”" target="_blank">“the book”</a>:

<ol>
<li style="margin-top:10px;">
<a href="https://doc.rust-lang.org/std/error/trait.Error.html"
title="Trait std::error::Error" target="_blank">Trait std::error::Error</a>
</li>

<li style="margin-top:10px;">
<a href="https://doc.rust-lang.org/std/fmt/trait.Display.html"
title="Trait std::fmt::Display" target="_blank">Trait std::fmt::Display</a>
</li>

<li style="margin-top:10px;">
<a href="https://doc.rust-lang.org/std/fmt/trait.Debug.html"
title="Trait std::fmt::Debug" target="_blank">Trait std::fmt::Debug</a>
</li>

<li style="margin-top:10px;">
<a href="https://doc.rust-lang.org/std/result/enum.Result.html"
title="Enum std::result::Result" target="_blank">Enum std::result::Result</a>
</li>

<li style="margin-top:10px;">
<a href="https://doc.rust-lang.org/book/ch09-00-error-handling.html"
title="Chapter 9: Error Handling" target="_blank">Chapter 9: Error Handling</a> 
section 
<a href="https://doc.rust-lang.org/book/ch09-02-recoverable-errors-with-result.html"
title="Recoverable Errors with Result"
target="_blank">Recoverable Errors with <code>Result</code></a> in 
<a href="https://doc.rust-lang.org/book/" title="“the book”" target="_blank">“the book”</a>.
</li>
</ol>

As a Rust beginner, I find 
<a href="https://doc.rust-lang.org/std/"
title="The Rust Standard Library" target="_blank">The Rust Standard Library</a> 
very helpful, it is concise and to the point. I feel that it complements
<a href="https://doc.rust-lang.org/book/" title="“the book”" target="_blank">“the book”</a>
quite nicely.

⓵ <a href="https://doc.rust-lang.org/std/error/trait.Error.html"
title="Trait std::error::Error" target="_blank">Trait std::error::Error</a> 
-- describes the basic requirements to implement our own <code>Error</code>
trait: we've to implement the 
<a href="https://doc.rust-lang.org/std/fmt/trait.Display.html"
title="Trait std::fmt::Display" target="_blank">Display</a> and 
<a href="https://doc.rust-lang.org/std/fmt/trait.Debug.html"
title="Trait std::fmt::Debug" target="_blank">Debug</a> traits.

And this:

> Error messages are typically concise lowercase sentences without trailing punctuation:
>
> ```rust
> let err = "NaN".parse::<u32>().unwrap_err();
> assert_eq!(err.to_string(), "invalid digit found in string");
> ```

⓶ <a href="https://doc.rust-lang.org/std/fmt/trait.Display.html"
title="Trait std::fmt::Display" target="_blank">Trait std::fmt::Display</a> --
helpful examples on how to implement this trait.

⓷ <a href="https://doc.rust-lang.org/std/fmt/trait.Debug.html"
title="Trait std::fmt::Debug" target="_blank">Trait std::fmt::Debug</a> -- 
I pay special attention to the discussions on derived implementation 
and manual implementation. I elect to use the later.

⓸ <a href="https://doc.rust-lang.org/std/result/enum.Result.html"
title="Enum std::result::Result" target="_blank">Enum std::result::Result</a> -- 
concise information on this enum. The main point for me is that 
<code>Ok(T)</code> and <code>Err(E)</code> are mutually exclusive.

The <code>Error</code> trait which I've in mind is simple: it has a 
single string field which is the error message itself. Based on the 
info in the above references, I came up with the following:

```rust
use std::fmt;

pub struct BhError {
    err_msg: String
}

impl BhError {
    fn new(msg: &str) -> BhError {
        BhError{err_msg: msg.to_string()}
    }
}

impl fmt::Debug for BhError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("BhError")
            .field("err_msg", &self.err_msg)
            .finish()
    }
}

impl fmt::Display for BhError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f,"{}", self.err_msg)
    }
}
```

⓵ It should display correctly for formats <code>{:?}</code> and 
<code>{:#?}</code>. ⓶ And <code>to_string()</code> method should
return the actual error text. To keep the post simple, we will not 
write tests, but just write output to the console for manual 
verifications. We can test it with:

```rust
fn main() {
    let err = BhError::new("this is a test error");
    println!("{:?}\n", err);
    println!("{:#?}\n", err);
    println!("{err:?}\n\n");
	
    println!("{}", err.to_string());
}
```

And the output is what we expect:

```
behai@hp-pavilion-15:~/rust/errors$ rustc src/example_01.rs
behai@hp-pavilion-15:~/rust/errors$ /home/behai/rust/errors/example_01
BhError { err_msg: "this is a test error" }

BhError {
    err_msg: "this is a test error",
}

BhError { err_msg: "this is a test error" }


this is a test error
behai@hp-pavilion-15:~/rust/errors$
```

Let's use it in <a href="https://doc.rust-lang.org/std/result/enum.Result.html"
title="Enum std::result::Result" target="_blank">Enum std::result::Result</a>.
Suppose we need a function to return an <code>u32</code> value on success, 
otherwise the <code>BhError</code> trait. We can write a mock function as 
follows:

```rust
/// Returns a Result with either a hard-coded ``u32`` value of 234, or 
/// ``BhError`` whose messsage is the value of the argument ``error_text``
/// 
/// # Arguments
/// 
/// * `raise` - ``true`` to return ``BhError``. false to return an 
///     ``u32`` of 234
/// 
/// * `error_text` - test error text. Blank when ``raise`` is ``false``,
///     some text when ``raise`` is ``true``
/// 
fn test_error_raising(raise: bool, error_text: &str) -> Result<u32, BhError> {
    if raise {
        Err(BhError::new(error_text))
    } else {
        Ok(234)
    }
}
```

Let's exam the “valid” case first:

```rust
fn main() {
    //
    // "Valid" test, we don't raise error, test_error_raising(...)
    // returns hard-coded Ok(234).
    // 
    let result = test_error_raising(false, "");

    //
    // For my own assertion that I can copy individual pieces of info out  
    // of the return value.
    //
    let mut u32_value: u32 = 0;
    let mut valid: bool = true;
    let mut error_msg = String::from("");
    match result {
        Ok(value) => u32_value = value,
        Err(error) => {
            valid = false;
            error_msg.push_str(&error.to_string());
        }
    };

    assert_eq!(valid, true);
    assert_eq!(u32_value, 234);
    assert_eq!(&error_msg, "");

    if valid {
        println!("1. u32_value = {}", u32_value);
    }
    else {
        println!("1. In error.\nError = {}", error_msg);
    }
}
```

The code is rather verbose, but not at all complicated. I break 
the return <code>Result&lt;u32, BhError&gt;</code> down into 
individual relevant variables to prove to myself that I understand 
how it works. As expected, the result is <code>234</code> for valid:

```
behai@hp-pavilion-15:~/rust/errors$ rustc src/example_02.rs
behai@hp-pavilion-15:~/rust/errors$ /home/behai/rust/errors/example_02
1. u32_value = 234
behai@hp-pavilion-15:~/rust/errors$
```

Next, the “invalid” case:

```rust
fn main() {
    //
    // "Invalid" test, we raise error, test_error_raising(...)
    // returns Err(BhError::new("behai raises test error")).
    //     
    let result = test_error_raising(true, "behai raises test error");

    let mut u32_value: u32 = 0;
    let mut valid: bool = true;
    let mut error_msg = String::from("");
    match result {
        Ok(value) => u32_value = value,
        Err(error) => {
            valid = false;
            error_msg.push_str(&error.to_string());
        }
    };

    assert_eq!(valid, false);
    assert_eq!(u32_value, 0);
    assert_eq!(&error_msg, "behai raises test error");
    
    if valid {
        println!("2. u32_value = {}", u32_value);
    }
    else {
        println!("2. In error.\nError = {}", error_msg);
    }    
}
```

The structure and the flow of the code are identical to 
the above “valid” case. And we get the error printed out 
as expected:

```rust
behai@hp-pavilion-15:~/rust/errors$ rustc src/example_03.rs
behai@hp-pavilion-15:~/rust/errors$ /home/behai/rust/errors/example_03
2. In error.
Error = behai raises test error
behai@hp-pavilion-15:~/rust/errors$
```

I'm very happy when understood how the <code>Error</code> trait works.
<a href="https://doc.rust-lang.org/std/"
title="The Rust Standard Library" target="_blank">The Rust Standard Library</a> 
is an essential reference. Overall, I'm very happy that
I'm able to complete this post. I hope it is helpful and relevant to somebody...
Thank you for reading and stay safe as always.

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
