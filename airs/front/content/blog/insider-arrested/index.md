---
slug: insider-arrested/
title: Liar, Liar, Pants on Fire!
date: 2021-12-13
subtitle: Insider attack suspect was arrested this month
category: attacks
tags: cybersecurity, cloud, company, credential, information, risk
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1639403262/blog/insider-arrested/cover_insider.webp
alt: Photo by Jametlene Reskp on Unsplash
description:  An individual was arrested for extorting Ubiquiti,
  the company where he worked as a developer.
  In this post,
  we narrate the key points of his attack.
keywords: Insider Threat, Vpn, Ubiquiti, Data, Arrest, Fbi, Aws,
  Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/Q79XFGuTFfM
---

A fairly recent insider attack could be adapted
as a stand-alone episode in a detective TV series:
It's got the FBI,
cybercrime and mystery;
you suspect someone from the investigation team is the bad guy;
it's revealed the criminal made some mistake that gives him away;
all the pieces fall into place,
and the episode ends with the guy being arrested.

Okay,
maybe it wouldn't be your favorite episode,
but, again,
you're a cybersecurity enthusiast
and it's got an optimistic ending,
so it's a must-see.
Sit back and read the plot.

## Rising action

The attack was centered around [Ubiquiti](https://www.ui.com/),
a New York-based technology company [known for](https://krebsonsecurity.com/2021/03/whistleblower-ubiquiti-breach-catastrophic/)
its cloud-enabled Internet of Things devices.
[In late December 2020](https://www.justice.gov/usao-sdny/press-release/file/1452706/download),
some of the company's employees found out
that a person with administrative access had been exfiltrating data
from the company's GitHub repositories.
An incident response team was formed
and they found
that the attacker had used a [Surfshark](https://surfshark.com/)
Virtual Private Network (VPN).
A VPN provides privacy by masking the user's IP address
with that of a VPN server
and encrypting their internet traffic.
At least one of the members of the team alleged
he had never used Surfshark VPN himself.

After this discovery,
senior employees at Ubiquiti got an email from the attacker
demanding a 50BTC ransom be paid
(which equaled about $1.9M at that moment)
before January 10 at midnight.
If they paid,
the extortionist would remain quiet about the breach,
give the stolen files back,
and provide information about the vulnerability he exploited
and a backdoor he installed.
[Backdoors](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-83r1.pdf)
are programs
that allow the attacker to access the host's functions and data remotely.

[Because](https://www.justice.gov/usao-sdny/press-release/file/1452706/download)
Ubiquiti didn't pay the ransom,
the attacker sent a message saying "No BTC. No talk. We done here."
With the message came a link to a public folder
containing some of Ubiquiti's proprietary data.
The company acted quickly and got the folder removed.

[On January 11](https://twitter.com/pcsecz/status/1348741883695165442),
the company finally communicated to their customers
that they became aware
that someone had gained unauthorized access to their systems
hosted by a third-party cloud provider.
Although they didn't know if user data was compromised,
they encouraged their customers to change their passwords.

## Unmasking the villain

The company,
[reportedly](https://therecord.media/former-ubiquiti-employee-charged-with-hacking-and-extorting-company/),
didn't pay the ransom and called law enforcement instead.
A suspect was identified promptly:
The man who appeared as the owner of the PayPal account
that was used to purchase the Surfshark account mentioned earlier.
In a very incriminating fashion,
the VPN connection failed during the intrusion,
which means that the intruder's real IP address was temporarily exposed.
The exfiltration of files even stopped
at the time the suspect's internet connection went down at his residence,
and resumed as his internet service was reenabled.
All the evidence pointed in the same direction\!

Who was this person?
Well,
he was one of the developers at Ubiquiti.
He was one of the guys on the incident response team\!
Really\!
One who said he had never used Surfshark\!
(Gasp\!)
It was proven
he even used his own work credentials to access the repositories.
No vulnerability exploitation was really needed nor performed.
The FBI confronted the individual on March 24
and searched his home and seized devices.
He had cloned the company's repositories on GitHub to his computer.
However,
he denied having anything to do with the incident.
He even suggested
that someone else might have used his PayPal account to pay for the VPN.

We do not know the motivations for this attack,
apart from monetary gain.
However,
[according to the investigation](https://www.justice.gov/usao-sdny/press-release/file/1452706/download),
the suspect had already applied for another job in December,
the day before the attack.

## So what's the truth?

Days after the FBI searched the suspect's residence,
[an anonymous informant](https://krebsonsecurity.com/2021/03/whistleblower-ubiquiti-breach-catastrophic/)
reached out to the media.
He said
that the claim
that the compromise involved a third-party cloud provider was a fabrication.
According to him,
the intruders had gained administrative access to Ubiquiti's servers
at Amazon Web Services (AWS).
Critically,
he informed that the company had insufficient logging
and thus could not prove nor disprove what the intruders had accessed.
So,
whether customer account credentials were compromised could not be ruled out.
With the credentials,
the adversaries might authenticate to a myriad of cloud-based devices.
He also informed that the attack was against Ubiquiti and,
instead,
they wanted to make everyone believe
the company was "merely a casualty" of the attack against AWS.
In a letter to the European Data Protection Supervisor,
the whistleblower said:
"The breach was massive,
customer data was at risk,
access to customers' devices deployed in corporations
and homes around the world was at risk."

Now,
something we all [should know](../shared-responsibility-model/)
is cloud service providers secure the underlying server hardware and software
but require the cloud tenant
to guarantee the security of any data stored there.
The whistleblower's account didn't paint a pretty picture for Ubiquiti.
After this story,
Ubiquiti's stock prices fell by approximately 20%
resulting in loss of over $4B in market capitalization.

## Happy ending scene

The FBI identified the whistleblower as the very suspect.
Yeah\!
He posed as the anonymous informant trying to mislead the public\!
But,
ultimately,
the evidence didn't help his case.
[He was fired](https://www.justice.gov/usao-sdny/press-release/file/1452706/download)
on or about April 1,
and the Department of Justice announced his arrest on December 1.
Their press release states he is charged in four separate counts:

> The first count charges him
> with transmitting a program to a protected computer
> that intentionally caused damage,
> which carries a maximum sentence of 10 years in prison.
> The second count charges transmission of an interstate threat,
> which carries a maximum sentence of two years in prison.
> The third count charges wire fraud,
> which carries a maximum sentence of 20 years in prison.
> The fourth count charges the making of false statements to the FBI,
> which carries a maximum sentence of five years in prison.
> The maximum potential sentences are prescribed by Congress
> and are provided here for informational purposes only,
> as any sentencing of the defendant will be determined by the judge.

We watch the end of the story with a bit of satisfaction,
knowing that the attacker was caught.
