---
slug: credential-stuffing/
title: 'My Favorite Password: "123456"'
date: 2020-09-25
subtitle: You could be a victim of Credential Stuffing
category: techniques
tags: credential, password, web, application, cybersecurity, business
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330841/blog/credential-stuffing/cover_t0zcnj.webp
alt: Photo by Cookie the Pom on Unsplash
description: I wrote this post to give you an overview of the Credential
  Stuffing attack and some short recommendations for its prevention.
keywords: Credential Stuffing, Credential, Password, Website, Application,
  Cybersecurity, Attack, Technique
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/siNDDi9RpVY
---

Data leakage is a daily occurrence phenomenon, or at least that’s what
I’ve read about. Lists of user/password pairs are stolen from various
places on the Internet. Those mountains of information are then offered
and sold in the '[dark web](../dark-web).' They are the required
resources to be used in *Credential Stuffing*, the kind of attack we’re
going to discuss in this post.

This form of attack consists of the large-scale automation of login
attempts on chosen websites, hoping that any of them will be successful
in gaining access to a user account and then violate their privacy, act
on their behalf, or steal from them. In addition to the lists of usually
thousands of user/password pairs to be tested, also called *Combo lists*
or just *Combos*, it is necessary to possess software that works for the
cybercriminal in an automated way.

