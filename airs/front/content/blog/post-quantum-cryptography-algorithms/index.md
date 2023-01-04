---
slug: post-quantum-cryptography-algorithms/
title: Approved Post-Quantum Cryptography?
date: 2022-07-22
subtitle: NIST chose four algorithms, and four others are pending
category: politics
tags: cryptography, cybersecurity, compliance
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1658499864/blog/post-quantum-cryptography-algorithms/cover_post-quantum-cryptography-algorithms.webp
alt: Photo by Billy Huynh on Unsplash
description: NIST chose the first four quantum-resistant cryptography algorithms. Here you'll learn about it with an intro to public key cryptography and quantum computing.
keywords: Quantum, Cryptography, Post Quantum Cryptography, Quantum Resistant Cryptography, Quantum Computers, Public Key Cryptography, Nist, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/W8KTS-mhFUE
---

A few days ago,
the U.S. Department of Commerce's
National Institute of Standards and Technology
(NIST) announced that the first four cryptographic algorithms
to withstand the potential assault of future quantum computers
were already selected.
It took six years for this to happen.

[By the end of 2016](https://www.nist.gov/news-events/news/2016/12/nist-asks-public-help-future-proof-electronic-information),
NIST publicly called for help
to avert the *imminent* threat of quantum computers
against information security.
It appealed to cryptographers worldwide to devise,
develop and vet new methods
to protect the confidentiality and integrity of information
from such devices that could break the encryption codes
we currently rely on.
Those experts who wanted to participate had until November 30, 2017,
to send their proposals.
From there,
they had to present them
in order to move on to an assessment phase
in the following years.

NIST speaks of imminent danger
because practical quantum computers have not yet been built.
[However](https://csrc.nist.gov/projects/post-quantum-cryptography),
in recent years
there has been a great deal of research on these computers,
which could solve very complex mathematical problems
(including those used for current encryption systems)
that can be intractable for conventional devices.
No one knows exactly
when a large-scale quantum computer might be built.
Still,
many already consider it more than a mere physical possibility,
a major engineering challenge for the near future.
In 2016,
some people were already making predictions
that these computers would be ready in a couple of decades.

A large-scale quantum computer could jeopardize,
for example,
an encryption system widely used nowadays by governments and industries
called public key cryptography.
Hence the need to quickly develop
the so-called post-quantum or quantum-resistant cryptography,
which,
indeed,
at NIST would replace three of its existing cryptographic standards
([FIPS 186-4](http://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf),
[NIST SP 800-56A](http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-56Ar2.pdf)
and [NIST SP 800-56B](http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-56Br1.pdf))
that use forms of public key cryptography.

Before mentioning the quantum-resistant algorithms selected by NIST,
let's elaborate upon a couple of key terms:
public key cryptography and quantum computing.

## Public key cryptography

[Also known as asymmetric cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography),
public key cryptography is an encryption system
for transforming and protecting information
when it is sent from one individual to another.
In this system,
everyone uses pairs of related keys:
a public key,
which is known to others,
and a private key,
which is known only to the owner.
These keys are very long numbers.
Both are generated from a large random number
using the same cryptographic algorithms
based on one-way functions.
These functions are so named
because the return to the input
from the output delivered by them
is pretty complex.

Each public key is distributed without any problem
so that anyone can encrypt with it a message addressed to its owner.
The latter,
with only their private key,
could decrypt the encoded information.
[These keys are](https://www.zdnet.com/article/quantum-computers-could-one-day-reveal-all-of-our-secrets/)
inevitably linked to each other.
The security of this system
lies in the complexity of obtaining the private key
from the public key,
which would involve the factoring of large numbers.

The trouble is that
quantum computers are expected to be able to break this mode of encryption
in a tiny amount of time,
with calculations taking perhaps a few minutes,
compared to the thousands or millions of years
it might take today's supercomputers to do so.
Quantum computers could apply quantum algorithms,
like the [one developed by mathematician Peter Shor](https://en.wikipedia.org/wiki/Shor%27s_algorithm)
in 1994,
which, in theory, can crack such public key cryptography.
The necessary conditions would be that
the computer where the algorithm operates has enough qubits
and does not manifest noise and lack of coherence.
But, what's a qubit?

## Quantum computing

Over the years,
scientists have been studying
the tricky and enigmatic world of atoms and their components,
such as electrons and protons.
[These so-called quantum particles](https://www.zdnet.com/article/what-is-quantum-computing-everything-you-need-to-know-about-the-strange-world-of-quantum-computers/)
are known to have enormous potential
to contain and process vast amounts of information.
Quantum computing involves controlling these particles,
that is,
isolating and keeping them in a special processor for manipulation.

Instead of bits,
the minimal units of information of classical computers,
we refer to qubits,
aka quantum bits,
for quantum computers,
which consist of quantum particles loaded with data.
A peculiar property of these particles is called superposition,
which allows them to exist in several states at the same time.
Thus,
unlike the inflexible bit,
the qubit can be a one and a zero simultaneously.
In addition to this property,
there is another one called entanglement
that allows the particles to be physically linked.
Consequently,
the incorporation of a new qubit to a system
leads it to grow in capacity exponentially and not linearly,
as in the case of bits.

Depending on such characteristics,
qubits can explore several routes in parallel,
performing multiple computations at the same time to solve a problem.
Apart from a downside,
such as the aforementioned breakdown of public key cryptography,
the enormous power of these new computers would bring significant benefits
to fields such as climate modeling and drug discovery.

Currently,
various companies have developed quantum processors of different types,
thanks to the diverse and complex means
by which particles can be obtained
and isolated from any alteration in the environment
to generate qubits.
For instance,
IBM and Google have developed so-called superconducting processors
that make use of electrons
and employ very low temperatures for their control.
These companies have resorted to technologies that,
for now,
are too difficult to scale up,
so the results remain limited.
As [Leprince-Ringuet comments in ZDNet](https://www.zdnet.com/article/what-is-quantum-computing-everything-you-need-to-know-about-the-strange-world-of-quantum-computers/),
"Right now,
with a mere 100 qubits being the state of the art,
there is very little that can actually be done with quantum computers.
For qubits to start carrying out meaningful calculations,
they will have to be counted in the thousands,
and even millions."

[Back in 2019](https://www.zdnet.com/article/google-weve-made-quantum-supremacy-breakthrough-with-54-qubit-sycamore-chip/),
Google,
with its 54-qubit superconducting processor Sycamore,
reported having achieved in 200 seconds the answer to a problem
that would have taken a current supercomputer 10,000 years to reach.
[Not long after](https://www.zdnet.com/article/quantum-supremacy-milestone-achieved-by-light-emitting-quantum-computer/),
researchers at a university in China reported that
their processor also completed in 200 seconds a task
that would have taken classical computers 600 million years to finish.
In both cases,
the challenges were very specific and of little real utility.
Apart from the need for more qubits to solve more useful computations,
another issue to keep in mind is that qubits are unstable,
and this can lead to miscalculations.

The development of a large-scale quantum computer is a clear goal
in a wild race of international companies and governments
with diverse methods under exploration and assessment.
As we have pointed out,
achieving this goal,
apart from some benefits,
may entail substantial risks to information privacy.
In fact,
[in October last year](https://www.dni.gov/files/NCSC/documents/SafeguardingOurFuture/FINAL_NCSC_Emerging%20Technologies_Factsheet_10_22_2021.pdf),
the U.S. National Counterintelligence and Security Center
highlighted quantum computing as one of five key technology sectors
that may pose threats to the country.
The others were artificial intelligence,
bioeconomy, autonomous systems and semiconductors.
The idea that countries like China could lead these sectors
in the next decade
is quite worrying for world powers like the U.S.

In line with the above,
[just this May](https://www.whitehouse.gov/briefing-room/statements-releases/2022/05/04/national-security-memorandum-on-promoting-united-states-leadership-in-quantum-computing-while-mitigating-risks-to-vulnerable-cryptographic-systems/),
the White House expressed the desire of the U.S. government
to be at the forefront of quantum information science
and the responsibility to migrate its cryptographic systems
to mitigate quantum risk asap.
And although official standards
for quantum-resistant cryptography
are not yet ready,
recent algorithm choices by NIST suggest that
it is getting closer.

## The first four quantum-resistant cryptographic algorithms

[NIST's post-quantum cryptography program](https://www.nist.gov/news-events/news/2022/07/nist-announces-first-four-quantum-resistant-cryptographic-algorithms)
has leveraged cryptography experts around the world
for the generation of algorithms
leading to the establishment of the aforementioned standards
in about two years.
[More than sixty were the algorithms](https://www.nist.gov/news-events/news/2020/07/nists-post-quantum-cryptography-program-enters-selection-round)
received by NIST,
of which [they chose the following four](https://csrc.nist.gov/Projects/post-quantum-cryptography/selected-algorithms-2022):
[CRYSTALS-Kyber](https://pq-crystals.org/kyber/index.shtml),
[CRYSTALS-Dilithium](https://pq-crystals.org/dilithium/index.shtml),
[FALCON](https://falcon-sign.info/)
and [SPHINCS+](https://sphincs.org/).
However,
there are presently four other algorithms under evaluation
that could be added to the shortlist soon.

It is envisioned that
the NIST post-quantum cryptographic standards will be able
to offer solutions for different situations with different systems
from multiple approaches and alternatives.
Thus the selection of various algorithms
that are mainly designed [to respond to two tasks](https://www.nist.gov/news-events/news/2022/07/nist-announces-first-four-quantum-resistant-cryptographic-algorithms):
General encryption,
which is used for the protection of information
exchanged over public networks,
and digital signature,
which is used for identity authentication.

Among the four selected algorithms,
CRYSTALS-Kyber is the only one
that would be used for general encryption;
the other three would be used for digital signatures.
Moreover,
concerning the mathematical problems they take as a basis,
SPHINCS+ is the only one that uses hash functions,
while the other three rely on structured lattices.
The four algorithms still under evaluation are designed for general encryption
and do not use any of the above mathematical methods.
All are expected to become intractable
for both conventional and quantum computers.

Though the new NIST standards are still under development,
this organization is encouraging security experts
to explore the chosen algorithms
and think about how their applications would use them.
For now,
without planning to integrate them
since changes may occur before the standards are finalized.
Many researchers may even take these algorithms
and try to find weaknesses in them
in order to contribute to their modification or maturation.

The transition to post-quantum cryptography protocols has to take place
when the standards are ready,
but it is something we can get involved in
from [sites like this one from NIST](https://www.nccoe.nist.gov/crypto-agility-considerations-migrating-post-quantum-cryptographic-algorithms).
This is something
that all organizations in the digital world need to be prepared for,
mainly so that we don't get any nasty surprises
in terms of cybersecurity.
Be careful!
[The media are already sounding the alarm](https://www.zdnet.com/article/quantum-computers-could-crack-encryption-warns-white-house-as-it-details-action-plan/)
about those criminals
who are currently bent on stealing encrypted data
in the hope of decrypting it
as soon as they get their hands on the longed-for quantum computers.

Concerned about your organization's cybersecurity?
We invite you to download and review `Fluid Attacks'` latest annual report,
[State of Attacks 2022](https://try.fluidattacks.tech/report/state-of-attacks-2022/).
Benchmark against our figures
how you are handling security in your organization.
Want to improve?
Get to know now our comprehensive [Continuous Hacking service](../../services/continuous-hacking/).
