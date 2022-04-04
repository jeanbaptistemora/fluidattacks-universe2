---
id: roles
title: Roles
sidebar_label: Roles
slug: /machine/web/groups/roles
---

Users on the ASM have different
roles with associated permissions
relevant to work on the platform.
Depending on your role,
you are granted access to certain
functions for your daily use
of the ASM.
You can see your role on the ASM in the
[drop-down menu](/machine/web/user-information)
that appears when you click the
user icon on the upper-right
part of your screen.

The following are the different
roles that are available on the ASM,
along with their descriptions.

## User manager role

This is the role
that gives the user
the most privileges,
this user can do everything
that a client is allowed to do
in the ASM.
This role is made for
the leaders of the product
and, besides the basic privileges,
it allows the user to generate reports,
define important treatments like
accepting vulnerabilities permanently,
requesting Zero Risk treatments,
adding and editing users for the group
and more.

## Executive role

This role is made for
users in managerial positions
that need to be informed
about all the vulnerabilities
that the project has
and interact with them
to ensure their solution.

## User role

This is the default user role,
it is the one given to developers
or the users in charge of
solving the vulnerabilities.
This user can check all the information
about the vulnerabilities
needed for solving them
and also request reattacks
when they deem them solved.

## Vulnerability manager role

The role of vulnerability
manager was designed for
people with a position as
technical leaders in their
company.
This role has access to the
basic privileges on the ASM
and is also enabled to
generate reports;
get notifications;
define,
change and approve treatments;
request reattacks,
and add tags.
The vulnerability manager
**does not** have permissions
to manage roots nor add,
edit or remove users.

## Functions

- **Add roots:**
  This function is for
  adding git roots
  to the scope of the group
  being managed.
- **Add tags:**
  This is for adding tags
  to the group being managed
  which is useful for
  categorizing different groups
  in an organization.
- **Add users:**
  This function is for
  adding user to a group
  and setting their privileges.
- **Approve treatments:**
  This function is for
  when a treatment change is requested,
  as there is a need to validate
  and then accept or reject
  this request.
- **Change treatments:**
  Each vulnerability can be given
  a specific treatment.
  This function gives the ability
  to request the change
  of this treatment.
- **Deactivate/Activate root:**
  This function allows you to:

  1. Deactivate repositories
     for which you no longer want
     an assessment;
  1. Activate repositories you want
     to leave available to our analysts,
     and
  1. Move a root to another group,
     taking all the associated
     vulnerabilities with it.

- **Delete groups:**
  With this function
  you are able to
  completely delete
  the group being managed.
- **Edit roots:**
  This function allows you
  to change URLs of roots
  that do not have reported
  vulnerabilities and edit
  root branches.
- **Edit users:**
  This option is for
  editing everything related
  to the users added
  to the group.
- **Exclusions:**
  This feature allows you
  to choose files or folders
  in your repository that
  you do not want to
  include in the security
  assessments.
- **Generate a report:**
  This feature allows you
  to generate and download
  a complete report with
  detailed information about
  the vulnerabilities of
  a specific group.
- **Receive notifications:**
  This is the ability to
  receive notifications
  that the ASM can send
  related to your group.
- **Request reattacks:**
  When a vulnerability is solved,
  there is the need to ask our hackers
  to verify that it was indeed solved.
  This function gives you
  the ability to make
  this kind of request.
- **View vulnerabilities:**
  The ability to view
  all the information available
  about all the vulnerabilities
  that the project has.

## Roles table

In the following table
we specify
what functions are enabled
for each role.

|                     |User|Executive|Vulnerability manager|User manager|
|:-------------------:|:--:|:-------:|:-------------------:|:----------:|
|View vulnerabilities |X   |X        |X                    |X           |
|Change treatments    |X   |X        |X                    |X           |
|Approve treatments   |    |         |X                    |X           |
|Request reattack     |X   |X        |X                    |X           |
|Add tags             |X   |X        |X                    |X           |
|Add roots            |X   |X        |                     |X           |
|Edit roots           |X   |X        |                     |X           |
|Delete group         |    |         |                     |X           |
|Add users            |    |         |                     |X           |
|Edit users           |    |         |                     |X           |
|Receive notifications|X   |         |X                    |X           |
|Generate a report    |    |         |X                    |X           |
|Exclusions           |    |         |                     |X           |
|Deactivate/Activate root  |    |         |                     |X           |
