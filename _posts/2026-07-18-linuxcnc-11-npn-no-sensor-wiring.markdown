---
layout: post
title: "Raspberry Pi 4B LinuxCNC: Wiring and “Configuring” Eight NPN Normally Open Inductive Proximity Sensors to the Mesa 7I96S Card"

description: This post describes how to wire eight NPN NO (Normally Open) inductive proximity sensors to the Mesa 7I96S card. The title and the wiring diagram refer to eight sensors, but I wired, configured, and tested only one. I originally bought eight sensors, but unfortunately managed to fry one, leaving seven available for future use. Again, this is not intended to be a tutorial, but rather a record of my learning progression. 

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
- NPN NO
- proximity
- sensor
- switch
---

<em>
This post describes how to wire eight NPN NO (Normally Open) inductive proximity sensors to the <a href="https://store.mesanet.com/index.php?route=product/product&product_id=374" title="7I96S STEP/IO card" target="_blank">Mesa 7I96S card</a>. The title and the wiring diagram refer to eight sensors, but I wired, configured, and tested only one. I originally bought eight sensors, but unfortunately managed to fry one, leaving seven available for future use. Again, this is not intended to be a tutorial, but rather a record of my learning progression.
</em>

<h3>
🐧 <a href="https://github.com/behai-nguyen/linuxcnc" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![168-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/07/168-feature-image.png) |
|:--:|
| *Raspberry Pi 4B LinuxCNC: Wiring and “Configuring” Eight NPN Normally Open Inductive Proximity Sensors to the Mesa 7I96S Card* |

<div style="background-color:yellow;width:100%;height:330px;margin-bottom:20px;">
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

<a id="published-video"></a>
This post is a supplement to a 30-second YouTube video that was published
on 5 March 2025:

<p>
<a href="https://www.youtube.com/watch?v=c-TEveXS3VI" target="_blank" 
title="LinuxCNC 2.9.4 HalShow, Raspberry Pi 4 Model B, Mesa 7I96S, NPN NO Inductive Proximity Sensor">
<img src="https://img.youtube.com/vi/c-TEveXS3VI/maxresdefault.jpg" 
alt="LinuxCNC 2.9.4 HalShow, Raspberry Pi 4 Model B, Mesa 7I96S, NPN NO Inductive Proximity Sensor">
</a>
</p>

As I mentioned in a previous post, one of my objectives for this project is
to document the various wiring configurations I have learned, so that if
someone happens to be building a similar setup, it will hopefully give them
a good head start. This post was written for completeness rather than to
present anything new beyond the existing video.

<a id="research-refs"></a>
❶ As with most other electronics topics, proximity switches were completely 
new to me. I spent a considerable amount of time researching the terminology 
and the different types of switches.

💡 First, the relevant documentation from the 
<a href="http://www.mesanet.com/pdf/parallel/7i96sman.pdf" 
title="Mesa 7I96S manual" target="_blank">Mesa 7I96S Manual</a>—
<strong>page 14</strong> states:

> For PNP type sensors or switches with a common positive, the input common pin is grounded and the sensor or switch applies a positive voltage to the input pin to activate the input.
> 
> For NPN type sensors or switches with a common ground, the input common is connected to +5 to +36V and the input pins are grounded to activate an input.

The following are some of the YouTube videos I watched to learn about switches:

<ol>
<li style="margin-top:10px;">
🎥 <a href="https://www.youtube.com/watch?v=75tAJ4tdBgs" 
title="How to build a spaceship with a Mesa 7i76e ethernet card - a tutorial for new Linuxcnc users" 
target="_blank">How to build a spaceship with a Mesa 7i76e ethernet card - a tutorial for new Linuxcnc users</a>
37:20 -- PNP Proximity sensor
</li>

<li style="margin-top:10px;">
🎥 <a href="https://www.youtube.com/watch?v=qHayhQMC9xo" 
title="NPN Sensor Explained | Working, Wiring, and Testing" 
target="_blank">NPN Sensor Explained | Working, Wiring, and Testing</a>
</li>

<li style="margin-top:10px;">
🎥 <a href="https://www.youtube.com/watch?v=zYdKN0jaxLs" 
title="Inductive Sensors - PNP vs NPN - N.O. vs N.C. - Datalogic" 
target="_blank">Inductive Sensors - PNP vs NPN - N.O. vs N.C. - Datalogic</a>
</li>

