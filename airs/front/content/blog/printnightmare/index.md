---
slug: printnightmare/
title: Come To Your Senses Already!
date: 2021-08-18
subtitle: And apply the patches to avoid the PrintNightmare
category: attacks
tags: windows, vulnerability, exploit, mistake, software, hacking
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1629328080/blog/printnightmare/cover_printnightmare_nmy9z1.webp
alt: Photo by Mathew MacQuarrie on Unsplash
description: You can read this post to learn about the nightmare that started
  to emerge within Windows months ago, which may affect many of its users,
  including you.
keywords: Printnightmare, Microsoft, Windows, Cybersecurity, Vulnerability,
  Ransomware, Pentesting, Ethical Hacking
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/u6OnpbMuZAs
---

When it comes to cybersecurity, few things can be more perilous than to
be asleep at the wheel. Every day, a great number of new vulnerabilities
appear. In 2020, for example, there was apparently [an average of 50 per
day](https://www.securitymagazine.com/articles/94602-record-number-of-critical-and-high-severity-vulnerabilities-were-logged-to-the-nist-nvd-in-2020).
However, patches continually emerge to close them. The problem arrives
when people fail to consider them, thus increasing their risk of getting
screwed. It is not uncommon to see a person or firm who inadvertently
falls asleep and ends up losing in this field. But the most peculiar of
all is that now that loss can also be provoked by a nightmare.

## What kind of nightmare are we referring to?

About two months ago, Microsoft warned about and released an out-of-band
patch (i.e., [a fix
published](https://whatis.techtarget.com/definition/out-of-band-patch)
at a time other than the regular release time) for **PrintNightmare**, a
security flaw. This bug that initially seemed to involve *two*
vulnerabilities,
[CVE-2021-34527](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-34527)
and
[CVE-2021-1675](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-1675),
allows attackers to take control of PCs. The issue lies specifically in
the Windows [Print
Spooler](https://docs.microsoft.com/en-us/windows/win32/printdocs/print-spooler)
(spoolsv.exe), a printing management service ["enabled by
default](https://www.semperis.com/blog/what-you-need-to-know-about-printnightmare-the-critical-windows-print-spooler-vulnerability/)
in all Windows clients and servers." As long as that first patch and the
subsequent ones are [not applied to the client
systems](https://www.zdnet.com/article/install-immediately-microsoft-delivers-emergency-patch-for-printnightmare-security-bug/)
that keep the service active, attackers will have code to exploit.

In general, we can understand PrintNightmare as a [remote code
execution](https://encyclopedia.kaspersky.com/glossary/remote-code-execution-rce/)
(RCE) vulnerability based on operations improperly performed with
privileged files by the mentioned Windows service. Therefore, attackers
exploiting such a flaw [can execute malicious
code](https://encyclopedia.kaspersky.com/glossary/remote-code-execution-rce/)
with system privileges inside the target device without physical access.
Moreover, they can install software, steal, modify or remove
information, or "create new accounts with full user rights," [according
to
Microsoft](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-34527).

[As Cimpanu
commented](https://therecord.media/poc-released-for-dangerous-windows-printnightmare-bug/)
for The Record in late June, a part of PrintNightmare (at least that one
with ID 1675) was at that time the latest of many Print Spooler-related
findings. It turns out that this bug had been discovered earlier this
year by several researchers. Microsoft already had the patch for all its
users to update their systems. However, the snag arose when supposedly
by an "accident," technical details of the bug and a
[proof-of-concept](https://encyclopedia.kaspersky.com/glossary/poc-proof-of-concept/)
exploit ended up being shared on GitHub by analysts from a Chinese
security firm. This information was online for just a few hours, but it
was enough to be cloned by different users. From there, it reappeared
later in the public domain.

Since then, it was known that this vulnerability could affect all
versions of the Windows operating system, even those now rarely used,
such as Vista and XP. The nightmare started to get darker when several
researchers reported that the patch delivered by Microsoft was
insufficient. Apparently, it *only* repaired that "part" 1675
([privilege
escalation](https://encyclopedia.kaspersky.com/glossary/privilege-escalation/)
vulnerability) but not "part" 34527 (RCE vulnerability), both of which
were initially grouped as if they were a single security flaw. Hence,
Microsoft requested users to disable the service, ["especially on
Windows
servers](https://therecord.media/poc-released-for-dangerous-windows-printnightmare-bug/)
running as domain controllers from where attackers can pivot to entire
internal networks." Days later, in early July, the second patch was
released, [surprisingly even for
Windows 7](https://www.zdnet.com/article/install-immediately-microsoft-delivers-emergency-patch-for-printnightmare-security-bug/),
which had lost general support more than a year ago. Microsoft
recommended its installation asap.

After Microsoft deployed patches for other versions of Windows ([printer
driver installation
restrictions](https://support.microsoft.com/en-us/topic/kb5005010-restricting-installation-of-new-printer-drivers-after-applying-the-july-6-2021-updates-31b91c02-05bc-4ada-a7ea-183b129578a7)
were becoming manifest), [there were
complaints](https://www.zdnet.com/article/get-updating-microsoft-delivers-printnightmare-patch-for-more-windows-versions/)
that they did not provide sufficient protection. Ideas from researchers
began to be made public about how the patches Microsoft had already
submitted to close PrintNightmare could be bypassed. It was not until
the first half of this month that authors like [Todd from
SecureWorld](https://www.secureworld.io/industry-news/author/drew-todd)
were able to say something like the following: ["Now,
Microsoft](https://www.secureworld.io/industry-news/microsoft-printnightmare-vulnerability)
has finally fixed the vulnerability."

At first, it was curious to see that the security flaw Todd referred to
in his post as PrintNightmare had been
[CVE-2021-36958](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-36958),
a different ID than those we saw above. However, [Microsoft recently
reported](https://msrc-blog.microsoft.com/2021/08/10/point-and-print-default-behavior-change/)
that there are really several vulnerabilities that together receive that
name. (Today, it seems, [they are
about 10](https://therecord.media/printnightmare-vulnerability-weaponized-by-magniber-ransomware-gang/).)
Another, for example, is the
[CVE-2021-34481](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2021-34481).
It was in relation to this design flaw that [Microsoft exposed its new
solution
approach](https://msrc-blog.microsoft.com/2021/08/10/point-and-print-default-behavior-change/)
on August 10. It is about changing the default behavior of the Windows
[Point and
Print](https://docs.microsoft.com/en-us/windows-hardware/drivers/print/introduction-to-point-and-print)
feature. In a nutshell, [as Cimpanu
said](https://therecord.media/microsoft-to-require-admin-rights-before-using-windows-point-and-print-feature/),
"While until now, any user could add a new printer to a Windows
computer, \[from now on\], only admin users will be able to add or
update a printer with drivers from a remote print server."

<div class="imgblock">

![MacQuarrie](https://res.cloudinary.com/fluid-attacks/image/upload/v1629334804/blog/printnightmare/macquarrie_qow9ny.webp)

<div class="title">

Figure 1. Photo by [Mathew
MacQuarrie](https://unsplash.com/@matmacq?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
on [Unsplash](https://unsplash.com/photos/KFdIgwm8HTs).

</div>

</div>

## Now ransomware weaponized with the nightmare?

Despite all the effort, the nightmare cannot come to an end as long as
many remain asleep. Meanwhile, others take advantage of it. More than a
month ago, [Kaspersky pointed
out](https://www.kaspersky.com/blog/printnightmare-vulnerability/40520/)
that cybercriminals could use PrintNightmare to carry out [ransomware
attacks](../ransomware/). Well, that’s indeed what has happened. Since
mid-July, the group of malicious hackers behind the [Magniber
ransomware](https://blog.malwarebytes.com/threat-analysis/2017/10/magniber-ransomware-exclusively-for-south-koreans/)
is [leveraging this
bug](https://therecord.media/printnightmare-vulnerability-weaponized-by-magniber-ransomware-gang/)
(especially 34527) to breach Windows systems, [mainly in South
Korea](https://www.crowdstrike.com/blog/magniber-ransomware-caught-using-printnightmare-vulnerability/).

[According to Palmer in
ZDNet](https://www.zdnet.com/article/ransomware-now-attackers-are-exploiting-windows-printnightmare-vulnerabilities/),
another group that has begun to attack taking quick advantage of
PrintNightmare is Vice Society, which appeared recently in June. They
use "double extortion attacks, stealing data from victims and
threatening to publish it if the ransom isn’t paid." Apparently, their
victims include small and medium-sized organizations, mainly educational
institutions.

Certainly, these are not the only threat actors resorting to the
nightmare for their benefit. And, no doubt, the number of ransomware
groups seeking to infect unpatched systems is likely to grow soon. At
present, what we must do to avoid this nightmare is to *wake up* and
apply all available patches as soon as possible. Individuals and
organizations must always stay vigilant and up-to-date with Windows
security updates to reduce critical risks and prevent falling victim to
harmful attacks.

From `Fluid Attacks`, we invite you to remember that these are just a
*few* vulnerabilities that may be identified within your systems. If you
want to discover all the security flaws that, if exploited, could lead
your company to catastrophe, do not hesitate to [contact
us](../../contact-us/).
