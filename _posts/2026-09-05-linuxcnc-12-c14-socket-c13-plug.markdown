---
layout: post
title: "Raspberry Pi 4B LinuxCNC: Wiring a Fused and Switched 10 A IEC C14 Male Socket, Emergency Stop and 10 A IEC C13 Female Line Plug"

description: I have recently learned that we can use a fused and switched 10 A IEC C14 male socket and a 10 A IEC C13 female line plug to bring mains AC power into the control box. This simplifies the wiring quite a bit. It also makes the emergency stop a completely independent component. I had some minor difficulties while learning how to wire these new components. This article is not a tutorial; I am documenting my learning process, assisted by ChatGPT, to arrive at the final correct wiring. 

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2026/09/169-c13-female-plug-01.jpg"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2026/09/169-c13-female-plug-02.jpg"

tags:
- Raspberry
- 4B
- Pi4
- LinuxCNC
- Mesa 7I96S
- 7I96S
- Motion Control
- Main Power Distribution
- Power Supply Unit
- UHP-750-36
- MDR-100-24
- MDR-10-5
- NPN NO
- 10A IEC C14
- 10A IEC C13
---

<em>
I have recently learned that we can use a fused and switched 10 A IEC C14 male socket and a 10 A IEC C13 female line plug to bring mains AC power into the control box. This simplifies the wiring quite a bit. It also makes the emergency stop a completely independent component. I had some minor difficulties while learning how to wire these new components. This article is not a tutorial; I am documenting my learning process, assisted by <a href="https://chat.chatbot.app/?model=4o-mini" title="ChatGPT" target="_blank">ChatGPT</a>, to arrive at the final correct wiring.
</em>

<h3>
🐧 <a href="https://github.com/behai-nguyen/linuxcnc" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![169-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/09/169-feature-image.png) |
|:--:|
| *Raspberry Pi 4B LinuxCNC: Wiring a Fused and Switched 10 A IEC C14 Male Socket, Emergency Stop and 10 A IEC C13 Female Line Plug* |

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

<a id="preface"></a>
💡 These new components are part of the main power wiring discussed in the article 
<a href="https://behainguyen.wordpress.com/2025/09/04/raspberry-pi-4b-linuxcnc-main-power-distribution-wiring/" 
title="Raspberry Pi 4B LinuxCNC: Main Power Distribution (Wiring)" target="_blank">Raspberry 
Pi 4B LinuxCNC: Main Power Distribution (Wiring)</a>. They replace the 
<a href="https://behainguyen.wordpress.com/2025/09/04/raspberry-pi-4b-linuxcnc-main-power-distribution-wiring/#main-switch" 
title="Raspberry Pi 4B LinuxCNC: Main Power Distribution (Wiring)" target="_blank">Main 
Switch</a> and 
<a href="https://behainguyen.wordpress.com/2025/09/04/raspberry-pi-4b-linuxcnc-main-power-distribution-wiring/#din-rail-terminals-main-fuse" 
title="Raspberry Pi 4B LinuxCNC: Main Power Distribution (Wiring)" target="_blank">
6.3 A 5 × 20 mm (M205) 250 V Fuse Holder</a> discussed in that article. This article 
updates the original article. Having a separate article makes it much more convenient 
to cover the new components in detail. After this article is published, the original 
article will be updated to reference it as an update.

<a id="components"></a>
❶ <strong>The Emergency Stop Button, C14 Male Socket, and C13 Female Line Plug</strong>

<a id="estop-comp"></a>
⓵ The emergency stop button is the same one as discussed in the 
<a href="https://behainguyen.wordpress.com/2025/09/04/raspberry-pi-4b-linuxcnc-main-power-distribution-wiring/#estop" 
title="Raspberry Pi 4B LinuxCNC: Main Power Distribution (Wiring)" target="_blank">
article</a>: <a href="https://www.ebay.com.au/itm/395284988266" 
title="Push Buttons Switch 1NO + 1NC e-stop Push Button AU Emergency Stop Shut Off" 
target="_blank">Push Buttons Switch 1NO + 1NC e-stop Push Button AU Emergency Stop Shut Off</a> 
— it provides one Normally Open (NO) and one Normally Closed (NC) contact. 

