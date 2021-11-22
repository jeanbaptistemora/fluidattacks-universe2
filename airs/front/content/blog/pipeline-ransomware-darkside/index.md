---
slug: pipeline-ransomware-darkside/
title: Don't Give Yourself to the Darkside
date: 2021-05-14
subtitle: The gang that hit Colonial Pipeline with ransomware
category: attacks
tags: cybersecurity, software, vulnerability, hacking, social-engineering, risk
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1621039654/blog/pipeline-ransomware-darkside/cover_cyypaa.webp
alt: Photo by Tommy van Kessel on Unsplash
description: America is talking about the DarkSide ransomware attack against
  Colonial Pipeline, one of the largest USA pipeline companies.
  Here is what we know about it.
keywords: Ransomware, Cybersecurity, Vulnerability, Software, Darkside,
  Colonial Pipeline, Ethical Hacking, Pentesting
author: Felipe Zárate
writer: fzarate
name: Felipe Zárate
about1: Cybersecurity Editor
source: https://unsplash.com/photos/_sDlQf6f7gc
---

In this blog, we will not delve into Colonial Pipelines, though we will
mention some details about them. Instead, our spotlight will be the
self-appointed criminal gang called DarkSide, which was behind the
attack. How they operate, who they are, and, more importantly, how can
your company avoid becoming a victim of such an attack?

## What happened?

