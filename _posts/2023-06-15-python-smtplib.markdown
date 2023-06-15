---
layout: post
title: "Sending emails via Gmail account using the Python module smtplib."
description: We look at using our own Gmail account to send emails via the Python module smtplib. We'll cover issues such as port 587 and port 465; plain text and HTML emails; emails with attachments; different classes used to create an email message. 
tags:
- Email
- Gmail 
- Python 
- smtplib
---

<em style="color:#111;">We look at using our own Gmail account to send emails via the Python module smtplib. We'll cover issues such as port 587 and port 465; plain text and HTML emails; emails with attachments; different classes used to create an email message.</em>

| ![071-feature-image.png](https://behainguyen.files.wordpress.com/2023/06/071-feature-image.png) |
|:--:|
| *Sending emails via Gmail account using the Python module smtplib.* |

Some posts related to emails I've written previously:

<ol>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/05/09/gmail-api-quick-start-with-python-and-nodejs/"
title="GMail API: quick start with Python and NodeJs." target="_blank">GMail API: quick start with Python and NodeJs</a>.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2022/05/11/gmail-api-send-emails-with-nodejs/" 
title="GMail API: send emails with NodeJs." target="_blank">GMail API: send emails with NodeJs</a>.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2023/02/03/ci-cd-02-jenkins-basic-email-using-your-gmail-account/" 
title="CI/CD #02. Jenkins: basic email using your Gmail account." target="_blank">CI/CD #02. Jenkins: basic email using your Gmail account</a>.
</li>
</ol>

This post will continue on with some of the information presented in 
the last post in the above list: <strong><em>we're using the same 
Gmail credential which we use in Jenkins. This time, we're using this
credential to send emails using the Python module <a href="https://docs.python.org/3/library/smtplib.html"
title="smtplib — SMTP protocol client" target="_blank">smtplib</a> 
— SMTP protocol client.</em></strong>

Since February, 2023, the time the above mentioned last post was written,
there appear to be some changes in the 
<span style="content: url('https://www.gstatic.com/images/branding/googlelogo/svg/googlelogo_clr_74x24px.svg');display: inline-block; height: 24px; width: 74px;vertical-align: middle;"></span>
<span style="color: #5f6368;opacity: 1;display: inline-block;font-family: 'Product Sans',Arial,sans-serif;font-size:1em;line-height: 24px;position: relative;top: -1.5px;vertical-align: middle;text-rendering: optimizeLegibility;">Account</span>
page area: the <code>Security</code> screen no longer has the link 
<code>App passwords</code>.

However, as of June, 2023, this option is still available via the following
link:

-- <a href="https://myaccount.google.com/apppasswords" title="Google App passwords" target="_blank">https://myaccount.google.com/apppasswords</a>

We'll get the <code>App passwords</code> screen:

![071-01.png](https://behainguyen.files.wordpress.com/2023/06/071-01.png)

We can delete existing ones and create new ones. The following screen from 
the above mentioned last post, where we generated a new one:

![056-03-1.png](https://behainguyen.files.wordpress.com/2023/02/056-03-1.png)

Following are the required information for the Gmail SMTP server:

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
SMTP ports: <code>465</code> and <code>587</code> -- see also 
<a href="https://sendgrid.com/blog/whats-the-difference-between-ports-465-and-587/"
title="SMPT Port 465 and Port 587: What’s the Difference?" target="_blank">SMPT Port 465 and Port 587: What’s the Difference?</a>
</li>
</ul>

Using the above Gmail SMTP information, we'll demonstrate sending 
emails using the Python module 
<a href="https://docs.python.org/3/library/smtplib.html"
title="smtplib — SMTP protocol client" target="_blank">smtplib</a>.
We'll look at both ports <code>587</code> 
(TLS or Transport Layer Security mode), and <code>465</code>
(SSL or Secure Socket Layer);
plain text and HTML emails; emails with attachments; classes
<a href="https://docs.python.org/3/library/email.message.html#email.message.EmailMessage" title="EmailMessage" target="_blank">EmailMessage</a>
and 
<a href="https://docs.python.org/3/library/email.mime.html?mimemultipart#email.mime.multipart.MIMEMultipart" title="MIMEMultipart" target="_blank">MIMEMultipart</a> 
(Multipurpose Internet Mail Extensions).

<h2>Table of contents</h2>

<ul>
	<li style="margin-top:10px;"><a href="#script-org">Script organisation</a></li>
	
	<li style="margin-top:10px;"><a href="#smtplib-ports-587-465">Python module 
        smtplib and ports <code>587</code>, <code>465</code></a>
	    <ul>
		   <li style="margin-top:10px;"><a href="#port-587">Port 587 -- TLS or Transport Layer Security mode</a></li>
		   <li style="margin-top:10px;"><a href="#port-465">Port 465 -- SSL or Secure Socket Layer</a></li>
	    </ul>
	</li>

	<li style="margin-top:10px;"><a href="#html-emails">HTML emails</a>
	    <ul>
		   <li style="margin-top:10px;"><a href="#html-emailmessage">Using EmailMessage class</a></li>
		   <li style="margin-top:10px;"><a href="#html-mimemultipart">Using MIMEMultipart class</a>
		   </li>
	    </ul>	
	</li>

	<li style="margin-top:10px;"><a href="#emails-attachments">Emails with attachments</a>
	    <ul>
		   <li style="margin-top:10px;"><a href="#attachment-emailmessage">Using EmailMessage class</a>
		   </li>
		   <li style="margin-top:10px;"><a href="#attachment-mimemultipart">Using MIMEMultipart class</a>
		   </li>
	    </ul>	
	</li>
	
	<li style="margin-top:10px;"><a href="#concluding-remarks">Concluding remarks</a></li>
</ul>

<h3 style="color:teal;">
  <a id="script-org">Script organisation</a>
</h3>

There's no virtual environment, we're not using any third party
packages in this post, all scripts, and test emails' attachment files are in 
the same directory. The <code>Python</code> executable is the 
global installation one.

The commands to run any script:

```
python <script_name.py>
python3 <script_name.py>
```

On Windows 10, all scripts have been tested with Python <code>version 3.11.0</code>.
On Ubuntu 22.10, all scripts have been tested with Python <code>version 3.10.7</code>.

Common constants used across all scripts are defined in <code>constants.py</code>.

```
Content of constants.py:
```

{% highlight python %}
host = 'smtp.gmail.com'
port_ssl = 465
port_tls = 587
# Use your own Gmail account.
user_name = 'YOUR_USER_NAME@gmail.com'
# Use your own Gmail account password: this password is no longer valid.
# I test the scripts with a different password.
password = 'gwrnafeanafjlgsj'
# Use your own test email account, which you have access to.
receiver_email = 'YOUR_USER_NAME@hotmail.com'

local_host = 'localhost'
local_port = 8500

text_email = ("""\
    Hello!

    Test email sent from Python SMTP Library, using {0}, port {1}.

    Official documentation: https://docs.python.org/3/library/smtplib.html

    Sent by script: {2}.

    ...behai
    """)

html_email = """\
    <html>
    <head></head>
    <body>
        <p>Hello!</p>

        <p>Test email sent from Python SMTP Library, using {0}, port {1}.</p>
        
        <p>
        Official documentation: <a href="https://docs.python.org/3/library/smtplib.html">
            smtplib</a> — SMTP protocol client.
        </p>

        <p>Sent by script: {2}.</p>

        <p>...behai</p>
    </body>
    </html>
"""

# Attachment files: they are in the same directory as the script files.
#
# happy_cat.jpg's URL: https://behainguyen.files.wordpress.com/2023/06/happy_cat.jpg
jpg_filename = 'happy_cat.jpg'
# Use a small PDF as 'optus_payment.pdf', or change this value to some PDF name you
# have available.
pdf_filename = 'optus_payment.pdf'

def guess_mimetypes(file_name: str) -> tuple:
    """Guessing MIME maintype and subtype from a file name.

    See also `mimetypes <https://docs.python.org/3/library/mimetypes.html>`_. 

    :param str file_name: absolute file name whose MIME maintype and subtype 
        are to be determined.

    :return: MIME maintype and subtype as a tuple.
    :rtype: tuple.
    """
    import mimetypes

    mimetype, _ = mimetypes.guess_type(file_name)
    types = mimetype.split('/')
    
    return types[0], types[1]
{% endhighlight %}

Please read comments in module <code>constants.py</code>, you will need to substitute 
your own values for the noted constants.

<h3 style="color:teal;">
  <a id="smtplib-ports-587-465">Python module <a href="https://docs.python.org/3/library/smtplib.html"
    title="smtplib — SMTP protocol client" target="_blank">smtplib</a> and 
    ports <code>587</code>, <code>465</code>
  </a>
</h3>

In the context of the <a href="https://docs.python.org/3/library/smtplib.html" title="smtplib — SMTP protocol client" target="_blank">smtplib</a>
module, to use <code>port 587</code> or <code>port 465</code>, requires
(only) how the SMTP protocol client is created and initialised, from 
thence on, everything should be the same.

Let's have a look some examples, we start with an example on
<code>port 587</code> (TLS), following by another one for 
<code>port 465</code> (SSL).

<h4>
  <a id="port-587">Port 587 -- TLS or Transport Layer Security mode</a>
</h4>

```
Content of tls_01.py:
```

{% highlight python linenos %}
from smtplib import (
    SMTP,
    SMTPHeloError,
    SMTPAuthenticationError,
    SMTPNotSupportedError,
    SMTPException,
    SMTPRecipientsRefused,
    SMTPSenderRefused,
    SMTPDataError,
)
import ssl
from email.message import EmailMessage

from constants import (
    host,
    port_tls,
    user_name,
    password,
    receiver_email,
    text_email,
)

server = SMTP(host, port_tls)
try:
    # server.ehlo() call can be omitted.
    server.ehlo()
    
    # Put the SMTP connection in TLS (Transport Layer Security) mode.
    # ssl.create_default_context(): secure SSL context.
    server.starttls(context=ssl.create_default_context())
    
    # server.ehlo() call can be omitted.
    server.ehlo()
    # SMTP server authentication.
    server.login(user_name, password)

    # Create and populate the email to be sent.
    msg = EmailMessage()

    msg['Subject'] = f'Test email: TLS/{port_tls}.'
    msg['From'] = user_name
    msg['To'] = receiver_email
    msg.set_content(text_email.format('TLS', port_tls, __file__))

    # Both send_message(...) and sendmail(...) work.
    # send_message(...) will eventually call to sendmail(...).
    #
    # server.send_message(msg)

    server.sendmail(user_name, receiver_email, msg.as_string())

    server.quit()

except SMTPHeloError as e:
    print("The server didn’t reply properly to the HELO greeting.")
    print(str(e))

except SMTPAuthenticationError as e:
    print("The server didn’t accept the username/password combination.")
    print(str(e))

except SMTPNotSupportedError as e:
    print("The AUTH command is not supported by the server.")
    print(str(e))

except SMTPException as e:
    print("No suitable authentication method was found.")
    print(str(e))

except SMTPRecipientsRefused as e:
    print("All recipients were refused. Nobody got the mail.")
    print(str(e))

except SMTPSenderRefused as e:
    print("The server didn’t accept the from_addr.")
    print(str(e))

except SMTPDataError as e:
    print("The server replied with an unexpected error code (other than a refusal of a recipient).")
    print(str(e))
{% endhighlight %}

<ul>
<li style="margin-top:10px;">
Line 23: we create an instance of the SMTP protocol client
via the class <a href="https://docs.python.org/3/library/smtplib.html#smtplib.SMTP" title="smtplib.SMTP" target="_blank">SMTP</a>,
using the Gmail host name, and <code>port 587</code>.
</li>

<li style="margin-top:10px;">
Lines 26 and 33: please see <a href="https://docs.python.org/3/library/smtplib.html#smtplib.SMTP.ehlo" title="SMTP.ehlo(name='')" target="_blank">SMTP.ehlo(name='')</a>.
Leave them out, and this script still works.
</li>

<li style="margin-top:10px;">
Line 30: compulsory, we must call 
<a href="https://docs.python.org/3/library/smtplib.html#smtplib.SMTP.starttls"
title="smtplib.SMTP.starttls" target="_blank">starttls(...)</a> to
put our SMTP connection to TLS (Transport Layer Security) mode, which uses
<code>port 587</code>.
</li>

<li style="margin-top:10px;">
Line 35: Gmail requires authentication. We must call 
<a href="https://docs.python.org/3/library/smtplib.html#smtplib.SMTP.login"
title="smtplib.SMTP.login" target="_blank">login(...)</a>.
</li>

<li style="margin-top:10px;">
Lines 38-43: we create a simple plain text email, using class 
<a href="https://docs.python.org/3/library/email.message.html#email.message.EmailMessage"
title="email.message.EmailMessage" target="_blank">EmailMessage</a>.
</li>

<li style="margin-top:10px;">
Line 43: call method 
<a href="https://docs.python.org/3/library/email.message.html#email.message.EmailMessage.set_content"
title="email.message.EmailMessage.set_content" target="_blank">set_content(...)</a>
to set the actual plain text email message.
</li>

<li style="margin-top:10px;">
Line 50: send the email out. Please note, both
<a href="https://docs.python.org/3/library/smtplib.html#smtplib.SMTP.sendmail"
title="smtplib.SMTP.sendmail"
target="_blank">sendmail(...)</a> and 
<a href="https://docs.python.org/3/library/smtplib.html#smtplib.SMTP.send_message"
title="smtplib.SMTP.send_message"
target="_blank">send_message(...)</a> work. I would actually prefer the latter.
</li>

<li style="margin-top:10px;">
Line 52: 
<a href="https://docs.python.org/3/library/smtplib.html#smtplib.SMTP.quit" title="smtplib.SMTP.quit" target="_blank">quit()</a>,
as per documentation, terminate the SMTP session and close the connection.
</li>

<li style="margin-top:10px;">
Lines 54-80: both 
<a href="https://docs.python.org/3/library/smtplib.html#smtplib.SMTP.login"
title="smtplib.SMTP.login" target="_blank">login(...)</a>.
and 
<a href="https://docs.python.org/3/library/smtplib.html#smtplib.SMTP.sendmail"
title="smtplib.SMTP.sendmail"
target="_blank">sendmail(...)</a> can potentially raise exceptions. 
For illustration purposes, we're listing out all exceptions 
which these two can potentially raise.
</li>
</ul>

<h4>
  <a id="port-465">Port 465 -- SSL or Secure Socket Layer</a>
</h4>

The SSL script, which uses <code>port 465</code> follows.

```
Content of ssl_01.py:
```

{% highlight python linenos %}
from smtplib import (
    SMTP_SSL,
    SMTPHeloError,
    SMTPAuthenticationError,
    SMTPNotSupportedError,
    SMTPException,
    SMTPRecipientsRefused,
    SMTPSenderRefused,
    SMTPDataError,
)
import ssl
from email.message import EmailMessage

from constants import (
    host,
    port_ssl,
    user_name,
    password,
    receiver_email,
    text_email,
)

# ssl.create_default_context(): secure SSL context.
server = SMTP_SSL(host, port_ssl, context=ssl.create_default_context())
try:
    # SMTP server authentication.
    server.login(user_name, password)

    # Create and populate the email to be sent.
    msg = EmailMessage()
    
    msg['Subject'] = f'Test email: SSL/{port_ssl}.'
    msg['From'] = user_name
    msg['To'] = receiver_email
    msg.set_content(text_email.format('SSL', port_ssl, __file__))

    # Both send_message(...) and sendmail(...) work.
    # send_message(...) will eventually call to sendmail(...).
    #
    # server.send_message(msg)

    server.sendmail(user_name, receiver_email, msg.as_string())

    server.quit()

except SMTPHeloError as e:
    print("The server didn’t reply properly to the HELO greeting.")
    print(str(e))

except SMTPAuthenticationError as e:
    print("The server didn’t accept the username/password combination.")
    print(str(e))

except SMTPNotSupportedError as e:
    print("The AUTH command is not supported by the server.")
    print(str(e))

except SMTPException as e:
    print("No suitable authentication method was found.")
    print(str(e))

except SMTPRecipientsRefused as e:
    print("All recipients were refused. Nobody got the mail.")
    print(str(e))

except SMTPSenderRefused as e:
    print("The server didn’t accept the from_addr.")
    print(str(e))

except SMTPDataError as e:
    print("The server replied with an unexpected error code (other than a refusal of a recipient).")
    print(str(e))
{% endhighlight %}

<ul>
<li style="margin-top:10px;">
Line 24: we create an instance of the SMTP protocol client via 
the class <a href="https://docs.python.org/3/library/smtplib.html#smtplib.SMTP_SSL" title="smtplib.SMTP_SSL" target="_blank">SMTP_SSL</a>, 
using the Gmail host name, and <code>port 465</code>. 
This is the only difference to the above TLS script. The rest is pretty much identical.
</li>
</ul>

From this point on, we will use TLS or <code>port 587</code>; we'll
also cut down the exception block.

🚀 We've covered plain text emails, and also the 
<a href="https://docs.python.org/3/library/email.message.html#email.message.EmailMessage" title="EmailMessage" target="_blank">EmailMessage</a>
class.

<h3 style="color:teal;">
  <a id="html-emails">HTML emails</a>
</h3>

We create and send emails in HTML using both 
classes
<a href="https://docs.python.org/3/library/email.message.html#email.message.EmailMessage" title="EmailMessage" target="_blank">EmailMessage</a>
and 
<a href="https://docs.python.org/3/library/email.mime.html?mimemultipart#email.mime.multipart.MIMEMultipart" title="MIMEMultipart" target="_blank">MIMEMultipart</a> 
(Multipurpose Internet Mail Extensions).

For <code>MINE type</code> and <code>MINE subtype</code>, see this MDM Web Docs' page  
<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types"
title="MIME types (IANA media types)" target="_blank">MIME types (IANA media types)</a>.

HTML emails are "multipart" emails. They have a plain text version alongside 
the HTML version. For explanations, see this article 
<a href="https://www.litmus.com/blog/best-practices-for-plain-text-emails-a-look-at-why-theyre-important/"
title="Why You Shouldn’t Dismiss Plain Text Emails (And How to Make Them Engaging)"
target="_blank">Why You Shouldn’t Dismiss Plain Text Emails (And How to Make Them Engaging)</a>.

<!--------------------------------------------------------------------------------->
<h4>
  <a id="html-emailmessage">Using  
  <a href="https://docs.python.org/3/library/email.message.html#email.message.EmailMessage" 
  title="EmailMessage" target="_blank">EmailMessage</a> class
  </a>
</h4>

Almost identical to creating and sending plain text emails,
we just need to add in the HTML content.

```
Content of tls_html_02.py:
```

{% highlight python linenos %}
from smtplib import SMTP
import ssl
from email.message import EmailMessage

from constants import (
    host,
    port_tls,
    user_name,
    password,
    receiver_email,
    text_email,
    html_email,
)

server = SMTP(host, port_tls)
try:
    # Put the SMTP connection in TLS (Transport Layer Security) mode.
    # ssl.create_default_context(): secure SSL context.
    server.starttls(context=ssl.create_default_context())
    # SMTP server authentication.
    server.login(user_name, password)

    msg = EmailMessage()

    msg['Subject'] = f'Test email: TLS/{port_tls}.'
    msg['From'] = user_name
    msg['To'] = receiver_email

    msg.set_content(text_email.format('TLS', port_tls, __file__), subtype='plain')
    msg.add_alternative(html_email.format('TLS', port_tls, __file__), subtype='html')

    # send_message(...) will eventually call to sendmail(...).
    # server.send_message(msg)

    server.sendmail(user_name, receiver_email, msg.as_string())

    server.quit()

except Exception as e:
    print("Some exception has occurred...")
    print(str(e))
{% endhighlight %}

<ul>
<li style="margin-top:10px;">
Line 29: we pass in an additional named argument <code>subtype='plain'</code> to method
<a href="https://docs.python.org/3/library/email.message.html#email.message.EmailMessage.set_content"
title="email.message.EmailMessage.set_content" target="_blank">set_content(...)</a>.
This is optional, without this named argument, Hotmail still displays it as HTML.
</li>

<li style="margin-top:10px;">
Line 30: use method 
<a href="https://docs.python.org/3/library/email.message.html#email.message.EmailMessage.add_alternative"
title="email.message.EmailMessage.add_alternative" target="_blank">add_alternative(...)</a> 
to set the HTML content. The named argument <code>subtype='html'</code> is required, 
without it, most likely mail clients would just display the plain text version. Hotmail does.
</li>
</ul>

<h4>
  <a id="html-mimemultipart">
  Using 
  <a href="https://docs.python.org/3/library/email.mime.html?mimemultipart#email.mime.multipart.MIMEMultipart" title="MIMEMultipart" target="_blank">MIMEMultipart</a> 
  class
  </a>
</h4>

From the documentation, it seems that the 
<a href="https://docs.python.org/3/library/email.mime.html?mimemultipart#email.mime.multipart.MIMEMultipart" title="MIMEMultipart" target="_blank">MIMEMultipart</a> 
class is older than the 
<a href="https://docs.python.org/3/library/email.message.html#email.message.EmailMessage" title="EmailMessage" target="_blank">EmailMessage</a> 
class, which has been introduced only in Python version 3.6. 
However, there is no mention of deprecation.

```
Content of tls_html_03.py:
```

{% highlight python linenos %}
from smtplib import SMTP
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from constants import (
    host,
    port_tls,
    user_name,
    password,
    receiver_email,
    text_email,
    html_email,
)

server = SMTP(host, port_tls)
try:
    # Put the SMTP connection in TLS (Transport Layer Security) mode.
    # ssl.create_default_context(): secure SSL context.
    server.starttls(context=ssl.create_default_context())
    # SMTP server authentication.
    server.login(user_name, password)

    msg = MIMEMultipart('mixed')

    msg['Subject'] = f'Test email: TLS/{port_tls}.'
    msg['From'] = user_name
    msg['To'] = receiver_email

    msg_related = MIMEMultipart('related')
    msg_alternative = MIMEMultipart('alternative')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg_alternative.attach(MIMEText(text_email.format('TLS', port_tls, __file__), 'plain'))
    msg_alternative.attach(MIMEText(html_email.format('TLS', port_tls, __file__), 'html'))

    msg_related.attach(msg_alternative)
    msg.attach(msg_related)

    # send_message(...) will eventually call to sendmail(...).
    server.send_message(msg)

    # server.sendmail(user_name, receiver_email, msg.as_string())

    server.quit()

except Exception as e:
    print("Some exception has occurred...")
    print(str(e))
{% endhighlight %}

<ul>
<li style="margin-top:10px;">
Lines 24, 30, 31: we create the message instances using the 
<a href="https://docs.python.org/3/library/email.mime.html?mimemultipart#email.mime.multipart.MIMEMultipart" title="MIMEMultipart" target="_blank">MIMEMultipart</a> 
class. On <code>mixed</code>, <code>related</code> and <code>alternative</code>
values for <code>_subtype</code> -- see this <a href="https://stackoverflow.com/a/66551704"
title="Stackoverflow answer" target="_blank">Stackoverflow answer</a>, particularly the
<em>“MIME Hierarchies of Body Parts”</em> chart.
</li>

<li style="margin-top:10px;">
Lines 36 and 37: we use the class 
<a href="https://docs.python.org/3/library/email.mime.html?mimemultipart#email.mime.text.MIMEText"
title="email.mime.text.MIMEText" target="_blank">MIMEText</a> to create plain
text and HTML content; as per the documentation, this class is used to create 
MIME objects of major type <code>text</code>.
</li>

<li style="margin-top:10px;">
Line 43: we switch to method 
<a href="https://docs.python.org/3/library/smtplib.html#smtplib.SMTP.send_message"
title="smtplib.SMTP.send_message" target="_blank">send_message(...)</a> 
to demonstrate that it works also.
</li>
</ul>

🚀 We've covered HTML emails, using both 
<a href="https://docs.python.org/3/library/email.message.html#email.message.EmailMessage" title="EmailMessage" target="_blank">EmailMessage</a>
and
<a href="https://docs.python.org/3/library/email.mime.html?mimemultipart#email.mime.multipart.MIMEMultipart" title="MIMEMultipart" target="_blank">MIMEMultipart</a>
classes to create email messages to be sent.

<h3 style="color:teal;">
  <a id="emails-attachments">Emails with attachments</a>
</h3>

We attach an image file and a PDF file to email messages.
The process for other file types should be similar.

<h4>
  <a id="attachment-emailmessage">
  Using 
  <a href="https://docs.python.org/3/library/email.message.html#email.message.EmailMessage" title="EmailMessage" target="_blank">EmailMessage</a>
  class
  </a>
</h4>

We also use an HTML email. Most of the code remains the same
as the <a href="#html-emailmessage">previous example</a>.

```
Content of tls_html_04.py:
```

{% highlight python linenos %}
from smtplib import SMTP
import ssl
from email.message import EmailMessage

from constants import (
    host,
    port_tls,
    user_name,
    password,
    receiver_email,
    text_email,
    html_email,
    jpg_filename,
    pdf_filename,
    guess_mimetypes,
)

server = SMTP(host, port_tls)
try:
    # Put the SMTP connection in TLS (Transport Layer Security) mode.
    # ssl.create_default_context(): secure SSL context.
    server.starttls(context=ssl.create_default_context())
    # SMTP server authentication.
    server.login(user_name, password)

    msg = EmailMessage()

    msg['Subject'] = f'Test email: TLS/{port_tls}.'
    msg['From'] = user_name
    msg['To'] = receiver_email

    msg.set_content(text_email.format('TLS', port_tls, __file__), subtype='plain')
    msg.add_alternative(html_email.format('TLS', port_tls, __file__), subtype='html')

    with open(jpg_filename, 'rb') as fp:
        img_data = fp.read()
    mtype, stype = guess_mimetypes(jpg_filename)
    msg.add_attachment(img_data, maintype=mtype, subtype=stype, filename=jpg_filename)

    with open(pdf_filename, 'rb') as fp:
        pdf_data = fp.read()
    mtype, stype = guess_mimetypes(jpg_filename)
    msg.add_attachment(pdf_data, maintype=mtype, subtype=stype, filename=pdf_filename)

    # send_message(...) will eventually call to sendmail(...).
    server.send_message(msg)

    # server.sendmail(user_name, receiver_email, msg.as_string())

    server.quit()

except Exception as e:
    print("Some exception has occurred...")
    print(str(e))
{% endhighlight %}

<ul>
<li style="margin-top:10px;">
Lines 35-43: call method 
<a href="https://docs.python.org/3/library/email.message.html#email.message.EmailMessage.add_attachment"
title="email.message.EmailMessage.add_attachment"
target="_blank">add_attachment(...)</a> to attach the image and the PDF files. 
The rest of the code we've gone through before.
</li>
</ul>

It seems that we can get away with not having to worry about the message 
<code>Content-Type</code> property, which should be <code>multipart/mixed</code> 
in this case. Hotmail shows the correct <code>Content-Type</code>:

![071-02.png](https://behainguyen.files.wordpress.com/2023/06/071-02.png)

<h4>
  <a id="attachment-mimemultipart">
  Using 
  <a href="https://docs.python.org/3/library/email.mime.html?mimemultipart#email.mime.multipart.MIMEMultipart" title="MIMEMultipart" target="_blank">MIMEMultipart</a>
  class
  </a>
</h4>

The script below is also an extension of the previous script in the section 
<a href="#html-mimemultipart">HTML email using MIMEMultipart class</a>.

We're using the class
<a href="https://docs.python.org/3/library/email.mime.html#email.mime.application.MIMEApplication"
title="email.mime.application.MIMEApplication" target="_blank">MIMEApplication</a>
to create email attachments. 

```
Content of tls_html_05.py:
```

{% highlight python linenos %}
from os.path import basename
from smtplib import SMTP
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from constants import (
    host,
    port_tls,
    user_name,
    password,
    receiver_email,
    text_email,
    html_email,
    jpg_filename,
    pdf_filename,
)

server = SMTP(host, port_tls)
try:
    # Put the SMTP connection in TLS (Transport Layer Security) mode.
    # ssl.create_default_context(): secure SSL context.
    server.starttls(context=ssl.create_default_context())
    # SMTP server authentication.
    server.login(user_name, password)

    msg = MIMEMultipart('mixed')

    msg['Subject'] = f'Test email: TLS/{port_tls}.'
    msg['From'] = user_name
    msg['To'] = receiver_email

    msg_related = MIMEMultipart('related')
    msg_alternative = MIMEMultipart('alternative')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg_alternative.attach(MIMEText(text_email.format('TLS', port_tls, __file__), 'plain'))
    msg_alternative.attach(MIMEText(html_email.format('TLS', port_tls, __file__), 'html'))

    msg_related.attach(msg_alternative)

    with open(jpg_filename, 'rb') as fp:
        img_data = MIMEApplication(fp.read(), Name=basename(jpg_filename))
        img_data['Content-Disposition'] = f'attachment; filename="{basename(jpg_filename)}"'
    msg_related.attach(img_data)

    with open(pdf_filename, 'rb') as fp:
        pdf_data = MIMEApplication(fp.read(), Name=basename(pdf_filename))
        pdf_data['Content-Disposition'] = f'attachment; filename="{basename(pdf_filename)}"'
    msg_related.attach(pdf_data)
    
    msg.attach(msg_related)    

    # send_message(...) will eventually call to sendmail(...).
    server.send_message(msg)

    # server.sendmail(user_name, receiver_email, msg.as_string())

    server.quit()

except Exception as e:
    print("Some exception has occurred...")
    print(str(e))
{% endhighlight %}

<ul>
<li style="margin-top:10px;">
Lines 45-53: we create attachments and attach them to the email message.
For an explanation on <code>Content-Disposition</code> header, see this
MDM Web Docs' page 
<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition"
title="Content-Disposition" target="_blank">Content-Disposition</a>.
</li>
</ul>

<code>Content-Type</code> as shown by Hotmail:

![071-03.png](https://behainguyen.files.wordpress.com/2023/06/071-03.png)

🚀 We've covered emails with attachments, using both 
<a href="https://docs.python.org/3/library/email.message.html#email.message.EmailMessage" title="EmailMessage" target="_blank">EmailMessage</a>
and
<a href="https://docs.python.org/3/library/email.mime.html?mimemultipart#email.mime.multipart.MIMEMultipart" title="MIMEMultipart" target="_blank">MIMEMultipart</a>
classes to create the email messages to be sent.

<h3 style="color:teal;">
  <a id="concluding-remarks">Concluding remarks</a>
</h3>

I hope I've not made any mistakes in this post. There're a vast number
of other methods in this area to study, we've only covered what I think
is the most use case scenarios.

I think 
<a href="https://docs.python.org/3/library/email.message.html#email.message.EmailMessage" title="EmailMessage" target="_blank">EmailMessage</a>
class requires less work. I would opt to use this class rather than the
<a href="https://docs.python.org/3/library/email.mime.html?mimemultipart#email.mime.multipart.MIMEMultipart" title="MIMEMultipart" target="_blank">MIMEMultipart</a> class.

Years ago, I've implemented a DLL in Delphi which pulls internal mail boxes 
at regular intervals and processes the emails. It would be interesting to
look at the email reading functionalities of the 
<a href="https://docs.python.org/3/library/smtplib.html"
title="smtplib — SMTP protocol client" target="_blank">smtplib</a>.

Thank you for reading. I hope the information in this post is useful. Stay safe as always.

✿✿✿

Feature image sources:

<ul>
<li>
<a href="https://in.pinterest.com/pin/337277459600111737/" target="_blank">https://in.pinterest.com/pin/337277459600111737/</a>
</li>
<li>
<a href="https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper" target="_blank">https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper</a>
</li>
<li>
<a href="https://seeklogo.com/vector-logo/332789/python" target="_blank">https://seeklogo.com/vector-logo/332789/python</a>
</li>
</ul>