<a id="c14-male-socket-comp"></a>
⓶ I bought the C14 male socket locally, in store: 
<a href="https://www.altronics.com.au/product/p8341-c14-male-socket-chassis-snap-in-fused-switched-10a-iec" 
title="C14 Male Socket Chassis Snap-In Fused Switched 10A IEC" target="_blank">C14 Male 
Socket Chassis Snap-In Fused Switched 10A IEC</a>. <a href="https://chat.chatbot.app/?model=4o-mini" title="ChatGPT" target="_blank">ChatGPT</a> 
suggested that I should confirm with the vendor that the fuse is in the Live/Active 
conductor, which the vendor support team confirmed via email.

Using this panel-mounted socket means that the control box no longer needs to have the 
emergency stop and the main switch permanently attached, as 
<a href="https://behainguyen.wordpress.com/2025/09/04/raspberry-pi-4b-linuxcnc-main-power-distribution-wiring/#first-attempt" 
title="Raspberry Pi 4B LinuxCNC: Main Power Distribution (Wiring)" target="_blank">
previously discussed</a>.

<a id="c13-female-plug-comp"></a>
⓷ I also bought the C13 female line plug at the same time, locally and in store:
<a href="https://www.altronics.com.au/product/p8310b-10a-iec-c13-line-plug-and-socket" 
title="C13 Female Line Mains Plug 10A IEC" target="_blank">C13 Female Line Mains Plug 10A IEC</a>.

<a id="wirings"></a>
❷ <strong>Wirings</strong>

<a id="c14-male-socket-wiring"></a>
⓵ Let's start with  
<a href="https://www.altronics.com.au/product/p8341-c14-male-socket-chassis-snap-in-fused-switched-10a-iec" 
title="C14 Male Socket Chassis Snap-In Fused Switched 10A IEC" target="_blank">C14 Male 
Socket Chassis Snap-In Fused Switched 10A IEC</a> — there are quite a few similar components 
that offer the same functionality. Apart from recognising that it is similar to the PC power 
supply socket, I know nothing about it. I watched the following YouTube videos to learn more:

<ol>
<li style="margin-top:10px;">
<a href="https://www.youtube.com/watch?v=kCohDhPZy0g" 
title="Wire an IEC 320 C14 Power Socket with LED Rocker Switch - Arcade Build Series" 
target="_blank">Wire an IEC 320 C14 Power Socket with LED Rocker Switch - Arcade Build Series</a>
</li>

<li style="margin-top:10px;">
<a href="https://www.youtube.com/watch?v=EAqq9vSmh-E" 
title="IEC jack and a separate switch" 
target="_blank">IEC jack and a separate switch</a>
</li>

<li style="margin-top:10px;">
<a href="https://www.youtube.com/watch?v=AUYqMc07xV0" 
title="How to connect 3 Pin IEC320 C14 power adapter"
target="_blank">How to connect 3 Pin IEC320 C14 power adapter</a>
</li>
</ol>

From the videos it was not clear which pair of the switch terminals is used for 
the Live and Neutral conductors: the top and bottom pairs, or the left and right pairs? 
<a href="https://chat.chatbot.app/?model=4o-mini" title="ChatGPT" target="_blank">ChatGPT</a> 
systematically suggested using a multimetre to test continuity between the switch 
terminals. I marked the 7 (seven) terminals as shown in the image below:

![169-c14-male-socket-01.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/09/169-c14-male-socket-01.png)

The <strong>Earth</strong> and <strong>Neutral</strong> terminals are clearly marked 
on the case; it follows that the remaining terminal is the <strong>Live</strong> 
terminal. <strong>The continuity tests were carried out without the fuse installed.</strong>

