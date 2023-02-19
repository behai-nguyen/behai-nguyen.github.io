---
layout: post
title: "GitHub Webhook: our own “server” in NodeJs to receive Webhook events over the internet."
description: We are writing an HTTP “server” in NodeJs to receive GitHub Webhook events. We use the ngrok program to make our server publicly accessible over the internet. Finally, we set up a GitHub repo and define some Webhook on this repo, then see how our now public NodeJs server handles GitHub Webhook's notifications.

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.files.wordpress.com/2023/02/08-060-a.png"
    - "https://behainguyen.files.wordpress.com/2023/02/08-060-b.png"

gallery-image-list-2:
    - "https://behainguyen.files.wordpress.com/2023/02/09-060-a.png"
    - "https://behainguyen.files.wordpress.com/2023/02/09-060-b.png"

gallery-image-list-3:
    - "https://behainguyen.files.wordpress.com/2023/02/13-060-a.png"
    - "https://behainguyen.files.wordpress.com/2023/02/13-060-b.png"

gallery-image-list-4:
    - "https://behainguyen.files.wordpress.com/2023/02/14-060.png"
    - "https://behainguyen.files.wordpress.com/2023/02/15-060.png"

tags:
- GitHub
- Git
- Webhook
- NodeJs
- ngrok
---

*We are writing an HTTP “server” in NodeJs to receive GitHub Webhook events. We use the ngrok program to make our server publicly accessible over the internet. Finally, we set up a GitHub repo and define some Webhook on this repo, then see how our now public NodeJs server handles GitHub Webhook's notifications.*

