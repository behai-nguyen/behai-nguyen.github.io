---
layout: post
title: "Bootstrap 5.0 Buttons with Icon and Text"
description: In this post, we discuss how to use Bootstrap 5.0 icon CSS with Bootstrap CSS to create buttons with icon and text, and buttons with icon and no text.
tags:
- Bootstrap 5.0
- Button
- Icon
- Text
---

*In this post, we discuss how to use Bootstrap 5.0 icon CSS with Bootstrap CSS to create buttons with icon and text, and buttons with icon and no text.*

| ![042-feature-image.png](https://behainguyen.files.wordpress.com/2022/10/042-feature-image.png) |
|:--:|
| *Bootstrap 5.0 Buttons with Icon and Text* |

Bootstrap provides free, high quality, open source icon library with over 1,600 icons. 
Please see <a href="https://icons.getbootstrap.com/"
title="Bootstrap Icons" target="_blank">https://icons.getbootstrap.com/</a>, this page
lists available icons and their names. We'll use these icon names to display the actual
icons.

Toward the bottom of the page, under the <strong>Install</strong> section, we'll find
the download button and 
<span style="font-family:Monaco,Consolas,Menlo,Courier,monospace;">
CDN</span> link to 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
bootstrap-icons.css</span>.

To create a button with icon using Bootstrap 5.0:

```html
<button type="button" class="btn btn-primary btn-sm"><span class="bi-ICON-NAME"></span>&nbsp;BUTTON-TEXT</button>
```

Replace 
<span class="keyword">
<strong>ICON-NAME</strong></span> with a name listed in the page mentioned above,
and of course
<span class="keyword">
<strong>BUTTON-TEXT</strong></span> with an appropriate label. For example:

```html
<button type="button" class="btn btn-secondary"><span class="bi-search"></span>&nbsp;Search</button>
```

Please note, in the above example, I don't use
<span class="keyword">
Bootstrap CSS btn-sm</span>.

To create a button with only an icon and no text, simply remove the label:

```html
<button type="button" class="btn btn-secondary"><span class="bi-search"></span></button>
```

I've created a simple 
<span class="keyword">
HTML</span> page which shows a few buttons which I'm using in my project:

```html
<!doctype html>
<html lang="en">
<head>
	<!-- Required meta tags -->
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="canonical" href="https://icons.getbootstrap.com/">

	<!-- Bootstrap CSS -->
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

	<!-- Bootstrap Icons CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.1/font/bootstrap-icons.css" rel="stylesheet">
	<title>Bootstrap Icons</title>
</head>

<body>
    <button type="button" class="btn btn-primary btn-sm"><span class="bi-plus-square-fill"></span>&nbsp;Add</button>
    <button type="button" class="btn btn-secondary"><span class="bi-search"></span>&nbsp;Search</button>
    <button type="button" class="btn btn-danger"><span class="bi-trash"></span>&nbsp;Delete</button>
    <br/><br/>
	
    <button type="button" class="btn btn-primary"><span class="bi-plus-square-fill"></span></button>
    <button type="button" class="btn btn-secondary btn-sm"><span class="bi-search"></span></button>
    <button type="button" class="btn btn-danger"><span class="bi-trash"></span></button>
</body>
</html>
```

The live URL of the example page: 
<a href="https://behai-nguyen.github.io/demo/042/bootstrap-5-button-icon.html"
title="Bootstrap 5.0 Icon Buttons"
target="_blank">https://behai-nguyen.github.io/demo/042/bootstrap-5-button-icon.html</a>

<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
bootstrap-icons.css</span> uses two font files: 

```css
@font-face {
  font-display: block;
  font-family: "bootstrap-icons";
  src: url("./fonts/bootstrap-icons.woff2?8d200481aa7f02a2d63a331fc782cfaf") format("woff2"),
url("./fonts/bootstrap-icons.woff?8d200481aa7f02a2d63a331fc782cfaf") format("woff");
}
```

These two font files are part of the download. I believe we can include
them in our own applications -- but please do your own investigations before you
redistribute them.

I did enjoy looking at how to do this... these two 
<span class="keyword">
Bootstrap CSS libraries</span> work together seamlessly. Thank you
for reading, and I hope you find this post useful. Stay safe as always.