---
layout: post
title: "Google Cloud Translation API: Local Development Environment Quick Start - Windows 10 and Ubuntu 22.10"

description: The process of obtaining credentials to use the Google Cloud Translation API (referred to as Google Translation from now on) in a local development environment is slightly different from the YouTube Data API v3 and Google AI Gemini API, both of which we have covered previously. This post describes the steps I took to set up the credentials and successfully run the official example. 

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/112-01.png"

gallery-image-list-2:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/112-02.png"

gallery-image-list-3:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/112-03.png"

gallery-image-list-4:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/112-04.png"

gallery-image-list-5:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/112-05a.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/112-05b.png"

gallery-image-list-6:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/112-06.png"

gallery-image-list-7:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/112-07-ubuntu.png"

gallery-image-list-8:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/112-08a-ubuntu.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/112-08b-ubuntu.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/112-08c-ubuntu.png"

gallery-image-list-9:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/112-09a.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/112-09b.png"

tags:
- Google Cloud Translation API
- Google
- Cloud
- Translation
- API
- Python
---

<em>The process of obtaining credentials to use the Google Cloud Translation API (referred to as <code>Google Translation</code> from now on) in a local development environment is slightly different from the <code>YouTube Data API v3</code> and <code>Google AI Gemini API</code>, both of which we have covered previously. This post describes the steps I took to set up the credentials and successfully run the official example.</em>

| ![112-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/06/112-feature-image.png) |
|:--:|
| *Google Cloud Translation API: Local Development Environment Quick Start - Windows 10 and Ubuntu 22.10* |

We previously covered two Google APIs:

<ol>
<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2024/06/01/using-the-youtube-data-api-v3-with-api-keys-and-oauth-2-0/" 
title="Using the YouTube Data API v3 with API Keys and OAuth 2.0" target="_blank">Using the YouTube Data API v3 with API Keys and OAuth 2.0</a>.
</li>

<li style="margin-top:10px;">
<a href="https://behainguyen.wordpress.com/2024/06/05/google-ai-gemini-api-a-complete-example-of-a-python-flask-chatbot/" 
title="Google AI Gemini API: A Complete Example of a Python Flask ChatBot" 
target="_blank">Google AI Gemini API: A Complete Example of a Python Flask ChatBot</a>
</li>
</ol>

Now, let's set up the credentials for <code>Google Translation</code> and 
get the official example running successfully.

<a id="setup-credentials"></a>
❶ Obtaining credentials involves two steps:

<ol>
<li style="margin-top:10px;">
Create a Google Cloud Project to house the 
<a href="https://cloud.google.com/translate/docs/reference/api-overview" 
title="Cloud Translation API" target="_blank">Cloud Translation API</a>.
</li>
<li style="margin-top:10px;">
Install and run the <code>gcloud CLI</code> to create the credentials 
file on the local development machine.
</li>
</ol>

<a id="create-cloud-project"></a>
⓵ Create a Google Cloud Project to house the
<a href="https://cloud.google.com/translate/docs/reference/api-overview" 
title="Cloud Translation API" target="_blank">Cloud Translation API</a>.

This step is similar to the first part of creating a cloud project for 
<a href="https://behainguyen.wordpress.com/2024/06/01/using-the-youtube-data-api-v3-with-api-keys-and-oauth-2-0/#create-google-cloud-project" 
title="Using the YouTube Data API v3 with API Keys and OAuth 2.0" 
target="_blank"><code>YouTube Data API v3</code></a>.

Using the <a href="https://console.cloud.google.com" 
title="Google Cloud Console" target="_blank">Google Cloud Console</a>, 
we create a new project and enable the <a href="https://cloud.google.com/translate/docs/reference/api-overview" 
title="Cloud Translation API" target="_blank">Cloud Translation API</a>.
That's all we need to do for now. (We create credentials in the next step.) 
We are then taken to a screen similar to the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-1 %}
<br/>

I left everything at the defaults. I accidentally clicked on the 
<code>CREATE CREDENTIALS</code> button, without any anticipation 
of what would happen next. On the next screen, as seen below:

{% include image-gallery.html list=page.gallery-image-list-2 %}
<br/>

I just selected <code>Application data</code> and clicked on the 
<code>DONE</code> button: then I was taken back to the previous screen. 
<strong>I'm not sure if this had any impact on the process.</strong> 
I'm unsure how to find these screens again when visiting the 
<a href="https://console.cloud.google.com" 
title="Google Cloud Console" target="_blank">Google Cloud Console</a>
subsequently.

