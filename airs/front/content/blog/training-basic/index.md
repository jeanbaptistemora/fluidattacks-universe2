---
slug: training-basic/
title: We Need More Training in Basics
date: 2019-08-15
subtitle: A chat with Ricardo Yepes. Part 1.
category: interview
tags: devops, training, security
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331106/blog/training-basic/cover_adnkzv.webp
alt: Bookshelf with some books
description: We spoke to the DevOps engineer Ricardo Yepes recently,
  and he shared his current vision of cybersecurity. Here is the first
  part of our conversation.
keywords: Interview, DevOps, Security, Machine Learning, Philosophy, Training,
  Ethical Hacking, Pentesting
author: Julian Arango
writer: jarango
name: Julian Arango
about1: Behavioral strategist
about2: Data scientist in training.
source: https://unsplash.com/photos/uEcSKKDB1pg
---

Ricardo is a `DevOps` engineer in Australia. Previously, he worked for
`Fluid Attacks` as a security analyst and instructor. He also spent a
couple of years developing and maintaining an educational platform
focused on coding and security, where students learned by solving
programming challenges. He also had his feet in academia for a while: he
holds an `MSc` in Engineering and finished his dissertation in Germany.
As with previous interviewees, we reached him out to discuss
cybersecurity.

At first, he shared a bit of his experience in doing his `MSc`. To our
surprise, he wasn’t that enthusiastic.

<div class="blog-questions">

**Why did you get frustrated about research?**

1. The main issue was the friction and the amount of time you have to
    spend justifying ideas already validated by the industry. You end up
    allocating too much energy looking for the right paper or the proper
    journal to support the choice of your methods, which is probably
    already outdated compared to alternative sources of information.
    This is even more pronounced in cybersecurity. + +

2. Another aspect was that the academic settings weren’t fun enough for
    me. I enjoy learning about technology because I can apply my skills
    to solve problems of increasing complexity. However, I found myself
    researching and writing papers without having enough time to play
    with the methods I have designed. Some people like to work on
    improving state of the art in methods and tools by designing
    rigorous experiments. Other people enjoy applying the best-known
    techniques to solve new problems. I discovered that I am in the
    latter group

**What can you say about academia and cybersecurity?**

1. There is a vast gap between what industry needs and what is taught
    in colleges. We need more training in security skills. It isn’t that
    difficult to learn; nonetheless, you still get to know plenty of
    developers with no notion of effective security practices. That’s
    the reason I was attracted to work on an education platform some
    time ago.

**What you just mentioned is paradoxical. Why this paradox?**

1. Some people get into college, waiting to be fed with everything
    needed to succeed in a future job. That job probably doesn’t exist
    yet; that’s the paradox. Therefore, no matter how much knowledge you
    accumulate. At some point, you will need to learn more every day. +
    +

2. For example, when I was an undergrad, all we know today as cloud
    computing wasn’t even mentioned, let alone how to protect those
    environments. In contrast, the industry was promoting these new ways
    of provisioning infrastructure, the tools were getting traction, and
    some companies were spreading knowledge and training people. But,
    this is the nature of our field. Computer science evolves so fast
    that academia is incapable of catching up. Self-teaching and
    self-learning are more widespread these days, and people are
    becoming more aware that they should keep learning.

**How do you study?** **How do you learn what you need to do in your
job?**

1. What I’ve done is learning online through some of the many platforms
    available. I have earned some certifications that are being demanded
    by organizations, like `AWS`, `GCP`, or `Kubernetes`. + +

2. Sometimes I pick a topic I don’t know, set a goal, and start
    browsing web resources. I train myself around specific tasks that
    interest me. Moreover, I also learn every day at work, solving new
    problems.

**Recently, I read somewhere that the most critical skill nowadays**
**for students is to know how to search in Google. You seem to nail
it…​**

1. It isn’t a joke\! You find people these days getting stuck in their
    jobs just because they don’t look for resources online. They might
    say that they need to speak to an expert. Also, these experts many
    times just google things out. It’s more of a mindset, rather than an
    inability. + +

2. I work building secure `IT` infrastructure using tools like
    `Terraform` and `GCP`. I like applying software development
    practices to the process of provisioning cloud resources, also known
    as Infrastructure as Code (`IaC`). You could say I am working on the
    defensive side of security; I have heard you’re doing cool stuff on
    the offensive side as well, aren’t you?

Security, as part of the development process, is essential to `Fluid
Attacks`. We are proud to be working with this approach for several
years now. Our [Continuous Hacking](../../services/continuous-hacking/)
and [One-shot Hacking](../../services/one-shot-hacking/) services rely
on `IaC` to support our customers consistently and faster.

We turned into cybersecurity specifics, and like with the other people
we have spoken with, we asked Ricardo about his opinion on machine
learning (`ML`) and artificial intelligence (`AI`).

**What is your opinion on the contributions from ML and AI to
cybersecurity?** **Do you find hype here?**

1. We’re in the hype phase according to the famous Gartner curve. But,
    indeed, there are several `ML` useful applications. I did some
    research on the topic years ago, and I concluded the field was in
    its early development. Around that time, some people even believed
    `ML/AI` would replace developers in a few years, for example.
    Something went wrong because I still got my paycheck last month
    (laughing). `ML` is a marvelous tool, and its development should
    continue. There are astonishing achievements, for instance, in
    health diagnosis, computers beating humans playing games, etc., with
    clear implications for society. However, those results are very
    domain-specific, and most problems in real life aren’t that well
    defined.

<div class="imgblock">

![Hype cicle for Emerging technologies 2017](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331106/blog/training-basic/emerging-tech-hc-2017_f5jlpr.webp)

<div class="title">

Figure 1. Hype Cycle for Emerging Technologies, 2017.

</div>

</div>

**Do you think ML and AI would soon help in addressing digital threats
better?**

1. To help yes, but not wholly address them. One of the most
    significant sources of vulnerabilities is what happens at the
    software design stage. Weaknesses created *“by design”*. For
    example, in eliciting requirements, some design decisions lead to
    developing functionalities in an insecure way. That is more frequent
    than thought. And this is crazy: these *“by-design”* weaknesses are
    so simple to avoid, that for a competent cybersecurity professional
    is almost unthinkable to find them. The problems with these
    weaknesses, if not identified in a development phase, is that they
    might not be easily fixed when the software is already deployed. + +

2. Perhaps, someday, a software solution could detect automatically
    that kind of problems involving human judgment in the elicitation of
    requirements. If so, we’re far from that.

**Is this you just mentioned linked to the gap** **in teaching secure
software development in academia?** **Do you think this can be solved?**

1. Of course, but it isn’t a particular challenge for universities;
    organizations, specifically development teams, should contribute
    too. Programmers must know this. But, other people involved in
    design processes, such as business analysts and software architects,
    should also get to know more about security. In the initial stages
    of development (requisites, domain analysis, design, etc.) it’s
    enormously helpful to include a cybersecurity guy that supervises
    and teaches people how to think about security and how to infuse it
    from the very beginning —thus avoiding potential setbacks in the
    future. Investing at that level is usually worth it.

</div>

The second part of this conversation will be published shortly. We hope
you have enjoyed this post and we look forward to hearing from
customers, partners, and friends. Do you want to share your thoughts?
[Do get in touch with us\!](../../contact-us/)
