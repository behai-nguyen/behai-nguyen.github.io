---
layout: post
title: "Using the YouTube Data API v3 with API Keys and OAuth 2.0"

description: The final result of this post is a functional Python Flask web server application that queries YouTube information using the YouTube Data API v3 (YouTube API) and OAuth 2.0 authorisation. We review the official documentation and discuss how to set up a Google Cloud Project that wraps the YouTube API. Next, we describe how to obtain credentials, including both the API key and OAuth 2.0 tokens, for the project. Finally, we present a functional Python Flask web server application. This example application also includes a function to manage the refresh_token, which is available only once during the first OAuth 2.0 authorization request. 

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/05/108-06.png"

gallery-image-list-9:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/05/108-09a.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/05/108-09b.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/05/108-09c.png"

tags:
- YouTube
- Data
- API 
- OAuth2
- API Key
- Python
- YouTube Data API v3
---

<em>The final result of this post is a functional Python <a href="https://flask.palletsprojects.com/en/3.0.x/" title="Flask" target="_blank">Flask</a> web server application that queries YouTube information using the <a href="https://developers.google.com/youtube/v3" title="YouTube Data API v3" target="_blank">YouTube Data API v3</a> (<code>YouTube API</code>) and OAuth 2.0 authorisation. We review the official documentation and discuss how to set up a Google Cloud Project that wraps the YouTube API. Next, we describe how to obtain credentials, including both the API key and OAuth 2.0 tokens, for the project. Finally, we present a functional Python <a href="https://flask.palletsprojects.com/en/3.0.x/" title="Flask" target="_blank">Flask</a> web server application. This example application also includes a function to manage the <code>refresh_token</code>, which is available only once during the first OAuth 2.0 authorization request.</em>

| ![108-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/05/108-feature-image.png) |
|:--:|
| *Using the YouTube Data API v3 with API Keys and OAuth 2.0* |

<p>
A few years ago, I experimented with the <code>YouTube API</code> using 
<a href="https://nodejs.org/en" title="NodeJs" target="_blank">NodeJs</a>. 
Unfortunately, I didn’t document that learning process, nor did I complete 
the project. Now, I’m revisiting this topic, but this time, I’m using Python 
and documenting my progress in this post.
</p>

<a id="own-youtube-channel"></a>
<p>
My goal is straightforward: for my own YouTube channel, I want to retrieve 
specific information about each video, including the <code>ID</code>, <code>title</code>, 
<code>description</code>, <code>search tags</code>, and <code>file name</code>.
</p>

<p>
Interestingly, while most of this information can be obtained using an 
<a href="https://developers.google.com/maps/documentation/javascript/get-api-key" 
title="Use API Keys" target="_blank">API key</a>, 
retrieving the video file name requires 
<a href="https://developers.google.com/identity/protocols/oauth2" 
title="Using OAuth 2.0 to Access Google APIs" target="_blank">OAuth 2.0 authorisation</a>. 
As a result, we’ll need both an API key and OAuth 2.0 credentials.
</p>

<p>
<strong>💥 Please note, my Gmail address for my developer account and YouTube channel 
is the same.</strong> 
</p>

<a id="post-objective"></a>
<p>
The primary objective of this post is to document the key points for getting 
started with the <code>YouTube API</code>, rather than creating a complete 
working application. In terms of coding, we will modify an 
<a href="https://github.com/youtube/api-samples/blob/07263305b59a7c3275bc7e925f9ce6cabf774022/python/quickstart_web.py" 
title="YouTube API Samples Python quickstart_web.py" 
target="_blank">existing official YouTube Data API v3 example</a>.
</p>

<!--------------------------------------------------------------------------------->

<h2>Table of contents</h2>

<ul style="list-style: none;">
<li style="margin-top:10px;">
<a href="#google-cloud-docs">❶ Review the Relevant Official YouTube Data API v3 Documentation</a>

<ul style="list-style: none; margin-left:30px;">
  <li style="margin-top:10px;">
  <a href="#auth-redirect-uris-doc">⓵ Note on OAuth 2.0 Authorized Redirect URIs</a>
  </li>
  
  <li style="margin-top:10px;">
  <a href="#auth-refresh-token-doc">⓶ Note on OAuth 2.0 Refresh Token</a>
  </li>

  <li style="margin-top:10px;">
  <a href="#auth-refresh-error-doc">⓷ Note on OAuth 2.0 <code>RefreshError</code> Exception</a>
  </li>  
</ul>
</li>

<li style="margin-top:10px;">
<a href="#create-google-cloud-project">❷ Create a New Google Cloud Project</a>
<ul style="list-style: none; margin-left:30px;">
  <li style="margin-top:10px;">
  <a href="#create-google-cloud-project-api-key">⓵ Create an <code>API key</code></a>
  </li>
  
  <li style="margin-top:10px;">
  <a href="#create-google-cloud-project-oauth-consent-screen">⓶ Configure the <code>OAuth consent screen</code></a>
  </li>

  <li style="margin-top:10px;">
  <a href="#create-google-cloud-project-client-id-secret">⓷ Create the OAuth 2.0 Client ID and Secret</a>
  </li>  
</ul>
</li>

<li style="margin-top:10px;">
<a href="#google-cloud-billing-account">❸ The Billing Account</a>
</li>

<li style="margin-top:10px;">
<a href="#google-api-playground">❹ The Google API Playground</a>

<ul style="list-style: none; margin-left:30px;">
  <li style="margin-top:10px;">
  <a href="#playground-retrieve-upload-playlist-id">⓵ Retrieving a Channel’s Upload Playlist ID Using a Channel ID</a>
  </li>
  
  <li style="margin-top:10px;">
  <a href="#playground-retrieve-upload-playlist-videos">⓶ Retrieving Videos from a Channel’s Playlist using the Playlist ID</a>
  </li>

  <li style="margin-top:10px;">
  <a href="#playground-retrieve-videos-file-names">⓷ Retrieving a Video’s File Name using a Video ID</a>
  </li>  
