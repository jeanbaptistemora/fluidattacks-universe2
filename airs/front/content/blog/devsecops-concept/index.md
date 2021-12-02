---
slug: devsecops-concept/
title: Everyone Is Responsible for SEC
date: 2020-05-14
subtitle: An overview of DevSecOps, better SecDevOps
category: philosophy
tags: security, devops, software, information, web, cloud
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330852/blog/devsecops-concept/cover_c4reuk.webp
alt: Photo by Sebastian Pena Lambarri on Unsplash
description: Through this blog post, you will know what DevSecOps is,
  how it applies, and why it is recommended for IT companies.
keywords: Security, Devops, Devsecops, Secdevops, Information, Web,
  Cloud, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/YV593oyMKmo
---

We recently published [a post about DevOps](../devops-concept/). At the
end of it, we asked about the inclusion of security in this methodology
of continuous integration and deployment. Consequently, we referred to
the emergence of the **DevSecOps** concept. But what does this term
mean?

### Definition of DevSecOps

If we search on the Internet for a short definition, we find what is
said in [Gartner’s
glossary](https://www.gartner.com/en/information-technology/glossary/devsecops):

<div class="imgblock">

![DevSecOps
Gartner](https://res.cloudinary.com/fluid-attacks/image/upload/v1627064266/blog/devsecops-concept/dev_pgtgub.webp)

</div>

Ok, that information might be enough. See you in the next post\!

<div class="imgblock">

![Huh?](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330850/blog/devsecops-concept/ah_jnw9fa.webp)

<div class="title">

Figure 1. Huh? (Taken from [imgur.com](https://i.imgur.com/YezxAlA.png).)

</div>

</div>

I was just kidding\! Let’s talk about it.

As we said, the element **Sec**, referring to security, is added to
**DevOps**. But to be clear, we don’t just add it anywhere, we add it in
the middle: **DevSecOps**. Security is then expected to play a
significant role alongside the development (**Dev**) and operations
(**Ops**) processes. DevSecOps is an evolution of DevOps where security
is understood and implemented. But why the inclusion of security in this
methodology?

Well, security in software engineering is still ignored by many. Others
still see it as an obstacle that slows down the production process. But
many others have come to see security as a *necessity* in an ample
shared virtual space, where the intentions of a lot turn out not to be
the best. The most attentive to this issue have been those wishing to
maintain the prestige of their companies, which may be handling personal
data of huge amounts of users.

We must be aware that user data and app functionality can be put at risk
by the presence of vulnerabilities. So, to avoid weaknesses and
subsequent attacks on products, security measures must be implemented
from the early stages in the software development lifecycles (SDLC).
It’s true that security tests usually have been carried out *just
before* the deployment of applications to the production environment.
But for many, this testing approach has been a burden. What about those
within the DevOps culture who are continually creating features on their
applications? Are they investing time and effort in finding and
detecting gaps in their code *just before* each deployment?

If they are already within the DevSecOps approach, the answer is *no*.
When we say implementation in the early stages, as shown in Figure 2,
the security element has to cover the cycle from its beginning to its
end.

<div class="imgblock">

![DevSecOps](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330850/blog/devsecops-concept/devsecops_vkkb14.webp)

<div class="title">

Figure 2. DevSecOps (taken from [images.idgesg.net](https://images.idgesg.net/images/article/2018/01/devsecops-gartner-image-100745815-orig.jpg)).

</div>

</div>

In this approach, companies have to establish security requirements that
they must meet during the SDLC. These requirements can be based on
system infrastructure assessments. Such evaluations carried out manually
and from the attacker’s point of view detect potential security issues.
In other words, these assessments are intended to answer questions such
as: Where can hackers attack us? What are the areas and information that
we must protect the most? What are the gaps that we must not allow in
our applications? What will be the countermeasures and solutions to
establish?

Following those security requirements, security checks for finding
vulnerabilities are performed continuously. These checks are carried out
through automatic tools combined with teams of security experts that use
their knowledge to detect gaps, keeping pace with DevOps. The use of
these tools and human capabilities integrated into the pipelines,
employing SAST and DAST techniques, makes it possible to minimize the
number of vulnerabilities. These weaknesses can be found early, while
the code is under construction, and their remediation can also be done
promptly. The timely activity of experts and tools, which should
generate continuous information logging and quick feedback, allows
companies to stay one step ahead of attackers and maintain security
control.

**Caution:** (a) **Relying heavily on tools and their automatic work can
lead to high rates of false positives and negatives**. For that reason,
human experts' role is fundamental to achieve precision and avoid
developers wasting time confirming if vulnerabilities are real. The main
risk is the existence of false negatives or escapes. Organizations may
not be aware of certain security vulnerabilities that current technology
is unable to identify. (b) **Perform the security checks gradually**,
starting [with high-priority
areas](https://medium.com/hackernoon/the-future-of-security-is-devsecops-9166db1d8a03),
trying not to overload the developers with work as they are usually
responsible for closing the gaps.

### DevSecOps with Fluid Attacks

Now, to have a clearer idea of the role of security within DevOps, let’s
briefly outline what Oscar Prado, Cybersecurity Analyst, shared with us
about what `Fluid Attacks` does for its clients. Our company offers
continuous hacking services, a constant search for vulnerabilities in IT
systems. But although some tools are used in this process, at `Fluid
Attacks`, our reliance on tools is for specific cases that support our
hackers' activities, contrary to what other companies do. Here we place
more value on the knowledge and skills of ethical hackers to ensure
greater accuracy in testing. Their work can begin "from the moment the
first commit is uploaded by developers," with every new change being
reviewed. That work can continue after the application has been deployed
to production.

When a vulnerability is detected in the client’s code, a member of our
team can develop a personalized script called Exploit, associated with
the finding. That Exploit "automatically checks if the analyst’s finding
persists." Therefore, "if the customer wants to make new changes to her
product, she must fix the finding first," because if she doesn’t, the
Exploit will continue reporting the presence of the vulnerability. Then,
according to a configuration by our team, it will break the build, and
the deployment process will be automatically stopped. "This way,
security is prioritized, and our security testing is integrated into the
client’s SDLC," Oscar concludes.

<div class="imgblock">

!['Break the build' means to stop the software deployment process
([photo-link](https://www.citymetric.com/sites/default/files/article_2015/01/149818154.jpg)).](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330851/blog/devsecops-concept/build_wmkfpb.webp)

<div class="title">

Figure 3. 'Break the build' means to stop the software deployment process
([photo-link](https://www.citymetric.com/sites/default/files/article_2015/01/149818154.jpg)).

</div>

</div>

**Bonus:** `Fluid Attacks` is convinced that speed without precision is
useless. Therefore, we have combined the best of each end: technology
and knowledge produce a good balance. Many cybersecurity companies offer
fast, automatic tools that are highly prone to false positives and
negatives when searching for vulnerabilities. `Fluid Attacks` has
recognized that there must be human work involved in these processes to
ensure accuracy and efficiency. `Fluid Attacks` has not forgotten the
value of speed but has always kept it in parallel with high-quality
testing and excellent results.

### SecDevOps?

It’s curious that when we spoke with Oscar, he didn’t use the name
DevSecOps, but **SecDevOps**. He moved security to the left. With
SecDevOps, perhaps more emphasis is placed on initially establishing
security requirements to be followed through testing processes carried
out continuously in the SDLC.

Regardless of the name we give to the inclusion of security into the
DevOps methodology, within this new business culture, security is
expected to play an essential role in software production and
maintenance from the beginning. It’s intended that all those involved in
the projects know and apply security; that’s why they need training.
Bear in mind that just as in DevOps, there shouldn’t be separate teams
by function but by product. In the end, everyone must be responsible for
security.

Companies that decide to implement the DevSecOps approach (or, perhaps
better said, SecDevOps) will achieve significant benefits, especially in
the quality and security of their processes and products. Would you like
some advice on how to do it? [Get in touch with our
team\!](../../contact-us/)