<ol>
<li style="margin-top:10px;">
<strong>The switch is OFF</strong>: there is no continuity between any of the 
<strong>T1</strong>, <strong>T2</strong>, <strong>T3</strong> and <strong>T4</strong> 
terminals. This is to be expected.
</li>

<li style="margin-top:10px;">
<strong>The switch is ON</strong>: there is continuity between <strong>T1</strong> 
and <strong>T3</strong>, and between <strong>T2</strong> and <strong>T4</strong>. That is, 
<strong>T1 ➜ T3</strong> is <strong>pole 1</strong>, and <strong>T2 ➜ T4</strong> 
is <strong>pole 2</strong>.
</li>
</ol>

I choose to use <strong>pole 1</strong> for <strong>Live</strong>, and 
<strong>pole 2</strong> for <strong>Neutral</strong>. The final wiring 
is illustrated in the image below:

![169-c14-male-socket-02.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/09/169-c14-male-socket-02.png)

<a id="c14-male-socket-fuse-holder"></a>
💡 Please note that the fuse holder has two slots. <strong>The fuse must be 
installed in the back (inner) slot. I found that I needed to push the holder back 
in firmly to close and lock it.</strong> When properly closed, the holder should stay 
flush and will not open when the switch is turned upside down. The front 
(outer) slot is for a spare fuse.

<a id="c13-female-plug-wiring"></a>
⓶ Wiring the <a href="https://www.altronics.com.au/product/p8310b-10a-iec-c13-line-plug-and-socket" 
title="C13 Female Line Mains Plug 10A IEC" target="_blank">C13 Female Line Mains Plug 10A IEC</a> 
is relatively simple: we wire it to the end of the main output cable coming off the 
emergency stop. As 
<a href="https://behainguyen.wordpress.com/2025/09/04/raspberry-pi-4b-linuxcnc-main-power-distribution-wiring/#first-attempt" 
title="Raspberry Pi 4B LinuxCNC: Main Power Distribution (Wiring)" target="_blank">
previously discussed</a>, the emergency stop output main cable is connected to the 
main switch — the C13 female plug replaces the main switch.

After unbolting the C13 female plug and taking off the upper lid, I found three (3) screw 
terminals, with <strong>L</strong>, <strong>E</strong> and <strong>N</strong> printed next 
to the corresponding terminal slots. We need to use crimp ring connectors on each of the 
emergency stop output main cable's <strong>Live</strong>, <strong>Earth</strong> and 
<strong>Neutral</strong> wires, then screw the wires onto the corresponding terminals.

Making these three connections can be quite fiddly. I found that the crimp ring connectors 
are a bit too long for this plug. I had to trim off the plastic ends of the connectors so 
that they could be fitted within the C13 casing. Once I had the unit on hand, I figured 
out how to do this. The photos below show the complete wiring of the emergency stop and 
the C13 plug:

{% include image-gallery.html list=page.gallery-image-list %}
<br>

💡 We should now have continuity on all three conductors from the AC plug end to the C13 
plug end. Set the multimetre to <code>Continuity</code>. Place one probe on one of the 
AC inlet plug prongs (pins), and place the other probe on the corresponding C13 plug 
terminal. There should be continuity. Repeat the test for the other two conductors. 
If any of the conductors fails the continuity test, we should recheck the connection 
to ensure that there is proper electrical contact.

<a id="independent-tests"></a>
❸ <strong>Independent Tests</strong>

The final wiring arrangement looks like the image below:

![169-final-wiring-01.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/09/169-final-wiring-01.png)

💥 <span style="color:red;font-weight:bold;">Do not connect the emergency stop to 
the AC main power inlet just yet.</span>