</ul>

</li>

<li style="margin-top:10px;">
<a href="#google-api-app">❺ The Complete Example Application</a>

<ul style="list-style: none; margin-left:30px;">
  <li style="margin-top:10px;">
  <a href="#app-changes-to-official-example">⓵ Modifications to the Official <code>quickstart_web.py</code> Example</a>
  </li>

  <li style="margin-top:10px;">
  <a href="#app-comple-example">⓶ Listing of the Complete Code and a Detailed Code Walkthrough</a>
  </li>

  <li style="margin-top:10px;">
  <a href="#app-comple-example-to-run">⓷ Running the Example Application and Checking the Output</a>
  </li>

  <li style="margin-top:10px;">
  <a href="#app-comple-example-copied-credentials-file">⓸ Executing the Example Application on a Different Machine Using the Granted Credentials</a>
  </li>

  <li style="margin-top:10px;">
  <a href="#app-comple-example-failed-auth">⓹ Attempt to Retrieve the File Name of a Video from a Different Channel</a>
  </li>  
</ul>

</li>

<li style="margin-top:10px;">
<a href="#google-api-helpful-links">❻ Some Helpful Links for Managing Google Cloud API Projects</a>
</li>

<li style="margin-top:10px;">
<a href="#gmail-google-api-posts">❼ Existing Posts on the Google Gmail API</a>
</li>

<li style="margin-top:10px;">
<a href="#concluding-remarks">❽ Concluding Remarks</a>
</li>
</ul>

<a id="google-cloud-docs"></a>
<p>
❶ Google APIs come with an extensive set of documentation and examples, 
which I find more than sufficient. However, I did get a bit lost in it. 
In this post, I’m listing the resources I’ve found most relevant for 
my needs. I encourage you to explore them as well. Keep in mind that 
this list is not exhaustive. While you can jump directly to the 
<a href="#create-google-cloud-project">create a new project</a> section, 
reading through these resources will make the later sections much easier 
to follow. <strong>Skipping the reading might not be the best approach</strong>.

</p>

<ul class="wp-block-list">
<li style="margin-top:10px;">
<a href="https://developers.google.com/youtube/registering_an_application" 
title="Obtaining authorization credentials" target="_blank">Obtaining authorization credentials</a>
</li>
<li style="margin-top:10px;">
<a href="https://developers.google.com/youtube/v3/getting-started"
title="YouTube Data API Overview" target="_blank">YouTube Data API Overview</a>
</li>

<li style="margin-top:10px;">
<a href="https://developers.google.com/identity/protocols/oauth2" 
title="Using OAuth 2.0 to Access Google APIs" target="_blank">Using OAuth 2.0 to Access Google APIs</a>
</li>

<li style="margin-top:10px;">
<a href="https://developers.google.com/identity/protocols/oauth2/web-server"
title="Using OAuth 2.0 for Web Server Applications" 
target="_blank">Using OAuth 2.0 for Web Server Applications</a>.
</li>
</ul>

<a id="auth-redirect-uris-doc"></a>
<p>
⓵ Note on OAuth 2.0 Authorized Redirect URIs:
</p>

<p>
In the section <strong>Create authorization credentials</strong>,
<a href="https://developers.google.com/identity/protocols/oauth2/web-server#creatingcred"
title="Create authorization credentials, point 4:"
target="_blank">specifically point 4</a>, 
please pay attention to the following statement:
</p>

> For testing, you can specify URIs that refer to the local machine, such as <code>http://localhost:8080</code>. With that in mind, please note that all of the examples in this document use <code>http://localhost:8080</code> as the redirect URI.
>
> We recommend that you <a href="https://developers.google.com/identity/protocols/oauth2/web-server#protectauthcode" title="design your app's auth endpoints" target="_blank">design your app's auth endpoints</a> so that your application does not expose authorization codes to other resources on the page.

<p>
Similarly, in the section 
<a href="https://developers.google.com/identity/protocols/oauth2/web-server#creatingclient" 
title="Step 1: Set authorization parameters" 
target="_blank">Step 1: Set authorization parameters</a>,
the explanation for the <strong>required</strong> parameter 
<code>redirect_uri</code> reads:
</p>

> Determines where the API server redirects the user after the user completes the authorization flow. The value must exactly match one of the authorized redirect URIs for the OAuth 2.0 client, which you configured in your client's API Console <a href="https://console.developers.google.com/apis/credentials" title="Credentials page" target="_blank">Credentials page</a>. If this value doesn't match an authorized redirect URI for the provided <code>client_id</code> you will get a <code>redirect_uri_mismatch</code> error.
> 
> Note that the <code>http</code> or <code>https</code> scheme, case, and trailing slash ('/') must all match.

<p>
Please note that, in a <a href="#auth-redirect-uris-cfg">later section</a>, 
we configure the value of <code>redirect_uri</code> to 
<code>http://localhost:5000/oauth2callback</code>.
</p>

<a id="auth-refresh-token-doc"></a>
<p>
⓶ Note on OAuth 2.0 Refresh Token:
</p>

<p>
While reading, I did take note of essential points about the refresh token. 
However, it didn’t fully register at the time. Initially, I got the code to 
work. But when I returned to run it again 2 or 3 days later, I encountered a 
<code>RefreshError</code> exception. I’ve included this section after 
troubleshooting the exception.
</p>

<p><strong>
💥 Despite the extensive amount of documentation, it is not explicitly stated 
that the <code>refresh_token</code> is provided only once, during the initial 
authorisation from users. This 
<a href="https://stackoverflow.com/a/10857806" 
title="The refresh_token is provided only once during the first authorisation from the user" 
target="_blank">Stack Overflow answer</a> clarifies this point.</strong>
</p>

