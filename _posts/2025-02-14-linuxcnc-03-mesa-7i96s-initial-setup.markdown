---
layout: post
title: "Raspberry Pi 4B LinuxCNC: Initial Setup for the Mesa 7I96S Ethernet Motion Control"

description: In this post, I describe the initial setup for the Mesa 7I96S Ethernet motion control STEP/IO Step & Dir plus I/O card. The setup includes selecting the power supply and configuring the network IP address. 

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2025/02/mdr-10-5-ac-input.jpg"

gallery-image-list-2:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2025/02/mesa-7i96s-power-connection.jpg"

gallery-image-list-3:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2025/01/mesa_7i96s_w5_up.jpg"

tags:
- Raspberry
- 4B
- Pi4
- LinuxCNC
- Mesa 7I96S
- 7I96S
- Motion Control
- power supply
- MDR-10-5
---

<em>
In this post, I describe the initial setup for the Mesa <a href="https://store.mesanet.com/index.php?route=product/product&product_id=374" title="7I96S STEP/IO Step & dir plus I/O card" target="_blank">7I96S Ethernet motion control STEP/IO Step & Dir plus I/O card</a>. The setup includes selecting the power supply and configuring the network IP address.
</em>

<h3>
🐧 <a href="https://github.com/behai-nguyen/linuxcnc" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![133-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2025/02/133-feature-image.png) |
|:--:|
| *Raspberry Pi 4B LinuxCNC: Initial Setup for the Mesa 7I96S Ethernet Motion Control* |

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

<a id="mesa-7i96s"></a>
❶ The Mesa 
<a href="https://store.mesanet.com/index.php?route=product/product&product_id=374" 
title="7I96S STEP/IO Step & dir plus I/O card" 
target="_blank">7I96S STEP/IO Step & dir plus I/O card</a> 
I have is <code>Rev E</code>. This is its 
<a href="http://www.mesanet.com/pdf/parallel/7i96sman.pdf" 
title="The Mesa 7I96S Manual" target="_blank">PDF manual</a>. 
The detailed diagram is on <strong>page 5</strong>. An older 
but larger and clearer <code>Rev B</code> diagram can be found in 
<a href="https://forum.linuxcnc.org/27-driver-boards/51710-mesa-firmware-versions-and-updating#293450" 
title="The Mesa 7I96S Rev B diagram" target="_blank">this forum post</a>.

<a id="power-supply"></a>
❷ <strong>Power Supply and Connection</strong>

<strong>Page 6</strong> of the manual specifies the power requirements and connection. 
Initially, I reused a USB cable to make a <code>5V</code> DC power supply: <strong>
I used a multimeter to ascertain that the USB power supply outputs 5V 
before using it.</strong> 
I used this power supply to power on the Mesa 7I96S card, set up its IP address, and ping it. However, I have been told that this USB power supply is not suitable for a production setup.

Based on the following two forum posts: 
<a href="https://forum.linuxcnc.org/27-driver-boards/53259-mesa-7i96s-power-supply" 
title="MESA 7i96S power supply" target="_blank">MESA 7i96S power supply</a> and 
<a href="https://forum.linuxcnc.org/27-driver-boards/52588-7i96s-psu?start=10#300712" 
title="7i96S PSU" target="_blank">7i96S PSU</a>, I purchased the 
<a href="https://www.power-supplies-australia.com.au/mean-well-mdr-10-5-power-supply" 
title="Mean Well MDR-10-5" target="_blank">Mean Well MDR-10-5</a>.

I am in Australia. The electrical system is 50Hz and 240V AC. The outlets are 
rated for 10 amps. The standard 3-pin plugs consist of an Active/Live, Neutral, 
and Earth connection. Please refer to 
<a href="https://www.finnleyelectrical.com.au/what-electrical-plug-does-australia-use/" 
title="What electrical plug does Australia use?" target="_blank">this page</a> 
for further information. I have been tutored on this subject before by an electrical engineer.

The AC input connection is shown in the image below. Please note that the colours for the Active/Live, Neutral, and Earth wires match the colours described on 
<a href="https://www.thelocalelectrician.com.au/wire-colour-codes-electrician-guide/" 
title="Wire Colour Codes – Electrician Guide" target="_blank">this page</a>:

| ![mdr-10-5-ac-input.jpg](https://behainguyen.wordpress.com/wp-content/uploads/2025/02/mdr-10-5-ac-input.jpg) |
|:--:|
| MEAN WELL MDR-10-5 AC Input Connection |


👉 As with the USB power supply, <strong>I used a multimeter to ascertain that 
the output voltage is 5V</strong> before connecting it to the Mesa 7I96S card.

💥 <strong>Please note:</strong> We must connect the power supply's positive (+) DC output line to the Mesa 7I96S positive (+) power input and the power supply's negative (-) DC output line to the Mesa 7I96S negative (-) power input. Otherwise, the Mesa 7I96S might get damaged.

Based on <strong>page 6</strong> of the 
<a href="http://www.mesanet.com/pdf/parallel/7i96sman.pdf" 
title="The Mesa 7I96S Manual" target="_blank">Mesa 7I96S manual</a>, 
the connection to the power supply is illustrated in the image below:

| ![mesa-7i96s-power-connection.jpg](https://behainguyen.wordpress.com/wp-content/uploads/2025/02/mesa-7i96s-power-connection.jpg) |
|:--:|
| MEAN WELL MDR-10-5 to Mesa 7I96S Connection |

<a id="ip-jumper-setting"></a>
❸ <strong>IP Jumper Setting and Network Configuration</strong>

I started with the official page 
<a href="http://linuxcnc.org/docs/2.8/html/man/man9/hm2_eth.9.html#INTERFACE%20CONFIGURATION" 
title="INTERFACE CONFIGURATION" target="_blank">INTERFACE CONFIGURATION</a> 
and the <a href="http://www.mesanet.com/pdf/parallel/7i96sman.pdf" 
title="The Mesa 7I96S Manual" target="_blank">Mesa 7I96S manual</a>, page 4, 
under the “IP Address Selection” section. I initially failed to get it to work correctly. 
I requested help from the LinuxCNC forum, and this thread set me on the right path: 
<a href="https://forum.linuxcnc.org/38-general-linuxcnc-questions/43854-network-configuration?start=0" 
title="network configuration" target="_blank">network configuration</a> 🙏.

Jumper <code>W5</code> needs to be in the up position as illustrated in the image below:

| ![mesa_7i96s_w5_up.jpg](https://behainguyen.wordpress.com/wp-content/uploads/2025/01/mesa_7i96s_w5_up.jpg) |
|:--:|
| Mesa 7I96S Jumper W5 Is In Up Position |

The 7I96S is an Ethernet-connected motion control interface. We use an RJ45 cable to connect it to the Raspberry Pi 4B via their Ethernet ports. We query the Pi 4B for available network interfaces with the following command:

```
$ ip link show
```

The output is:

```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN mode DEFAULT group default qlen 1000
    link/ether d8:3a:dd:25:8c:37 brd ff:ff:ff:ff:ff:ff
    altname end0
3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DORMANT group default qlen 1000
    link/ether d8:3a:dd:25:8c:38 brd ff:ff:ff:ff:ff:ff
```

<ol>
<li style="margin-top:10px;">
<code>lo</code>: The loopback interface.
</li>

<li style="margin-top:10px;">
<code>eth0</code>: The first Ethernet interface.
</li>

<li style="margin-top:10px;">
<code>wlan0</code>: The first wireless network interface.
</li>
</ol>

The dedicated network interface to use is <code><strong>eth0</strong></code>. 
Use the <code>nano</code> text editor to edit the <code>/etc/network/interfaces</code> 
file with the following command: 

```
$ sudo nano /etc/network/interfaces
```

Add the following lines to the end of <code>/etc/network/interfaces</code>:

```
auto eth0
iface eth0 inet static
address 10.10.10.100
hardware-irq-coalesce-rx-usecs 0
```

Then restart the network interfaces with the following commands:

```
$ sudo ifdown -a
$ sudo ifup -a
```

Power on the 7I96S card and ping it using its fixed EEPROM IP address:

```
$ ping 10.10.10.10
```

If everything goes well, it should respond successfully. When the network cable is disconnected in the middle of pinging, it reports <code>Destination Host Unreachable</code>, which is what should happen. When reconnected, it picks up again. The output of this sequence looks as follows:

```
PING 10.10.10.10 (10.10.10.10) 56(84) bytes of data.
64 bytes from 10.10.10.10: icmp_seq=1 ttl=64 time=0.202 ms
64 bytes from 10.10.10.10: icmp_seq=2 ttl=64 time=0.086 ms
64 bytes from 10.10.10.10: icmp_seq=3 ttl=64 time=0.086 ms
64 bytes from 10.10.10.10: icmp_seq=4 ttl=64 time=0.083 ms
64 bytes from 10.10.10.10: icmp_seq=5 ttl=64 time=0.102 ms
64 bytes from 10.10.10.10: icmp_seq=6 ttl=64 time=0.080 ms
From 10.10.10.100 icmp_seq=9 Destination Host Unreachable
From 10.10.10.100 icmp_seq=13 Destination Host Unreachable
From 10.10.10.100 icmp_seq=16 Destination Host Unreachable
From 10.10.10.100 icmp_seq=19 Destination Host Unreachable
From 10.10.10.100 icmp_seq=20 Destination Host Unreachable
64 bytes from 10.10.10.10: icmp_seq=21 ttl=64 time=0.143 ms
64 bytes from 10.10.10.10: icmp_seq=22 ttl=64 time=0.085 ms
^C
--- 10.10.10.10 ping statistics ---
26 packets transmitted, 14 received, +5 errors, 46.1538% packet loss, time 25587ms
rtt min/avg/max/mdev = 0.080/0.099/0.202/0.032 ms, pipe 4
```

<a id="concluding-remarks"></a>
❹ It has been an interesting learning experience. There is still a lot to learn ahead. Hopefully, I can finish this project successfully at some point in the future.

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
