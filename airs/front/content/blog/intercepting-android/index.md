---
slug: intercepting-android/
title: Intercepting Android
date: 2019-10-23
category: hacking
subtitle: Intercept applications in newer Android phones
tags: security, android, application, pentesting
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330925/blog/intercepting-android/cover_d3ec8a.webp
alt: 'Turned on Android smartphone. Photo by Pathum Danthanarayana on Unsplash:
  https://unsplash.com/photos/t8TOMKe6xZU'
description: Android is one of the most suitable targets for hackers.
  Here we show how to intercept Android apps' web traffic
  by installing a self-signed certificate.
keywords: Android, Security, Intercept, Hacking, Proxy, Application,
  Ethical Hacking, Pentesting
author: Jonathan Armas
writer: johna
name: Jonathan Armas
about1: Systems Engineer, Security+
about2: '"Be formless, shapeless like water" Bruce Lee'
source: https://unsplash.com/photos/t8TOMKe6xZU
---

`Android` is an operating system based on the `Linux` kernel and used by
mobile devices such as smartphones and tablets. Due to its popularity,
it is the major target for hackers. One of their common techniques is to
intercept and try to break an app’s web traffic using attack methods
like fuzzing and brute force.

Mobile applications usually share the same communication structure as
web applications, meaning that we can intercept requests by using a
proxy. If an application is using a secure channel like HTTPS, we are
going to have to install a digital certificate into the phone in order
to make it accept our proxied requests.

