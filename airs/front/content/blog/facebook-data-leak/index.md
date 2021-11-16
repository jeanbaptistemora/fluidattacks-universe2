---
slug: facebook-data-leak/
title: Facebook Data Leak? Again?
date: 2021-04-09
subtitle: About 533 million user phone numbers now for 'free'
category: attacks
tags: cybersecurity, software, vulnerability, mistake, hacking, application
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330872/blog/facebook-data-leak/cover_u38ho9.webp
alt: Photo by Barefoot Communications on Unsplash
description: This post outlines the most recent Facebook data leak
  with approximately 533 million records, including users' phone numbers,
  now posted for free.
keywords: Facebook, Data, Leak, Breach, Scraping, Vulnerability,
  Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/z2M7JefmTEw
---

A few days ago, someone published the phone numbers and other account
information of hundreds of millions of Facebook users on a cybercrime
forum. We’re talking about information that is now 'free' but which had
been circulating on the web months before and that even Facebook refers
to as material extracted from its platform in 2019. This case comes in
addition to several previous ones that have cast serious doubt on this
widely used social network’s security. Let’s take a look\!

If you were asked why you use Facebook, what would you answer (that is
if you use it)? Perhaps your reason wouldn’t be too far from the funny
remark expressed by [Gewirtz in
ZDNet](https://www.zdnet.com/article/new-poll-shows-facebooks-severe-trust-problem/):
"We all use Facebook because it’s the only way we can know what people
we haven’t talked to in years have eaten for dinner." But, whatever your
reason for using it, have you been aware of its security and user data
handling issues? One of the most mentioned incidents has been [the
Cambridge Analytica
scandal](https://en.wikipedia.org/wiki/Facebook%E2%80%93Cambridge_Analytica_data_scandal),
where Facebook shared the data of millions of its users without their
consent to that British company, mainly for political advertising. Apart
from this, there have been cases of [harvesting of user email
contacts](https://www.zdnet.com/article/facebook-harvested-1-5-million-user-email-contacts-without-permission/)
without permission, [passwords stored in plain
text](https://www.zdnet.com/article/facebook-we-stored-hundreds-of-millions-of-passwords-in-plain-text/),
and, well, information leaks, our concern here.

On this occasion, the information that has been made public corresponds
to [533,313,128 Facebook
users](https://www.bleepingcomputer.com/news/security/533-million-facebook-users-phone-numbers-leaked-on-hacker-forum/).
Apparently, almost all the records include the user’s ID (a long number
linked to the account), name, gender, and a piece of information that
makes this situation more alarming: their phone number. We can also find
data such as the user’s email address, relationship status, date of
birth, occupation, city, among others, in some records. These data are
part of the user profiles, and the passwords have not been exposed.
However, phone numbers, now public, are information that usually remains
private within accounts.

<div class="imgblock">

![Founders in data leak](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330871/blog/facebook-data-leak/founders_hnumfx.webp)

<div class="title">

Figure 1. [Facebook’s founders in data
leak](https://www.bleepingcomputer.com/news/security/533-million-facebook-users-phone-numbers-leaked-on-hacker-forum/).

</div>

</div>

In this database, the affected users are separated by country (although
Africa is listed, perhaps referring to South Africa). The threat
actor(s) registered 106 nations ([the list may
show 107](https://threadreaderapp.com/thread/1349671294808285184.html),
but there’s an error with Tunisia appearing twice) and specified the
total number of users for each of them. For instance, in rounded
figures, the U.S. has 32.3M records; Colombia, 18.0M; Mexico, 13.3M;
Peru, 8.1M; Chile, 6.9M; and Panama, 1.5M.

Currently, those are 106 separate download packages in a public
cybercrime forum. Nevertheless, [as Cimpanu in The Record
says](https://therecord.media/phone-numbers-for-533-million-facebook-users-leaked-on-hacking-forum/),
"While the forum is publicly accessible and anyone can register a
profile, the download links for these packages are only available to
users who bought forum credits." Specifically, [it is
said](https://www.bleepingcomputer.com/news/security/533-million-facebook-users-phone-numbers-leaked-on-hacker-forum/)
that any person must pay eight credits to access the database, with each
credit costing approximately $2.19. This is pretty cheap for the amount
of information available; that’s why people say it’s "free data" in
almost all the sources I checked.

Typically, these stolen data sets are initially sold privately at high
prices. Later, they are sold at lower costs, and, in the end, they are
given for free by their owners mostly to gain reputation within the
hacker community. In this case, the stolen information corresponds,
especially [according to Facebook
itself](https://about.fb.com/news/2021/04/facts-on-news-reports-about-facebook-data/),
to the same data that malicious actors harvested from its platform in 2019.
[Abrams in BleepingComputer says](https://www.bleepingcomputer.com/news/security/533-million-facebook-users-phone-numbers-leaked-on-hacker-forum/)
it was in mid-2020 when this stolen information came to light in a
hacker community with one member selling it to other members. Later, in
January 2021, Hudson Rock’s CTO [Alon Gal tweeted
that](https://twitter.com/UnderTheBreach/status/1349674272227266563) "a
user created a Telegram bot allowing users to query the database for a
low fee, enabling people to find the phone numbers linked to a very
large portion of Facebook accounts." Finally, at the beginning of this
month, [Gal tweeted
that](https://twitter.com/UnderTheBreach/status/1378314424239460352)
those "Facebook records were just leaked for free."

But what happened to Facebook to have all that information from ["about
a
fifth"](https://therecord.media/phone-numbers-for-533-million-facebook-users-leaked-on-hacking-forum/)
of its complete user pool leaked? Several sources refer to a
vulnerability in the 'Add Friend' feature on Facebook that hackers could
have exploited. ["It is unknown
if](https://www.bleepingcomputer.com/news/security/533-million-facebook-users-phone-numbers-leaked-on-hacker-forum/)
this alleged vulnerability allowed the threat actor to retrieve all of
the information in the leaked data or just the phone number, which was
then combined with information scraped from public profiles," says
Abrams. It was from there that criminals could have created the database
of 533M users.

[Facebook, on the other
hand](https://about.fb.com/news/2021/04/facts-on-news-reports-about-facebook-data/),
does not mention vulnerability or hacking in its public statement. They
believe that only the 'scraping' technique was used by criminals to
extract user data before September 2019, employing their 'contact
importer' feature. Facebook created this function for people to easily
find their friends on the network (supposedly getting limited but public
information from the profiles) using their contact lists (phone
numbers). Apparently, after realizing how some individuals were using
this characteristic, the company decided to change it and resolve the
situation. "We updated it to prevent malicious actors from using
software to imitate our app and upload a large set of phone numbers to
see which ones matched Facebook users," says Clark, Facebook’s Product
Management Director.

Interestingly, on September 4, 2019, [Whittaker in TechCrunch
reported](https://techcrunch.com/2019/09/04/facebook-phone-numbers-exposed/)
many Facebook users' phone numbers (linked to IDs and other data)
recently exposed online. Expressly, he referred to an exposed,
unprotected server (["not a Facebook
one"](https://www.forbes.com/sites/daveywinder/2019/09/05/facebook-security-snafu-exposes-419-million-user-phone-numbers/?sh=2e0ad5901ab7))
with more than 419M records. On that occasion, the U.S. had 133M
records, about four times more than in the 'most recent case.' At that
time, Facebook said malicious actors scraped that data before they
restricted access to users' phone numbers on their platform, i.e., *more
than a year ago*. ["Until
April 2018](https://edition.cnn.com/2019/09/04/tech/facebook-phone-numbers-exposed),
people could enter another person’s phone number to find him or her on
Facebook." But, wait a minute, didn’t they say users could do this up
until August 2019? That doesn’t add up\! And while there may be
discussions about this inconsistency, nobody mentioned it in the posts I
had the opportunity to review.

<div class="imgblock">

![,
Director, Strategic Response Communications at
Facebook.](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330871/blog/facebook-data-leak/lizb_mqlyam.webp)

<div class="title">

Figure 2. [Tweet by Liz
Bourgeois](https://twitter.com/Liz_Shepherd/status/1378398417450377222),
Director, Strategic Response Communications at Facebook.

</div>

</div>

The thing now is that, for this 533M records situation, people are
talking about "old data" from 2019, leaked from a problem that Facebook
"resolved" in August of the same year. However, even if the data is
around two years old, it can still be valuable to cybercriminals. Phone
numbers and email addresses are often the same over many years. Threat
actors can then engage in phishing (with email addresses), smishing
(mobile text phishing), SIM swap attacks (["steal multi-factor
authentication](https://www.bleepingcomputer.com/news/security/533-million-facebook-users-phone-numbers-leaked-on-hacker-forum/)
codes sent via SMS"), and other scams or impersonation attacks.
Therefore, if you use Facebook, you should beware of strange messages
with requests for further information or enclosed links, possibly even
associated with the pandemic.

By the way, since Facebook seems not to have made it available,
[haveibeenpwned.com](https://haveibeenpwned.com/) allows you to check if
you’re part of the victims of this data leak. Initially, this page only
allowed verification via email address. But this data is quite limited
in quantity in this leak ([only for 2.5M of the affected
users](https://www.bleepingcomputer.com/news/security/how-to-check-if-your-info-was-exposed-in-the-facebook-data-leak/)),
so, a few days ago, [the website enabled the search through phone
numbers](https://www.troyhunt.com/the-facebook-phone-numbers-are-now-searchable-in-have-i-been-pwned/#comment-5332905964).
Good luck\!
