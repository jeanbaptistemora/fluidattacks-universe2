---
id: synopsys
title: Fluid Attacks vs. Synopsys
sidebar_label: Synopsys
slug: /about/compare/synopsys
---

One of the most common questions about
Fluid Attacks’ Continuous Hacking is
how it compares to Synopsys.
The following comparison table allows
you to understand how both providers perform
on different attributes that may be essential
to meet your company’s cybersecurity needs.

|         **Criteria**         |                                                                                                                                               **Fluid Attacks  Squad**                                                                                                                                              |                                                                                                                            **Fluid Attacks Machine**                                                                                                                           |                                                                                                                                                                                                                                                                                                                              **Synopsys**                                                                                                                                                                                                                                                                                                                             |
|:----------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| **Precision**                | The severity of the vulnerabilities is  identified in 90% of the cases. ([The  accuracy](/about/sla/accuracy/) is calculated based on the false  positives, false negatives and the F-Score  model). The severity of vulnerabilities is  calculated using [CVSSF = 4^(CVSS-4).](/about/faq/#adjustment-by-severity) | Our SAST tool achieved the best possible  result against the OWASP Benchmark  ([read the post here](https://fluidattacks.com/blog/owasp-benchmark-fluid-attacks/)): A TPR (True Positive  Rate) of 100% and an FPR (False Positive  Rate) of 0%.                               | Coverity, Synopsys' SAST tool, obtained   an accuracy value of 63.3%, according to   [a study](https://www.researchgate.net/figure/Metrics-obtained-by-the-SAST-tools-comparison-Fig-3-shows-a-comparative-graphic-of-the_fig2_342597384) with its own benchmark. [Another   study](https://www.researchgate.net/publication/348739709_A_Critical_Comparison_on_Six_Static_Analysis_Tools_Detection_Agreement_and_Precision) attributes to it an accuracy of 37%.   They reduce false positives and negatives   with the help of their other products and   services                                                                                                  |
| **Techniques**               | SAST, DAST, SCA, [Reverse Engineering](https://fluidattacks.com/categories/re/), and [MPT](https://fluidattacks.com/categories/re/)                                                                                                                                                                                 | [SAST](https://fluidattacks.com/categories/sast/), [DAST](https://fluidattacks.com/categories/sast/), and [SCA](https://fluidattacks.com/categories/sca/)                                                                                                                      | [SAST](https://www.synopsys.com/software-integrity/security-testing/static-analysis-sast.html), [DAST](https://www.synopsys.com/software-integrity/application-security-testing-services.html), [SCA](https://www.synopsys.com/software-integrity/security-testing/software-composition-analysis.html), [IAST](https://www.synopsys.com/software-integrity/security-testing/interactive-application-security-testing.html), and [Fuzzing](https://www.synopsys.com/software-integrity/security-testing/fuzz-testing.html) (each  of these products is sold separately; they  also offer [MPT](https://www.synopsys.com/software-integrity/penetration-testing.html)). |
| **Compliance**               | [We validate the following standards:](https://docs.fluidattacks.com/criteria/compliance/)  OWASP, GDPR, NERC, NIST, PCI DSS,  HIPAA, ISO 27002, ISO 27001, CWE, CVE,  EPR, BSIMM9, COMMON CRITERIA,  CAPEC, ePrivacy Directive as well as  company-specific requirements.                                          | [We validate some of the requirements  included in the following standards:](https://docs.fluidattacks.com/criteria/compliance/) OWASP, GDPR, NERC, NIST, PCI DSS,  HIPAA, ISO 27001, ISO 27002, CWE, CVE,  EPR, BSIMM9, COMMON CRITERIA,  CAPEC, CIS, and ePrivacy Directive. | [They validate the following standards:](https://www.synopsys.com/software-integrity/solutions/compliance.html)  WP 29, GLBA, MDR, FD&C Act,  HITECH Act, HIPAA, CCPA, CPRA,  FISMA, GDPR, SOX Act, NIST SP,  CMMC, DISA-STIG, DO-178C, AUTOSAR, ISO 26262, MISRA, ISO/CD  24089, ISO/SAE 21434, NERC CIP, PCI  DSS, ANSI/CAN/UL, IEC 62304, UL  2900-2-1, ANSI/ISA/IEC, CWE top 25,  FIPS, ISACA-COBIT, ISO/IEC, OWASP,  among others.                                                                                                                                                                                                                               |
| **Fast and automatic**       | We complement our Machine Plan with   hours or days of manual search for the   most critical vulnerabilities.                                                                                                                                                                                                       | Our scans take minutes for deterministic   vulnerabilities.                                                                                                                                                                                                                    | Their tests can take minutes, [hours or   days](https://www.synopsys.com/blogs/software-security/myth-3-penetration-testing-solves-everything/) depending on the product or   service in operation as well as the   characteristics of the target.                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Support**                  | Our standard service includes consulting  and clarification by hackers (via our  [Attacks Resistance Manager](https://docs.fluidattacks.com/machine/web/arm)) so that users  understand vulnerabilities.                                                                                                            | No additional charge for [support.](/machine/web/support/live-chat)                                                                                                                                                                                                            | In addition to the Standard Support, they   offer Premium and Premium Plus Support   programs. The latter two programs   increase the levels of coverage and   provide access to internal subject matter   experts.                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **Break the build**          | We break the build                                                                                                                                                                                                                                                                                                  | [We break the build](https://fluidattacks.com/solutions/devsecops/)                                                                                                                                                                                                            | [They can break the build](https://www.synopsys.com/blogs/software-security/integrating-static-analysis-tools-with-build-servers-for-continuous-assurance/)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Method**                   | Hybrid (automated tools + AI + human   intelligence).                                                                                                                                                                                                                                                               | Automated tools                                                                                                                                                                                                                                                                | [Automated tools.](https://www.synopsys.com/software-integrity/security-testing.html) (Separately, they offer   [manual testing](https://www.synopsys.com/software-integrity/security-testing.html).)                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **Correlation of attacks**   | By combining vulnerabilities A and B, we   discover a new, higher impact   vulnerability C, which may compromise   more records.                                                                                                                                                                                    | _________                                                                                                                                                                                                                                                                      | They do not refer to this kind of [correlation.](https://news.synopsys.com/2021-06-08-Synopsys-Acquires-Code-Dx-to-Extend-Application-Security-Portfolio)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **Safe mode**                | We can operate in safe mode, avoiding   being detected by the Security   Operations Center (SOCs) or affecting   service availability in productive   environments.                                                                                                                                                 | _________                                                                                                                                                                                                                                                                      | _________                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **Type of evidence**         | Our evidence is delivered in (a) PDF   executive reports, (b) XLS/PDF technical   reports, (c) animated screenshots (GIFs)   of the attack, (d) code pieces, (e) attack   screenshots with explanatory annotations,   and (f) system’s security status illustrated   by graphics and metrics.                       | Our evidence is delivered in (a) PDF executive reports, (b) XLS/PDF technical reports, (c) code pieces, (d) attack screenshots with explanatory annotations, and (e) system’s security status illustrated by graphics and metrics.                                             | [Their evidence](https://sig-docs.synopsys.com/polaris/topics/c_rp_pol_reports.html) is delivered in (a)   PDF/CSV/HTML executive reports and   (b) customized reports                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **Exploitation**             | We can do exploitation as long as we   have (a) an available environment and   (b) the appropriate authorization                                                                                                                                                                                                    | _________                                                                                                                                                                                                                                                                      | They offer the [Managed Penetration   Testing](https://www.synopsys.com/software-integrity/penetration-testing.html) service and [can do exploitation](https://www.synopsys.com/software-integrity/resources/ebooks/penetration-testing-buyers-guide.html).                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Zero-day vulnerabilities** | Our hackers are skilled at finding   zero-day vulnerabilities.                                                                                                                                                                                                                                                      | _________                                                                                                                                                                                                                                                                      | They have security research teams (not   tools) that find and store [exclusive   vulnerabilities.](https://www.synopsys.com/software-integrity/security-testing/software-composition-analysis/knowledgebase.html)                                                                                                                                                                                                                                                                                                                                                                                                                                                     |