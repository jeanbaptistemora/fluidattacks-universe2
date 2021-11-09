---
slug: attack-no-announce/
title: Attacking Without Announce
date: 2019-01-11
category: opinions
subtitle: Nobody knows, but everything is allowed
tags: protect, information, business, red-team, blue-team, policies
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330672/blog/attack-no-announce/cover_fx1pcf.webp
alt: Executive leaking business information
description: We want to guide you about some management policies we suggest
  that you could take to answer with high precision
  how secure your information is.
keywords: Business, Information, Security, Policy, Protection,
  Hacking, Best Practices,Ethical Hacking, Pentesting
author: Jonathan Armas
writer: johna
name: Jonathan Armas
about1: Systems Engineer, Security+
about2: Be formless, shapeless like water, Bruce Lee
source: https://unsplash.com/photos/QBpZGqEMsKg
---

We talk a lot about the advantages of extreme connectivity and
information availability, but so little about how our company’s data,
client’s data, or even personal data is secured. Here we want to guide
you about some management policies we suggest that you could take in
advance to be able to answer with high precision how secure your
information is, how effective your defense measurements are, and also
what could happen if you don’t apply these policies.

From our experience, we know that company heads usually assume that
"buying more technology" should solve all their security problems. Such
a solution is, in fact, the main cause of the issue, because poorly
implemented, built, or configured technology is the source of all
vulnerabilities.

For modern companies, protecting their information by making it
inaccessible, hiding it, or keeping it on paper is no longer a viable
option. In a world where digital transformation is the norm, exposing
more information to the client is a must. This transformation’s benefits
go from improving times and transaction costs, to the rising of service
windows and client satisfaction. Operations that were only possible
on-site during office hours are now 24 hours a day, 7 days a week, all
year long.

However, these benefits bring new possible dangers: Can the buyer modify
the product price before paying for it? Can an employee know the salary
changes of his coworkers? Can members of the labor union read board
minutes? Can a guest get network administrator passwords? Can someone
connect to the enterprise network, turn on a mic on the manager’s
computer, and listen to conversations? Can a client modify the website
of my company? Can I check the medical record of another person from the
internet?

## Securing your organization

The question “how secure is my organization” is answered by making real
(well meant) attacks; this goes by many names: ethical hacking,
penetration testing, and red teaming, among others. The first policy we
recommend is:

1. **Continuous attacks** on your organization, in order to find
    vulnerabilities that allow malicious attackers to take control of
    your information. The word 'Continuous' means that these exercises
    must be performed with a specific and immovable frequency
    (quarterly, biannual, etc.). When this policy isn’t clear,
    organizations tend to stop further attacks with the excuse of being
    unable to fix the vulnerabilities found in the previous cycle. Once
    your organization’s policies evolve into periodic exercises of
    continuous attacks, the next policy is to do them quietly and
    unexpectedly.

2. **Zero-knowledge attacks**. It makes no sense that the ones who
    attack (red team) perform the test when the defenders (blue team)
    are aware of these intrusions' time and place. It’s absurd for red
    team members to report advances or ask for permission (in the scope
    of these attacks) from blue team members, someone within the
    organization that could have links with defense software/hardware
    vendors or bosses that might be compromised. In order to know with
    certainty the security level of your company, these exercises must
    be as close to reality as possible. In real life, a malicious
    attacker will not notify when, how, and where he might attack, what
    techniques he might be using, what the penetration level is, what
    machines he owns, and what information has been disclosed. Because
    of this, we must maintain a minimum privilege information disclosure
    about the test. Only a minimum amount of personnel should know about
    it. This is known as a zero-knowledge policy.

    <div class="imgblock">

    ![Red team vs blue team](https://res.cloudinary.com/fluid-attacks/image/upload/c_scale,w_500/v1620330673/blog/attack-no-announce/red-blue_pzcaso.webp)

    <div class="title">

    Figure 1. Security Exercises: Red team vs. Blue team

    </div>

    </div>

    This policy implies that those responsible for the security of
    organizations shouldn’t be the ones who organize and coordinate an
    ethical hacking test. This is due to a possible tendency for them,
    with the information of the attack, to prepare for it
    unrealistically, limit its scope to strong zones, and filter out
    critical vulnerabilities to their managers to avoid risking their
    current positions. Even though it’s now a trend to have Purple
    Teams, a combination of attackers and defenders, we should clearly
    define our objective: knowing precisely the security level. The
    existence of these mixed teams creates the possibility of polluting
    test results because these teams create a conflict of interest in
    the company’s organizational design.
    Proceeding with the last policy brings an outstanding advantage:
    knowing your organization’s real detection and reaction skills in
    the event of an attack. If the blue team doesn’t know if the
    attacker is a 'white hat' hacker (members on red teams are these
    type of hackers) or a 'black hat' hacker (a malicious one), they
    will always be in a state of alert and will respond according to the
    defined procedures until the end: blocking, reporting, handling
    incidents, etc. The following is our third policy:

3. **React until the end** to every detection, without taking into
    account the hacker’s intentions. This approach keeps the incident
    response engine oiled and well maintained, allows to test the
    quality of the hired red team, measures the efficiency of your
    investments on defense, and finally helps you achieve cost
    reductions or apply penalties that, after some frequency, make the
    attacking exercise pay for itself.

    <div class="imgblock">

    ![Information protection](https://res.cloudinary.com/fluid-attacks/image/upload/c_scale,w_500/v1620330670/blog/attack-no-announce/protect_gosch3.webp)

    <div class="title">

    Figure 2. Continuous protection of business information

    </div>

    </div>

    The direct implication of the last two policies is our next policy:

4. **Total intrusion:** The red team must have a complete authorization
    on paper, email, and all forms of legal protection, from the highest
    authority of the company (CEO or manager) to do any offensive
    tactic, i.e., get any information, modify any data, access any
    workstation, or shut down any service. Everything should be allowed
    to ensure maximum criticality and compromise security at the highest
    level. If this policy isn’t in place, the red team that you hired
    will have their hands tied and not be allowed to find real
    vulnerabilities, explore existing paths that a malicious attacker
    might walk, and show you your real security flaws. In the end, if on
    the ethical hacking tests they don’t find anything significant, it
    surely will be due to the limitations that you imposed on the red
    team, and your doubts on whether your security is genuine or fake
    will rise. As a final point, we want to invite you to one of the
    most forgotten aspects of the ethical hacking tests; we call it the:

5. **Coherence policy:** If you ask a manager: Between availability or
    confidentiality, what is most important? Most of the time, the
    answer will be both. But if you ask: Will you shut down your servers
    given the presence of an attacker? Saying yes to that question puts
    confidentiality above availability. The answer that you will find is
    that managers would rather maintain their servers on and try to deal
    with the attacker. It is common for most organizations to have
    availability higher than confidentiality and integrity in the
    precedence list. It is paradoxical that, even though availability is
    the most important of the triad, they won’t authorize red teams to
    test `DoS` (denial of service) attacks survival rate. In this case,
    the invitation is: turn your restrictions into encouragement to
    attack for the red team. In this way, you can verify with an ally
    how vulnerable your company is to malicious attackers.

## Conclusion

With these simple policies, **continuous attacks**, **zero-knowledge**,
**react until the end**, **total intrusion** and **coherence**, you can
know how secure your systems really are, improve your security at
vertiginous rates and save money by not buying technologies that
generate huge and incomprehensive vulnerability reports, many of those
with false positives and a lack of context about their real impact on
your organization.