Thus, contrary to what the attackers have to do in [Password
Cracking](../pass-cracking/), in this case, they don’t have to guess
passwords. They already have at their disposal the credentials to be
tested. It seems to be a piece of cake, as well as something effective,
especially when people have the naive habit of using the same passwords
on different websites or applications. So, the attacker doesn’t have to
be a hacker; they could be just [script
kiddies](https://en.wikipedia.org/wiki/Script_kiddie) to perform
credential stuffing.

The skilled hackers are those that, exploiting vulnerabilities, can
steal and decrypt the databases of credentials. They then decide if they
give them away to the world or offer and sell them in closed
communities. The more recent the leaked combo, the more valuable it can
be for anyone interested in this kind of crime.

So, once the script kiddies have access to a usually big list of
credentials, they need a program that works for them. It will check
every user and its corresponding password against a previously selected
web application (without knowing if they will achieve anything there) to
identify those that successfully log in. If there’s a match with an
existing account, we can say that this one has been cracked. The tool
would save that user/password pair along with the others that were also
successful in the combo. From there, the attackers would proceed
according to their purposes.

## What about tools?

<div class="imgblock">

![Pomeranian](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330839/blog/credential-stuffing/pome_rt79wj.webp)

<div class="title">

Figure 1. [Photo](https://unsplash.com/photos/gySMaocSdqs)
by Cookie the Pom on Unsplash

</div>

</div>

Nowadays, although some experienced crackers use their scripts, there
are tools (seemingly not free) exclusively designed for credential
stuffing. We can easily find tips and tutorials on how to use them on
the Internet. Some of the most popular programs are **Sentry MBA** and
**STORM**. However, more recently, **SNIPR** has emerged with similar
functionalities, but apparently with greater stability and a more
intuitive interface.

The tools to employ in this kind of attack should have the ability to
bypass diverse security mechanisms. For example, *some* websites have
protection against massive login attempts from the same IP address. This
behavior tends to be suspicious and associated with cracking by the web
application’s owners. That’s why in these cases, the credential stuffing
tool usually incorporates lists of proxies that simulate requests from
several sites on the Internet, thus ensuring anonymity and non-stop
automation.

Even with proxies, large numbers of login requests in short periods can
draw attention (though not always). Here’s when the mature and patient
attackers (not desperate teenagers) can perform slow credential stuffing
with few requests for a day. However, it could take months for them to
test thousands of pairs of the combo list. That gives time for users to
change their passwords and make those leaked databases lose value.

Having a combo list, a tool, and proxies, the attackers commonly need to
find and buy configurations or plugins to attack particular web
applications or websites. The programs have some of them for free, but
skilled hackers cleverly have built an additional market where they
offer and sell other plugins to those attackers who have no idea how to
make them. That’s another way for them to make a profit.

<div class="imgblock">

![Words by
(background image on
)](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330839/blog/credential-stuffing/jasny_eyxl97.webp)

<div class="title">

Figure 2. Words by [Mateusz
Jasny](https://medium.com/@mtjasny/how-to-deal-with-credential-stuffing-attacks-c1456e499093)
(background image on [wallhaven](https://wallhaven.cc/w/q6q92r))

</div>

</div>

## Any recommendation for prevention?

### For users

Do not reuse passwords. Try to make sure that there are marked
differences between the passwords you use. Modify them continuously and
in a creative way. You can create patterns for helping your memory, but
I don’t mean just adding intuitive prefixes or suffixes. It’d be
something like passphrases with words you easily remember, with peculiar
variations for each account, not forgetting the use of any symbols,
numbers, and capital letters. Of course, you can use password managers
like [1Password](https://1password.com/) or
[LastPass](https://www.lastpass.com/) when you think there are many
passwords to remember and keep safe.

### For web application managers

First of all, give the previous paragraph’s advice to your users (do you
*know* them? You should). Additionally, check their passwords against
those that have appeared in known breaches. You can use
[HaveIBeenPwned](https://haveibeenpwned.com/) and lists like the
[top 1000
leaked](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-1000.txt)
to identify publicly exposed credentials, and although they are not the
most recent data, they can serve as a warning to your users.

Regarding login requests, it is foolish not to pay attention to the user
traffic and login trends on your website, and especially if they are out
of regular preliminary patterns — which can be more substantial through
the
[fingerprinting](https://cheatsheetseries.owasp.org/cheatsheets/Credential_Stuffing_Prevention_Cheat_Sheet.html#device-fingerprinting)
technique. Those times when you see multiple IP addresses in action as
something unusual (perhaps due to proxies in credential stuffing), you
can also use geolocation and find out if the countries or regions to
which those IPs belong correspond to those places from which your
application is typically accessed. You could send emails to those users
to guarantee that they were the ones who tried to gain access.

It is important that you establish countermeasures to potential attacks
and thus let attackers know that they may waste time and effort with
your web application. You could start by considering even simple
solutions such as
[Fail2ban](https://www.fail2ban.org/wiki/index.php/Main_Page) for
blocking IP addresses when many failed requests are generated from a
single one. [CAPTCHA](https://en.wikipedia.org/wiki/CAPTCHA) may be an
additional countermeasure, and [reCAPTCHA
v3](https://developers.google.com/recaptcha/docs/v3), which is easy to
integrate into the applications, is usually more recommended these days
to differentiate between bots and humans.

A slightly more advanced and recommended strategy to prevent credential
stuffing is the [Multi-Factor
Authentication](https://en.wikipedia.org/wiki/Multi-factor_authentication).
This security solution could indeed affect, to some extent, your 'users'
journey' in your application while they respond with every evidence
(factor) required for information access. For this reason, you should be
very careful, and preferably choose to use this method in cases of
suspected attack or in circumstances where the user requires sensitive
data.

Finally, and after considering the prior low-cost options to hinder the
attackers' efforts, you can also call on commercial services against
credential stuffing such as [Cloudflare Bot
Management](https://www.cloudflare.com/es-es/products/bot-management/)
and [F5 Bot
Management](https://www.f5.com/solutions/application-security/bot-management).
Always keeping in mind that "No silver bullet exists so be wary of any
company who tries to sell you one"
([Overson](https://medium.com/@jsoverson/10-tips-to-stop-credential-stuffing-attacks-db249cac6428)).

> It was from a text in
> [Nivel4](https://blog.nivel4.com/noticias/que-es-el-credential-stuffing-o-relleno-de-contrasenas/)
> that I decided to read more about credential stuffing. To better
> understand the subject, you could also read the posts on Medium that I
> used as references to build this entry:
> [CK](https://medium.com/@costask/the-economics-of-credential-stuffing-attacks-c2dd5f77a48e),
> [jbron](https://medium.com/@jbron/credential-stuffing-how-its-done-and-what-to-do-with-it-57ad66302ce2),
> [Jasny](https://medium.com/@mtjasny/how-to-deal-with-credential-stuffing-attacks-c1456e499093),
> and Overson
> [(1)](https://medium.com/@jsoverson/3-misunderstandings-about-credential-stuffing-attacks-3526c618a8d6)
> [(2)](https://medium.com/@jsoverson/10-tips-to-stop-credential-stuffing-attacks-db249cac6428).
