---
layout: post
title: "Raspberry Pi 4B: Natively Build a 64 Bit Fully Preemptible Kernel (Real-Time) with Desktop"

description: In this article, I present a step-by-step procedure to natively patch and build a 64-bit Fully Preemptible Kernel (Real-Time) for my Raspberry Pi 4B (Pi 4B). We start with a pre-made operating system image that includes a desktop environment. After building and installing the real-time patch kernel, querying the kernel information with the command uname -a should report something similar to&#58; “Linux picnc 6.6.59-rt45-v8-behai-rt-build+ #1 SMP PREEMPT_RT Sat Nov 2 10:20:46 AEDT 2024 aarch64 GNU/Linux”. This indicates that the token PREEMPT_RT is present in the output. Natively in this instance means that we patch and build the kernel using the very Pi 4B on which the newly built kernel is installed." 

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list-1:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/11/125-01.png"
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/11/125-02.png"

gallery-image-list-2:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/11/125-03.png"

gallery-image-list-3:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/11/125-04.png"

gallery-image-list-4:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/11/125-05.png"

gallery-image-list-5:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/11/125-06.png"

gallery-image-list-6:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/11/125-07.png"

gallery-image-list-7:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/11/125-08.png"

gallery-image-list-8:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/11/125-09.png"

gallery-image-list-9:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/10/002-pi-os-full-64-bit-debian-bookworm.png"

gallery-image-list-10:
    - "https://behainguyen.wordpress.com/wp-content/uploads/2024/11/125-10.png"

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
In this article, I present a step-by-step procedure to natively patch and build a 64-bit Fully Preemptible Kernel (Real-Time) for my Raspberry Pi 4B (Pi 4B). We start with a pre-made operating system image that includes a desktop environment. After building and installing the real-time patch kernel, querying the kernel information with the command <code>uname -a</code> should report something similar to:

```
Linux picnc 6.6.59-rt45-v8-behai-rt-build+ #1 SMP PREEMPT_RT Sat Nov  2 10:20:46 AEDT 2024 aarch64 GNU/Linux
```

This indicates that the token <strong><code>PREEMPT_RT</code></strong> is present in the output. <strong>Natively</strong> in this instance means that we patch and build the kernel using the very Pi 4B on which the newly built kernel is installed.
</em>

<h3>
🐧 <a href="https://github.com/behai-nguyen/linuxcnc" title="Index of the Complete Series" target="_blank">Index of the Complete Series</a>.
</h3>

