---
layout: post
title: "CI/CD #02. Jenkins: basic email using your Gmail account."
description: We look at the most basically approach to send emails in Jenkins. The SMTP server we use is the Gmail SMTP server.
tags:
- CICD
- Jenkins
- Gmail
- SMTP
---

*We look at the most basically approach to send emails in Jenkins. The SMTP server we use is the Gmail SMTP server.*

| ![056-feature-image-1.png](https://behainguyen.files.wordpress.com/2023/02/056-feature-image-1.png) |
|:--:|
| *CI/CD #02. Jenkins: basic email using your Gmail account.* |

To recap, I have installed 
<a href="https://www.jenkins.io/" title="Jenkins" target="_blank">Jenkins</a> 
2.388 LTS on my Ubuntu 22.10, with all suggested plugins, the name of this machine 
is <code>HP-Pavilion-15</code>. 

I am accessing Jenkins on <code>HP-Pavilion-15</code> from my <strong>Windows 10 
machine</strong> using FireFox -- <em>please keep in mind this point</em>.

The steps required to get the Gmail SMTP server to work with Jenkins are straightforward:
❶ apply some simple configurations to the Gmail account, 
some of which we might have already done; ❷ configure Jenkins, which is quite easy. 
❸ Not part of the steps, but we will have to prove that the configuration is working,
we will write a simple Jenkins Pipeline whose main task is just to send out
an email. 

❶ Configure the Gmail account which we are using with Jenkins.

The Gmail account I'm using is <code>behai.van.nguyen@gmail.com</code>,
and it is the <em>Gmail SMTP user name</em>.

Start Gmail, click on the avatar icon on the top right hand corner, then 
click on <code>Manage your Google Account</code> button, then on the 
<span style="content: url('https://www.gstatic.com/images/branding/googlelogo/svg/googlelogo_clr_74x24px.svg');display: inline-block; height: 24px; width: 74px;vertical-align: middle;"></span>
<span style="color: #5f6368;opacity: 1;display: inline-block;font-family: 'Product Sans',Arial,sans-serif;font-size:1em;line-height: 24px;position: relative;top: -1.5px;vertical-align: middle;text-rendering: optimizeLegibility;">Account</span>
page, click on the <code>Security</code> button:

![056-01-2.png](https://behainguyen.files.wordpress.com/2023/02/056-01-2.png)

On this screen, we are interested in:

<ol>
<li style="margin-top:10px;">
<strong>2-Step Verification</strong> -- this must be turned on.
</li>
<li style="margin-top:10px;">
<strong>App passwords</strong> -- it sounds scary, but it is simple. 
We use this to generate the password for the Gmail SMTP server. 
Click anywhere on this row to go to the <strong>App passwords</strong> 
screen, it might ask for the password, use your current Gmail password.
</li>
</ol>

On the <strong>App passwords</strong> screen, for <strong>Select device</strong>,
I have to select <code>Windows Computer</code>, since I'm running Jenkins on 
Windows 10 using FireFox. For <strong>Select app</strong>, select 
<code>Other <em>(Custom name)</em></code>, then enter <code>Jenkins</code>.
The screen now should look like:

![056-02-1.png](https://behainguyen.files.wordpress.com/2023/02/056-02-1.png)

Click on the <code>GENERATE</code> button to generate the password. 
The 16 (sixteen) letter string in the orange box is the Gmail SMTP
server password.

![056-03-1.png](https://behainguyen.files.wordpress.com/2023/02/056-03-1.png)

We now have all required information for the Gmail SMTP server:

<ul>
<li style="margin-top:10px;">
Gmail SMTP server address: <code>smtp.gmail.com</code>
</li>
<li style="margin-top:10px;">
Gmail SMTP user name: <code>behai.van.nguyen@gmail.com</code>
</li>
<li style="margin-top:10px;">
Gmail SMTP password: <code>gwrnafeanafjlgsj</code>
</li>
<li style="margin-top:10px;">
Gmail SMTP port: <code>465</code> -- <em>please note</em>, 
some resulting posts for this Google search 
<a href="https://www.google.com/search?q=port+465+vs+25&sxsrf=AJOqlzUN4jZNHU8pi2tAiO4MZsThrY06WQ%3A1675386667199&ei=K1_cY7_pC7Hu4-EP0vugkAg&oq=port+465+vs&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAxgBMgUIABCABDIFCAAQgAQyBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yCAgAEBYQHhAKOgoIABBHENYEELADOgcIABCwAxBDOgQIIxAnOgsIABCABBCxAxCDAToICAAQsQMQgwE6CwguEIAEELEDEIMBOggIABCABBCxAzoFCAAQkQI6EQguEIAEELEDEIMBEMcBENEDOggILhCxAxCDAToOCC4QgAQQsQMQxwEQrwE6CAguEIAEENQCOgUILhCABDoICC4QgAQQsQM6BAgAEEM6CwguEIAEELEDENQCOgsILhCABBDHARCvAToLCC4QsQMQgwEQ1AI6CAgAEIAEEMsBOgUIABCGA0oECEEYAEoECEYYAFD0BViHK2C1OWgBcAF4AYABygSIAZMTkgELMC44LjEuMS4wLjGYAQCgAQHIAQrAAQE&sclient=gws-wiz-serp"
title="Google search: port 465 vs 25" target="_blank">port 465 vs 25</a>
state that <strong>port 465</strong> has been deprecated, we should use port 587 instead.
I did try port 587, it does not work yet!
</li>
</ul>

❷ Configure Jenkins.

<strong>Please note</strong>, during the configuration process, sometimes 
Jenkins raises the error, (possibly due to long idle period), 
<strong style="color:red;">HTTP ERROR 403 No valid crumb was included in the 
request</strong>, I just do a hard refresh, losing any unsaved information, 
but my next submission is usually valid.

Click on <code>Manage Jenkins</code>, then <code>Configure System</code>. On
the <strong>Configure System</strong> screen, scroll a bit down to 
<strong>Jenkins Location</strong>, enter a valid email for <strong>System 
Admin e-mail address</strong>:

![056-04-1.png](https://behainguyen.files.wordpress.com/2023/02/056-04-1.png)

Scroll down to the last section <strong>E-mail Notification</strong>, click on
the <code>Advanced</code> button to open the SMTP section, then fill out
the screen as per below, I think all fields are compulsory, I understand that
port 465 requires SSL:

![056-05.png](https://behainguyen.files.wordpress.com/2023/02/056-05.png)

Jenkins should now be able to send emails via user <code>behai.van.nguyen@gmail.com</code>.
Let's test it. Click on the checkbox <code>Test configuration by sending test e-mail</code>, 
enter a valid email address which you have access to for <strong>Test e-mail recipient</strong>,
then click on the <code>Test configuration</code> button. After a little while, we should get 
the <em>Email was successfully sent</em> as per the screen below:

![056-06.png](https://behainguyen.files.wordpress.com/2023/02/056-06.png)

I can confirm that I did receive the email to address <strong>Test e-mail recipient</strong>,
whose content is:

```
From: behai.van.nguyen@gmail.com 
Subject: Test email #2
Body: This is test email #2 sent from Jenkins
```

<code>#2</code> means the second test email, since this was the second test
email which I've sent.

Click on the <code>Save</code> button to save the 
<strong>Configure System</strong> information.

❸ A simple Jenkins Pipeline whose main task is to send out an email using the 
above configurations.

Click on <code>+ New Item</code>. On the next page, for 
<strong>Enter an item name</strong>, enter something meaningful, 
then select the second option <code>Pipeline</code>. Click on the <code>OK</code> 
button to move to the <strong>General</strong> page.

On the <strong>General</strong> page, scroll down to the bottom, then click on
the <code>Pipeline Syntax</code> link, the next page helps us write the Pipeline
code to send emails. 

On the next page, under 
<strong>Sample Step</strong>, select <code>mail: Mail</code>, then fill out
<strong>To</strong>, <strong>Subject</strong> and <strong>Body</strong> fields.
For <strong>To</strong> email address, ensure some valid address and 
you have access to it, I don't fill out other fields, but you could certainly
try:

![056-07.png](https://behainguyen.files.wordpress.com/2023/02/056-07.png)

Scroll a bit further down to see last section of the page.
Click on the <code>Advanced</code> button to see the rest of the fields.
I did not fill out any other fields under this section.

Finally, click on the <code>Generate Pipeline Script</code> button, 
the code to send email based on the information we fill out appears in the 
text box underneath the button, as seen:

![056-08.png](https://behainguyen.files.wordpress.com/2023/02/056-08.png)

<strong>Note also</strong>, <em>it seems that there is an idle
time set on this screen, too. If we leave it for too long then
clicking on the <code>Generate Pipeline Script</code> button, 
there would be no response. I had to do a hard refresh, losing
all unsaved information, and start again.</em>

Below is the original generated code:

```
mail bcc: '', body: 'This email was sent by a test Jenkins Pipeline job, using Gmail SMTP.', cc: '', from: '', replyTo: '', subject: 'Jenkins Pipeline job email', to: '***kiem@gmail.com'
```

I removed the <code>bcc</code>, <code>cc</code>, <code>from</code> and
<code>replyTo</code> fields, since they are empty; and wrapped the parameters 
in parentheses:

```
mail(body: 'This email was sent by a test Jenkins Pipeline job, using Gmail SMTP.', subject: 'Jenkins Pipeline job email', to: '***kiem@gmail.com')
```

Go back to the Pipeline <strong>General</strong> page, select 
<code>Hello World</code> as per the screen below:

![056-09.png](https://behainguyen.files.wordpress.com/2023/02/056-09.png)

Then, change <code>'Hello'</code> to <code>'Send Test Email'</code>,
and <code>echo 'Hello World'</code> with the modified code above. The 
final Pipeline:

```
pipeline {
    agent any

    stages {
        stage('Send Test Email') {
            steps {
                mail(body: 'This email was sent by a test Jenkins Pipeline job, using Gmail SMTP.', subject: 'Jenkins Pipeline job email', to: '***kiem@gmail.com')
            }
        }
    }
}
```

Click on the <code>Save</code> button to save the Pipeline and to 
move to the project page. Then click <code>▷ Build Now</code> to 
run. It should run successfully:

![056-10.png](https://behainguyen.files.wordpress.com/2023/02/056-10.png)

And we should receive the email as expected:

![056-11.png](https://behainguyen.files.wordpress.com/2023/02/056-11.png)

This post is a baby step to understand how email works in Jenkins. There are much
more to email. I have tried the Gmail API before, e.g.:
<a href="https://behainguyen.wordpress.com/2022/05/09/gmail-api-quick-start-with-python-and-nodejs/"
title="GMail API: quick start with Python and NodeJs." target="_blank">GMail API: quick start with Python and NodeJs</a>, 
and 
<a href="https://behainguyen.wordpress.com/2022/05/11/gmail-api-send-emails-with-nodejs/" 
title="GMail API: send emails with NodeJs." target="_blank">GMail API: send emails with NodeJs.</a>
-- It is tough. With <strong>App passwords</strong>, Gmail SMTP server seems much easier to use.
We don't have to use Gmail, there're other free services available, but I haven't tried any yet.

I'll feel comfortable knowing how email works in Jenkins. And I hope the information in 
this post is useful. Thank you for reading and stay safe as always.

✿✿✿

PS: I have already removed the Gmail SMTP password used in this post 😂, and generated
a new one -- we can do that and Jenkins email should still work.