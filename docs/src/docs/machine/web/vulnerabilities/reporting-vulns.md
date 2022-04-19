---
id: reporting-vulns
title: Reporting in existing types of vulnerabilities
sidebar_label: Reporting in existing types of vulnerabilities
slug: /machine/web/vulnerabilities/reporting-vulns
---

## Where can I report them?

The Fluid Attacks ASM
has the necessary tools
to be able to report all the vulnerabilities
encountered in the group's scope.
In order to access this functionality,
you can go to the main screen
for the specific type of vulnerability
you want to report

![Bulk Edit Button](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211882/docs/web/vulnerabilities/reporting-vulns/bulkedit_highlight_t6bbgm.webp)

When you get there
you can click on the button **Bulk edit**
and the buttons used for reporting vulnerabilities
will appear on the bottom of the page,
you might need to scroll down to see them

![Vulnerability Report Buttons](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211882/docs/web/vulnerabilities/reporting-vulns/reportbuttons_highlight_xw07m2.webp)

The first button
**Download Vulnerabilities**
gives you a .yaml file
describing all the vulnerabilities of this type,
the second button that contains the word **Explore**
is the one you use to search on your device
the .yaml file with the vulnerabilities
that you want to report
and lastly the **Update Vulnerabilities** button
is used after you select said file
and want to upload its vulnerabilities.

## The format to report vulnerabilities

The .yaml file mentioned before
needs to have a specific format
or it will give you an error.
You can report vulnerabilities
present in the code of a repository
or directly in the application
that results from this code,
in order to do this
you can write a section in the .yaml file
starting with **inputs** or **lines** respectively

![Yaml Report Format](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211881/docs/web/vulnerabilities/reporting-vulns/yaml_report_format_gyphfh.webp)

You can add as many vulnerabilities as you need,
you just have to separate each one with a hyphen
and add the necessary fields.
Inputs and lines need different information.
First we have the fields for the inputs:

### The inputs yaml format

- **Field:**
  The name of the specific field or fields
  in the application
  that enables the vulnerability.
- **State:**
  This field specifies
  if the vulnerability
  currently still persists
  or if it has already been resolved.
  It can be **open** or **closed**.
- **Url:**
  This is the web address
  in which we can find the field
  that has the vulnerability.
- **Stream:**
  This information is very important
  for future analysts that access the group
  to be able to find the vulnerability.
  You must write a breadcrumb trail
  that starts at the page
  that is viewed first
  when accessing the environment url
  (e.g. Home, Login, Dashboard)
  and write each link name
  or functionality
  you have to access
  in order to be able to reach
  the field that has the vulnerability.
- **Repo_nickname:**
  This is the nickname
  that a group administrator gives
  to a specific repository.
  You can find it
  in the **Scope** tab of the group
  in the **Nickname** column
  of the **Git roots** section,
  as seen in the following image.

![Repository Nickname](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211883/docs/web/vulnerabilities/reporting-vulns/reponickname_highlight_ol9x9f.webp)

You can also use
the GraphQL API
to find the nickname
by using this query:

```graphql
query {
  project(projectName: "your project name") {
    roots {
      ...on GitRoot {
        nickname
      }
    }
  }
}
```

You can go to this
[link](/machine/api)
in order to learn more
about using the GraphQL API
to access all of the information
in the ASM.

### The lines yaml format

Then,
we also have the format
for reporting line vulnerabilities:

- **Line:**
  This is the specific line or lines
  in the file that contains
  the type of vulnerability
  that is being reported.
- **Commit_hash:**
  This is a 40 characters long string
  that points to the specific commit
  that last modified the file
  before encountering the vulnerability.
- **Path:**
  This is the directory path
  to find the file inside its repository.
- **State:**
  This field specifies
  if the vulnerability currently still persists
  or if it has already been resolved.
  It can be **open** or **closed**.
- **Repo_nickname:**
  This field is the same one as in the
  [inputs format](/machine/web/vulnerabilities/reporting-vulns#the-inputs-yaml-format).
