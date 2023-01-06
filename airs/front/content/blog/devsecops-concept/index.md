---
slug: devsecops-concept/
title: What Is DevSecOps?
date: 2020-05-14
modified: 2022-06-13
subtitle: Best practices and a description of the basics
category: philosophy
tags: cybersecurity, devsecops, software, training, company
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330852/blog/devsecops-concept/cover_c4reuk.webp
alt: Photo by Sebastian Pena Lambarri on Unsplash
description: Learn about what DevSecOps is, its importance, how it differs from DevOps, and its advantages on IT security for continuous delivery, testing and deployment.
keywords: Devsecops Meaning, Devops Vs Devsecops, Shift Left Security, Devsecops Best Practices, Devsecops Automation, Security Testing, Software Development Lifecycle, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/YV593oyMKmo
---

Broadly speaking,
DevSecOps is a methodology
that incorporates security into the development (Dev)
and operations (Ops) processes.
In simple terms,
it means that the security of technology is assessed during its development,
but also that security is everybody's business.

You have probably noticed
that seemingly everyone is jumping on the [DevSecOps](../../solutions/devsecops/)
bandwagon.
Just in 2021,
about 36% of respondents
in GitLab's worldwide
[DevSecOps survey study](https://learn.gitlab.com/c/2021-devsecops-report?x=u5RjB_)
said their teams develop software using DevOps or DevSecOps.
And you'd probably very much like to know
just what the meaning of DevSecOps is.
In this blog post,
we will give you all the basics about this methodology.
After reading it,
be sure to check out the others in our [DevSecOps blog series](/../tags/devsecops/).

## DevOps vs DevSecOps

DevSecOps [has been called](https://www.infoq.com/articles/evolve-devops-devsecops/)
"the natural extension of DevOps."
So,
we need to explain
what is the difference between DevOps and DevSecOps.

### DevOps

Perhaps as famous a concept as DevSecOps,
[DevOps](../devops-concept/) is defined as a development methodology
that aims to bridge the gap between development and operations.
It accomplishes this
by stressing communication between developers and operators
and shared responsibility in quality assurance.

What's considered a main feature of DevOps is velocity.
Indeed,
here's where two processes shine,
for they are hardly absent when talking about DevOps.
One is continuous integration (CI).
This refers to the process of developers
integrating the code they work on into a shared repository
several times during the day,
every day.
Along with CI is continuous delivery (CD),
which means moving software to the production environment,
providing swift response to modifications and constant feedback.
Here's a positive outcome:
In GitLab's aforementioned
[2021 survey](https://learn.gitlab.com/c/2021-devsecops-report?x=u5RjB_),
almost 60% of developers said
they released code twice as fast thanks to DevOps.

### DevSecOps

Great as DevOps may sound,
there's no point in releasing fast
if the product is riddled with bugs.
Teams attempt to prevent this
by [implementing DevSecOps](../how-to-implement-devsecops),
meaning they adopt a culture
in which everyone is responsible for security
and every developer assesses their own code
with security testing automated tools
or manual techniques.
They do this during the entire development lifecycle (SDLC).
That's right: from its beginning to its end.

## DevSecOps meaning

We published [a post about DevOps](../devops-concept/) a while ago.
At the end of it,
we asked about the inclusion of security
in this methodology of continuous integration and deployment.
Consequently,
we referred to the emergence of the [**DevSecOps**](../../solutions/devsecops/)
concept.
If we search on the Internet for a short definition, we find what is
said in [Gartner's
glossary](https://www.gartner.com/en/information-technology/glossary/devsecops):

<div class="imgblock">

![DevSecOps Gartner definition](https://res.cloudinary.com/fluid-attacks/image/upload/v1627064266/blog/devsecops-concept/dev_pgtgub.webp)

</div>

Ok, that information might be enough. See you in the next post\!

<div class="imgblock">

![What is DevSecOps](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330850/blog/devsecops-concept/ah_jnw9fa.webp)

<div class="title">

Image taken from [i.imgur.com](https://i.imgur.com/YezxAlA.png).

</div>

</div>

I was just kidding\! Let's talk about it.

So,
what does DevSecOps stand for?
As we said in the DevOps post,
the element **Sec**,
referring to security,
is added to **DevOps**.
But to be clear,
we don't just add it anywhere,
we add it in the middle: **DevSecOps**.
Security is then expected to play a significant role
alongside the development (**Dev**) and operations (**Ops**) processes.
DevSecOps is an evolution of DevOps
where security is understood and implemented.
But why the inclusion of security in this methodology?
Why is DevSecOps important?

## Why do we need DevSecOps?

Security in software engineering is still ignored by many.
Others still see it as an obstacle
that slows down the production process.
But many others have come to see security as a *necessity*
in an ample shared virtual space,
where the intentions of a lot turn out not to be the best.
The most attentive to this issue
have been those wishing to maintain the prestige of their companies,
which may be handling personal data of huge amounts of users.

We must be aware
that user data and app functionality can be put at risk
by the presence of vulnerabilities.
So,
to avoid weaknesses
and subsequent attacks on products,
security measures must be implemented from the early stages in the SDLC.
It's true
that security tests usually have been carried out
*just before* the deployment of applications to the production environment.
But for many,
this testing approach has been a burden.
What about those within the DevOps culture
who are continually creating features on their applications?
Are they investing time and effort
in finding and detecting gaps in their code *just before* each deployment?

If they are already within the DevSecOps approach,
the answer is *no*.
When we say implementation in the early stages,
as shown in the figure below,
the security element has to cover the cycle from its beginning to its end.

<div class="imgblock">

![Security in DevSecOps](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330850/blog/devsecops-concept/devsecops_vkkb14.webp)

<div class="title">

DevSecOps covers development and operations.
Figure taken from [images.idgesg.net](https://images.idgesg.net/images/article/2018/01/devsecops-gartner-image-100745815-orig.jpg).

</div>

</div>

## How does DevSecOps work?

In this approach,
companies have to establish security requirements
that they must meet during the SDLC.
These requirements can be based on system infrastructure assessments.
Such evaluations carried out manually
and from the attacker's point of view
detect potential security issues.
In other words,
these assessments are intended to answer questions such as:
Where can hackers attack us?
What are the areas and information
that we must protect the most?
What are the gaps
that we must not allow in our applications?
What will be the countermeasures
and solutions
we have to establish?

Following those security requirements,
security checks for finding vulnerabilities are performed continuously.
These checks are carried out through automatic tools
combined with [teams of security experts](../../solutions/ethical-hacking/)
that use their knowledge to detect gaps,
keeping pace with DevOps.
The use of these tools and human capabilities integrated into the pipelines,
employing [static application security testing](../../categories/sast/)
and [dynamic application security testing](../../categories/dast/) techniques,
makes it possible to minimize the
number of vulnerabilities.
These weaknesses can be found early,
while the code is under construction,
and their remediation can also be done promptly.
The timely activity of experts and DevSecOps tools,
which should generate continuous information logging
and quick feedback,
allows companies to stay one step ahead of attackers
and maintain security controls.
That is why DevSecOps practices are important.

**Caution:**
(a) **Relying heavily on tools and their automatic work
can lead to high rates of false positives and negatives**.
For that reason,
the role of human experts is fundamental to achieve precision
and avoid that developers waste time confirming if vulnerabilities are real.
The main risk is the existence of false negatives or escapes.
Organizations may not be aware of certain security vulnerabilities
that current technology is unable to identify.
(b) **Perform the security checks gradually**,
starting [with high-priority areas](https://medium.com/hackernoon/the-future-of-security-is-devsecops-9166db1d8a03),
trying not to overload the developers with work
as they are usually responsible for closing the gaps.

## Benefits of DevSecOps

Forrester's 2021 report
on the state of application security
[showed](https://securityboulevard.com/2021/04/forresters-state-of-application-security-report-2021-key-takeaways/)
that 30% of security decision-makers surveyed in 2020
whose companies were breached
said the attack was possible because of software vulnerabilities.
DevSecOps aims to avoid this.
As changes to code are tested for vulnerabilities,
it's possible to get ahold of them
before the end-user gets a buggy software handed to them.

Yet another [worrying trend](../cybersecurity-trends-2021/)
is supply chain attacks.
Teams use third-party components
more often than not
to develop their software.
Also,
if they built the components themselves,
other teams will probably use them.
If attackers find a vulnerability
that allows them to mess with code,
components,
cloud services,
etc.,
common to various software projects,
they end up compromising the whole supply chain.
DevSecOps practices aim to secure software from upstream risk
and prevent teams from generating downstream risk.

And as we mention further below,
DevSecOps may also enable your team to save on remediation costs.

## How to evolve DevOps to DevSecOps

"Well, sign me up! How can I start?"
It's good that you ask!
Fortunately,
we offer a complete guide on [how to implement DevSecOps](../how-to-implement-devsecops)
in a dedicated post.
Here,
we'll give you a simple advice on
how to evolve DevOps to DevSecOps.

You may start
by deciding to **expand shared responsibility and ownership**
of the software
to encompass its security also.
For the most part,
this is achieved by creating the possibility of collaboration
between the development,
operations and security teams.
What we're aiming for here
is for people to adopt a DevSecOps culture and mindset.

You may also move on
to **specify the security checks**
in need of implementation into your DevOps processes.
Ideally,
most of them should be automated.
However,
an effort needs to be made to train developers on secure coding,
reviewing code for vulnerabilities as soon as a change is done.
Moreover,
it doesn't matter if they are not developers,
engineers or whatever;
every one of the employees must be aware
of any newly established security requirements
and know how to implement them in their daily work.

In this process,
some DevSecOps roles and responsibilities should emerge.
There is a person whose job is to define actions,
lead the security checks
(e.g., conducting risk assessments and threat modeling)
and monitor practices in the DevSecOps process.
We're talking about the DevSecOps engineer.
We've dedicated a blog post about this role
that even mentions how to become a DevSecOps engineer.
Be sure to [check it out](../what-does-a-devsecops-engineer-do/).

<cta-banner
  buttontxt="Read more"
  link="/solutions/devsecops/"
  title="Get started with Fluid Attacks' DevSecOps solution right now"
/>

## DevSecOps best practices

It's vital to show a commitment to security
and enhance DevSecOps capabilities.
We have identified a set of best practices,
which we talk about more extensively
in a [dedicated blog post](../devsecops-best-practices).
Here,
we make a brief summary:

- **Collaboration:**
  Encouraging prompt communication
  and making it possible for the entire project team
  to find out where the vulnerabilities are in the code,
  who introduced them,
  what's been done about them
  and their remediation status.

- **Cybersecurity awareness:**
  Regularly informing employees about company-wide security policies
  (vital for maintaining cybersecurity awareness);
  educating them to incorporate security practices
  (e.g., testing and code review)
  into their daily work;
  and holding them accountable
  "for assessing and maintaining the security of their work."

- **Velocity:**
  Launching small code changes quickly and securely.

- **Shift-left testing:**
  Having security scans built into the developers' workflow
  at the early stages of development
  to search for known vulnerabilities in the code they've just written;
  this way they can fix them
  before the security team reviews the scan results.

- **Automation in combination with manual pentesting:**
  Successfully integrating security into the CI/CD pipelines,
  so that every change in the code is automatically scanned,
  inventoring code dependencies continuously
  and keeping them up to date,
  and automatically creating issues/tickets
  or breaking the build
  (whichever is the organization policy)
  in case a vulnerability is found.
  And doing this continually
  along with manual security testing.

- **Security standards:**
  Automating the use of security standards,
  evaluated and set by the security team,
  and continuously evaluating compliance
  and the integrity of the systems' physical components,
  network security
  and employee behavior.

- ***Continuous* instead of *regular* security audits:**
  Identifying the entire attack surface,
  and possible attack vectors for information systems,
  which is commonly a part of risk assessments
  and threat modeling.

- **Continuous penetration tests:**
  Having ethical hackers assess the security of your systems
  throughout the entire SDLC,
  as opposed to conducting *just regular* penetration tests
  that could allow a time window
  during which threat actors can get a way in.

- **Break the build:**
  Preventing vulnerable code from reaching production
  and fixing it promptly,
  thus cutting remediation time by [up to about 30%](https://try.fluidattacks.tech/state-of-attacks-2022/).

And what are the phases of DevSecOps adoption?
It's ideal
that you start the above practices
gradually.
Some, like automation,
may become more sophisticated
as you become more mature
in DevSecOps.
For a detailed DevSecOps roadmap,
go to [our dedicated blog post](../how-to-implement-devsecops).

## Shift-left security

We can't stress enough
the importance of starting security testing from the very beginning.
Visualize the SDLC across a straight horizontal line,
project planning on the leftmost point
and production deployment on the rightmost point:
We're asking you to move security testing ever to the left.

The whole idea concerning shift-left testing is to identify
and address security issues in software
from the early stages of development.
That is,
not well into the traditional testing stage of the SDLC
but much earlier,
even when defining its requirements
(e.g., what it should do and the resources needed).

Shifting testing to the left may help you
produce more secure software and save money.
It has been argued
that remediation at the early stages of development
[is less costly](https://landing.fluidattacks.com/us/ebook/)
than at the production deployment stage.

## DevSecOps automation along with manual techniques

As we mentioned earlier,
it's ideal to have automated security checks.
This includes essential things
like having automated security testing tools
(e.g., [SAST](../../categories/sast/),
[DAST](../../categories/dast/))
running in your CI pipelines.
However,
these tools may generate false positives
and false negatives,
so an even better strategy is to have actual people use manual techniques
(e.g., manual SAST, DAST
and [SCA](../../categories/sca/))
to find vulnerabilities in your software.
In fact,
our ethical hackers [found about 81%](https://try.fluidattacks.tech/report/state-of-attacks-2021/)
of the high and critical severity vulnerabilities reported
in systems over an analysis period in 2020.
In short,
process automation does save you time
but a manual intervention is needed to achieve accuracy.

## DevSecOps as a service

Some organizations may find it necessary
to outsource DevSecOps services.
When they do this,
they expect to be provided a solution
that leverages the knowledge and practical experience
of certified DevSecOps professionals.
The provider of DevSecOps as a service is responsible
for embedding security methodologies and toolkits
(such as tools to run security checks in CI/CD pipelines)
across the entire SDLC.
Moreover,
they should assess current
and potential vulnerabilities in the system
and help enforce cybersecurity best practices beyond secure coding.

We at `Fluid Attacks` offer [DevSecOps](../../solutions/devsecops/)
implementation
as part of our [Continuous Hacking](../../services/continuous-hacking/)
solution.
As mentioned above,
we understand
that using manual techniques for security testing
has evident benefits over automated security testing tools.
So,
we help organizations implement DevSecOps
by offering our ethical hackers' skills (in addition to automated tools)
to find vulnerabilities across the SDLC.
By performing continuous [penetration tests](../../solutions/penetration-testing/),
organizations can validate the security of their technology
and test it against new techniques used by threat actors
and therefore out of the scope of automated tools.

## How does DevSecOps relate to red teams?

You may then want your system to be tested for vulnerabilities
in the most realistic way.
That is,
to have ethical hackers perform actual attacks.
[Red teaming](../../solutions/red-teaming/) can do this for you.
Its relation with DevSecOps is
that you can gain a better understanding of your system's security
if ethical hackers continually test the system versions
just like malicious attackers would.
This implies
that [only some people](../tiber-eu-framework/)
in your organization
should be aware of the contractual agreement with the red team;
the rest will have to respond to the attacks,
which will be carried out [without any previous announcement](../attacking-without-announcing/).
Security should be all about being prepared for actual attacks anytime,
and this is how DevSecOps relates to red teams.

A resulting way in which red teaming [may enhance](https://www.devsecops.org/blog/tag/Red+Team)
your DevSecOps adoption
is by challenging a pernicious mindset:
That vulnerabilities can be accepted,
since there's little chance they will be exploited.
So,
when you have actual evidence
that hackers exploited it,
you have no option but to prioritize its remediation
instead of focusing on deploying new features.

## DevSecOps with Fluid Attacks

Now,
to have a clearer idea of the role of security within DevOps,
let's briefly outline what Oscar Prado,
Cybersecurity Analyst,
shared with us about what `Fluid Attacks` does for its clients.
Our company offers continuous hacking services,
a constant search for vulnerabilities in IT systems.
But although some tools are used in this process,
at `Fluid Attacks`,
we rely on tools only as a support for our hackers' activities,
contrary to what other companies do.
Here we place more value on the knowledge
and skills of ethical hackers
to ensure greater accuracy in testing.
Their work can begin
"from the moment the first commit is uploaded by developers,"
with every new change being reviewed.
That work can continue
after the application has been deployed to production.

When a vulnerability is detected in the client's code,
a member of our team can develop a personalized script called exploit,
associated with the finding.
That exploit "automatically checks if the analyst's finding persists."
Therefore,
"if the customer wants to make new changes to her product,
she must fix the finding first,"
because if she doesn't,
the exploit will continue reporting the presence of the vulnerability.
Then,
according to a configuration by her team,
it will break the build,
and the deployment process will be automatically stopped.
"This way,
security is prioritized,
and our security testing is integrated into the client's SDLC,"
concludes Oscar.

<div class="imgblock">

![Break the build](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330851/blog/devsecops-concept/build_wmkfpb.webp)

<div class="title">

To 'break the build' means to stop the software deployment process.
Image taken from [citymetric.com](https://www.citymetric.com/sites/default/files/article_2015/01/149818154.jpg).

</div>

</div>

**Bonus:** `Fluid Attacks` is convinced
that speed without precision is useless.
Therefore,
we have combined the best of each end:
Technology and knowledge produce a good balance.
Many cybersecurity companies offer fast,
automated tools that are highly prone to false positives
and false negatives
when searching for vulnerabilities.
`Fluid Attacks` has recognized
that there must be human work involved in these processes
to ensure accuracy and efficiency.
`Fluid Attacks` has not forgotten the value of speed
but has always kept it in parallel with high-quality testing
and excellent results.
So,
we invite organizations to automate tools and processes
where it is possible
and rely on ethical hackers to perform sophisticated security testing.
This way they can achieve their DevSecOps goals.

## SecDevOps?

It's curious
that when we spoke with Oscar,
he didn't use the name DevSecOps,
but **SecDevOps**.
He moved security to the left
With SecDevOps,
perhaps more emphasis is placed
on initially establishing security requirements to be followed
through testing processes carried out continuously in the SDLC.

Regardless of the name we give
to the inclusion of security into the DevOps methodology,
within this new business culture,
security is expected to play an essential role in software production
and maintenance
from the beginning
It's intended
that all those involved in the projects know and apply security;
that's why they need training.
Bear in mind that just as in DevOps,
there shouldn't be separate teams by function but by product.
In the end,
everyone must be responsible for security.

Companies that decide to implement the [DevSecOps](../../solutions/devsecops/)
approach
(or, perhaps better said, SecDevOps)
will achieve significant benefits,
especially in the quality and security of their processes and products.
Would you like some advice on how to do it?

We at `Fluid Attacks` help you enact your DevSecOps practices:
You can integrate our [DevSecOps agent](https://docs.fluidattacks.com/machine/agent)
into your pipelines
and configure it to [break the build](../../solutions/devsecops/)
if our SAST or DAST tools find a vulnerability in your code.
Moreover,
you can ask us about our [Squad Plan](../../plans/),
which involves [ethical hackers](../../solutions/ethical-hacking/)
assessing the security of your technology.
To learn more
and get all your DevSecOps questions answered,
[contact us](../../contact-us/)\!
