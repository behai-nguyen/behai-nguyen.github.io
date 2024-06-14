---
layout: post
title: "Microsoft Azure AI: Quick Steps to Get Started with the Text to Speech API"

description: Microsoft Azure AI’s Text to Speech API (referred to as Azure TTS from now on) is not as intimidating as I first assumed based on some prior experiences. This post is my personal interpretation of the official documentation on how to get started with Azure TTS. The final outcomes of this post include&#58; ⓵ getting the official Python example to work locally, ⓶ updating the example to save the speech to an audio file on disk, and finally, ⓷ working with languages other than English that are available. 

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/111-01.png"

gallery-image-list-2:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/111-02.png"

gallery-image-list-3:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/111-03.png"

gallery-image-list-4:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/111-04.png"

gallery-image-list-5:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/111-05.png"

gallery-image-list-6:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/111-06.png"

gallery-image-list-7:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/111-07.png"

gallery-image-list-8:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/111-08a.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/111-08b.png"

tags:
- Python
- Microsoft Azure AI
- Microsoft
- Azure
- AI
- Text to Speech
- API
---

<em>Microsoft Azure AI’s Text to Speech API (referred to as <code>Azure TTS</code> from now on) is not as intimidating as I first assumed based on some prior experiences. This post is my personal interpretation of the official documentation on how to get started with <code>Azure TTS</code>. The final outcomes of this post include: ⓵ getting the official Python example to work locally, ⓶ updating the example to save the speech to an audio file on disk, and finally, ⓷ working with languages other than English that are available.</em>

| ![111-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/06/111-feature-image.png) |
|:--:|
| *Microsoft Azure AI: Quick Steps to Get Started with the Text to Speech API* |

<a id="create-azure-account"></a>
❶ To create an Azure account, visit the “Clouding Computing Services | Microsoft Azure” 
site at <a href="https://azure.microsoft.com/" title="Clouding Computing Services | Microsoft Azure" 
target="_blank">https://azure.microsoft.com/</a>, if you don’t already have one.

Azure may ask for credit card information. You’ll need to provide a valid card, 
including the CVV code. I created my account a few years ago, used it for a few days, 
and then left it inactive. When I accessed it again in June 2024, my credit card 
had already expired, and Azure requested an update. I haven’t been charged anything yet. 
I believe that even if we do get charged, it operates on a <em>pay-as-you-go</em> scheme. 
(I was charged several times by <a href="https://aws.amazon.com/" title="Amazon Web Services" 
target="_blank">Amazon Web Services</a>, but all charges were under 50 cents.)

<a id="api-key-region-code"></a>
❷ Create an Azure project to obtain the <code>API Key</code> and the 
<code>Location/Region</code>. Please note:

<ol>
<li style="margin-top:10px;">
We are provided with two keys, <code>KEY 1</code> and <code>KEY 2</code>. 
We only need to use <code>KEY 1</code> in the program code.
</li>

<li style="margin-top:10px;">
At runtime, the value of <code>KEY 1</code> is assigned to the environment 
variable named <code>SPEECH_KEY</code>, and the value of 
<code>Location/Region</code> is assigned to the <code>SPEECH_REGION</code>
environment variable.
</li>
</ol>

I had already created a project prior to this post. I created 
another one to take screenshots for this post.

⓵ Visit 
<a href="https://portal.azure.com/" 
title="The Azure Portal" target="_blank">https://portal.azure.com/</a>.
You will be greeted with a screen similar to the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-1 %}
<br/>

Click on the <code>+ Create a resource</code> icon to continue.

⓶ On the next screen, type <strong><em>speech</em></strong> into the 
search box and press the <code>Enter</code> key. From the results list, 
under <code>Speech Microsoft Azure Service</code>, click on the 
<code>Create ˅</code> link and select <code>Speech</code>. This is illustrated 
in the following screenshot:

{% include image-gallery.html list=page.gallery-image-list-2 %}
<br/>

⓷ On the next screen, titled <code>Create Speech Services</code>, fill in 
the form as illustrated in the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-3 %}
<br/>

Please note the following:

