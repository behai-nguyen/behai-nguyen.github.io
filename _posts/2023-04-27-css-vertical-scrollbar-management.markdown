---
layout: post
title: "Pure CSS: Vertical ScrollBar Management."
description: CSS property scrollbar-gutter helps working with vertical scrollbar much easier. We can now have a pure CSS solution rather than having to fiddle around with JavaScript -- which can be very painful! I have just solved a problem I had with vertical scrollbar using this property, I am discussing my implementation with a complete working demo HTML page.

tags:
- Pure
- CSS
- Vertical
- Scrollbar
---

<em>CSS property scrollbar-gutter helps working with vertical scrollbar much easier. We can now have a pure CSS solution rather than having to fiddle around with JavaScript -- which can be very painful! I have just solved a problem I had with vertical scrollbar using this property, I am discussing my implementation with a complete working demo HTML page. </em>

| ![063-feature-image.png](https://behainguyen.files.wordpress.com/2023/04/063-feature-image.png)
|:--:|
| *Pure CSS: Vertical ScrollBar Management.* |

Let's first briefly discuss what we want to achieve. I am using <a href="https://getbootstrap.com/docs/5.0/getting-started/introduction/" title="Bootstrap v5.0" target="_blank">Bootstrap v5.0</a> grid layout in my <code>HTML</code> pages. I have a long dynamic data list sitting in a <code>div</code>, and so this <code>div</code> must have a vertical scrollbar, users can select a row at a time from this list to move to a second list. They can also remove a row from this second list, and the just removed row will be moved back to the first list.

As the second list grows, the vertical scrollbar will eventually appear. And on the first list, the vertical scrollbar could disappear. It goes without saying, if enough rows get removed from the second list, the vertical scrollbar would disappear also.

The above behaviour happens naturally, all we have to do is setting the height and vertical scrolling on the two <code>div</code>s.

The two lists also have a header or a label row, each. <strong>And this's where the issue is: <em>I want the scrollbar to always sit under the header row, and the data columns must always align with the respective header columns -- both when the list has the vertical scrollbar and without.</em></strong> The below screen capture, from the demo page, shows this behaviour:

![063-01.png](https://behainguyen.files.wordpress.com/2023/04/063-01.png)

Originally, I had <code>JavaScript</code> to recalculate the columns' width in response to when a vertical scrollbar appears and disappears -- I had around 45 (forty five) lines of <code>JavaScript</code>, and still, I could not get it to work correctly at all times. After some searching, I came to this <a href="https://developer.mozilla.org/en-US/docs/Web/CSS/scrollbar-gutter" title="scrollbar-gutter" target="_blank">scrollbar-gutter</a> <code>CSS</code> property. 

It is so beautiful, and easy to use... Please run the following demo to see this <code>CSS</code> property in action:

<strong>🚀 Demo URL</strong> -- <a href="https://behai-nguyen.github.io/demo/063/css-vertical-scrollbar.html" title="https://behai-nguyen.github.io/demo/063/css-vertical-scrollbar.html" target="_blank">https://behai-nguyen.github.io/demo/063/css-vertical-scrollbar.html</a>

It's a self-contained page, you can copy it to your localhost and play around with it. For example, try removing <code>scrollbar-gutter: stable;</code> from:

```css
.vertical-scrollable {
	overflow-y: auto;
	overflow-x: hidden;
	scrollbar-gutter: stable;
}
```

to see how it affects the layout. 

Please note that, I have <code>vertical-scrollable</code> on both lists' header rows:

```html
<div class="row py-2 border-bottom vertical-scrollable">
...
```

This feels strange, since the header rows do not have a scrollbar. There is a reason for it. The documentation <a href="https://developer.mozilla.org/en-US/docs/Web/CSS/scrollbar-gutter" title="scrollbar-gutter" target="_blank">scrollbar-gutter</a> states:

> The scrollbar-gutter CSS property allows authors to reserve space for the scrollbar, preventing unwanted layout changes as the content grows while also avoiding unnecessary visuals when scrolling isn't needed.
> 
> An element's scrollbar gutter is the space between the inner border edge and the outer padding edge, where the browser may display a scrollbar. If no scrollbar is present, the gutter will be painted as an extension of the padding.

So, basically, I am just “reserving” vertical scrollbar space on the header rows, so that <strong>header columns are pushed to the left by the same amount as the data columns</strong> -- making them always aligned.

The <code>div</code> containers for the two lists should be self-explanatory:

```html
<div class="col-6 vertical-scrollable data-list-height selector-available-data"></div>
<div class="col-6 vertical-scrollable data-list-height selector-selected-data" data-render-target="true"></div>
```

This demo page is actually a simplified version of pages from a project I have been working. An example of a page:

![063-02.jpg](https://behainguyen.files.wordpress.com/2023/04/063-02.jpg)

I do realise that <a href="https://getbootstrap.com/docs/5.0/getting-started/introduction/" title="Bootstrap v5.0" target="_blank">Bootstrap v5.0</a> handles vertical scrollbar quite well, if we accept the default behaviour: the scrollbar actually comes up beside the header row. I do not like this look, this is the only reason why I went through all this trouble. It feels satisfying nailing this issue at last though 😂.

I hope you find this information useful. Thank you for reading. And stay safe as always.

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
<a href="https://pngtree.com/element/down?id=NDE3NDU3MQ==&type=1&time=1682603162&token=M2Y3OTQwOWEyMGZhMGJmZjNjYmVlNjcxOWU0MzNhYzA=" target="_blank">https://pngtree.com/element/down?id=NDE3NDU3MQ==&type=1&time=1682603162&token=M2Y3OTQwOWEyMGZhMGJmZjNjYmVlNjcxOWU0MzNhYzA=</a>
</li>
</ul>