| ![125-feature-image.jpg](https://behainguyen.wordpress.com/wp-content/uploads/2024/11/125-feature-image.jpg) |
|:--:|
| *Raspberry Pi 4B: Natively Build a 64 Bit Fully Preemptible Kernel (Real-Time) with Desktop* |

Let's first describe the steps and then provide some background information on why I looked into this.

<a id="proc-step-by-step"></a>
❶ We will now discuss the step-by-step procedure.

<a id="proc-install-rpi-imager"></a>
⓵ I use a newly installed Ubuntu 24.04.1 LTS to write the target operating system (OS) image onto a microSD card. We need to install <code>Raspberry Pi Imager</code>:

```
$ sudo apt install rpi-imager
```

There should not be any problem. <code>Raspberry Pi Imager v1.8.5</code> should appear in the Ubuntu application list. 💥 I first tried to install it on Ubuntu 22.10 Kinetic, but it reported a lot of errors, which I tried to fix without success.

<a id="proc-install-pre-made-os"></a>
⓶ Use <code>Raspberry Pi Imager</code> to write a pre-made OS image onto a microSD card. This application should be self-explanatory. For <code>Operating System</code>, I select <code>Raspberry Pi OS (other)</code>, then <code>Raspberry Pi OS Full (64-bit)</code>. Please see the screenshots below:

{% include image-gallery.html list=page.gallery-image-list-1 %}
<br/>

The <code>NEXT</code> button lets us configure the new OS. Please see the illustration below:

{% include image-gallery.html list=page.gallery-image-list-2 %}
<br/>

In the <code>SERVICES</code> tab, we can enable SSH. The writing of the OS image should not take too long. After finishing writing, we should be able to boot without any issues. My <code>hostname</code> is <code>picnc.local</code>, and my <code>username</code> is <code>behai</code>. Both of the following commands should work:

```
$ ping picnc.local
$ ssh behai@picnc.local
```

<a id="proc-install-pre-made-os-query-kernel-info"></a>
We can query the kernel information with:

```
$ uname -a
```

In my case, the output is:

```
Linux picnc 6.6.51+rpt-rpi-v8 #1 SMP PREEMPT Debian 1:6.6.51-1+rpt3 (2024-10-08) aarch64 GNU/Linux
```

Note the <strong><code>PREEMPT</code></strong> token. We are going to change that to <strong><code>PREEMPT_RT</code></strong>.

We can also use the following commands to query the kernel information:

```
$ uname -r
$ uname -srm
$ hostnamectl
$ cat /proc/version
```

👉 The following steps are extracted from the Raspberry Pi page <a href="https://www.raspberrypi.com/documentation/computers/linux_kernel.html" title="The Linux kernel" target="_blank">The Linux kernel</a>. This official page covers multiple OSes. I have arranged the steps to suit the OS that I am using.

<a id="proc-download-latest-kernel-code"></a>
⓷ Download the latest kernel source code. Please refer to <a href="https://www.raspberrypi.com/documentation/computers/linux_kernel.html#download-kernel-source" title="Download kernel source" target="_blank">this official section</a>. Change to the <code>$HOME</code> directory:

```
$ cd $HOME
```

And run the command:

```
$ git clone --depth=1 https://github.com/raspberrypi/linux
```

This downloads the kernel source code to <code>$HOME/linux</code>. Please note that the <code>git</code> utility is included with the OS image. It can be installed with:

```
$ sudo apt install git
```

<a id="proc-real-time-kernel"></a>
⓸ Patch the real-time kernel. Please refer to <a href="https://www.raspberrypi.com/documentation/computers/linux_kernel.html#patch-the-kernel" title="Patch the kernel" target="_blank">this official section</a>.

● Determine the current kernel version:

```
$ uname -r
```

The output will be something like:

```
6.6.51+rpt-rpi-v8
```

● Determine the kernel source version. Change to the kernel source directory:

```
$ cd linux
```

Run the following command to get the kernel source version:

```
$ head Makefile -n 4
```

The output will be something like:

```
# SPDX-License-Identifier: GPL-2.0
# SPDX-License-Identifier: GPL-2.0
VERSION = 6
PATCHLEVEL = 6
SUBLEVEL = 59
```

In this instance, the kernel source version is <code>6.6.59</code>. At the time, there was no version <code>6.6.59</code> of the real-time kernel patch at <a href="https://www.kernel.org/pub/linux/kernel/projects/rt/6.6/" title="Real-time kernel patches" target="_blank">https://www.kernel.org/pub/linux/kernel/projects/rt/6.6/</a>, so I used patch version <code>6.6.58</code> instead. Please note that on the internet, there are numerous mentions of this issue. Sometimes patches are behind, and using a not-so-older version of the patch should be okay.

● Apply the target real-time kernel patch. 🙏 Please recall that the present working directory is <code>$HOME/linux</code>. The following commands download, uncompress, and patch the kernel source code with the target real-time kernel patch:

```
$ wget https://www.kernel.org/pub/linux/kernel/projects/rt/6.6/patch-6.6.58-rt45.patch.gz
$ gunzip patch-6.6.58-rt45.patch.gz
$ cat patch-6.6.58-rt45.patch | patch -p1
```

<a id="proc-config-kernel"></a>
⓹ Configure the kernel. Please refer to <a href="https://www.raspberrypi.com/documentation/computers/linux_kernel.html#configure-the-kernel" title="Configure the kernel" target="_blank">this official section</a>. 

● Install build tools/dependencies:  

```
$ cd $HOME
$ sudo apt install libncurses5-dev flex build-essential bison libssl-dev bc make
$ cd linux
```

I don't think it's necessary to navigate to the <code>$HOME</code> directory to perform the installation, but I prefer to do so.

● Prepare the default kernel configuration: <code>$HOME/linux/.config</code>. Please refer to <a href="https://www.raspberrypi.com/documentation/computers/linux_kernel.html#native-build-configuration" title="Build configuration" target="_blank">this official section</a>. 🙏 The present working directory is <code>$HOME/linux</code>. Run the following commands:

```
$ KERNEL=kernel8
$ make bcm2711_defconfig
```

The last output lines of the second command are:

```
...
#
# configuration written to .config
#
```

● Check real-time configuration items in <code>/home/behai/linux/.config</code>. Open <code>/home/behai/linux/.config</code> and look for the following real-time entries:

```
...
CONFIG_PREEMPT_BUILD=y
# CONFIG_PREEMPT_NONE is not set
# CONFIG_PREEMPT_VOLUNTARY is not set
CONFIG_PREEMPT=y
# CONFIG_PREEMPT_RT is not set
CONFIG_PREEMPT_COUNT=y
CONFIG_PREEMPTION=y
# CONFIG_PREEMPT_DYNAMIC is not set
...
```

Based on my previous <a href="#background-failed-attempts">failed attempts</a>, I want to ascertain that <code>PREEMPT_RT</code> is not turned on. And indeed, it is not.

<a id="proc-config-localversion"></a>
⓺ Customise the kernel version using <code>LOCALVERSION</code>. Please refer to <a href="https://www.raspberrypi.com/documentation/computers/linux_kernel.html#native-customisation" title="Customise the kernel version using LOCALVERSION" target="_blank">this official section</a>.

In <code>/home/behai/linux/.config</code>, locate the <code>LOCALVERSION</code> entry, which should be:

```
CONFIG_LOCALVERSION="-v8"
```

And update it to:

```
CONFIG_LOCALVERSION="-v8-behai-rt-build"
```

In the next section on <a href="#proc-config-menuconfig"><code>menuconfig</code></a>, we will verify that this manual update <a href="#proc-config-localversion-confirm">takes effect</a>.

<a id="proc-config-menuconfig"></a>
⓻ Using the UI tool <code>menuconfig</code> to configure the kernel to Fully Preemptible Kernel (Real-Time). Please refer to <a href="https://www.raspberrypi.com/documentation/computers/linux_kernel.html#menuconfig" title="menuconfig" target="_blank">this official section</a>. 🙏 The present working directory is <code>$HOME/linux</code>.

-- Please note that this UI tool also updates the <code>$HOME/linux/.config</code> file.

Run the command:

```
$ make menuconfig
```

If everything goes well, and it should, you will get the UI shown below:

{% include image-gallery.html list=page.gallery-image-list-3 %}
<br/>

Use the up and down arrow keys to move between the vertical entries, use the left and right arrow keys to move between the horizontal entries at the bottom of the screen. Press the Enter key to select the highlighted item. Activate the <code>&lt; Load &gt;</code> menu item. The following pop-up appears:

{% include image-gallery.html list=page.gallery-image-list-4 %}
<br/>

Select <code>&lt; Ok &gt;</code> to confirm using the <code>$HOME/linux/.config</code> configuration file, which has been loaded by default.

Activate the first menu item <code>General setup ---&gt;</code>. On the next screen, select <code>Preemption Model (Preemptible Kernel (Low-Latency Desktop))  ---&gt;</code> as shown below:

{% include image-gallery.html list=page.gallery-image-list-5 %}
<br/>

In the pop-up dialog, select <code>( ) Fully Preemptible Kernel (Real-Time)</code> as per the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-6 %}
<br/>

