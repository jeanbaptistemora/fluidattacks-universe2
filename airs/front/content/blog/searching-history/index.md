---
slug: searching-history/
title: Search the History
date: 2020-04-29
category: attacks
subtitle: Searching for credentials in a repository
tags: security, git, vulnerability, credential
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331090/blog/searching-history/cover_qkuncf.webp
alt: Photo by Mick Haupt on Unsplash
description: As everyone knows in our context, production credentials should
  be protected. In this post, we explain how to extract old credentials
  and how to protect them.
keywords: Git, Security, Vulnerability, Hacking, Repository, Credentials,
  Ethical Hacking, Pentesting
author: Jonathan Armas
writer: johna
name: Jonathan Armas
about1: Systems Engineer, OSCP - Security+
about2: '"Be formless, shapeless like water" Bruce Lee'
source: https://unsplash.com/photos/eQ2Z9ay9Wws
---

At the moment, every company that develops their own product is sure
that they are using some form of a `source control management tool`.
This is used to track modifications to a source code repository and also
helps developers by preventing loss of work due to conflict overwriting
and ensures that they are always working on the right version of the
source code.

The most common form of `version control systems` is a `centralized
version control`, where the repository is in one place, and it allows
access to multiple clients. Here [Git](https://git-scm.com/) is one of
the biggest ones; it is an open-source distributed `source code
management system` that allows you to create a copy of your repository
known as a `branch`. With this `branch`, you can work on your code
independently, and when you are ready with your changes, you can store
them as a `commit`, then `Git` compare your changes with the main
`branch` (this is called a `diff`) and finally you can `merge` them to
the master `branch`. It also allows you to reverse the changes and to
work in different versions of the same source code. Used by millions of
developers, it is the base of many platforms such as
[Github](https://github.com/), [Gitlab](https://gitlab.com/),
[Bitbucket](https://bitbucket.org/), among others.

As you know, storing clear text passwords in your machine, code, or
anywhere (yes, I mean the sticky notes too) is a huge hole in your
security.
[OWASP](https://owasp.org/www-community/vulnerabilities/Password_Plaintext_Storage)
and [CWE](https://cwe.mitre.org/data/definitions/256.html) mark this as
a vulnerability, but many developers make this mistake by creating
configuration files and uploading them to a repository.

Maybe you are thinking, "who in the world is going to do that?" But this
practice is more common than it appears. Recently (September 2019), it
was discovered that a big bank was storing highly sensitive data on a
publicly accessible repository on `Github`, maybe your company is doing
this right now.

## Git disclosure lab

To set up our lab, we are going to create an empty repository, here we
are going to create a database file with some credentials and commit the
change:

**db.sql.**

``` sql
use mysql;

CREATE USER 'coder'@'localhost' IDENTIFIED BY 'ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T';
GRANT ALL PRIVILEGES ON *.* TO 'coder'@'localhost';
FLUSH PRIVILEGES;

create database if not exists coder;
  use coder;
  create table if not exists admin(id int,username varchar(50),password varchar(50));
  insert into admin values(1,"administrator","q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo");
exit
```

**setting up the lab.**

``` bash
$ mkdir gitcredentials
$ cd gitcredentials
gitcredentials$ git init
gitcredentials$ nano db.sql #Add here the content
gitcredentials$ git add --all
gitcredentials$ git commit -m "Added file"
```

Now we have a repository with clear text credentials. What the
developers usually do to solve the problem? Let’s delete the credentials
and commit the change:

**db.sql modified.**

``` sql
use mysql;

CREATE USER 'coder'@'localhost' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON *.* TO 'coder'@'localhost';
FLUSH PRIVILEGES;

create database if not exists coder;
  use coder;
  create table if not exists admin(id int,username varchar(50),password varchar(50));
  insert into admin values(1,"administrator","");
exit
```

**deleting the credentials.**

``` bash
gitcredentials$ nano db.sql #Add here the content
gitcredentials$ git add --all
gitcredentials$ git commit -m "Delete credentials"
```

If this change goes to production, then there are no credentials in the
file but anyone with access to the repository could view those changes.
Also, it is common that the credentials do not change because it will
break some interconnected systems.

To get credentials from a git repository, we can use several tools such
as:

- [truffleHog](https://github.com/dxa4481/truffleHog)

- [gittyleaks](https://github.com/kootenpv/gittyleaks)

- [git-secrets](https://github.com/awslabs/git-secrets)

- [Repo-supervisor](https://github.com/auth0/repo-supervisor)

- [Git Hound](https://github.com/ezekg/git-hound)

In this example, we are going to use
[truffleHog](https://github.com/dxa4481/truffleHog) because it searches
for keys based on entropy. To install it, we simply need to use `PyPI`:

**installing truffleHog.**

``` bash
gitcredentials$ pip3 install trufflehog
gitcredentials$ trufflehog -h
usage: trufflehog [-h] [--json] [--regex] [--rules RULES]
                  [--entropy DO_ENTROPY] [--since_commit SINCE_COMMIT]
                  [--max_depth MAX_DEPTH] [--branch BRANCH]
                  [-i INCLUDE_PATHS_FILE] [-x EXCLUDE_PATHS_FILE]
                  [--repo_path REPO_PATH] [--cleanup]
                  git_url

Find secrets hidden in the depths of git.
...
```

We are ready to go.

## Getting the credentials

One way to simply get credentials from a repository is to run the
command `grep` with a keyword like username, password, key, admin, etc.:

**using grep.**

``` bash
gitcredentials$ grep -nr "password" .
./db.sql:9:  create table if not exists admin(id int,username varchar(50),password varchar(50));
gitcredentials$ grep -nr "admin" .
..db.sql:10:  insert into admin values(1,"administrator","");
```

As we see, it shows us the file, line, and content of that line of code,
if we have a big source code, this is useful to locate potential files
that could contain clear text credentials in them.

Next, we can search for the history of that file using `git`:

**history git.**

``` bash
gitcredentials$ git log -p db.sql
commit e36e9322c94e5a3f41f80505e56e370fa164b7a1 (HEAD -> master)
Author: root <root@fluidattacks.localdomain>
Date:   Wed Apr 29 10:50:17 2020 -0500

    Delete credentials

diff --git a/db.sql b/db.sql
index fa065ad..b6eaabb 100644
--- a/db.sql
+++ b/db.sql
@@ -1,11 +1,11 @@
 use mysql;

-CREATE USER 'coder'@'localhost' IDENTIFIED BY 'ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T';
+CREATE USER 'coder'@'localhost' IDENTIFIED BY '';
 GRANT ALL PRIVILEGES ON *.* TO 'coder'@'localhost';
 FLUSH PRIVILEGES;

 create database if not exists coder;
   use coder;
   create table if not exists admin(id int,username varchar(50),password varchar(50));
-  insert into admin values(1,"administrator","q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo");
+  insert into admin values(1,"administrator","");
 exit
```

There is a more efficient way to do this and is by using `truffleHog`,
this tool searches automatically through the entire repository and
prints the keys with high entropy:

**history git.**

``` bash
gitcredentials$ trufflehog .
~~~~~~~~~~~~~~~~~~~~~
Reason: High Entropy
Date: 2020-04-29 10:50:17
Hash: e36e9322c94e5a3f41f80505e56e370fa164b7a1
Filepath: db.sql
Branch: origin/master
Commit: Delete credentials

@@ -1,11 +1,11 @@
 use mysql;

-CREATE USER 'coder'@'localhost' IDENTIFIED BY '';
+CREATE USER 'coder'@'localhost' IDENTIFIED BY 'ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T';
 GRANT ALL PRIVILEGES ON *.* TO 'coder'@'localhost';
 FLUSH PRIVILEGES;

 create database if not exists coder;
   use coder;
   create table if not exists admin(id int,username varchar(50),password varchar(50));
-  insert into admin values(1,"administrator","");
+  insert into admin values(1,"administrator","q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo");
 exit
```

## Solution

As we have seen by now, if a developer puts sensitive data into a file
and commits the changes, an attacker could get our credentials by
searching the history of our source code, but what can we do about that?

First of all, we can avoid using credentials at all by using environment
variables and pipelines; every major source code management platform has
this feature within their services. Pipelines are the top-level
component of continuous integration, delivery, and deployment. With
this, we can test, build, and deploy our projects, and by setting our
credentials there into environment variables, we ensure the principle of
least privilege.

- [Variables in
  Bitbucket](https://confluence.atlassian.com/bitbucket/variables-in-pipelines-794502608.html)

- [Variables in Gitlab](https://docs.gitlab.com/ee/ci/variables/)

- [Variables in
  Github](https://help.github.com/en/actions/configuring-and-managing-workflows/using-environment-variables)

Another thing we can do is to delete them from the repository using
tools like [BFG
Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/). This searches
through the commit history and removes sensitive data. Using our
example, we can put our credentials into a file:

**passwords.txt.**

``` txt
q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo
ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T
```

Then run the `BFG Repo-Cleaner` in our repository:

**running BFG.**

``` bash
gitcredentials$ nano passwords.txt #Add here the content
gitcredentials$ java -jar bfg-1.13.0.jar  --replace-text passwords.txt .
...
Cleaning

Found 2 commits
Cleaning commits:       100% (2/2)
Cleaning commits completed in 118 ms.

Updating 1 Ref

        Ref                 Before     After
        refs/heads/master | e36e9322 | 38604def
...
Changed files

        Filename   Before & After
        db.sql   | fa065ad9 ? 489ca3e7
...
```

Now if we check the history of our file, we will see that the
credentials are removed:

**history git removed.**

``` bash
gitcredentials$ git log -p db.sql
commit 38604def7c70e35dbb94159abacbeb069d7e2835 (HEAD -> master)
Author: root <root@fluidattacks.localdomain>
Date:   Wed Apr 29 10:50:17 2020 -0500

    Delete credentials

diff --git a/db.sql b/db.sql
index 489ca3e..b6eaabb 100644
--- a/db.sql
+++ b/db.sql
@@ -1,11 +1,11 @@
 use mysql;

-CREATE USER 'coder'@'localhost' IDENTIFIED BY '***REMOVED***';
+CREATE USER 'coder'@'localhost' IDENTIFIED BY '';
 GRANT ALL PRIVILEGES ON *.* TO 'coder'@'localhost';
 FLUSH PRIVILEGES;

 create database if not exists coder;
   use coder;
   create table if not exists admin(id int,username varchar(50),password varchar(50));
-  insert into admin values(1,"administrator","***REMOVED***");
+  insert into admin values(1,"administrator","");
 exit
```

If, for whatever reason, we could not avoid storing passwords into
configuration files, then it is possible to store them encoded in a
strong cryptographic algorithm. Please avoid the use of `base64` for
this endeavor because the encoding can be detected and decoded easily.

The last thing that we must do is to revoke any exposed credentials in
order to minimize the damage done.

If you want more information about secure coding, you can check our
[**Criteria**](https://docs.fluidattacks.com/criteria/) about them.