<a id="install-run-cli"></a>
⓶ To access the <code>Google Translation</code> service from your local development machine, 
you'll need to create a credentials file using the <code>gcloud CLI</code>. Follow the 
instructions in the official documentation: <a href="https://cloud.google.com/sdk/docs/install" 
title="Install and initialize the gcloud CLI" target="_blank">Install and initialize the gcloud CLI</a>.

The final outcome of this process is the creation of a credentials 
JSON file, located at the following paths:

```
▶️Linux, macOS: $HOME/.config/gcloud/application_default_credentials.json
▶️Windows: %APPDATA%\gcloud\application_default_credentials.json
```

For more information about these credentials files, refer to the 
Google Cloud documentation on 
<a href="https://cloud.google.com/docs/authentication/application-default-credentials#personal" 
title="User credentials provided by using the gcloud CLI" 
target="_blank">User credentials provided by using the gcloud CLI</a>.

<a id="install-run-cli-win"></a>
● On Windows 10, after downloading the Google Cloud SDK installer 
(<code>GoogleCloudSDKInstaller.exe</code>), run it as an administrator. 
You will be prompted to log in to continue. Google will initiate an 
authentication process using your default web browser. Make sure to select 
the correct account. Once complete, you should see a screen like the one 
shown below:

{% include image-gallery.html list=page.gallery-image-list-3 %}
<br/>

<a id="install-run-cli-win-project"></a>
The console is now asking us to select a project. Please see the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-4 %}
<br/>

We should select the project we <a href="#create-cloud-project">just created</a>. 
The response is shown in the screenshots below:

{% include image-gallery.html list=page.gallery-image-list-5 %}
<br/>

<a id="install-run-cli-win-sqlite"></a>
The above process <strong>did not</strong> create the credentials file 
<code>application_default_credentials.json</code> in 
<code>C:\Users\behai\AppData\Roaming\gcloud\</code>. Instead, the folder contains 
<code>credentials.db</code>, <code>access_tokens.db</code> and <code>default_configs.db</code>, 
among other files. These three files are 
<a href="https://sqlite.org/" title="SQLite" target="_blank">SQLite</a> database files and, 
while they appear to contain credentials, they are not.

I attempted to run the official example at this point. I got the below exception: 

```
...
    raise exceptions.DefaultCredentialsError(_CLOUD_SDK_MISSING_CREDENTIALS) \
	google.auth.exceptions.DefaultCredentialsError: Your default credentials \
	were not found. To set up Application Default Credentials, see \ 
	https://cloud.google.com/docs/authentication/external/set-up-adc \
	for more information.
```

This was to be anticipated. Based on the link given in the above exception, 
I ran the following command:

```
▶️Windows 10: gcloud auth application-default login
```

<a id="install-run-cli-win-json"></a>
I followed the prompted instructions. The credentials file was created 
after the login process was completed successfully. 
<strong>And the official example executes successfully, too.</strong>
Please see the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-6 %}
<br/>

● On Ubuntu 22.10: I just followed the instructions in the document mentioned above, 
but for Linux: <a href="https://cloud.google.com/sdk/docs/install#linux" 
title="Install the gcloud CLI | Linux" target="_blank">Install the gcloud CLI | Linux</a>. 
It worked the first time. I am describing my observation of the process.

To determine the Linux platform and kernel architecture, run the following command:

```
▶️Ubuntu 22.10: behai@hp-pavilion-15:~$ uname -a
```

I have the following output:

```
Linux hp-pavilion-15 5.19.0-46-generic #47-Ubuntu SMP PREEMPT_DYNAMIC \
Fri Jun 16 13:30:11 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
```

So, the package name I need to download is
<code>google-cloud-cli-480.0.0-linux-x86_64.tar.gz</code>.

After installation, when running the commands to obtain credentials, ensure 
you have access to the desktop. The authentication process will require you 
to use a web browser to select your account and grant permissions, similar 
to the Windows process.

Note the following:

<span style="font-size:1.5em;font-weight:bold;">⑴</span> 
<strong>Running</strong> the command: 

```
▶️Ubuntu 22.10: ./google-cloud-sdk/bin/gcloud init
```

