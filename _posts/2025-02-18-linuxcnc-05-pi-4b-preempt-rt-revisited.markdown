---
layout: post
title: "Raspberry Pi 4B: Natively Built 64 Bit Fully Preemptible Kernel (Real-Time) Gets Overridden"

description: Running PnCconf on the natively built 64-bit Fully Preemptible Kernel (Real-Time) kernel, as previously discussed, resulted in the following message&#58; You are using a simulated-realtime version of LinuxCNC, so testing / tuning of hardware is unavailable. In this post, we will examine what has happened, prove that the finding is correct, and present the results of the jitter or latency test we conducted on the Raspberry Pi OS. 

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2025/02/135-02.png"

gallery-image-list-2:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2025/02/135-03.png"

tags:
- Raspberry
- PREEMPT_RT
- kernel
- 64 Bit
- Real-Time
- 4B
- Pi4
- RT extension
- Fully Preemptible Kernel
- Preempt-RT
- Patch
---

<em>
Running <a href="https://linuxcnc.org/docs/html/config/pncconf.html" title="PnCconf Mesa Configuration Wizard" target="_blank">PnCconf</a> on the natively built 64-bit Fully Preemptible Kernel (Real-Time) kernel, as <a href="https://behai-nguyen.github.io/2024/11/03/pi-4b-preempt-rt-kernel-patch.html" title="Raspberry Pi 4B: Natively Build a 64 Bit Fully Preemptible Kernel (Real-Time) with Desktop" target="_blank">previously discussed</a>, resulted in the following message: <code>You are using a simulated-realtime version of LinuxCNC, so testing / tuning of hardware is unavailable</code>. In this post, we will examine what has happened, prove that the finding is correct, and present the results of the jitter or latency test we conducted on the Raspberry Pi OS.
</em>

<h3>
🐧 <a href="https://github.com/behai-nguyen/linuxcnc" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![135-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/02/135-feature-image.png) |
|:--:|
| *Raspberry Pi 4B: Natively Built 64 Bit Fully Preemptible Kernel (Real-Time) Gets Overridden* |

<a id="the-cause"></a>
<strong><em>Accepting the Raspberry Pi OS prompt to update the system results in my natively built 64-bit Fully Preemptible Kernel (Real-Time) being removed and the original kernel reinstalled! 🤬</em></strong>

❶ Toward the end of October 2024, I finished building a <code>64-bit Fully Preemptible 
Kernel (Real-Time)</code> for use with LinuxCNC, 
<a href="https://behai-nguyen.github.io/2024/11/03/pi-4b-preempt-rt-kernel-patch.html" 
title="Raspberry Pi 4B: Natively Build a 64 Bit Fully Preemptible Kernel (Real-Time) with Desktop" 
target="_blank">as documented</a>. I received the 
<a href="https://store.mesanet.com/index.php?route=product/product&product_id=374" 
title="7I96S STEP/IO Step & dir plus I/O card" 
target="_blank">7I96S STEP/IO Step & dir plus I/O card</a> on 22/01/2025. 
On 05/02/2025, I was able to run the Mesa Configuration Wizard, 
<a href="https://linuxcnc.org/docs/html/config/pncconf.html"
title="PnCconf Mesa Configuration Wizard" target="_blank">PnCconf</a>. 
When clicking on the <code>Test / Tune Axis</code>, I got the above message as illustrated in the following screenshot:

![pncconf-02.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/02/pncconf-02.png)

I actually built LinuxCNC from source and installed the locally built package. 
I followed the instructions to the letter but thought my build had issues. 
Unsure of what had happened, I 
<a href="https://forum.linuxcnc.org/39-pncconf/55238-pncconf-mesa-7i96s-you-are-using-a-simulated-realtime-version-of-linuxcnc" 
title="PNCConf, Mesa 7I96S: &quot;You are using a simulated-realtime version of LinuxCNC...&quot;" 
target="_blank">sought help</a> from the forum. I was advised to use the official image: 
<a href="https://linuxcnc.org/iso/rpi-4-debian-bookworm-6.12.11-arm64-ext4-2025-01-27-0404.img.xz" 
title="https://linuxcnc.org/iso/rpi-4-debian-bookworm-6.12.11-arm64-ext4-2025-01-27-0404.img.xz" 
target="_blank">https://linuxcnc.org/iso/rpi-4-debian-bookworm-6.12.11-arm64-ext4-2025-01-27-0404.img.xz</a>.
I heeded the advice, as seen in previous posts.

