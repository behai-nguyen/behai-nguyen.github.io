---
layout: bootstrap-livedemo
permalink: /jquery-bhdropdownselect/

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
    - "https://cdn.jsdelivr.net/gh/behai-nguyen/jquery-bhdropdownselect@main/src/bhDropdownSelect.css"

custom-javascript-list:
    - "https://code.jquery.com/jquery-3.6.0.min.js"
    - "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
    - "https://cdn.jsdelivr.net/gh/behai-nguyen/jquery-bhdropdownselect@main/src/bhDropdownSelect.js"
    - "https://cdn.jsdelivr.net/gh/behai-nguyen/jquery-bhdropdownselect@main/example/bhDropdownSelectDemoLists.js"

---

<body class="d-flex flex-column h-100">
	<style>
		/* User-defined theme: example02. */
		.dropdown-select.theme-example02 .modal-header { background-color: #adbcce; }

		.dropdown-select.theme-example02 .modal-header input[type="text"] {
			background-color: #d5dce5;
		}

		.dropdown-select.theme-example02 .modal-body { background-color: #879ebc; }

		.dropdown-select.theme-example02 .modal-body .container .row:nth-child( odd ) {
			background-color: #9fc5f7;
		}

		.dropdown-select.theme-example02 .modal-body .container .row:nth-child( even ) {
			background-color: #3b87ec;
		}

		.dropdown-select.theme-example02 .item-highlight {
			background-color: #c1d8f5;
			font-style: italic;
			font-weight: bold;
		}

		.dropdown-select.theme-example02 .item-normal {
			font-style: normal;
			font-weight: normal;
		}
	</style>

    <script>
	    function selectLanguage( params ) {
		    $( '#selectedLanguage' ).val( `${params[0]}, ${params[1]}` );
		};

		$( document ).ready( function() {
		    // 01.

			$( '#btnLanguage' ).bhDropdownSelect({
			    source: AVAILABLE_LANGUAGES,
				selectCallback: selectLanguage,
				theme: 'safe'
			}).addClass( 'fw-bold' );

			$( '#btnTropicalFruits' ).bhDropdownSelect({
			    source: TROPICAL_FRUITS,

				selectCallback: function( params ) {
				    $( '#selectedFruit' ).val( `${params[0]}, ${params[1]}` );
				},

                theme: 'eyesore'
			});

			$( '#btnNoSource' ).bhDropdownSelect({
			    source: null
			});

            // 02.

			$( '#btnTropicalFruits2' ).bhDropdownSelect({
			    source: TROPICAL_FRUITS,

				selectCallback: function( params ) {
				    $( '#selectedFruit2' ).val( `${params[0]}, ${params[1]}` );
				},

                theme: 'example02'
			});
        });

    </script>

	{%- include bootstrap-livedemo-header.html -%}

    <main>
		<div class="container">
		    <div class="demo-container">
<h1>jQuery plugin: bhDropdownSelect</h1>

<p>
bhDropdownSelect implements a multi-column drop-down select
using Bootstrap v5.1.3 dialog and jQuery v3.6.0.
</p>

<p>
This v1.0.0 version implements a two-column grid in a fixed
size dialog.
</p>

<p>
There is still much to be done. For example, among others,
smart positioning is the first priority, currently it is just
assumed that there is optimal space available for this plugin
to look its best.
</p>

<p>
GitHub address: <a href="https://github.com/behai-nguyen/jquery-bhdropdownselect" title="jQuery plugin: bhDropdownSelect" target="_blank">https://github.com/behai-nguyen/jquery-bhdropdownselect</a>.
</p>

<p>
Let's look at how it works. Full example codes are also included in the above
GitHub repo.
</p>

				<div class="row g-3 align-items-center my-3">
					<div class="col">
						<h3>jQuery plugin bhDropdownSelect usage Example 01.</h3>
					</div>
				</div>

				<div class="row g-3 align-items-center">
					<div class="col">
						<span class="fw-bold">“Select a Language”</span> demonstrates default
						behaviours.

						<ul>
							<li>
								Please note that option “theme” ( safe ) could be omitted as it
								is the default theme.
							</li>

							<li>
								Changing the button <span class="fw-bold">“Select a Language”</span>
								label text to <span class="fw-bold">bold</span> programmatically to
								demonstrate that this plugin is chainable: it behaves
								correctly according to jQuery plugin guidelines.
							</li>
						</ul>
					</div>
				</div>

				<div class="row g-3 align-items-center mb-4">
					<div class="col-3">
						<button type="button" id="btnLanguage" class="btn btn-primary">Select a Language</button>
					</div>

					<div class="col-9">
						<input type="text" id="selectedLanguage" class="form-control" placeholder="Language..." aria-label="Language">
					</div>
				</div>
				
<p>
The HTML for the button and the text field are listed below:
</p>

{% highlight html %}
<div class="row g-3 align-items-center">
	<div class="col-3">
		<button type="button" id="btnLanguage" class="btn btn-primary">Select a Language</button>
	</div>

	<div class="col-9">
		<input type="text" id="selectedLanguage" class="form-control" placeholder="Language..." aria-label="Language">
	</div>
</div>
{% endhighlight %}

<p>
And the corresponding JavaScript codes:
</p>

{% highlight javascript %}
function selectLanguage( params ) {
	$( '#selectedLanguage' ).val( `${params[0]}, ${params[1]}` );
};

$( document ).ready( function() {
	$( '#btnLanguage' ).bhDropdownSelect({
		source: AVAILABLE_LANGUAGES,
		selectCallback: selectLanguage,
		theme: 'safe'
	}).addClass( 'fw-bold' );
});

{% endhighlight %}

				<div class="row g-3 align-items-center mt-2">
					<div class="col">
						“Select Your Tropical Fruit” demonstrates:
						<ul>
							<li>
								Using a different data list. That is, on the same page,
								different instances of this plugin are able to operate
								on different data lists.
							</li>

							<li>
								Setting “theme” to <span class="fw-bold">“eyesore”</span>
								-- which is the second CSS that comes with this plugin.
							</li>
						</ul>
					</div>
				</div>

				<div class="row g-3 align-items-center mb-4">
					<div class="col input-group mb-3">
						<button class="btn btn-outline-primary" type="button" id="btnTropicalFruits">Select Your Tropical Fruit</button>
						<input type="text" id="selectedFruit" class="form-control" placeholder="" aria-label="Example text with button addon" aria-describedby="btnTropicalFruits">
					</div>
				</div>

<p>
HTML for “Select Your Tropical Fruit”:
</p>

{% highlight html %}
<div class="row g-3 align-items-center">
	<div class="col input-group mb-3">
		<button class="btn btn-outline-primary" type="button" id="btnTropicalFruits">Select Your Tropical Fruit</button>
		<input type="text" id="selectedFruit" class="form-control" placeholder="" aria-label="Example text with button addon" aria-describedby="btnTropicalFruits">
	</div>
</div>
{% endhighlight %}				

<p>
JavaScript for “Select Your Tropical Fruit”:
</p>
				
{% highlight javascript %}
$( document ).ready( function() {
	$( '#btnTropicalFruits' ).bhDropdownSelect({
		source: TROPICAL_FRUITS,

		selectCallback: function( params ) {
			$( '#selectedFruit' ).val( `${params[0]}, ${params[1]}` );
		},

		theme: 'eyesore'
	});
});	
{% endhighlight %}				

				<div class="row g-3 align-items-center mt-2 mb-2">
					<div class="col">
						“Click to Select” -- this last one demonstrates what happen
						when “source” -- that is, the data list -- is set to null,
						this is also the default setting for option “source”.
					</div>
				</div>

				<div class="row g-3 align-items-center mb-4">
					<div class="col-4">
						<button type="button" id="btnNoSource" class="btn btn-secondary">Click to Select</button>
					</div>

					<div class="col-8">
						<input type="text" class="form-control" placeholder="Something..." aria-label="No Source Data">
					</div>
				</div>
				
<p>
HTML for “Click to Select”:
</p>

{% highlight html %}
<div class="row g-3 align-items-center">
	<div class="col-4">
		<button type="button" id="btnNoSource" class="btn btn-secondary">Click to Select</button>
	</div>

	<div class="col-8">
		<input type="text" class="form-control" placeholder="Something..." aria-label="No Source Data">
	</div>
</div>
{% endhighlight %}				

<p>
JavaScript for “Click to Select”:
</p>

{% highlight javascript %}
$( document ).ready( function() {
	$( '#btnNoSource' ).bhDropdownSelect({
		source: null
	});
});
{% endhighlight %}								

<p class="my-4">
<h3>Libraries' Scripts and Data List Format</h3>
</p>

<p>
This plugin needs Bootstrap and jQuery. We must include the followings:
</p>

{% highlight javascript %}
<!-- Bootstrap 5.1.3 and jQuery 3.6.0. -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>

<!-- jQuery plugin bhDropdownSelect's CSS and JS. --->
<link href="https://cdn.jsdelivr.net/gh/behai-nguyen/jquery-bhdropdownselect@main/src/bhDropdownSelect.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/gh/behai-nguyen/jquery-bhdropdownselect@main/src/bhDropdownSelect.js"></script>
{% endhighlight %}

<p>
Please note the above is just one way of doing the inclusion. And also for 
this plugin, I am not providing minified version of the source files. For 
my project, I am just bundling them into the project's minified JS and 
minified CSS.
</p>

<p>
Data lists, such as <span class="fw-bold">AVAILABLE_LANGUAGES</span> 
and <span class="fw-bold">TROPICAL_FRUITS</span> as seen previously, 
are arrays of objects. Each object has two string properties: 
<span class="fw-bold">'code'</span> and <span class="fw-bold">'name'</span>. 
For example:
</p>

{% highlight javascript %}
const TROPICAL_FRUITS = [
	{ code: "tf00255", name: "Watermelon"},
	...
	{ code: "tf00000", name: "Apple"},
	{ code: "tf00005", name: "Apricot"}	
];
{% endhighlight %}

<p class="my-4">
<h3>Theming</h3>
</p>

<p>
This plugin has two built-in themes: <span class="fw-bold">safe</span> 
and <span class="fw-bold">eyesore</span>. <span class="fw-bold">safe</span>
is basically the default colours provided by Bootstrap CSS. 
<span class="fw-bold">eyesore</span>
is my own colour scheme. I am horrible with colours, I name them like
that for attention catching.
</p>

<p>
Users can define their colour scheme, such as 
<span class="fw-bold">example02</span> as seen in the 
following next and final example.
</p>

				<div class="row g-3 align-items-center mt-3">
					<div class="col">
						<h3>jQuery plugin bhDropdownSelect usage Example 02.</h3>
					</div>
				</div>

				<div class="row g-3 align-items-center mt-2 mb-2">
					<div class="col">
						This example demonstrates using user-defined theme: <span class="fw-bold">example02</span>.
					</div>
				</div>

				<div class="row g-3 align-items-center mb-4">
					<div class="col input-group mb-3">
						<button class="btn btn-outline-primary" type="button" id="btnTropicalFruits2">Select Your Tropical Fruit</button>
						<input type="text" id="selectedFruit2" class="form-control" placeholder="" aria-label="Example text with button addon" aria-describedby="btnTropicalFruits2">
					</div>
				</div>

<p>
The CSS for <span class="fw-bold">example02</span> theme:
</p>

{% highlight css %}
/* User-defined theme: example02. */
.dropdown-select.theme-example02 .modal-header { background-color: #adbcce; }

.dropdown-select.theme-example02 .modal-header input[type="text"] {
	background-color: #d5dce5;
}

.dropdown-select.theme-example02 .modal-body { background-color: #879ebc; }

.dropdown-select.theme-example02 .modal-body .container .row:nth-child( odd ) {
	background-color: #9fc5f7;
}

.dropdown-select.theme-example02 .modal-body .container .row:nth-child( even ) {
	background-color: #3b87ec;
}

.dropdown-select.theme-example02 .item-highlight {
	background-color: #c1d8f5;
	font-style: italic;
	font-weight: bold;
}

.dropdown-select.theme-example02 .item-normal {
	font-style: normal;
	font-weight: normal;
}
{% endhighlight %}

<p>
HTML:
</p>

{% highlight html %}
<div class="row g-3 align-items-center mb-4">
	<div class="col input-group mb-3">
		<button class="btn btn-outline-primary" type="button" id="btnTropicalFruits2">Select Your Tropical Fruit</button>
		<input type="text" id="selectedFruit2" class="form-control" placeholder="" aria-label="Example text with button addon" aria-describedby="btnTropicalFruits2">
	</div>
</div>
{% endhighlight %}				

<p>
JavaScript:
</p>

{% highlight javascript %}
$( document ).ready( function() {

	$( '#btnTropicalFruits2' ).bhDropdownSelect({
		source: TROPICAL_FRUITS,

		selectCallback: function( params ) {
			$( '#selectedFruit2' ).val( `${params[0]}, ${params[1]}` );
		},

		theme: 'example02'
	});
});
{% endhighlight %}				

<p class="my-4">
<h3>Some Further Notes</h3>
</p>

<p>
As mentioned before, this version of the plugin does not have
smart positioning, it is just assumed that there is enough
space to make it fully visible. I would like to address this
as the first priority in the next version.
</p>

<p>
The container dialog is fixed size, there are no options to set
the width nor the height.
</p>

<p>
Still related to positioning, while the dialog is opened, if we
scroll the screen up, it does not move with the element that it
is attached to.
</p>

<p>
I would also like to make the number of columns a configureable
option. 
</p>

<p>
Another desirable option is to enable multiple selection, whereby 
users can select multiple items, then hit ( a new button ) to 
select and close the dialog.
</p>
			</div>
		</div>
    </main>

	{%- include bootstrap-livedemo-footer.html -%}

</body>