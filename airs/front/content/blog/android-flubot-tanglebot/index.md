---
slug: android-flubot-tanglebot/
title: Your Phone Is All Eyes and Ears
date: 2021-10-11
subtitle: Android devices are catching FluBot and TangleBot
category: attacks
tags: android, cybersecurity, credential, flaw, social-engineering, risk
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1633991486/blog/android-flubot-tanglebot/cover_android.webp
alt: Photo by Markus Winkler on Unsplash
description: Read this post to learn about two Android malware campaigns.
  FluBot fools its victims using clever lures and
  TangleBot can be used to spy on the victims.
keywords: Android, Flubot, Tanglebot, SMS, Malware, App,
  Smishing, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/j2MRdUmr1SU
---

Malware campaigns have been terrorizing Android users across the world
this year. Here, we will talk about two ongoing campaigns that have been
spreading through SMS messages: FluBot in Europe, the UK and New
Zealand, and TangleBot in the US and Canada.

## A different kind of Spanish flu

A few days ago, New Zealand’s Computer Emergency Response Team (CERT NZ)
released an
[alert](https://www.cert.govt.nz/individuals/news-and-events/parcel-delivery-text-message-infecting-android-phones/)
in which they warned about FluBot malware affecting Android phones. The
victims had received an SMS message that tricked them into downloading
the malware. The CERT NZ reported that "The wording of the text messages
may be about a parcel delivery or that photos of the recipient have been
uploaded or a voicemail. In all cases there will be a link, asking you
to install an app or a security update."

FluBot was already known [in
Europe](https://www.proofpoint.com/us/blog/threat-insight/flubot-android-malware-spreading-rapidly-through-europe-may-hit-us-soon#)
and [the
UK](https://www.zdnet.com/article/this-password-stealing-android-malware-is-spreading-quickly-heres-watch-to-watch-out-for/)
since April and apparently hit [Spain
first](https://twitter.com/ThreatFabric/status/1346807894860300288), in
late 2020. Even before it expanded out of Spain, four suspects [were
arrested](https://therecord.media/flubot-malware-gang-arrested-in-barcelona/)
in Barcelona on suspicion of distributing the malware. Clearly, that
didn’t stop its spreading. Apart from being written in the respective
languages of each country, the messages are like the ones currently
spreading in New Zealand. The user gets infected with FluBot when they
install the application. After that, it can access the phone contacts
list and keep on spreading. But, as it’s usual in [smishing
attacks](../smishing/), the main function of FluBot is to reveal the
victim’s credentials to the attacker. It produces [overlay
screens](https://www.lifewire.com/what-is-screen-overlay-4176177)
(screens that appear on top of another application in use) resembling
login pages of legitimate banking applications, or a Google Play
verification screen asking for credit card information, and proceeds to
collect the sensitive information typed by the victim.

As for how FluBot transmits the data, it uses [domain generation
algorithms](https://blog.malwarebytes.com/security-world/2016/12/explained-domain-generating-algorithm/).
Basically, it constantly switches to new domain names where it can meet
the attacker and pass on the information.

The fact that it keeps changing its lures makes FluBot a resistant kind
of sickness. Most recently, FluBot is trying to fool users by telling
them that they’ve [already been
infected](https://threatpost.com/flubot-malware-targets-androids-with-fake-security-updates/175276/).
It prompts the user to tap on "Install security update" in order to
remove the malware, only to really get infected.

<div class="imgblock">

![FluBot screen](https://res.cloudinary.com/fluid-attacks/image/upload/v1633991393/blog/android-flubot-tanglebot/Android-Figure-1.webp)

<div class="title">

Figure 1. Screen prompting to download FluBot. Source: [cert.gov.nz.](https://www.cert.govt.nz/assets/Uploads/images/Flubot-install-page.png)

</div>

</div>

## Update Flash Player? Sure, why not?!

A more recent malware, and arguably more dangerous, is TangleBot. It was
[discovered last
month](https://www.cloudmark.com/en/blog/mobile/tanglebot-new-advanced-sms-malware-targets-mobile-users-across-us-and-canada-covid-19)
by researchers at Proofpoint. Some of the SMS messages crafted to spread
it act as notifications about COVID-19 vaccination appointments or new
regulations; others falsely inform about potential local power outages.
The message provides a legit-looking link. When the user taps on it, the
game is on.

Probably the first noticeable red flag is that the user is presented
with a request to update Adobe Flash Player in order to visualize the
content. As the success of this campaign has proven, many people are not
aware or are too distracted to remember that, starting this year, Adobe
[stopped
supporting](https://www.adobe.com/products/flashplayer/end-of-life.html)
Flash Player and hasn’t supported it anyways on Android devices
[since 2012](https://community.adobe.com/t5/flash-player-discussions/flash-player-for-android-phones/td-p/9954925).
There. Inform your loved ones.

A second red flag should be that the user is asked to go to Settings and
allow the installation of applications from unknown sources. Once
installed, this fake Flash Player (henceforth, TangleBot) asks to have
full control of the device. And it means just that. Take a quick look at
Figure 2. Those are the permissions requested by TangleBot.

<div class="imgblock">

![TangleBot permissions](https://res.cloudinary.com/fluid-attacks/image/upload/v1633991394/blog/android-flubot-tanglebot/Android-Figure-2.webp)

<div class="title">

Figure 2. Permissions requested by TangleBot. Source:
[proofpoint.com](https://www.proofpoint.com/sites/default/files/inline-images/image-20211001134835-14.png)

</div>

</div>

From the user’s side of the story, they have surrendered their device
configuration settings, functionalities and information to TangleBot.
Now, from the attacker’s side, it’s a matter of communicating with the
malware to gain access. They do this by sending cryptic messages to the
device through social media messaging. The messages may seem like
gibberish but, to the malware, they are orders. Once connected to the
device, the attacker goes into full surveillance mode. As
[reported](https://www.proofpoint.com/us/blog/threat-insight/mobile-malware-tanglebot-untangled)
by the researchers, "The control afforded by the malware allows for the
monitoring and recording of all aspects of user activity, including
websites visited, collection of typed passwords, audio and video from
the microphone/camera, and can harvest data including SMS activity and
stored content."

Just like Flubot, TangleBot can generate overlay screens resembling
login pages of known applications and access the victim’s contacts to
propagate by sending SMS messages to them. But one of the
characteristics that has been found to set TangleBot apart from other
malware is that it allows the attacker to record audio and stream it in
their systems. This poses the risks of identity theft and impersonation.
In relation to this, the researchers also highlight the possibility of
attackers dialing costly premium services, resulting in financial loss
for the victim.

Finally, a characteristic that earned TangleBot its name is the
complexity of techniques that it uses to hide its functionality and
prevent being detected by anti-malware software. This behavior is
commonly known as
"[obfuscation](https://www.zdnet.com/article/a-question-of-security-what-is-obfuscation-and-how-does-it-work/)."
The [researchers
say](https://www.proofpoint.com/us/blog/threat-insight/mobile-malware-tanglebot-untangled),
"The malware uses various obfuscating techniques including hidden .dex
files \[into which Android programs are compiled\], modular and
functional design characteristics, minified code, and excessive unused
code. Taken together, this is a tangled mess of code that is both
difficult and timely to dissect."

## Any tips other than not tapping?

In [our post](../blog/smishing/) about smishing, we advise to avoid
opening links in SMS messages and to contact the supposed sender through
their official communication channels instead. But, of course, we’ve
learned a few other things from the malware campaigns we described here.
Namely, beware of any application asking you to allow the installation
of applications from unknown sources and always make sure to check the
permissions an application requests. Oh\! And remember that you won’t be
needing Adobe Flash Player\!