will initiate the authentication process using your default web browser. 
You will still need to select your project 
<a href="#install-run-cli-win-project">as described for Windows</a>. This 
command will create 
<a href="https://sqlite.org/" title="SQLite" target="_blank">SQLite</a> files, 
<a href="#install-run-cli-win-sqlite">as with the Windows process</a>, but it 
does not create the credentials file. See the screenshot below for reference:

{% include image-gallery.html list=page.gallery-image-list-7 %}
<br/>

<span style="font-size:1.5em;font-weight:bold;">⑵</span> <strong>The command</strong>: 

```
▶️Ubuntu 22.10: ./google-cloud-sdk/bin/gcloud auth application-default login
```

will also initiate the login process. Once completed, it will create 
the credentials file at <code>$HOME/.config/gcloud/application_default_credentials.json</code>. 
See the following screenshots for illustration:

{% include image-gallery.html list=page.gallery-image-list-8 %}
<br/>

<a id="run-the-python-example"></a>
❷ We are ready to run the example Python program.

<a id="run-install-python-lib"></a>
⓵ To use the 
<a href="https://cloud.google.com/translate/docs/setup#client_libraries" 
title="Cloud Translation - Advanced client libraries" 
target="_blank">Cloud Translation - Advanced client libraries</a>
for Python, we need to install them into the active virtual environment, 
<code>venv</code>. Use this command:

```
▶️Windows 10: (venv) F:\pydev>venv\Scripts\pip.exe install --upgrade google-cloud-translate
▶️Ubuntu 22.10: (venv) behai@hp-pavilion-15:~/pydev$ ./venv/bin/pip install --upgrade google-cloud-translate
```

<a id="run-copy-example"></a>
⓶ The example code is found on the following official page: 
<a href="https://cloud.google.com/translate/docs/advanced/translate-text-advance" 
title="Translate text with Cloud Translation Advanced" 
target="_blank">Translate text with Cloud Translation Advanced</a>. 
This code is not a ready-to-run example; we need to replace the marked constants 
with our own data, such as the <code>project_id</code>, and the text to be translated.

I modified the code to translate the following quote by 
<a href="https://en.wikipedia.org/wiki/Albert_Camus" title="Albert Camus" 
target="_blank">Albert Camus</a> into Vietnamese: 
<strong><em>“It is the job of thinking people not to be on the side of the executioners.”</em></strong>

```
Content of google_translate_01.py:
```

{% highlight python linenos %}
# Imports the Google Cloud Translation library
from google.cloud import translate

# Initialize Translation client
def translate_text(
    text: str, project_id: str
) -> translate.TranslationServiceClient:
    """Translating Text."""

    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    # Translate text from English to French
    # Detail on supported types can be found here:
    # https://cloud.google.com/translate/docs/supported-formats
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": "en-US",
            "target_language_code": "vi",
        }
    )

    # Display the translation for each input text provided
    for translation in response.translations:
        print(f"Translated text: {translation.translated_text}")

    return response

res = translate_text(
    'It is the job of thinking people not to be on the side of the executioners.', 
    'text-translation-20240615' )

print(res)
{% endhighlight %}

These screenshots demonstrate how to run the program and show its output.

{% include image-gallery.html list=page.gallery-image-list-9 %}
<br/>

While the translation isn't perfect, it's still comprehensible.

This example is not particularly useful on its own, but it serves as proof 
that the credentials we obtained are valid for using <code>Google Translation</code> 
within a local development environment.

<a id="concluding-remarks"></a>
❸ This credential setup exercise has been interesting and informative. While 
I've learned something new, there are still many other topics I haven't covered. 
This is a good starting point. If I want to do something more substantial with 
translation and speech-to-text, I now have a solid foundation to build on.

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
<a href="https://www.google.com/" target="_blank">https://www.google.com/</a>
</li>
<li>
<a href="https://lh3.googleusercontent.com/w1QGh5p564_r4oMo3rsX6n1gvnt4A-jWNn3xSekpKbrPrQ23a5TmfLuMF4to0YszlBopUlnLAhs-g8nVZXC-" target="_blank">https://lh3.googleusercontent.com/w1QGh5p564_r4oMo3rsX6n1gvnt4A-jWNn3xSekpKbrPrQ23a5TmfLuMF4to0YszlBopUlnLAhs-g8nVZXC-</a>
</li>
<li>
<a href="https://seeklogo.com/vector-logo/332789/python" target="_blank">https://seeklogo.com/vector-logo/332789/python</a>
</li>
</ul>
