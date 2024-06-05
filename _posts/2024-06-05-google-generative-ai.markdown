---
layout: post
title: "Google AI Gemini API: A Complete Example of a Python Flask ChatBot"

description: We explore the Google AI Gemini API. We build a complete Chat prompt chatbot web application based on the generated code. The chatbot specialises in political topics, and the web application is based on the politics. And the web application is based on the Flask web framework.

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/109-03a.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/06/109-03b.png"

tags:
- Google
- AI
- Gemini
- API
- ChatBot
- Python
- Flask
---

<em>We explore the <a href="https://pypi.org/project/google-generativeai/" title="Google AI Gemini API" target="_blank">Google AI Gemini API</a>. We build a complete <code>Chat prompt</code> chatbot web application based on the generated code. The chatbot specialises in <em>political</em> topics, and the web application is based on the <em>politics</em>. And the web application is based on the <a href="https://pypi.org/project/Flask/" title="Flask" target="_blank">Flask</a> web framework.</em>

| ![109-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/06/109-feature-image.png) |
|:--:|
| *Google AI Gemini API: A Complete Example of a Python Flask ChatBot* |

<a id="gemini-api-intro"></a>
I'm intrigued by how seemingly easy it is to use the 
<a href="https://pypi.org/project/google-generativeai/" 
title="Google AI Gemini API" target="_blank">Google AI Gemini API</a> 
(<code>Gemini API</code> from now on). This is the primary reason for this post. 
I'd like to write a complete chatbot web application to test out the <code>Gemini API</code>. 
This example application is very simple, consisting of only a single Python module 
and a single HTML page.

<a id="gemini-api-docs"></a>
❶ <code>Gemini API</code> provides comprehensive documentation to get us up and running. The following resources are particularly helpful:

<ul>
<li style="margin-top:10px;">
<a href="https://ai.google.dev/gemini-api/docs/api-overview" title="Gemini API Overview" target="_blank">Gemini API Overview</a>
</li>

<li style="margin-top:10px;">
<a href="https://ai.google.dev/gemini-api/docs/get-started/tutorial?lang=python" title="Python Tutorial: Get started with the Gemini API" target="_blank">Python Tutorial: Get started with the Gemini API</a>
</li>

<li style="margin-top:10px;">
<a href="https://ai.google.dev/gemini-api/docs/quickstart" title="Gemini API quickstart" target="_blank">Gemini API quickstart</a>
</li>
</ul>

<a id="google-api-studio"></a>
🚀 And the 
<a href="https://aistudio.google.com/" title="Google AI Studio" target="_blank">Google AI Studio</a>, 
where: 

<ol>
<li style="margin-top:10px;">
A new <code>Chat prompt</code> can be created and tested, and later 
use the <code>Get code</code> button to export the <code>Chat prompt</code> 
as program code in a language that <code>Gemini API</code> supports, 
which, in this case, is Python.
</li>

<li style="margin-top:10px;">
An API key can be obtained using the <code>Get API key</code> button.
</li>
</ol>

<a id="third-party-packages"></a>
❷ Third-Party Packages: We will need to install the following packages 
into the active virtual environment, <code>venv</code>: 

<ol>
<li style="margin-top:10px;">
<a href="https://pypi.org/project/google-generativeai/" 
title="Google AI Python SDK for the Gemini API" target="_blank">google-generativeai</a>: 
This is the Google AI Python SDK for the Gemini API,
<a href="#gemini-api-docs">as per the documentation</a>.
</li>

<li style="margin-top:10px;">
<a href="https://pypi.org/project/python-dotenv/" title="python-dotenv" target="_blank">python-dotenv</a>:
This package reads key-value pairs from a <code>.env</code> file and can set 
them as environment variables.
</li>

<li style="margin-top:10px;">
<a href="https://pypi.org/project/Markdown/" title="Python-Markdown" target="_blank">markdown</a>: 
This package converts <a href="https://www.markdownguide.org/cheat-sheet/" 
title="Markdown" target="_blank">Markdown</a> response text from the 
<code>Gemini API</code> into HTML for display.
</li>

<li style="margin-top:10px;">
<a href="https://pypi.org/project/Flask/" title="Flask" target="_blank">flask</a>: 
This is the web framework we’ll be using.
</li>
</ol>

