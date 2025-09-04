---
layout: post
title: "Raspberry Pi 4B LinuxCNC: Main Power Distribution (Wiring)"

description: By “main power,” I mean the wiring from the AC inlet to the three power supply units used in the LinuxCNC system I am building. In this post, I list the relevant components and share the wiring pictures.

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
---

<em>
By “main power,” I mean the wiring from the AC inlet to the three power supply units used in the LinuxCNC system I am building. In this post, I list the relevant components and share the wiring pictures.
</em>

<h3>
🐧 <a href="https://github.com/behai-nguyen/linuxcnc" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![150-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/09/150-feature-image.png) |
|:--:|
| *Raspberry Pi 4B LinuxCNC: Main Power Distribution (Wiring)* |

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

<p>
This post begins with this 
<a href="https://forum.linuxcnc.org/18-computer/55831-4-gang-1-way-switch-to-control-3-power-supplies-and-a-router-independently" 
title="Main Power Distribution" target="_blank">LinuxCNC forum thread</a>, 
where I was seeking help on the wiring. The final result presented here is based on 
suggestions from Mr. tommylight, Mr. RodW, and Mr. unknow (Rob). I am also 
fortunate to have a friend who is a professional electrical engineer, who has been 
very kind in helping me whenever I had questions. 
<a href="https://chat.chatbot.app/?model=4o-mini" 
title="ChatGPT" target="_blank">ChatGPT</a> and 
<a href="https://copilot.microsoft.com/" 
title="Copilot" target="_blank">Copilot</a> have also been essential to my learning. 
All errors and mistakes are, of course, mine.
</p>

💡 As you can see from the forum thread, I was completely clueless at the start. 
I studied a lot in order to complete this wiring. This is not a tutorial, so please do not 
treat it as one — I am simply documenting my progress for my future self.

<a id="the-three-psus"></a>
❶ <strong>The Three Power Supply Units (PSU)</strong>

<a id="mdr-10-5"></a>
⓵ <a href="https://www.power-supplies-australia.com.au/mean-well-mdr-10-5-power-supply" 
title="Mean Well MDR-10-5" target="_blank">MEAN WELL MDR-10-5</a> — This PSU powers 
the <a href="https://store.mesanet.com/index.php?route=product/product&product_id=374" 
title="7I96S STEP/IO Step & dir plus I/O card" target="_blank">7I96S STEP/IO Step & dir 
plus I/O card</a>, which we discussed in 
<a href="https://behainguyen.wordpress.com/2025/02/14/raspberry-pi-4b-linuxcnc-initial-setup-for-the-mesa-7i96s-ethernet-motion-control/" 
title="Raspberry Pi 4B LinuxCNC: Initial Setup for the Mesa 7I96S Ethernet Motion Control" 
target="_blank">this post</a>. I bought this one locally.

<a id="mdr-100-24"></a>
⓶ <a href="https://au.mouser.com/ProductDetail/MEAN-WELL/MDR-100-24?qs=TaOZSEYtRiUHDfSuqlnTDA%3D%3D" 
title="MEAN WELL MDR-100-24" target="_blank">MEAN WELL MDR-100-24</a> — This PSU powers 
a 24VDC contactor, as documented in 
<a href="https://behainguyen.wordpress.com/2025/07/01/raspberry-pi-4b-linuxcnc-wiring-the-mesa-7i96s-card-and-a-contactor-to-control-a-grinder-router-via-the-linuxcnc-application/#24vdc-psu" 
title="Raspberry Pi 4B LinuxCNC: Wiring the Mesa 7I96S Card and a Contactor to Control a Grinder/Router via the LinuxCNC Application | 24VDC Power Supply Unit (PSU)" 
target="_blank">this post</a>, as well as the <strong>proximity switches</strong>, 
which I have not covered yet. I ordered this PSU online, shipped from a warehouse in Texas, U.S.A.