<p>
● Note the example immediately preceding the section 
<a href="https://developers.google.com/identity/protocols/oauth2/web-server#offline" 
title="Refreshing an access token (offline access)" 
target="_blank">Refreshing an access token (offline access)</a>:
</p>

```python
authorization_url, state = flow.authorization_url(
    # Enable offline access so that you can refresh an access token without
    # re-prompting the user for permission. Recommended for web server apps.
    access_type='offline',
    # Enable incremental authorization. Recommended as a best practice.
    include_granted_scopes='true')
```

<p>
In my understanding, this section reiterates and emphasizes that it is 
more beneficial to set <code>access_type</code> to <code>offline</code>.
The reason is included in the comment in the above code block.
</p>

<p>
● This document, 
<a href="https://developers.google.com/youtube/v3/guides/authentication#OAuth2_Server_Side_Web_Applications_Flow" 
title="Implementing OAuth 2.0 Authorization" target="_blank">Implementing OAuth 2.0 
Authorization</a>, also reinforces the same point using different wording:
</p>

> For example, a server-side web application exchanges the returned token for an access token and a refresh token. The access token lets the application authorize requests on the user's behalf, and the refresh token lets the application retrieve a new access token when the original access token expires.

<p>
● And the last one I would like to quote is from the 
<a href="https://github.com/googleapis/google-api-python-client/blob/main/docs/start.md" 
title="Python official example documentation" target="_blank">Python official example 
documentation</a>: 
</p>

> <strong>Refresh and access tokens</strong>: When a user grants your application access, the OAuth 2.0 authorization server provides your application with refresh and access tokens. These tokens are only valid for the scope requested. Your application uses access tokens to authorize API calls. Access tokens expire, but refresh tokens do not. Your application can use a refresh token to acquire a new access token.
> 
> <strong>Warning</strong>: Keep refresh and access tokens private. If someone obtains your tokens, they could use them to access private user data.

<p>
<strong>🚀 To sum up, developers must save the refresh token in permanent storage 
and include it during subsequent authorisation requests. This ensures that a new 
access token can be generated if the current access token expires.</strong>
</p>

<a id="auth-refresh-error-doc"></a>
<p>
⓷ Note on OAuth 2.0 <code>RefreshError</code> Exception:
</p>

<p>
As <a href="#auth-refresh-token-doc">mentioned in the previous section</a>, 
I encountered the <code>RefreshError</code> exception because the access token 
had expired, and I had not included the <code>refresh_token</code> in the 
authorisation request. The text of the exception is:
</p>

<code class="danger-text">google.auth.exceptions.RefreshError: The credentials do not contain the necessary fields need<br/> to refresh the access token. You must specify refresh_token, token_uri, client_id, and client_secret.</code>

<p>
Fortunately, this problem has been thoroughly discussed in the following GitHub issue: 
<a href="https://github.com/googleapis/google-auth-library-python/issues/659" 
title="Google Auth Library Python issues 659" 
target="_blank">https://github.com/googleapis/google-auth-library-python/issues/659</a>.
</p>

<p>
<strong>🚀 Summary of the Solution:</strong>
</p>

<ol>
<li style="margin-top:10px;">
Visit <a href="https://myaccount.google.com/u/0/permissions"
title="Third-party apps & services" target="_blank">https://myaccount.google.com/u/0/permissions</a>.
</li>
<li style="margin-top:10px;">
Select <code>youtube data api scraper</code>.
</li>
<li style="margin-top:10px;">
Click on 
<code>Delete all connections you have with youtube data api scraper</code>. 
</li>
<li style="margin-top:10px;">
This action revokes the previously granted authorisation.
</li>
<li style="margin-top:10px;">
The next time we request authorisation, the Google Cloud API will guide us 
through the entire OAuth 2.0 user authorisation process again.
</li>
<li style="margin-top:10px;">
<strong>Ensure that we save the <code>refresh_token</code> to permanent storage 
this time.</strong>
</li>
</ol>

<a id="create-google-cloud-project"></a>
<p>
❷ Create a Google Cloud Project using the
<a href="https://console.cloud.google.com" 
title="Google Cloud Console" target="_blank">Google Cloud Console</a>.
This project will house the 
<a href="https://developers.google.com/youtube/v3/docs" 
title="YouTube Data API" target="_blank">YouTube Data API</a>. 
Please follow the steps below.
</p>

<ol>
<li style="margin-top:10px;">
Sign into your Google account. Typically, signing into Gmail is sufficient.
</li>

<li style="margin-top:10px;">
Navigate to the Google Cloud Console: 
<a href="https://console.cloud.google.com" 
title="Google Cloud Console" target="_blank">https://console.cloud.google.com</a>.
If this is your first time accessing the Cloud Console, 
you’ll encounter a welcome pop-up window. Agree to the 
<code>Terms of Service</code>, then click the 
<code>AGREE AND CONTINUE</code> button.
</li>

<li style="margin-top:10px;">
On the Google Cloud page:

<ul>
<li style="margin-top:10px;">
Click on the project drop-down list in the top right-hand corner (RHS).
</li>
<li style="margin-top:10px;">
In the pop-up window, click the <code>NEW PROJECT</code> button on the RHS.
</li>
</ul>
</li>
</ol>

<p>
Please refer to the screenshot illustration below:
</p>

![108-01.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/05/108-01.png)

<ol>
<li style="margin-top:10px;">
<strong>On the <code>New Project</code> page</strong>, enter an 
appropriate project name, such as <code>YouTube 02</code>.
</li>

<li style="margin-top:10px;">
Click on the <code>CREATE</code> button.
</li>

