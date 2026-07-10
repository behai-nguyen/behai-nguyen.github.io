---
layout: post
title: "Raspberry Pi 4B LinuxCNC: Homing to the Origin (0, 0, 0)"

description: My LinuxCNC 2.9.4 home position was set to coordinates I didn't quite understand. I am documenting the Gemini-assisted troubleshooting process I used to set it to the origin (0, 0, 0). This is not a tutorial, but rather a record of my learning progression.

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
- Home
- Origin
---

<em>
My LinuxCNC 2.9.4 home position was set to coordinates I didn't quite understand. I am documenting the Gemini-assisted troubleshooting process I used to set it to the origin <code>(0, 0, 0)</code>. This is not a tutorial, but rather a record of my learning progression.
</em>

<h3>
🐧 <a href="https://github.com/behai-nguyen/linuxcnc" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![166-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/07/166-feature-image.png) |
|:--:|
| *Raspberry Pi 4B LinuxCNC: Homing to the Origin (0, 0, 0)* |

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
<br/>

Setting the home coordinates to the origin <code>(0, 0, 0)</code> is an 
exercise in understanding LinuxCNC a bit better, rather than a definitive final setup.

In the 
<a href="https://behainguyen.wordpress.com/2026/06/29/raspberry-pi-4b-linuxcnc-mesa-7i96s-ethernet-motion-control-expanded-to-four-cl57t-drivers-and-four-nema-23-closed-loop-stepper-motors/" 
title="Raspberry Pi 4B LinuxCNC: Mesa 7I96S Ethernet Motion Control" 
target="_blank">last post</a>, which accompanies this 
<a href="https://www.youtube.com/watch?v=pEOmPJ4gfqo" 
title="Raspberry Pi 4 Model B: Mesa 7I96S YouTube Video" 
target="_blank">YouTube video</a>, I mentioned that the initial homing position 
was unexpected, as illustrated in the screenshot below:

![01-166-home-position.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/07/01-166-home-position.png)

The tool cone moved to the shown position after clicking the <code>Home All</code> 
button in the UI. 💡 Please note: the Preview screen shows a reading of 
<code>G54 X = -20.000</code>.

I am not entirely certain how this offset happened. I can only assume that I must have 
configured something incorrectly or misunderstood a setting during the initial setup process. 
For this exercise, I want to force the homing position to <code>(0, 0, 0)</code> 
purely to gain a better understanding of how LinuxCNC handles homing sequences.

For reference, you can check out the official LinuxCNC documentation on 
<a href="https://linuxcnc.org/docs/html/config/ini-homing.html" 
title="Homing Configuration" target="_blank">Homing Configuration</a>.

🙏 Please note, this was a brand new setup for the 
<a href="https://store.mesanet.com/index.php?route=product/product&product_id=374" title="7I96S STEP/IO card" target="_blank">Mesa 7I96S card</a> 
using the Mesa Configuration Wizard, 
<a href="https://linuxcnc.org/docs/html/config/pncconf.html" 
title="Mesa Configuration Wizard" target="_blank">PnCconf</a>.

<a id="tried-failed"></a>
❶ I first went through the following steps suggested by 
<a href="https://gemini.google.com/app" title="Google Gemini" target="_blank">Google Gemini</a>—but 
unfortunately, they did not solve the issue.

<a id="tried-failed-axis-home-home-offset"></a>
⓵ In the main <code>.ini</code> configuration file (<code>Test_XYZ.ini</code>), under the respective joint blocks for the X axis (<code>[JOINT_0]</code>), Y axis (<code>[JOINT_1]</code> and <code>[JOINT_2]</code>), and Z axis (<code>[JOINT_3]</code>), I made sure <code>HOME</code> was set to <code>0.0</code> and added a <code>HOME_OFFSET = 0.0</code> entry:

```ini
[AXIS_X]
MAX_VELOCITY = 5.0
MAX_ACCELERATION = 750.0
MIN_LIMIT = -20.0
MAX_LIMIT = 100.0

[JOINT_0]
TYPE = LINEAR
HOME = 0.0
HOME_OFFSET = 0.0
HOME_SEQUENCE = 2
...

[AXIS_Y]
MAX_VELOCITY = 25.0
MAX_ACCELERATION = 750.0
MIN_LIMIT = -0.01
MAX_LIMIT = 200.0

[JOINT_1]
TYPE = LINEAR
HOME = 0.0
HOME_OFFSET = 0.0
HOME_SEQUENCE = -3
...

[JOINT_2]
TYPE = LINEAR
HOME = 0.0
HOME_OFFSET = 0.0
HOME_SEQUENCE = -3
FERROR = 10.0
...

[AXIS_Z]
MAX_VELOCITY = 25.0
MAX_ACCELERATION = 750.0
MIN_LIMIT = -100.0
MAX_LIMIT = 0.01

[JOINT_3]
TYPE = LINEAR
HOME = 0.0
HOME_OFFSET = 0.0
HOME_SEQUENCE = 1
FERROR = 10.0
...
```

After saving the file and relaunching LinuxCNC, this configuration update alone did not fix the problem.

<a id="tried-failed-axis-0-touch-off"></a>
⓶ For my next attempt, I tried using the LinuxCNC UI directly. I selected the <code>X-axis</code>, 
jogged it to what should be <code>0</code>, and clicked <code>Touch Off</code>. However, after 
relaunching LinuxCNC, this did not solve the issue either. 💡 At that time, I did not yet fully 
understand exactly what the <code>Touch Off</code> function does under the hood.