The main screen should show <code>Preemption Model (Fully Preemptible Kernel (Real-Time))  ---&gt;</code> as per the following screenshot:

{% include image-gallery.html list=page.gallery-image-list-7 %}
<br/>

<a id="proc-config-localversion-confirm"></a>
Recall that in a <a href="#proc-config-localversion">previous section</a>, we customised the kernel version <code>LOCALVERSION</code>. The third entry in the previous screen confirms this manual customisation as shown below:
 
{% include image-gallery.html list=page.gallery-image-list-8 %}
<br/>

Save the changes and exit <code>menuconfig</code>. 💥 As a precaution, rerun <code>menuconfig</code> to confirm that your changes were saved.

👉 As a final verification, ensure that <code>CONFIG_PREEMPT_RT</code> is updated to <code>y</code>. Open <code>/home/behai/linux/.config</code> and look for the following real-time entries:

```
...
# CONFIG_PREEMPT_NONE is not set
# CONFIG_PREEMPT_VOLUNTARY is not set
# CONFIG_PREEMPT is not set
CONFIG_PREEMPT_RT=y
CONFIG_PREEMPT_COUNT=y
CONFIG_PREEMPTION=y
...
```

<a id="proc-kernel-native-build"></a>
⓼ We now discuss the actual kernel build process.