● For the <code>Subscription *</code> field: There seems to be only a single dropdown entry.

● For the <code>Resource group *</code> field: I used the 
<code>Create new</code> link to create a new entry.

● As mentioned above, I had already created a project prior to this, and the 
<code>Region</code> for this project is also <code>Australia East</code>. 
Hence, the notice about being unable to select the free tier (F0) pricing.

● For the <code>Pricing tier *</code> field: Please select 
<code>Free (F0)</code> – you should have this option in your list.

⓸ Click on the <code>Review + create</code> button. This will bring up 
the summary screen as illustrated below:

{% include image-gallery.html list=page.gallery-image-list-4 %}
<br/>

⓹ Click on the <code>Create</code> button to create the project. 
This will take you to a new screen, as shown in the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-5 %}
<br/>

⓺ Click on <code>Go to resource</code> to proceed. The next screen is shown below:

{% include image-gallery.html list=page.gallery-image-list-6 %}
<br/>

<a id="tts-api-key-region"></a>
⓻ As mentioned at the start of this section, we only need the 
<code>KEY 1</code> value and the <code>Location/Region</code> 
value to use <code>Azure TTS</code> in code. The value of 
<code>KEY 1</code> is assigned to the environment variable 
<code>SPEECH_KEY</code>, and the value of <code>Location/Region</code> 
is assigned to the <code>SPEECH_REGION</code> environment variable.

<a id="run-the-python-example"></a>
❸ We are now essentially ready to run the official Python example. 
The example code can be found on the following official tutorial page: 
<a href="https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-text-to-speech?tabs=windows%2Cterminal&pivots=programming-language-python" 
title="Quickstart: Convert text to speech" target="_blank">Quickstart: Convert text to speech</a>.

<a id="run-install-python-sdk"></a>
⓵ We need to install the “Microsoft Cognitive Services Speech SDK for Python”, 
also known as 
<a href="https://pypi.org/project/azure-cognitiveservices-speech/" 
title="Microsoft Cognitive Services Speech SDK for Python" 
target="_blank">azure-cognitiveservices-speech</a>, onto the active virtual environment, 
<code>venv</code>. Please use the following command: 

```
▶️Windows 10: (venv) F:\pydev>venv\Scripts\pip.exe install azure-cognitiveservices-speech
▶️Ubuntu 22.10: (venv) behai@hp-pavilion-15:~/pydev$ ./venv/bin/pip install azure-cognitiveservices-speech
```

<a id="run-set-env-variables"></a>
⓶ We need to set the <code>SPEECH_KEY</code> and the <code>SPEECH_REGION</code> 
environment variables for each console session, <a id="tts-api-key-region">as recapped 
above</a>: 

```
▶️Windows 10: (venv) F:\pydev>set SPEECH_KEY=&lt;KEY 1 value&gt;
▶️Ubuntu 22.10: (venv) behai@hp-pavilion-15:~/pydev$ export SPEECH_KEY="&lt;KEY 1 value&gt;"
```

```
▶️Windows 10: (venv) F:\pydev>set SPEECH_REGION=&lt;Location/Region value&gt;
▶️Ubuntu 22.10: (venv) behai@hp-pavilion-15:~/pydev$ export SPEECH_REGION="&lt;Location/Region value&gt;"
```

To verify that the environment variables have been set, use the following commands:

```
▶️Windows 10: (venv) F:\pydev>echo %SPEECH_KEY%
▶️Ubuntu 22.10: (venv) behai@hp-pavilion-15:~/pydev$ printenv SPEECH_KEY
```

```
▶️Windows 10: (venv) F:\pydev>echo %SPEECH_REGION%
▶️Ubuntu 22.10: (venv) behai@hp-pavilion-15:~/pydev$ printenv SPEECH_REGION
```

<a id="run-copy-example"></a>
⓷ Copy the example code into the file named <code>azure_speech_synthesis.py</code>. 
I am listing the code as it is:

```
Content of azure_speech_synthesis.py:
```

{% highlight python linenos %}
import os
import azure.cognitiveservices.speech as speechsdk

# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# The neural multilingual voice can speak different languages based on the input text.
speech_config.speech_synthesis_voice_name='en-US-AvaMultilingualNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# Get text from the console and synthesize to the default speaker.
print("Enter some text that you want to speak >")
text = input()

speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))
elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = speech_synthesis_result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
{% endhighlight %}

<a id="run-example-as-is"></a>
⓸ Let’s run the example as it is. The command to run is as follows:

```
▶️Windows 10: (venv) F:\pydev>venv\Scripts\python.exe azure_speech_synthesis.py
```

Since the voice in the example code is <code>en-US-AvaMultilingualNeural</code>,
enter some English text, for example, 
<strong><em>The rain in Spain stays mainly in the plain.</em></strong> 
Then hit the <code>Enter</code> key. We should hear the text being 
read aloud through the machine’s default speaker. The console response 
should look like the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-7 %}
<br/>

<a id="run-example-audio-to-file"></a>
⓹ Let’s save the audio into a file. For <strong>Line 6</strong>, we 
replace the <code>use_default_speaker=True</code> parameter with 
<code>filename='azure_speech_synthesis.mp3'</code>:

<figure class="highlight"><pre><code class="language-python" data-lang="python"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">5
6
7
8
9
10
11
</pre></td><td class="code"><pre><span class="n">speech_config</span> <span class="o">=</span> <span class="n">speechsdk</span><span class="p">.</span><span class="n">SpeechConfig</span><span class="p">(</span><span class="n">subscription</span><span class="o">=</span><span class="n">os</span><span class="p">.</span><span class="n">environ</span><span class="p">.</span><span class="n">get</span><span class="p">(</span><span class="s">'SPEECH_KEY'</span><span class="p">),</span> <span class="n">region</span><span class="o">=</span><span class="n">os</span><span class="p">.</span><span class="n">environ</span><span class="p">.</span><span class="n">get</span><span class="p">(</span><span class="s">'SPEECH_REGION'</span><span class="p">))</span>
<span class="n hl">audio_config</span> <span class="o hl">=</span> <span class="n hl">speechsdk</span><span class="p hl">.</span><span class="n hl">audio</span><span class="p hl">.</span><span class="n hl">AudioOutputConfig</span><span class="p hl">(</span><span class="n hl">filename</span><span class="o hl">=</span><span class="s hl">'azure_speech_synthesis.mp3'</span><span class="p hl">)</span>

<span class="c1"># The neural multilingual voice can speak different languages based on the input text.
</span><span class="n">speech_config</span><span class="p">.</span><span class="n">speech_synthesis_voice_name</span><span class="o">=</span><span class="s">'en-US-AvaMultilingualNeural'</span>

<span class="n">speech_synthesizer</span> <span class="o">=</span> <span class="n">speechsdk</span><span class="p">.</span><span class="n">SpeechSynthesizer</span><span class="p">(</span><span class="n">speech_config</span><span class="o">=</span><span class="n">speech_config</span><span class="p">,</span> <span class="n">audio_config</span><span class="o">=</span><span class="n">audio_config</span><span class="p">)</span>
</pre></td></tr></tbody></table></code></pre></figure>

Run it <a href="#run-example-as-is">as described above</a>. 
After the program finishes running, we should have the audio file 
<code>azure_speech_synthesis.mp3</code> in the same folder as the Python source file.

<a id="run-example-audio-viet"></a>
⓺ Finally, let’s try a language other than English. All we have to do is replace 
<code>en-US-AvaMultilingualNeural</code> with an available voice name. 
The official page 
<a href="https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts" 
title="Language and voice support for the Speech service" 
target="_blank">Language and voice support for the Speech service</a>
lists all available languages and voices. The data we are interested in is under the column 
<code>Text to speech voices</code>. For example, for Vietnamese, we have two voices 
<code>vi-VN-HoaiMyNeural</code> and <code>vi-VN-NamMinhNeural</code>.

For <strong>Line 9</strong>, let’s replace 
<code>en-US-AvaMultilingualNeural</code> with <code>vi-VN-HoaiMyNeural</code>:

