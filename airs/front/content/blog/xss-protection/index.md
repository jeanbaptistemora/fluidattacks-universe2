---
slug: xss-protection/
title: Dude, Where's My XSS Protection?
date: 2017-04-26
category: challenges
subtitle: 'Solving Halls of Valhalla Challenge: XSS4'
tags: xss, web, protect, challenge
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331241/blog/xss-protection/cover_hihzge.webp
alt: Computer with four padlocks, one unlocked
description: 'Web security nowadays is a matter of concern. In this article,
  we explain how to avoid one of the most common attacks: Cross Site Scripting (XSS).'
keywords: Security, Input, Cross Site Scripting, XSS, Web, Risks,
  Ethical Hacking, Pentesting
author: Juan Aguirre
writer: juanes
name: Juan Esteban Aguirre González
about1: Computer Engineer
about2: Netflix and hack.
source: https://unsplash.com/photos/kYlYwQze5vI
---

Web application security is a major concern nowadays. You have to make
sure your application is secure, especially if you have a lot of users.
There are many controls a developer can implement to attempt to make the
site safer. Or so they think. The fun of hacking is looking for a
different way to get things done. There are many reasons to why these
developers are mistaken, in this article we will be talking about a very
common XSS (Cross-Site Scripting) "solution" that all it really does is
make the game that much more interesting.

XSS is a technique or an attack used to exploit vulnerabilities in which
malicious scripts are injected or inserted into what is believed to be a
trusted web site. These attacks can occur when data enters a web
application through an untrusted source, most frequently a web request,
and that data is included in dynamic content that is sent to a web user
without being validated for malicious content. The malicious content
sent to the web browser is often `JavaScript`, but may also include
`HTML`, `Flash`, or any other type of code that the browser may execute.
`XSS` based attacks most commonly include transmitting private data,
like cookies or other session information, to the attacker, redirecting
the victim to web content controlled by the attacker, or performing
other malicious operations on the user’s machine under the guise of the
vulnerable site (OWASP, 2016).

To explain a specific XSS prevention method and one of the ways we can
bypass this control we will be looking at a really cool challenge from
our pals at [Halls of
Valhalla](http://halls-of-valhalla.org/beta/challenges).

## Halls of Valhalla Challenge: XSS4

Our task here is to perform an XSS injection with alert(1). The
JavaScript alert(1) method generates a pop up alert window with 1 as a
the alert message.

<div class="imgblock">

![challenge](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331240/blog/xss-protection/image1_wi65fl.webp)

<div class="title">

Figure 1. Challenge XSS4 on halls-of-valhalla.org

</div>

</div>

In this challenge we are presented with an input in which we can submit
a message with a title, very much like a forum. The key is that we are
also given the source code for the function that displays my message.
This function is written in PHP. First we need to go through the source
code and understand what it is doing. Once we have done this we can look
for possible vulnerabilities.

<div class="imgblock">

![message](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331240/blog/xss-protection/image2_yb1p3l.webp)

<div class="title">

Figure 2. Display message function source code

</div>

</div>

From the code we see a conditional check. The if statement checks the
return value of the method ISSET(param) which determines if the param is
set and is not NULL. Inside the conditional check we see three very
similar instructions followed by an echo. The three similar instructions
all take one of the input fields from the form, pass it through the
strip\_tags() method and assign the new value to a variable. The echo
message then echoes or prints on screen an `HTML` \<div\> tag. The tag
has some basic attributes and one of the attributes used is the title
variable with my input after strip\_tags. So the echo instruction
displays the message along side the user name.

If we try the basic injection, "\<script\>alert(1)\</script\>", we can
see that the strip\_tags() method removes everything starting at "\<"
and ending in "\>". The echoed message would then be "alert(1)" which is
useless without the correct script tags.

We said before that an XSS can occur when data enters a web application
through a web request, and that data is included in dynamic content that
is sent to a web user without being validated for malicious content.
That is pretty much exactly what we have here with one small exception.
Our input IS validated for malicious content, strip\_tags() is applied
to all my input strings. So if we can find a way to bypass that
validation, we can then exploit the XSS vulnerability.

OWASP provides very helpful and complete documentation on various
security topics. For attacks it provides great cheat sheets that can
guide you in the Ethical Hacking process. Here is [TheirOfficial
Homepage](https://www.owasp.org/index.php/Main_Page) for a look into the
many topics and resources `OWASP` offers.

After further research on filter evasion, we can find that the
strip\_tags() method has a common and well known vulnerability. Since
the method needs to identify the "\<" and "\>" symbols in order to know
what to delete, we need to inject our script without the use of these
symbols.

<div class="imgblock">

![xss](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331239/blog/xss-protection/image3_g9zfbw.webp)

<div class="title">

Figure 3. Can you say XSS

</div>

</div>

Note that in the echo message, one of the input strings, $title, is used
inside the actual `HTML` tag. This gives us a possible injection. We
know we can’t add any tags, but no one has said anything about adding
attributes. We can add an event as an attribute and in that event call
our JavaScript alert code. The best way to do this is through the
"onmouseover" event. This attribute sets of an event when the mouse
pointer is moved onto an element. So what we need to do is inject our
JavaScript alert as the event.

Note that the `HTML` tag puts single quotes " ' " before and after the
$title input. Hence we need to close the first " ' " in order to be able
to add an other attribute. We can’t forget about the closing single
quote, when adding the attribute we need to leave the quotes open in
order to use the single quote added by the `HTML` tag and therefore
maintain a valid syntax.

<div class="imgblock">

![event](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331239/blog/xss-protection/image4_b6eixl.webp)

<div class="title">

Figure 4. Event: onmouseover='alert(1)'

</div>

</div>

Know that we have successfully posted our message containing the
injection, all we need to do to test it out is trigger the onmouseover
event.

<div class="imgblock">

![xss-protection](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331239/blog/xss-protection/image5_kjglyq.webp)

<div class="title">

Figure 5. There goes your XSS protection

</div>

</div>

Once we place the mouse pointer over our message we can see we get the
alert 1 pop up.

There are many filters you can use to validate your website’s input and
reduce the chances of a successful XSS injection. If you only use one
filter there is a very high probability that an attacker will be able to
find a way around your control. There are many functions in different
programming languages which implement not only one but many different
filters to validate the user input. If you are passionate about
programming, you can easily do some basic research and find different
functions you can call in order to make one big and complete XSS filter.

## References

1. [OWASP. Cross-Site Scripting
    (XSS)](https://www.owasp.org/index.php/Cross-site_Scripting_\(XSS\)).

## Challenge Link

[Halls of Valhalla
XSS4](http://halls-of-valhalla.org/challenges/xss/xss4.php)
