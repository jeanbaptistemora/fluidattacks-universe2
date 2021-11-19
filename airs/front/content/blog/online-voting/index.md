---
slug: online-voting/
title: Online Voting for a New President?
date: 2020-06-24
subtitle: The trouble with OmniBallot and other voting platforms
category: politics
tags: security, cybersecurity, software, web, vulnerability, risk
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330960/blog/online-voting/cover_hrlrgj.webp
alt: Photo by visuals on Unsplash
description: In this post, we show you the exposed vulnerabilities of one of
  the many online voting options likely to be used
  in the upcoming presidential election.
keywords: Security, Cybersecurity, Software, Web, Vulnerability, Risk
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/TJ6BM5VGdgI
---

Near the end of this year, there will be a new presidential election in
the `US`. From the Democratic side, Biden seems to be leading [according
to some early
ratings](https://www.npr.org/2020/06/17/877951588/2020-electoral-map-ratings-biden-has-an-edge-over-trump-with-5-months-to-go),
competing with Trump on the Republican side seeking reelection. This
election process may occur amid the
[COVID-19](https://www.nature.com/articles/s41591-020-0820-9) pandemic
that is currently affecting us. Thus, considering that we aim to
maintain safe distances to prevent contagion, questions arise on how to
carry out the voting processes. Could it be somewhat more convenient and
more secure to perform such processes over the Internet?

A few days ago, the researchers Michael A. Specter, of MIT, and Alex
Halderman, of the University of Michigan, [published an
article](https://internetpolicy.mit.edu/wp-content/uploads/2020/06/OmniBallot.pdf)
that reports how an online election could be affected by undetected
attackers. These authors made the first review explicitly focused on
[Democracy Live’s
`OmniBallot`](https://democracylive.com/omniballot-online/) platform
used in different states on certain voting activities. Using [reverse
engineering](../reverse-engineering/) to analyze platform security,
Specter and Halderman found that `OmniBallot` is vulnerable to specific
attacks that can mean alteration of votes or theft of personal data.
They also gave some recommendations to take into account for the next
elections.

### OmniBallot

Current health risks have led some states to consider the Internet as a
means of running the coming elections. Generally, the Internet has been
used to allow specific vulnerable populations or those not present in
the country to participate in elections. Tools such as `OmniBallot` have
been used for these purposes. `OmniBallot` is a web-based platform that
can serve for three modes of operations: blank ballot delivery, ballot
marking, and *online voting*. Now, reportedly, it is going to be used
for *online voting* for the first time in Delaware, West Virginia, and
New Jersey with larger groups of voters. This is the riskiest mode in
relation to cyberattacks.

Let’s clarify each `OmniBallot’s` mode of operation:

1. *Online blank ballot delivery:* The voter downloads her
    corresponding blank ballot, and it is printed, manually marked, and
    physically returned to the election authorities.

2. *Online ballot marking:* The voter marks her ballot on the website
    and then downloads it to print it and return it physically. Some
    jurisdictions give the option to return it via fax or email.

3. *Online ballot return (online voting):* The voter marks her ballot
    and transmits it to the authorities over the Internet through a
    service of Democracy Live. Among the `OmniBallot` customers and in
    comparison with the two previous modes, this is the least used.

Following ethical and legal principles, Specter and Halderman limited
their analysis to the publicly available parts of `OmniBallot`,
specifically the Delaware version. Therefore, as a general description
of the `OmniBallot` architecture, they proposed the following:

<div class="blog-questions">

1. The web app runs in the browser and uses HTTPS to load files and
    call REST-like APIs from several domains. When voting online or
    marking a ballot, the app sends the voter’s identity and ballot
    selections to Democracy Live services running in Amazon’s cloud. The
    app runs JavaScript loaded from Amazon, Google, and Cloudflare,
    making all three companies (as well as Democracy Live itself)
    potential points of compromise for the election.

</div>

After having a clear understanding of the platform’s architecture and
client-server interactions, the authors analyzed the risks created when
`OmniBallot` is used in each of the three modes mentioned above. Before
we talk about that, let’s state the possible attackers or adversaries:

First, adversaries may have access to the voter’s device. These
attackers could be system administrators, abusive partners, or remote
attackers that control certain malware, and could modify `HTTP` or
inject JavaScript to alter the behavior of the web browser. In second
place are the attackers with access to the server infrastructure of
`OmniBallot`. These adversaries could be, for example, internal staff
from Democracy Live or Amazon, and external attackers ready to access
and affect the systems involved. In third place are the adversaries with
control of third-party code. This involves attackers who may have access
to third-party software and services which `OmniBallot` integrates, such
as Google Analytics, AngularJS, reCAPTCHA, and Fingerprint JS. Also,
customers load some libraries from Amazon, Cloudflare, and Google, where
there could also be malicious subjects willing to modify the
`OmniBallot` platform.

So, what could these attackers end up doing in the different ways
`OmniBallot` works?

### OmniBallot risks

1. *Online blank ballot delivery:* We can start with the fact that the
    attacker could manipulate the ballot design, for example, swapping
    or removing candidates. In a more difficult to detect manipulation,
    for instance, an attacker could even change bar codes to alter the
    records when tabulated by a scanner. On the other hand, there may be
    attacks not directed at the ballot itself but at the ballot return
    instructions. The attacker could make the ballot be sent to an
    inappropriate place, after knowing the voter’s site that is among
    the data verified by OmniBallot at the start. Additionally, the
    attacker could mail a different ballot (following their preferences)
    to the appropriate place employing the voter’s data.

2. *Online ballot marking:* Here, the attacker could know the voter’s
    selection before the ballot’s generation, and from this, modify that
    particular ballot to suppress the vote for a specific candidate.
    Attacks may also involve reordering the candidates and swapping the
    barcodes linked to each of them. In these online marking cases, the
    attacker could also simply alter the voter’s marking and select a
    different candidate. And while some might notice the change, many
    others would not detect the errors on their ballots and return them
    as they are.

3. *Online ballot return:* `OmniBallot` does not use the "end-to-end
    verifiability ([E2E-V](https://arxiv.org/abs/1504.03778))" approach
    for a secure remote voting protocol. Computer scientists have been
    working on it for several decades, and to some extent, it is the
    most recommended approach. It "allows each voter to independently
    check that their vote is correctly recorded and included in the
    election result." `OmniBallot` uses a protocol in which no one can
    verify that what the voters gave as a selection is the same as what
    the officials received. Hence the possibility of the attacker
    changing the votes without being noticed.

Finally, a risk associated with all modes of operation is the collection
and storage of privacy-sensitive data, including names, addresses, and
dates.

### Recommendations and conclusion

Apparently, Democracy Live’s security controls are limited. Following
the authors' recommendations, `OmniBallot’s` online ballot return should
be eliminated, and the physical ballot return should be improved on
accessibility and efficiency. Also, online marking should be offered
only to voters who have this mode as necessary to join the elections.
Moreover, officials should carry out risk-limiting audits
([RLAs](https://en.wikipedia.org/wiki/Risk-limiting_audit)) to test at
least in part the accuracy of the computers' work. Additionally,
Democracy Live could reduce risks eliminating *unnecessary* reliance on
third parties that may constitute multiple routes of attack. And as a
final tip related to some legal protections, `OmniBallot` should have a
posted privacy policy informing voters of the limitations on the use of
their data by Democracy Live and third parties. The fact is that such
data should only be used for the election process.

The public security review of `OmniBallot` by security experts is
something of high value when its use —due to a positive record in much
smaller procedures— is under consideration for the next presidential
election. In the end, they warn us that with such high risks of election
outcomes being altered without detection, and without sufficient tools
to mitigate those risks, it is best that `OmniBallot’s` (or any similar
voting platform’s) online ballot return doesn’t become the default
voting process.