<li style="margin-top:10px;">
After the project is created, <strong>select it</strong>. You will 
be taken to a screen as shown below:
</li>
</ol>	

![108-02.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/05/108-02.png)

<ol>
<li style="margin-top:10px;">
<strong>Click on the <code>API Explore and enable APIs</code> link.</strong>
</li>

<li style="margin-top:10px;">
On the new screen, click on the 
<code>+ ENABLE APIS AND SERVICES</code> button (or link) in the top band, 
toward the left-hand side (LHS).
</li>

<li style="margin-top:10px;">
In the next screen, titled <code>Welcome to the API Library</code>, 
type <strong>“YouTube Data API”</strong> into the search box and hit 
the Enter key.
</li>

<li style="margin-top:10px;">
You will be taken to the result page, which looks similar to 
the screenshot below:
</li>
</ol>	

![108-03.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/05/108-03.png)

<ol>
<li style="margin-top:10px;">
<strong>Select the first entry: <code>YouTube Data API v3</code>.</strong>
</li>

<li style="margin-top:10px;">
On the next page, click on the <code>ENABLE</code> button.
</li>

<li style="margin-top:10px;">
This will take you to a new page that looks like the screenshot below:
</li>
</ol>

![108-04.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/05/108-04.png)

<p>
I am not familiar with the <code>CREATE CREDENTIALS</code> button 
in the above screen. The next step is to create credentials, both the 
<code>API key</code> and <code>OAuth 2.0</code>. Click on the 
<code>Credentials</code> link on the left-hand side (LHS). We will be 
taken to the following new screen:
</p>

![108-05.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/05/108-05.png)

<a id="create-google-cloud-project-api-key"></a>
<p>
⓵ Click on <code>API key</code> to create a new API key.
</p>

<a id="create-google-cloud-project-oauth-consent-screen"></a>
<p>
⓶ Click on <code>OAuth consent screen</code> to start creating a new OAuth 2.0 credential:
</p>

1. For <code>User Type</code>, we can only select <code>External</code>. Then click on <code>CREATE</code>.

2. On the next screen:

    - Enter something meaningful for <code>App name*</code>. I use <code>youtube data api scraper</code>. 

    - For <code>User support email *</code>, I use the email I currently sign in with, which is also the email associated with <a href="#own-youtube-channel">my YouTube channel</a>.

    - Under <strong>Developer contact information </strong>, in the <code>Email addresses *</code> section, I also use the same email as the one in <code>User support email *</code>.

    - Click the <code>SAVE AND CONTINUE</code> button.

<a id="create-google-cloud-project-scope"></a>
3. On the next screen, click on the <code>ADD OR REMOVE SCOPES</code> button. Then select the <code>../auth/youtube.readonly</code> scope, as illustrated in the screenshot below:

    ![108-06.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/05/108-06.png)

    Click the <code>UPDATE</code> button. The newly selected scope is now added under the <strong>Your sensitive scopes</strong> section of the screen. 

    Click the <code>SAVE AND CONTINUE</code> button.

4. On the new screen, under the <strong>Test users</strong> section, click on <code>+ ADD USERS</code>. Use the same email for <code>User support email *</code>.

    Click the <code>SAVE AND CONTINUE</code> button.

5. You will be taken to the <strong>OAuth consent screen</strong> summary page. We have completed the OAuth consent.

<a id="create-google-cloud-project-client-id-secret"></a>
<p>
⓷ Create the OAuth 2.0 Client ID and Secret:
</p>

<ol>
<li style="margin-top:10px;">
Click on the <code>Credentials</code> link on the LHS.
</li>

<li style="margin-top:10px;">
Then click <code>+ CREATE CREDENTIALS</code> and select 
<code>OAuth client ID</code>, as shown in the screenshot below:
</li>
</ol>

![108-07.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/05/108-07.png)

<a id="auth-redirect-uris-cfg"></a>
<p>
On the new screen: 
</p>

1. For <code>Application type *</code>, select <code>Web application</code>.

2. For <code>Name *</code>, enter something meaningful. I use <code>YouTube 02 Test Client</code>.

3. Under the section <strong>Authorized redirect URIs</strong>, click on the <code>+ ADD URI</code> button. Specify <code>http://localhost:5000/oauth2callback</code>. Please refer to the <a href="#auth-redirect-uris-doc">quoted documentation</a> for an explanation of why <code>http://localhost:5000</code> is a valid choice. Later, in the code, we will see how <a href="#app-comple-example-callback-uri"><code>http://localhost:5000/oauth2callback</code> is implemented</a>.

4. Click the <code>CREATE</code> button. After a few seconds, a <code>OAuth client created</code> notification screen will appear, as illustrated in the screenshot below:

    ![108-08.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/05/108-08.png)

    Click on <code>DOWNLOAD JSON</code> to save the OAuth 2.0 credential file to disk. Our applications will need this client secrets file.

<p>
We have completed creating an OAuth 2.0 credential. We can now use the 
downloaded credential file in our applications to obtain authorisation 
for using the <a href="https://developers.google.com/youtube/v3/docs" 
title="YouTube Data API" target="_blank">YouTube Data API</a>.
</p>

<p>
🚀 Note: If you already have a project selected, you can directly access its 
credentials page using the following URL: 
<a href="https://console.cloud.google.com/apis/credentials" 
title="Google Cloud Console project credentials page" 
target="_blank">https://console.cloud.google.com/apis/credentials</a>.
Here, you can make changes to existing credentials.
</p>

<a id="google-cloud-billing-account"></a>
<p>
❸ The Billing Account:
</p>

<p>
Please note that you might be asked to set up a billing account. A few years ago, I set one up, but unfortunately, I didn’t document the process. I don’t recall the exact steps off the top of my head. However, I haven’t been charged anything yet, as my usage has always remained below the free quota.
</p>

