---
slug: thoughtless-reporting/
title: Thoughtless Vulnerability Reporting
date: 2021-01-29
subtitle: The Colombian Foreign Ministry faced a big trouble
category: opinions
tags: cybersecurity, vulnerability, information, web, risk, standard
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331106/blog/thoughtless-reporting/cover_j9r5l2.webp
alt: Photo by Jono Hirst on Unsplash
description: Here I give you an overview of the recent Colombian Foreign
  Ministry's security problem and the inadequate disclosure
  of such vulnerability in the media.
keywords: Vulnerability, Ministry, Foreign, Visa, Data, Web,
  Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/dKS6CQZ5mgo
---

Assume you set out to check and download your visa through the
corresponding federal agency website in a country where you’re a
foreigner. Then, amid your curious behavior, to your surprise, you
realize that you can do something you are not supposed to be able to do
on that website. It turns out that you can see and download many other
people’s visas just by making a small change at the end of the URL. What
do you think you should do in this kind of situation? To whom should you
tell this, assuming, of course, that you do not intend to be a
cybercriminal?

Well, such a scenario was [recently
faced](https://www.dw.com/es/colombia-falla-inform%C3%A1tica-expone-datos-de-550000-personas-extranjeras/a-56245939)
by a foreign individual who was about to check his visa (i.e.,
identification document as a foreigner) on the Colombian electronic visa
platform. According to the Colombian news [website La Silla
Vacía](https://lasillavacia.com/) (LSV) [on
Twitter](https://twitter.com/lasillavacia/status/1350221344231796747),
it was on **January 13** when this citizen with a fresh opportunity to
work in this South American country discovered the platform’s issue.
Specifically, this man could access a link through a QR code attached to
his digital visa. And, from there, by changing the final numbers of that
link, he could see and obtain not just his but other people’s visas on
PDF without any restriction.

Perhaps this citizen hadn’t the foggiest idea of the magnitude of the
snag. An estimated **550,000** people had their data in that vulnerable
information system at that time. Therefore, from any of them, our
individual could obtain data such as the following: photograph, full
name, date of birth, nationality, passport number, and job position. By
the way, would this man actually be the first to notice this pitfall?
How long ago did this vulnerability exist? Days, months? Questions with
no answers shared publicly so far, it seems.

Anyway, following up on what was communicated on Twitter by LSV, our
individual in question decided to write emails to the embassy, from
where he got no solution, and then to the Ministry of Foreign Affairs,
to receive no response. How the hell could that be possible? Okay, I
forget for the moment that *slow request processing* is easy to find in
the bureaucracy almost anywhere. Afterward, the individual allegedly
initiated communication with LSV, and they were able to witness the
security weakness on the electronic visa platform.

That day, **January 15**, these journalists, apart from doing so on
social networks, published [on their
website](https://lasillavacia.com/bache-seguridad-amenazo-los-datos-extranjeros-y-cancilleria-no-sabia-79749)
'EVERYTHING' that was known so far about the issue. What did they do
with their reckless conduct? They brought Christmas early for many
malicious hackers, chiefly in Latin America. LSV revealed a
cybersecurity vulnerability for which there was no implemented solution
at that time. Though censoring URLs and people’s information, they gave
a gif showing the platform error. Were they not aware of the harm they
could be doing? Or were they just hurriedly thinking about their profits
as a media outlet? Again, unanswered questions.

Nevertheless, LSV communicated by chatting the imbroglio to the
appropriate authorities at the Ministry. This entity then said to LSV
that it would soon remediate the vulnerability and, hours later,
published a terse [official
bulletin](https://www.cancilleria.gov.co/newsroom/news/cancilleria-informa-falla-sistema-informacion-plataforma-visas-electronicas)
on the subject (see Figure 1). However, it seems they did not suggest
LSV remove the posts that were not far from looking like cybercrime
incentives. Data that by law is supposed to be protected was at the
mercy of many cunning individuals with obscure intentions of committing
frauds such as identity theft and extortion. The next day (I don’t know
how much time they disabled the platform service), the Technology
Directorate closed the breach, and the Ministry distributed [a new
bulletin](https://www.cancilleria.gov.co/newsroom/news/cancilleria-informa-fue-solucionada-superada-falla-presentada-sistema-informacion),
only one sentence long.

<div class="imgblock">

![Report](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331105/blog/thoughtless-reporting/report_wlm92j.webp)

<div class="title">

Figure 1. Taken from [cancilleria.gov.co](https://www.cancilleria.gov.co/newsroom/news/cancilleria-informa-falla-sistema-informacion-plataforma-visas-electronicas).

</div>

</div>

How many attackers could have taken advantage of this vulnerability?
What image of Colombia’s national security does this event provide to
foreigners? [Are there
similar](https://www.enter.co/empresas/seguridad/la-falla-de-la-cancilleria-colombiana-que-expuso-miles-de-visas/)
problems in this government’s systems (using the same technology) that
have not been solved? Engaging questions, although I would like to keep
focused on the vulnerability reporting issue at this point.

As [Oakley for
GlobeLiveMedia](https://globelivemedia.com/a-computer-error-by-the-colombian-foreign-ministry-made-the-visas-of-some-550000-foreigners-public/)
said, some other people were also rejecting the publication by LSV. I
repeat: they could have been calling for cybercrime\! Their behavior was
not appropriate or judicious in terms of disclosing an IT system
vulnerability. However, before that, our individual should not have gone
beyond failed communication with a couple of authorities to share his
findings with a journalistic group. As suggested by Rafael Alvarez,
`Fluid Attacks'` CTO, this man should have tried repeatedly to establish
a conversation with the Ministry. Finding no response or being ignored,
his next step should have been to contact an intermediary, such as the
police.

Or, in his possible ignorance of what to do, why not resort to Google?
This individual could easily have found the [colCERT
website](http://www.colcert.gov.co/), where people in Colombia can
report cybercrime and related incidents. (Although, for example,
[Carolina
Botero](https://www.elespectador.com/opinion/la-importancia-de-reportar-fallos-en-sistemas-informaticos-del-estado/),
director of the Karisma Foundation, disqualifies this site for the
appropriate reporting of vulnerabilities.) However, already in the hands
of the media, continually looking for traffic generation, we could
hardly expect responsible handling of this kind of data. "Unfortunately
—as Rafael said—, the search for fame by newspapers or pseudo-hackers
always takes prisoner the common good, which in reality is what matters
most here." LSV should have transmitted the event to the authorities and
then waited long enough for the problem to be resolved before publishing
the story. Those affected had to be informed in detail later, but mainly
by the organization responsible for their data storage.

Reading the
[ISO/IEC 29147:2018](https://www.iso.org/standard/72311.html) (about
which I may emphasize more on a future occasion), a standard concerning
'vulnerability disclosure,' we find the following: "The goal of
vulnerability disclosure is to reduce the risk associated with
exploiting vulnerabilities." Reduce the risk\! In the end, in this case,
none of the parties involved succeeded in doing so. It is real that the
Ministry made a mistake with its IT infrastructure that kept the data of
thousands of foreigners on exposure. But, for their part, the
journalists made the situation public, conveying an implicit message:
*these people are in deep trouble, but it doesn’t matter if they get
screwed even more; the right to information (and our recognition) must
be above other principles*.

Finally, as Rafael said, opportunities for improvement for organizations
such as the Ministry arise in cases like this one where there were
technical or methodological security failures. It is also true that
companies responsible for their security should pay more attention to
the management of reports and the implementation of standards (see ISO’s
'[IT Security](https://www.iso.org/ics/35.030/x/)'). In general, we
could overcome the lack of knowledge on vulnerability reporting with,
for instance, what
[Botero](https://www.elespectador.com/opinion/la-importancia-de-reportar-fallos-en-sistemas-informaticos-del-estado/)
recommended: the establishment of an easily accessible state-coordinated
disclosure channel for the secure and transparent transmission of
information.

If you find yourself in a situation similar to that of the
aforementioned foreign citizen, do not forget the following: **(1)**
Accessing third parties' sensitive data is a crime. **(2)** There are
intermediaries such as the police who can help. **(3)** Social networks
are not the right place to report a vulnerability. On the other hand,
all of us should strive to be more aware of the harm our actions can
cause to others. That would be a good start to respond to some signs of
unheeded moral principles.
