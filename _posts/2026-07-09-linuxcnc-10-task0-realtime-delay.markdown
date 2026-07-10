---
layout: post
title: "Raspberry Pi 4B LinuxCNC: Resolving the “Unexpected realtime delay on task0…” Startup Error"

description: After launching LinuxCNC, it consistently reported Unexpected realtime delay on task0 with period 500000. Despite this startup error, LinuxCNC otherwise appeared to operate normally. I am documenting the AI-assisted troubleshooting process I used to resolve this error. Again, this is not a tutorial, but rather a record of my learning progression. 

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
- realtime
- delay
- task0
---

<em>
After launching LinuxCNC, it consistently reported <code>Unexpected realtime delay on task0 with period 500000</code>. Despite this startup error, LinuxCNC otherwise appeared to operate normally. I am documenting the AI-assisted troubleshooting process I used to resolve this error. Again, this is not a tutorial, but rather a record of my learning progression.
</em>

<h3>
🐧 <a href="https://github.com/behai-nguyen/linuxcnc" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![167-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2026/07/167-feature-image.png) |
|:--:|
| *Raspberry Pi 4B LinuxCNC: Resolving the “Unexpected realtime delay on task0…” Startup Error* |

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

<a id="problem-desc"></a>
<p style="margin-top:20px">
The full text of the error is:
</p>

```text
Unexpected realtime delay on task0 with period 500000

This message will only display once per session.

Run the Latency Test and resolve before continuing.
```

Please see the screenshot below, which shows this error.

