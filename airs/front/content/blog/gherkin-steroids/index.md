---
slug: gherkin-steroids/
title: Gherkin on Steroids
date: 2018-03-13
subtitle: How to document detailed attack vectors
category: documentation
tags: documentation, vector, software
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330882/blog/gherkin-steroids/cover_iwilpg.webp
alt: Cucumber lot
description: In this post, we work on how to use Gherkin to document
  attack vectors in vulnerable applications, employing more advanced
  keywords from the Gherkin syntax.
keywords: Gherkin, Attack Vector, Documentation, Report, Vulnerability, Inclusion,
  Ethical Hacking, Pentesting
author: Rafael Ballestas
writer: raballestasr
name: Rafael Ballestas
about1: Mathematician
about2: with an itch for CS
source: https://unsplash.com/photos/Ky6x9T8j128
---

In the field of information security, 'finding all vulnerabilities' is
as important as 'reporting them as soon as possible'. For that, we need
an effective means to communicate with all stakeholders. We have
proposed [before](../app-pickle/) using `Gherkin`. In that entry, we
showed how to use \`Gherkin’s syntax in order to document attack
vectors, i.e., how to find and exploit vulnerabilities in an app. We
also showed the basics of the language, so if you haven’t done so
already, we recommend you to take a look a it.

## More keywords

Sometimes you need to specify a larger piece of text than fits in a
[decent-length
line.](https://en.wikipedia.org/wiki/Characters_per_line#In_programming)
For that, `Gherkin`, has `docstrings` (`"""`):

**Specifying long input.**

``` gherkin
When I inject the following SQL query in the input field:
  """
  INSERT INTO mysql.user (user, host, password)
         VALUES ('name', 'localhost', PASSWORD('pass123'))
  """
Then I have granted myself access to the database
```

You may write anything between the `docstrings`, but they must be in
their own lines and the indentation is relative to them. They are
particularly useful for citing code, output from `CLI` programs and
unstructured plain text.

For 'structured' plain text, `Gherkin` has the `Data Table` syntax
element, (don’t confuse with tables from Scenario Outlines):

**Tabular data with tables.**

``` gherkin
Given the database is populated with the species:
| Common Name    | Genus         | Species  | Family         |
| Lion           | Panthera      | Leo      | Felidae        |
| GNU            | Connochaetes  | Gnou     | Bovidae        |
| Gentoo Penguin | Pygoscelis    | Papua    | Spheniscidae   |
| Burr gherkin   | Cucumis       | Anguria  | Cucurbitaceae  |
```

You don’t have to align the pipes (`|`) as above, but it makes your
`.feature` file look nicer. `Gherkin` doesn’t care about that, only that
the number of columns match.

Speaking of Scenario Outlines, as seen in our previous entry, these are
very useful to specify many cause-effect relations:

``` gherkin
When I do <action>
Then I get a <result>

Examples:
  |    <action>     |      <result>      |
  | Drink coffee    | Be more alert      |
  | Take a cab      | Get there faster   |
  | Open the window | Ventilate the room |
```

## Detailed attack vectors

Let us put these to practice by documenting a vulnerability in detail
from our good old friend [bWAPP](http://itsecgames.blogspot.com.co/),
which simply gives us a cryptic message:

<div class="imgblock">

!["Page with mysterious message"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330881/blog/gherkin-steroids/default-file_eg7655.webp)

<div class="title">

Figure 1. A mysterious message

</div>

</div>

No matter how dumb it might seem, this is the first thing we need to
document: how the page, app or whatever we’re testing works at the
moment we tested it. We might use a separate "Normal use case" scenario
as we did before.

### Background

Or we can just plug that behavior right into the `Background`. This must
also include, in detail, everything needed to run the app. Our target
`bWAPP` is a `PHP` web server; Maybe you’re running it inside a
[`bee-box`](http://itsecgames.blogspot.com.co/2013/07/bee-box-hack-and-deface-bwapp.html)
virtual machine? Or did you set up the
[`LAMP`](https://en.wikipedia.org/wiki/LAMP_%28software_bundle%29)
server yourself? On what operating system? All of this must be in the
background, in order to allow reproducibility.

I, for one, am running `bWAPP` inside a
[`Docker`](https://www.docker.com/) container made by
[`raesene`](https://hub.docker.com/r/raesene/bwapp/), so let there be a
record of that in our attack feature:

``` gherkin
  Background:
    Given I am running Manjaro GNU/Linux kernel 4.9.86
    And I am running bWAPP 2.2 in Docker container raesene/bwapp:
    """
    ubuntu 14.04 LTS, kernel=host(4.9), MySQL 5.5, Apache 2.4.7, PHP 5.5
    """
    Given a PHP site showing a message:
    """
    URL: bwapp/directory_traversal1.php?page=message.txt
    Message: Try to climb higher Spidy...
    Evidence: default-file.png
    """
```

All programs and versions are explicitly listed, plus the `URL` and
field where the vulnerability was found. Note how we can refere to
external evidence files, too.

### Dynamic detection and exploitation

Now, the cryptic message in the page might be trying to tell us
something. Where can we climb? As it turns out, anywhere. The next hint
is in the `URL`. The page takes a `GET` parameter `page=message.txt`. So
the file `message.txt` is a simple text file that contains the words
above, and what the page does is display it. What if we change it to
another text file? Let’s try `/commandi.php`.

<div class="imgblock">

!["Screenshot of abused page"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330882/blog/gherkin-steroids/source_tib0qk.webp)

<div class="title">

Figure 2. Abusing the website

</div>

</div>

Notice two things here: first, the `PHP` code and text commentaries are
shown. Hence we could theoretically access the `PHP` source of any page
in this server. Second, the `HTML` part is actually rendered in the
browser, which could lead to a [`XSS`](../xss-protection/) or
[`CSRF`](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_\(CSRF\))
attack.

But wait. The server is not just `` `floating'' in space:
it lives inside a `GNU/Linux `` machine. And 'everything' in such an
`OS` is a file, many of which are plain-text files. One of them is of
particular importance:
[`/etc/passwd`](https://www.cyberciti.biz/faq/understanding-etcpasswd-file-format/),
which stores information about users. Let us try to display it in this
page, setting `page=/etc/passwd`:

<div class="imgblock">

!["Viewing the contents of a system file in the page"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330881/blog/gherkin-steroids/passwd_r3cgvo.webp)

<div class="title">

Figure 3. Listing users in the `bWAPP` servers

</div>

</div>

We can document that using `Gherkin` data tables, in a scenario of its
own, due to the importance of the finding:

**Documenting a particular exploitation.**

``` gherkin
  Scenario: Users record extraction
    When I change the page=message.txt parameter to page=/etc/passwd
    Then we retrieve the following user records:

    # Records extracted
    | username | pw? | UID | GID | info | home | shell |
    | root     | x | 0 | 0 | root | /root | /bin/bash |
    | daemon   | x | 1 | 1 | daemon | /usr/sbin | /usr/sbin/nologin |
    | bin      | x | 2 | 2 | bin | /bin | /usr/sbin/nologin |
    | sys      | x | 3 | 3 | sys | /dev | /usr/sbin/nologin |
    | sync     | x | 4 | 65534 | sync | /bin | /bin/sync |
    | games    | x | 5 | 60 | games | /usr/games | /usr/sbin/nologin |
    | man      | x | 6 | 12 | man | /var/cache/man | /usr/sbin/nologin |
    | lp       | x | 7 | 7 | lp | /var/spool/lpd | /usr/sbin/nologin |
    | mail     | x | 8 | 8 | mail | /var/mail | /usr/sbin/nologin |
    | news     | x | 9 | 9 | news | /var/spool/news | /usr/sbin/nologin |
    | uucp     | x | 10 | 10 | uucp | /var/spool/uucp | /usr/sbin/nologin |
    | proxy    | x | 13 | 13 | proxy | /bin | /usr/sbin/nologin |
    | www-data | x | 33 | 33 | www-data | /var/www | /usr/sbin/nologin |
    | backup   | x | 34 | 34 | backup | /var/backups | /usr/sbin/nologin |
    | list     | x | 38 | 38 | Mailing List Manager | /var/list | /usr/sbin/nologin |
    | irc      | x | 39 | 39 | ircd | /var/run/ircd | /usr/sbin/nologin |
    | gnats    | x | 41 | 41 | Gnats Bug-Reporting System (admin) | /var/lib/gnats | /usr/sbin/nologin |
```

Now we know how many users there are on the server, and which of them
have passwords set. Those are stored in
[`/etc/shadow`](https://www.cyberciti.biz/faq/understanding-etcshadow-file/)
in the form of hashes, which can be [cracked if the passwords are
weak](../storing-password-safely/). However, the `shadow` file, unlike
the `passwd` file, is protected:

<div class="imgblock">

!["foo bar"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330881/blog/gherkin-steroids/protected_rphxjb.webp)

<div class="title">

Figure 4. A failure

</div>

</div>

'Drat\!' Well, we’ll find a way around it, sooner or later. Now that we
got the hang of it we can try other files. Since we always do the same:
change `page=message.txt` to `page=desired-file.txt` we can use a
Scenario Outline for that, using one column for what we give as input,
and the other for the result:

**Documenting many cases in one Outline.**

``` gherkin
  Scenario Outline: Dynamic detection and exploitation
    Given the message and the page=message.txt GET parameter in the URL
    When I change the GET parameter page=message.txt to another page=<path>
    Then I see the file <printed> in the page, if it is a text file:

    Examples:
      |        <path>        |             <printed>             | <evidence>    |
      | /etc/passwd      | User accounts info          | passwd.png    |
      | /etc/group       | User groups info                |               |
      | /etc/shadow      | Couldn't open       | protected.png |
      | /etc/hosts       | Hosts file        |     |
      | commandi.php         | PHP source code and rendered HTML | source.png  |
      | passwords/heroes.xml | Heroes' passwords and secrets     |     |
      | admin/settings.php   | No output, but file exists        |     |
```

It is only natural to make several tries, some of which fail, some of
which succeed. All of them should be reported in the most scientific
spirit.

### Static detection and possible fixes

Let us see why `passwd` could be read and `shadow` couldn’t. From
'inside' the server let us say

``` text
ls -l /etc/{passwd,shadow}
-rw-r--r-- 1 root root   1012 Feb 15  2016 /etc/passwd
-rw-r----- 1 root shadow  559 Feb 15  2016 /etc/shadow
```

Notice that `passwd` has three ``r’s:
one for the owner (the user `root``), one for the the owner’s group
(again, just `root`) and the final one is for everyone else. However
`shadow` doesn’t have that last `r`, so it can only be read by `root`.

While we’re at static detection of problems, let us see what is wrong
with that page so we can try to fix it. The source code for the page
simply takes the `GET` parameter `page`, and displays it.

**Adapted from bWAPP code. Some lines and brackets omitted for
clarity.**

``` php
$file = $_GET["page"];
show_file($file);
function show_file($file)
   if(is_file($file))
     $fp = fopen($file, "r") or die("Couldn't open $file.");
     while(!feof($fp))
       $line = fgets($fp,1024);
       echo($line);
       echo "<br />";
```

We can include this exact snippet, numbers and all, between
`docstrings`, while discussing code exploration in our feature file.

Now the main problem with this is that we can pass, as seen before, any
file as a `GET` parameter and it will be shown, i.e., that input should
have been validated and cleaned before `show_file`.

To fix that, a good first step would be to clean strings like `..`, `./`
and `../`, which is what you would generally use to \`\`climb higher
Spidy'':

``` php
if(strpos($data, "../") !== false || strpos($data, "..\\") !== false ||
   strpos($data, "/..") !== false || strpos($data, "\..") !== false ||
   strpos($data, ".") !== false)
        $directory_traversal_error = "Directory Traversal detected!";
```

This would block attackers who do not know the file system hierarchy in
the server, but still allows us to give absolute paths as the parameter.
An even better defense would be that the user should not be allowed to
display files outside the current folder:

``` php
// Gives the current directory path
$real_base_path = realpath("");
// Gives the absolute path equal to user input
$real_user_path = realpath($user_path);
if(strpos($real_user_path, $real_base_path) === false)
  $directory_traversal_error = ""Directory Traversal detected!";
```

But this still allows us to display the file with the heroes' passwords.
In fact, it would be better just not to allow users to display files at
their will.

### More details

So far, we’ve documented in `Gherkin`:

1. the background where we’re running the vulnerable app,

2. the dynamic detection and exploitation phase, with several examples
    and evidences,

3. the important records we were able to extract from the app,

4. the static detection part, with specific bad code snippets, issues
    and suggestions.

To finish a proper `.feature` file, we’re missing, well, the feature
itself, which is the vulnerability, or rather, the finding and
exploitation thereof.

Remember that we can document features and scenarios using
'descriptions'. After the keywords `Feature`, `Scenario`, `Scenario
Outline` or `Example` we can write anything we like, as long as no line
starts with a keyword (including comments - you can’t mix descriptions
with comments, I learned that the hard way).

It is usual to describe features with the format As \<type of user\> I
want to \<do something\> In order to \<get some result\>. We can take
advantage of such a structure to document the 'Scenario' and 'Actor' of
the vulnerability, the 'Threat' and what records can be 'compromised'.
We can also use that space to document anything else we consider to be
globally important:

``` gherkin
Feature: Vulnerability FIN.S.0075 Local file inclusion
  From the bWAPP application
  From the A7 - Missing functional level access controls category
  In URL bwapp/directory_traversal_1.php
  As any user from Internet with access to bWAPP
  I want to be able to see local files I'm not supposed to
  In order to gain access to system objects with sensitive content
  Due to missing functional level access controls
  Recommendation: restrict access to sensitive files (REQ.0176)
```

For anything else, use comments. I will include details such as the
vulnerability code, [`CWE`](https://cwe.mitre.org/),
[`CVE`](https://nvd.nist.gov/) if present, computed metrics such as
[`CVSS`](https://nvd.nist.gov/vuln-metrics/cvss) scores, etc in comments
(`#`) at the beginning of the file. See the [full feature](#apx-feature)
below.

---
And that is how we propose using this language to document attacks. You
may ask: why `Gherkin` and not just plain text? Because it is
[line-oriented](https://en.wikipedia.org/wiki/Line-oriented_programming_language)
and has a light structure, we can define a template like the one
discussed here, and we can enforce following of the format using the
readily available
[parsers](https://github.com/cucumber/cucumber/tree/master/gherkin),
[linters](https://github.com/vsiakka/gherkin-lint) and
[compilers](https://github.com/cucumber/cucumber/) for the language. We
still need to work further on the template definition, so stay tuned.

## Appendix: full feature

local-file-inclusion.feature [here](./local-file-inclusion.feature)
