---
layout: post
title: "Raspberry Pi 4B LinuxCNC: Mesa 7I96S Ethernet Motion Control, Expanded to Four CL57T Drivers and Four Nema 23 Closed-Loop Stepper Motors"

description: I now have four CL57T drivers and four Nema 23 closed-loop stepper motors for the X, Y, Y-tandem, and Z axes. This video briefly recaps the configuration and wiring, and concludes by running a test G-code program that draws a square on the X-Y plane, showing the X-axis motor and both Y-axis motors running.

tags:
- Raspberry
- 4B
- Pi4
- LinuxCNC
- Mesa 7I96S
- 7I96S
- Main Power Distribution
- Power Supply Unit
- UHP-750-36
- MDR-100-24
- MDR-10-5
- G-code
---

<em>
I now have four CL57T drivers and four Nema 23 closed-loop stepper motors for the X, Y, Y-tandem, and Z axes. This video briefly recaps the configuration and wiring, and concludes by running a test G-code program that draws a square on the X-Y plane, showing the X-axis motor and both Y-axis motors running.
</em>

<h3>
🐧 <a href="https://github.com/behai-nguyen/linuxcnc" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![feature_image.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/06/feature_image.png) |
|:--:|
| *Raspberry Pi 4B LinuxCNC: Mesa 7I96S Ethernet Motion Control, Expanded to Four CL57T Drivers and Four Nema 23 Closed-Loop Stepper Motors* |

<div style="background-color:yellow;width:100%;height:330px">
    <div style="float:left;width:18%;height:100px;background-image:url('https://behainguyen.files.wordpress.com/2022/07/danger-2324940__340.png');background-repeat:no-repeat;background-position:center center;background-size:80px 80px;background-repeat:no-repeat">
    </div>

	<div style="float:right;width:82%;font-weight:bold;padding:10px 10px 0 0">
<p>
I am just an ordinary computer programmer and not trained in any of the electronic engineering disciplines. This LinuxCNC project is a learning process for me. This post is not meant to be a tutorial or instructional guide; it is my own documentation so I will not forget what I have learned.
</p>

<p>
I am not to be held responsible for any damages or injuries resulting from using the information presented in this post.
</p>
	</div>
</div>

<iframe 
  src="https://www.youtube.com/embed/pEOmPJ4gfqo" 
  title="Raspberry Pi 4 Model B: Mesa 7I96S, Four Drivers & Motors, Draws a Square on X-Y Plane" 
  frameborder="0" 
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
  allowfullscreen
  style="width: 100%; aspect-ratio: 16 / 9; margin:20px 0 20px 0">
</iframe>

💡 To expand on a few points from the video: 

● This seventh post, 
<a href="https://behai-nguyen.github.io/2025/09/04/linuxcnc-07-main-power-wiring.html" 
title="Raspberry Pi 4B LinuxCNC: Main Power Distribution (Wiring)" 
target="_blank">Raspberry Pi 4B LinuxCNC: Main Power Distribution (Wiring)</a>, 
describes how all of the essential components are wired together to form a basic, 
functional, and testable machine. 

● The fourth post,
<a href="https://behai-nguyen.github.io/2025/02/16/linuxcnc-04-mesa-7i96s-clt57t-motor-driver.html" 
title="Raspberry Pi 4B LinuxCNC: Wiring the Mesa 7I96S Ethernet Motion Control, Closed-Loop CL57T Stepper Driver, and Nema 23 Stepper Motor" 
target="_blank">Raspberry Pi 4B LinuxCNC: Wiring the Mesa 7I96S Ethernet Motion Control, Closed-Loop CL57T Stepper Driver, and Nema 23 Stepper Motor</a>, 
describes how to connect the motor driver to the Mesa 7I96S card. It illustrates the 
connection using a single driver and a single motor. The same wiring applies to the 
remaining three drivers and motors; simply use the next three slots on the Mesa 7I96S 
card.

● I have not yet settled on how to wire the four drivers to the UHP-750-36 power supply. 
In the video, I am temporarily using two common distribution blocks. Please see the 
picture below, which is also included in the video: 

| ![UHP-750-36 PSU To Drivers Using Common Distribution Blocks](https://behainguyen.wordpress.com/wp-content/uploads/2026/06/uhp-750-36-to-drivers-common-dist-blocks.png) |
|:--:|
| UHP-750-36 PSU To Drivers Using Common Distribution Blocks |

There is also the option of using DIN rail terminal blocks. I may choose this option
for the final wiring.

● The GitHub location of the draw-square 
<a href="https://github.com/behai-nguyen/linuxcnc/blob/main/building_gcodes/02_draw_square.ngc" 
title="GitHub location of the draw square G-code program" 
target="_blank">G-code program</a> is available here.

✿✿✿

Feature image source:

<ul>
<li>
<a href="https://www.instructables.com/Easy-Raspberry-Pi-Based-ScreensaverSlideshow-for-E/" target="_blank">https://www.instructables.com/Easy-Raspberry-Pi-Based-ScreensaverSlideshow-for-E/</a>
</li>
<li>
<a href="https://forum.linuxcnc.org/show-your-stuff/32672-linuxcnc-logo?start=20#gallery-6" target="_blank">https://forum.linuxcnc.org/show-your-stuff/32672-linuxcnc-logo?start=20#gallery-6</a>
</li>
</ul>

<h3>
🐧 <a href="https://github.com/behai-nguyen/linuxcnc" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>