| ![060-feature-image.png](https://behainguyen.files.wordpress.com/2023/02/060-feature-image.png) |
|:--:|
| *GitHub Webhook: our own “server” in NodeJs to receive Webhook events over the internet.* |

<a href="https://github.com/" title="GitHub" target="_blank">GitHub</a>
enables subscribing to receive activities occur on repositories.
This is known as Webhooks. This is the official documentation page 
<a href="https://docs.github.com/en/developers/webhooks-and-events/webhooks/about-webhooks"
title="About webhooks" target="_blank">About webhooks</a>.

To subscribe, we must have a public HTTP endpoint which understands how
to process notifications from GitHub Webhook's events. We are going to
write our own “server” application, in 
<a href="https://nodejs.org/en/" title="NodeJs" target="_blank">NodeJs</a>, 
which implements this endpoint: all it does is logging the received 
notifications to the console. 

To make our “server” public, <a href="https://github.com/" title="GitHub" target="_blank">GitHub</a>
recommends using 
<a href="https://ngrok.com/" title="ngrok" target="_blank">ngrok</a> -- 
this application enables localhost applications accessible over the internet.

<h2>Table of contents</h2>

<ul>
	<li style="margin-top:10px;"><a href="#environments">Environments</a></li>

	<li style="margin-top:10px;"><a href="#nodejs-server">Our “server” in NodeJs</a></li>

	<li style="margin-top:10px;"><a href="#install-ngrok-ubuntu">Install ngrok for Ubuntu 22.10 kinetic</a></li>

	<li style="margin-top:10px;"><a href="#github-webhook-test-our-server">Set up GitHub Webhook and test our server</a></li>
</ul>

<h3 style="color:teal;">
  <a id="environments">Environments</a>
</h3>

In this post, I'm using 
<a href="https://ubuntu.com/download/desktop/thank-you?version=22.10&architecture=amd64"
title="Ubuntu" target="_blank">Ubuntu</a>
version <code>22.10 kinetic</code>,
and <a href="https://nodejs.org/en/" title="NodeJs" target="_blank">NodeJs</a>
version <code>18.7.0</code>, and 
<a href="https://ngrok.com/" title="ngrok" target="_blank">ngrok</a>
version <code>3.1.1</code>. 

But, please note, both <a href="https://nodejs.org/en/" title="NodeJs" target="_blank">NodeJs</a>
and <a href="https://ngrok.com/" title="ngrok" target="_blank">ngrok</a>
are available under Windows 10. All material discussed in this post should 
also work in Windows 10, I have not tested it, but I have done something 
similar (using Python) under Windows 10.

<h3 style="color:teal;">
  <a id="nodejs-server">Our “server” in NodeJs</a>
</h3>

The primary objective is to demonstrate the flow -- how everything 
works together: I'm keeping it to a minimum demonstrable piece of 
functionality.

After we subscribe to an event in GitHub, and whenever that event 
has occurred, GitHub will <code><strong>POST</strong></code> a 
notification to the <code>Payload URL</code> that we specify when setting 
up the Webhook. In the context of this post, the <code>Payload URL</code>
is just simply a <code>POST</code> route that we implement on the server.

The <code>Payload URL</code> method is extremely simple: it just prints 
to the console whatever GitHub gives it, and sends back a text response 
so that GitHub knows the notification has been successfully received.

The default root route (<code>/</code>) is a <code>GET</code>, and will
just simply send back a <em>“Hello, World!”</em> message.

I have the code running under <code>/home/behai/webwork/nodejs</code>.

```
Content of /home/behai/webwork/nodejs/package.json:
```

```javascript
{
    "name": "Git Webhook",
    "version": "0.0.1",
    "dependencies": {
        "express": "latest",
        "body-parser": "latest"
    },
    "author": "Van Be Hai Nguyen",
    "description": "Learn Git Webhook Server"
}
```

We use the latest versions of 
<a href="https://expressjs.com/" title="Express web framework"target="_blank">Express web framework</a> 
and the middleware 
<a href="https://www.npmjs.com/package/body-parser" title="body-parser" target="_blank">body-parser</a>.

To install the packages, while within <code>/home/behai/webwork/nodejs</code>, run:

```
$ npm i
```

```
Content of /home/behai/webwork/nodejs/webhook.js:
```

```javascript
const express = require( 'express' );
const bodyParser = require("body-parser")

const app = express();

app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))

app.get( '/', function ( req, res ) {
        res.send("Hello, World!")
    }
);

app.post('/git-webhook', function(req, res) {
    let data = req.body;
    console.log(data);
    res.send('Received!');
})

const port = 8008;

app.listen( port, function() {
  console.log( `App listening on port ${port}!` )
});
```

<ul>
<li style="margin-top:10px;">
The server listens on port <code>8008</code>.
</li>

<li style="margin-top:10px;">
The <code>Payload URL</code>'s route is <code>/git-webhook</code>.
That means the full URL on localhost is <code>http://localhost:8008/git-webhook</code>.
</li>

<li style="margin-top:10px;">
The <code>Payload URL</code> method's response is simply <code>Received!</code>.
</li>

<li style="margin-top:10px;">
The default route <code>http://localhost:8008</code> responds with 
<code>Hello, World!</code>.
</li>
</ul>

Run it with:

```
$ node webhook.js
```

![01-060.png](https://behainguyen.files.wordpress.com/2023/02/01-060.png)

On the Ubuntu machine, <code>curl http://localhost:8008</code> on a 
command line, and <code>http://localhost:8008</code> via a browser 
should respond with <code>Hello, World!</code>.

<h3 style="color:teal;">
  <a id="install-ngrok-ubuntu">Install ngrok for Ubuntu 22.10 kinetic</a>
</h3>

The official page 
<a href="https://ngrok.com/docs/getting-started" title="Getting Started with ngrok" target="_blank">Getting Started with ngrok</a>,
describes the installation process for different operating systems. 
I skipped Step 1 of this instruction, since I already have a web server application of my own.

In 
<a href="https://ngrok.com/docs/getting-started#step-2-install-the-ngrok-agent"
title="Step 2: Install the ngrok Agent" target="_blank">Step 2: Install the ngrok Agent</a>,
I just ran the long and scary looking command listed under <strong>"For Linux, use Apt:"</strong>.

I then completed all the instructions described under 
<a href="https://ngrok.com/docs/getting-started#step-3-connect-your-agent-to-your-ngrok-account"
title="Step 3: Connect your agent to your ngrok account"
target="_blank">Step 3: Connect your agent to your ngrok account</a>.

Please read through 
<a href="https://ngrok.com/docs/getting-started#step-4-start-ngrok"
title="Step 4: Start ngrok" target="_blank">Step 4: Start ngrok</a>.
Since our server above listens on port <code>8008</code>, provided
that it is still running, we start <code>ngrok</code> with:

```
$ ngrok http 8008
```

The screen should look like the following:

![02-060.png](https://behainguyen.files.wordpress.com/2023/02/02-060.png)

<code>https://53a0-58-109-142-244.au.ngrok.io/</code> is the public
URL for our server above: anybody with this URL can access our server
running on our private network.

The GitHub <code>Payload URL</code> is then 
<code>https://53a0-58-109-142-244.au.ngrok.io/git-webhook</code>.

<strong>Please note that, since we're running the free version of <code>ngrok</code>,
every time we start <code>ngrok</code>, we'll have a different URL!</strong> Please
be mindful of that, but for our learning purpose, this is not a problem.

From my Windows 10 machine, I request <code>https://53a0-58-109-142-244.au.ngrok.io/</code>
using Postman, (but a browser would do, too), I get the expected response, as seen:

![03-060.png](https://behainguyen.files.wordpress.com/2023/02/03-060.png)

<code>ngrok</code> also logs the request:

![04-060.png](https://behainguyen.files.wordpress.com/2023/02/04-060.png)

It appears <code>ngrok</code> works okay with our “server”. We 
can now set up GitHub Webhook, and test our 
<code>https://53a0-58-109-142-244.au.ngrok.io/git-webhook</code>
endpoint.

<h3 style="color:teal;">
  <a id="github-webhook-test-our-server">Set up GitHub Webhook and test our server</a>
</h3>

Webhooks are local to each GitHub repo. We'll create a new repo 
<code>learn-git</code> for this purpose.

When <code>learn-git</code> has been created, click on <code>Settings</code>
on the top right hand corner, then on <code>Webhooks</code> on left hand side,
then <code>Add webhook</code> button on the top right hand.

For <strong>Payload URL</strong>, specify 
<code>https://53a0-58-109-142-244.au.ngrok.io/git-webhook</code>. 
For <strong>Content type</strong>, select <code>application/json</code>:

![05-060.png](https://behainguyen.files.wordpress.com/2023/02/05-060.png)

Leave everything else at default, click the green <code>Add webhook</code> button:

![06-060-1.png](https://behainguyen.files.wordpress.com/2023/02/06-060-1.png)

Note under <strong>Which events would you like to trigger this webhook?</strong>,
we leave it at the default <code>Just the <strong>push</strong> event.</code>
That means, this Webhook will notify our server only when we check something
into this repo.

GitHub tells us that it has sent our server (i.e. to the <strong>Payload URL</strong>),
a ping event:

![07-060.png](https://behainguyen.files.wordpress.com/2023/02/07-060.png)

According to the above screen, our server should have received
this ping event with no problem: indeed, it logs some JSON data, 
and <code>ngrok</code> also logs a new POST request to 
<code>/git-webhook</code> endpoint:

{% include image-gallery.html list=page.gallery-image-list-1 %}

At this point, the repo is still empty. Let's do some check in, 
i.e. <code>push</code>. The Webhook should trigger.

<code>D:\learn-git\</code> has some files. Let's initialise 
the repo and check them in. Note the check in message
<em>“Initial checking should have two files.”</em> (I meant 
<em>“check in”</em> 😂):

```
D:\learn-git>git init

D:\learn-git>git config user.name "behai-nguyen"
D:\learn-git>git config user.email "behai_nguyen@hotmail.com"

D:\learn-git>git add .
D:\learn-git>git commit -m "Initial checking should have two files."

D:\learn-git>git branch -M main
D:\learn-git>git remote add origin https://github.com/behai-nguyen/learn-git.git
D:\learn-git>git push -u origin main
```

The Webhook does trigger, our server logs the notification data, 
note that the logged message matches the check in message above;
and also <code>ngrok</code> records another new POST request to 
<code>/git-webhook</code> endpoint:

{% include image-gallery.html list=page.gallery-image-list-2 %}

Back to GitHub <code>learn-git</code> repo, go back to Webhook 
area, click on the <code>payload link</code> as pointed to by
the arrow in the following screen:

![10-060.png](https://behainguyen.files.wordpress.com/2023/02/10-060.png)

Click on <code>Recent Deliveries</code> tab, there are two
(2) events, <em>push</em> and <em>ping</em> as we've gone 
through above:

![11-060.png](https://behainguyen.files.wordpress.com/2023/02/11-060.png)

Pick on the <code>push</code> event, then click on 
<code>Response 200</code> tab, under <strong>Body</strong>,
we should see the text <code>Received!</code>, which is the 
response from our NodeJs server:

![12-060.png](https://behainguyen.files.wordpress.com/2023/02/12-060.png)

Note that, the <code>Request</code> tab has two sections, 
<strong>Headers</strong> and <strong>Payload</strong>. The
data that gets posted to our server is the <strong>Payload</strong>
data: GitHub Webhook documentation should help us understand
what this data means, so can we can use it correctly. 

Pick a file in https://github.com/behai-nguyen/learn-git.git, 
edit it directly and commit. This should trigger a <code>push</code> 
event. It does. Our server does get notified, note that the
messages match:

{% include image-gallery.html list=page.gallery-image-list-3 %}

Let's sync <code>js1.js</code>, edit it locally and check it in
properly. Command to sync:

```
D:\learn-git>git pull
```

Make some changes to <code>js1.js</code> locally; then check it in.
Note the two messages <em>“Test Webhook.”</em> and <em>“Check in from 
local machine via command.”</em>:

```
D:\learn-git>git add js1.js
D:\learn-git>git commit -m "Test Webhook." -m "Check in from local machine via command."
D:\learn-git>git push -u origin main
```

We get the expected response to our server. And <code>ngrok</code> 
records four (4) POST requests to <code>/git-webhook</code> endpoint:

{% include image-gallery.html list=page.gallery-image-list-4 %}

The <code>Recent Deliveries</code> tab (discussed before), 
should now have four (4) entries.

Through the screen captures presented throughout this post, it 
should be apparent that we can change properties of an existing 
Webhook, including the <code>Payload URL</code>. 

Due to the fact that our so-called server is so simple, it will
work happily with other Webhook events beside <code>push</code>.
I have tested with <code>Send me everything.</code>, and raised
issues to the <code>learn-git</code> repo, the server logs
notifications as it does for <code>push</code>. This little server
is good for examining the structure of the payloads we get for
different Webhook events.  The GitHub documentation should have this info,
but for me personally, visualising the data makes reading these
documents easier.

This concludes this post. I hope you find it helpful and useful.
Thank you for reading, and stay safe as always.
