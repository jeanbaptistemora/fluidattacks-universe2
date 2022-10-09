---
id: metadata
title: Metadata
sidebar_label: Metadata
slug: /development/writing/blog/metadata
---

Metadata are variables that influence the final rendering of pages
and how search engines index them.
Below, we show a table with the **mandatory** metadata for a blog post:

|Metadata             |Description                                    |
|:--------------------|:----------------------------------------------|
|:page-slug:          |The portion of the link that goes after fluidattacks.com/blog/, completing the URL where we can find the new blog post (e.g., code-translate/). It *must not* exceed **35 characters** and *must* contain the main words of the post (preferably associated with the title and subtitle), all in lower case and separated by hyphens. In addition, it *may* have numbers but no spaces, prepositions, conjunctions or connectors, or special characters.|
|:page-date:          |Date of publication of the blog post. It *must* follow the format YYYY-MM-DD (e.g., 2021-06-24).|
|:page-subtitle:      |Short subtitle that can capture the purpose or main idea of the blog post. It *must not* exceed **55 characters**.|
|:page-category:      |The category (only one) to which the new blog post belongs (e.g., attacks, philosophy, machine-learning; see all categories [here](https://fluidattacks.com/blog/categories/)). It *must* appear in lowercase letters.|
|:page-tags:          |Noteworthy words related to the main topic that index the blog post internally. They *must* be no more than **six** and *must* appear in lower case and separated by commas (see all tags [here](https://fluidattacks.com/blog/tags/)).|
|:page-image:         |The full link to the cover image of the blog post. It *must* be in [Cloudinary](https://cloudinary.com/), and its filename extension *must* be *.webp* (this also applies to the images that appear in the body of the post).|
|:page-alt:           |The reference to the author of the cover photo or image (e.g., Photo by Tomas Sobek on Unsplash).|
|:page-description:   |A summary of the main idea of the blog post that appears in the blog index and search engine results. It *must* be no longer than **160 characters** and no shorter than **80 characters**.                                            |
|:page-keywords:      |The most important words in the blog post through which a search engine can find it. They *must* be no more than **nine** (including the keywords *Ethical Hacking* and *Pentesting* that we must always use). Some of them can be the same as the tags, and all of them *must* appear with initial capital letters and separated by commas.|
|:page-author:        |Name and first surname of the author of the blog post.|
|:page-writer:        |Name of the image (in lower case) that represents the author of the blog post (e.g., the name of Arturo Monsalve's image is *amonsalve*).|
|:about1:             |Information describing the author, such as academic experience, profession or business role (e.g., Systems Engineering undergraduate student; Cybersecurity Editor).|
|:about2:             |Additional information about the author (this is optional): personal interests, links to personal blogs or profiles, motivational quotes.|
|:source:             |Link to the cover image from [Unsplash](https://unsplash.com/).|