<a id="tried-failed-vel-sequence-sensor"></a>
⓷ This third attempt involved modifying several configuration variables at once. All of the updates discussed in <a href="#tried-failed-axis-home-home-offset">point ⓵</a> remained in place during this test.

● First, I verified that in the <code>Test_XYZ.ini</code> file, there were originally no active entries for <code>HOME_SEARCH_VEL</code> and <code>HOME_LATCH_VEL</code>.

● Next, I updated the <code>HOME_SEQUENCE</code> for each joint in the <code>Test_XYZ.ini</code> file to the following values:

```ini
[JOINT_0]
HOME_SEQUENCE = 1

[JOINT_1]
HOME_SEQUENCE = 1

[JOINT_2]
HOME_SEQUENCE = 1

[JOINT_3]
HOME_SEQUENCE = 0
```

● I then explicitly added <code>HOME_SEARCH_VEL = 0.0</code> and <code>HOME_LATCH_VEL = 0.0</code> to the <code>[JOINT_0]</code>, <code>[JOINT_1]</code>, <code>[JOINT_2]</code>, and <code>[JOINT_3]</code> sections of the file:

```ini
HOME_SEARCH_VEL = 0.0
HOME_LATCH_VEL = 0.0
```

● Finally, inside the main HAL file (<code>Test_XYZ.hal</code>), I commented out the previously configured <code>X-axis</code> limit proximity sensor connections to isolate the software behavior:

```text
# net x-home-sw     =>  joint.0.home-sw-in
# net x-neg-limit     =>  joint.0.neg-lim-sw-in
# net x-pos-limit     =>  joint.0.pos-lim-sw-in
```

( Note: Once I got the homing sequence <a href="#tried-succeeded">working successfully</a>, I re-wired the physical X-axis proximity switch sensor back up and reinstated the HAL lines above. Everything now works perfectly as expected. )

<a id="tried-succeeded"></a>
❷ Finally, ✔️ the correct resolution! This step was carried out while all of the configuration changes to the main <code>.ini</code> and <code>.hal</code> files <a href="#tried-failed">discussed above</a> were still in place.

I finally noticed the line <code>G54 X = -20.000</code> on the Preview panel and fed this clue back to 
<a href="https://gemini.google.com/app" title="Google Gemini" target="_blank">Google Gemini</a>. Gemini accurately pointed out that there was an <code><strong>active Coordinate Offset</strong></code> <em>“saved in LinuxCNC's memory (usually <code>G54</code> or <code>G92</code>). LinuxCNC remembers these offsets even if you restart the software, restart the computer, or change the <code>.ini</code> file config.”</em>

The official documentation covering this behavior can be found under 
<a href="https://linuxcnc.org/docs/2.8/html/gcode/coordinates.html" title="Coordinate Systems" target="_blank">LinuxCNC Coordinate Systems</a>.

Gemini proposed a clear solution: clear the active <code>G54</code> Fixture Offsets and the <code>G92</code> Offsets. To do this in LinuxCNC, open the <code>MDI</code> (Manual Data Input) tab and execute the following three commands sequentially:

```
G54
G10 L2 P1 X0 Y0 Z0
G92.1
```

I am operating largely on "faith" here 😂, as I have not studied these commands in deep technical detail yet. However, here is what they achieve:

● <code>G54</code> ensures that the machine is actively using the default work coordinate system.

● The second command, <code>G10 L2 P1 X0 Y0 Z0</code>, clears out the G54 offsets. Alternatively, this can be done manually via the GUI: select the axis, click the <code>Touch Off</code> button, enter <code>0</code> in the dialog box, and hit <code>OK</code> (repeating for X, Y, and Z).

● <code>G92.1</code> immediately clears any global, temporary axis offsets that might otherwise persist across sessions inside LinuxCNC's internal parameters.

I didn't inspect the <code>/home/behai/linuxcnc/configs/Test_XYZ/linuxcnc.var</code> 
file prior to executing these commands, so I don't know exactly what numbers were 
overwritten. But the results speak for themselves: now, every time LinuxCNC starts, 
the tool cone defaults perfectly to <code>(0, 0, 0)</code>, the Preview screen shows
the coordinate accordingly, as shown below:

![02-166-home-position.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/07/02-166-home-position.png)

Because everything is already zeroed out out-of-the-box, clicking <code>Home All</code> now leaves the visual display completely unchanged—exactly what I wanted to achieve!

<a id="github-ini-hal"></a>
❸ I have committed both the modified <code>.ini</code> and <code>.hal</code> configuration files to GitHub for reference:

<ul>
<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/linuxcnc/blob/3528d0c20023a9f9e75ee180ef65d5cbd8c57592/linuxcnc/configs/Test_XYZ/Test_XYZ.ini" 
title="Test_XYZ/Test_XYZ.ini" target="_blank"><code>Test_XYZ/Test_XYZ.ini</code></a>
</li>

<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/linuxcnc/blob/3528d0c20023a9f9e75ee180ef65d5cbd8c57592/linuxcnc/configs/Test_XYZ/Test_XYZ.hal" 
title="Test_XYZ/Test_XYZ.hal" target="_blank"><code>Test_XYZ/Test_XYZ.hal</code></a>
</li>
</ul>

<a id="concluding-remarks"></a>
❹ This has been an incredibly interesting troubleshooting exercise. I fully recognise that I took a few shortcuts to get these quick results—but hey, we all need a quick win to feel good sometimes! 😂 This definitely won't be the last time I look at homing configurations, and I am sure I will revisit and refine this process as my learning journey continues.

Thank you so much for reading. I hope you find this breakdown helpful for your own setups. Take care and stay safe!

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
