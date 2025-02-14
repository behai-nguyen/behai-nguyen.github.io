---
layout: post
title: "Raspberry Pi 4B: LinuxCNC Max Jitter or Latency Test"

description: I conducted the LinuxCNC Max Jitter or Latency Test on my Raspberry Pi 4 Model B Rev 1.5, equipped with 8GB of RAM and running Debian GNU/Linux 12 (Bookworm) 6.12.11. The results are rather erratic, and I'm not sure how to interpret them. In this post, I present the results and describe the tests.

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2025/02/132-01-test-01.png"

gallery-image-list-2:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2025/02/132-02-test-02.png"
tags:
- Raspberry
- 4B
- Pi4
- LinuxCNC
- Max Jitter
- Latency Test
- Jitter Test
---

<em>
I conducted the LinuxCNC Max Jitter or Latency Test on my Raspberry Pi 4 Model B Rev 1.5, equipped with 8GB of RAM and running Debian GNU/Linux 12 (Bookworm) 6.12.11. The results are rather erratic, and I'm not sure how to interpret them. In this post, I present the results and describe the tests.
</em>

<h3>
🐧 <a href="https://github.com/behai-nguyen/linuxcnc" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![132-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/02/132-feature-image.png) |
|:--:|
| *Raspberry Pi 4B: LinuxCNC Max Jitter or Latency Test* |

I use the following official image:
<a href="https://linuxcnc.org/iso/rpi-4-debian-bookworm-6.12.11-arm64-ext4-2025-01-27-0404.img.xz" 
title="https://linuxcnc.org/iso/rpi-4-debian-bookworm-6.12.11-arm64-ext4-2025-01-27-0404.img.xz" 
target="_blank">https://linuxcnc.org/iso/rpi-4-debian-bookworm-6.12.11-arm64-ext4-2025-01-27-0404.img.xz</a>.
Then, I enabled WiFi, installed Samba, and set up remote desktop access. For more information on these official images, please refer to this forum post:
<a href="https://forum.linuxcnc.org/9-installing-linuxcnc/55192-linuxcnc-the-rpasberry-pi-4-5" 
title="Linuxcnc & the Rpasberry Pi (4 & 5)" target="_blank">Linuxcnc & the Rpasberry Pi (4 & 5)</a>.

The command:

```
C:\Users\behai>ssh cnc@192.168.0.45
```

reports the following information:

```
cnc@192.168.0.45's password:
   Debian GNU/Linux 12 (bookworm) 6.12.11 #1_RT Mon Jan 27 02:47:25 AEDT 2025
                                    aarch64

                                                 Raspberry Pi 4 Model B Rev 1.5

── DISK
Filesystem      Size  Used Avail Use% Mounted on
/dev/mmcblk0p2   29G  4.8G   23G  18% /
/dev/mmcblk0p1  508M   97M  411M  20% /boot/broadcom

── NETWORK
Hostname:    picnc
Wired:       eth0 DOWN 10.10.10.100
Wireless:    wlan0 UP 192.168.0.45

── SYSTEM
Processor:   Cortex-A72 @ 1800MHz 43°C
Frequency:   1800MHz
Online:      0-3
Governor:    performance
Memory:      7.6G 370M
Entropy:     256
Uptime:      14:08:00 up 4 min, 0 user, load average: 0.03, 0.18, 0.09

Last login: Fri Feb  7 01:22:37 2025 from 192.168.0.2
```

And the kernel information:

```
$ uname -a
```

reports:

```
Linux picnc 6.12.11 #1 SMP PREEMPT_RT Mon Jan 27 02:47:25 AEDT 2025 aarch64 GNU/Linux
```

<a id="test-environment"></a>
❶ <strong>The Test Environment</strong>

<ul>
<li style="margin-top:10px;">
The Raspberry Pi 4B was enclosed in a heat sink, but the fans were not running.
</li>

<li style="margin-top:10px;">
WiFi is enabled.
</li>

<li style="margin-top:10px;">
A USB wireless keyboard and mouse were used.
</li>

<li style="margin-top:10px;">
A USB stick was plugged in, but it was not accessed during any tests.
</li>

<li style="margin-top:10px;">
The Geany editor was running and used during the tests.
</li>
</ul>

<a id="test-results-and-description"></a>
❷ <strong>Test Results and Description</strong>

<a id="test-01"></a>
⓵ <strong>Test 1, Duration: 111 Minutes</strong>

Max Jitter recorded at the end of this test:

<ul>
<li style="margin-top:10px;">
<strong>Servo Thread:</strong> 164,463 nanoseconds (164.463 microseconds). 
This was reached at the <code>41st</code> minute.
</li>

<li style="margin-top:10px;">
<strong>Base Thread:</strong> 210,589 nanoseconds (210.589 microseconds).
This was reached at the <code>66th</code> minute.
</li>
</ul>

While the test was running, I carried out the following activities:

<ol>
<li style="margin-top:10px;">
From the start to the end of the test, Firefox was trying to load a 350MB MP4 file, but it never loaded and played.
</li>

<li style="margin-top:10px;">
From the 1st to the 17th minutes: ⓵ Used the file explorer application to copy and delete the 350MB MP4 once. ⓶ Opened a terminal window. ⓷ Switched windows and edited a text file.
</li>

<li style="margin-top:10px;">
From the 17th to the 41st minutes: ⓵ Used the file explorer application. ⓶ Opened another Firefox tab to download a 28MB file. ⓷ Opened a third Firefox tab to search. ⓸ Ran glxgears. ⓹ Switched windows and edited a text file.
<p>
👉 <strong>Please note:</strong> The Max Jitter for the <strong>Servo Thread</strong> 
reached <code>164,463 nanoseconds</code> and remained constant until the end of the test.
</p>
<p>
🙏 At this point, the heat sink felt really hot, so I wrapped a wet cloth around it. Eventually, the heat sink temperature came down, and it just felt warm to the touch.
</p>
</li>

