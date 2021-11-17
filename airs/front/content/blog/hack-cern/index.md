---
slug: hack-cern/
title: Preventing Hacks at CERN
date: 2019-05-13
subtitle: A chat with Andrés Gómez
category: interview
tags: security, machine-learning, testing
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330889/blog/hack-cern/cover_fqngm1.webp
alt: Photo by Aurélien Clément Ducret on Unsplash
description: For this post, we spoke with Andrés Gómez, a former Fluid Attacks'
  member, who is researching to protect a computer grid supporting experiments
  at the LHC.
keywords: CERN, Hacking, Security, Interview, LHC, Machine Learning,
  Pentesting, Ethical Hacking
author: Julian Arango
writer: jarango
name: Julian Arango
about1: Behavioral strategist
about2: Data scientist in training.
source: https://unsplash.com/photos/Cm8n6CIMZnY
---

Have you heard about God’s particle? In 2012, the Large Hadron Collider
(`LHC`) found the Higgs Boson; a particle predicted to exist in the
1960s thanks to the work of Peter Higgs and other physicists. The `LHC`
consists of a 27-kilometer ring of superconducting magnets with several
accelerating structures to boost the energy of particles along the way.
According to
[Forbes](https://www.forbes.com/sites/alexknapp/2012/07/05/how-much-does-it-cost-to-find-a-higgs-boson/#695f65e63948),
finding the Higgs Boson had cost around `USD` `13.25` billion. Now you
have a sense of what we will discussing in this post.

<div class="imgblock">

![Large Hadron Collider. Source: https://commons.wikimedia.org/wiki/File:Large_Hadron_Collider.JPG](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330887/blog/hack-cern/lhc_ybns7h.webp)

<div class="title">

Figure 1. Large Hadron Collider.

</div>

</div>

A good friend of ours and former `Fluid Attacks` security engineer, has
been working in that huge scientific project. Andrés is a final `Ph.D.`
student in Computer Science at the Goethe University in Germany. His
work has focused on securing the computer grid that allows many
physicists around the world to analyze data on subatomic particle
collisions at the `LHC`. He has a fantastic record in cybersecurity.
Before starting his doctoral studies, he found several serious
weaknesses in commercial software. One of his most striking findings was
the [CVE-2013 3174
(MS13-56)](http://kuronosec.blogspot.com/2013/07/directshow-arbitrary-memory-overwrite.html),
which refers to a Remote Execution Vulnerability affecting Microsoft
Windows Systems. You can read more about Andrés in his [academic
profile](https://iri-wiki.uni-frankfurt.de/cms/?q=node/90),[blog](https://iri-wiki.uni-frankfurt.de/cms/?q=node/90)
or [Twitter account](https://twitter.com/kuronosec).

- ***What is your doctoral thesis about?***

  “It is about creating a security monitoring system for the
  [`ALICE`](https://home.cern/science/experiments/alice) computational
  grid. `ALICE` is one of the major `LHC` experiments. The grid is
  made up of computer centers interconnected around the world that
  allow scientists to run applications for analyzing data obtained
  from particle collisions inside `ALICE`. My project is composed of a
  software framework that isolates applications scientists use in a
  sandbox. Then, it collects information about the behavior those
  applications, classifying them as normal or malicious using Machine
  Learning (`ML`). And finally, it allows performing actions upon
  detection of malicious behavior, such as sending alerts or stopping
  their execution.”

That’s amazing. Researching protecting such a tremendous scientific
*“device”* is undoubtedly a huge challenge. Andrés has been featured
in the prestigious magazine [`Scientific
American`](https://www.scientificamerican.com/article/worlds-most-powerful-particle-collider-taps-ai-to-expose-hack-attacks/).
He told us that the `CERN`, owner of the `LHC`, is a constant target for
cyber attacks and that this is not surprising: many `CERN` systems are
exposed to the Internet. We wanted to know more about `ML` in his work…​

- ***Tell us a bit about how ML contributes to the framework you
  developed***

  “I used two `ML` models. The first performs a classification of
  applications into malicious and non-malicious. The other generates
  synthetic attacks to improve the training of the first.
  I used thousands of examples of typical applications as well as
  `Linux` malware for training and testing both models. My framework
  managed to identify malicious software with an accuracy of `99%` and
  less than `0.06%` of false positives.”

Impressive. We see a link to what we shared days ago on
[antifragility](../seek-chaos/) and this cutting-edge work. By constant
training and exposure to stressors, the framework makes itself better
and better (just like lifting weights). According to [Cybersecurity
Ventures](https://cybersecurityventures.com/cybersecurity-almanac-2019/),
by 2021 it is estimated that cybersecurity damages will add up to `USD`
6 trillion in the world, `3` trillion more than in 2015. These `ML`
designs, capable of detecting security weaknesses and responding are
seen as an answer for the rampant threats nowadays. If you want to dig
deeper into Andrés' work, [here is a
link](https://arxiv.org/abs/1801.04179) of a recent paper.

<div class="imgblock">

![design architecture](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330887/blog/hack-cern/architecture_lhg5cz.webp)

<div class="title">

Figure 2. Gomez Ramirez, et. al. (2018) Proposed Arhuaco design architecture.

</div>

</div>

Now, we turn to more general security-related issues with him.

- **In your opinion, what trends in cybersecurity we should pay
  more attention to?**

  “I think of three relevant topics:

    - One is the use of Artificial Intelligence (`AI`) for both attack
      detection as well as for vulnerability detection. I focused on
      the former in my doctoral research. + +

    - Another is the implementation of cryptographic techniques to
      increase reliance in execution environments, so user privacy is
      improved. For example, by using something called ***homomorphic
      encryption***, an end-user could cipher his/her sensitive
      information before sharing it with a third-party (i.e., a
      company). The third-party can then perform operations over the
      encrypted data and finally, the user deciphers the results. No
      one (especially potential attackers) has access to plain,
      actionable data. Homomorphic encryption is used, for instance,
      in blockchain-based applications. + +

    - The last trend is the emergence of computer systems designed
      from formal mathematical models which, in theory, are
      vulnerability-proof.”

An example of that vulnerability-proof software can be found
[here](https://github.com/project-everest/hacl-star).

As a company focused on proving security in an offensive way, `AI` is
definitely a focus of research for us. Although we haven’t yet got dirty
developing `ML` or `AI` artifacts, is something very likely to happen
soon.

- ***What threats are worth "having on the radar"?***

  “In general, with the rise of `AI`, I believe we will start to see
  more attacks that learn automatically from the environment where
  they are carried out. Attacks on *"Internet of Things"* (`IoT`)
  devices have also wreaked havoc in recent months. Finally, the
  leakage of sensitive user data is becoming more problematic as time
  passes on.”

`IoT` weaknesses and leakage of sensitive information are well under our
scope. We provide [Continuous
hacking](../../services/continuous-hacking/), as well as [One-shot
hacking](../../services/one-shot-hacking/). If you have `IoT` devices
deployed on your premises, we can help you identifying attacks vectors,
as well as providing ways to increase their security. We can help you to
protect better your sensitive information.

Our services rely on highly-skilled security analysts as well as on
technology designed to deliver real value to your company. But, we go
further. [Get in touch](../../contact-us/) so we can discuss how we can
help you.

We continue our conversation with Andrés.

- ***What do you think is a persistent problem within
  organizations?***

  “I would say there are still many companies receiving well-intended
  warnings from third parties concerning security holes in their
  systems. But, instead of taking a good skill in fixing the problems
  and thanking the contributions, what they do is threaten or sue the
  guy pointing to the risk.”

This is a sensitive topic and a critique. We know that some companies
foster this kind of actions in what is called Big Bounty programs, with
clear rules and rewards. These companies, presumably, have reached an
understanding of the costs of a cybersecurity breach, so these programs
are a win-win. Is it a matter of rules? Is it a matter of incentives? It
is a topic worth discussing in more depth in the future.

We want to conclude this post with two quick questions to Andrés:

- ***Where should companies focus their learning efforts to
  improve their risk management?***

  “Organizations should adopt a data-driven strategy and invest in
  automation. They should also invest in research to stay relevant in
  a continuously changing field.”

- ***Do you expect any further development based on your doctoral
  thesis?***

  “I am exploring to go further with the framework. The idea is to
  push what has been developed so far in a research stage into a
  commercial product that can be put to work in different
  organizations.”

We hope you liked this post in which we shared some experiences and
opinions with Andrés. We would love to hear from you on these topics.
Drops us a mail to <communications@fluidattacks.com> and engage with
us\!

Thank you, Andrés\!

## References

1. [Ramirez, A. G., Lara, C., Betev, L., Bilanovic, D. , & Kebschull,
    U. (2018).](https://arxiv.org/abs/1801.04179)