● Install kernel headers. Please refer to <a href="https://www.raspberrypi.com/documentation/computers/linux_kernel.html#kernel-headers" title="Kernel headers" target="_blank">this official section</a>. Run the following commands:

```
$ cd $HOME
$ sudo apt install linux-headers-rpi-v8
$ cd linux
```

● Build the kernel. Please refer to <a href="https://www.raspberrypi.com/documentation/computers/linux_kernel.html#native-build" title="Build" target="_blank">this official section</a>. 🙏 The present working directory is <code>$HOME/linux</code>.

My Pi 4B has 8GB of RAM and 4 cores. The build process takes around 2 hours. To determine the number of cores, run the command:

```
$ nproc
```

We use the number of cores in the build command:

```
$ make -j4 Image.gz modules dtbs
```

It takes a few hours. We can do something else in the meantime, but keep an eye on it.

<a id="proc-install-newly-built-kernel"></a>
⓽ Install the newly built kernel. Please refer to <a href="https://www.raspberrypi.com/documentation/computers/linux_kernel.html#native-install" title="Install the kernel" target="_blank">this official section</a>. 🙏 The present working directory is still <code>$HOME/linux</code>.

● First, install the kernel modules onto the boot media:

```
$ sudo make -j4 modules_install
```

● Then, install the kernel and Device Tree blobs into the boot partition, backing up the original kernel with the commands listed below. Please recall that the temporary environment variable <code>$KERNEL</code> is defined in <a href="#proc-config-kernel">this step</a>. If you were interrupted and had to turn off the computer or terminated the SSH session, you will need to set it again.

```
$ sudo cp /boot/firmware/$KERNEL.img /boot/firmware/$KERNEL-backup.img
$ sudo cp arch/arm64/boot/Image.gz /boot/firmware/$KERNEL.img
$ sudo cp arch/arm64/boot/dts/broadcom/*.dtb /boot/firmware/
$ sudo cp arch/arm64/boot/dts/overlays/*.dtb* /boot/firmware/overlays/
$ sudo cp arch/arm64/boot/dts/overlays/README /boot/firmware/overlays/
```

<a id="proc-reboot-verify"></a>
⓾ Finally, reboot to ensure that the OS works 😂 and the kernel is indeed a <code>Fully Preemptible Kernel (Real-Time)</code> kernel.

To reboot:

```
$ sudo reboot
```

Ping should respond successfully:

```
$ ping picnc.local
```

SSH should work:

```
$ ssh behai@picnc.local
```

The response I received was:

```
Linux picnc 6.6.59-rt45-v8-behai-rt-build+ #1 SMP PREEMPT_RT Sat Nov  2 10:20:46 AEDT 2024 aarch64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Nov  2 12:03:31 2024
```

Please note the tokens <strong><code>6.6.59-rt45-v8-behai-rt-build+</code></strong> and <strong><code>PREEMPT_RT</code></strong> in the first line. We have successfully built and installed a <code>Fully Preemptible Kernel (Real-Time)</code> kernel. ✔️ I also ran the commands to query the kernel information as discussed in a <a href="#proc-install-pre-made-os-query-kernel-info">prior section</a>.

<a id="proc-xrdp"></a>
💥 As a final note on this OS, the open-source Remote Desktop Protocol server <a href="https://www.xrdp.org/" title="an open-source Remote Desktop Protocol server" target="_blank">xrdp</a> does not seem to work properly. <strong>After writing the</strong> <a href="#proc-install-pre-made-os">initial OS image</a>, I installed this <code>xrdp</code> server, but Windows Remote Desktop Connection just shows a blank black screen. A few days prior, I tried this same image, but the release date was 04/July/2024, as seen in the screenshot below:

{% include image-gallery.html list=page.gallery-image-list-9 %}
<br/>

And Remote Desktop Connection worked perfectly. Raspberry Pi updated this image while I was still trying to resolve this <code>Fully Preemptible Kernel (Real-Time)</code> issue.

