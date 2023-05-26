---
layout: post
title: "Ubuntu Bootable USB stick: The “elusive” 😂 “Try or Install Ubuntu” option..."

custom-css-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/css/uikit.min.css"

custom-javascript-list:
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit.min.js"
    - "https://cdn.jsdelivr.net/npm/uikit@3.14.1/dist/js/uikit-icons.min.js"

gallery-image-list:
    - "https://behainguyen.files.wordpress.com/2023/05/068-02.jpg"
    - "https://behainguyen.files.wordpress.com/2023/05/068-03.jpg"

description: My Ubuntu 22.10 no longer booted. I tried to do a reinstallation using the original bootable USB stick, but there was no “Try or Install Ubuntu” option. The BIOS USB 3.0 option setting seems to affect this behaviour.
tags:
- Ubuntu
- USB
- Installation
- Bootable
---

<em style="color:#111;">My Ubuntu 22.10 no longer booted. I tried to do a reinstallation using the original bootable USB stick, but there was no “Try or Install Ubuntu” option. The BIOS USB 3.0 option setting seems to affect this behaviour.</em>

| ![068-feature-image.png](https://behainguyen.files.wordpress.com/2023/05/068-feature-image.png) |
|:--:|
| *Ubuntu Bootable USB stick: The “elusive” 😂 “Try or Install Ubuntu” option...* |

Back in December, 2022,
my first 
<a href="https://releases.ubuntu.com/kinetic/" title="Ubuntu 22.10 (Kinetic Kudu)" target="_blank">Ubuntu 22.10 (Kinetic Kudu)</a>
installation went smoothly. 

The machine I installed it to is my old laptop, an <em>HP Pavilion 15 Notebook PC</em>,
its <code>Born On Date</code> is <code>04/October/2014</code>, the original OS was 
Windows 8.1. All USB ports are USB 2.0. The Ubuntu bootable USB stick I use is also 
USB 2.0, I purposely selected USB 2.0 for bootable USB stick.

I scrapped Windows 8.1, installing only Ubuntu 22.10.

In the laptop BIOS, I changed the boot order, moved 
<code>USB Diskette on Key/USB Hard Disk</code> as the first option:

![068-01.jpg](https://behainguyen.files.wordpress.com/2023/05/068-01.jpg)

Inserted the bootable USB stick and rebooted the machine. From thence on,
just followed the instructions in the official document 
<a href="https://ubuntu.com/tutorials/install-ubuntu-desktop#1-overview"
title="Install Ubuntu desktop" target="_blank">Install Ubuntu desktop</a>.

Third week of May, 2023; while experimenting with some configurations, 
I installed <code>SELinux</code> -- which damaged my Ubuntu 22.10.
(<code>SELinux</code> is no longer for Ubuntu 22.10, do not install it).
After this, when booted up, it just displayed the <code>GRUB</code> menu,
I can't work it out. So I decided that it is simpler just to reinstall.

I change BIOS boot option as before, using the same bootable USB stick...
There was no <code>Try or Install Ubuntu</code> option! The available 
options are:

{% include image-gallery.html list=page.gallery-image-list %}

Neither of those four (4) available options helps.

After a few hours of searching, I came across a post discussing a similar
issue, whereby the author has a single sentence which mentions that if
there is a USB 3.0 option in the BIOS, it should be set to <code>Auto</code>.
Focusing on getting my problem addressed, I forgot to write down the URL of 
the post, I could not find it for reference in this post, I do apologise 
for that. 

In my laptop BIOS, there is an <code>USB3.0 Configuration in Pre-OS</code>
and it was set to <code>Enabled</code>: <strong>this is the default setting,
it was like this the first time I installed Ubuntu 20.10</strong>:

![068-04-usb-3-enabled.jpg](https://behainguyen.files.wordpress.com/2023/05/068-04-usb-3-enabled.jpg)

I do not know why it worked at the first time! I set it to <code>Auto</code>:

![068-05-usb-3-auto.jpg](https://behainguyen.files.wordpress.com/2023/05/068-05-usb-3-auto.jpg)

This time, it does have the <code>Try or Install Ubuntu</code> option:

![068-06-install-option.jpg](https://behainguyen.files.wordpress.com/2023/05/068-06-install-option.jpg)

I am in the dark as to why it is like this... But that's how it is.
Afterward, I went to the BIOS again, set the first boot option to
<code>OS boot Manager</code>.

That's about it for this post. 
Thank you for reading. I do hope someone will find this post useful. 
Stay safe as always.
