---
slug: switch-git/
title: Git Moving!
date: 2022-01-21
subtitle: You should switch to Git right now
category: opinions
tags: git, software, code, company, devops, cybersecurity
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1642780554/blog/switch-git/cover_git.webp
alt: Photo by Liam Pozz on Unsplash
description: Switching to Git will boost your productivity and allow you to go fast. It will also open up your possibility of achieving DevSecOps with us.
keywords: Git, Version Control System, Source Code, Gitlab, Security, Devsecops, Application, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/4iwLxkESGe4
---

Let's start with a bit of a history lesson.
A few decades ago,
[not all](https://hackernoon.com/how-git-changed-the-history-of-software-version-control-5f2c0a0850df)
software developers
had access to the master version of a software solution project.
In fact, only one of them had access to it
and was responsible for sharing only what was necessary.
For example,
the specific part of code one project member needed to work on.
Suffice to say,
this wouldn't work too well if you were on a schedule
and needed help from several pairs of extra hands.
Anyways,
in those days,
teams who had no copies of previous versions of their projects
risked losing everything in a fleeting moment.

The issue of lack of documentation versioning was tackled
with the birth of version control systems (VCS).
They [are](https://bitbucket.org/product/version-control-software)
basically "a software utility that tracks and manages changes to a filesystem."
In the 1970s,
Marc Rochkind [created](https://www.iiis.org/cds2011/cd2011imc/iceme_2011/paperspdf/fb394vz.pdf)
the first VCS,
the Source Code Control System (SCCS),
in order to answer the question "What changed?"
when something goes wrong in the development.
This was a very important accomplishment
because if someone messed up,
they could just go back to a previous stable version of the code.
That's a neat thing that couldn't be done without a VCS.

The days before VCS were pretty slow.
Today's fast-paced development makes it challenging
to manage the different versions of systems.
As teams need to go fast,
they [need](https://bitbucket.org/product/version-control-software)
to be able to distribute work
and make changes to the same source code at the same time.
Contrary to the old ways of developing software,
VCS [offer](https://about.gitlab.com/topics/version-control/)
the benefit of continuous cooperative
and highly communicative work between team members.

## It's best when everyone gets a clone!

When considering the [kinds](https://www.iiis.org/cds2011/cd2011imc/iceme_2011/paperspdf/fb394vz.pdf)
of VCS that exist,
we need to understand
that they vary according to where the *repository* sits
and where the developer… well, sits.
(Repository is a filesystem that is being tracked for modifications.)
The **local** kind of VCS is relatively simple:
The person works on the same machine where the repository is kept.
What other kinds are there?
Well,
there is a kind that keeps the repository in a **shared folder**
and users from within a local area network can collaborate in it.
However,
it's safer to have a trusted server safeguard your repository,
so,
in the **client/server model** kind of VCS,
the repository sits on the server
and clients can read and submit changes from their machines.

The server model has been known as a centralized VCS.
Developers *commit* changes to a central server
that contains all the versioned files.
(To commit [means](https://faun.pub/centralized-vs-distributed-version-control-systems-a135091299f0)
to record the change in the central system.)
Some centralized VCS [are](https://medium.com/polarsquad/devops-whats-it-all-about-part-2-tooling-git-the-master-of-version-control-systems-59e976c1881e)
Subversion (SVN),
CVS
and Perforce.
The [disadvantages of this model](https://about.gitlab.com/blog/2020/11/19/move-to-distributed-vcs/)
refer to velocity,
workflow flexibility
and safety.
So,
first off,
commits are slow
because they are done through a single network to the central repository.
Further,
if developers are not in the network,
they can't commit.
Lastly and critically,
suppose the only copy of the repository becomes corrupted somehow:
It'd be necessary to wait until the repository is fixed.

Luckily,
there's a more efficient kind of VCS.
Namely,
the distributed one.
This one allows collaboration without needing a central repository.
Its benefits are clear:
**velocity**,
**code quality**
and **collaboration**.

The distributed VCS can be cloned.
In this model,
every developer has a clone as their local repository
and every clone can be used as backup.
It also offers flexibility for personal workflows
because developers can commit to their local repositories while offline.
Through their personal branches
or transient branches
created for making a change,
developers can merge their work into the main repository
and so they are able to go fast.
When mentioning this category,
[Git](https://about.gitlab.com/topics/version-control/) is what comes to mind.
This free and open-source VCS
has been used for software development projects,
large or small.
Some platforms that could host your Git repository are
[GitLab](https://about.gitlab.com/),
[GitHub](https://github.com/),
[Bitbucket](https://bitbucket.org/product),
[Azure DevOps Server](https://azure.microsoft.com/en-us/services/devops/server/),
among others.
At `Fluid Attacks`,
we use GitLab
and can attest to its benefits,
which include boosting productivity,
accelerating delivery,
enhancing traceability,
simplifying audits
and providing security.

We know it's possible
that you feel uneasy thinking about using a VCS
or moving from your centralized VCS to Git.
Indeed, [some mentions](https://stackoverflow.com/questions/2539050/reasons-against-using-git-in-the-enterprise)
have been made
about being afraid
that moving to Git means having no regular support.
However,
it turns out that Git's [community](https://dev.to/t/git)
is constantly there to help.
Also,
even though the change [could](https://blog.inf.ed.ac.uk/sapm/2014/02/14/if-you-are-not-using-a-version-control-system-start-doing-it-now/)
be complicated at first,
it is worth the effort
as your customer base increases
and your team becomes bigger.

## Security as an essential kind of peer review

When a developer is done with the intended change
and wants to incorporate it into the main repository,
then they make a *merge request*.
Basically,
they're proposing a change and are asking their peers to review it.
This is the essence of peer review.
It works wonders
not only because merge requests are saved in the repository,
helping keep track of the changes to the project,
but also because it encourages interactions between developers.

Now,
we would like to propose
that security is also a kind of peer review.
When you integrate security into your pipeline,
even if only with automated tools,
you are trusting the work of people
probably from outside your project
to [review your code](../../solutions/secure-code-review/) for vulnerabilities.
This is key.
If you release your software solution
and it's got commonly known vulnerabilities,
**it won't stand a chance in the wild**.
The best strategy is constantly reviewing for vulnerabilities while developing
and before any changes are made to the main repository.

<div class="imgblock">

![Continuous Hacking flowchart](https://res.cloudinary.com/fluid-attacks/image/upload/v1643984451/blog/switch-git/Git-Figure-1.webp)

<div class="title">

Figure 1. Fluid Attacks' [Continuous Hacking](../../services/continuous-hacking/)
solution flowchart.

</div>

</div>

At `Fluid Attacks`,
we're all for it.
We help our clients [achieve DevSecOps](../../solutions/devsecops/),
securing their projects
as early in the software development lifecycle as possible (see Figure 1).
Everything begins when their management team logs into our application,
the [Attack Surface Manager](https://app.fluidattacks.com/) (ASM).
Once they provide the URL to their Git repository,
it's all ready to start scanning
with all the might of AI and automation.
They get reports through the ASM,
which leads to their remediating the vulnerabilities,
and so the cycle is constantly repeated.
Through our [solutions](../../plans/),
we enable our clients to **go fast without crashing**.
What's more,
clients of our Squad Plan can achieve better precision
(less false positives and false negatives)
as our [highly certified](../../about-us/certifications/) ethical hackers
use [manual techniques](../../categories/)
to test the security of their software.
Want to learn more?
[Contact us](../../contact-us/)\!
