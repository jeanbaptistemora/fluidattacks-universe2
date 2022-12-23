---
id: export
title: Export
sidebar_label: Export
slug: /machine/web/export
---

To download all of your organization's
vulnerabilities (including all
vulnerability statuses) in a .CSV file,
you can go to the Analytics section
and click on the Vulnerabilities button.

![Analytics Section](https://res.cloudinary.com/fluid-attacks/image/upload/v1671814148/docs/web/download_button_vuln.png)

When you click on it,
you will be asked for a verification
code that will be sent to you via SMS.
If you have not yet registered
your phone number to ARM,
we invite you to enter
[here](/machine/web/user) and register.

![Verification Code](https://res.cloudinary.com/fluid-attacks/image/upload/v1663089476/docs/web/vuln_download_verification_code.png)

When you enter the verification code,
you will download a compressed
file where you will find the
file with a .CSV extension.
When you open it,
you will be able to see all the
vulnerabilities of the organization.
You can also get this information
via API with the `vulnerabilitiesUrl` method.
To know how to make the API
request to our ARM,
we invite you to click
[here](/machine/api).
