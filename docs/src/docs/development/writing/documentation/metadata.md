---
id: metadata
title: Metadata
sidebar_label: Metadata
slug: /development/writing/documentation/metadata
---

Metadata are variables that influence the final rendering of pages
and how search engines index them.
Below, we show a table with the **mandatory** metadata for documentation:

|Metadata             |Description                                    |
|:--------------------|:----------------------------------------------|
|id:          |The portion of text at the end of the URL (after the last forward slash) of the subsection under consideration. For example, *foss* in docs.fluidattacks.com/machine/scanner/plans/foss. It *must not* exceed **25 characters** and **three words**. It *must* contain the main words of the title of the subsection, all in lower case and separated by hyphens. In addition, it *may* have numbers but no spaces, prepositions, conjunctions or connectors, or special characters.|
|title:          |The title of the subsection before its body of text.|
|sidebar_label:      |The name of the subsection (i.e., the title) appearing in the left-hand menu.|
|slug:          |The part of the URL of the subsection that goes after docs.fluidattacks.com (e.g., /machine/scanner/plans/foss).|
