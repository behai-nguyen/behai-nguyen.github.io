---
layout: post
title:  "Bootstrap 5.0 Draggable Dialogs Without jQuery UI."
---

jQuery UI 
comes with draggable capability, and so do jQuery dialogs.
Bootstrap 5.0 dialogs are not draggable.

<a href="https://behai-nguyen.github.io/demo/014/bootstrap-5-draggable-dialog.html" class="medium-font-size" target="_blank">Draggable Bootstrap 5.0 Dialogs Demo</a>.

I thought I would have to write something to enable draggability for 
Bootstrap 5.0 dialogs. But _Draggable without jQuery UI_ is a popular 
subject on the Internet. And while researching, I have come across 
several sites whom have done this already. The one I like best is 
[ https://css-tricks.com/snippets/jquery/draggable-without-jquery-ui/ ](https://css-tricks.com/snippets/jquery/draggable-without-jquery-ui/){:target="_blank"}.

It is a general purpose code, which can be used with Bootstrap 5.0 dialogs.
I re-list this code below as it is, with my own comments:

{% highlight javascript %}

//
// Description:
//
//    Enables draggable without using jQuery UI.
//
// Sources:
//
//    This code is not mine, it is from:
//
//    https://css-tricks.com/snippets/jquery/draggable-without-jquery-ui/
//
//    Referenced on Stackoverflow:
//
//    https://stackoverflow.com/questions/45194164/bootstrap-3-modal-make-it-movable-draggable-without-jquery-ui
//
//    See answer on Apr 13, 2020 by jstuardo.
//    Reproduced code from css-tricks with some slight modifications.
// 
//    ( I found css-tricks first, then this Stackoverflow post :) )
//
// Usage:
//
//   $( '#exampleModal' ).on('shown.bs.modal', function () {
//       $(this).find('.modal-dialog').drags();
//   });
//
//   exampleModal is a Bootstrap 5.1 modal dialog HTML.
//
(function ($) {
    $.fn.drags = function (opt) {

        opt = $.extend({ handle: "", cursor: "move" }, opt);

        var $el = null;
        if (opt.handle === "") {
            $el = this;
        } else {
            $el = this.find(opt.handle);
        }
        return $el.css('cursor', opt.cursor).on("mousedown", function (e) {
            var $drag = null;
            if (opt.handle === "") {
                $drag = $(this).addClass('draggable');
            } else {
                $drag = $(this).addClass('active-handle').parent().addClass('draggable');
            }
            var z_idx = $drag.css('z-index'),
                drg_h = $drag.outerHeight(),
                drg_w = $drag.outerWidth(),
                pos_y = $drag.offset().top + drg_h - e.pageY,
                pos_x = $drag.offset().left + drg_w - e.pageX;
            $drag.css('z-index', 1000).parents().on("mousemove", function (e) {
                $('.draggable').offset({
                    top: e.pageY + pos_y - drg_h,
                    left: e.pageX + pos_x - drg_w
                }).on("mouseup", function () {
                    $(this).removeClass('draggable').css('z-index', z_idx);
                });
            });
            e.preventDefault(); // disable selection
        }).on("mouseup", function () {
            if (opt.handle === "") {
                $(this).removeClass('draggable');
            } else {
                $(this).removeClass('active-handle').parent().removeClass('draggable');
            }
        });

    }
})(jQuery);

{% endhighlight %}

GitHub: [ https://github.com/behai-nguyen/js/blob/main/drags.js ](https://github.com/behai-nguyen/js/blob/main/drags.js){:target="_blank"}.

jsdelivr: [ https://cdn.jsdelivr.net/gh/behai-nguyen/js@latest/drags.js ](https://cdn.jsdelivr.net/gh/behai-nguyen/js@latest/drags.js){:target="_blank"}.

The HTML 
below is from 
[ https://getbootstrap.com/docs/5.0/components/modal/ ](https://getbootstrap.com/docs/5.0/components/modal/){:target="_blank"}.
Also, if you are not yet familiar 
Bootstrap 5.0 modal events, please take a look at 
[ https://getbootstrap.com/docs/5.0/components/modal/#events ](https://getbootstrap.com/docs/5.0/components/modal/#events){:target="_blank"} --
which explains events in detail.

{% highlight javascript %}

<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <title>Draggable Bootstrap v5.1 Dialog</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>

    <script src="https://cdn.jsdelivr.net/gh/behai-nguyen/js@latest/drags.js"></script>

    <script>
        $( document ).ready( function() {

            $( '#exampleModal' ).on('shown.bs.modal', function () {
                $(this).find('.modal-dialog').drags();
            });

        });
    </script>
</head>

<body>
    <!-- Button trigger modal -->
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
        Launch demo modal
    </button>

    <!-- Modal -->
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>

                <div class="modal-body">
                    ...
                </div>

                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary">Save changes</button>
                </div>
            </div>
        </div>
    </div>
</body>
</html>

{% endhighlight %}

We're interested in the following lines: on the modal open event, we give it 
the draggable capability:

{% highlight javascript %}
$( '#exampleModal' ).on('shown.bs.modal', function () {
	$(this).find('.modal-dialog').drags();
});
{% endhighlight %}

<a href="https://behai-nguyen.github.io/demo/014/bootstrap-5-draggable-dialog.html" class="medium-font-size" target="_blank">Draggable Bootstrap 5.0 Dialogs Demo</a>.

I'm interested in making Bootstrap 5.0 dialogs draggable, there're others 
who're interested in it as well, so I thought I would just document my 
findings. I hope you find this useful somehow and thank you for visiting.