<a id="uhp-750-36"></a>
⓷ <a href="https://au.mouser.com/ProductDetail/MEAN-WELL/UHP-750-36?qs=3HJ2avRr9PLre%2FdtWu%2FMgA%3D%3D&srsltid=AfmBOopJg7L_5yMSWcrgNhjI6qmmsz6-E7AJpnvY3grMpLJ29HELBwFs" 
title="MEAN WELL UHP-750-36" target="_blank">MEAN WELL UHP-750-36</a> — This PSU powers 
the four 
<a href="https://www.omc-stepperonline.com/closed-loop-stepper-driver-v4-1-0-8-0a-24-48vdc-for-nema-17-23-24-stepper-motor-cl57t-v41" 
title="CL57T Closed-Loop Stepper Driver" target="_blank">CL57T Closed-Loop Stepper 
Driver</a>s, and therefore the four 
<a href="https://www.omc-stepperonline.com/nema-23-closed-loop-stepper-motor-3-0nm-424oz-in-encoder-1000ppr-4000cpr-23hs45-4204d-e1000" 
title="Nema 23 Stepper Motor" target="_blank">Nema 23 Stepper Motor</a>s. We previously 
discussed the stepper drivers and motors in 
<a href="https://behainguyen.wordpress.com/2025/02/16/raspberry-pi-4b-linuxcnc-wiring-the-mesa-7i96s-ethernet-motion-control-closed-loop-cl57t-stepper-driver-and-nema-23-stepper-motor/" 
title="Raspberry Pi 4B LinuxCNC: Wiring the Mesa 7I96S Ethernet Motion Control, Closed-Loop CL57T Stepper Driver, and Nema 23 Stepper Motor" 
target="_blank">this post</a>. I also ordered this PSU online, again shipped from 
a warehouse in Texas, U.S.A.

At this stage, I still have only one driver and one motor; I have not purchased the other 
three yet. Let’s discuss why this PSU is suitable.

<code>UHP-750-36</code> specifications:

<ol>
<li style="margin-top:10px;">
Output Voltage (Channel 1): 36 VDC 
</li>
<li style="margin-top:10px;">
Output Power: 752.4 W
</li>
<li style="margin-top:10px;">
Input Voltage: 90–264 VAC, 127–370 VDC 
</li>
<li style="margin-top:10px;">
Output Current (Channel 1): 20.9 A 
</li>
</ol>

The <code>Nema 23</code> stepper motors require 24–48 VDC. I am in Australia, where the 
nominal AC voltage is 
<a href="https://wilken.com.au/voltage-electrical-outlets-australia/" 
title="What Is the Voltage of Electrical Outlets in Australia?" 
target="_blank">230–240 VAC</a>. Therefore, the PSU <code>input voltage</code> and 
<code>output voltage</code> are appropriate. According to this Stepper Online article: 
<a href="https://www.omc-stepperonline.com/support/how-to-choose-a-power-supply-for-my-stepper-motor" 
title="How to choose a power supply for my stepper motor?" 
target="_blank">How to choose a power supply for my stepper motor?</a>, the 
<strong>maximum power draw (P) in watts to run all four <code>Nema 23</code> 
stepper motors at full current and under full load at the same time is</strong>:

<strong><code>P = n × I × V × 1.2</code></strong>

where:

<ul>
<li style="margin-top:10px;">
<strong>n</strong>: the total number of stepper motors, here <strong>4</strong>.
</li>
<li style="margin-top:10px;">
<strong>I</strong>: the maximum current drawn by each motor, <strong>4.2 A</strong>.
</li>
<li style="margin-top:10px;">
<strong>V</strong>: the voltage required by each motor, <strong>36 VDC</strong>.
</li>
<li style="margin-top:10px;">
<strong>1.2</strong>: the “kindness factor” — a <strong>20% safety margin</strong>.
</li>
</ul>

Therefore: <strong><code>P = 4 × 4.2 × 36 × 1.2 = 725.76 W</code></strong>.

The total current draw at full load would be: <strong><code>4 × 4.2 A = 16.8 A</code></strong>.

Both the PSU <code>output power</code> and <code>output current</code> are 
appropriate. <strong>In practice, all motors running at full current and under full 
load simultaneously is rare</strong>.

<a id="emi-filter"></a>
❷ <strong>The EMI Filter</strong>

In the aforementioned LinuxCNC forum thread, 
<a href="https://forum.linuxcnc.org/18-computer/55831-4-gang-1-way-switch-to-control-3-power-supplies-and-a-router-independently#325751" 
title="Main Power Distribution" target="_blank">Mr. RodW</a> recommended this 
<a href="https://www.jaycar.com.au/240v-ac-emi-filter/p/MS4001" title="240V AC EMI Filter" 
target="_blank">240V AC EMI Filter</a>, which I was able to get from a local Jaycar store.

After a rather long learning process, I arrived at this first working wiring:

| ![emi-filter-to-psu-first-try.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/09/emi-filter-to-psu-first-try.png) |
|:--:|
| **First Wiring Attempt** |