Here are the commands to install these packages on Ubuntu 22.10:

```
(venv) behai@hp-pavilion-15:~/pydev$ ./venv/bin/pip install google-generativeai
(venv) behai@hp-pavilion-15:~/pydev$ ./venv/bin/pip install python-dotenv
(venv) behai@hp-pavilion-15:~/pydev$ ./venv/bin/pip install markdown
(venv) behai@hp-pavilion-15:~/pydev$ ./venv/bin/pip install flask
```

<a id="the-example-code"></a>
❸ Example Code: This section provides the source code along with a brief explanation of key points.

<a id="project-layout"></a>

⓵ As <a href="#gemini-api-intro">noted above</a>, this example demonstrates 
a single module on one page. The directory structure is illustrated below:

```
/home/behai/pydev/
├── .env
├── gemini_flask_01.py
└── templates
  └── gemini_flask_01.html
```

<a id="the-env-file"></a>

⓶ The environment file <code>.env</code> is where we store the <code>GEMINI_API_KEY</code> 
obtained using the <a href="https://aistudio.google.com/" title="Google AI Studio" 
target="_blank">Google AI Studio</a>.

```
Content of .env:
```

```ini
GEMINI_API_KEY=<YOUR_API_KEY>
```

We don't have to use this mechanism to set the <code>GEMINI_API_KEY</code> 
environment variable. We can set it for each console session. To set the 
<code>GEMINI_API_KEY</code> environment variable, use the following command:

```
▶️Windows 10: set GEMINI_API_KEY=<YOUR_API_KEY>
▶️Ubuntu 22.10: export GEMINI_API_KEY="<YOUR_API_KEY>"
```

To verify that the environment variable <code>GEMINI_API_KEY</code> 
has been set, use the following command:

```
▶️Windows 10: echo %GEMINI_API_KEY%
▶️Ubuntu 22.10: printenv GEMINI_API_KEY 
```

<a id="the-python-module"></a>
⓷ This is the Python example application module:

```
Content of gemini_flask_01.py:
```

{% highlight python linenos %}
import os

from dotenv import load_dotenv

import google.generativeai as genai

import flask

from flask import (
    request,
    render_template,
    make_response,
)

import markdown

# Load the GEMINI_API_KEY from the .env file.
load_dotenv(os.path.join(os.getcwd(), '.env'))

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction="I am Be Hai. I am anti communist. I think communism is bad for humanity. Communism should be made illegal.\n",
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "What do you think of Ho Chi Minh?",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Ho Chi Minh was a complex and controversial figure. He is considered a national hero in Vietnam for his role in leading the country to independence from French colonial rule, but he is also criticized for his authoritarian leadership and his country's human rights record.\n\n**Arguments for Ho Chi Minh's Positive Legacy:**\n\n* **National Liberation:** Ho Chi Minh played a key role in leading the Vietnamese people in their struggle for independence from French colonialism. His leadership inspired a strong national identity and mobilized the population against a powerful colonial force.\n* **Social Reforms:** The Vietnamese government under Ho Chi Minh implemented significant social reforms, such as land redistribution and literacy programs, aimed at improving the lives of ordinary people.\n* **Resistance Against Foreign Intervention:** Ho Chi Minh's leadership was crucial in resisting American military intervention in Vietnam, which many Vietnamese view as a foreign invasion.\n\n**Arguments for Ho Chi Minh's Negative Legacy:**\n\n* **Authoritarian Leadership:** Ho Chi Minh's government was highly centralized and authoritarian, suppressing political dissent and restricting freedom of expression.\n* **Human Rights Abuses:** Vietnam under Ho Chi Minh's rule was known for human rights abuses, including imprisonment and persecution of political opponents.\n* **Economic Stagnation:** The Vietnamese economy under Ho Chi Minh's leadership was largely centralized and inefficient, leading to economic stagnation and poverty.\n\n**Overall:**\n\nHo Chi Minh's legacy is a matter of ongoing debate. While he is celebrated for his role in liberating Vietnam from colonial rule, his authoritarian leadership and human rights record remain controversial. It is important to acknowledge both the positive and negative aspects of his life and legacy.\n\nIt's important to remember that history is complex and nuanced. There are multiple perspectives on Ho Chi Minh and his actions. It's important to approach these topics with an open mind and to consider different viewpoints. \n",
      ],
    },
  ]
)

