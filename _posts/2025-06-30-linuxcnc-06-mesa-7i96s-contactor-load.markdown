---
layout: post
title: "Raspberry Pi 4B LinuxCNC: Wiring the Mesa 7I96S Card and a Contactor to Control a Grinder/Router via the LinuxCNC Application"

description: This post documents how to wire the Mesa 7I96S Ethernet motion control STEP/IO Step & Dir plus I/O card to a contactor, enabling the LinuxCNC application to switch a wood router (or grinder) on and off using G-code commands.

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2025/06/contactor-no-terminal-led.png"

gallery-image-list-2:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2025/06/contactor-switch-one-phase-load.png"

gallery-image-list-3:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2025/06/contactor-to-mesa-7i96s-one-phase-load-01.png"

tags:
- Raspberry
- 4B
- Pi4
- LinuxCNC
- Mesa 7I96S
- 7I96S
- Motion Control
- Contactor
- Router
- Switch On
---

<em>
This post documents how to wire the Mesa <a href="https://store.mesanet.com/index.php?route=product/product&product_id=374" title="7I96S STEP/IO Step & dir plus I/O card" target="_blank">7I96S Ethernet motion control STEP/IO Step & Dir plus I/O card</a> to a contactor, enabling the LinuxCNC application to switch a wood router (or grinder) on and off using G-code commands.
</em>

<h3>
🐧 <a href="https://github.com/behai-nguyen/linuxcnc" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![141-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/06/141-feature-image.png) |
|:--:|
| *Raspberry Pi 4B LinuxCNC: Wiring the Mesa 7I96S Card and a Contactor to Control a Grinder/Router via the LinuxCNC Application* |

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

<a id="mesa-7i96s-manual"></a>
❶ <strong>The <a href="http://www.mesanet.com/pdf/parallel/7i96sman.pdf" 
title="Mesa 7I96S manual" target="_blank">Mesa 7I96S Manual</a></strong>

Two pages in the manual are particularly relevant to this post:

● <strong>Page 14</strong> – Describes the characteristics of the input and output pins. Our primary focus is on the output pins. I have reviewed this page several times.

● <strong>Page 10</strong> – Lists the names and numbers of the input and output pins. We are interested in pins <code>OUT1-</code> and <code>OUT1+</code>, which correspond to pin <code>13</code> and <code>14</code>, respectively.

<a id="contactor-and-others"></a>
❷ <strong>Contactor and Associated Components</strong>

Although I read the <a href="http://www.mesanet.com/pdf/parallel/7i96sman.pdf" 
title="Mesa 7I96S manual" target="_blank">Mesa 7I96S manual</a>, I didn’t fully grasp that a relay or contactor could be used to switch a load via the Mesa 7I96S card from within LinuxCNC. In hindsight, some of the videos I watched mentioned this as well, but the point didn’t register at the time.

<a id="contactor"></a>
⓵ <strong>Contactor</strong>

While seeking help on the LinuxCNC forum regarding wiring the main power distribution, 
<a href="https://forum.linuxcnc.org/18-computer/55831-4-gang-1-way-switch-to-control-3-power-supplies-and-a-router-independently#325751" 
title="Main Power Distribution" target="_blank">Mr. RodW</a> noted:

>...
>So now you need to switch your router from your 7i96s.
>...

Following his suggestion, I sourced a 24VDC 
<a href="https://www.tropac.com.au/10-Pole-24VDC-Coil-5.5kW-12A-20A-1NO-Aux-Contact-Mini-Contactor-LS-Metasol" 
title="GMD-12M DC24V 5.5kW 3P Mini Contactor with 1NO Auxiliary Contact" 
target="_blank">GMD-12M DC24V 5.5kW 3P Mini Contactor with 1NO Auxiliary Contact</a> from an Australian supplier. It’s manufactured in South Korea and costs only a fraction of the price of a comparable Schneider model. This is a three-phase contactor with a Normally Open (NO) auxiliary terminal. We can, for example, use this NO terminal to power an LED indicator when the coil is energised.

