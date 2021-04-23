---
id: strict_transport_security
title: Strict Transport Security
sidebar_label: Strict Transport Security
slug: /types/043/details/strict_transport_security
---

The HTTP `Strict-Transport-Security` response header informs the browser that
it should never load a site using HTTP and should automatically convert all
attempts to access the site using HTTP to HTTPS requests instead.

## Exploitation scenario

You log into a free WiFi access point at an airport and start surfing the web,
visiting your online banking service to check your balance and pay a couple of bills.
Unfortunately, the access point you're using is actually a hacker's laptop,
and they're intercepting your original HTTP request and redirecting you to a
clone of your bank's site instead of the real thing.
Now your private data is exposed to the hacker.

`Strict Transport Security` resolves this problem;
as long as you've accessed your bank's web site once using HTTPS,
and the bank's web site uses `Strict Transport Security`,
your browser will know to automatically use only HTTPS,
preventing hackers from performing this sort of man-in-the-middle attack.

## Words of caution

It's important to note that in order for the `Strict Transport Security`
response header to work your users **must** have accessed your website through
HTTPS **at least once**.

Configuring this header in all responses (including error pages) increases
the effectiveness of the `Strict Transport Security` by increasing the
probability that your users had visited the website through HTTPS at least once.
Once this condition is met, the browser will remember (during `max-age` seconds) that your site must only be accessed through HTTPS.

Using a large value for `max-age` also increases the effectiveness of the
header.

# Secure implementation

Set `Strict-Transport-Security: max-age=31536000` HTTP header in all
responses from your site, including error pages, HTTP and HTTPS.