I still had another SD card with the real-time kernel and LinuxCNC mentioned above. 
In an effort to understand the issue, on 17th February 2025, I removed my original build 
and installation of LinuxCNC 2.9.3, downloaded, and installed the 
<a href="https://www.linuxcnc.org/dists/bookworm/2.9-uspace/binary-arm64/linuxcnc-uspace_2.9.4_arm64.deb" 
title="LinuxCNC 2.9.4 Package" target="_blank">linuxcnc-uspace_2.9.4_arm64.deb</a> 
package. The commands to remove and install are: 

```
$ sudo apt remove linuxcnc-uspace
$ sudo dpkg -i /home/behai/Public/linuxcnc-uspace_2.9.4_arm64.deb
```

This time, I was able to run 
<a href="https://linuxcnc.org/docs/html/config/pncconf.html"
title="PnCconf Mesa Configuration Wizard" target="_blank">PnCconf</a> successfully, as 
mentioned in previous posts. I was convinced that my LinuxCNC 2.9.3 build was 
the problem 😂. I shut down <code>PnCconf</code> to run the latency test. 
Raspberry Pi OS notified me of pending updates, which I accepted. Then I started the 
<code>HAL Latency Test</code> application. With only three instances of 
<code>glxgears</code> running, the Max Jitter for the <strong>Base Thread</strong> 
reached nearly <strong>500,000 nanoseconds</strong>!

I was quite taken aback. The previous latency 
<a href="https://behainguyen.wordpress.com/2025/02/13/raspberry-pi-4b-linuxcnc-max-jitter-or-latency-test/" 
title="Raspberry Pi 4B: LinuxCNC Max Jitter or Latency Test" target="_blank">test results</a> 
were nowhere near this bad: the tests were conducted on a different OS, but the hardware was 
the same. When I looked at the <code>Kernel-version</code> field on the <code>HAL Latency 
Test</code> screen, it showed <code>PREEMPT</code> not <code>PREEMPT_RT</code>.

💥 That was when I realised that <strong><em>accepting the Raspberry Pi OS prompt to update the system led to the custom-built 64-bit Fully Preemptible Kernel (Real-Time) being removed and the original kernel reinstalled!</em></strong>

Just to be doubly certain, I ran 
<a href="https://linuxcnc.org/docs/html/config/pncconf.html"
title="PnCconf Mesa Configuration Wizard" target="_blank">PnCconf</a> 
again and expected the above message to appear — and it did. 
<strong>I accepted the prompted update on the first SD card too.</strong>

<a id="rebuild-the-os-image"></a>
❷ Three months have passed since November 2024, and it’s time for a new updated real-time kernel. 
Following the 
<a href="https://behainguyen.wordpress.com/2024/11/03/raspberry-pi-4b-natively-build-a-64-bit-fully-preemptible-kernel-real-time-with-desktop/" 
title="Raspberry Pi 4B: Natively Build a 64 Bit Fully Preemptible Kernel (Real-Time) with Desktop" 
target="_blank">first post</a>, I successfully built a real-time kernel version 
<code>6.6.77-rt50</code>: 

![135-01.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/02/135-01.png)

With this version, we need to install <code>ifupdown</code>, which is a set of high-level scripts to configure network interfaces. The command to install it is:

```
$ sudo apt install ifupdown
```

Before we can install the downloaded LinuxCNC 2.9.4 
<a href="https://www.linuxcnc.org/dists/bookworm/2.9-uspace/binary-arm64/linuxcnc-uspace_2.9.4_arm64.deb" 
title="LinuxCNC 2.9.4 Package" target="_blank">linuxcnc-uspace_2.9.4_arm64.deb</a> 
package, we need to install the missing packages. The command is: 

```
$ sudo apt --fix-broken install
```

Then, finally: 

```
$ sudo dpkg -i /home/behai/Public/linuxcnc-uspace_2.9.4_arm64.deb
```

<a href="https://linuxcnc.org/docs/html/config/pncconf.html"
title="PnCconf Mesa Configuration Wizard" target="_blank">PnCconf</a> now runs, and 
LinuxCNC also “runs”. I am able to move along the X-axis, and the single stepper motor 
(please refer to 
<a href="https://behainguyen.wordpress.com/2025/02/16/raspberry-pi-4b-linuxcnc-wiring-the-mesa-7i96s-ethernet-motion-control-closed-loop-cl57t-stepper-driver-and-nema-23-stepper-motor/" 
title="Raspberry Pi 4B LinuxCNC: Wiring the Mesa 7I96S Ethernet Motion Control, Closed-Loop CL57T Stepper Driver, and Nema 23 Stepper Motor" 
target="_blank">this post</a>) also turns. Please see the screenshot below: 

{% include image-gallery.html list=page.gallery-image-list-1 %}
<br/>

