---
slug: purple-team/
title: Do We Need a Purple Team?
date: 2019-10-04
category: politics
subtitle: Understanding Purple Teams
tags: security, testing
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330976/blog/purple-team/cover_ohgfsv.webp
alt: 'Multicolored hallway. Photo by Efe Kurnaz on Unsplash:
  https://unsplash.com/photos/RnCPiXixooY'
description: In this blog, we discuss the fundamentals of Purple Teams
  and possible ways to implement them in an organization successfully.
keywords: Purpleteam, Pentesting, Communication, Cooperation, Hacking,
  Organization, Ethical Hacking, Pentesting
author: Alejandro Herrera
writer: alejandrohg7
name: Alejandro Herrera
about1: Tourism Business Administrator
about2: Passionate about programming
source: https://unsplash.com/photos/RnCPiXixooY
---

A good way to think of Purple Teams is that they are a mixture of Red or
sword, and Blue or shield teams in pentesting processes. They are
professional hackers that simulate attacks and protect an organization’s
information.

## Concept

In cybersecurity, organizations should understand that a Purple Team is
a communication bridge that allows Blue and Red Teams to work together
in a simulated cyberattack. The main goal is to help improve
organization security posture. In other words, they can help coordinate
and increase the effectiveness of both teams. We have to be careful with
the implementation and execution of a Purple team
[<sup>\[1\]</sup>](#r1), as Julian Arango [<sup>\[2\]</sup>](#r6) says:

**A Conflict of Interest?**

> " In some cases, this interaction can propitiate malfunctions inside
> the organizations, especially when the affected parties are biased by
> their interest and can manipulate or conduct the results of a
> pentest.”

## What does a Purple Team do?

Important features are [<sup>\[3\]</sup>](#r2):

1. **Analyze:** They analyze the behavior and interactions between the
    Red and Blue Teams. Throughout the process, they can also generate
    recommendations, suggestions, and improvements for both parties.
    However in practice, if there are not [well-defined cybersecurity
    objectives](../attack-no-announce/) [<sup>\[4\]</sup>](#r7) and
    there are personal interests regarding the test outcome, it is
    likely that there will be a [conflict of
    interest](../conflict-interest/). The organization can then
    encounter a variety of problems including tampering of pentesting
    outcomes and lack of blindspot detection [<sup>\[5\]</sup>](#r6),
    among others.

2. **Detection:** How the Red Team can bypass the detection
    capabilities of the Blue Team.

3. **Remedial Actions:**: They can suggest fixes to avoid
    vulnerabilities.

4. **Transfer**: Ultimately a company derives the maximum value from a
    Purple Team exercise by applying the new knowledge it acquires,
    while at the same time, ensuring stronger defenses to guard its
    information.

## When does an organization need a Purple Team?

When Red and Blue Teams get out of sync with each other and/or have
cooperation issues, it’s time to consider using a Purple Team. Some
common causes that signal the need for a Purple Team are
[<sup>\[6\]</sup>](#r3):

1. **Bad Politics:** Bad organizational politics does not encourage a
    good flow of internal information within an organization. An
    organization may evaluate the success of the Red Team by the amount
    of failed controls from the Blue Team, while the success of the Blue
    Team may be evaluated by the number of alerts. Therefore, partners
    may not be motivated to share information.

2. **Slow Feedback Loop:** Needed information moves too slowly between
    the Red and Blue Teams or, in some cases, does not even move at all.
    There is poor communication between the teams.

3. **Mindset:** Each team works separately to obtain its objectives.
    For instance, the Red Team enhances offensive exploit. The Blue Team
    enhances defensive findings. This mindset can weaken and damage the
    overall security system of an organization.

4. **Arrogance:** Each team believes they are superior to the other
    team, and therefore, neither team recognizes the need to share
    information between them.

5. **Restricted:** The Red Team is pulled inside the organization and
    becomes restricted, ultimately resulting in a catastrophic reduction
    in its effectiveness.

6. **Bad Design:** The Red Team and Blue Team are not designed to
    interact with each other continuously, as a matter of course.
    Therefore, lessons learned on each side remain within each team but
    are effectively lost to the other.

7. **Separate Efforts:** Information security management does not see
    the Red and Blue Teams as cooperating partners within the same work
    project. There are no shared metrics between them.

<div class="imgblock">

!["Red vs Blue"](https://res.cloudinary.com/fluid-attacks/image/upload/c_scale,w_600/v1620330974/blog/purple-team/redblue_z6vcfk.webp)

<div class="title">

Figure 1. Red vs Blue, source: [Photo by Samuel Zeller on
Unsplash](https://images.unsplash.com/photo-1492435793713-b1f8565c25ae?ixlib=rb-1.2.1&auto=format&fit=crop&w=334&q=80).

</div>

</div>

If your organization has one or more of these issues, a Purple Team
could be your solution. Rather than considering it as a separate group
of people, organizations should consider a Purple Team as a bridge
facilitating maximum effective communication between Red and Blue
partners.

## What is not the solution?

It is not, under any circumstances, recommended that an organization use
a permanent and separate Purple Team as intermediaries between the Red
and Blue Teams. This would not solve the underlying problem, which is a
breakdown in communication and collaboration between these teams.

## So what are the possible solutions?

We need to improve communication and cooperation between teams. The
following techniques can be used to accomplish both of these.

- **Team Engagement:** A third party analyzes how the Red and Blue
  teams regularly communicate and cooperate. Based on this analysis,
  the third-party makes recommendations. This measure is momentary and
  finite. The main goal of this technique is [<sup>\[7\]</sup>](#r4):
  to make the communication process smoother and to ease knowledge
  transfer.

    1. **Team Exercise:** Both teams are monitored in real-time to see
        how they work. The main goal of this technique is
        [<sup>\[8\]</sup>](#r5): to evaluate your security controls and
        ability to detect attacks, to compromise, for lateral movement,
        to command and to control communications, and data exfiltration.
        This technique enriches and validates the detection mechanisms
        used in situ and helps to identify and reduce cyber attack
        paths.

    2. **Team Meetings:** Periodically, Red and Blue Teams meet to
        share knowledge and give feedback about attacks and defenses
        used in the pentest process.

## The benefits of appropriate implementation

Appropriate implementation will create a better flow of information
between Red and Blue Teams which means, Red Team will learn how Blue
Team is detecting and mitigating their offenses, and Blue Team will
understand how Red Team is bypassing their defenses. This loop of
enhanced communication and knowledge sharing between teams improves the
organization’s security posture.

## Conclusion

A Purple Team should be understood as a temporary intermediary
facilitating communication and collaboration between Red and Blue Teams,
allowing information to flow in a continuous loop which enhances the
abilities of both teams. Under no circumstances should it be used as a
permanent group to mediate the relationship between a Red and Blue Team.

## References

1. [My Experience Coleading Purple
    Team.](https://www.cgisecurity.com/2018/05/my-experiences-leading-purple-team.html).

2. [The Roles of Red, Blue and Purple
    Teams](https://www.itlab.com/blog/understanding-the-roles-of-red-blue-and-purple-security-teams).

3. [The Definition of a Purple
    Team](https://danielmiessler.com/study/purple-team/).

4. [The Purple Team
    Pentest](http://www.circleid.com/posts/20161130_the_purple_team_pentest/).

5. [Purple Team Assessment
    Service](https://www.swordshield.com/purple-team-assessment-service/).

6. [A Conflict of Interest?](../conflict-interest/)

7. [Attacking Without Announce](../attack-no-announce/).