<figure class="highlight"><pre><code class="language-python" data-lang="python"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">6
7
8
9
10
11
</pre></td><td class="code"><pre><span class="n">audio_config</span> <span class="o">=</span> <span class="n">speechsdk</span><span class="p">.</span><span class="n">audio</span><span class="p">.</span><span class="n">AudioOutputConfig</span><span class="p">(</span><span class="n">filename</span><span class="o">=</span><span class="s">'azure_speech_synthesis.mp3'</span><span class="p">)</span>

<span class="c1"># The neural multilingual voice can speak different languages based on the input text.
</span><span class="n hl">speech_config</span><span class="p hl">.</span><span class="n hl">speech_synthesis_voice_name</span><span class="o hl">=</span><span class="s hl">'vi-VN-HoaiMyNeural'</span>

<span class="n">speech_synthesizer</span> <span class="o">=</span> <span class="n">speechsdk</span><span class="p">.</span><span class="n">SpeechSynthesizer</span><span class="p">(</span><span class="n">speech_config</span><span class="o">=</span><span class="n">speech_config</span><span class="p">,</span> <span class="n">audio_config</span><span class="o">=</span><span class="n">audio_config</span><span class="p">)</span>
</pre></td></tr></tbody></table></code></pre></figure>

Run it <a href="#run-example-as-is">as before</a>. But this time, we have to input 
Vietnamese text. For example, <strong><em>Rải rác biên cương mồ viễn xứ</em></strong>.

```
▶️Ubuntu 22.10: (venv) behai@hp-pavilion-15:~/pydev$ ./venv/bin/python azure_speech_synthesis.py
```

The output is as illustrated in the screenshots below: 

{% include image-gallery.html list=page.gallery-image-list-8 %}
<br/>

<a id="official-documenation"></a>
❹ <code>Azure TTS</code> has an extensive set of documentation. I have only read or skimmed through a few. Here is my list:

<ol>
<li style="margin-top:10px;">
<a href="https://azure.microsoft.com/en-gb/get-started/welcome-to-azure/"
title="You’re ready to start with Azure" target="_blank">You’re ready to start with Azure</a>.
</li>

<li style="margin-top:10px;">
<a href="https://learn.microsoft.com/en-us/azure/ai-services/speech-service/rest-text-to-speech?tabs=streaming" 
title="Text to speech REST API" target="_blank">Text to speech REST API</a>.
</li>

<li style="margin-top:10px;">
<a href="https://learn.microsoft.com/en-us/azure/ai-services/speech-service/index-text-to-speech" 
title="Text to speech documentation" 
target="_blank">Text to speech documentation</a>.
</li>

<li style="margin-top:10px;">
<a href="https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-text-to-speech?tabs=windows%2Cterminal&pivots=programming-language-python" 
title="Quickstart: Convert text to speech | Python" 
target="_blank">Quickstart: Convert text to speech | Python</a>: 
We have listed this page in <a href="#run-the-python-example">this section</a>.
</li>
</ol>	

❺ The primary reason for me to try <code>Azure TTS</code> is that it offers two 
Southern Vietnamese voices, <a href="#run-example-audio-viet">as described</a>.
The <a href="https://cloud.google.com/text-to-speech/docs/reference/rest" 
title="Google Cloud Text-to-Speech API" target="_blank">Google Cloud Text-to-Speech API</a> 
also supports Vietnamese, but all the available voices are Northern.

I found the process of creating projects a bit confusing. 
However, we <a href="#api-key-region-code">managed to do it</a>. 
This post serves as a good reference document for me. I hope that 
exploring other Azure AI services will be a bit easier in the future.

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
<a href="https://1000logos.net/wp-content/uploads/2020/06/Microsoft_Azure_logo_PNG13.png" target="_blank">https://1000logos.net/wp-content/uploads/2020/06/Microsoft_Azure_logo_PNG13.png</a>
</li>
<li>
<a href="https://seeklogo.com/vector-logo/332789/python" target="_blank">https://seeklogo.com/vector-logo/332789/python</a>
</li>
</ul>
