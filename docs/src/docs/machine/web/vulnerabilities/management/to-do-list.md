---
id: to-do-list
title: To-Do List
sidebar_label: To-Do List
slug: /machine/web/vulnerabilities/management/to-do-list
---

If you want to organize your daily
work on ARM, you can use our To-Do
List feature.
Through this function, you can be
aware of all the vulnerabilities
assigned to you and have good
tracking in your daily tasks.
To access it, you just have to
click on the **To-Do List** icon
in the top bar or follow
[this link](https://app.fluidattacks.com/todos)
(/todos).

![ToDoList table](https://res.cloudinary.com/fluid-attacks/image/upload/v1675157504/docs/web/vulnerabilities/management/todo_list.png)

However,
an initial question could be:
How can we assign vulnerabilities
to our team?
Enter this [link](/machine/web/vulnerabilities/management/vulnerability-assignment),
and you will see how to do it!

## To-Do List table

The To-Do List table shows
us what vulnerabilities
are assigned to me,
and I am responsible
for solving them.
You find the following information:

- **Organization:**
  The name of the [organization](/machine/web/creating-organization)
  where the specific
  vulnerabiity is found.
- **Group name:**
  The name of the [group](/machine/web/groups)
  where that specific
  vulnerability is found,
  clicking on it redirects you
  to the vulnerability
  typology tab of the group.
- **Type:**
  The typology is that [vulnerability](/criteria/vulnerabilities/).
  When you click on it you
  will be redirected to the
  description of that location.
- **Vulnerability:**
  Where it is located,
  the vulnerability.
- **Evidence:**
  Clicking on view will
  redirect you to the
  [evidence](/machine/web/vulnerabilities/evidence)
  tab in the locations tab.
- **Last reattack:**
  The [Reattack](/squad/reattacks)
  status requested
  in the list of vulnerabilities
  assigned to the user.
- **Severity:**
  Severity level based on the CVSS.
- **Tags:**
  The tags that you put at the
  time of assigning the vulnerability.

## Functionalities

In this section of the **ARM**
we find the following functionalities:

### Edit vulnerabilities

To edit a vulnerability,
you must select it in the
check box on the left,
followed by the **Edit button**.

![Edit button](https://res.cloudinary.com/fluid-attacks/image/upload/v1675158155/docs/web/vulnerabilities/management/edit_action.png)

A pop-up window will appear
for you to edit the vulnerability,
where you can change the treatment,
assigned,
and the other fields that compose it.
To save the changes you have made,
click on the **Confirm button**.

![Edit window](https://res.cloudinary.com/fluid-attacks/image/upload/v1674756505/docs/web/vulnerabilities/management/edit_pop_up.png)

Remember that for any change you make,
you will receive a notification of these;
also,
note that the changes you can make
when editing is according
to the role you have.
To learn more about roles,
click [here](/machine/web/groups/roles/)

### Reattack

You can perform the
[Reattack](/squad/reattacks)
action in the
[locations](/machine/web/vulnerabilities/management/locations)
view and in the
[To-Do List](/machine/web/vulnerabilities/management/to-do-list).
Remember that a reattack is
when you have already applied
a solution for an existing
vulnerability and you want
to validate its effectiveness.

To perform a reattack
from the To-Do List view,
you have to select which
vulnerability you want
to validate by clicking
on the check box on the left,
followed by the **Reattack button**.

![Reattack ToDoList](https://res.cloudinary.com/fluid-attacks/image/upload/v1675159057/docs/web/vulnerabilities/management/reattack.png)

A pop-up window will appear asking
you for the justification you applied
in the solution;
remember that this justification
is composed of 10 or more characters.
When you have typed the validation,
click on the **Confirm button**.

![Justification ToDo](https://res.cloudinary.com/fluid-attacks/image/upload/v1674757123/docs/web/vulnerabilities/management/reattack_justification.png)

Here this vulnerability enters
in **Requested** status waiting
for the validation of its solution.
We invite you to enter [here](/squad/reattacks/)
to understand the status of the
reattacks and their validation procedure.

### Filters

Filters are one of the features
found throughout our **ARM** platform,
helping us to analyze data quickly.
The filters in this section are
located on the right side next
to the search bar.

![Filters ToDo](https://res.cloudinary.com/fluid-attacks/image/upload/v1675158605/docs/web/vulnerabilities/management/filter_todo.png)

Here you can filter by **Organization**,
**Group name**,
**type**,
**Last reattack**,
**Severity** and
**tags**.
Note that you must set clear filters
since the filter you apply will
be maintained until you change
any of these.

![Filters options](https://res.cloudinary.com/fluid-attacks/image/upload/v1666267778/docs/web/vulnerabilities/management/filters_options_todo_list.png)

### Table refresh

If you need to refresh the
To-Do List table view,
you can do so with the button
on the right next to the
reattack button.

![refresh](https://res.cloudinary.com/fluid-attacks/image/upload/v1675159342/docs/web/vulnerabilities/management/refrest.png)

### Search bar

The search bar filters the information
contained in the columns of the table.

:::tip
Remember that in the table of
this section you have links that
redirect you to the
[vulnerability](/machine/web/groups/vulnerabilities)
view,
[locations](/machine/web/vulnerabilities/management),
[evidence](/machine/web/vulnerabilities/evidence)
and [details](/machine/web/vulnerabilities/management/details)
of the vulnerability.
:::