<li style="margin-top:10px;">
🎥 <a href="https://www.youtube.com/watch?v=7CUj3ZE88FQ" 
title="NPN Inductive Proximity sensor. PNP Inductive proximity switch. PNP NPN proximity sensor Animation." 
target="_blank">NPN Inductive Proximity sensor. PNP Inductive proximity switch. PNP NPN proximity sensor Animation.</a>
</li>

<li style="margin-top:10px;">
🎥 <a href="https://www.youtube.com/watch?v=aJc9C1F4uSo" 
title="What is PNP Sensor? Working, Wiring and Testing" 
target="_blank">What is PNP Sensor? Working, Wiring and Testing</a>
</li>

<li style="margin-top:10px;">
🎥 <a href="https://www.youtube.com/watch?v=BxjsZW4aLhQ" 
title="How to identify proximity switches NPN and PNP" 
target="_blank">How to identify proximity switches NPN and PNP</a>
</li>

<li style="margin-top:10px;">
🎥 <a href="https://www.youtube.com/watch?v=y-wkzgZE7zc" 
title="3 Wire PNP & NPN Sensor wiring | Sensor Connection Diagram ‪@TheElectricalGuy‬" 
target="_blank">3 Wire PNP & NPN Sensor wiring | Sensor Connection Diagram ‪@TheElectricalGuy‬</a>
</li>

<li style="margin-top:10px;">
🎥 <a href="https://www.youtube.com/watch?v=iLWCZfuY65A" 
title="Proximity Switch - Introduction, Wiring and Testing" 
target="_blank">Proximity Switch - Introduction, Wiring and Testing</a>
</li>

<li style="margin-top:10px;">
🎥 <a href="https://www.youtube.com/watch?v=jnha4hQYt38" 
title="Frankenlab CNC #13 - Sensors and Switches" 
target="_blank">Frankenlab CNC #13 - Sensors and Switches</a>
</li>
</ol>

The following are LinuxCNC forum discussions that I read while learning about the wiring:

<ol>
<li style="margin-top:10px;">
<a href="https://forum.linuxcnc.org/38-general-linuxcnc-questions/51758-mesa-7i96s-limit-switches-and-homing-switches" 
title="Mesa 7i96s limit switches and homing switches" 
target="_blank">Mesa 7i96s limit switches and homing switches</a>
</li>

<li style="margin-top:10px;">
<a href="https://www.forum.linuxcnc.org/27-driver-boards/27877-mesa-cards-and-inductive-proximity-switches" 
title="Mesa Cards and Inductive Proximity Switches" 
target="_blank">Mesa Cards and Inductive Proximity Switches</a>
</li>

<li style="margin-top:10px;">
<a href="https://forum.linuxcnc.org/27-driver-boards/53080-7i96s-npn-nc-proximity-sensors-and-npn-no-3d-probe" 
title="7i96S - NPN-NC Proximity Sensors and NPN-NO 3D Probe" 
target="_blank">7i96S - NPN-NC Proximity Sensors and NPN-NO 3D Probe</a>
</li>

<li style="margin-top:10px;">
<a href="https://forum.linuxcnc.org/49-basic-configuration/39239-home-limit-advice-please" 
title="Home/Limit advice, please" target="_blank">Home/Limit advice, please</a>
</li>

<li style="margin-top:10px;">
<a href="https://forum.linuxcnc.org/49-basic-configuration/45098-help-with-limits-and-switch-configuration-and-homing" 
title="Help with Limits and Switch Configuration and Homing" 
target="_blank">Help with Limits and Switch Configuration and Homing</a>
</li>

<li style="margin-top:10px;">
<a href="https://forum.linuxcnc.org/49-basic-configuration/49840-homing-with-limit-switches" 
title="Homing with limit switches" target="_blank">Homing with limit switches</a>
</li>
</ol>

🙏 I also have a friend who is a professional electronics engineer. He has 
patiently answered many of my questions and drawn numerous diagrams explaining 
the internal operation of various components, including the proximity switches. 
I am very grateful for his help.

Based on what I learned from the references listed above, together with the 
official LinuxCNC documentation 
<a href="https://linuxcnc.org/docs/html/config/ini-homing.html" 
title="Homing Configuration" target="_blank">Homing Configuration</a>, 
I decided on the following approach for my machine:

<ol>
<li style="margin-top:10px;">
Two switches for each axis.
</li>

<li style="margin-top:10px;">
I plan to have four axes: <code>X</code>, <code>Y</code>, 
<code>Y-tandem</code> and <code>Z</code>, which is why I bought eight switches. 
I am also aware that some machines successfully use only four switches.
</li>
</ol>

