---
id: surface
title: Surface
sidebar_label: Surface
slug: /machine/web/groups/surface
---

The surface tab gives more information
about the Target of Evaluation (ToE).
This ToE is the result of repositories,
environments and languages specified
in the scope roots section.

There are three sections in Surface:
**Lines** referring to the Git Roots
repositories,
**Inputs** representing
the environments to test,
such as URLs/IPs and
**Languages** identify the different
languages used in your code.

![Surface Tab](https://res.cloudinary.com/fluid-attacks/image/upload/v1668022585/docs/web/groups/surface/surface_section.png)

## Lines

It shows us the internal content
of the repositories registered
in Git Roots,
visualizing its roots and the
filenames that compose them,
being the ToE that the
Hackers will validate.

![Surface Lines](https://res.cloudinary.com/fluid-attacks/image/upload/v1668022667/docs/web/groups/surface/lines_table.png)

This section shows a table providing
the following information:

- **Root:**
  Name of the root or
  repository that was
  specified in Git Roots.
- **Filename:**
  Path of files that
  compose the root.
- **LOC (Lines of Code):**
  How many lines of code
  does this file have in total.
- **Status:**
  If the file is vulnerable.
- **Modified date:**
  The last time the
  file was modified.
- **Last commit:**
  The last commit was
  identified in the file.
- **Last author:**
  The last author who
  modified the file.
- **Seen at:**
  The date the
  file was added.
- **Priority (IA/ML):**
  It gives a score if
  that file possibly
  has a vulnerability.
  This is done by AI
  (Artificial Intelligence).
- **Be present:**
  The file or document
  is present in the
  repository.

### Filters in Lines section

We have several filters
in the Lines section,
helping us find information
quickly and safely.
By clicking on the
Filters button,
you can access them.

![Lines Filters](https://res.cloudinary.com/fluid-attacks/image/upload/v1668022808/docs/web/groups/surface/lines_filters.png)

## Inputs

It shows us the environments to
test specified in the Scope
section in Environment URLs/IP,
giving us the entry points that
the Hackers will validate.

![Surface Inputs](https://res.cloudinary.com/fluid-attacks/image/upload/v1668022927/docs/web/groups/surface/inputs_table.png)

This section shows a table
providing the following information:

- **Root:**
  Name of the root or
  repository specified
  in Environment URLs.
- **Component:**
  The URLs/IPs that this
  environment has.
- **Entry point:**
  Specific Input in the
  component that will be
  tested by the Hacker.
- **Status:**
  If the component is
  vulnerable.
- **Seen at:**
  The date the component
  was added.
- **Be present:**
  If the component
  is present in the Root.

### Filters in Inputs section

We have several filters options
in the Inputs section.
By clicking on the Filters button,
you will have access to that options
filtering the information of
your interest.

![Inputs Filters](https://res.cloudinary.com/fluid-attacks/image/upload/v1668023023/docs/web/groups/surface/inputs_filters.png)

## Languages

Here you can see the
languages used in your repositories.

![Surface Languages](https://res.cloudinary.com/fluid-attacks/image/upload/v1663758054/docs/web/groups/surface/surface_languages.png)

This section shows a table
providing the following information:

- **Language:**
  The specific type of language
  detected in your inputs.
- **Lines of Code:**
  Total lines of code detected
  by this language.
- **Percentage:**
  The percentage of its usability

### Export button

You can download the information
in the Lines and Inputs table by
clicking on the export button,
which will download a file with
CSV (comma-separated values)
extension.
It contains the data that
composes the tables of these
two surface sections.

### Columns filter

You can show or hide columns
in the table by clicking on
the Columns button and toggling
the on/off button in front
of each column name.