I tested this wiring with the 
<a href="https://linuxcnc.org/docs/html/config/pncconf.html" title="Mesa Configuration 
Wizard" target="_blank">LinuxCNC PnCconf wizard</a>, and the stepper motor responded to software 
commands. I then asked my friend to review it, and he suggested a better version:

| ![emi-filter-to-psu-recommended.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/09/emi-filter-to-psu-recommended.png) |
|:--:|
| **Recommended Wiring Version** |

💡 High-wattage PSUs such as the 
<a href="https://au.mouser.com/ProductDetail/MEAN-WELL/UHP-750-36?qs=3HJ2avRr9PLre%2FdtWu%2FMgA%3D%3D&srsltid=AfmBOopJg7L_5yMSWcrgNhjI6qmmsz6-E7AJpnvY3grMpLJ29HELBwFs" 
title="MEAN WELL UHP-750-36" target="_blank">MEAN WELL UHP-750-36</a> can generate 
<a href="https://en.wikipedia.org/wiki/Electromagnetic_interference" 
title="Electromagnetic interference" target="_blank">electromagnetic interference 
(EMI) or radio frequency interference (RFI)</a>, which may affect other components — especially 
in a CNC system. An external EMI filter helps reduce this side effect. This is why only the UHP-750-36 has an external filter, while the smaller 
<a href="https://www.power-supplies-australia.com.au/mean-well-mdr-10-5-power-supply" 
title="Mean Well MDR-10-5" target="_blank">MEAN WELL MDR-10-5</a> and 
<a href="https://au.mouser.com/ProductDetail/MEAN-WELL/MDR-100-24?qs=TaOZSEYtRiUHDfSuqlnTDA%3D%3D" 
title="MEAN WELL MDR-100-24" target="_blank">MEAN WELL MDR-100-24</a> are used without one. 
All three PSUs also include internal EMI filtering, according to their block diagrams.

<a id="estop-and-main-switch"></a>
❸ <strong>The Emergency Stop Button, the Main Switch, and Their Cable Glands</strong>

<a id="estop"></a>
⓵ I had never actually seen an emergency stop button by itself before. After some 
research, I decided on this eBay model: 
<a href="https://www.ebay.com.au/itm/395284988266" 
title="Push Buttons Switch 1NO + 1NC e-stop Push Button AU Emergency Stop Shut Off" 
target="_blank">Push Buttons Switch 1NO + 1NC e-stop Push Button AU Emergency Stop Shut Off</a> 
— it provides one Normally Open (NO) and one Normally Closed (NC) contact. 

It is inexpensive, and the quality reflects the price. However, it is still usable. 
The terminals are not labelled NC or NO, but my friend helped me identify which pair 
was which.  

This Instructables article: 
<a href="https://www.instructables.com/Emergency-Stop-Button/" 
title="Emergency Stop Button" target="_blank">Emergency Stop Button</a> explains 
wiring using the NC contact. I followed those instructions successfully and tested 
the setup using a 240 VAC microwave fan. Unfortunately, I held the wires with 
alligator clips, and vibration from the fan caused a short circuit. This blew the 
main fuse and disabled about half of the outlets in my house. Luckily, with some 
guidance over the phone, I was able to reset the fuse and restore power.  
Lesson learned: never rely on loose clip connections for mains wiring.

This e-stop button came with a single cable gland. Since I also needed to secure the 
output cable, I added this 
<a href="https://www.altronics.com.au/p/h4382-11-14mm-mg20-black-ip68-ul94-cable-gland/"
title="11-14mm MG20 Black IP68 Nylon Cable Gland" target="_blank">11–14 mm MG20 Black 
IP68 Nylon Cable Gland</a>. It turned out visibly larger than the supplied one.

<a id="main-switch"></a>
⓶ For the main switch, I chose this model: 
<a href="https://directwholesale.com.au/products/clipsal-easy56-easy56-switch-1p-10a-250v-ey56sw110/" 
title="Schneider Electric Easy 56 Switch - 1P - 10A - 250V - EY56SW110" 
target="_blank">Schneider Electric Easy 56 Switch — 1P, 10A, 250V, EY56SW110</a>.  
Although the website listed the dimensions, I overlooked them and only realised 
on arrival that it is much larger than the e-stop. That said, it is very sturdy 
and well built. The lower half of the casing has one large threaded opening on one 
side and two smaller ones on the other, all sealed with caps. These are intended 
for the incoming and outgoing cables.

