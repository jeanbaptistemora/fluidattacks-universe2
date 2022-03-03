---
id: main
title: Main
sidebar_label: Main
slug: /development/writing/blog/main
---

* **BM01:** Our target audience is anyone interested in cybersecurity.
  Therefore, we *must* use non-technical English as much as possible.

* **BM02:** We *must* write blog posts
  that have some relation to cybersecurity.
  (We have a list of **recommended topics** [here](https://fluidattacks.com/topics/),
  but we can address many others;
  see [the latest posts](https://fluidattacks.com/blog/)).

* **BM03:** We *must* generate blog posts
  in the markup language [Markdown](https://daringfireball.net/projects/markdown/).
  (Please refer to
  [this document](https://github.com/markdownlint/markdownlint/blob/master/docs/RULES.md)
  for Markdown rules.)

## Title and subtitle

* **BT01:** We *should* grab the readers' attention
  with the blog posts' titles,
  making them funny, thought-provoking or exciting.
  We *can*, for example, write a title as a question
  (e.g., "[What's the Perfect Crime?](https://fluidattacks.com/blog/spectre/)")
  or address it directly to the reader
  (e.g., "[I Saw Your Data on the Dark Web](https://fluidattacks.com/blog/dark-web/)"),
  but we *must not* create a generic title
  (e.g., "SQL Injection").

* **BT02:** We *must* write titles that do not exceed **35 characters**.

* **BT03:** In each case,
  we *should* create a subtitle
  that reflects the purpose or central idea of the blog post
  (e.g., "[Get a digest of Internet crime over the last year](https://fluidattacks.com/blog/fbi-2020-report/),"
  "[Confusion with the cloud shared responsibility model](https://fluidattacks.com/blog/shared-responsibility-model/)").

* **BT04:** We *must* write subtitles that do not exceed **55 characters**.

## Length and structure

* **BS01:** We *must* write blog posts of between **800** and **1,200 words**.

* **BS02:** We *should* write blog posts
  with structures similar to the following
  (based on recommendations by the American Lecturer
  [Robert Pozen](https://www.amazon.com/Extreme-Productivity-Boost-Results-Reduce-ebook/dp/B007HBLNSS)):

  1. An introduction that contextualizes the reader,
     states the main theme,
     and describes the organization of the text.
  1. A body with paragraphs highlighting central ideas
     and providing supporting information for them
     (subtitles can make the structure clearer).
  1. A conclusion that, rather than condensing the main points,
     provides lessons learned, possible implications
     or recommendations to keep in mind.

* **BS03:** We *must* build blog posts
  with a [LIX](https://en.wikipedia.org/wiki/Lix_(readability_test))
  value below **50**
  to make them easy to read.
  (To achieve this,
  we can use short sentences and short words.)

## Images

* **BI01:** We *must* include a cover image
  taken *only* from [Unsplash](https://unsplash.com/)
  for each blog post
  (it *must* have a size of **900 × 600 px** and less than **800 KB**).

* **BI02:** We *must* name the cover image as follows:
  cover_[main keyword of the post]
  (e.g., cover_pentesting; both words in lower case).

* **BI03:** We *can* use images from different websites and other sources
  within the bodies of the blog posts.

* **BI04:** We *must* name each image
  with a corresponding keyword in lower case.
  (We *can* repeat the name with an initial capital letter
  between the brackets after the link of the image
  and even accompany it with other keywords.)
  Example:

  ![BI04](https://res.cloudinary.com/fluid-attacks/image/upload/v1625267521/docs/development/writing/bib_qq6euu.webp)

* **BI05:** We *should* put a brief description
  under each image we use
  (it must be no longer than **80 characters**).

* **BI06:** We *must* include the reference as a hyperlink
  in the description of each image that does not belong to us.
  Example:

  ![BI06](https://res.cloudinary.com/fluid-attacks/image/upload/v1624049949/docs/development/writing/bia_xv4isk.webp)

* **BI07:** We *must* always upload the images to [Cloudinary](https://cloudinary.com/)
  and then use their links,
  changing their filename extensions to .webp
  inside the .adoc files.
  (Only for `Fluid Attacks` staff.)

## Others

* **BO01:** Whenever we create a post with an interview,
  we *must* use
  the `[role="fluid-question"]` and `[role="fluid-answer"]` commands
  to display each question and answer (this one indented by two spaces)
  in a specific way.
  Example:

  ![BO01](https://res.cloudinary.com/fluid-attacks/image/upload/v1625258536/docs/development/writing/boa_jlahex.webp)