💡 I installed a 6.3A fuse in the C14's fuse holder <a href="#c14-male-socket-fuse-holder">
as described</a>. <span style="color:blue;font-weight:bold;">Plug the C13 mains plug into the C14 
socket.</span> We should now have continuity on all three conductors from the AC plug 
end to the corresponding C14 <strong>Earth Load</strong>, <strong>Neutral Load</strong> 
and <strong>Live Load</strong> wires. We should carry out continuity tests. If any of the 
conductors fails the test, we must fix it before going to the next step.

To independently test this wiring, I temporarily connected the C14's 
<strong>Earth Load</strong>, <strong>Neutral Load</strong> and <strong>Live Load</strong> 
to a 
<a href="https://behainguyen.wordpress.com/wp-content/uploads/2026/09/female-cord-extension-socket.png" 
title="Female Cord Extension Socket" target="_blank">Female Cord Extension Socket</a>, 
so that I could connect real appliances for testing.

🙏 <span style="color:blue;font-weight:bold;">We should now connect the emergency stop to 
the AC main power inlet.</span>

<ol>
<li style="margin-top:10px;">
I first tested it using my 15+ year-old Dremel; its plug has only two pins. The C14's switch 
and the emergency stop button behaved as expected.
</li>

<li style="margin-top:10px;">
I then tested it using my 30+ year-old Black &amp; Decker drill; its plug is a 
three-pin plug. Again, the C14's switch and the emergency stop button behaved 
as expected.
</li>
</ol>

It appears that the wiring is correct and that it works as intended. The next step is 
to connect it to the DIN rail blocks.

<a id="cnc-connection"></a>
❹ <strong>Replacing the Main Switch and Fuse Holder</strong>

As mentioned at the <a href="#preface">outset</a>, the C14 socket replaces the 
main switch and fuse holder. The change is simple: the C14's <strong>Earth Load</strong>, 
<strong>Neutral Load</strong> and <strong>Live Load</strong> wires are connected 
to the corresponding DIN rail blocks in place of the main switch output wires. It 
was almost a drop-in replacement. This wiring update is illustrated in the diagram 
below:

![main-power-wiring-third-cut.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/09/main-power-wiring-third-cut.png)

I have made a steel bracket for the C14 socket. This is made from the same steel used 
for the 3-Pin 10A flush-mount mains socket bracket, 
<a href="https://behainguyen.wordpress.com/2025/07/01/raspberry-pi-4b-linuxcnc-wiring-the-mesa-7i96s-card-and-a-contactor-to-control-a-grinder-router-via-the-linuxcnc-application/#socket-router-connection" 
title="Raspberry Pi 4B LinuxCNC: Wiring the Mesa 7I96S Card and a Contactor to Control a Grinder/Router via the LinuxCNC Application" 
target="_blank">as described</a>. The photo below shows the C14 mounted in the bracket, 
which is bolted onto a wooden temporary stand using two M4 bolts:

![169-c14-in-bracket.jpg](https://behainguyen.wordpress.com/wp-content/uploads/2026/09/169-c14-in-bracket.jpg)

The cut-out in this bracket is a touch too large. I might make another one if it proves 
to be insufficiently secure.

<a id="concluding-remarks"></a>
❺ I am quite happy with this change. Not having the bulky emergency stop and main 
switch permanently attached to the control box makes everything much more compact 
and portable.

The C14 fuse holder caught me out, I failed the Live conductor continuity test when 
at the final stage, since I installed the fuse into the spare slot, which means no 
fuse installed. This caused the fuse holder is not closed securely. I thought I have 
a faulty unit. But I remembered reading on another vendor website of a similar component 
that it has a slot for a spare fuse. It has been an interesting learning experience. 
I enjoy it.

The C14 fuse holder caught me out. I failed the Live conductor continuity test at 
the final stage because I had installed the fuse into the spare slot, which meant that 
no fuse was actually installed. This meant that the fuse holder could not be closed 
securely. I thought I had a faulty unit. But I remembered reading on another vendor's 
website that a similar component had a slot for a spare fuse. It has been an interesting 
learning experience. I enjoy it.

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