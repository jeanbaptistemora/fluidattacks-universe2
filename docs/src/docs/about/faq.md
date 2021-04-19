---
id: faq
title: Frequently Asked Questions
sidebar_label: Frequently Asked Questions
slug: /about
---

### 1. What is Continuous Hacking?
Continuous Hacking is a security testing service
that allows the hacking process to begin at an early stage
in the software development cycle.
Its purpose is to guarantee `100%` testing coverage of the application.


### 2. What are the benefits of Continuous Hacking?
Continuous Hacking:
1. Minimizes the cost of remediation (repair) of a vulnerable security risk
while the software is in development rather than when it is in production.

1. Reduces application certification time to zero
because the hacking is done during development.

1. Provides clear and detailed information about vulnerable security risks
and facilitates a coordinated effort between external project personnel
(`Fluid Attacks` experts) identifying security risks,
and internal project personnel (client company)
fixing security issues without delays.

### 3. In what industries does Fluid Attacks have experience?
Along our career trajectory we have been working with companies
from different sectors, such as financial, transportation,
industrial, consumer, communications, technology and utilities.

### 4. How does Fluid Attacks stay on top of new techniques and changes?
We ensure to constantly research and keep updated
with the new techniques and changes related to cybersecurity and `IT`.
Through [blog entries](https://fluidattacks.com/blog)
we keep our team updated with the state of art.

### 5. What are the necessary inputs and requirements for Continuous Hacking?
The necessary inputs and requirements are:

1. **Phase 1:** Access to the integration branch of the repository
for the not-yet-deployed application’s source code.
Ethical Hacking focuses on the source code.

1. **Phase 2:** When the project has a deployed application
(Integration Environment), the hacking coverage expands
to include application security testing.

1. **Phase 3:** This phase applies only if the infrastructure
supporting the application is defined as code and kept
in the integration branch of the repository referred to in Phase 1.
This phase includes infrastructure hacking.

### 6. What are the technical conditions that I must meet for Continuous Hacking?

Access to `Git` and a monitored environment in the branch are required,
through automated Linux.
The following environments are not supported:

1. Access through a `VPN` that only runs on `Windows`.
1. `VPN` in `Windows` that requires manual interaction such as an `OTP` token.
1. `VPN` Site to Site.

### 7. What type of hacking is included in Continuous Hacking?
Continuous Hacking includes source code analysis,
application hacking (see question 5),
and infrastructure hacking (see question 5).

### 8. What is a vulnerability?
A vulnerability is anything that represents a security risk
(Integrity, Availability, Confidentiality, Non-repudiation)
to the application.

### 9. What is an active author and how can I identify it?
An active author is a user with access to the `Git` repository
who makes changes to the stored code in the repository during
the analyzed month.

### 10. Does Continuous Hacking use a series of automated tools or is it the result of a manual (by hand) process?
Automated tools, by themselves,
are not capable of extracting sensitive business information,
such as client or employee information.
In our Continuous Hacking service, we use a series of tools
which are acquired and developed by us at `Fluid Attacks`,
as well as a detailed review process performed by our expert technical staff.
We go the extra mile because automated tools present the following problems:

1. Vulnerability leakages (detection of a minimal percentage
of existing security risk vulnerabilities).

1. Detected vulnerabilities are primarily false positives.

1. Incapability of combining individual vulnerabilities
in order to reveal additional vulnerabilities
which may be an even greater security risk
than the individual vulnerabilities alone.

### 11. If Continuous Hacking includes a manual review, how does Fluid Attacks ensure that development cycles are not slowed down?
Continuous Hacking is first performed on the source code.
This allows for hacking and development to occur simultaneously,
which in turn minimizes the dependency on functional environments,
as well as the need for coordination between hackers and developers.
The decisions regarding which findings are prioritized for each sprint
rest solely with the client.
Unless we are dealing with a company with daily `CI/CD`
(Continuous Integration/Continuous Deployment),
not all sprints generate code eligible for release and deployment,
which improves the remediation (repair) time for detected vulnerabilities.

### 12. If Continuous Hacking is done manually, how can a big project move rapidly and expand as more active authors (developers) join the team?
Standard Continuous Hacking
covers `95%` of all business applications being developed,
as the subscription is based on the number
of active developers in the project and this defines the amount of resources
assigned to the project.

### 13. If Continuous Hacking is done manually, how does it move rapidly when a client has a big application portfolio that is constantly increasing?
Based on our historical data,
and thanks to our recruitment and training capabilities,
as well as our ability to innovate internal processes,
we are fully capable of taking on
between `5` and `10` new applications each month.

### 14. What kind of information does Fluid Attacks need in order to provide a quotation?

To provide a proposal, we need to determine
what the target of evaluation (scope) will be.
So, we require the following information:

1. *One-shot hacking* (by project):

  a. How many ports are included in the scope?

  b. How many inputs of applications are included in the scope?

  c. How many `LoC` are included in the scope? We recommend running
  [`CLOC`](https://github.com/AlDanial/cloc) in order to facilitate quantification.

**Note:** It would be desirable to obtain the access credentials
(standard user, not privileges) to the applications
in cases where this will be included.

2. **Continuous hacking** (`SDLC`):
Under this model, we need to know how many active authors
will be involved in the project.

Regarding the health check estimation,
the same considerations apply as for one-shot hacking,
so the client should provide the above-mentioned information as well.

### 15. Does the cost of Continuous Hacking vary according to the scope or development phases?
Yes. The service cost varies depending on the number of active authors
identified in the project each month.

### 16. Why is it necessary for Continuous Hacking to have access to the source code stored in the repository?
Continuous Hacking needs access to the source code
because it is based on continuous attacks
on the latest version available.

### 17. When does Continuous Hacking begin?
Continuous Hacking begins immediately after receiving the purchase order.

### 18. Why is there a month 0 and how does setup work?

Month `0` begins the test setup and is the start of the monthly payment.
A project leader is assigned who is responsible
for managing the connection of environments, profiling, user creation,
allocation of privileges, and all the necessary inputs
to begin the review without setbacks.

### 19. Is it possible to hire On-the-Premises Continuous Hacking?
No. Due to the operational model that supports Continuous Hacking,
it can only be done remotely.

### 20. Is it possible to schedule follow-up meetings?
Yes. All applications covered by the contract for Continuous Hacking
are assigned to a specific project leader who is available
to attend all necessary meetings.
We simply require sufficient notice of an impending meeting
in order to schedule availability.