<a id="google-api-playground"></a>
<p>
❹ Google API Playground is a valuable tool that allows us to explore how any API works in terms of parameter requirements. This understanding will greatly assist us when coding later on. For our purposes, we will focus on three specific APIs. The way the playground operates should be consistent across other APIs as well.
</p>

<p>
<a href="#google-api-app">In our code example</a>, we will create three 
methods corresponding to these three APIs. These methods will use OAuth 2.0 
authorisation to retrieve data, although an API key can also be used for some 
methods.
</p>

<p>
To begin, visit the <a href="https://developers.google.com/youtube/v3" 
title="YouTube Data API v3" target="_blank">YouTube Data API documentation</a>. 
Click on the <strong>Search for content</strong> header, which will take you 
to the <strong>Search: list</strong> page 
<a href="https://developers.google.com/youtube/v3/docs/search/list"
title="Search for content"
target="_blank">https://developers.google.com/youtube/v3/docs/search/list</a>. 
On this page, pay attention to the three links: 
<a href="https://developers.google.com/youtube/v3/docs/videos" 
title="video" target="_blank">video</a>, 
<a href="https://developers.google.com/youtube/v3/docs/channels" 
title="channel" target="_blank">channel</a>, and 
<a href="https://developers.google.com/youtube/v3/docs/playlists"
title="playlist" target="_blank">playlist</a> 
— these are the APIs we are interested in. Also, take note of the 
<strong><span style="font-size:1.3em;">★</span>&nbsp;Quota impact</strong> warning.
</p>

<a id="playground-retrieve-upload-playlist-id"></a>
<p>
⓵ Retrieving a Channel’s Upload Playlist ID Using a Channel ID:
</p>

<p>
Click the <a href="https://developers.google.com/youtube/v3/docs/channels" 
title="channel" target="_blank">channel</a> link. On the new page, under the 
<a href="https://developers.google.com/youtube/v3/docs/channels#methods" 
title="Methods" target="_blank">Methods</a> header, click the 
<a href="https://developers.google.com/youtube/v3/docs/channels/list" 
title="list" target="_blank">list</a> link. This will take you to the 
YouTube Data API Channels: 
<a href="https://developers.google.com/youtube/v3/docs/channels/list" 
title="Channels: list" 
target="_blank">https://developers.google.com/youtube/v3/docs/channels/list</a>.
</p>

<p>
Please note the following general format:
</p>

<ul>
<li style="margin-top:10px;">
The middle pane contains the documentation for this API, including explanations for all input parameters and the HTTP request endpoint address.
</li>
<li style="margin-top:10px;">
The RHS pane is where we can try out the API.
</li>
</ul>

<p>
Let’s try with the following parameter values:
</p>

<ul>
<li style="margin-top:10px;">
<code>part</code>: <code>contentDetails</code>
</li>
<li style="margin-top:10px;">
<code>id</code>: <code>my own channel ID</code>
</li>

<li style="margin-top:10px;">
Leave both <code>Google OAuth 2.0</code> and 
<code>API key</code> checked.
</li>
</ul>

<p>
Click the <code>Execute</code> button, then follow the instructions. 
You should receive a response similar to the one below:
</p>

```json
{
	"kind": "youtube#channelListResponse",
	"etag": "76zI1v9YitYCtGvsZ6X_K11enRQ",
	"pageInfo": {
		"totalResults": 1,
		"resultsPerPage": 5
	},
	"items": [
		{
			"kind": "youtube#channel",
			"etag": "lXsff8mgRvFZ4QLKCa2LX-6JYDc",
			"id": "UCPB9BdRkJRd3aGm9qAY3CTw",
			"contentDetails": {
				"relatedPlaylists": {
					"likes": "LL",
					"uploads": "UUPB9BdRkJRd3aGm9qAY3CTw"
				}
			}
		}
	]
}
```

<p>
The equivalent HTTP request, using the API key set up when creating 
your <a href="#create-google-cloud-project">Google Cloud Project</a>, 
is as follows:
</p>

```javascript
https://www.googleapis.com/youtube/v3/channels?
    key=<API key>&
    part=contentDetails&
    id=<a YouTube channel ID>
```

<a id="playground-retrieve-upload-playlist-videos"></a>
<p>
⓶ Retrieving Videos from a Channel’s Playlist using the Playlist ID:
</p>

<p>
On the <strong>Search: list</strong> page, click the 
<a href="https://developers.google.com/youtube/v3/docs/playlists"
title="playlist" target="_blank">playlist</a> link. 
Then, on the new page, click the 
<a href="https://developers.google.com/youtube/v3/docs/playlistItems/list" 
title="PlaylistItems: list" target="_blank">playlistItems.list</a> link:
</p>

<p>
We can try this API with the following parameter values:
</p>

<ul>
<li style="margin-top:10px;">
<code>part</code>: <code>snippet</code>
</li>
<li style="margin-top:10px;">
<code>playlistId</code>: for example, the 
<code><a href="#playground-retrieve-upload-playlist-id">default upload playlist ID</a></code>
</li>
<li style="margin-top:10px;">
<code>maxResults</code>: <code>1</code> to <code>50</code>
</li>
<li style="margin-top:10px;">
Either <code>Google OAuth 2.0</code> or 
<code>API key</code> will suffice.
</li>
</ul>

<p>
Click the <code>Execute</code> button, then follow the instructions. 
We should get a valid response. It is rather long, so we will not list it here.
</p>

<p>
And this is the HTTP request equivalent, using the API key which we have set up 
when creating our <a href="#create-google-cloud-project">Google Cloud Project</a>:
</p>

```javascript
https://www.googleapis.com/youtube/v3/playlistItems?
   key=<API key>&
   part=snippet&
   playlistId=<a YouTube playlist ID>
   maxResults=2	
```

