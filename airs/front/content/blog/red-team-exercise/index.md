---
slug: red-team-exercise/
title: Red Team Exercise
date: 2019-09-18
category: documentation
subtitle: What is a Red Team exercise?
tags: security, testing
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331047/blog/red-team-exercise/cover_kmvlzc.webp
alt: 'Foosball red vs blue. Photo by Stefan Steinbauer on Unsplash:
  https://unsplash.com/photos/va-B5dBbpr4'
description: Here we give the reader a general context about what a
  Red Team does and the main strategy used during a Red Team exercise
  and its benefits for customers.
keywords: Redteam, Red, Team, Pentesting, Attack, KillChain, Hacking, Business,
  Ethical Hacking, Pentesting
author: Anderson Taguada
writer: anders2d
name: Anderson Taguada
about1: Software Engineering undergrad student
about2: '"Test" -Anonymous Tester'
source: https://unsplash.com/photos/va-B5dBbpr4
---

Red Team refers to a team of professional hackers that attempts to
access a system by simulating a cyberattack. During a Red Team exercise,
each team member plays a specific role while the team, as a whole, uses
offensive strategies, a variety of techniques, and tools in order to
weaken a system.

## Red Team (the concept)

In cybersecurity, a Red Team’s knowledge, skills, and abilities go
beyond those of a pentester whose role is to search, find, and report
system vulnerabilities. A Red Team also simulates a real attack by
assuming an adversarial role.

## Divide and conquer

