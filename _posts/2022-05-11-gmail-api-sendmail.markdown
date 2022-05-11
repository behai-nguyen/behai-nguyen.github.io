---
layout: post
title: "GMail API: send emails with NodeJs."

---

NodeJs v10.15.3 test codes for sending out emails via GMail API.

| ![018-feature-image.png](https://behainguyen.files.wordpress.com/2022/05/018-feature-image.png) |
|:--:|
| *GMail API: send emails with NodeJs.* |

This post is a continuation of this 
<a href="https://behai-nguyen.github.io/2022/05/09/gmail-api.html" 
title="GMail API: quick start with Python and NodeJs" target="_blank">GMail API: quick start with 
Python and NodeJs</a> post of mine -- I've now done the codes for sending out emails in 
<span class="keyword">NodeJs v10.15.3</span>.

We'll need <span class="keyword">nodemailer</span>
library. Please run the below command to install it, in the same directory where 
we've run:
<span class="keyword">npm install googleapis@39 --save</span>
before.

```
    npm install nodemailer
```

I'm using the starting codes provided by 
Google's API <a href="https://developers.google.com/gmail/api/quickstart/nodejs" title="Node.js quickstart" target="_blank">Node.js quickstart: https://developers.google.com/gmail/api/quickstart/nodejs</a>.
I'm replacing:	

{% highlight javascript %}
function listLabels(auth)
{% endhighlight %}

with

{% highlight javascript %}
async function sendEmail( auth )
{% endhighlight %}

The codes in this <span class="keyword">sendEmail( ... )</span>
function is a condensed and cut down version of the codes in this post 	
<a href="https://www.labnol.org/google-api-service-account-220405" 
title="How to Send Email with the Gmail API and Node.js" target="_blank">
How to Send Email with the Gmail API and Node.js</a>.

```
File: gmail-api-sendmail.js
```

{% highlight javascript %}
const fs = require( 'fs' );
const readline = require( 'readline' );
const { google } = require( 'googleapis' );
const MailComposer = require( 'nodemailer/lib/mail-composer' );

// If modifying these scopes, delete token.json.
const SCOPES = [ 'https://www.googleapis.com/auth/gmail.send' ];
// The file token.json stores the user's access and refresh tokens, and is
// created automatically when the authorization flow completes for the first
// time.
const TOKEN_PATH = 'token.json';

// Load client secrets from a local file.
fs.readFile('client_secret_oauth_gmail.json', (err, content) => {
  if ( err ) return console.log( 'Error loading client secret file:', err );
  // Authorize a client with credentials, then call the Gmail API.
  authorize( JSON.parse(content), sendEmail );
});

/**
 * Create an OAuth2 client with the given credentials, and then execute the
 * given callback function.
 * @param {Object} credentials The authorization client credentials.
 * @param {function} callback The callback to call with the authorized client.
 */
function authorize( credentials, callback ) {
  const { client_secret, client_id, redirect_uris } = credentials.installed;
  const oAuth2Client = new google.auth.OAuth2(
      client_id, client_secret, redirect_uris[0] );

  // Check if we have previously stored a token.
  fs.readFile( TOKEN_PATH, (err, token) => {
    if ( err ) return getNewToken( oAuth2Client, callback );
    oAuth2Client.setCredentials( JSON.parse(token) );
    callback( oAuth2Client );
  });
}

/**
 * Get and store new token after prompting for user authorization, and then
 * execute the given callback with the authorized OAuth2 client.
 * @param {google.auth.OAuth2} oAuth2Client The OAuth2 client to get token for.
 * @param {getEventsCallback} callback The callback for the authorized client.
 */
function getNewToken( oAuth2Client, callback ) {
  const authUrl = oAuth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES,
  });
  console.log('Authorize this app by visiting this url:', authUrl);
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  rl.question( 'Enter the code from that page here: ', (code) => {
    rl.close();
    oAuth2Client.getToken( code, (err, token) => {
      if ( err ) return console.error( 'Error retrieving access token', err );
      oAuth2Client.setCredentials( token );
      // Store the token to disk for later program executions
      fs.writeFile( TOKEN_PATH, JSON.stringify(token), (err) => {
        if ( err ) return console.error(err);
        console.log( 'Token stored to', TOKEN_PATH );
      });
      callback( oAuth2Client );
    });
  });
}

/**
 * Send a test email.
 *
 * @param {google.auth.OAuth2} auth An authorized OAuth2 client.
 */
async function sendEmail( auth ) {
	const options = {
		from: 'Email_Used_In_Google_Cloud_Platform_Project@gmail.com',
		to: 'behai_nguyen@hotmail.com',
		cc: 'behai_nguyen@protonmail.com',
		replyTo: 'Email_Used_In_Google_Cloud_Platform_Project@gmail.com',
		subject: 'Message via GMail API written in NodeJs',
		text: 'Hello, this email is sent from GMail using GMail API OAuth written in NodeJs.',
		html: '<h1>Hello, this email is sent from GMail using GMail API OAuth written in NodeJs.</h1>',
		textEncoding: 'base64'
	};
	
	const gmail = google.gmail({ version: 'v1', auth: auth });  
	
    const mailComposer = new MailComposer( options );
    const message = await mailComposer.compile().build();	
	const rawMessage = Buffer.from(message).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
	
    const { data: { id } = {} } = await gmail.users.messages.send({
        userId: 'me',
        resource: {
            raw: rawMessage,
        },
    });
	
	console.log( id );
};
{% endhighlight %}

This is my command to run it:

```
    "C:\Program Files\nodejs\node.exe" gmail-api-sendmail.js
```

| ![018-gmail-api-nodejs-01.png](https://behainguyen.files.wordpress.com/2022/05/018-gmail-api-nodejs-01.png) |
|:--:|
| *The sent email as seen in my Hotmail account.* |

| ![018-gmail-api-nodejs-02.png](https://behainguyen.files.wordpress.com/2022/05/018-gmail-api-nodejs-02.png) |
|:--:|
| *The sent email as seen in my Proton Mail account.* |

<span class="medium-font-size">
    This Google link 
    <a href="https://developers.google.com/identity/protocols/oauth2/scopes" 
    title="OAuth 2.0 Scopes for Google APIs" target="_blank">OAuth 2.0 Scopes for Google APIs</a>
	lists all OAuth 2.0 Scopes.
</span>

The scope used in the codes above is:

{% highlight javascript %}
const SCOPES = [ 'https://www.googleapis.com/auth/gmail.send' ];
{% endhighlight %}

That's all for this post. Thank you for visiting and I do 
hope you find it useful.