Since Android 7 Nougat ([API
\>= 24](https://android-developers.googleblog.com/2016/07/changes-to-trusted-certificate.html))
we can no longer use the simple method of setting our proxy and the
certificate to capture `HTTPS` traffic as the `Burpsuite` page explains
[here](https://support.portswigger.net/customer/portal/articles/1841102-installing-burp-s-ca-certificate-in-an-android-device).
If we try this method, we will receive thousands of certificate failures
from our proxy. This is because the Android operating system no longer
trusts certificates installed by the user.

To solve this we need to have a rooted `Android` smartphone, then create
and sign a digital certificate, and finally put it in the system’s
certificate folder in our phone.

In order to intercept the application’s traffic we are going to need
some tools. The tools that we are going to use are:

- [Burpsuite](https://portswigger.net/burp)

- [OpenSSL](https://www.openssl.org/source/)

- [Android Studio](https://developer.android.com/studio)

## Creating the certificate

So what is a `TLS CA certificate`? When you communicate with a third
party using a secure channel like `HTTPS`, the `SSL` (Secure Socket
Layer) protocol and the `TLS` (Transport Layer Security) protocol
include a security measure called digital certificates that implements
asymmetric encryption by using a private and public key.

In this protocol, a public key is signed by the `CA` (Certificate
Authority) using their private key. This way a certificate provides a
link between the public key and the `CA` that signed that key. The
following process is how a connection works:

1. The browser connects to the server using a secure protocol.

2. The server responds with the digital certificate containing the
    server’s public key.

3. The browser looks to see if the `CA` from the certificate is
    included on its trusted list of `CA’s`. This is where we will work.

4. Once the browser verifies that the `CA` from the certificate is in
    its trusted list of `CA’s`, it uses the public key provided in `(2)`
    to create a session key.

5. Finally, the browser and the server encrypt data over the connection
    using the session key.

Having a `CA-issued` digital certificate with its public keys stored on
the trusted list indicates to a cellphone that it can *"trust"* the
proxy `HTTPS` responses. Without this, we cannot intercept secure
channel traffic. As we don’t have a `CA` we are going to create a
self-signed one.

First, we generate the certificate with 3650 days of validity and using
a `SHA256` hash. It will also request some information. We can put our
personal/company information here or leave it blank:

**Generating the certificate.**

``` bash
openssl req -x509 -days 3650 -nodes -newkey rsa:2048 -outform der -keyout fluidattacks.key -out fluidattacks.der -extensions v3_ca
Generating a RSA private key

writing new private key to 'fluidattacks.key'

You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.

Country Name (2 letter code) [AU]:CO
State or Province Name (full name) [Some-State]:Antioquia
Locality Name (e.g., city) []:Medellin
Organization Name (e.g., company) [Internet Widgits Pty Ltd]:Fluid Attacks
Organizational Unit Name (eg, section) []:Fluid Attacks
Common Name (e.g., server FQDN or YOUR name) []:Fluid Attacks
Email Address []:continuous@fluidattacks.com
```

After generating the certificate, we have to convert it to `PEM` in
order to import it into the phone, and `DER` to import it into `burp`:

**Converting the cert.**

``` bash
openssl x509 -inform DER -outform PEM -text -in fluidattacks.der -out fluidattacks.pem
openssl rsa -in fluidattacks.key -inform pem -out fluidattacks.key.der -outform der
```

Finally, we export our key into a `PKCS8` file in order to import it to
`burp`:

**Modifying for burp.**

``` bash
openssl pkcs8 -topk8 -in fluidattacks.key.der -inform der -out fluidattacks.key.pkcs8.der -outform der -nocrypt
```

Once we have all the files, we need to start configuring our phones.

## Configuring Android

The certificates installed on the phone follow the name `HASH.0`; so we
need the hash of the certificate:

**Getting the hash.**

``` bash
openssl x509 -inform PEM -subject_hash -in fluidattacks.pem | head -1
```

After getting the hash, we create a copy of the certificate with that
hash in the name. For example, something like `49ef1764.0`:

**Renaming for Android.**

``` bash
cp fluidattacks.pem <HASH>.0
```

Then, we need to upload our certificate to the phone. We can do it
manually by connecting the phone and moving the file into a folder or
with the following command using `adb`:

**Uploading the cert.**

``` bash
adb push <HASH>.0 /data/local/tmp
```

Once the file is in the phone, log in as `root`, remount the folder
`/system` with read and write permissions (it is not mounted with those
permissions by default), copy our certificate to the
`/system/etc/security/cacerts/` folder and change its permissions and
ownership to `644` and `root:root:`

**Setting the cert.**

``` bash
adb shell
phone$ su
phone# mount -o rw,remount /system
phone# mv /data/local/tmp/<HASH>.0 /system/etc/security/cacerts/
phone# chmod 644 /system/etc/security/cacerts/<HASH>.0
phone# chown root:root /system/etc/security/cacerts/<HASH>.0
```

The last thing left to do is to restart our phone to load our changes:

**Restarting.**

``` bash
phone# reboot
```

Once we turn the phone back on, our certificate will be installed on the
system’s trusted credentials tab and the phone will accept the responses
of our proxy.

<div class="imgblock">

![Android certificate](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330921/blog/intercepting-android/android-cert_q8pnfu.webp)

<div class="title">

Figure 1. Android certificate

</div>

</div>

## Configuring the Proxy

Now we need to set our proxy in order to use our certificate. Open
`Burpsuite` and create a new project. Then move to the `Proxy` tab and
open the `Options` tab.

<div class="imgblock">

![Burp
options](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330924/blog/intercepting-android/burp-options_iwk6fc.webp)

<div class="title">

Figure 2. Burp options

</div>

</div>

The next step is to import our certificate by clicking on `Import /
export CA certificate`, then selecting `Certificate` and private key in
`DER` format, and choosing our `fluidattacks.der` and
`fluidattacks.key.pkcs8.der` files that we previously created.

<div class="imgblock">

![Import
DER](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330924/blog/intercepting-android/import-der_uo3ssz.webp)

<div class="title">

Figure 3. Import DER

</div>

</div>

<div class="imgblock">

![Choose
file](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330922/blog/intercepting-android/cert-file_l1dmwv.webp)

<div class="title">

Figure 4. Choose file

</div>

</div>

Now, we need to set our proxy in our phones. Go to `WiFi` settings,
select a shared connection between the phone and the computer; we can
use the same network that our computer is connected to or use our
computer as a mobile hotspot to share it with our phone. Then, expand
the `Advanced options`, set the `Proxy` to `Manual` and input the `IP`
address and proxy’s port.

<div class="imgblock">

![Android
Proxy](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330924/blog/intercepting-android/android-proxy_horg4w.webp)

<div class="title">

Figure 5. Android Proxy

</div>

</div>

We are now capturing secure channel requests made from our phone
applications and browsers without having problems with certificate
failures.

<div class="imgblock">

![Capture](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330923/blog/intercepting-android/capture_z1upry.webp)

<div class="title">

Figure 6. Capture

</div>

</div>

If we want to have less default traffic on our proxy, we can again
modify the `WiFi` settings of our phones and fill-in the `Bypass proxy`
input with the following domains:

**Default traffic sites.**

``` bash
*.google.com
*.googleapis.com
*.gstatic.com
```