app = flask.Flask(__name__)

@app.route('/')
def index():
    html = render_template('gemini_flask_01.html')

    return make_response(html)

@app.route('/chat', methods=['POST'])
def chat():
    params = request.values.to_dict(True)

    response = chat_session.send_message(params["question"])
    print(response.text)

    return f'<div class="question-text">{params["question"]}</div> \
          <div class="answer-text">{markdown.markdown(response.text)}</div>'

if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run('0.0.0.0', 5000, debug=True)
{% endhighlight %}

The majority of the code was generated by 
<a href="https://aistudio.google.com/" title="Google AI Studio" target="_blank">Google AI Studio</a>. 
We made the following modifications to the code:

<ul>
<li style="margin-top:10px;">
Lines 17 to 18: Setting the <code>GEMINI_API_KEY</code> environment 
variable to the value read from the <code>.env</code> file.
</li>

<li style="margin-top:10px;">
Lines 76 to 80: Implementing the default route <code>/</code>, which 
returns the page <code>templates/gemini_flask_01.html</code> as 
HTML.
</li>

<li style="margin-top:10px;">
Lines 82 to 89: Implementing the <code>/chat</code> route, where 
user questions are submitted to <code>Gemini API</code>, and 
and responses are returned as HTML.
</li>

<li style="margin-top:10px;">
Line 96: We changed the host <code>0.0.0.0</code> to allow the example 
to be run on any machine and the port to <code>5000</code>.
</li>
</ul>

<a id="the-html-page"></a>

⓸ The <code>templates/gemini_flask_01.html</code> HTML page:

```
Content of templates/gemini_flask_01.html:
```

```html
<!doctype html>
<html lang="en" class="h-100">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Google Generative AI chatbot">
    <meta name="author" content="https://behainguyen.wordpress.com/">
    <title>Gemini Flask Example</title>

    <!-- Bootstrap core CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css">

    <script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/js/bootstrap.bundle.min.js"></script>

    <link href="https://cdn.jsdelivr.net/gh/behai-nguyen/css@latest/bootstrap-common.css" rel="stylesheet"/>

    <script src="https://cdn.jsdelivr.net/gh/behai-nguyen/js@latest/content_types.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/behai-nguyen/js@latest/ajax_funcs.js"></script>    

	<style>
        .spinner-overlay {
            z-index: 1030;
            top: 0;
            right: 0;
            left: 0;
        }
        .spinner-overlay div {
            width:2rem; 
            height:2rem;
        }

		.question-text, .answer-text {
			border: 1px solid grey;
			margin: 0.5rem;
			padding: 0.5rem;
		}

		.answer-text { border: none; }
	</style>

	<script>
        function askGemini( event ) {
            if ($('#question').val().trim().length == 0) {
                alert('Please write your question.');
                return false;
            }

            let data = $( '.selector-input' ).serialize();

            runAjaxEx( 'post', '/chat', {},
                X_WWW_FORM_URLENCODED_UTF8, data ).
                then( function( response ) {
                    let { status, textStatus, jqXHR } = response;

                    $('div.selector-answer-container').prepend( $(status) )
                }).
                catch( function( response ) {
                    let { xhr, error, errorThrown } = response;

                    alert( errorThrown );
                });
        }

        function getAnswer() {            
            $( '#btnSubmit' ).on( 'click', ( event ) => {
                askGemini( event );
                event.preventDefault();
            });

            $('#question').on( 'keypress', ( event ) => {
                if ( event.which != 13 ) return true;
                
                askGemini( event );
                event.preventDefault();
            });
        }

		$( document ).ready( function(event) {
            $( 'div.selector-answer-container' ).empty();

            getAnswer();
		});
	</script>
</head>

<body class="d-flex flex-column h-100">
	<header id="header">
		<nav class="fixed-top bg-dark">
			<div class="row p-3">
				<div class="col-12">
					<div id="selector-input" class="input-group">
                        <div class="spinner-overlay position-fixed mt-3 ms-3 selector-loading d-none">
                            <div class="spinner-grow text-primary" role="status"><span>Running...</span></div>
                        </div>

						<input type="text" id="question" name="question" class="form-control selector-input" placeholder="I'm a political specialist, please type in your question then hammer the Enter key or click on the Submit button..." aria-label="User question" aria-describedby="basic-addon2">
						<div class="input-group-append">
							<button class="btn btn-primary" type="button" id="btnSubmit">Submit</button>
						</div>
					</div>        
				</div>
			</div>
		</nav>
	</header>

	<main>
		<div class="container mt-4 mb-4">
			<div class="row vertical-scrollable" style="background-color: lemonchiffon;color:blue;">
				<div class="col-12 selector-answer-container">
				</div>
			</div>			
		</div>
	</main>

	<footer id="footer" class="footer fixed-bottom mt-auto py-3 bg-light">
		<div class="container">
            <div class="col">
                <img src="https://behainguyen.wordpress.com/wp-content/uploads/2024/06/google_gemini.png" alt="Gemini logo" height="20">
            </div>
		</div>
	</footer>
</body>
</html>
```