<li style="margin-top:10px;">
From the 41st to the 66th minutes: ⓵ Had 3 glxgears instances running. ⓶ Used the terminal windows. ⓷ Used an existing Firefox tab to search. ⓸ Did a screen capture. ⓹ Switched windows and edited a text file.
<p>
👉 <strong>Please note:</strong> The Max Jitter for the <strong>Base Thread</strong> reached  
<code>210,589 nanoseconds</code> and remained constant until the end of the test.
</p>
</li>

<li style="margin-top:10px;">
From the 66th to the 93rd minutes: ⓵ Progressively had 6 glxgears instances running. ⓶ Used Ristretto Image Viewer to view an image, then terminated it. ⓷ Switched windows and edited a text file.
</li>

<li style="margin-top:10px;">
From the 93rd to the 111th minutes: Progressively stopped applications. ⓵ Closed the Firefox tab which was still trying to load a 350MB MP4 file. ⓶ Then terminated all 6 glxgears instances at some minute intervals. ⓷ Switched windows, edited a text file, etc.
</li>

<li style="margin-top:10px;">
Shut down the <code>HAL Latency Test</code> application.
</li>
</ol>

The screenshot below shows the result of this test:

{% include image-gallery.html list=page.gallery-image-list-1 %}
<br/>

<a id="test-02"></a>
⓶ <strong>Test 2, Duration: 109 Minutes</strong>

Max Jitter recorded at the end of this test:

<ul>
<li style="margin-top:10px;">
<strong>Servo Thread:</strong> 175,368 nanoseconds (175.368 microseconds).
This was reached at the <code>60th</code> minute.
</li>

<li style="margin-top:10px;">
<strong>Base Thread:</strong> 127,312 nanoseconds (127.312 microseconds).
This was reached at the <code>60th</code> minute.
</li>
</ul>

🙏 Throughout this test, the temperature of the heat sink felt warm to the touch. It was not too hot.

For this test, only the Geany editor was running initially. Then, I started the 
<code>HAL Latency Test</code> application. To start off, the 
<strong>Servo Thread</strong> jitter was <code>68,997 nanoseconds</code>, 
and the <strong>Base Thread</strong> jitter was <code>67,054 nanoseconds</code>.

While the test was running, I carried out the following activities:

<ol>
<li style="margin-top:10px;">
From the 1st to the 43rd minutes: ⓵ Started Firefox and used Google to search for various things. ⓶ From the 26th minute, a total of 6 glxgears instances were running. ⓷ Switched windows and edited a text file.
</li>

<li style="margin-top:10px;">
From the 43rd to the 60th minutes: No activities other than switching windows 
and editing a text file. Both the <strong>Servo Thread</strong> and the 
<strong>Base Thread</strong> jitters increased.

<p>
👉 <strong>At the 60th minute</strong>, the Max Jitter for the <strong>Servo Thread</strong> 
reached <code>175,368 nanoseconds</code>, and for the <strong>Base Thread</strong> 
reached <code>127,312 nanoseconds</code>. These values remained constant until the end of the test.
</p>
</li>

<li style="margin-top:10px;">
From the 60th to the 109th minutes: ⓵ I progressively started a total of 12 glxgears instances. ⓶ Then, I progressively shut them down 3 at a time until there were none. ⓷ Switched windows and edited a text file in between.
<p>
The Max Jitter for both threads remained unchanged from the 60th minute.
</p>
</li>
</ol>

The screenshot below shows the result of this test:

{% include image-gallery.html list=page.gallery-image-list-2 %}
<br/>

<a id="test-03"></a>
⓷ <strong>Test 3, Duration: 30 Minutes</strong>

Continuing from <a href="#test-02">Test 02</a> above, except for the Geany editor, all other applications were terminated. With only the Geany editor running, I clicked the <code>Reset Statistics</code> button and let the test run.

Max Jitter recorded at the end of this test:

<ul>
<li style="margin-top:10px;">
<strong>Servo Thread:</strong> 67,333 nanoseconds (67.333 microseconds).
</li>

<li style="margin-top:10px;">
<strong>Base Thread:</strong> 94,072 nanoseconds (94.072 microseconds).
</li>
</ul>

<a id="concluding-remarks"></a>
❸ According to the official page on 
<a href="https://linuxcnc.org/docs/html/install/latency-test.html" 
title="Latency Testing" target="_blank">Latency Testing</a>, the results reported by the first two tests indicate that this computer is not a good candidate for running LinuxCNC. However, people have successfully run LinuxCNC on similar hardware and software, so I might conduct some more tests.

I am using the 
<a href="https://store.mesanet.com/index.php?route=product/product&product_id=374" 
title="7I96S STEP/IO Step & dir plus I/O card" 
target="_blank">7I96S STEP/IO Step & dir plus I/O card</a> for LinuxCNC.
Since the setup uses hardware step generation, kernel latency is somewhat less critical. However, I still want to determine the latency as accurately as possible. I will revisit this issue in the future as needed.

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
<a href="https://forum.linuxcnc.org/show-your-stuff/32672-linuxcnc-logo?start=20#gallery-6" target="_blank">https://forum.linuxcnc.org/show-your-stuff/32672-linuxcnc-logo?start=20#gallery-6</a>
</li>
</ul>

<h3>
🐧 <a href="https://github.com/behai-nguyen/linuxcnc" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>