To secure the cables, I purchased one 
<a href="https://www.power-supplies-australia.com.au/power-source-pgland-m32-plastic-pa66-cable-gland" 
title="POWER SOURCE PGLAND-M32 Plastic PA66 Cable Gland M32 - 18-25mm IP68" 
target="_blank">POWER SOURCE PGLAND-M32 Plastic PA66 Cable Gland (18–25 mm, IP68)</a> 
and two 
<a href="https://www.power-supplies-australia.com.au/power-source-pgland-m25-plastic-pa66-cable-gland" 
title="POWER SOURCE PGLAND-M25 Plastic PA66 Cable Gland M25 - 12.5-18mm IP68" 
target="_blank">POWER SOURCE PGLAND-M25 Plastic PA66 Cable Glands (12.5–18 mm, IP68)</a> 
— even though I only needed one. Aesthetically, using one large and one small gland 
made the switch look unbalanced and somewhat awkward.

💡 None of these glands could properly grip the standard cables I used. Even when 
fully tightened, the fit was too loose. As a workaround, I shimmed the cables with 
short lengths of cut water hose. While effective, this is not ideal.

<a id="psu-mcb"></a>
❹ <strong>Miniature Circuit Breakers (MCB) for the PSUs</strong>

From what I have learned, choosing MCBs for power supplies involves two main requirements. 
First, the <strong>nominal current rating</strong> must be correct. Second, the 
<strong>tripping curve</strong> must suit the PSU’s inrush current at the input AC voltage.

For calculating the nominal current, I found the following references helpful:

<ol>
<li style="margin-top:10px;">
<a href="https://magna-power.com/learn/kb/calculating-power-supply-ac-input-current" 
title="Calculating Power Supply AC Input Current" target="_blank">Calculating Power 
Supply AC Input Current</a> — explains how to calculate the theoretical AC input 
current for a PSU:
<p>
<math xmlns="http://www.w3.org/1998/Math/MathML"><mstyle displaystyle="true"><mrow><mtext>Theoretical AC Input Current</mtext><mspace width="1ex"></mspace></mrow><mo>=</mo><mfrac><mrow><mtext>DC Output Power</mtext></mrow><mrow><mrow><mtext>Power Factor</mtext></mrow><mo>×</mo><mrow><mtext>Efficiency</mtext></mrow><mo>×</mo><mrow><mtext>AC Input Voltage</mtext></mrow></mrow></mfrac></mstyle></math>
</p>
</li>

<li style="margin-top:10px;">
<a href="https://www.allumiax.com/breaker-size-calculator" title="Breaker Size Calculator" 
target="_blank">Breaker Size Calculator</a> and 
<a href="https://www.onesto-ep.com/blog/calculate-capacity-of-circuit-breaker/" 
title="How to calculate the capacity of a circuit breaker" target="_blank">How to 
calculate the capacity of a circuit breaker</a> — both emphasise applying a 
<strong>25% safety margin</strong> when selecting the nominal current rating of an MCB.
</li>
</ol>

For the tripping curve, this article provides a clear overview:

<ul>
<li style="margin-top:10px;">
<a href="https://www.electricaltechnology.org/2021/07/tripping-curves-circuit-breaker.html" 
title="Tripping Curves of Circuit Breakers – B, C, D, K and Z Trip Curve" 
target="_blank">Tripping Curves of Circuit Breakers – B, C, D, K and Z Trip Curve</a>
</li>
</ul>

<a id="mcb-uhp-750-36"></a>
⓵ MCB for <a href="https://au.mouser.com/ProductDetail/MEAN-WELL/UHP-750-36?qs=3HJ2avRr9PLre%2FdtWu%2FMgA%3D%3D&srsltid=AfmBOopJg7L_5yMSWcrgNhjI6qmmsz6-E7AJpnvY3grMpLJ29HELBwFs" 
title="MEAN WELL UHP-750-36" target="_blank">MEAN WELL UHP-750-36</a> — The datasheet 
specifies:

<ol>
<li style="margin-top:10px;">
RATED POWER: 752.4W 
</li>
<li style="margin-top:10px;">
VOLTAGE RANGE: 90 ~ 264VAC 127 ~ 370VDC
</li>
<li style="margin-top:10px;">
POWER FACTOR (Typ.): PF≥0.95/230VAC PF≥0.98/115VAC at full load
</li>
<li style="margin-top:10px;">
EFFICIENCY (Typ.): 95% 
</li>
<li style="margin-top:10px;">
AC CURRENT (Typ.): 7.5A/115VAC 3.8A/230VAC
</li>
<li style="margin-top:10px;">
INRUSH CURRENT (Typ.): Cold start 20A @ 115VAC; 40A @ 230VAC
</li>
</ol>

