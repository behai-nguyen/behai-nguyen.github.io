---
layout: post
title: "Rust: seconds since epoch -- “1970-01-01 00:00:00 UTC”."

description: We look at some simple <em>seconds since epoch</em> calculations std::time and time crate.

tags:
- Rust
- time
- time
- epoch
---

<em>We look at some simple <em>seconds since epoch</em> calculations using <a href="https://doc.rust-lang.org/std/time/index.html" title="std::time" target="_blank">std::time</a> and <a href="https://docs.rs/time/latest/time/" title="Crate time" target="_blank">time</a> crate.</em>

| ![088-feature-image.png](https://behainguyen.files.wordpress.com/2023/11/088-feature-image.png) |
|:--:|
| *Rust: seconds since epoch -- “1970-01-01 00:00:00 UTC”.* |

I've done some <em>seconds since epoch</em> calculations in Python before. I try to do similar calculations in Rust. This is a documentation of the code which I've tried out. These're just simple calculations which enable me to understand this epoch time subject better.

<a id="the-first-example">❶ The first example</a> is from <a href="https://doc.rust-lang.org/std/time/constant.UNIX_EPOCH.html" title="Constant std::time::UNIX_EPOCH" target="_blank">Constant std::time::UNIX_EPOCH</a>, and does not require any third party crate, and can be compiled using <code>rustc</code>:

```
Content of src/main.rs:
```

```rust
use std::time::{SystemTime, UNIX_EPOCH};

fn main() {
    //
    // UNIX_EPOCH: "1970-01-01 00:00:00 UTC"
    //
    match SystemTime::now().duration_since(UNIX_EPOCH) {
        Ok(n) => println!("1970-01-01 00:00:00 UTC was {} seconds ago!", n.as_secs()),
        Err(_) => panic!("SystemTime before UNIX EPOCH!"),
    }
}
```

On both Ubuntu 22.10 and Windows 10, the output looks like:

```
1970-01-01 00:00:00 UTC was 1699787014 seconds ago!
```

Of course, if you happen to run this example, there would be more seconds than in the reported output -- we're getting older by the seconds 😂!

The next examples require <a href="https://docs.rs/time/latest/time/" title="Crate time" target="_blank">time</a> crate. <code>Cargo.toml</code> is common for all examples. Its <code>dependencies</code> section is as follow:

```toml
...
[dependencies]
time = {version = "0.3.22", default-features = false, features = ["formatting", "macros"]}
```

-- We've previously also discussed <a href="https://docs.rs/time/latest/time/" title="Crate time" target="_blank">time</a> crate in a bit more detail in this post <a href="https://behainguyen.wordpress.com/2023/09/03/rust-baby-step-some-preliminary-look-at-date/" title="Rust: baby step -- some preliminary look at date." target="_blank">Rust: baby step -- some preliminary look at date</a>.

<a id="the-second-example">❷ In this second example</a>, I'd like to assert that if we've a date and time just <strong>one (1) second</strong> after <em>the epoch</em>, i.e. <a href="https://docs.rs/time/latest/time/struct.OffsetDateTime.html#associatedconstant.UNIX_EPOCH" title="UNIX_EPOCH" target="_blank">UNIX_EPOCH</a>, then the <strong>seconds since epoch</strong> should be <strong>one (1) second</strong>.

Following is the complete working example, it's compiled with <code>cargo build</code>.

```
Content of src/main.rs:
```

```rust
use time::macros::datetime;
use std::time::{SystemTime, UNIX_EPOCH};

fn main() {
    // "1970-01-01 00:00:01 UTC"
    let offset_dt = datetime!(1970-01-01 0:00:01 UTC);
    let system_time = SystemTime::from(offset_dt);

    println!("offset_dt: {:#?} \n", offset_dt);
    println!("system_time: {:#?} \n", system_time);

    match system_time.duration_since(UNIX_EPOCH) {
        Ok(n) => println!("1970-01-01 00:00:00 UTC was {} seconds ago!", n.as_secs()),
        Err(_) => panic!("SystemTime before UNIX EPOCH!"),
    }
}
```

My Rust version on Windows 10 and Ubuntu 22.10 are the same:

```
F:\rust\datetime>rustc --version
rustc 1.70.0 (90c541806 2023-05-31)

behai@hp-pavilion-15:~/rust/datetime$ rustc --version
rustc 1.70.0 (90c541806 2023-05-31)
```

However, the output is slightly different between the two OSes. On Windows 10:

```
offset_dt: 1970-01-01 0:00:01.0 +00:00:00

system_time: SystemTime {
    intervals: 116444736010000000,
}

1970-01-01 00:00:00 UTC was 1 seconds ago!
```

On Ubuntu 22.10:

```
behai@hp-pavilion-15:~/rust/datetime$ ./target/debug/datetime
offset_dt: 1970-01-01 0:00:01.0 +00:00:00

system_time: SystemTime {
    tv_sec: 1,
    tv_nsec: 0,
}

1970-01-01 00:00:00 UTC was 1 seconds ago!
```

However, both report <strong>one (1) second</strong> since epoch, which's what we've expected.

<a id="the-third-example">❸ In this third example</a>, I'd like to assert that if we've a date and time just <strong>one (1) second</strong> after <em>the epoch</em>, as in <a href="#the-second-example">the second example</a> then <strong>add another 1 (one) minute</strong>, then the <strong>seconds since epoch</strong> should be <strong>sixty one (61) seconds</strong>.

```
Content of src/main.rs:
```

```rust
use time::{macros::datetime, Duration};
use std::time::{SystemTime, UNIX_EPOCH};

fn main() {
    // "1970-01-01 00:00:01 UTC"
    let offset_dt = datetime!(1970-01-01 0:00:01 UTC) + Duration::minutes(1);
    let system_time = SystemTime::from(offset_dt);

    println!("offset_dt: {:#?} \n", offset_dt);
    println!("system_time: {:#?} \n", system_time);

    match system_time.duration_since(UNIX_EPOCH) {
        Ok(n) => println!("1970-01-01 00:00:00 UTC was {} seconds ago!", n.as_secs()),
        Err(_) => panic!("SystemTime before UNIX EPOCH!"),
    }
}
```

Output on Windows 10:

```
offset_dt: 1970-01-01 0:01:01.0 +00:00:00

system_time: SystemTime {
    intervals: 116444736610000000,
}

1970-01-01 00:00:00 UTC was 61 seconds ago!
```

Output on Ubuntu 22.10:

```
behai@hp-pavilion-15:~/rust/datetime$ ./target/debug/datetime
offset_dt: 1970-01-01 0:01:01.0 +00:00:00

system_time: SystemTime {
    tv_sec: 61,
    tv_nsec: 0,
}

1970-01-01 00:00:00 UTC was 61 seconds ago!
```

<a id="the-fourth-example">❹ In this fourth and last example</a>, I'd like to see that if I <strong>add one (1) hour</strong> to the <em>current UTC date time</em>, then the <strong>seconds since epoch</strong> of the later is <strong><code>1*60*60 = 3,600</code> (three thousand six hundred) seconds</strong> more than the former's.

```
Content of src/main.rs:
```

```rust
use time::{OffsetDateTime, Duration};
use std::time::{SystemTime, UNIX_EPOCH};

fn main() {
    let offset_dt = OffsetDateTime::now_utc();
    let offset_dt_1_hour = offset_dt + Duration::hours(1);

    let dt_secs: u64;
    let dt_1_hour_secs: u64;

    match SystemTime::from(offset_dt).duration_since(UNIX_EPOCH) {
        Ok(n) => dt_secs = n.as_secs(),
        Err(_) => panic!("1. SystemTime before UNIX EPOCH!"),
    }

    match SystemTime::from(offset_dt_1_hour).duration_since(UNIX_EPOCH) {
        Ok(n) => dt_1_hour_secs = n.as_secs(),
        Err(_) => panic!("2. SystemTime before UNIX EPOCH!"),
    }

    println!("Seconds: {}", dt_1_hour_secs - dt_secs);    
}
```

And the output is as expected:

```
Seconds: 3600
```

My three (3) examples are almost puerile 😂, actually I think they are... However, they help me to understand this issue much more concretely. Puerile as they are, I still like them. I hope you find them helpful too.

For more on epoch, the following Wikipedia article is worth skimming over: <a href="https://en.wikipedia.org/wiki/Epoch_(computing)" title="Epoch (computing)" target="_blank">Epoch (computing)</a>.

Thank you for reading and please stay safe as always.

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