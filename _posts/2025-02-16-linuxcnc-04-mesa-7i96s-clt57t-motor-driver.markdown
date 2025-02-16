---
layout: post
title: "Raspberry Pi 4B LinuxCNC: Wiring the Mesa 7I96S Ethernet Motion Control, Closed-Loop CL57T Stepper Driver, and Nema 23 Stepper Motor"

description: This post documents the wiring of the Mesa 7I96S Ethernet motion control STEP/IO Step & Dir plus I/O card to the CL57T closed-loop stepper driver, which in turn controls the closed-loop Mema 23 stepper motor. 

tags:
- Raspberry
- 4B
- Pi4
- LinuxCNC
- Mesa 7I96S
- 7I96S
- Motion Control
- Closed-Loop
- CL57T
- Driver
- Nema 23
---

<em>
This post documents the wiring of the Mesa <a href="https://store.mesanet.com/index.php?route=product/product&product_id=374" title="7I96S STEP/IO Step & dir plus I/O card" target="_blank">7I96S Ethernet motion control STEP/IO Step & Dir plus I/O card</a> to the <a href="https://www.omc-stepperonline.com/closed-loop-stepper-driver-v4-1-0-8-0a-24-48vdc-for-nema-17-23-24-stepper-motor-cl57t-v41" title="CL57T Closed-Loop Stepper Driver" target="_blank">CL57T closed-loop stepper driver</a>, which in turn controls the closed-loop <a href="https://www.omc-stepperonline.com/nema-23-closed-loop-stepper-motor-3-0nm-424oz-in-encoder-1000ppr-4000cpr-23hs45-4204d-e1000" title="Mema 23 Stepper Motor" target="_blank">Mema 23</a> stepper motor.
</em>

<h3>
🐧 <a href="https://github.com/behai-nguyen/linuxcnc" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![134-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/02/134-feature-image.png) |
|:--:|
| *Raspberry Pi 4B LinuxCNC: Wiring the Mesa 7I96S Ethernet Motion Control, Closed-Loop CL57T Stepper Driver, and Nema 23 Stepper Motor* |

<div style="background-color:yellow;width:100%;height:220px;margin-bottom:20px;">
    <div style="float:left;width:18%;height:100px;background-image:url('https://behainguyen.files.wordpress.com/2022/07/danger-2324940__340.png');background-repeat:no-repeat;background-position:center center;background-size:80px 80px;background-repeat:no-repeat">
    </div>

	<div style="float:right;width:80%;font-weight:bold;padding:10px 10px 0 0">
<p>
I am just an ordinary computer programmer and not trained in any of the electronic engineering disciplines. This LinuxCNC project is a learning process for me. This post is not meant to be a tutorial or instructional guide; it is my own documentation so I will not forget what I have learned.
</p>

<p>
I am not to be held responsible for any damages or injuries resulting from using the information presented in this post.
</p>
	</div>
</div>

This post is a continuation of the <a href="https://github.com/behai-nguyen/linuxcnc" title="Index of the Complete Series" target="_blank">previous posts</a> in this series. Please refer to them for information on hardware mentioned in this post but not discussed here. We will only discuss hardware introduced in this post. First, we will describe the hardware. Next, we will discuss the wiring, illustrated with diagrams. Finally, we will review some background stories and referenced literature.

<a id="cl57t-closed-loop-driver-nema23"></a>
❶ I chose to use a closed-loop stepper motor driver and motor. The driver is a 
<a href="https://www.omc-stepperonline.com/closed-loop-stepper-driver-v4-1-0-8-0a-24-48vdc-for-nema-17-23-24-stepper-motor-cl57t-v41" 
title="CL57T Closed-Loop Stepper Driver" target="_blank">CL57T</a>. 
The accompanying printed manual states it is version <code>4.1</code> (CL57T-V41),
but mine came with no free debugging cable. 
I can't find the PDF manual for version <code>4.1</code>, only for 
<a href="https://www.omc-stepperonline.com/download/CL57T_V4.0.pdf"
title="CL57T_V4.0.pdf" target="_blank">version 4.0</a>.

The stepper motor is a 
<a href="https://www.omc-stepperonline.com/nema-23-closed-loop-stepper-motor-3-0nm-424oz-in-encoder-1000ppr-4000cpr-23hs45-4204d-e1000" 
title="Mema 23 Stepper Motor" target="_blank">Mema 23</a> with a shaft diameter of 8mm.

