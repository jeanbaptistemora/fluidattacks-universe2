---
slug: aws-devsecops-with-fluid-attacks/
title: How We Boost AWS DevSecOps
date: 2022-10-24
subtitle: Continuous manual security tests for AWS CAF compliance
category: philosophy
tags: cybersecurity, devsecops, cloud, company
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1666640460/blog/aws-devsecops-with-fluid-attacks/cover_aws.webp
alt: Photo by Pejvak Samadani on Unsplash
description: AWS has sketched the way to achieve DevSecOps and provided its Cloud Adoption Framework. In it, it advises pen testing and red teaming, two things we excel at.
keywords: Devsecops, Aws Devsecops, Aws Devsecops Tools, Cloud Devsecops, Devsecops On Aws, Aws Cloud Adoption Framework, Red Teaming, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/rDQFKhNiHzs
---

[Amazon Web Services](https://aws.amazon.com/what-is-aws/) (AWS)
makes it easier and cheaper to develop scalable apps.
With a list of hundreds of services that is continually growing,
this leading cloud platform offers a highly granular approach
to infrastructure as a service.
Furthermore,
its highly redundant infrastructure
extended around the world
guarantees availability and reliability.
Accordingly,
it pays attention to security of and in the cloud.
It is with respect to the latter that AWS enables users
to enhance their DevSecOps capabilities.

But [DevSecOps](../devsecops-concept/) has been misinterpreted by many
as merely using automated tools to test security.
As AWS itself advises
in its [Cloud Adoption Framework](https://aws.amazon.com/professional-services/CAF/)
(CAF),
manual techniques such as [**pentesting**](../what-is-manual-penetration-testing/)
and [**red teaming**](../what-is-red-team-in-cyber-security/)
should be leveraged as well
to identify security issues.
This is critical,
since our ethical hackers [often find](../secure-infra-code/) AWS credentials
in code
and misconfigurations in AWS services.
In this blog post,
we talk about how `Fluid Attacks` boosts your AWS DevSecOps implementation
by deploying manual techniques in combination with automated testing.

## Security in and of the pipeline

Let us first remind you of the cloud security [shared responsibility model](../shared-responsibility-model/)
(SRM) adopted by AWS and several others in the big league.
Why, though?
Because lack of knowledge or negligence are leading to vulnerabilities
of the kind that are exploited on a daily basis.
So,
we all need to be aware
of what AWS is going to deal with regarding security,
and what lies in our hands.

When AWS talks about security of the cloud,
it means the things for which AWS is accountable.
This includes maintaining their availability zones
and building security features into their products
(e.g., making sure the users have the options
to restrict access to pipeline resources
through IAM roles and S3 bucket policies,
encrypt data at rest and in transit
and store data and secrets safely).

Security in the cloud,
however,
is our responsibility.
We users are accountable
for the security of what we deploy in the cloud
and our configuration of AWS services.
The sooner we find and fix issues in those respects, the better.
It is in this matter that the adoption of [cloud DevSecOps](../why-is-cloud-devsecops-important/)
is crucial.

## DevSecOps on AWS with Fluid Attacks

[DevSecOps](../devsecops-concept/) is a culture
that stems from integrating security seamlessly
into the entire development and operations workflows.
This means,
and this is critical:
Security is worked into the early stages
of the software development lifecycle (even from the planning stage).
(See [here](../how-to-implement-devsecops/)
how you can implement DevSecOps.)
When this is attempted in the cloud,
additional security requirements arise,
such as the proper configuration of cloud services
and continuous security testing of infrastructure as code (IaC) files
and container images.

AWS has provided steps to support DevSecOps with AWS services
and automated security testing tools.
Also,
it has published its [CAF](https://aws.amazon.com/professional-services/CAF/),
which contains a security perspective.
In it,
AWS briefly states prescriptive best practices
that improve the security status of cloud application projects.

From the outset,
you should verify that you have given some thought and started
best practices of a directive nature in the AWS CAF,
which are those that aim at enhancing **security governance**
and **security assurance** capabilities.

Mainly, concerning the former,
you should have identified the specific risks to your assets
and the shared responsibility for security
by everyone in your organization.
From this knowledge,
you can develop, maintain and communicate policies,
responsibilities, accountabilities, etc.

As for security assurance,
you would need to review the precautions you take
with respect to privacy and security configurations through controls
(e.g., making sure that account credentials are rotated,
deleting inactive IAM users and unused roles, etc.).

The CAF also contemplates best practices of a responsive nature,
which would enhance your **incident response** capability.
In short,
they state
that the AWS environment should be recognized in your incident response plans
and such plans need to be simulated.

But the capabilities in the CAF that are closer
to what we aim at strengthening at `Fluid Attacks`
are those of preventive and detective nature.
Here they are,
along with a summed-up version of the best practices in each:

- **Identity and access management:**
  Having controls
  that verify the identity of people and machines
  and validating
  that account permissions do not violate the principle of least privilege.

- **Infrastructure protection:**
  Guarding against unauthorized access
  to systems and services within your workload (i.e.,
  processes and resources that support your application
  and the interaction users have with it).

- **Data protection:**
  Following security requirements regarding data storage and encryption.

- **Application security:**
  Finding and remediating vulnerabilities during the SDLC.

- **Threat detection:**
  Deploying monitoring
  to identify security misconfigurations,
  vulnerabilities and unexpected behavior.

- **Vulnerability management:**
  Identifying, characterizing, reporting on
  and mitigating security vulnerabilities.

<cta-banner
  buttontxt="Read more"
  link="/solutions/devsecops/"
  title="Get started with Fluid Attacks' DevSecOps solution right now"
/>

With the purpose of supporting these capabilities,
there are AWS DevSecOps tools
(e.g., AWS code scanning and vulnerability management tools)
that run automatically and continuously in the CI/CD pipeline.
DevSecOps software that runs seamlessly with the service AWS CodeBuild -which
compiles code, runs tests and produces software packages- can perform
static application security testing (SAST),
software composition analysis (SCA)
and dynamic application security testing (DAST)
at stages of development earlier than the traditional testing phase.
The first technique analyzes source code for known security vulnerabilities,
the second finds vulnerable third-party software,
and the third assesses the running app from the outside
by sending attack vectors to its endpoints.
(Read [here](../differences-between-sast-sca-dast/)
how together they make up a comprehensive approach to security testing.)

You've probably heard
that to achieve DevSecOps
you have to automate processes and security controls.
We're not here to contradict that.
It's evidently important to have processes be consistent and iterative.
What we endorse is that you avoid leaving it all to automation.
Tools show false positive and false negative rates.
Their results must therefore be reviewed manually,
and ethical hackers should be added to the security testing strategy
to complete the search for vulnerabilities and issues.

The combination of automation and manual work is absolutely necessary.
Our [2022 State of Attacks](https://try.fluidattacks.tech/state-of-attacks-2022/)
shows
that **the totality** of critical severity vulnerabilities
in the systems of our clients
were detected by our ethical hackers only.
One such vulnerability was
having AWS credentials stored in plain text within the source code.
This issue ranked second
among those that expose organizations the most to risks.

Fortunately,
the AWS CAF backs us up.
It encourages deploying manual methods that simulate "real-world" cyberattacks
as a best practice related to the vulnerability management capability.
Namely,
pen testing and red teaming,
two methodologies we excel at.

**Penetration testing** refers to simulations of genuine attacks,
which often involves creating custom exploits to bypass defenses.
But the role of ethical hackers (or pentesters) in this approach
is not limited to functional testing,
since they can also perform manual SAST and SCA.
(Notice
that we always refer in this blog post to "manual" penetration testing.
Elsewhere,
we explain why we think "manual" is the only kind of pentesting.)

The following are the main benefits of our [Penetration Testing solution](../../solutions/penetration-testing/):

- The hackers' expert knowledge
  allows for a much more detailed understanding of vulnerabilities.

- The combination of automation and manual security testing allows us
  to guarantee the detection of critical severity vulnerabilities
  with very low rates of false positives and false negatives.

- It can be done continuously
  as the cloud-native software evolves,
  in what is known as
  the [penetration testing as a service](../what-is-ptaas/) (PTaaS) model,
  so you have up-to-date knowledge on your security status.

- We break the build
  to ensure
  that no vulnerable build that violates your organization's policies
  goes into production.

- Once you have remediated a vulnerability,
  you can ask our hackers to verify
  that it really was,
  as many times as it takes you to solve it,
  without extra charge.

**Red teaming** also refers to simulations of real-world attacks,
but it's got some differences compared to pentesting.
First is red teaming's holistic approach,
as it sets out to test an organization's security
at the technological and human level
(e.g., ethical hackers may use [social engineering](../social-engineering/)
techniques)
to find out the effectiveness of its attack prevention,
detection and response strategies.
Which begs for an explanation
that also refers to a second difference between red teaming and pentesting.
Namely,
in the former,
most people on the incident response team and employees don't know
that the attacks are performed
with the consent of the organization's executive leadership.
Finally,
we would like to mention
that red teaming may have specific objectives
instead of being focused on finding all the vulnerabilities.

In addition to those of our Penetration Testing solution,
the following are the main benefits of our [Red Teaming solution](../../solutions/red-teaming/):

- Highly realistic attack simulations
  that follow the tactics, techniques
  and procedures of malicious threat actors.

- Ethical hackers
  with advanced [certifications](../../about-us/certifications/) (OSEE,
  CRTO, CRTE and CARTP)
  give you a broad view of your organization's security.

What's more,
in line with AWS DevOps security best practices
and one under the operations perspective of the CAF,
we present all the findings aggregated in a single pane of glass:
our [Attack Resistance Management platform](../../product-overview/)
(ARM).
There you get detailed, updated reports,
find out the risk associated with each detected vulnerability,
assign members of your team responsible for remediation,
get in touch with our hackers,
among many other things.

Now that you're ready to begin AWS [DevSecOps](../../solutions/devsecops/)
with `Fluid Attacks`,
[contact us](../../contact-us-demo/).

If you're still on the fence
and want to try our automated security testing first,
start your [21-day free trial](../../free-trial/).
You can upgrade anytime to add manual security testing.
