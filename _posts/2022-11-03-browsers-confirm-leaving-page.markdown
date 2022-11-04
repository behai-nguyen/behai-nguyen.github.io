---
layout: post
title: "Web browsers: confirm leaving page when there is modified data."
description: Web sites such as Facebook implements a confirmation to leave the current page when there is unsaved data. This is not at all hard to do, but it did take me some experimentations to find out what works. I'm discussing my findings in this post.
tags:
- Web Browser
- Confirm
- Leave
- Page
- Unload

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list:
    - "https://behainguyen.files.wordpress.com/2022/11/043-firefox-confirmation.png"
    - "https://behainguyen.files.wordpress.com/2022/11/043-opera-confirmation.png"
    - "https://behainguyen.files.wordpress.com/2022/11/043-chrome-confirmation.png"
    - "https://behainguyen.files.wordpress.com/2022/11/043-edge-confirmation.png"
---

<em><span style="color:rgb(17, 17, 17);">Web sites such as Facebook implements a confirmation to leave the current page when there is unsaved data. This is not at all hard to do, but it did take me some experimentations to find out what works. I'm discussing my findings in this post.</span></em>

| ![043-feature-image.png](https://behainguyen.files.wordpress.com/2022/11/043-feature-image.png) |
|:--:|
| <em><span style="color:rgb(17, 17, 17);">Web browsers: confirm leaving page when there is modified data.</span></em> |

I'm using the 
<a href="https://jinja.palletsprojects.com/en/3.1.x/" title="Jinja templating engine" target="_blank">Jinja templating engine</a>
to generate HTML pages. For client-side, I'm using
<a href="https://jquery.com/" title="JQuery" target="_blank">JQuery</a>.
I'm mentioning the use of the 
<a href="https://jinja.palletsprojects.com/en/3.1.x/" title="Jinja templating engine" target="_blank">Jinja templating engine</a>
is for the shake of completeness, whatever methods employed to generate dynamic HTML 
are irrelevant, since what we're discussing is purely client-side.

To implement this leave page confirmation, we need to handle the 
<a href="https://developer.mozilla.org/en-US/docs/Web/API/Window/beforeunload_event"
title="Window: beforeunload event" target="_blank">Window: beforeunload event</a>.
I'd like to do it for all pages 
across the site, so I implement it in the base template:

```
File base_template.html
```

```html
<!doctype html>
<html lang="en" class="h-100">
<head>
    ...
	<script src="http://localhost/work/jquery/js/jquery-3.6.0.min.js"></script>
    ...

	<script>
        // Individual pages must set and reset this during their operations.	
        let dataChanged = false;
		
        const setDataChanged = () => dataChanged = true;
        const resetDataChanged = () => dataChanged = false;
		
		$( document ).ready( function(event) {

            $( window ).on( 'beforeunload', function( event ) {
				if ( dataChanged ) 
				    // return confirm( 'There are unsaved data. Please confirm.' );
				    // return false;
				    // return true;
					return null;
			});

		});
	</script>
</head>

<body class="d-flex flex-column h-100">
    {% raw %}
	{% block content %}
    <!-- Content of specific individual pages go here. -->
	{% endblock %}
	{% endraw %}
</body>
</html>
```

The only thing 
<span class="keyword">
“Jinja”</span> about this page is the following block:

```
{% raw %}
	{% block content %}
    <!-- Content of specific individual pages go here. -->
	{% endblock %}
{% endraw %}
```

Basically, at runtime the processing engine replaces this block
with a requested page to make a complete and valid HTML page
to return to the requesting client.

The codes for the 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
beforeunload</span> event is simple: if variable
<span class="keyword">
dataChanged</span> is 
<span class="keyword">
true</span>, then do a 
<span class="keyword">
return null</span>, otherwise nothing.

I have three ( 3 )
<span class="keyword">
return</span> statements commented out: they have the same effect as
<span class="keyword">
return null</span>.

It's the responsibility of the pages to set and reset 
<span class="keyword">
dataChanged</span> by calling 
<span class="keyword">
setDataChanged()</span> and 
<span class="keyword">
resetDataChanged()</span> respectively. 
<span style="color:blue;">
Please note that when the page is first loaded,
<span class="keyword">
dataChanged</span> is initialised to 
<span class="keyword">
false</span></span>.

The general structure 
of individual pages that go into 
<span class="keyword">
base_template.html</span>'s block content:

```
File a_specific_page.html
```

```html
{% raw %}{% extends "page_template.html" %}{% endraw %}

{% raw %}{% block content %}{% endraw %}
<script>
	function bindDataChange() {
		$( '.selector-input, input[type="checkbox"]' ).on( 'change', function(event) {
			...
			setDataChanged();

			event.preventDefault();
		});
	};

	function bindSave() {
		function savedSuccessful( data ) {
			resetDataChanged();
			...
		};

		$( '#saveBtn' ).on( 'click', function( even ) {

            if ( !$('#somethingFrm').parsley().validate() ) return false;

            // Send data to server using AJAX. Response is JSON status.
			saveData( '/save-something/', '{{ csrf_token() }}',
			    $( '#somethingFrm' ).serialize(), savedSuccessful );

			event.preventDefault();
		});
	};

	$( document ).ready( function() {
	    ...
        bindDataChange();
        bindSave();
        ...
	});
</script>

<div class="d-flex row justify-content-center h-100">
    ...
</div>
{% raw %}{% endblock %}{% endraw %}
```

<span style="color:blue;">
Note where 
<span class="keyword">
setDataChanged()</span> and 
<span class="keyword">
resetDataChanged()</span> get called.
</span> Please also recall that when the page is first loaded,
<span class="keyword">
dataChanged</span> is initialised to 
<span class="keyword">
false</span>.

This 
<span class="keyword">
a_specific_page.html</span> saves data via 
<span class="keyword">
AJAX</span> call, the response is a 
<span class="keyword">
JSON</span> status, which indicates the outcome of the request: the
page does not get reloaded during this operation.

In short, whenever users do anything on the screen which requires
data to be persisted, 
<span class="keyword">
setDataChanged()</span> must be called. And after data has been
successfully saved, 
<span class="keyword">
resetDataChanged()</span> must get called.

<h2>What about form submission?</h2>

Form submission means leaving the current page, 
the 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
beforeunload</span> event could potentially be triggered.
The page segment below shows how I solve this issue:

```
File a_form_submit_page.html
```

```html
{% raw %}{% extends "base_form_template.html" %}{% endraw %}

{% raw %}{% block content %}{% endraw %}
<script>
	function bindDataChange() {
	    $( 'selectors' ).on( 'change', function( event ) {
			...
			setDataChanged();
		});
    };

	function bindUpdateBtn() {
        $( '#updateBtn' ).on( 'click', (event) => {
			form = $( '#someFrm' );
			...
			//Don't trigger page leaving event.
			resetDataChanged();
			
			form.submit()

			event.preventDefault();
		});
	};
	
	$(document).ready( () => {
		bindDataChange();
	    bindUpdateBtn();
	});	
</script>

<div class="d-flex">
    <form method="POST" action="{{ request.path }}" id="someFrm">
        {{ form.csrf_token }}
        ...
        <button type="submit" id="updateBtn" class="btn btn-primary btn-sm" disabled="disabled">Update</button>
        ...
    </form>
</div>

{% raw %}{% endblock %}{% endraw %}
```

I must submit forms manually, in this case via
<span class="keyword">
function bindUpdateBtn()</span>. This gives me a chance
to call 
<span class="keyword">
resetDataChanged()</span> -- even though the data has not been saved --
before unloading the page so the event will not be triggered.

If you have noticed, each page has two ( 2 )
<span class="keyword">
$(document).ready()</span> declarations, browsers seem to allow this,
so far I don't have any complaint. But I am not sure if this is a
good implementation?

I have tested this approach with the following browsers:

<ul>
<li style="margin-top:5px;">FireFox -- Version: 106.0.3 (64-bit)</li>
<li style="margin-top:10px;">Opera -- Version: 92.0.4561.21, System: Windows 10 64-bit</li>
<li style="margin-top:10px;">Chrome -- Version 106.0.5249.119 (Official Build) (64-bit)</li>
<li style="margin-top:10px;">Edge -- Version 106.0.1370.52 (Official build) (64-bit)</li>
</ul>

{% include image-gallery.html list=page.gallery-image-list %}

<span style="color:blue;">
I've also tested it with browsers' tab closing, and it also works.
</span>

I'm not at all sure if this is the best implementation or not, but
it seems to work for me. If problems arise later on, I'll do an update on it.
Thank you for reading. I do hope you find this post useful. Stay safe as
always.