Therefore:

<p>
<math xmlns="http://www.w3.org/1998/Math/MathML"><mstyle displaystyle="true"><mrow><mtext>Theoretical AC Input Current</mtext><mspace width="1ex"></mspace></mrow><mo>=</mo><mfrac><mrow><mtext>752.4</mtext></mrow><mrow><mrow><mtext>0.95</mtext></mrow><mo>×</mo><mrow><mtext>0.95</mtext></mrow><mo>×</mo><mrow><mtext>230</mtext></mrow></mrow></mfrac><mo>=</mo><mtext>3.62A</mtext></mstyle></math>
</p>

The datasheet states <strong>3.8A at 230VAC</strong>, this is steady-state current draw. 
The theoretical AC input current calculated above matches well with this value. 
<strong>3.8A</strong> is the value we should use to calculate the MCB's nominal current: 
<strong><code>3.8 × 1.25 = 4.75A</code></strong>.

The MCB for the <code>UHP-750-36</code> PSU should have the following characteristics:

● A <strong>5A</strong> or <strong>6A</strong> MCB would be most appropriate. 
Both are <strong>above the continuous draw</strong> but still tight enough to 
protect in the event of an overload or fault. 6A offers slightly better tolerance, 
especially with minor surges or long cable runs. 5A offers a stricter cutoff, but 
may trip if the PSU is run at full continuous load.

● <strong>Type C trip curve</strong> tolerates inrushes up to <strong>30A–60A</strong>, 
which safely covers the <strong>40A</strong> inrush.

● Voltage should be <strong>230VAC-240VAC</strong> to match the Australian standard.

✔️ I selected this RCBO: 
<a href="https://directwholesale.com.au/products/clipsal-max9-rcbo-1pn-c-6a-30ma-a-slim-mx9r3106/" 
title="Clipsal MAX9 RCBO 1PN C 6A 30mA A SLIM - MX9R3106" 
target="_blank">Clipsal MAX9 RCBO 1PN C 6A 30mA A SLIM - MX9R3106</a>. 
An RCBO includes a MCB. For detail explanation, refer to 
<a href="https://eshop.se.com/in/blog/post/what-is-the-difference-between-mcb-mccb-rcb-rcd-rccb-and-rcbo.html" 
title="What is the Difference between MCB, MCCB, RCB, RCD, RCCB, and RCBO?" 
target="_blank">What is the Difference between MCB, MCCB, RCB, RCD, RCCB, and RCBO?</a>
From a wiring perspective, RCBOs take both the <strong>Live</strong> and the 
<strong>Neutral</strong> wires.

<a id="mcb-mdr-10-5"></a>
⓶ MCB for <a href="https://www.power-supplies-australia.com.au/mean-well-mdr-10-5-power-supply" 
title="Mean Well MDR-10-5" target="_blank">MEAN WELL MDR-10-5</a> — The datasheet specifies: 

<ol>
<li style="margin-top:10px;">
RATED POWER: 10W
</li>
<li style="margin-top:10px;">
VOLTAGE RANGE: 85 ~ 264VAC 120 ~ 370VDC
</li>
<li style="margin-top:10px;">
POWER FACTOR (Typ.): Not specified
</li>
<li style="margin-top:10px;">
EFFICIENCY (Typ.): 77%
</li>
<li style="margin-top:10px;">
AC CURRENT (Typ.): 0.33A/115VAC 0.21A/230VAC
</li>
<li style="margin-top:10px;">
INRUSH CURRENT (Typ.): COLD START 35A/115VAC 70A/230VAC
</li>
</ol>

The <code>Power Factor</code> is not given, <code>Theoretical Average Input Current</code> 
can not be calculated, but we do not need it anyhow, since the <em>steady-state current 
draw</em> is available: <strong>0.21A at 230VAC</strong>.

The MCB for the <code>MDR-10-5</code> PSU should have the following characteristics:

● A <strong>1A</strong> or <strong>2A</strong> MCB is sufficient. 
2A provides more margin and is more tolerant of transient events. 
Due to the high inrush current (70A), nuisance tripping is possible even with 
a type C device. If that occurs, a larger MCB (for example, 6A) can be used, 
since the PSU itself has internal protection against overloads and short circuits.

● <strong>Type C trip curve</strong> would <strong>absorb inrush current</strong>
of <strong>70A</strong> without nuisance tripping.