<a id="implemented"></a>
❷ I began this work by asking for help in the following LinuxCNC forum discussion:
<a href="https://forum.linuxcnc.org/27-driver-boards/55423-mesa-7i96s-and-proximity-switches"
title="Mesa 7I96S and Proximity Switches" target="_blank">Mesa 7I96S and Proximity Switches</a>.

The diagram below is the one I submitted to the forum for approval:

<a id="impl-initial"></a>

![8-npn-no-switches-to-mesa-7i96s.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/02/8-npn-no-switches-to-mesa-7i96s.png)

The proposed wiring was approved by members of the Mesa support team on the
LinuxCNC forum. I then wired the first switch and configured it as the positive
limit switch for the <code>X</code> axis. I also documented the process in the
YouTube video <a href="#published-video">mentioned earlier</a>.

<a id="impl-8-switches"></a>
The diagram below shows my intended wiring for all eight switches:

![8-npn-no-switches-to-mesa-7i96s-01.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/07/8-npn-no-switches-to-mesa-7i96s-01.png)

<strong>💥 Please note that, although the diagram shows all eight switches, I have
wired and tested only one.</strong> The components are currently laid out on a
coffee table, so the wiring is a little untidy.

<a id="24vdc-psu"></a>
❸ As described in an earlier
<a href="https://behainguyen.wordpress.com/2025/07/01/raspberry-pi-4b-linuxcnc-wiring-the-mesa-7i96s-card-and-a-contactor-to-control-a-grinder-router-via-the-linuxcnc-application/#24vdc-psu"
title="Raspberry Pi 4B LinuxCNC: Wiring the Mesa 7I96S Card and a Contactor to Control a Grinder/Router via the LinuxCNC Application"
target="_blank">article</a>, I am using the
<a href="https://au.mouser.com/ProductDetail/MEAN-WELL/MDR-100-24?qs=TaOZSEYtRiUHDfSuqlnTDA%3D%3D"
title="MEAN WELL MDR-100-24" target="_blank">MEAN WELL MDR-100-24</a> PSU to power
the proximity switches. This PSU also supplies power to the contactor coil. I
have verified that it can provide sufficient current for both the contactor coil
and the proximity switches.

<a id="the-switches"></a>
❹ I sourced the switches and the mounting brackets from a local supplier. 
(I have no affiliation with the supplier.)

<ul>
<li style="margin-top:10px;">
<a href="https://www.makerstore.com.au/product/brac-lj12-90/" 
title="LJ12 Angle Mounting Bracket" target="_blank">LJ12 Angle Mounting Bracket</a>
</li>

<li style="margin-top:10px;">
<a href="https://www.makerstore.com.au/product/elec-lj2a3/" 
title="Inductive Proximity Sensor – LJ12A3-4-Z/BX" target="_blank">Inductive Proximity Sensor – LJ12A3-4-Z/BX</a>
<p>
Specifications:
</p>

    <ul>
	<li style="margin-top:10px;">
    Model: LJ12A3-4-Z/BX
	</li>
	<li style="margin-top:10px;">
    Output Type: NPN NO (Normally Open)
	</li>
	<li style="margin-top:10px;">
    Detecting Distance: 4mm±10%
	</li>
	<li style="margin-top:10px;">
    Theory: Inductive Sensor
	</li>
	<li style="margin-top:10px;">
    Wire Type: 3 Wire Type (Brown, Blue, Black)
	</li>
	<li style="margin-top:10px;">
    Switch Appearance Type: Block Type, Aluminum Shell (it is actually “cylindrical threaded inductive proximity sensor”.)
	</li>
	<li style="margin-top:10px;">
    Supply Voltage: DC 6-36V
	</li>
	<li style="margin-top:10px;">
    Current: 300mA
	</li>
	<li style="margin-top:10px;">
    Detect Object: Iron
	</li>
	<li style="margin-top:10px;">
    Diameter: 12mm
	</li>
	<li style="margin-top:10px;">
    Cable Length: 1M/3.3Ft
	</li>
    </ul>
<p>
My temporary wiring works, but it is not intended to be the final installation.
I understand I should use shielded wires such as 
<a href="https://www.makerstore.com.au/product/elec-cable-3s-705/" 
title="Shielded 3 Core Cable 7/0.5" target="_blank">this one</a> to connect the 
switches to both the Mesa 7I96S and the 24 VDC power supply.
</p>