<a id="playground-retrieve-videos-file-names"></a>
<p>
⓷ Retrieving a Video’s File Name using a Video ID:
</p>

<p>
On the <strong>Search: list</strong> page, click the 
<a href="https://developers.google.com/youtube/v3/docs/videos" 
title="video" target="_blank">video</a> link. Then, on the new page, 
under the <a href="https://developers.google.com/youtube/v3/docs/videos#methods"
title="Methods" target="_blank">Methods</a> header, click the 
<a href="https://developers.google.com/youtube/v3/docs/videos/list"
title="Videos: list" target="_blank">list</a> link: 
</p>

<p>
We can try it with the following parameter values:
</p>

<ul>
<li style="margin-top:10px;">
<code>part</code>: <code>fileDetails</code>
</li>
<li style="margin-top:10px;">
<code>id</code>: <code>my own video ID</code>
</li>

<li style="margin-top:10px;">
Check only <code>Google OAuth 2.0</code>.
</li>
</ul>

<p>
We should get a response similar to the below:
</p>

```json
{
	"kind": "youtube#videoListResponse",
	"etag": "hKdZjPcW_VDYbyPRxoJ_WXoYj6A",
	"items": [
		{
			"kind": "youtube#video",
			"etag": "CMbJrlI-T_BK7YezgVi1Jpkb2-0",
			"id": "hMG1JjBwVx4",
			"fileDetails": {
				"fileName": "20240319-con chó giữa chúng ta-1.movie.mp4"
			}
		}
	],
	"pageInfo": {
		"totalResults": 1,
		"resultsPerPage": 1
	}
}
```

<p>
It seems that this API requires OAuth 2.0, which requires an authorisation code. For this reason, I have not tried out the HTTP request. According to the above page, the endpoint is:
</p>

```javascript
GET https://www.googleapis.com/youtube/v3/videos
```
<a id="google-api-app"></a>
<p>
❺ The Complete Example Application:
</p>

<p>
We will begin with the 
<a href="https://github.com/youtube/api-samples/blob/07263305b59a7c3275bc7e925f9ce6cabf774022/python/quickstart_web.py" 
title="YouTube API Samples Python quickstart_web.py" 
target="_blank"><code>quickstart_web.py</code></a>
example from the official YouTube API Samples in Python.
</p>

<a id="app-changes-to-official-example"></a>
<p>
⓵ We will make the following changes:
</p>

<ol>
<li style="margin-top:10px;">
The scope is set to <code>https://www.googleapis.com/auth/youtube.readonly</code> 
to match the <a href="#create-google-cloud-project-scope">project scope</a>.
</li>

<li style="margin-top:10px;">
The <code>refresh_token</code> is written into a local JSON file 
after the first successful 
<a href="#auth-refresh-token-doc">authorisation request</a>. In 
this implementation, we will simply write the entire granted credentials 
into the local JSON file.
</li>

<li style="margin-top:10px;">
Every time the application needs credentials, it first checks if the credentials JSON file exists. If it does, the application will attempt to load and use these credentials rather than submitting a new authorisation request.
</li>

<li style="margin-top:10px;">
<a href="#google-api-playground">As mentioned previously</a>, we implement 
three methods corresponding to the three APIs we have studied. Accordingly, 
the official example method <code>channels_list_by_username(client, **kwargs):</code>
is replaced by three new methods: 
<code>channels_get_upload_playlist_id(client, **kwargs):</code>, 
<code>playlist_get_videos(client, **kwargs):</code>, and 
<code>videos_get_file_names(client, **kwargs):</code>.
</li>
</ol>

<a id="app-comple-example"></a>
<p>
⓶ Listing the complete example code: Below is the content of <code>youtube_data_api.py</code>.
</p>

{% highlight python linenos %}
import os
import json

import flask

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret_youtube.json"

# Credentials obtained from Google Clould YouTube Data API v3.
CREDENTIALS_FILE = 'credentials_youtube.json'

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

app = flask.Flask(__name__)
# Note: A secret key is included in the sample so that it works, but if you
# use this code in your application please replace this with a truly secret
# key. See http://flask.pocoo.org/docs/0.12/quickstart/#sessions.
app.secret_key = 'REPLACE ME - this value is here as a placeholder.'

@app.route('/')
def index():
    # Attempt to load previous credentials stored on local JSON file...
    if 'credentials' not in flask.session:    
        load_credentials()

    # There is no credentials stored on local JSON file. Try to authorise.
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    # Load the credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    client = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)
  
    """
    return channels_get_upload_playlist_id(client,
        part='contentDetails',
        id='UCPB9BdRkJRd3aGm9qAY3CTw')
    """

    """
    return playlist_get_videos(client,
        part='snippet,contentDetails',
        maxResults=2,
        playlistId='UUPB9BdRkJRd3aGm9qAY3CTw')
    """

    """ 
    # Note: hMG1JjBwVx4 is my own video. That is, the email address 
    #     associated with the hMG1JjBwVx4's channel is also the email
    #     address I used to obtain the OAuth 2.0 credentials.
    # 
    # ACTION ITEM for readers: 
    #     You have to replace hMG1JjBwVx4 with your own.
    #
    return videos_get_file_names(client,
        part='fileDetails',
        id='hMG1JjBwVx4')
    """

    return f'<h2>Please enable either channels_get_upload_playlist_id(...), \
            playlist_get_videos(...), or videos_get_file_names(...) call \
            to see a YouTube Data API v3 in action.</h2>'