● Voltage should be <strong>230VAC-240VAC</strong> to match the Australian standard.

✔️ I selected this MCB: 
<a href="https://directwholesale.com.au/products/clipsal-max9-mcb-1p-c-2a-6000a-mx9mc102/" 
title="Clipsal MAX9 MCB 1P C 2A 6000A - MX9MC102" target="_blank">Clipsal MAX9 MCB 1P C 
2A 6000A - MX9MC102</a>. MCBs take only the <strong>Live</strong> wire.

<a id="mcb-mdr-100-24"></a>
⓷ MCB for 
<a href="https://au.mouser.com/ProductDetail/MEAN-WELL/MDR-100-24?qs=TaOZSEYtRiUHDfSuqlnTDA%3D%3D" 
title=" MEAN WELL MDR-100-24" target="_blank">MEAN WELL MDR-100-24</a> — The datasheet 
specifies: 

<ol>
<li style="margin-top:10px;">
RATED POWER: 96W
</li>
<li style="margin-top:10px;">
VOLTAGE RANGE: 85 ~ 264VAC 120 ~ 370VDC
</li>
<li style="margin-top:10px;">
POWER FACTOR (Typ.): PF≥0.95/230VAC PF≥0.98/115VAC at full load
</li>
<li style="margin-top:10px;">
EFFICIENCY (Typ.): 86%
</li>
<li style="margin-top:10px;">
AC CURRENT (Typ.): 1.3A/115VAC 0.8A/230VAC
</li>
<li style="margin-top:10px;">
INRUSH CURRENT (Typ.): COLD START 30A/115VAC 60A/230VAC
</li>
</ol>

✔️ I selected the same 
<a href="https://directwholesale.com.au/products/clipsal-max9-mcb-1p-c-2a-6000a-mx9mc102/" 
title="Clipsal MAX9 MCB 1P C 2A 6000A - MX9MC102" target="_blank">MCB</a> as per 
<a href="#mcb-mdr-10-5">MDR-10-5</a> above. As with the MDR-10-5, the inrush 
current (60A) is much higher than the steady-state current (0.8A), so a larger 
MCB may be required in practice if nuisance tripping occurs.

<a id="din-rail"></a>
❺ <strong>DIN Rail</strong>

According to the datasheets for the 
<a href="https://www.power-supplies-australia.com.au/mean-well-mdr-10-5-power-supply" 
title="Mean Well MDR-10-5" target="_blank">MEAN WELL MDR-10-5</a> and 
<a href="https://au.mouser.com/ProductDetail/MEAN-WELL/MDR-100-24?qs=TaOZSEYtRiUHDfSuqlnTDA%3D%3D" 
title="MEAN WELL MDR-100-24" target="_blank">MEAN WELL MDR-100-24</a>:

> Can be installed on "DIN rail TS-35/7.5 or 15

I bought the <code>MDR-10-5</code> PSU from a local supplier, but they did not stock 
DIN rail in the required specification. Other local suppliers had it available, 
but only in 2-metre lengths—far more than I needed—and at a higher cost. Instead, 
I settled on a cheaper aluminium version: 
<a href="https://www.amazon.com.au/dp/B0BXWBRV8S" 
title="TEHAUX 3pcs DIN Rail Slotted, 12 inch Aluminum DIN Rail Mounting Electrical" 
target="_blank">TEHAUX 3pcs DIN Rail Slotted, 12 inch Aluminum DIN Rail Mounting Electrical</a>. 
Back on 13 April 2025, it was priced at AUD 23.89. While it does not feel as sturdy as 
the steel version, it should be perfectly adequate for the job.

<a id="din-rail-terminals"></a>
❻ <strong>DIN Rail Terminals, DIN Rail Fuse Holder and the Main Fuse</strong>

In the same LinuxCNC forum thread, 
<a href="https://forum.linuxcnc.org/18-computer/55831-4-gang-1-way-switch-to-control-3-power-supplies-and-a-router-independently#325751" 
title="Main Power Distribution" target="_blank">Mr. RodW</a> recommended using DIN rail terminals. 
I was able to source them locally: I could check them both online and in-store, which I prefer. 
Here’s what I purchased:

<ol>
<li style="margin-top:10px;">
4 × 
<a href="https://www.altronics.com.au/p/p2408-dinkle-35a-4mm-red-din-rail-terminal/" 
title="35A 4mm Red DIN Rail Terminal" target="_blank">35A 4mm Red DIN Rail Terminal</a> — 
for the <strong>Live</strong> wires. Each terminal has two connection points, so these 
four blocks together can accommodate 8 live wires.
</li>