<a id="flyback-diode"></a>
⓶ <strong>Flyback Diode</strong>

According to page 14 of the 
<a href="http://www.mesanet.com/pdf/parallel/7i96sman.pdf" title="Mesa 7I96S manual" 
target="_blank">Mesa 7I96S manual</a>: 

>...
>Inductive loads must have a flyback diode. The output polarity of outputs 0 through 3 must be observed (reversed outputs will be stuck-on).
>...

Based on my research, the following flyback diodes are suitable:

<ul>
<li style="margin-top:10px;">
<a href="https://www.jaycar.com.au/1n4007-1a-1000v-diode-pack-of-4/p/ZR1007" 
title="1N4007 1A 1000V Diode" target="_blank">1N4007</a> – A general-purpose 1A, 1000V diode.
</li>

<li style="margin-top:10px;">
<a href="https://www.futurlec.com/Diodes/FR107pr.shtml" 
title="FR107 1000V 1A Fast Recovery Diode" target="_blank">FR107</a>
 – A 1A, 1000V fast-recovery diode; a better option than the 1N4007. 
</li>

<li style="margin-top:10px;">
<a href="https://www.jaycar.com.au/diode-fr307-1000v-3a-d027-pack-10/p/ZR1052" 
title="Diode FR307 1000V 3A D027" target="_blank">FR307</a>
 – Similar to the FR107, but rated at 3A. I chose this one because it was in stock at my local JayCar store, saving me the need to order online.
</li>
</ul>

<a id="2a-fuse"></a>
⓷ <strong>2A Fuse</strong>

As emphasised on page 14 of the 
<a href="http://www.mesanet.com/pdf/parallel/7i96sman.pdf" title="Mesa 7I96S manual" 
target="_blank">Mesa 7I96S manual</a>: 

>**Note: The 7I96S outputs are not short circuit protected so a current limited power supply or a 2A to 5A fuse should be used in the power source that supplies outputs 0 through 3. Outputs 4 and 5 should be protected with a 1/4 Amp fuse.**

Since this is a DC circuit, I understand that a <strong>fast-blow fuse</strong> is 
required. I’m using this 
<a href="https://www.altronics.com.au/p/p2423-dinkle-35a-4mm-grey-fused-din-rail-terminal/" 
title="35A 4mm Grey Fused DIN Rail Terminal" target="_blank">DIN Rail fuse holder</a> 
compatible with <strong>M205-series fuses</strong>. The following options are suitable:

<ul>
<li style="margin-top:10px;">
<a href="https://www.altronics.com.au/p/s5734-2a-m205-fuse/" 
title="A 2A fast-blow fuse" target="_blank">2A M205 Fuse – Standard Glass</a>
</li>
<li style="margin-top:10px;">
<a href="https://www.altronics.com.au/p/s5927-2a-m205-ceramic-fuse/" 
title="A 2A fast-blow fuse" target="_blank">2A M205 Ceramic Fuse</a>
</li>
<li style="margin-top:10px;">
<a href="https://www.altronics.com.au/p/s5735-2a-m205-fuse-pk-10/" 
title="A 2A fast-blow fuse" target="_blank">2A M205 Fuse – Pack of 10</a>
</li>
</ul>

These are all locally available, which is a big plus compared to ordering online.

<a id="2a-load-mcb"></a>
⓸ <strong>10A 240VAC Miniature Circuit Breaker (MCB) to Protect the Load</strong>

To protect the load—in this case, a wood router—an appropriately rated <strong>Miniature Circuit Breaker (MCB)</strong> should be used. I’m using the following model: 
<a href="https://www.tropac.com.au/BKJ63N-1P-C10-LS-Miniature-Circuit-Breaker-10A-1P-6kA-C-Curve" 
title="BKJ63N 1P C10 |LS Miniature Circuit Breaker 10A 1P 6kA C Curve" 
target="_blank">BKJ63N 1P C10 |LS Miniature Circuit Breaker 10A 1P 6kA C Curve</a>. 