![Unexpected realtime delay on task0…](https://behainguyen.wordpress.com/wp-content/uploads/2026/07/167-01-task0-error.png)

<code>500000</code> is the value of the <code>SERVO_PERIOD</code> setting in the main <code>Test_XYZ.ini</code> file. This corresponds to 500,000 nanoseconds (500 µs).

💡 I previously performed the latency tests as documented in this post <a href="https://behainguyen.wordpress.com/2025/02/13/raspberry-pi-4b-linuxcnc-max-jitter-or-latency-test/" title="Raspberry Pi 4B: LinuxCNC Max Jitter or Latency Test" target="_blank">Raspberry Pi 4B: LinuxCNC Max Jitter or Latency Test</a>.

This problem has been present since the first day, but I have largely ignored it. Now that I have assembled all of the essential electronic components needed to build a functional, testable machine, it is time to investigate and resolve it.

This issue appears to be a common problem across different hardware environments. There are numerous related discussions on different social media platforms. Two examples from the official LinuxCNC forum are:

<ul>
<li style="margin-top:10px;">
<a href="https://www.forum.linuxcnc.org/38-general-linuxcnc-questions/40044-error-unexpected-realtime-delay-on-task-0-with-period-1000000" title="Error：Unexpected realtime delay on task 0 with period 1000000" target="_blank">Error：Unexpected realtime delay on task 0 with period 1000000</a> 
</li>

<li style="margin-top:10px;">
<a href="https://www.forum.linuxcnc.org/qtpyvcp/54203-unexpected-realtime-delay-on-task-0-with-period-1000000" title="Unexpected realtime delay on task 0 with period 1000000" target="_blank">Unexpected realtime delay on task 0 with period 1000000</a>
</li>
</ul>

The following commands show the kernel information for my Raspberry Pi 4B.

```
$ cat /proc/version
```

The output is:

```
Linux version 6.6.77-rt50-v8-behai-rt-build+ (behai@picnc) (gcc (Debian 12.2.0-14) 12.2.0, GNU ld (GNU Binutils for Debian) 2.40) #1 SMP PREEMPT_RT Tue Feb 18 12:45:31 AEDT 2025
```

```
$ hostnamectl
```

The output is:

```
 Static hostname: picnc
       Icon name: computer
      Machine ID: 9018........................da35
         Boot ID: 1909........................5104
Operating System: Debian GNU/Linux 12 (bookworm)
          Kernel: Linux 6.6.77-rt50-v8-behai-rt-build+
    Architecture: arm64
```

<a id="task0"></a>
❶ I was told that <code>task0</code> essentially corresponds to the <code>servo-thread</code>. It is the primary real-time thread responsible for running the motion control calculations, monitoring limit switches, and performing other time-critical tasks. This error indicates that the system was busy doing something, causing <code>task0</code> to miss its scheduled execution every 500,000 nanoseconds; in other words, it woke up late.

💥 I can't remember exactly why I set <code>SERVO_PERIOD</code> to 500,000 nanoseconds.

<a id="tried-failed"></a>
❷ I first worked through the following steps suggested by various AI assistants. They only partially resolved the issue.

● Checked and verified that in the main <code>Test_XYZ.ini</code> file, there is no entry for <code>BASE_PERIOD</code>, since <a href="https://store.mesanet.com/index.php?route=product/product&product_id=374" title="7I96S STEP/IO card" target="_blank">Mesa 7I96S card</a> does not use this entry. This was a brand-new configuration generated using the Mesa Configuration Wizard (<a href="https://linuxcnc.org/docs/html/config/pncconf.html" title="Mesa Configuration Wizard" target="_blank">PnCconf</a>), so the absence of <code>BASE_PERIOD</code> is expected.

● In the main <code>Test_XYZ.hal</code> file, I verified that:

<ul>
<li style="margin-top:10px;">
There is no entry attached to <code>base-thread</code>.
</li>

<li style="margin-top:10px;">
There are no <code>loadrt threads…</code>, <code>loadrt stepgen…</code>, <code>loadrt encoder…</code>, and <code>loadrt pwmgen…</code> entries.
</li>

<li style="margin-top:10px;">
There are no <code>addf hm2_7i96s.0.read servo-thread</code> and <code>addf hm2_7i96s.0.write servo-thread</code> entries.
</li>
</ul>

● 💡 In the main <code>Test_XYZ.ini</code> file, I updated <code>SERVO_PERIOD</code> to 1,000,000. I have observed that:

<ul>
<li style="margin-top:10px;">
After shutting down every other application, I relaunched LinuxCNC. With only LinuxCNC running, the error was not reported. I repeated this test several times, and the behaviour was consistent.
</li>

<li style="margin-top:10px;">
With <strong>only</strong> the <code>File Manager</code> running, relaunched LinuxCNC. The error was reported with <code>Unexpected realtime delay on task0 with period 1000000</code>. I have also repeated this several times, the behaviour was consistent.
</li>
</ul>

● Next, 💡 in the main <code>Test_XYZ.ini</code> file, I updated <code>SERVO_PERIOD</code> to 2,000,000. I have observed that, with the <code>File Manager</code> running, LinuxCNC did not raise this error. The behaviour was also consistent. However, when the <code>Terminal</code> was also running, the error was reported.

<a id="solution"></a>
❸ ✔️ Disable IPv6 networking and apply kernel <code>isolcpus</code>. I found this solution to be the most reliable.

<a id="solution-disable-ipv6"></a>
⓵ Disable IPv6 networking — the Mesa 7I96S card communicates with the Raspberry Pi through Ethernet using a fixed address. Disabling IPv6 removes unnecessary IPv6 networking activity, which may reduce background network processing and help avoid delays in the <code>servo-thread</code>.

Update the <code>kernel command-line</code> file to instruct the boot process to disable IPv6 networking. In <code>Debian GNU/Linux 12 (bookworm)</code>, this file is <code>/boot/firmware/cmdline.txt</code>:

```
$ sudo nano /boot/firmware/cmdline.txt
```

Add the following parameter, preceded by a space, to the end of the existing line. This file should contain only a single line.

```
network.disable_ipv6=1
```

<a id="solution-kernel-isolcpus"></a>
⓶ Kernel <code>isolcpus</code> — instructing Linux to isolate one or more CPU cores from normal scheduler activity, allowing LinuxCNC realtime tasks to run with less interference.

The Raspberry Pi 4B has <strong>4 CPU cores</strong>. To determine the number of cores, run the command <code>nproc</code>. By default, the operating system schedules normal background tasks, such as networking, the graphical user interface (GUI), and system maintenance, on the same CPU cores that LinuxCNC uses for realtime tasks.

For my Pi 4B, isolating a core for LinuxCNC realtime processing was the most effective step in eliminating the <code>Unexpected realtime delay</code> errors.

I isolated Core 3 by adding the following parameters, preceded by a space, to the end of the existing line in the <code>kernel command-line</code> file <code>/boot/firmware/cmdline.txt</code>:

```
isolcpus=3 nohz_full=3 rcu_nocbs=3
```

Please note:

<ul>
<li style="margin-top:10px;">
<code>isolcpus=3</code>: removes CPU 3 from normal scheduler load balancing. Not all kernel activity is removed from that CPU.
</li>
<li style="margin-top:10px;">
<code>nohz_full=3</code>: enables tickless operation on CPU 3 when possible.
</li>
<li style="margin-top:10px;">
<code>rcu_nocbs=3</code>: moves RCU callback processing away from CPU 3.
</li>
</ul>

Whenever the <code>kernel command-line</code> file is updated, the machine must be rebooted for the new parameters to take effect. After rebooting, the boot parameters can be verified with the command <code>cat /proc/cmdline</code>.

⓷ In the main <code>Test_XYZ.ini</code> file, restore <code>SERVO_PERIOD</code> to 1,000,000 nanoseconds.

I observed the following:

<ol>
<li style="margin-top:10px;">
With the <code>File Manager</code> and <code>Mousepad Text Editor</code> running, and <code>Test_XYZ.ini</code> loaded, <strong>the error did not occur</strong>.
</li>

<li style="margin-top:10px;">
With the <code>File Manager</code> and <code>Mousepad Text Editor</code> running, and <code>Test_XYZ.ini</code> loaded, and with <code>Chrome</code> running and the <a href="https://github.com/behai-nguyen/" title="behai-nguyen GitHub" target="_blank">GitHub page</a> loaded, <strong>the error did occur</strong>. This is understandable because a web browser introduces additional system activity, and it should not affect normal LinuxCNC operation.
</li>

<li style="margin-top:10px;">
With the <code>File Manager</code> and <code>Mousepad Text Editor</code> running, and <code>Test_XYZ.ini</code> loaded, and with the <code>Thonny Python IDE</code> running without any files loaded, <strong>the error did not occur</strong>.
</li>
</ol>

I am happy with this outcome. I consider the issue resolved for normal LinuxCNC operation.

<a id="ethernet-networkmgr"></a>
❹ <a href="https://wiki.debian.org/NetworkManager" title="Debian Wiki NetworkManager" target="_blank">NetworkManager</a>, the Ethernet Interface, and Network Latency.

The initial setup process for the Mesa 7I96S card, as described in the article <a href="https://behainguyen.wordpress.com/2025/02/14/raspberry-pi-4b-linuxcnc-initial-setup-for-the-mesa-7i96s-ethernet-motion-control/" title="Raspberry Pi 4B LinuxCNC: Initial Setup for the Mesa 7I96S Ethernet Motion Control" target="_blank">Raspberry Pi 4B LinuxCNC: Initial Setup for the Mesa 7I96S Ethernet Motion Control</a>, means that the Ethernet interface was configured using the traditional Linux network configuration method, which bypasses NetworkManager completely. NetworkManager is not controlling this connection. Therefore, it is unlikely to be the cause of the observed network latency issue between the Pi and the Mesa 7I96S card.

We can query the status of network devices using the command:

```
$ nmcli device status
```

```
behai@picnc:~ $ nmcli device status
DEVICE         TYPE      STATE                   CONNECTION
wlan0          wifi      connected               preconfigured
lo             loopback  connected (externally)  lo
p2p-dev-wlan0  wifi-p2p  disconnected            --
eth0           ethernet  unmanaged               --
behai@picnc:~ $
```

💡 Please note the line <code>eth0           ethernet  unmanaged</code>.

We observe an important LinuxCNC principle: <strong>a deterministic real-time system does not necessarily require zero network traffic; it requires predictable timing.</strong>

<a id="github-checkin"></a>
❺ All relevant configuration files have been committed to GitHub and are available for reference:

<ol>
<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/linuxcnc/blob/3528d0c20023a9f9e75ee180ef65d5cbd8c57592/linuxcnc/configs/Test_XYZ/Test_XYZ.ini" title="Test_XYZ/Test_XYZ.ini" target="_blank"><code>Test_XYZ/Test_XYZ.ini</code></a>
</li>

<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/linuxcnc/blob/3528d0c20023a9f9e75ee180ef65d5cbd8c57592/linuxcnc/configs/Test_XYZ/Test_XYZ.hal" title="Test_XYZ/Test_XYZ.hal" target="_blank"><code>Test_XYZ/Test_XYZ.hal</code></a>
</li>

<li style="margin-top:10px;">
<a href="https://github.com/behai-nguyen/linuxcnc/blob/50a45da3a17fb5cc21c99bb8d32c0edc18aaa6b6/boot/firmware/cmdline.txt" title="/boot/firmware/cmdline.txt" target="_blank"><code>/boot/firmware/cmdline.txt</code></a>
</li>
</ol>

<a id="concluding-remarks"></a>
❻ I have never gone through a troubleshooting process like this before. I find it very interesting. Hopefully, this issue has now been resolved. I understand that the Raspberry Pi 5 is much more powerful, even though it still has only four CPU cores. If I ever finish building this machine, I might consider upgrading to a Raspberry Pi 5 8GB model.

Thank you for reading. I hope you find this breakdown helpful for your own setups. Take care and stay safe!

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