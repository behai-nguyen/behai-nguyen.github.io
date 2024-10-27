---
layout: post
title: "Ubuntu 24.04.1 LTS (Noble Numbat): Sharing Directories Across the LAN"

description: In this guide, we describe how to make the $HOME/Public/ directory of a newly installed Ubuntu 24.04.1 LTS (Noble Numbat) available for sharing across the home network. This shared directory allows authenticated users to read and write. An example of $HOME/Public/ is /home/behai/Public/. 

tags:
- Ubuntu
- Samba
- Share 
- Directory
- Folder
---

<em>
In this guide, we describe how to make the <code>$HOME/Public/</code> directory of a newly installed <code>Ubuntu 24.04.1 LTS (Noble Numbat)</code> available for sharing across the home network. This shared directory allows authenticated users to read and write. An example of <code>$HOME/Public/</code> is <code>/home/behai/Public/</code>.
</em>

| ![124-feature-image.png](https://behainguyen.wordpress.com/wp-content/uploads/2024/10/124-feature-image.png) |
|:--:|
| *Ubuntu 24.04.1 LTS (Noble Numbat): Sharing Directories Across the LAN* |

I have performed a clean, fresh installation of <code>Ubuntu 24.04.1 LTS (Noble Numbat)</code>, replacing <code>Ubuntu 22.10 (Kinetic Kudu)</code>, which reached End of Life on July 20, 2023. I followed my own previously noted steps to share the <code>/home/behai/Public/</code> directory. The UI part of the process no longer works, but I have found another solution. I successfully shared the <code>/home/behai/Public/</code> directory, and my Windows 10 Pro can access it. I will describe step by step what I did to get it to work. 

💥 <strong>Please note</strong>: <code>behai</code> is the user created during the installation process.

⓵ Install the <code>nautilus-share</code> package by running the following commands:

```
$ sudo apt-get update -y
$ sudo apt-get install -y nautilus-share
```

These commands install the Samba <code>smbd</code> service, <code>samba-common-bin</code> version <code>2:4.19.5+dfsg-4ubuntu9</code>, and <code>acl</code> version <code>2.3.2-1build1</code>. I'm not sure what the latter two are.

To verify the <code>smbd</code> service has been installed, query its version using the command:

```
$ smbd --version
```

My installation reports <code>Version 4.19.5-Ubuntu</code>.

⓶ Add the directory to be shared to the Samba configuration. Edit the Samba configuration with the following command:

```
$ sudo nano /etc/samba/smb.conf
```

At the end of the file, add the following content:

```cfg
[Public]
comment = behai Public folder
path = /home/behai/Public
browsable = yes
guest ok = no
read only = no
create mask = 0755
```

I am matching the section name <code>[Public]</code> to the directory name <code>/Public</code>. Next, allow authenticated users full access to the shared directory with:

```
$ sudo chmod 777 Public
```

<a id="samba-password"></a>
⓷ Set the Samba password for user <code>behai</code>:

```
$ sudo smbpasswd -a behai
```

⓸ Open the Samba port:

```
$ sudo ufw allow 445
```

⓹ Restart the Samba service and check its status.

To restart:

```
$ sudo service smbd restart
```

To check the Samba status:

```
$ sudo service smbd status
```

If everything goes well, it should report <code>active (running)</code>.

⓺ On Windows 10 Pro, you can now attempt to access this newly shared Ubuntu 24.04.1 directory using Windows <code>Map network drive...</code>. The mapped folder would be <code>\\Ubuntu 24.04.1 IP Address\Public</code>, for example, <code>\\192.168.0.16\Public</code>. It will ask for credentials; use the username and password we set up in <a href="#samba-password">section ⓷</a>.

⓻ I assume the same steps can be followed to share other directories. I have not done this myself.

⓼ For further reading, please refer to the following posts and articles:

<ol>
<li style="margin-top:10px;">
<a href="https://askubuntu.com/questions/1464804/ubuntu-23-04-network-file-sharing-windows-cannot-access-ubuntu-public" title="Ubuntu 23.04 Network File Sharing / Windows cannot access \\UBUNTU\Public" target="_blank">Ubuntu 23.04 Network File Sharing / Windows cannot access \\UBUNTU\Public</a>
</li>

<li style="margin-top:10px;">
<a href="https://www.techrepublic.com/article/share-directories-lan-from-ubuntu-desktop-22-04/" title="How to share directories to your LAN From Ubuntu Desktop 22.04" target="_blank">How to share directories to your LAN From Ubuntu Desktop 22.04</a>
</li>

<li style="margin-top:10px;">
<a href="https://www.zdnet.com/article/how-to-share-folders-to-your-network-from-linux/" title="How to share folders to your network from Linux" target="_blank">How to share folders to your network from Linux</a>
</li>

<li style="margin-top:10px;">
<a href="https://medium.com/@honghiphop_37058/how-to-create-share-folder-on-ubuntu-16-04-command-line-e9a88bc49a37" title="How to create share folder on Ubuntu 18.04 by using samba(command line)" target="_blank">How to create share folder on Ubuntu 18.04 by using samba(command line)</a>
</li>

<li style="margin-top:10px;">
<a href="https://www.atlantic.net/vps-hosting/how-to-create-samba-share-on-ubuntu/" title="How to Create Samba Share on Ubuntu" target="_blank">How to Create Samba Share on Ubuntu</a>
</li>
</ol>	

Thank you for reading. I hope you find the information in this post useful. Stay safe, as always.

✿✿✿

Feature image source:

<ul>
<li>
<a href="https://www.omgubuntu.co.uk/2024/03/ubuntu-24-04-wallpaper" target="_blank">https://www.omgubuntu.co.uk/2024/03/ubuntu-24-04-wallpaper</a>
</li>

<li>
<a href="https://w7.pngwing.com/pngs/728/291/png-transparent-hard-drives-computer-icons-disk-external-storage-others-miscellaneous-electronics-floppy-disk-thumbnail.png" target="_blank">https://w7.pngwing.com/pngs/728/291/png-transparent-hard-drives-computer-icons-disk-external-storage-others-miscellaneous-electronics-floppy-disk-thumbnail.png</a>
</li>
</ul>
