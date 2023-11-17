---
layout: post
title: "Rust: JSON Web Token -- some investigative studies on crate jwt-simple."

description: Via experimentations, I seek to answer the following question regarding crate jwt-simple how do we check if a token is still valid, i.e. not already expired? I've found the answer to this question, and I hope it's a correct answer.

tags:
- Rust
- json
- web
- token
---

<em>Via experimentations, I seek to answer the following question regarding crate <a href="https://docs.rs/jwt-simple/latest/jwt_simple/" title="jwt-simple" target="_blank">jwt-simple</a>: <em>how do we check if a token is still valid, i.e. not already expired?</em> I've found the answer to this question, and I hope it's a correct answer.</em>

| ![089-feature-image.png](https://behainguyen.files.wordpress.com/2023/11/089-feature-image.png) |
|:--:|
| *Rust: JSON Web Token -- some investigative studies on crate jwt-simple.* |

<a id="jwt-background"></a>For the purpose of this post, we primarily use <code>JSON Web Token (JWT)</code> at the server side to verify the validity of an encoded string token before allowing access to certain resources. This encoded string token has originally been created by the server.

This Internet Engineering Task Force (IETF) RFC7519 article <a href="https://datatracker.ietf.org/doc/html/rfc7519" title="JSON Web Token (JWT)" target="_blank">JSON Web Token (JWT)</a> is the formal specification of JWT. This Wikipedia article <a href="https://en.wikipedia.org/wiki/JSON_Web_Token" title="JSON Web Token" target="_blank">JSON Web Token</a> would make a somewhat easier reading on the subject.

Basically, a JWT token consists of three (3) parts: <code>Header</code>, <code>Payload</code> and <code>Signature</code>. The <code>Signature</code> is calculated from the <code>Header</code> and the <code>Payload</code>, and in a lot of implementations together with a <code>secret string</code>, defined by the applications which use the library.

All components are encoded using Base 64 Url Encoding strings. The period or full stop, i.e. <code>.</code>, separates each part. 

An example of token from <a href="https://datatracker.ietf.org/doc/html/rfc7519#section-3.1" title="RFC7519 section 3.1" target="_blank">RFC7519 section 3.1</a>, where line breaks are for display purposes only:

```
eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9
.
eyJpc3MiOiJqb2UiLA0KICJleHAiOjEzMDA4MTkzODAsDQogImh0dHA6Ly9leGFt
cGxlLmNvbS9pc19yb290Ijp0cnVlfQ
.
dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
```

🚀 If we paste our own JWT tokens into <a href="https://jwt.io/" title="jwt.io | Auth0 by Okta" target="_blank">https://jwt.io/</a>, it should be decoded correctly, and we should see the information in <code>Payload</code> displayed as a JSON object. However, all tokens generated throughout this post always get reported <span style="color:red;"><strong><code>Invalid Signature</code></strong></span>.

This <a href="https://stackoverflow.com/questions/50774780/always-getting-invalid-signature-in-jwt-io" title="Always getting invalid signature in jwt.io" target="_blank">Stack Overflow</a> post discusses this issue -- this error does not seem at all relevant to our discussion.

The <code>Payload</code> has a set of standard claims. The specification defines these <a href="https://datatracker.ietf.org/doc/html/rfc7519#section-4.1" title="Registered Claim Names" target="_blank">Registered Claim Names</a>. Some are required, that is, if the <code>Payload</code> does not have any of these, the final token is not valid. We can define our own custom claims in the <code>Payload</code>, too; e.g., an <code>email</code> field.

There's a plethora of crates which implement JWT. I've studied two (2). Crate <a href="https://docs.rs/jwt-simple/latest/jwt_simple/" title="jwt-simple" target="_blank">jwt-simple</a> has more than 1 (one) million downloads and seems to be being actively maintained. <em>However, I've yet to find any post which comprehensively discusses how to use it.</em> And after spending times studying it, I feel that its documentations could improve significantly.

One of the central tenets of JWT is checking for token expiration. Reading through the official examples, it isn't clear how we go about doing that. After some experimentations, I seem to get it, at least, I think it'll work for me. Let's go through the experimentations which I've carried out. 

<code>Cargo.toml</code> is common for all examples. Its <code>dependencies</code> section is as follow:

```toml
...
[dependencies]
jwt-simple = "0.11"
serde = {version = "1.0.188", features = ["derive"]}
```

<strong>Please note:</strong> <em>the example code has been tested on both Windows 10 and Ubuntu 22.10.</em>

Also note that this crate does not use a <code>secret string</code> to calculate token's <code>Signature</code>.

<a id="the-first-example">❶ In this first example</a>, which is taken from the official documentation, the simplest example, we just create a token with no custom <code>Payload</code>, then decode the token, we also print out relevant data for visual inspection.

```
Content of src/main.rs:
```

```rust
use jwt_simple::prelude::*;

fn main() {
    // create a new key for the `HS256` JWT algorithm
    let key = HS256Key::generate();

    // create claims valid for 2 hours
    let claims = Claims::create(Duration::from_hours(2));

    println!("1. claims: {:#?}", claims);

    let token = match key.authenticate(claims) {
        Ok(x) => x,
        Err(e) => {
            println!("Failed to create token. Error: {}", e.to_string());
            panic!("Program terminated!");
        }
    };

    println!("1. token: {:#?}", token);

    let claims1 = match key.verify_token::<NoCustomClaims>(&token, None) {
        Ok(x) => x,
        Err(e) => {
            println!("Failed to verify token. Error: {}", e.to_string());
            panic!("Program terminated!");
        }        
    };

    println!("2. claims: {:#?}", claims1);
}
```

Output:

```
1. claims: JWTClaims {
    issued_at: Some(
        Duration(
            7301655513801696707,
        ),
    ),
    expires_at: Some(
        Duration(
            7301686437566227907,
        ),
    ),
    invalid_before: Some(
        Duration(
            7301655513801696707,
        ),
    ),
    issuer: None,
    subject: None,
    audiences: None,
    jwt_id: None,
    nonce: None,
    custom: NoCustomClaims,
}
1. token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MDAwNDkxNTMsImV4cCI6MTcwMDA1NjM1MywibmJmIjoxNzAwMDQ5MTUzfQ.ZF4SIJJ-PhSyL6cm_ocHuStZ5tv4hdYK-kg9RZ8kT-Y"
2. claims: JWTClaims {
    issued_at: Some(
        Duration(
            7301655513727500288,
        ),
    ),
    expires_at: Some(
        Duration(
            7301686437492031488,
        ),
    ),
    invalid_before: Some(
        Duration(
            7301655513727500288,
        ),
    ),
    issuer: None,
    subject: None,
    audiences: None,
    jwt_id: None,
    nonce: None,
    custom: NoCustomClaims,
}
```

Looking at the output, <strong>the following issues jump out</strong>: 

⓵ <a href="https://docs.rs/jwt-simple/latest/jwt_simple/claims/struct.JWTClaims.html" title="Struct jwt_simple::claims::JWTClaims" target="_blank">Struct jwt_simple::claims::JWTClaims</a> does not use any of the <a href="https://datatracker.ietf.org/doc/html/rfc7519#section-4.1" title="Registered Claim Names" target="_blank">Registered Claim Names</a>.

⓶ For the original claim (<code>1. claims:</code>), the value of <code>issued_at</code> is <code>7301655513801696707</code>, and for the decoded or verified claim, (<code>2. claims:</code>), the value of <code>issued_at</code> is <code>7301655513727500288</code>: they are different. Values for <code>expires_at</code> across both claims are also different. <strong>I started out with the assumption that values for each should be the same in both claims!</strong> I don't know what this means.

<a id="what-are-issued-at-expires-at"></a>⓷ Values of <code>issued_at</code>, <code>expires_at</code> are large. The documentation does not tell us what they represent! <a href="https://docs.rs/jwt-simple/latest/jwt_simple/claims/struct.JWTClaims.html" title="Struct jwt_simple::claims::JWTClaims" target="_blank">Struct jwt_simple::claims::JWTClaims</a> shows that they're <a href="https://docs.rs/jwt-simple/latest/jwt_simple/prelude/type.UnixTimeStamp.html" title="Type Alias jwt_simple::prelude::UnixTimeStamp" target="_blank">type alias jwt_simple::prelude::UnixTimeStamp</a>, and the real data type is <a href="https://docs.rs/jwt-simple/latest/jwt_simple/prelude/struct.Duration.html" title="Struct jwt_simple::prelude::Duration" target="_blank">struct jwt_simple::prelude::Duration</a>; whom documentation states:

> A duration type to represent an approximate span of time

We've made this call <code>Duration::from_hours(2)</code> in the code. And the documentation for <a href="https://docs.rs/jwt-simple/latest/jwt_simple/prelude/struct.Duration.html#method.from_hours" title="pub fn from_hours(hours: u64) -> Duration" target="_blank">pub fn from_hours(hours: u64) -> Duration</a> states:

> Creates a new Duration from the specified number of hours

<strong><em>It is not clear what they actually are. </em>We're coming back to this question in <a href="#the-third-example">❸ example three</a> in a section following.</strong>

<a id="the-second-example">❷ In this second example</a>, we're looking at custom claim or custom <code>Payload</code>. The code is taken from the following sections of the official documentation: <a href="https://docs.rs/jwt-simple/latest/jwt_simple/index.html#key-pairs-and-tokens-creation" title="Key pairs and tokens creation" target="_blank">Key pairs and tokens creation</a> and <a href="https://docs.rs/jwt-simple/latest/jwt_simple/index.html#custom-claims" title="Custom claims" target="_blank">Custom claims</a>. However, I define my own <code>Payload</code> rather than using <code>struct MyAdditionalData</code> from the document.

```
Content of src/main.rs:
```

```rust
use jwt_simple::prelude::*;

// A custom payload.
#[derive(Serialize, Deserialize, Debug)]
pub struct PayLoad {
    iat: u64,
    exp: u64,
    email: String,
}

fn main() {
    // create a new key pair for the `ES256` JWT algorithm
    let key_pair = ES256KeyPair::generate();

    // a public key can be extracted from a key pair:
    let public_key = key_pair.public_key();

    // iat, exp are willy-nilly set to some random values.
    let pay_load = PayLoad {
        iat: 1,
        exp: 5,
        email: String::from("behai_nguyen@hotmail.com"),
    };

    // Claim creation with custom data:
    let claims = Claims::with_custom_claims(pay_load, Duration::from_secs(30));

    println!("1. claims: {:#?}", claims);

    let token = key_pair.sign(claims).expect("Failed to sign claims.");

    println!("1. token: {:#?}", token);

    // Claim verification with custom data. Note the presence of the custom data type:

    let claims1 = match public_key.verify_token::<PayLoad>(&token, None) {
        Ok(x) => x,
        Err(e) => {
            println!("Failed to verify token. Error: {}", e.to_string());
            panic!("Program terminated!");
        }        
    };

    println!("2. claims: {:#?}", claims1);

    assert_eq!(claims1.custom.email, "behai_nguyen@hotmail.com");
}
```

In <code>pub struct PayLoad</code>, <strong>I purposely use</strong> the standard names for fields <code>iat</code> and <code>exp</code>.

Token creation happens successfully, but verifying or decoding the token results in the following handled error:

<span style="color:red;"><strong><code>Failed to verify token. Error: duplicate field `iat` at line 1 column 57</code></strong></span>

Commented out <code>iat</code> proving that <code>exp</code> also results in a pretty much similar error.

<a id="the-third-example">❸ It'd seem that we should use <code>expires_at</code> to check for token expiration</a>. We come back to <a href="#what-are-issued-at-expires-at">the question</a> above: what are the values of <code>issued_at</code> and <code>expires_at</code>?

In other words, when the server receives the token, what value do we have to work out to compare against <code>expires_at</code>, to determine if the token has expired or not?

The <a href="https://docs.rs/jwt-simple/latest/src/jwt_simple/claims.rs.html#303" title="Source code claims.rs.html#109-172" target="_blank">source code</a>, lines 303-331 show how values for <code>issued_at</code> and <code>expires_at</code> are calculated:

```rust
...
pub struct Claims;

impl Claims {
    /// Create a new set of claims, without custom data, expiring in
    /// `valid_for`.
    pub fn create(valid_for: Duration) -> JWTClaims<NoCustomClaims> {
        let now = Some(Clock::now_since_epoch());
        JWTClaims {
            issued_at: now,
            expires_at: Some(now.unwrap() + valid_for),			
...
    }

    /// Create a new set of claims, with custom data, expiring in `valid_for`.
    pub fn with_custom_claims<CustomClaims: Serialize + DeserializeOwned>(
        custom_claims: CustomClaims,
        valid_for: Duration,
    ) -> JWTClaims<CustomClaims> {
        let now = Some(Clock::now_since_epoch());
        JWTClaims {
            issued_at: now,
            expires_at: Some(now.unwrap() + valid_for),
...			
```

The value for <code>issued_at</code> is <code>Some(Clock::now_since_epoch())</code>.

The documentation for <a href="https://docs.rs/jwt-simple/latest/jwt_simple/prelude/struct.Clock.html#method.now_since_epoch" title="pub fn now_since_epoch() -> Duration" target="_blank">pub fn now_since_epoch() -> Duration</a> states:

> Returns the elapsed time since the UNIX epoch

-- It'd be nice if they also state what the unit of this elapsed time since the UNIX epoch is!

🦀 Please note, standard time <a href="https://doc.rust-lang.org/std/time/index.html" title="std::time" target="_blank">std::time</a> defines <a href="https://doc.rust-lang.org/std/time/constant.UNIX_EPOCH.html" title="Constant std::time::UNIX_EPOCH" target="_blank">Constant std::time::UNIX_EPOCH</a>, the “seconds since epoch” is calculated based on this constant, see <a href="https://behainguyen.wordpress.com/2023/11/13/rust-seconds-since-epoch-1970-01-01-000000-utc/#the-first-example" title="Standard time UNIX_EPOCH constant example" target="_blank">this example</a>.

This large <a href="https://docs.rs/jwt-simple/latest/jwt_simple/prelude/struct.Duration.html" title="Struct jwt_simple::prelude::Duration" target="_blank">Struct jwt_simple::prelude::Duration</a> number is actually the number of “ticks”, obtained by calling <a href="https://docs.rs/jwt-simple/latest/jwt_simple/prelude/struct.Duration.html#method.as_ticks" title="pub fn as_ticks(&self) -> u64" target="_blank">pub fn as_ticks(&self) -> u64</a>.

Let's try to mimic <code>issued_at</code> and <code>expires_at</code> calculations as per by the crate.

```
Content of src/main.rs:
```

```rust
use jwt_simple::prelude::*;

fn main() {
    let issued_at = Clock::now_since_epoch();
    let valid_for = Duration::from_hours(1);
    let expires_at = issued_at + valid_for;

    println!("issued_at: {:#?}", issued_at);
    println!("issued_at.as_ticks(): {}", issued_at.as_ticks());

    println!("expires_at: {:#?}", expires_at);
    println!("expires_at.as_ticks(): {}", expires_at.as_ticks());    
}
```

Output:

```
issued_at: Duration(
    7302219092803468401,
)
issued_at.as_ticks(): 7302219092803468401
expires_at: Duration(
    7302234554685734001,
)
expires_at.as_ticks(): 7302234554685734001
```

<a id="the-fourth-example">❹ In this final example</a>, we're attempting to do expiration check based on <code>expires_at</code>:

Create a token with a custom <code>Payload</code> (although not used in the code). This token is valid for only a few short seconds, defined by constant <code>SECONDS_VALID_FOR</code>. Then sleep for a few short seconds, defined by constant <code>SECONDS_TO_SLEEP</code>. Then decode the token. Next, obtain the current time using <a href="https://docs.rs/jwt-simple/latest/jwt_simple/prelude/struct.Clock.html#method.now_since_epoch" title="pub fn now_since_epoch() -> Duration" target="_blank">pub fn now_since_epoch() -> Duration</a>, as per <a href="#the-third-example">❸ example three</a> above. Finally, we compare <code>expires_at</code> and current time using ticks, seconds should also work, if <code>expires_at</code> is greater than the current time, the token is still valid, otherwise it is expired.

```
Content of src/main.rs:
```

```rust
use std;
use jwt_simple::prelude::*;

static SECONDS_VALID_FOR: u64 = 5;
static SECONDS_TO_SLEEP: u64 = 4;

// A custom payload.
#[derive(Serialize, Deserialize, Debug)]
pub struct PayLoad {
    email: String,
}

fn as_ticks(val: Option<Duration>) -> u64 {
    // This call will never fail!
    match val {
        Some(x) => x.as_ticks(),
        None => unreachable!(), // ! Coerced to u64.
    }
}

fn main() {
    // create a new key pair for the `ES256` JWT algorithm
    let key_pair = ES256KeyPair::generate();

    // a public key can be extracted from a key pair:
    let public_key = key_pair.public_key();

    let pay_load = PayLoad {
        email: String::from("behai_nguyen@hotmail.com"),
    };

    // Create a token and send it to the client.
    let claims1 = Claims::with_custom_claims(pay_load, Duration::from_secs(SECONDS_VALID_FOR));
    let token1 = key_pair.sign(claims1).expect("1. Failed to sign claims.");

    // Sleep for SECONDS_TO_SLEEP seconds.
    // (I.e. a few seconds later, the client submits the token to the server.)
    let sleep_time = std::time::Duration::from_secs(SECONDS_TO_SLEEP);
    std::thread::sleep(sleep_time);

    // Token has been submitted to the server: verify it.
    // Assume not failing!
    let verified_claims1 = public_key.verify_token::<PayLoad>(&token1, None)
        .expect("1. Failed to verify token.");

    // Getting current time.
    let now = Some(Clock::now_since_epoch());

    if as_ticks(verified_claims1.expires_at) > as_ticks(now) {
        println!("Token is still valid!");
    }
    else {
        println!("Token expired already!");
    }
}
```

Adjust the values of <code>SECONDS_VALID_FOR</code> and <code>SECONDS_TO_SLEEP</code>, recompile, and see the response. ⓵ When <code>SECONDS_VALID_FOR</code> is greater than <code>SECONDS_TO_SLEEP</code>, we should get “<code>Token is still valid!</code>”. ⓶ When <code>SECONDS_VALID_FOR</code> is equal to or less than <code>SECONDS_TO_SLEEP</code>, we should get “<code>Token expired already!</code>”

I hope my interpretation of how this <a href="https://docs.rs/jwt-simple/latest/jwt_simple/" title="jwt-simple" target="_blank">jwt-simple</a> crate works is correct. Before finishing up this post, I'd like to point out the followings:

<ul>
<li style="margin-top:10px;">
Unanswered question: why do <code>issued_at</code> and <code>expires_at</code> values are different when a token is decoded (verified). I really don't get this behaviour.
</li>
<li style="margin-top:10px;">
The documentation mentions that we could write the generated key to file as bytes, then later read it back and use it. I've tried this, and it works. I'm not yet certain how to apply this to a proper web application.
</li>
<li style="margin-top:10px;">
And finally, in the next post, I'm doing a similar sort of studies on another JWT crate.
</li>
</ul>

I do hope I haven't made any mistake in this post, and you find the information in this post helpful. Thank you for reading and stay safe as always.

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