@app.route('/authorize')
def authorize():
    # Create a flow instance to manage the OAuth 2.0 Authorization Grant Flow
    # steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # This parameter enables offline access which gives your application
        # both an access and refresh token.
        access_type='offline',
        # This parameter enables incremental auth.
        include_granted_scopes='true')

    # Store the state in the session so that the callback can verify that
    # the authorization server response.
    flask.session['state'] = state

    return flask.redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verify the authorization server response.
    state = flask.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url

    flow.fetch_token(authorization_response=authorization_response)

    # Store the credentials in the session.
    # ACTION ITEM for developers:
    #     Store user's access and refresh tokens in your data store if
    #     incorporating this code into your real app.
    credentials = flow.credentials

    credentials_as_dict = credentials_to_dict(credentials)

    flask.session['credentials'] = credentials_as_dict

    # Store the credentials as JSON to a file on disk.
    with open(CREDENTIALS_FILE, 'w') as f: 
        json.dump(credentials_as_dict, f)

    return flask.redirect(flask.url_for('index'))

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

def load_credentials():
    in_error = False

    try:
        with open(CREDENTIALS_FILE) as f:
            credentials = json.load(f)
            f.close()

        keys = ['token', 'refresh_token', 'token_uri', 'client_id', 'client_secret', 'scopes']
        for key in keys:
            in_error = (key not in credentials)
            if in_error: break

    except Exception as e:
        in_error = True
    finally:
        if not in_error: 
            flask.session['credentials'] = {
                'token': credentials['token'],
                'refresh_token': credentials['refresh_token'],
                'token_uri': credentials['token_uri'],
                'client_id': credentials['client_id'],
                'client_secret': credentials['client_secret'],
                'scopes': credentials['scopes']
            }

        return in_error

def channels_get_upload_playlist_id(client, **kwargs):
    response = client.channels().list(
      **kwargs
    ).execute()

    return flask.jsonify(**response)

def playlist_get_videos(client, **kwargs):
    response = client.playlistItems().list(
      **kwargs
    ).execute()

    return flask.jsonify(**response)

def videos_get_file_names(client, **kwargs):
    response = client.videos().list(
        **kwargs
    ).execute()

    return flask.jsonify(**response)    

if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run('0.0.0.0', 5000, debug=True)
{% endhighlight %}

<p>
The example code should be self-explanatory, but let’s go over some of the key points:
</p>

<a id="app-comple-example-callback-uri"></a>
<p>
● For the <code>/oauth2callback</code> endpoint, there are two key points:
</p>

<p>
<span style="font-size:1.5em;font-weight:bold;">⑴</span> In the section 
<a href="#auth-redirect-uris-doc">Note on OAuth 2.0 Authorized redirect URIs</a> 
we mentioned configuring <code>http://localhost:5000/oauth2callback</code>
as the value for <code>redirect_uri</code>. This <code>/oauth2callback</code> 
is the endpoint, and the application has been coded to listen to <code>
port 5000</code> at line 191: <code>app.run('0.0.0.0', 5000, debug=True)</code>.
</p>

<p>
<span style="font-size:1.5em;font-weight:bold;">⑵</span> In the
endpoint handler method <code>oauth2callback():</code>, lines 124 to 126:
</p>

<figure class="highlight"><pre><code class="language-python" data-lang="python"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">124
125
126
</pre></td><td class="code"><pre>    <span class="c1"># Store the credentials as JSON to a file on disk.
</span>    <span class="k">with</span> <span class="nb">open</span><span class="p">(</span><span class="n">CREDENTIALS_FILE</span><span class="p">,</span> <span class="s">'w'</span><span class="p">)</span> <span class="k">as</span> <span class="n">f</span><span class="p">:</span> 
        <span class="n">json</span><span class="p">.</span><span class="n">dump</span><span class="p">(</span><span class="n">credentials_as_dict</span><span class="p">,</span> <span class="n">f</span><span class="p">)</span>
</pre></td></tr></tbody></table></code></pre></figure>

<p>
This is where we write the entire granted credentials to a 
local JSON file as 
<a href="#app-changes-to-official-example">discussed in point 2 above</a>.
</p>

<a id="app-comple-example-load-credentials"></a>
<p>
● For the method <code>load_credentials()</code>, we attempt to load credentials 
from an existing credentials JSON file. 
<a href="#app-changes-to-official-example">Please see point 3 above</a>.
</p>

<a id="app-comple-example-default-endpoint"></a>
<p>
● The default endpoint handler method <code>index()</code>: 
This is like the “main” function of this example “program”:
</p>

<p>
<span style="font-size:1.5em;font-weight:bold;">⑴</span> If 
the application has not been authorised yet, we attempt to load 
the previously acquired credentials from the local JSON file. If there 
are no previous credentials, or the local JSON content is in error, 
we attempt to request authorisation from the Google Cloud API.
</p>

<p>
<strong>We optimistically assume that one of the above steps will 
succeed. This is not production-ready code as stated in the 
<a href="#post-objective">introduction</a>.</strong>
</p>

<p>
<span style="font-size:1.5em;font-weight:bold;">⑵</span> The 
rest of the code in this method is as per the official example.
<strong>💥 Please note that the three API call methods 
<a href="#app-changes-to-official-example">discussed in point 4</a>
above have all been commented out. You will need to enable each one of them to see how they work.
</strong>
</p>

<a id="app-comple-example-to-run"></a>
<p>
⓷ To run the example application, we need to install the required packages onto the 
active virtual environment as per the 
<a href="https://developers.google.com/identity/protocols/oauth2/web-server#python"
title="Using OAuth 2.0 for Web Server Applications" target="_blank">official instructions</a>:
</p>

```
pip install --upgrade google-api-python-client
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2
pip install --upgrade flask
```

<p>
From the active virtual environment <code>venv</code>, launch the example as follows:
</p>

```
▶️<code>Windows 10:</code>venv\Scripts\python.exe youtube_data_api.py 
▶️<code>Ubuntu 22.10:</code>./venv/bin\python youtube_data_api.py
```