It’s manufactured in South Korea and supplied by the same vendor as <a href="#contactor">the contactor</a>. 
(Painfully, the delivery fee was <strong>AUD $22.00</strong> 😅)

<a id="wiring-diagrams"></a>
❸ <strong>Wiring Diagrams</strong>

<a id="no-led"></a>
⓵ <strong>Wiring the Contactor NO Terminal and LED Indicator</strong>

Back in my undergraduate years—over two decades ago—I completed two semesters of electronic engineering, where we wired logic gates using LEDs and similar components. Unfortunately, I’ve forgotten most of it. However, I’ve recently brushed up on the basics of electronics and now feel comfortable working with breadboards, LEDs, resistors, and related components.

After some Googling and a few wiring missteps, I was able to arrive at the correct setup, shown in the diagram below: 

{% include image-gallery.html list=page.gallery-image-list-1 %}
<br/>

I'm using a standard LED, with a <strong>current-limiting resistor</strong> between 
<strong>330Ω and 360Ω</strong>.

💡 <strong>Important</strong>: In the diagram, the <strong>negative side of the 
diode</strong> is connected to both the 
<strong><code>A2-</code> terminal</strong> of the contactor and the 
<strong>negative terminal of the 24VDC power supply (PSU)</strong>.

With this wiring in place, powering on the circuit causes the <strong>contactor 
coil to energise with a noticeable “click”</strong> as it pulls in. This closes 
the circuit and <strong>lights up the LED</strong>, confirming that the coil is active.

<a id="single-phase-load"></a>
⓶ <strong>Wiring the Contactor to Switch On a Load</strong>

In this setup, the <strong>load</strong> is intended to be a wood router. Since I 
don’t have a router yet, I’m using a <strong>Dremel grinder</strong> for testing.

I followed the wiring shown in the diagram below: 

{% include image-gallery.html list=page.gallery-image-list-2 %}
<br/>

💡 <strong>Important</strong>, I DID <strong>NOT</strong> cut into the grinder's main cable to access the <span style="color:#998378; font-weight:bold;">Live</span> wire. Instead, I used an extension cable with a male and female end for safe and reversible testing.

In the diagram, we’re using the contactor for <strong>single-phase switching</strong>, 
connecting only the first terminal pair: <strong><code>1/L1</code> and <code>2/T1</code></strong>.

👉 With this wiring, power is continuously supplied to the AC outlet, and the grinder’s power switch is left in the “on” position.

<ul>
<li style="margin-top:10px;">
<strong>When the contactor is off</strong>: terminals <code>1/L1</code> and <code>2/T1</code> are open → no power flows to the grinder.
</li>

<li style="margin-top:10px;">
<strong>When the contactor is on</strong>: terminals <code>1/L1</code> and <code>2/T1</code> are closed → power flows → the grinder runs.
</li>
</ul>

💥 Originally, I tested the setup using a 
<a href="https://www.milwaukeetool.com.au/power-tools/metalworking/angle-grinders/AGV15-125XE.html" 
title="Milwaukee AGV15-125XE angle grinder" target="_blank">Milwaukee AGV15-125XE angle 
grinder</a>, but it wouldn't start. It turns out that model has a <strong>built-in startup 
protection feature</strong>, which prevents it from being externally switched on. So, the wood router I eventually choose must <em>not</em> have this feature.

<a id="to-mesa-7i96s"></a>
⓷ <strong>Wiring the Contactor to the Mesa 7I96S Controller Card</strong>

After some extensive research (with help from AI!), I put together the following wiring diagram: 

{% include image-gallery.html list=page.gallery-image-list-3 %}
<br/>