<li style="margin-top:10px;">
4 × 
<a href="https://www.altronics.com.au/p/p2411-dinkle-35a-4mm-blue-din-rail-terminal/" 
title="35A 4mm Blue DIN Rail Terminal" target="_blank">35A 4mm Blue DIN Rail Terminal</a> — 
for the <strong>Neutral</strong> wires. Same as above, but in blue.
</li>

<li style="margin-top:10px;">
2 × 
<a href="https://www.altronics.com.au/p/p2444-4-way-insertion-bridge-for-4mm-din-rail-terminals/" 
title="4 Way Insertion Bridge For 4mm DIN Rail Terminals" target="_blank">4-Way Insertion 
Bridge for 4mm DIN Rail Terminals</a> — used to join each group of 4 terminals together. 
This leaves each group with 4 spare connection points.
</li>

<li style="margin-top:10px;">
6 × 
<a href="https://www.altronics.com.au/p/p2415-dinkle-35a-4mm-green-yellow-din-rail-terminal/" 
title="35A 4mm Green/Yellow DIN Rail Terminal" target="_blank">35A 4mm Green/Yellow DIN Rail 
Terminal</a> — for the <strong>Earth</strong> wires. Unlike the live/neutral blocks, these 
have metal clamps at the base, so the DIN rail itself acts as a natural conductor, connecting 
them all together as a common ground. Each terminal has two connection points, so technically 
I only needed three. I bought six because the salesperson didn’t know about this feature, and 
I didn’t bother returning the extras.
</li>

<li style="margin-top:10px;">
1 × 
<a href="https://www.altronics.com.au/p/p2472-dinkle-end-cap-for-din-rail-terminals/" 
title="End Cap For DIN Rail Terminals" target="_blank">End Cap for DIN Rail Terminals</a> — 
covers the last red or blue terminal block. Not strictly necessary if an Earth block follows, 
but I installed one anyway.
</li>

<li style="margin-top:10px;">
1 × 
<a href="https://www.altronics.com.au/p/p2423-dinkle-35a-4mm-grey-fused-din-rail-terminal/" 
title="35A 4mm Grey Fused DIN Rail Terminal (P2423)" target="_blank">35A 4mm Grey Fused DIN Rail Terminal (P2423)</a> — 
a fuse holder for <code>M205</code> fuses. (M205 refers to 20 mm length × 5 mm diameter.)
</li>

<li style="margin-top:10px;">
1 × 
<a href="https://www.altronics.com.au/p/p2480-dinkle-end-cap-to-suit-p2423/" 
title="End Cap To Suit P2423" target="_blank">End Cap to suit P2423</a> — 
covers the exposed side of the above fuse holder. A fuse can still be inserted with the cap on: 
simply lift the lever to pull out the carriage, insert the fuse, and push the lever back down. 
Very easy to use.
</li>

<a id="din-rail-terminals-main-fuse"></a>
<li style="margin-top:10px;">
5 × 
<a href="https://www.altronics.com.au/p/s5748-6.3a-m205-fuse/" 
title="6.3A 5x20 (M205) 250V Fuse" target="_blank">6.3A 5×20 (M205) 250V Fuse</a> — 
the store did not stock <strong>6A</strong> M205 fuses. These are also <strong>fast-blow</strong>, 
while I should really be using <strong>slow-blow</strong> (time-delay) fuses.
</li>
</ol>

💡 <strong>Why a 6A Fuse?</strong>

As described previously, the typical AC input currents for each PSU are:

<ul>
<li style="margin-top:10px;">
<a href="#mcb-mdr-10-5">MDR-10-5</a>: <strong>0.21 A</strong>
</li>
<li style="margin-top:10px;">
<a href="#mcb-mdr-100-24">MDR-100-24</a>: <strong>0.8 A</strong>
</li>
<li style="margin-top:10px;">
<a href="#mcb-uhp-750-36">UHP-750-36</a>: <strong>3.8 A</strong>
</li>
</ul>

Together, that adds up to <strong>4.81 A</strong>. Adding a <strong>25%</strong> safety margin 
brings it to about <strong>6.01 A</strong>.

<a id="first-attempt"></a>
❼ <strong>First Attempt</strong>

The image below shows my first working attempt at wiring everything together:

| ![main-power-wiring-first-cut.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/09/main-power-wiring-first-cut.png) |
|:--:|
| **First Working Attempt** |