<p>
<strong>🚀 Then, on the same machine</strong>, access the example URL 
<a href="http://localhost:5000/" title="http://localhost:5000/" 
target="_blank">http://localhost:5000/</a>.
</p>

<p>
For the first time requesting authorisation, the Google Cloud API will initiate the OAuth 2.0 user process, requesting the user to grant permissions. Please see the screenshots of this process below. Your experience should look similar:
</p>

{% include image-gallery.html list=page.gallery-image-list-9 %}
<br/>

<p>
The default endpoint method handler <code>index():</code>
was calling <code>videos_get_file_names(...)</code>. 
After the user granted permissions and the OAuth 2.0 process was successful, we should have a response similar to the one illustrated below:
</p>

![108-10.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/05/108-10.png)

<p>
<strong>💥 Most importantly, the credentials JSON file <code>credentials_youtube.json</code> 
should have been written to the directory where <code>youtube_data_api.py</code> is located. 
Please check this for yourself.</strong>
</p>

<a id="app-comple-example-copied-credentials-file"></a>
<p>
⓸ Using the <code>credentials_youtube.json</code> file on another machine: 
For learning purposes, I copied both the 
<code>youtube_data_api.py</code> and <code>credentials_youtube.json</code> 
files to Ubuntu 22.10, set up the virtual environment, and ran the example without 
<a href="#auth-redirect-uris-doc">reconfiguring <code>redirect_uri</code></a>. 
The Google Cloud API happily accepted these credentials. Please see the screenshot below:
</p>

![108-11.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/05/108-11.png)

<a id="app-comple-example-failed-auth"></a>
<p>
⓹ The method <code>videos_get_file_names(client, **kwargs):</code>
can only work with videos which belong to 
<a href="#own-youtube-channel">our own YouTube channel</a>. For understanding purposes, I tried to access a public video from another public channel, and below is the response:
</p>

<span class="danger-text">
googleapiclient.errors.HttpError: &lt;HttpError 403 when requesting https://youtube.googleapis.com/youtube/v3/videos?part=fileDetails&id=97t-8NF7oz4&alt=json returned "The request is not properly authorized to access video file or processing information. Note that the <code>fileDetails</code>, <code>processingDetails</code>, and <code>suggestions</code> parts are only available to that video's owner.". Details: "[{'message': "The request is not properly authorized to access video file or processing information. Note that the <code>fileDetails</code>, <code>processingDetails</code>, and <code>suggestions</code> parts are only available to that video's owner.", 'domain': 'youtube.video', 'reason': 'forbidden', 'location': 'part', 'locationType': 'parameter'}]"&gt;
</span>

<a id="google-api-helpful-links"></a>
<p>
❻ Here are some helpful links for managing Google Cloud API projects.
</p>

<ul>
<li style="margin-top:10px;">
<a href="https://console.cloud.google.com" 
title="Google Cloud Console" target="_blank">https://console.cloud.google.com</a>: 
Google Cloud Console.
</li>

<li style="margin-top:10px;">
<a href="https://console.developers.google.com/apis/credentials" 
title="Credentials page" target="_blank">https://console.developers.google.com/apis/credentials</a>: 
API credentials console.
</li>

<li style="margin-top:10px;">
<a href="https://myaccount.google.com/u/0/permissions"
title="Third-party apps & services" 
target="_blank">https://myaccount.google.com/u/0/permissions</a>: 
Revoke OAuth 2.0 authorisations previously granted.
</li>
</ul>

<a id="gmail-google-api-posts"></a>
<p>
❼ Please note: We have previously discussed the 
<a href="https://developers.google.com/gmail/api/guides" 
title="Google Gmail API" target="_blank">Google Gmail API</a> 
in the following posts:
</p>

<ol>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/05/09/gmail-api-quick-start-with-python-and-nodejs/"
title="GMail API: quick start with Python and NodeJs" 
target="_blank">GMail API: quick start with Python and NodeJs</a>
</li>
<li style="margin-top:10px;">	
<a href="https://behainguyen.wordpress.com/2022/05/11/gmail-api-send-emails-with-nodejs/"
title="GMail API: send emails with NodeJs" 
target="_blank">GMail API: send emails with NodeJs</a>
</li>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/02/03/ci-cd-02-jenkins-basic-email-using-your-gmail-account/"
title="CI/CD #02. Jenkins: basic email using your Gmail account"
target="_blank">CI/CD #02. Jenkins: basic email using your Gmail account</a>
</li>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/06/15/sending-emails-via-gmail-account-using-the-python-module-smtplib/"
title="Sending emails via Gmail account using the Python module smtplib"
target="_blank">Sending emails via Gmail account using the Python module smtplib</a>
</li>
</ol>

<p>
In addition to the <a href="https://developers.google.com/gmail/api/guides" 
title="Google Gmail API" target="_blank">Google Gmail API</a>, I have also used the 
<a href="https://cloud.google.com/text-to-speech/docs/reference/rest" 
title="Cloud Text-to-Speech API" target="_blank">Cloud Text-to-Speech API</a> 
with Python. The Text-to-Speech API is comparatively easier to set up than both 
the Gmail API and the YouTube API.
</p>

<a id="concluding-remarks"></a>
❽ I did not intend for this post to be this long. There are just so 
many details to cover. Hopefully, this post will serve as a stepping 
stone for trying other Google Cloud APIs. I have learned a lot writing 
this post. And I apologise for not being able to make it shorter.

Thank you for reading. I hope you find the information in this post useful. Stay safe, as always.

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
<a href="https://commons.wikimedia.org/wiki/File:YouTube_logo_%282017%29.png" target="_blank">https://commons.wikimedia.org/wiki/File:YouTube_logo_%282017%29.png</a>
</li>
</ul>