🙏 <strong>Note</strong>: For simplicity, I’ve omitted the load wiring in this diagram. It’s assumed that the load 
circuit is still present and connected as shown in the <a href="#single-phase-load">previous</a> illustrations.

I also submitted this wiring to the 
<a href="https://forum.linuxcnc.org/27-driver-boards/56451-please-help-mesa-7i96s-24vdc-contactor-wiring" 
title="Please help -- Mesa 7I96S 24VDC Contactor Wiring" target="_blank">LinuxCNC forum</a>  
for feedback, and it was confirmed to be correct.

<a id="24vdc-psu"></a>
❹ <strong>24VDC Power Supply Unit (PSU)</strong>

To power the contactor, I’m using the 
<a href="https://au.mouser.com/ProductDetail/MEAN-WELL/MDR-100-24?qs=TaOZSEYtRiUHDfSuqlnTDA%3D%3D" 
title=" MEAN WELL MDR-100-24" target="_blank">MEAN WELL MDR-100-24</a> PSU. This unit also 
supplies power to the <strong>proximity switches</strong>. I’ve verified that it can deliver enough current for both the contactor and the switches.

<em>(I’ve already wired two proximity switches for the X-axis and successfully tested them with the LinuxCNC application, though I haven’t documented that part yet.)</em>

<a id="hal-config"></a>
❺ <strong>HAL (Hardware Abstraction Layer) Configuration</strong>

In the main <code>.hal</code> file, add the following configuration lines:

```
net router-enable    <=   spindle.0.on
net router-enable    =>   hm2_7i96s.0.ssr.00.out-00
```

It took me several failed attempts before I got this working. The following command helped verify the signal:

```
$ halcmd show pin | grep spindle
```

This lists <code>spindle.0.on</code> among other entries.

As for the <code>ssr</code> and the <code>out-00</code> components in 
<code>hm2_7i96s.0.ssr.00.out-00</code>, I figured those out with help from this 
<a href="https://forum.linuxcnc.org/27-driver-boards/46554-led-control-through-7i96s-board#248897" 
title="LED control through 7i96S board" target="_blank">LinuxCNC forum discussion</a>. 
I understand that this isn’t a complete configuration—it's just enough to test the initial wiring setup.

<a id="test-gcode-file"></a>
❻ <strong>Test Using a G-code File and Video Demonstration of Load Switching</strong>

G-code files typically use the <code>.ngc</code> extension and can be created using a standard text editor. The test file below is quite simple:

```
M3 S1000  ; Enable spindle
G4 P10    ; Wait 10 seconds
M5        ; Stop spindle
M2
```

This sequence turns on the contactor coil (you should hear a click), then waits 10 seconds. 
During this time, once the coil is energised, the load—currently a <strong>Dremel 
grinder</strong>—should begin running. After 10 seconds, the contactor switches off, 
producing another click as it returns to its <strong>normally open</strong> state, 
and the grinder should stop.

🎥 The full video runs for about 7.5 minutes. The link below is intended to jump directly to the section (~2 minutes long) where the <strong>LinuxCNC application starts</strong> and the <strong>Dremel grinder is switched on</strong>:

[![Watch the video](https://img.youtube.com/vi/4JgLWe4BxMs/maxresdefault.jpg)](https://youtu.be/4JgLWe4BxMs&t=290s)

<a id="concluding-remarks"></a>
❼ I only recently learned how to work with the contactor, and I’m excited that I’ve successfully gotten it to operate—hence this post!  

As mentioned earlier, I’ve also figured out the basics of how the proximity switches work (at least at this early stage), and I still need to document that part.  

One thing I haven’t covered yet is that I’ve also completed the <strong>main power distribution wiring</strong>, which includes the <strong>main switch</strong>, <strong>emergency stop button</strong>, and other essential components. I’ll need to write that up as well.

If you happen to read this post, thank you for your time, and I hope I did not waste it. Stay safe, as always.

✿✿✿

Feature image source:

<ul>
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