<p>
The three wires (brown, blue, and black) on the sensors are quite small and appear fragile. 
I have not yet worked out the best way to connect them to the shielded cable. This is 
something I still need to resolve before completing the final wiring.
</p>
</li>
</ul>

<a id="configuration"></a>
❺ To get LinuxCNC to recognise the single wired switch, use the Mesa
Configuration Wizard,
<a href="https://linuxcnc.org/docs/html/config/pncconf.html"
title="Mesa Configuration Wizard" target="_blank">PnCconf</a>.
In the <code>TB3</code> tab, select <code>X Maximum Limit</code> for the first
<code>INM</code> input entry. This switch is connected to the <code>IN0</code>
input on the <code>TB3</code> isolated input terminal block, as
<a href="#impl-8-switches">illustrated</a>. This <code>TB3</code> tab is shown
in the screenshot below:

![168-01-pncconf-tb3.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/07/168-01-pncconf-tb3.png)

I need to refresh my memory, but I believe the following entries are created in
the main
<a href="https://github.com/behai-nguyen/linuxcnc/blob/3528d0c20023a9f9e75ee180ef65d5cbd8c57592/linuxcnc/configs/Test_XYZ/Test_XYZ.hal#L80-L84"
title="Test_XYZ/Test_XYZ.hal" target="_blank"><code>Test_XYZ/Test_XYZ.hal</code></a>
file:

<figure class="highlight"><pre><code class="language-text" data-lang="text"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">80
81
82
83
84
</pre></td><td class="code"><pre># ---setup home / limit switch signals---

net x-home-sw     =&gt;  joint.0.home-sw-in
net x-neg-limit     =&gt;  joint.0.neg-lim-sw-in
net x-pos-limit     =&gt;  joint.0.pos-lim-sw-in
</pre></td></tr></tbody></table></code></pre></figure>

Every time we run
<a href="https://linuxcnc.org/docs/html/config/pncconf.html"
title="Mesa Configuration Wizard" target="_blank">PnCconf</a> and save the
configuration, manually added entries in the generated main <code>.hal</code>
file may be overwritten. They should not be relied upon for permanent custom
changes. Manually added HAL entries should be placed in the
<code>custom.hal</code> file.

<a id="test-max-x-switch-linuxcnc"></a>
❻ To test the switch, launch LinuxCNC, enable the machine, and move a metal
object towards the blue sensing end of the switch. When it is close enough, the
light on the switch will turn on.

<a id="test-max-x-switch-halshow"></a>
❼ We can also monitor the internal HAL signals using the
<code>halshow</code> CLI.
<strong>💡 LinuxCNC must be running in order for <code>halshow</code> to access
internal <code>Components</code>, <code>Pins</code>, <code>Parameters</code>,
<code>Signals</code>, etc.</strong>

In a <code>Terminal</code> window, type <code>halshow</code> and press Enter.
A screen similar to the screenshot below will appear:

![168-02-halshow-start.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/07/168-02-halshow-start.png)

Locate <code>max-x</code> under <code>Signals</code>, as illustrated below:

![168-03-halshow-max-x-signal.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/07/168-03-halshow-max-x-signal.png)

Click <code>max-x</code> to add it to the <code>WATCH</code> list on the
right-hand side:

![168-04-halshow-max-x-selected.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/07/168-04-halshow-max-x-selected.png)

Move a metal object closer to the blue sensing end. When it is close enough,
the light on the switch will turn on, and the <code>max-x</code> entry in the
<code>WATCH</code> list will turn yellow, as illustrated in the screenshot below:

![168-05-halshow-max-x-activated.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/07/168-05-halshow-max-x-activated.png)

💥 This is as far as I have managed to understand the switches at this stage.
I understand that I will need to do more study to get them working properly
once I have a complete machine. The reason I am confident in the wiring of all
eight switches is, as mentioned <a href="#impl-initial">earlier</a>, my initial
diagram submitted to the LinuxCNC forum. That diagram specifies eight switches,
and it was confirmed as correct by the Mesa support team on the LinuxCNC forum.

The remaining seven switches should follow the same wiring and configuration pattern; however, they will be fully verified once the machine is assembled.

<a id="concluding-remarks"></a>
❽ I hope this article contains some useful information. It is merely
documentation of the work I have done, so that I can refer back to it whenever
I need to refresh my memory.

Thank you for reading. I hope you find this record of my learning process
helpful for your own setups. Take care and stay safe!

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