<a id="latency-test"></a>
❸ We will not describe the test sequence in detail. Briefly, the test ran for more than an hour. With 12 instances of <code>glxgears</code>, the Max Jitter for the two threads remained constant at:

<ul>
<li style="margin-top:10px;">
<strong>Servo Thread</strong>: 98,571 nanoseconds (98.571 microseconds)
</li>
<li style="margin-top:10px;">
<strong>Base Thread</strong>: 100,776 nanoseconds (100.776 microseconds)
</li>
</ul>

The raw recording of the test is included below:

```
The environment:

FileManager
Terminal Window
Text Editor
Chromium opened with Google tab
USB stick plugged-in

15:26 -- trying to capture screen, moving windows etc.

15:32
Servo-Thread: 54,080 ns
Base-Thread: 56,944 ns

15:34: applied cooling.
15:35: Change to YouTube run a 1:20:00 clip.

15:37:
Servo-Thread: 365,375 ns
Base-Thread: 610,162 ns

15:40 -- Shutdown Chromium.

15:41:
Servo-Thread: 369,687 ns
Base-Thread: 610,162 ns

15:42: Reset Statistics

15:42 -- 15:46
Servo-Thread: 31,981 ns
Base-Thread: 57,369 ns

15:46: run 3 glxgears in succession.

Servo-Thread: 67,487 ns
Base-Thread: 60,221 ns

15:49: run Chromium single Google tab search for something.

15:53:
Servo-Thread: 93,932 ns
Base-Thread: 100,776 ns

15:55:
run another 3 glxgears in succession. 6 instances now.
Google something else.

16:04: Archive /home/behai/linux: 2.7GB

On the first terminal window, under /home/behai, run:

$ tar -zcvf  6-6-77-rt50-v8-behai-rt-build-home-behai-linux.tar.gz /home/behai/linux

-rw-r--r--  1 behai behai 748173752 Feb 18 16:08 6-6-77-rt50-v8-behai-rt-build-home-behai-linux.tar.gz

16:12:
Servo-Thread: 98,571 ns
Base-Thread: 100,776 ns

16:14: 
run another 3 glxgears in succession. 9 instances now.

16:22
Servo-Thread: 98,571 ns
Base-Thread: 100,776 ns

16:23:
run another 3 glxgears in succession. 12 instances now.

16:36
Servo-Thread: 98,571 ns
Base-Thread: 100,776 ns

16:37: using a preinstalled UI app to open 6-6-77-rt50-v8-behai-rt-build-home-behai-linux.tar.gz.
16:44: finished browsing the above *.gz file.
16:45: using File Manager moved 6-6-77-rt50-v8-behai-rt-build-home-behai-linux.tar.gz to /home/behai/Public/.

16:46
Servo-Thread: 98,571 ns
Base-Thread: 100,776 ns

16:51: ran behai@picnc:~ $ rm -rf linux/

16:52
Servo-Thread: 98,571 ns
Base-Thread: 100,776 ns

16:53: shutdown 3 instances (first) glxgears. 9 remain.
16:55: shutdown 3 instances (first) glxgears. 6 remain.
16:57: shutdown 3 instances (first) glxgears. 3 remain.
16:59: copied around 740 MB to the USB stick using File Manager.
17:01: shutdown the last 3 glxgears instances.

17:02
Servo-Thread: 98,571 ns
Base-Thread: 100,776 ns

17:03: went to YouTube using Chromium:
Servo-Thread: 98,571 ns
Base-Thread: 140,405 ns

17:04: played a 1:36:00 clip.
17:05:
Servo-Thread: 281,238 ns
Base-Thread: 375,605 ns

17:05:
Servo-Thread: 355,255 ns
Base-Thread: 453,918 ns

17:06: Reset Statistics.
Servo-Thread: 470,420 ns
Base-Thread: 498,306 ns
```

The screenshot below illustrates a result of the test:

{% include image-gallery.html list=page.gallery-image-list-2 %}
<br/>

<a id="concluding-remarks"></a>
❹ I had no plan to write this post, but what I have found is rather unexpected and quite interesting. Hopefully, this post will be helpful to someone in the future.

If you happen to read this post, thank you for your time, and I hope I did not waste it. Stay safe, as always.

✿✿✿

Feature image source:

<ul>
<li>
<a href="https://www.instructables.com/Easy-Raspberry-Pi-Based-ScreensaverSlideshow-for-E/" target="_blank">https://www.instructables.com/Easy-Raspberry-Pi-Based-ScreensaverSlideshow-for-E/</a>
</li>
</ul>

<h3>
🐧 <a href="https://github.com/behai-nguyen/linuxcnc" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>