The FBI confirmed that on May 7th, the Colonial Pipeline networks were
attacked by the [DarkSide
ransomware](https://www.fbi.gov/news/pressrel/press-releases/fbi-statement-on-compromise-of-colonial-pipeline-networks)
gang. After that, the company [closed its complete
network](https://www.reuters.com/technology/fireeye-shares-jump-after-pipeline-cyberattack-2021-05-10/)
for some days. In fact, until the date this post is published, [the main
pipeline is still
shut](https://www.usatoday.com/story/news/nation/2021/05/12/colonial-pipeline-hack-shutdown-gas-outages-refuel/5065013001/).
However, [it was
known](https://www.bloomberg.com/news/articles/2021-05-13/colonial-pipeline-paid-hackers-nearly-5-million-in-ransom)
that the company already paid $5 million in cryptocurrency [to decrypt
locked
systems](https://www.zdnet.com/article/colonial-pipeline-paid-close-to-5-million-in-ransomware-blackmail-payment/?ftag=TRE-03-10aaa6b&bhid=29868913901264489308848757891800&mid=13366532&cid=2399622965).
(Which seems insignificant compared to the [$15 million coverage that
their cyber-security insurance can
cover](https://www.reuters.com/business/energy/colonial-pipeline-has-cyber-insurance-policy-sources-2021-05-13/)).

## Who are involved?

The Colonial Pipeline network [transports almost
half](https://www.bbc.com/news/technology-57063636) of the East Coast’s
fuel supply. This is why [prices at the pumps
increased](https://www.cbsnews.com/news/colonial-pipeline-resumes-operations-cyberattack/)
after the long-lasted cut. In total, [the pipeline network is 5,500
miles
long](https://www.wsj.com/articles/why-the-colonial-pipeline-shutdown-is-causing-gasoline-shortages-11620898203),
which makes it the longest in the country (see Figure 1).

<div class="imgblock">

![Figure 1](https://res.cloudinary.com/fluid-attacks/image/upload/v1621039653/blog/pipeline-ransomware-darkside/image1_xfinzi.webp)

<div class="title">

Figure 1. [Colonial
Pipeline.](https://www.wsj.com/articles/why-the-colonial-pipeline-shutdown-is-causing-gasoline-shortages-11620898203).

</div>

</div>

The pipeline’s primary source is in Texas, the state where, by far,
stands the most significant number of refineries. While [Texas has more
than 20 refineries with a total capacity less than a million barrels a
day, the whole East Coast has only
seven](https://www.wsj.com/articles/why-the-colonial-pipeline-shutdown-is-causing-gasoline-shortages-11620898203#:~:text=According%20to%20an%20Energy%20Department,a%20million%20barrels%20a%20day.).
Therefore, a disruption in the flow from that state has paralyzed
operations in several sectors ([including seven of the largest airports
in the country and five military
bases](https://www.reuters.com/business/energy/us-govt-top-fuel-supplier-work-secure-pipelines-closure-enters-4th-day-2021-05-10/);
see Figure 2).

<div class="imgblock">

![Figure 2](https://res.cloudinary.com/fluid-attacks/image/upload/v1621039652/blog/pipeline-ransomware-darkside/image2_myicaj.webp)

<div class="title">

Figure 2. [Pipelines
flow.](https://www.reuters.com/business/energy/us-govt-top-fuel-supplier-work-secure-pipelines-closure-enters-4th-day-2021-05-10/).

</div>

</div>

Let’s talk about **DarkSide**. It looks like they became public [in
August
of 2020](https://www.bleepingcomputer.com/news/security/darkside-new-targeted-ransomware-demands-million-dollar-ransoms/),
and they were discovered [by
MalwareHunterTeam](https://heimdalsecurity.com/blog/what-is-darkside-ransomware/)
(see Figure 3). DarkSide is perhaps [one of the most important exponents
of the rising
Ransomware-as-a-Corporation](https://www.digitalshadows.com/blog-and-research/darkside-the-new-ransomware-group-behind-highly-targeted-attacks/)
(RaaC) trend. They differ from other ransomware criminal groups in their
victims' search method. An ordinary criminal uses spoofing,
[smishing](../smishing/), or [phishing](../phishing/), waiting for a
victim to take the bait. Instead, DarkSide studies its potential victims
carefully by determining its economic activity, income, and expenses.
After that, they analyze the attack difficulty, its success probability
and inquire about the company’s most vulnerable point to start their
attack from there. Unlike well-known criminal groups such as
DoppelPaymer, Sodinokibi,
[Maze](https://statescoop.com/maze-ransomware-attackers-leak-data-stolen-from-suburban-washington-schools/),
and NetWalker, DarkSide is structured around a "[business
model](https://www.cnbc.com/2021/05/10/hacking-group-darkside-reportedly-responsible-for-colonial-pipeline-shutdown.html)."
In addition, it is noticeable that [they have a code of
ethics](https://www.cybereason.com/blog/cybereason-vs-darkside-ransomware)
that prohibits them from attacking hospitals, schools, and government
agencies. [It is also reported
that](https://www.bbc.com/news/technology-54591761) they look to obtain
the most significant profit by attacking big companies. At the same
time, [they make donations using some of the money received through
ransomware](https://www.bbc.com/news/technology-54591761). For example,
they gave 10 thousand dollars to Children International and another 10
thousand dollars to the Water Project Receipt in October 2020. Both of
them were rejected by the NGO’s.

<div class="imgblock">

![Figure 3](https://res.cloudinary.com/fluid-attacks/image/upload/v1621039653/blog/pipeline-ransomware-darkside/image3_cqph45.webp)

<div class="title">

Figure 3. [DarkSide
leaks.](https://www.bloomberg.com/news/articles/2021-05-12/darkside-hackers-mint-money-with-ransomware-franchise).

</div>

</div>

## How did it happen?

DarkSide infiltrated the Colonial Pipeline network by blocking data from
their computers and servers. To unblock their data, the company must pay
the money criminals asked for. Specifically, they [stole 100 gigabytes
of data threatening to share it on the
web](https://www.bloomberg.com/news/articles/2021-05-09/colonial-hackers-stole-data-thursday-ahead-of-pipeline-shutdown).
Besides, though details are not precise, [their modus operandi
starts](https://www.trendmicro.com/en_us/research/21/e/what-we-know-about-darkside-ransomware-and-the-us-pipeline-attac.html)
with (but is not limited to) a [phishing](../phishing/) email that
tricked an employee. Likewise, by using [penetration
testing](../importance-pentesting/) tools, [they can perform lateral
movements](https://www.csoonline.com/article/3618688/darkside-ransomware-explained-how-it-works-and-who-is-behind-it.html?upd=1620908660505).
In addition, [it can be assumed
that](https://www.nytimes.com/2021/05/10/us/politics/pipeline-hack-darkside.html)
the attack was directed to the commercial area and not the operational
one. Apparently, their goal was not to crash down the pipeline but to
extort the company to make money (as has been done in [previous
cases](https://www.zdnet.com/article/darkside-the-ransomware-group-responsible-for-colonial-pipeline-cyberattack-explained/)).
In this sense, their main attack is not so different from the typical
ransomware attack.

DarkSide gets data from their victims' servers, encrypts them, uploads
them to their leak-website (which can only be accessed by search engines
that allow you to enter the [deep web](../dark-web/) as Tor), and then
asks for the money to decrypt them. The encryption is twofold; first,
they use a [SALSA20
key](https://www.mcafee.com/enterprise/en-us/threat-center/threat-landscape-dashboard/ransomware-details.darkside-ransomware.html),
one of the fastest encryption on the market, and then use an RSA-1024
key. Then, [they
withdraw](https://www.bleepingcomputer.com/news/security/darkside-new-targeted-ransomware-demands-million-dollar-ransoms/)
data servers and disable the [termination of specific
processes](https://github.com/k-vitali/Malware-Misc-RE/blob/master/2020-08-21-crime_darkside_ransomware.vk.notes.raw).
Finally, every file [extension changes to
.DarkSide](https://heimdalsecurity.com/blog/what-is-darkside-ransomware/)
and any of them open [an executable that redirects to .txt with the
following
text](https://www.pcrisk.com/removal-guides/18504-darkside-ransomware):

<div class="imgblock">

![Figure 4](https://res.cloudinary.com/fluid-attacks/image/upload/v1621039652/blog/pipeline-ransomware-darkside/image4_syrgzj.webp)

<div class="title">

Figure 4. "Welcome to Dark."

</div>

</div>

[The gang lists all types of stolen data and
sends](https://malwarewarrior.com/how-to-remove-darkside-ransomware-and-decrypt-darkside-files/)
a "personal website" URL to their victim. Data is already loaded and
expected to be published automatically if the company does not pay
before the deadline. If that is not enough, they also threaten to delete
that information from the victim’s network. In fact, in a press release
posted on a Tor website in August 2020, [they announce
that](https://www.digitalshadows.com/blog-and-research/darkside-the-new-ransomware-group-behind-highly-targeted-attacks/).

<div class="imgblock">

![Figure 5](https://res.cloudinary.com/fluid-attacks/image/upload/v1621039652/blog/pipeline-ransomware-darkside/image5_vxa4nd.webp)

<div class="title">

Figure 5. "If you refuse to pay."

</div>

</div>

## What have we learned?

[President Biden himself
said](https://edition.cnn.com/videos/politics/2021/05/10/colonial-pipeline-white-house-biden-sot-vpx.cnn/video/playlists/this-week-in-politics/)
he is now very interested in the cyberattack situation. In fact, on
Wednesday, May 12th, [the White House released an Executive
Order](https://www.whitehouse.gov/briefing-room/presidential-actions/2021/05/12/executive-order-on-improving-the-nations-cybersecurity/)
in which they declare that the Federal Government is going to: "improve
its efforts to identify, deter, protect against, detect, and respond to
these actions and actors." The extensive document is clearly motivated
by the DarkSide attack, but also by recent ones (surely the [hack to
Microsoft Exchange Server](../exchange-server-hack/), the [SolarWinds
security fiasco](../solarwinds-attack/), or the [Facebook Data
Leak](../facebook-data-leak/)).

This means US law enforcement ["are likely to be putting significant
resources into uncovering" their
identity](https://grahamcluley.com/darkside-ransomware-gang-fear/). So,
it should not be surprising that Congressman Jim Langevin (D-RI), chair
of the House Armed Services Subcommittee on Cybersecurity, Innovative
Technologies, and Information Systems [has
said](https://langevin.house.gov/press-release/langevin-praises-sweeping-biden-executive-actions-cybersecurity):
"Cybersecurity is the most urgent national security challenge facing our
nation, and I applaud President Biden for taking action early in his
term to address and eliminate glaring vulnerabilities."

For all this, it seems that DarkSide regrets the social harm caused by
their criminal activity. We can assume that not only for their "ethical
code" but also because they are now in the limelight. In this respect,
what Nicole Perlroth, a New York Times cybercrime reporter, said last
[Monday](https://twitter.com/nicoleperlroth/status/1391794316507418624?s=20)
turns very interesting:

<div class="imgblock">

![Figure 6](https://res.cloudinary.com/fluid-attacks/image/upload/v1621039653/blog/pipeline-ransomware-darkside/image6_bsbosm.webp)

<div class="title">

Figure 6. [@nicoleperlroth](https://twitter.com/nicoleperlroth).

</div>

</div>

We also learned that ransomware can jeopardize [companies and the
infrastructure](https://www.zdnet.com/article/colonial-pipeline-ransomware-attack-everything-you-need-to-know/)
of an entire country. This means, in turn, that companies and
governments must reinforce their cybersecurity systems. Because
[**they’re not paying enough attention to these
risks**](https://www.osti.gov/biblio/1602649): "the ONG (Oil & Natural
Gas) industry is unaware of potentially useful technologies that have
been developed for ensuring cyber-security of other infrastructure
systems, such as the electric grid."

[Robert Smallwood was one of the
consultants](https://www.secureworldexpo.com/industry-news/colonial-pipeline-poor-cybersecurity)
who delivered an 89-page report in January 2018 after conducting a
six-month audit. He said last Wednesday that the deficiencies and
vulnerabilities in the cybersecurity system were so high that "[an
eighth-grader could have hacked into that
system](https://apnews.com/article/va-state-wire-technology-business-1f06c091c492c1630471d29a9cf6529d)."
All of this resulted in a costly and embarrassing lesson: prevention in
terms of cybersecurity risks is very important. Never take it lightly.
Otherwise, there will be no guarantee that you will not be attacked by
the DarkSide.

For now, we’ll just recommend you what they say throughout the Galaxy:
may the force be with you.

If you want to know more about how to protect yourself from
cyberattacks, we invite you to review our page.

At `Fluid Attacks` we are specialized in cybersecurity through
[Pentesting](../../solutions/penetration-testing/) and [Ethical
Hacking](../../solutions/ethical-hacking/).
For more information, don’t hesitate to [contact
us\!](../../contact-us/)