I bought a single set of the 
<a href="https://www.ebay.com.au/itm/176350713978?_skw=nema+23+closed+loop+stepper+motor&itmmeta=01JA6QGH0K0096SNYAH36KN7HF&hash=item290f52587a%3Ag%3ARCIAAOSwKwVkso6S&var=475861444821" 
title="CL57T-V41 Closed-Loop Stepper Driver and Nema 23 Stepper Motor" 
target="_blank">CL57T-V41 Driver and Nema 23 Stepper Motor</a> from the StepperOnline Australian eBay store. I still need another three sets. I'm feeling uneasy about not being able to get them when the time comes, so I am keeping my fingers crossed 😂.

Presently, I don't yet have a proper power supply for this stepper motor. 
I'm using a 
<a href="https://www.amazon.com.au/dp/B07K7H7NB3?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1" 
title="DC Power Supply,30V 10A Variable Bench Lab Power Supply Switching 3-Digital Display Single-Output 220V, with Alligator Leads, AU Power Cord,Repairing Phones, Electronics,DIY,Test" 
target="_blank">DC 30V 10A Variable Bench Lab Power Supply</a> for learning purposes. 
I was not sure if this power supply was appropriate, so I made an inquiry to StepperOnline and received a response the next day confirming that it is okay for testing purposes. After I received the set, I actually made another three technical inquiries, and the assistance I received was simply impressive.

<a id="cl57t-nema23-7i96s-wiring"></a>
❷ <strong>CL57T-V41 Driver, Nema 23, and Mesa 7I96S Connection</strong>

<a id="cl57t-nema23-wiring"></a>
⓵ This StepperOnline page 
<a href="https://help.stepperonline.com/en/article/wiring-diagram-for-closed-loop-stepper-motor-4cddqy/" 
title="Wiring Diagram for Closed-Loop Stepper Motor" 
target="_blank">Wiring Diagram for Closed-Loop Stepper Motor</a> 
shows how to wire a CL57T-V41 driver to a closed-loop Nema 23 stepper motor, power supply, and <code>controller</code>:

| ![cl57t-controller-nema23-power-supply-wiring-diagram.jpg](https://behainguyen.wordpress.com/wp-content/uploads/2025/02/cl57t-controller-nema23-power-supply-wiring-diagram.jpg) |
|:--:|
| CL57T-V41 to a Controller, a Nema 23 and Power Supply wiring diagram |

The <code>controller</code> in the diagram can be a Raspberry Pi 4B or 
the Mesa <a href="https://store.mesanet.com/index.php?route=product/product&product_id=374" 
title="7I96S STEP/IO Step & dir plus I/O card" 
target="_blank">7I96S STEP/IO Step & dir plus I/O card</a>, among other devices.
I first learned how to control the driver and the stepper motor using the Raspberry Pi 4B and Python, 
which we will briefly describe in a <a href="#pi4b-cl57t-python ">later section</a>.

<a id="cl57t-7i96s-wiring"></a>
⓶ <strong>Page 12</strong> of the 
<a href="http://www.mesanet.com/pdf/parallel/7i96sman.pdf" 
title="The Mesa 7I96S Manual" target="_blank">Mesa 7I96S manual</a>, 
section "STEP/DIR INTERFACE," describes how to connect motor drivers to the 7I96S. I followed the instructions and presented my wiring to the forum for help. It turned out I did not get it correct. These two forum threads set me in the right direction:

<ol>
<li style="margin-top:10px;">
<a href="https://forum.linuxcnc.org/27-driver-boards/46380-7i96s-card-arrived-what-setup-is-recomended?start=80#319947" 
title="7i96S card arrived what setup is recomended" target="_blank">7i96S card arrived what setup is recomended</a>
</li>

<li style="margin-top:10px;">
<a href="https://forum.linuxcnc.org/27-driver-boards/53951-connecting-mesa-7i96s-to-dm542t#319951" 
title="Connecting mesa 7i96s to DM542T" target="_blank">Connecting mesa 7i96s to DM542T</a>
</li>
</ol>

The correct wiring is illustrated in the diagram below:

| ![clt57t-mesa-7i96s-channel-1.jpg](https://behainguyen.wordpress.com/wp-content/uploads/2025/02/clt57t-mesa-7i96s-channel-1.jpg) |
|:--:|
| CL57T-V41 Closed-Loop Stepper Driver to Mesa 7I96S Channel 1 |

The image below shows a close-up of the wiring:

| ![clt57t-mesa-7i96s-channel-1-close-up.jpg](https://behainguyen.wordpress.com/wp-content/uploads/2025/02/clt57t-mesa-7i96s-channel-1-close-up.jpg) |
|:--:|
| CL57T-V41 Closed-Loop Stepper Driver to Mesa 7I96S Channel 1 Close-Up |

The CL57T-V41 driver is connected to the Mesa 7I96S Step/Dir <code>Channel 1</code>. 
At the time of this writing, I have already got the Mesa Configuration Wizard application,
<a href="https://linuxcnc.org/docs/html/config/pncconf.html"
title="PnCconf Mesa Configuration Wizard" target="_blank">PnCconf</a>, 
to recognise this single stepper motor as the X-axis, and <code>PnCconf</code> is able to run (tune) this stepper motor.

I plan to have two stepper motors for the Y-axis, wired to 
<code>Channel 2</code> and <code>Channel 3</code>, respectively.
The Z-axis stepper motor is wired to <code>Channel 4</code>, leaving 
<code>Channel 5</code> unused.

👉 <strong>Regarding the CL57T-V41 driver 5V/24V <code>S3-Selector</code></strong> 
switch, it must be set to 5V for the Mesa 7I96S, as illustrated in the photo below: 

| ![cl57t-s3-set-to-5v.jpg](https://behainguyen.wordpress.com/wp-content/uploads/2025/02/cl57t-s3-set-to-5v.jpg) |
|:--:|
| The CL57T-V41 driver 5V/24V S3-Selector Switch Set to 5V |

👉 Please note that when used with a Raspberry Pi 4B, the CL57T-V41 driver 5V/24V 
<code>S3-Selector</code> switch is also set to 5V.

<a id="background-info"></a>
❸ <strong>Some Background Stories</strong>

In this section, I describe how I was led to the CL57T-V41 closed-loop driver, Nema 23, and Mesa 7I96S motion controller. Then, I briefly discuss my attempt to control the CL57T-V41 and Nema 23 using a Raspberry Pi 4B and Python.

<a id="background-stories"></a>
⓵ When I first started researching stepper motors, I found this video on the 
<strong>MrPragmaticLee</strong> channel, <a href="https://www.youtube.com/watch?v=WBEdVl9QlvY" 
title="MrPragmaticLee channel | Controlling Large Stepper Motor With Raspberry Pi" 
target="_blank">Controlling Large Stepper Motor With Raspberry Pi</a>, very helpful. 
Initially, I thought I would go with an open-loop stepper driver.

<a id="background-stories-thehardwareguy-video"></a>
Further studies led me to this decisive video: 
<a href="https://www.youtube.com/watch?v=Og-nvmThAJE" 
title="thehardwareguy | DIY CNC 010 - Closed Loop NEMA Wiring and Mach3 Setup" 
target="_blank">DIY CNC 010 - Closed Loop NEMA Wiring and Mach3 Setup</a> 
by <strong>thehardwareguy</strong>. 
After watching it, I made up my mind to go with the same closed-loop stepper driver and motor, which is the CL57T-V41 driver and Nema 23. I keep referring back to this video as I progress and need to carry out the next step. 🙏 <strong>For the electronics, I am going to adhere to his instructions to the letter.</strong>

Initially, I thought I would use the <code>Mach3</code> application as well. 
However, further research led me to 
<a href="http://linuxcnc.org/" title="LinuxCNC" target="_blank">LinuxCNC</a>, which, 
according to forum posts, offers better performance. It is also free and can run on Raspberry Pi 4B and 5. The drawback is that there is no cheap LinuxCNC breakout board available. After some study, it became apparent that the Mesa 7I96S is the clear choice. Instead of paying for a <code>Mach3</code> license, I decided to pay for the Mesa 7I96S card.

I already have a Raspberry Pi 4B. I ordered and received the 
<a href="https://www.ebay.com.au/itm/176350713978?_skw=nema+23+closed+loop+stepper+motor&itmmeta=01JA6QGH0K0096SNYAH36KN7HF&hash=item290f52587a%3Ag%3ARCIAAOSwKwVkso6S&var=475861444821" 
title="CL57T-V41 Closed-Loop Stepper Driver and Nema 23 Stepper Motor" 
target="_blank">CL57T-V41 Driver and Nema 23 Stepper Motor</a> 
set toward the end of October 2024. (I had the Mesa 7I96S card on hand on 22/01/2025.)

<a id="pi4b-cl57t-python"></a>
⓶ After some more research and studies, as well as asking StepperOnline for help, I was able to get my Raspberry Pi 4B to run with the CL57T-V41 driver and Nema 23 stepper motor. The <code>Description</code> section of my following video includes the complete Python code and other essential information:

[![Raspberry Pi 4 Model B, Microstep with CL57T Driver, Nema 23 Closed Loop Stepper Motor 3Nm](https://i.ytimg.com/an_webp/CJ-oipeuJJY/mqdefault_6s.webp?du=3000&sqp=CPqbx70G&rs=AOn4CLAC8l5VX46klhMQaW2nI492xKpExg)](https://www.youtube.com/watch?v=CJ-oipeuJJY)

The image below shows the wiring diagram used in the video:

| ![01-cl57t-cl57t-raspberry-pi-4b-wiring-diagram.jpg](https://behainguyen.wordpress.com/wp-content/uploads/2024/10/01-cl57t-cl57t-raspberry-pi-4b-wiring-diagram.jpg) |
|:--:|
| Raspberry Pi 4B and the CL57T-V41 Closed-Loop Stepper Driver |

I also sought help from the forum to further my understanding of microstepping: 
<a href="https://forum.linuxcnc.org/51-ot-posts/54440-please-help-with-nema-23-closed-loop-cl57t-v41-driver-microstep-switches" 
title="Please help with Nema 23 closed loop CL57T-V41 driver Microstep Switches" 
target="_blank">Please help with Nema 23 closed loop CL57T-V41 driver Microstep Switches</a>.

This video shows my first attempt with the CL57T-V41 driver, where I was not yet able to work out the microstepping: 
<a href="https://www.youtube.com/watch?v=UKlGz3DbJzk" 
title="Raspberry Pi 4 Model B, CL57T Driver, Nema 23 Closed Loop Stepper Motor 3Nm (424.83oz.in)" 
target="_blank">Raspberry Pi 4 Model B, CL57T Driver, Nema 23 Closed Loop Stepper Motor 3Nm (424.83oz.in)</a>

I should have done a post on this subject, I thought about it... But it never eventuated. When I started this project in the second week of October 2024, everything was a bit chaotic. I frequently switched between researching hardware and software. I can't clearly remember the exact sequence of what I have done.

<a id="concluding-remarks"></a>
❹ This post is documentation for myself so that I will not forget what I have done. I have taken great care in my learning process, and hopefully, there are not too many major errors and mistakes in my understanding. I document bits and pieces of my progress with this project in the hope that, if I ever get to successfully finish it, there will be a complete set of diagrams and steps that might help some future new starters in some way. I also believe that, being a non-professional in this area, the information I present can be easily related to by people on the same page.

If you happen to read this post, thank you for your time, and I hope I did not waste it. Stay safe, as always.

✿✿✿

Feature image source:

<ul>
<li>
<a href="https://commons.wikimedia.org/wiki/File:Debian_12_%28Bookworm%29_-_GNOME_desktop.png" target="_blank">https://commons.wikimedia.org/wiki/File:Debian_12_%28Bookworm%29_-_GNOME_desktop.png</a>
</li>
<li>
<a href="https://www.instructables.com/Easy-Raspberry-Pi-Based-ScreensaverSlideshow-for-E/" target="_blank">https://www.instructables.com/Easy-Raspberry-Pi-Based-ScreensaverSlideshow-for-E/</a>
</li>
<li>
<a href="https://store.mesanet.com/index.php?route=product/product&product_id=374" target="_blank">https://store.mesanet.com/index.php?route=product/product&product_id=374</a>
</li>
<li>
<a href="https://forum.linuxcnc.org/show-your-stuff/32672-linuxcnc-logo?start=20#gallery-6" target="_blank">https://forum.linuxcnc.org/show-your-stuff/32672-linuxcnc-logo?start=20#gallery-6</a>
</li>
</ul>

<h3>
🐧 <a href="https://github.com/behai-nguyen/linuxcnc" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>