Red Team members possess different [hacking
skills](https://www.tutorialspoint.com/ethical_hacking/ethical_hacking_skills.htm)
in order to simulate a real attack. This attack may be structured and
divided, with the attackers focusing on specific activities to achieve
success. Therefore, in a Red Team, you will find team members with the
following skills:

<div class="imgblock">

![Possible roles in a Red Team via Medium.com.](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331046/blog/red-team-exercise/skillredteam_khyqsr.webp)

<div class="title">

Figure 1. Possible roles in a Red Team via
[medium.com](https://medium.com/@redteamwrangler/how-do-i-prepare-to-join-a-red-team-d74ffb5fdbe6).

</div>

</div>

Regarding the information above, we spoke with [Andres
Roldan](../../about-us/people/aroldan/). When we asked him about the Red
Team exercise done by `Fluid Attacks`, he said:

<div class="blog-questions">

1. "First, the Red Team proposes hacking objectives. For example:
    escalate privileges, modify system files or install a backdoor to do
    it. We use the kill chain strategy."

</div>

Take a look at this video from `Fox9` about a Red Team exercise.

<div style="text-align: center;">
<iframe
  width="560"
  height="315"
  src="https://www.youtube.com/embed/YIV0xvatX0M"
  frameborder="0"
  allowfullscreen>
</iframe>
</div>

## What is Kill Chain?

Kill Chain is a military term to describe the steps in launching an
attack. One of its models is the `F2T2EA` and includes the following
phases:[\[1\]](#r3)

1. **Find**: Identify a target using surveillance, reconnaissance data
    or intelligence gathering.

2. **Fix**: Fix the target’s location. Obtain specific coordinates for
    the target either from existing data or by collecting additional
    data.

3. **Track**: Monitor the target’s movement. Keep track of the target
    until either a decision is made not to engage the target or the
    target is successfully engaged.

4. **Target**: Select an appropriate weapon or asset to use on the
    target to create desired effects. Apply command and control
    capabilities to assess the value of the target and the availability
    of appropriate weapons to engage it.

5. **Engage**: Apply the weapon to the target.

6. **Assess**: Evaluate the effects of the attack, including any
    intelligence gathered at the location.

<div class="imgblock">

![`F2T2EA` - The Kill Chain](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331046/blog/red-team-exercise/f2t2ea-killchain_lhmilw.webp)

<div class="title">

Figure 2. `F2T2EA` - The Kill Chain via [Biz -n- Seen
blog](http://myarick.blogspot.com/2014/02/f2t2ea.html).

</div>

</div>

## Cyber Kill Chain

This term was adopted by [Lockheed
Martin](https://www.lockheedmartin.com/en-us/index.html) and its
incident team to prevent cyberattacks. Cyber Kill Chain has the
following phases:

1. **Reconnaissance**: Learning about the target using a variety of
    different techniques.

2. **Weaponization**: Combining your vector of attack with a malicious
    payload.

3. **Delivery**: Transmitting the payload via a communications vector.

4. **Exploitation**: Taking advantage of a software or human weakness
    in order to get your payload to run.

5. **Installation**: The payload establishes the persistence of an
    individual host.

6. **Command & Control (C2**): The malware calls home, providing
    attacker control.

7. **Actions on objectives**: The bad actor steals or does whatever he
    was planning on doing.

<div class="imgblock">

![Cyber Kill Chain Phases](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331045/blog/red-team-exercise/cyber-kill-chain_hq3v77.webp)

<div class="title">

Figure 3. Cyber Kill Chain Phases via [Lockheed
Martin](https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html).

</div>

</div>

## Cyber Kill Chain 3.0

This is an update of the cyber kill chain for better defense by [Corey
Nachreiner](https://www.watchguard.com/es/wgrd-about/leadership/corey-nachreiner),
Watchguard Chief Technology Officer.

Cyber Kill Chain 3.0 has the following phases[\[2\]](#r1):

1. Recon

2. Delivery

3. Exploitation

4. Infection

5. Command & Control - Lateral Movement & Pivoting

6. Objective/Exfiltration.

As you can see, version 3.0 has minor changes designed for better
security defense, but those are not unique strategies. As mentioned in
[Help Net
Security:](https://www.helpnetsecurity.com/2015/02/10/kill-chain-30-update-the-cyber-kill-chain-for-better-defense/)

<div class="blog-questions">

1. "Security professionals have differing opinions on the effectiveness
    of the kill chain as a defense model. Some love it, pointing out how
    several successful infosec teams use it, while others think it’s
    lacking crucial details, and only covers a certain type of attacks.
    I think there is truth to both views, so I’d like to propose three
    simple steps to make the kill chain even better, let’s call it `Kill
    Chain 3.0`."

</div>

Therefore, Kill Chain is not the only option. You can also adapt your
attack [strategy](https://en.wikipedia.org/wiki/Military_strategy).

## Customer benefits

Then, what are the benefits on the client side? Simply put, Red Team’s
cyberattack simulations expose the weaknesses within a client’s systems
or applications so that a client can better protect its information from
a real attack scenario.

The client can then fix, build, design, and maximize its
cybersecurity[\[3\]](#r4); this is why the [Blue
Team](https://en.wikipedia.org/wiki/Blue_team_\(computer_security\))
exists. Like Red Team, Blue Team also has its defensive strategies, but
we will save that discussion for a future post.

## Conclusions

According to
[Medium.com](https://medium.com/@redteamwrangler/how-do-i-prepare-to-join-a-red-team-d74ffb5fdbe6),
a Red Team member must have an offensive mindset. For this reason,
"CTFs, wargames, or pen testing labs are a great way to exercise
offensive mindset"[\[4\]](#r5). At `Fluid Attacks`, every new member
trains in hacking and programming challenges to check and assess their
level of offensive mindset.

Our current talents are in the [Top 10 for
Colombia](https://www.wechall.net/country_ranking/for/31/Colombia), and,
in fact, some of them are in the [Top 100
Worldwide](https://www.wechall.net/ranking).

## References

1. [Kill Chain 3.0: Update the cyber kill chain for better
    defense](https://www.helpnetsecurity.com/2015/02/10/kill-chain-30-update-the-cyber-kill-chain-for-better-defense).

2. [Red Team
    Exercises](https://sci-hub.tw/https://ieeexplore.ieee.org/abstract/document/8406561).

3. [Kill chain](https://en.wikipedia.org/wiki/Kill_chain).

4. [Red Teaming Overview, Assessment &
    Methodology](https://resources.infosecinstitute.com/red-teaming-overview-assessment-methodology/#gref).

5. [How Do I Prepare to Join a Red
    Team?](https://medium.com/@redteamwrangler/how-do-i-prepare-to-join-a-red-team-d74ffb5fdbe6)