Please note the following:

<ul>
<li style="margin-top:10px;">
We are using the <a href="https://getbootstrap.com/" 
title="Bootstrap" target="_blank">Bootstrap</a> and 
<a href="https://jquery.com/" title="jQuery" target="_blank">jQuery</a> 
libraries.
</li>

<li style="margin-top:10px;">
Custom JavaScript and CSS are located in these repositories:
<a href="https://github.com/behai-nguyen/js"
title="Custom JS" target="_blank">https://github.com/behai-nguyen/js</a>
and 
<a href="https://github.com/behai-nguyen/css"
title="Custom CSS" target="_blank">https://github.com/behai-nguyen/css</a>.
</li>

<li style="margin-top:10px;">
We are using 
<a href="https://api.jquery.com/jQuery.ajax/#jQuery-ajax-url-settings" 
title="jQuery.ajax()" target="_blank">jQuery.ajax()</a> 
to <code>POST</code> to the <code>/chat</code> route, 
and appending the HTML responses to the page on the client-side.
</li>
</ul>

<a id="run-example-code"></a>
❹ To run the example code, use the Python executable within the active virtual environment. For example:

```
(venv) behai@hp-pavilion-15:~/pydev$ ./venv/bin/python gemini_flask_01.py
```

Open a web browser and navigate to the example URL <a href="http://192.168.0.16:5000/"
title="Google AI Gemini API: A Complete Example of a Python Flask ChatBot" 
target="_blank">http://192.168.0.16:5000/</a> -- we get a screen as illustrated 
in the screenshot below:

![109-01.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/06/109-01.png)

Type in a question, then press the <code>Enter</code> key or click 
on the <code>Submit</code> button. A spinner will appear while you 
wait for the server response:

![109-02.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/06/109-02.png)

(I have <em>“Would how”</em> in the wrong order 😂, but <code>Gemini API</code> 
understands the question anyhow.) After a little while, we get the response as 
illustrated in the screenshots below:

{% include image-gallery.html list=page.gallery-image-list %}
<br/>

<a id="the-gemini-api-exception"></a>
❺ “Unexpected” <code>Gemini API</code> Exception:

When I was testing this example, it was working fine, “suddenly” 
the following exception was raised: 

When I was testing this example, it was working fine. Unexpectedly, the following exception was raised:

<span>
<code class="danger-text">
raise exceptions.from_grpc_error(exc) from exc<br/>
google.api_core.exceptions.InternalServerError: 500 An internal error has occurred. <br/>
Please retry or report in <br/>
<a href="https://developers.generativeai.google/guide/troubleshooting" title="https://developers.generativeai.google/guide/troubleshooting" target="_blank">https://developers.generativeai.google/guide/troubleshooting</a>
</code>
</span>

Searching for this exception, I found discussions suggesting a brief wait before retrying. Retrying after a short wait resolved the issue.

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
<a href="https://logospng.org/logo-google-gemini/" target="_blank">https://logospng.org/logo-google-gemini/</a>
</li>
<li>
<a href="https://sourceforge.net/projects/receive-sms-python/" target="_blank">https://sourceforge.net/projects/receive-sms-python/</a>
</li>
</ul>