<a id="background"></a>
❷ As mentioned at the beginning, in this section I'm discussing why I have looked into this issue. I am interested in learning CNC, and my goal is to build my own CNC machine. I know nothing about CNC and electronics. I have been doing a little bit of basic physical computing with the Pi 4B using Python. In the process, I have learned some basic electronics as well.

My initial research on CNC pointed to the <a href="https://www.machsupport.com/software/mach3/" title="Mach3 CNC machine controller" target="_blank">Mach3 CNC machine controller</a>, which runs on Windows. Further research led me to <a href="http://www.linuxcnc.org/docs/html/getting-started/system-requirements.html" title="LinuxCNC" target="_blank">LinuxCNC</a>, which I found to be a more attractive option, especially since it can run on a Raspberry Pi computer. It became apparent that we need a real-time kernel.

<a id="background-source-info-01"></a>
⓵ My initial source of information is a 6-year-old YouTube series, <a href="https://www.youtube.com/playlist?list=PLaamliiI72ntlrHKIFjh2VjmehRGgZpjm" title="LinuxCNC for the Hobbyist by Mr. Joe Hildreth" target="_blank">LinuxCNC for the Hobbyist</a>, by Mr. Joe Hildreth. The 17th video, <a href="https://www.youtube.com/watch?v=RjTfKF7gcIo&list=PLaamliiI72ntlrHKIFjh2VjmehRGgZpjm&index=17" title="Compiling a Realtime Kernel for LinuxCNC" target="_blank">Compiling a Realtime Kernel for LinuxCNC</a>, discusses building a real-time kernel. I found the accompanying written tutorial, <a href="https://myheap.com/cnc-stuff/linuxcnc-emc2/92-my-heap-articles/computer-numerical-control/linuxcnc/written-tutorials/198-compiling-a-realtime-kernel-for-linuxcnc.html" title="Compiling a Realtime Linux kernel with the preemp-rt kernel patch" target="_blank">Compiling a Realtime Linux kernel with the preemp-rt kernel patch</a>, much easier to follow.

<a id="background-source-info-02"></a>
⓶ My second source of information is a 2-year-old LinuxCNC forum post titled <a href="https://forum.linuxcnc.org/9-installing-linuxcnc/47662-installing-linuxcnc-2-9-on-raspberry-pi-4b-with-preempt-rt-kernel?start=0" title="Installing LinuxCNC 2.9 on Raspberry Pi 4B with Preempt-RT kernel" target="_blank">Installing LinuxCNC 2.9 on Raspberry Pi 4B with Preempt-RT kernel</a>.

<a id="background-failed-attempts"></a>
⓷ I will not go into the details of my failed attempts to build a real-time kernel. However, between the instructions, I had about 6 tries over the span of 12 days 😂, and despite successfully building and installing, the kernel only showed <code>PREEMPT</code>, not <code>PREEMPT_RT</code>.

On my last failed attempt, I went ahead and installed <a href="http://www.linuxcnc.org/docs/html/getting-started/system-requirements.html" title="LinuxCNC" target="_blank">LinuxCNC</a> anyway. A variation of it was installed successfully, and I was able to run it via Remote Desktop Connection as shown below:

{% include image-gallery.html list=page.gallery-image-list-10 %}
<br/>

<a id="background-break-through"></a>
⓸ This nearly 3-year-old Stack Overflow post, <a href="https://stackoverflow.com/questions/71645509/raspberry-pi4-kernel-64bit-with-rt-extension" title="Raspberry pi4: kernel 64bit with RT extension" target="_blank">Raspberry pi4: kernel 64bit with RT extension</a>, addresses the very same problem I had, and the author managed to solve it. This post eventually led me to the previously mentioned Raspberry Pi official page, <a href="https://www.raspberrypi.com/documentation/computers/linux_kernel.html" title="The Linux kernel" target="_blank">The Linux kernel</a>, and this successful build and installation.

Compiling the Linux kernel is not my cup of tea. However, I wouldn't say my failed attempts were a waste of time. I have learned many things during these exercises, and some of the steps are similar to the final successful attempt.

<a id="background-concluding-remarks"></a>
⓹ This has been a new and interesting experience for me. I have learned quite a few things during this process. I am not sure if I can achieve my goal, as I have done some research into hardware, and there are many things I have no knowledge of. But I keep my fingers crossed...

Thank you for reading. I hope you find the information in this post useful. Stay safe, as always.

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
