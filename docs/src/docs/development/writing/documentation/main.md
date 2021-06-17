---
id: main
title: Main
sidebar_label: Main
slug: /development/writing/documentation/main
---

## General

* **DG01:** We *must* create titles for the sections
  (those that appear in the top menu) of **a single word**.

* **DG02:** We *must* create short titles for the subsections
  (those that appear in the left side menu),
  not exceeding **32 characters**.

* **DG03:** We *must not* be repetitive
  in the handling of titles and subtitles.

* **DG04:** We *must* express the names of the sections and subsections
  in the same way wherever we refer to them.

* **DG05:** We *must not* use the same section or subsection names
  in other subsections or elements within them.
  For instance, we do not want URLs ending like this:
  /security/**transparency**/open-source/**transparency**/.

* **DG06:** For each section (e.g., Machine, Development, Criteria),
  we *must* write an introduction that makes it clear to readers
  what they will find there in general and in the subsections.

* **DG07:** We *should* be consistent
  in the presentation of the introductions to all sections.
  Based on recommendations by the American Lecturer
  [Robert Pozen](https://www.amazon.com/Extreme-Productivity-Boost-Results-Reduce-ebook/dp/B007HBLNSS),
  we *can* follow three steps:
  **(a)** Contextualize the reader with facts or background data and issues
  that may be driving them to spend their time there.
  **(b)** Mention, as a summary, the main topic of the section,
  i.e., what we are going to discuss next.
  **(c)** Explain the organization, the text structure,
  and be coherent with the titles and subtitles within the section.
  We can follow a sequence, saying something like:
  "In the first part, we will expose (...).
  In the second part, we will describe (...)."

* **DG08:** We *should* keep the presentation structure
  of the subsections that are part of the same level
  homogeneous (e.g., all of them with an introductory paragraph).

* **DG09:** We *should* exhibit all segments
  of the same group of information in a subsection
  following the same style
  (e.g., saying what the user will find in each case).

* **DG10:** We *must* include all first,
  second and third level subtitles of a subsection
  in the menu on the right side.

* **DG11:** We *must* present the subtitles in the right-hand menu
  in a homogeneous way
  (e.g., in all subsections without bold).

* **DG12:** We *must* speak in the first person,
  but as a group (i.e., using the pronoun we),
  not as an individual.

* **DG13:** We *must* use illustrative images
  every time we explain the elements of an application or software.

* **DG14:** We *must* upload all the images we need to [Cloudinary](https://cloudinary.com/)
  and then use their corresponding links
  (which we must end with *.webp* inside the *.md* files).

* **DG15:** In cases of warnings for the reader,
  pointing out something that *is not* part of the content,
  we *must* use the following command in Markdown
  (the word *note* is just an option): `> **NOTE:** > [Text]`.
  Example:

  ![DG11](https://res.cloudinary.com/fluid-attacks/image/upload/v1623943552/docs/development/writing/dg11_uauncn.webp)
  > **NOTE:**
  > This section of our documentation is under construction.

## [FAQ](https://docs.fluidattacks.com/about/faq)

* **DF01:** We *must* answer the questions without circumlocutions.

* **DF02:** We *must* use the same names of the concepts
  (especially the keywords)
  in the questions and the answers.

## [Glossary](https://docs.fluidattacks.com/about/glossary)

* **DS01:** We *must* generate customized definitions,
  which may be paraphrases of other people's texts.

* **DS02:** We *must* display the words in alphabetical order (A-Z).

## [Requirements](https://docs.fluidattacks.com/criteria/requirements/)

* **DR01:** We *must* make a complete exposition of each requirement
  (i.e., including main sentence, description,
  associated vulnerabilities and references).

* **DR02:** We *must* start in each case with the title of the requirement
  and, below this, we *must* immediately put the main sentence
  without using the word *Requirement* as a subtitle.

* **DR03:** We *should* write the main sentence of the requirement
  starting with a subject in charge of fulfilling a specific task,
  accompanied by the modal verb must.

* **DR04:** In the description of the requirement,
  we *should* expand the information of the main sentence
  with the exposition of the processes involved,
  short definitions of elements and justifications of the requirement.

* **DR05:** We *must* put in quotation marks
  all external information (copied from their sources)
  that is part of the references
  (e.g., [CWE](https://cwe.mitre.org/), [OWASP](https://owasp.org/)).

## [Vulnerabilities](https://docs.fluidattacks.com/criteria/vulnerabilities/)

* **DV01:** We *must* make a complete exposition of each vulnerability
  (i.e., including description and associated requirements).

> **NOTE:**
> This section of our documentation is under construction.
