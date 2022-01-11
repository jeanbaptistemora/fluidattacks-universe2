---
slug: azure-source-code-exposure/
title: Your Source Code Out in the Wild
date: 2022-01-07
subtitle: What was Azure's four-year-old vulnerability?
category: attacks
tags: cybersecurity, cloud, flaw, git, code, web
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1641563215/blog/azure-source-code-exposure/cover_azure.webp
alt: Photo by Vincent van Zalinge on Unsplash
description: A recently discovered four-year-old vulnerability in Microsoft's Azure App Service has been keeping the source codes of customer applications public.
keywords: Notlegit, Azure, Source Code, Local Git, Bug, Cloud, Wiz, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/KEvB5mNmzwA
---

Imagine you just learned from a vulnerability report
that your application's source code has been kept public since its deployment.
There's more:
Imagine it's been like this for a couple of years now
and anyone anywhere could download files that are not intended to be public,
such as authentication information.
Is your heart racing now?

Problems like that arise when teams leave exposed [`.git` directories](https://gaurav5430.medium.com/web-security-exposed-git-folder-in-production-51ad9484dee0).
About a year ago,
an ethical hacking and security research team [gained access](https://www.bleepingcomputer.com/news/security/united-nations-data-breach-exposed-over-100k-unep-staff-records/)
to over 100,000 private records of United Nations Environment Programme (UNEP)
employees.
The contents that were publicly accessible included files
exposing the administrator's database credentials,
which granted access to UNEP's source code,
as well as databases exposing project funding source records,
UN staff demographic data
and travel history.
Plenty of other information was there for the prying eyes.
It was suggested back then that "threat actors likely already have the data."

In this post,
we will talk about a recently discovered four-year-old vulnerability
that also involved compromised `.git` directories.

## The NotLegit vulnerability

On September 12 last year,
researchers at cloud security firm Wiz [found](https://blog.wiz.io/azure-app-service-source-code-leak/)
a security issue at [Microsoft Azure App Service](https://azure.microsoft.com/en-us/services/app-service/#overview).
The latter is a cloud computing-based platform for creating
and deploying web and mobile applications for any device.
One very worrying thing is that,
according to the researchers,
the vulnerability has existed since September 2017.
Just like with the security issue that enabled access to UNEP's databases,
the researchers say
Azure's misconfiguration has probably been exploited in the wild for a while.

Users can deploy source code and artifacts to Azure in multiple ways.
For example,
they may pull their source code from a Git-based repository hosting service
(e.g., GitHub, Bitbucket).
An alternative is using "Local Git."
This method lets users create a local Git repository
within the Azure App Service container
that lets them push their code to the server.
Following deployment,
anyone can access the application on the internet
under the `.azurewebsites.net` domain.

The recently discovered security problem [affected](https://msrc-blog.microsoft.com/2021/12/22/azure-app-service-linux-source-repository-exposure/)
applications deployed using Local Git.
More specifically,
those written in PHP, Node, Python, Java or Ruby,
which are not served
in Microsoft's very own Internet Information Services (IIS) server.
As [described](https://blog.wiz.io/azure-app-service-source-code-leak/)
by the researchers,
the Local Git method created the Git repository
within a publicly accessible directory,
namely,
`/home/site/wwwroot.`
This vulnerability,
which researchers named **NotLegit** (don't ask us why\!),
reportedly,
left hundreds of source code repositories exposed for anyone to see.

## Time for the long-overdue fixes

As [reported](https://blog.wiz.io/azure-app-service-source-code-leak/),
Microsoft was aware of Local Git's behavior
and had mitigated the risk of unauthorized access
by adding a `web.config` file that placed restrictions.
This file can only be handled by the ISS server, though.
So,
applications written in C# or ASP.NET were protected
because they are deployed with this server.
However,
applications written in other languages are deployed with other servers
like Nginx or Apache.
These servers do not support `web.config` files.
As there were no restrictions in place,
anyone could access the source code and other sensitive information.

The researchers at Wiz reported the issue to Microsoft on October 7.
The Microsoft Security Response Center (MSRC) [explained](https://msrc-blog.microsoft.com/2021/12/22/azure-app-service-linux-source-repository-exposure/)
in a very recent post what caused the vulnerability.
What happened is the applications served the `.git` folder as static content
that goes into the public content root folder.
Static content [is](https://stackoverflow.com/a/37320839)
all the data that doesn't have to be generated for each and every request
and thus is served the same to every end-user.
Microsoft fixed the problem for PHP applications on November 17.
The fix disallows serving the `.git` folder as static content.

Fixes for applications written in Node, Python, Java or Ruby
require manual work from customers, though.
It's the application code that controls the serving of static content.
So,
customers themselves need to look at the code
and make sure the `.git` folder is not served within the public folder.

On December 7,
Microsoft started sending emails notifying all vulnerable customers
and advising them to take specific actions to protect their applications.
It turns out,
customers using Local Git from the start were not the only ones affected.
Customers whose applications were deployed using other methods
but had got files created or modified in the Azure App Service container
[were also impacted](https://msrc-blog.microsoft.com/2021/12/22/azure-app-service-linux-source-repository-exposure/).

## Do you know where your source code sits now?

As we hinted at the start of this post,
teams may mistakenly publish the `.git` folder to the internet.
Of course,
NotLegit was not enabled by admin error.
Rather,
it was the cloud service provider
that mistakenly exposed the customers' `.git` folders.
[It's been said](https://malware.guide/article/notlegit-vulnerability-azure-app-service-makes-source-code-public/)
experts are urging users to check if their source code has been leaked.
This should not be regarded as a serious matter by Azure's customers only.
All teams should know if they are exposing things they want to keep private,
so they need to ensure security is an [integral part](../devsecops-concept/)
of development.

We have stated [elsewhere](../oss-security/),
however,
that **a hidden source code isn't necessarily a secure one**.
Indeed,
the bigger issue isn't exactly that anyone can review your code,
but rather
that if your exposed code has any vulnerability,
you're just moments away from being attacked.

At `Fluid Attacks`,
we perform comprehensive testing
in search of vulnerabilities during the entire software development lifecycle.
By using our services,
you can find out,
among many other things,
whether you are inadvertently exposing your `.git` folder and,
in doing so,
possibly compromising sensitive data.
But most importantly,
you can find out just **how secure your code is**
at each point in development.
So,
if it's actually supposed to be out there,
you'll know it's fine.
Take this step now and
[contact us](../../contact-us/)\!
