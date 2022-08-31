---
id: reporting-vulns
title: Reporting in existing types of vulnerabilities
sidebar_label: Reporting in existing types of vulnerabilities
slug: /machine/web/vulnerabilities/reporting-vulns
---

The `Fluid Attacks` ARM has the
necessary tools to be able to
report all the vulnerabilities
encountered in the group's scope.
In order to access this functionality,
you can go to the main screen
for the specific type of
vulnerability you want to report.

When you get there you will
see three different buttons
at the bottom of the table.

![Report](https://res.cloudinary.com/fluid-attacks/image/upload/v1661973578/docs/web/vulnerabilities/reporting-vulns/reporttab.png)

The first button
**Download Vulnerabilities** gives
you a `.yaml` file describing all
the vulnerabilities of this type.
Second button “Explore” is the one
you use to search on your device
the `.yaml` vulnerabilities file.
Lastly the **Update Vulnerabilities**
button is used after you select
said file and want to upload
its vulnerabilities.

## The format to report vulnerabilities

The `.yaml` file mentioned before
needs to have a specific format
or it will give you an error.
You can report vulnerabilities
present in the code of a repository
or directly in the application
that results from this code,
in order to do this you can
write a section in the `.yaml`
file starting with **inputs**
or **lines** respectively.

![Format Report Yaml](https://res.cloudinary.com/fluid-attacks/image/upload/v1661973578/docs/web/vulnerabilities/reporting-vulns/formatreport_yaml.png)

You can add as many
vulnerabilities as you need,
you just have to separate
each one with a hyphen and
add the necessary fields.
Inputs and lines need
different information.
First we have the fields for the inputs:

### The inputs yaml format

This is the structure of the
inputs that you have to fill in.
Here we explain what each field refers to.

![Inputs Yaml Format](https://res.cloudinary.com/fluid-attacks/image/upload/v1661973578/docs/web/vulnerabilities/reporting-vulns/format_lines.png)

- **Field:**
  The name of the specific
  field or fields in the
  application that enables
  the vulnerability.
- **Source:**
  Where the origin of the
  location was given.
  Which can be **Analyst**,
  **Machine** or **Escape**.
- **State:**
  This field specifies if the
  vulnerability currently still
  persists or if it has already
  been resolved.
  It can be **open** or **closed**.
- **Url:**
  This is the web address in
  which we can find the field
  that has the vulnerability.
- **Stream:**
  This information is very important
  for future analysts that access
  the group to be able to find
  the vulnerability.
  You must write a breadcrumb trail
  that starts at the page that is
  viewed first when accessing the
  environment url (e.g. Home,
  Login,
  Dashboard) and write each link
  name or functionality you have
  to access in order to be able
  to reach the field that
  has the vulnerability.
- **Tool:**
  It will give us information on
  which tool the vulnerability was found.
  This field is divided into
  two fields: **Impact**;
  here,
  you specify if it was direct or
  indirect and **name** you
  specify the tool's name.
  Keep in mind that you
  can put several tools.
- **Repo_nickname:**
  This is the nickname that
  a group administrator gives
  to a specific repository.
  You can find it in the
  **Scope** tab of the group
  in the downward-facing arrow
  on the left of the
  Type column,
  which,
  upon click,
  will unfold the description
  for each repository and you
  will see de Nickname,
  as seen in the following image.

![Inputs Format Nickname](https://res.cloudinary.com/fluid-attacks/image/upload/v1661973578/docs/web/vulnerabilities/reporting-vulns/format_report_nickname.png)

You can also use the GraphQL API
to find the nickname by using this query:

```graphql
query {
  group(groupName: "your group name") {
    name
    roots {
      ... on GitRoot {
        environment
        nickname
      }
      ... on IPRoot {
        address
        nickname
        state

      }
      ... on URLRoot {
        host
        nickname
        path
      }
    }
  }
}

```

You can go to this [link](/machine/api)
in order to learn more about using the}
GraphQL API to access all of the
information in the ARM.

### The lines yaml format

Then,
we also have the format for
reporting line vulnerabilities:

![Lines Format](https://res.cloudinary.com/fluid-attacks/image/upload/v1661973578/docs/web/vulnerabilities/reporting-vulns/format_report_inputs.png)

- **Line:**
  This is the specific line or
  lines in the file that contains
  the type of vulnerability
  that is being reported.
- **Commit_hash:**
  This is a 40 characters long
  string that points to the
  specific commit that last
  modified the file before
  encountering the vulnerability.
- **Path:**
  This is the directory path
  to find the file inside
  its repository.
- **State:**
  This field specifies if the
  vulnerability currently still
  persists or if it has already
  been resolved.
  It can be **open** or **closed**.
- **Repo_nickname:**
  This field is the same
  one as in the
  [inputs format](/machine/web/vulnerabilities/reporting-vulns#the-inputs-yaml-format).
- **Source:**
  Where the origin of the
  location was given.
  Which can be **Analyst**,
  **Machine** or **Escape**.
- **Tool:**
  It will give us information
  on which tool the
  vulnerability was found.
  This field is divided into
  two fields: **Impact**;
  here,
  you specify if it was direct
  or indirect and **name** you
  specify the tool's name.
  Keep in mind that you
  can put several tools.