By <em>working</em>, I mean that I tested this wiring using the 
<a href="https://linuxcnc.org/docs/html/config/pncconf.html" title="Mesa Configuration 
Wizard" target="_blank">Linux PnCconf</a>, and the stepper motor responded to software 
commands. I also asked a friend to review the setup, and he recommended adding a main fuse 
<a href="#din-rail-terminals-main-fuse">as described here</a>. The revised wiring is shown below:

| ![main-power-wiring-second-cut.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/09/main-power-wiring-second-cut.png) |
|:--:|
| **An Improved Version** |

In fact, this was the wiring in place when I tested the contactor as described in the last 
post: <a href="https://behainguyen.wordpress.com/2025/07/01/raspberry-pi-4b-linuxcnc-wiring-the-mesa-7i96s-card-and-a-contactor-to-control-a-grinder-router-via-the-linuxcnc-application/" 
title="Raspberry Pi 4B LinuxCNC: Wiring the Mesa 7I96S Card and a Contactor to Control a Grinder/Router via the LinuxCNC Application" 
target="_blank">Raspberry Pi 4B LinuxCNC: Wiring the Mesa 7I96S Card and a Contactor to Control a Grinder/Router via the LinuxCNC Application</a>.

<a id="secondary-switches"></a>
❽ <strong>Adding Secondary Switches to Control Each PSU Independently</strong>

The RCBO and MCBs previously <a href="#psu-mcb">discussed</a> each have an on/off switch, which could be used to control their respective PSUs. However, that’s not their intended purpose. I’d prefer to install dedicated switches for this function. While not strictly necessary, it would be a nice addition. I haven’t purchased the switches yet, and the wiring remains unchanged from the last image above.

This is the switch I have in mind: 
<a href="https://www.altronics.com.au/p/s3244-dpst-illuminated-neon-ip65-weatherproof-rocker-switch/" 
title="DPST 16A IP65 Weatherproof Rocker Switch" target="_blank">DPST 16A IP65 
Weatherproof Rocker Switch</a>. It’s available at a nearby store, which saves on delivery fees, and the pricing is quite reasonable. I’ve revised the previous wiring picture into four smaller, focused images.

💥 For the switch above, I’m not yet certain which terminals correspond to <strong>Live</strong> and which to <strong>Neutral</strong>. In the following images, please treat the switch connections as illustrative only—not technically precise.

| ![main-power-wiring-01.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/09/main-power-wiring-01.png) |
|:--:|
| **From AC Inlet to DIN Rail Terminal Blocks** |

The image above shows the connection from the AC inlet to the DIN rail terminal blocks, with an inset illustrating the wiring between the emergency stop and the main switch.

| ![main-power-wiring-02.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/09/main-power-wiring-02.png) |
|:--:|
| **Wiring of the <a href="https://au.mouser.com/ProductDetail/MEAN-WELL/UHP-750-36?qs=3HJ2avRr9PLre%2FdtWu%2FMgA%3D%3D&srsltid=AfmBOopJg7L_5yMSWcrgNhjI6qmmsz6-E7AJpnvY3grMpLJ29HELBwFs" title="MEAN WELL UHP-750-36" target="_blank">MEAN WELL UHP-750-36</a> PSU** |

| ![main-power-wiring-03.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/09/main-power-wiring-03.png) |
|:--:|
| **Wiring of the <a href="https://au.mouser.com/ProductDetail/MEAN-WELL/MDR-100-24?qs=TaOZSEYtRiUHDfSuqlnTDA%3D%3D" title=" MEAN WELL MDR-100-24" target="_blank">MEAN WELL MDR-100-24</a> PSU** |

| ![main-power-wiring-04.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/09/main-power-wiring-04.png) |
|:--:|
| **Wiring of the <a href="https://www.power-supplies-australia.com.au/mean-well-mdr-10-5-power-supply" title="Mean Well MDR-10-5" target="_blank">MEAN WELL MDR-10-5</a> PSU.** |

<a id="concluding-remarks"></a>
❾ It has taken me several months—though not full-time—to learn and assemble this wiring setup. I’m not yet certain how well it performs in a real-world scenario, but so far, it behaves as expected. I’ll post updates whenever there’s something meaningful to document.

Although the title of this post is “Raspberry Pi 4B LinuxCNC: Main Power Distribution (Wiring),” it should be clear that the wiring described here isn’t specific to the Raspberry Pi 4B. This same setup can be used with any computer running LinuxCNC.

If you’ve taken the time to read this post—thank you. I hope it was worth your time. Stay safe out there.

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
