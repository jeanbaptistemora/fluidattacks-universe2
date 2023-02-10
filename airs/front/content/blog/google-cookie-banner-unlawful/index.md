---
slug: google-cookie-banner-unlawful/
title: Google Cookie Banner Unlawful in EU
date: 2022-04-27
subtitle: Google is forced to give EU users a 'Reject all' option
category: politics
tags: compliance, cybersecurity, web, company
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1651084575/blog/google-cookie-banner-unlawful/cover_cookie.webp
alt: Photo by Umberto on Unsplash
description: Users in France can now reject all cookies in Google Search and YouTube more easily after these services' banners were found to break EU data privacy laws.
keywords: Cookies, Cnil, Reject All, Gdpr, Eprivacy, Google, Facebook, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/t_Fh1jzwgFM
---

In February,
[we talked about](../google-analytics-illegal/) the case of Google Analytics
being illegal in France and Austria.
Both the CNIL
(*Commission Nationale de l'Informatique et des Libertés*)
and the DSB
(*Datenschutzbehörde*),
the data protection agencies in those countries,
found that the web service was sending IP addresses
and other identifiers from users in Europe to the U.S.,
thus breaching the [GDPR](../../compliance/gdpr/)
(General Data Protection Regulation).

Something we did not mention at that time was
that in January the CNIL [fined Google and Facebook](https://www.cnil.fr/en/cookies-cnil-fines-google-total-150-million-euros-and-facebook-60-million-euros-non-compliance)
because they were making it way too cumbersome
for users to reject cookies.
(These are character strings placed in a browser's memory
in response to a requested resource
to be used on any subsequent visits or requests.)
Google and Facebook's fines were €150 million ($170 million)
and €60 million ($68 million) respectively.
Last week,
Google introduced a button in their cookie banner
that lets users in France reject all cookies without any further screens,
as easily as they can accept all cookies.
Let's look at the details.

## CNIL to defend the freedom of consent

What [happened](https://www.theverge.com/2022/4/21/23035289/google-reject-all-cookie-button-eu-privacy-data-laws)
is these companies' cookie banners were violating EU data privacy laws.
The problem was simply something we users are all too familiar with.
It's when there is a button that says "Accept all,"
or any variation of that,
but then there is no option
that makes it equally easy to reject cookies.
Instead,
the user has to go through a lengthy process of configuration.
And sometimes,
for example in [the case of Facebook](https://www.dataprotectionreport.com/2022/02/rejecting-cookies-should-be-as-easy-as-accepting-cookies-new-sanctions-by-the-french-authority-cnil/),
users are presented with a button
ambiguously labeled "Accept cookies"
after they went through the whole process
of configuring each cookie used individually,
even disabling all of them.

In its [article](https://www.cnil.fr/en/cookies-cnil-fines-google-total-150-million-euros-and-facebook-60-million-euros-non-compliance)
announcing the fines,
the CNIL backed its argument
by appealing to a psychological phenomenon.
Namely,
because users are interested in quickly consulting a website,
the asymmetry of steps required for accepting
and rejecting cookies
influences their choice in favor of consent.
This simple strategy was found to infringe Article 82
of the French Data Protection Act.

The companies not only had to pay the fines,
but they were also ordered by the CNIL
to provide Internet users located in France
with an option to reject all cookies
as simple as that to accept them all.
Cue Google's new cookie consent option.

<cta-banner
  buttontxt="Read more"
  link="/solutions/security-testing/"
  title="Get started with Fluid Attacks' Security Testing solution right now"
/>

## Reject all cookies upon the first click

The introduction of the "Reject all" button was announced last week
in a [blog post](https://blog.google/around-the-globe/google-europe/new-cookie-choices-in-europe/)
by Google's product manager Sammit Adhya.
This button is presented next to the "Accept all" option
and is designed to be equally weighted visually.
This design choice is not negligible,
as the companies are required to eliminate any variable
that could make one option more salient than the other.

Both Google Search and YouTube now show the button to users in France
while signed out or in Incognito Mode.
According to Adhya,
this option will be available soon
to users across the rest of the European Economic Area,
as well as those in the U.K. and Switzerland.
Of course,
users in France that are signed in can adjust their preferences
from their Google account's [data and privacy](https://myaccount.google.com/data-and-privacy)
options.

<div class="imgblock">

![New cookie banner on YouTube](https://res.cloudinary.com/fluid-attacks/image/upload/v1651084752/blog/google-cookie-banner-unlawful/cookie-figure-1.webp)

</div>

## noyb to end the "cookie banner terror"

The use of unlawful cookie banners has,
of course,
got the attention of the European Center for Digital Rights,
known shortly as noyb
(the meaning of this acronym is none of your business).
In a [news article](https://noyb.eu/en/noyb-aims-end-cookie-banner-terror-and-issues-more-500-gdpr-complaints)
they posted almost one year ago,
they explained
they developed a software
that detects banners
that make it more difficult to reject
than to accept cookies
and generates GDPR complaints.

Back then,
noyb said they had sent complaint drafts to 560 websites from 33 countries.
These drafts were more of a warning,
giving companies one month to change their banner
and software settings.
What's more,
they sent violators a guide showing every step to make the changes.
But if the companies failed to comply,
noyb officially notified the relevant authority.

noyb [announced](https://noyb.eu/en/more-cookie-banners-go-second-wave-complaints-underway)
this year in March
that they launched a second round,
filing 270 draft complaints
and extending the response deadline to two months.
They also informed
that 42% of all violations found last year were remedied within the deadline.
But 82% of all companies failed to fully comply with the demand
and were reported to the data protection authorities.
Although most of the latter confirmed the receipt of complaints,
what is next appears to be a lengthy process.
Still,
after Google's case,
companies may feel encouraged to follow suit.

## Just promote people's informed choice

Up until this point,
we talked about cookies like they are an unwanted thing.
Still,
websites normally tell you that they use cookies
"to provide you with a better user experience."
We are not about to discuss whether this is always the case.
You probably know
that necessary cookies include those that detect errors,
store your consent state
or help the website know that you are not a bot.
Other kinds track your surfing behavior,
some of their purposes being user profiling
and selling for further advertising.
What's key here is that you know what you are agreeing to
and know that you can complain when that's not made clear.

Finally,
if you are in charge of engineering how cookies work
on your company's website
or deciding on the content of the banner,
make sure that you comply with standards
such as the [GDPR](https://docs.fluidattacks.com/criteria/compliance/gdpr)
and the [ePrivacy directive](https://docs.fluidattacks.com/criteria/compliance/eprivacy),
especially if you have users in Europe.
