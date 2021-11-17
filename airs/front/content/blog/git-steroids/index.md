---
slug: git-steroids/
title: Git on Steroids
date: 2019-03-04
subtitle: From messy logs to Data Analytics
category: documentation
tags: git, software, documentation, standard, engineering, business, linters
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330885/blog/git-steroids/cover_glgn3d.webp
alt: Computer with do what is great sign.
description: Learn here, among other things, how to define a Git commit message
  syntax and use real-time commit message linters to improve your Git history.
keywords: Git, Standardization, Commitlint, Data Analytics, Efective Logging,
  Documentation, Ethical Hacking, Pentesting
author: Daniel Salazar
writer: dsalazaratfluid
:name: Daniel Salazar
about1: Software Engineer
about2: '“An intellectual says a simple thing in a hard way. An artist says a
  hard thing in a simple way.” Charles Bukowski'
source: https://unsplash.com/photos/5Xwaj9gaR0g
---

There is a universal law that anyone in the tech world should know: If
you ask a programmer to do something, he/she will do it their way.

Even though creativity, abstract thinking, and putting your signature in
your source code is a
[fundamental](https://venturebeat.com/2013/10/19/841449/) part of
programming, sometimes it also becomes a barrier when it comes to
maintainability, readability and usability due to lack of code
standardization.

Many efforts to help programmers to implement best practices in their
code have been made, being Python’s
[PEP 8](https://www.python.org/dev/peps/pep-0008/#introduction) and
Ruby’s [Rubocop Style
Guide](https://github.com/github/rubocop-github/blob/master/STYLEGUIDE.md)
some of the most popular examples. [Linting
tools](https://develoger.com/linting-is-parenting-878b2470836a) are also
of the essence for this task, as they provide a dynamic way for
programmers to check if their code is following all the established
conventions.

So far, it seems like the standardization problems can be easily solved
and never again a bunch of crazy programmers will make a mess out of
something.

<div class="imgblock">

!["Rambo"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330887/blog/git-steroids/thumb-up_d8hk1a.gif)

<div class="title">

Figure 1. It’s all good

</div>

</div>

But wait a minute…​ Is there any other activity involving a creative
process that programmers frequently do? Oh yes, we have
[Git](https://git-scm.com/) commit messages.

## Most Git repositories have messy logs

Thanks to the [`Continuous Hacking`](../../services/continuous-hacking/)
service we offer at `Fluid Attacks`, we get to see `Git` repositories
from different organizations in several countries. A vast majority of
these repositories have messy logs.

Such problem can be easily explained: Teams do not stick to a specific
standard when it comes to commit messages and general `Git` logging.
Programmers just fill out their commit messages the way they personally
think it is best.

You may say:

> Ok, logs may be a little messy, but should I really care that much
> about them?

The short answer is: Yes, you definitely should.

For the long answer, I am first going to number the cons of having messy
`Git` logs.

### Cons

1. **Logs fail to accomplish their purpose:**

    Usually, due to vague or incomplete commit messages, a commit
    message log can only be understood by the one who wrote it (just
    like it happens with source code), thus making the log useless.

2. **Reverting becomes a headache:**

    If there is not a clear history of your repo, reverting to a
    previous version given the need will always be painful, as you will
    have to decipher such history in order to know to what point you
    want to go back.

3. **Knowing who did what becomes harder:**

    Good commit messages express, from a high level perspective, what
    changes were made. Not-so-good commit messages usually have two or
    three words and do not actually tell the reader what was changed,
    forcing him/her to look at the source code.

Lastly, let me bring it down to a specific example of how a `Git`
repository history looks when programmers do whatever they want:

<div class="imgblock">

!["Bad Log"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330884/blog/git-steroids/bad-log_q1n4bx.webp)

<div class="title">

Figure 2. Bad Git Log

</div>

</div>

Notice how these commit messages do not communicate anything regarding
the changes that were made, they’re basically trash logs.

### Pros

Other than solving all the cons mentioned above, there are two extra
pros:

1. **Data Analytics for the repo becomes possible:**

    When you have one hundred developers working simultaneously on a
    repository, you definitely want to know things like:

    - What percentage of time do they spend fixing bugs?

    - What percentage of the programmers focus on creating new
      features?

    - What are the main causes of reverts in the repo?

    And an endless number of questions whose answers might be incredibly
    useful for both business insights and development
    performance/quality improving within the company. By having a
    defined commit message syntax, such answers can be found by using
    [Data
    Analytics](https://www.techopedia.com/definition/26418/data-analytics)
    techniques

2. **Logs (partially) become your documentation:**

    By standardizing commit messages, you will no longer have to create
    huge documentation manuals explaining all the details of how a
    product internally works. Each file within the repo will have its
    related history with detailed information about how it currently
    works and worked in the past. Some documentation will probably still
    be needed (user documentation, for example), but we have witnessed
    how the amount of documentation required dramatically diminishes
    thanks to good logs.

After setting a standard syntax for commit messages, your repo history
will start to look like this:

<div class="imgblock">

!["Good Log"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330883/blog/git-steroids/good-log_pbxxpb.webp)

<div class="title">

Figure 3. Good Git Log

</div>

</div>

I want you to notice the three most important details to begin with:

1. Titles include keywords like `feat`, `front`, `fix`, `doc`…​ These
    tags will be essential for the Data Analytics efforts, as they will
    allow [algorithms](../crash-course-machine-learning/) to know what
    the purpose of the commit was.

2. Body section is usually itemized, with every item describing
    relevant changes made in the commit.

3. An issue (\#N.N) is always referenced with the purpose of
    understanding what the programmer was trying to do with the commit.
    This is useful for version control services with issue trackers like
    [Gitlab](https://gitlab.com/), [Github](https://github.com/), etc.

## Implementing a commit message Syntax

If by this point you are convinced about the importance of having a
standard commit message syntax, and are interested in implementing it,
make sure to keep reading, as I will show the syntax we use, the tools
that support it, and the benefits we get from it.

In `Fluid Attacks` we use the [Angular JS Commit Message
Conventions](https://docs.google.com/document/d/1QrDFcIiPjSLDn3EL15IJygNPiHORgU1_OOAqWjiDU5Y/edit)
syntax with a few modifications inspired by our specific needs.

### Syntax

The syntax is as follows:

``` text
  [type]([scope]): #[issue-number]{.issue-part} [title] // This is the commit title
                 // This blank line separates the commit title from the commit body
  [body]         // This is the commit body. It CAN have multiple lines
```

Where:

- **\[variable\]** are **required** variables that must be replaced in
  a final commit message (**\[\]** symbols must be removed).

- **{variable}** are **optional** variables that must be replaced or
  removed in a final commit message (**{}** symbols must be removed).

- **// Comment** are comments that must be removed in a final commit
  message.

In the following sections I will explain in detail what this syntax can
help us achieve.

### Types

Types offer a high level perspective of the commit purpose. They are
explicitly defined in a closed list that covers most (if not all)
possible scenarios.

In the syntax, the **\[type\]** variable has to be one of the following:

``` text
  rever  // Revert to a previous commit in history
  feat   // New feature
  perf   // Improves performance
  fix    // Bug fix
  refac  // Neither fixes a bug or adds a feature
  test   // Adding missing tests or correcting existing tests
  style  // Do not affect the meaning of the code (formatting, etc)
```

Notice how types are short words that can be easily read by anyone, but
also represent keywords that can be processed by a machine.

### Scopes

Scopes provide specific detail about what part of the repository/system
was modified in the commit. Just like types, they are explicitly defined
in a closed list.

In the syntax, the **\[scope\]** variable has to be one of the
following:

``` text
    front  // Front-End change
    back   // Back-End change
    infra  // Infrastructure change
    conf   // Configuration files change
    build  // Build system, CI, compilers, etc (scons, webpack...)
    job    // asynchronous or schedule tasks (backups, maintenance...)
    cross  // Mix of two or more scopes
    doc    // Documentation only changes
```

Notice how scopes, just like types, are also human-readable and
machine-readable.

### Other important rules

Articles like [this one](https://chris.beams.io/posts/git-commit/) and
learning on the fly helped us to define other rules for improving
general commit message quality:

1. A **Commit title** must exist.

2. A **Commit title** must **not** contain the '**:**' character aside
    from the one specified in the syntax.

3. A **Commit title** must have 50 characters or less.

4. A **Commit title** must be lower case.

5. A **Commit title** must not finish with a dot '**.**'.

6. A **Commit title** must reference an issue.

7. A **Commit title** must be meaningful. Avoid using things like
    `feat(build): #5.1 feature`.

8. A **blank line** between commit title and commit body must exist.

9. A **commit body** must exist.

10. Lines in **commit body** must be 72 characters or less.

11. Try to itemize your **commit body**.

12. Do **not** use the word '**part**' for splitting commits for a
    single issue. Use **\#\[issue-number\]{.issue-part}** instead as
    specified in the syntax.

### Explaining combinations

Below is a table explaining all the possible combinations between types
and scopes for a commit message (Types are columns, scopes are rows):

|                   | rever                                                | feat                                                                  | perf                                          | fix                                            | refac                                             | test                                        | style                                              |
| ----------------- | ---------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------- | ---------------------------------------------- | ------------------------------------------------- | ------------------------------------------- | -------------------------------------------------- |
| <p> **front** <p> | <p> Revert front-end to a previous version      </p> | <p> Add new feature to front-end                                 </p> | <p> Improve perf in front-end            </p> | <p> Fix something in front-end            </p> | <p> Change something in front-end            </p> | <p> Add tests for front-end            </p> | <p> Change front-end code style               </p> |
| <p> **back**  <p> | <p> Revert back-end to a previous version       </p> | <p> Add new feature to back-end                                  </p> | <p> Improve perf in back-end             </p> | <p> Fix something in back-end             </p> | <p> Change something in back-end             </p> | <p> Add tests for back-end             </p> | <p> Change back-end code style                </p> |
| <p> **infra** <p> | <p> Revert infra to a previous version          </p> | <p> Add new feature to infra                                     </p> | <p> Improve perf in infra                </p> | <p> Fix something in infra                </p> | <p> Change something in infra                </p> | <p> Add tests for infra                </p> | <p> Change infra code style                   </p> |
| <p> **conf**  <p> | <p> Revert config files to a previous version   </p> | <p> Add new feature to config files                              </p> | <p> NA                                   </p> | <p> Fix something in config files         </p> | <p> Change something in config files         </p> | <p> NA                                 </p> | <p> Change config files code style            </p> |
| <p> **build** <p> | <p> Revert building tools to a previous version </p> | <p> Add new feature to building tools or add a new building tool </p> | <p> Improve building perf                </p> | <p> Fix something in building tools       </p> | <p> Change something in building tools       </p> | <p> Add tests for building tools       </p> | <p> Change building tools code style          </p> |
| <p> **job**   <p> | <p> Revert jobs to a previous version           </p> | <p> Add new feature to jobs or add a new job                     </p> | <p> Improve jobs perf                    </p> | <p> Fix something in jobs                 </p> | <p> Change something in jobs                 </p> | <p> Add tests for jobs                 </p> | <p> Change jobs code style                    </p> |
| <p> **cross** <p> | <p> Revert several scopes to a previous version </p> | <p> Add new feature for several scopes                           </p> | <p> Improve perf in several system parts </p> | <p> Fix something in several system parts </p> | <p> Change something in several system parts </p> | <p> Add tests for several system parts </p> | <p> Change code style in several system parts </p> |
| <p> **doc**   <p> | <p> Revert doc to a previous version            </p> | <p> Add new doc                                                  </p> | <p> NA                                   </p> | <p> Fix something in doc                  </p> | <p> Change something in doc                  </p> | <p> NA                                 </p> | <p> Change doc style                          </p> |

Where:

- `perf` is performance.

- `infra` is infrastructure.

- `config` is configuration.

- `doc` is documentation.

- `NA` is not applicable.

### Differences with pure AngularJS syntax

In this section I will talk about the changes we made to the original
`AngularJS` syntax and the reasons behind them.

#### Types

1. Instead of creating a particular syntax only for reverts as
    specified in the [AngularJS'
    document](https://docs.google.com/document/d/1QrDFcIiPjSLDn3EL15IJygNPiHORgU1_OOAqWjiDU5Y/edit#heading=h.fpepsvr2gqby),
    for the sake of simplicity, we decided to make a **rever** type that
    follows the same syntax as everything else.

2. The **docs** type was renamed to **doc** and turned into a scope.
    The reason of such change was to make **doc** commits more
    informative by allowing programmers to specify the purpose of the
    documentation change. For example:

    - **feat(doc):** documenting new feature.

    - **fix(doc):** fixing documentation.

    - **style(doc):** changing its style.

3. We added a **perf** type for performance changes with the purpose of
    identifying what commits have a performance improvement as main
    objective and reducing the number of commits that would fall under
    the **refac** type.

4. **chore** type was removed as any maintenance commit can be
    translated to a **perf**/**refac**/**fix** commit.

5. In order to have shorter commit titles, we shortened types like
    **docs** to **doc**, **revert** to **rever**, **refactor** to
    **refac**.

#### Scopes

When it comes to scopes, the difference consists in us having a closed
list of keywords while `AngularJS` allowing programmers to specify any
scope they want.

According to the `AngularJS` document, “Scope can be anything specifying
place of the commit change. For example `$location`, `$browser`,
`$compile`, `$rootScope`, `ngHref`, `ngClick`, `ngView`, etc…​”.

We, on the other hand, consider that this information should go in the
commit **\[title\]**.

By moving the “place of the commit change” to the **\[title\]**, we get
to define some generic scopes that allow us to make commit messages more
informative.

Scopes like **front**, **back**, **build**, etc, although not as precise
as **ngClick**, are machine-readable and still provide information about
where the change was made. This, combined with allowing the programmer
to be more specific in the **\[title\]**, is why we decided to create a
closed list for scopes.

#### Other differences

The last big difference between the `AngularJS` syntax and ours is the
**\#\[issue-number\]{.issue-part}** part, whose purpose is to force
commits to always reference an issue in order to be able to track what
motivated such commit.

Other minor differences, like making a maximum of 50 characters for the
commit title mandatory, are either based on personal opinions of what we
think makes a commit message look better, or preferring rules taken from
other places over the `AngularJS` ones.

## Make syntax usage a reality

You may be thinking:

> Ok, we just defined a huge commit message syntax with a ton of rules.
> But, how are we actually going to make programmers follow it in a
> pragmatic way?

Enter the savior:
[Commitlint](https://conventional-changelog.github.io/commitlint/#/).

`Commitlint` is an incredible tool that can check all the syntax we just
defined. Not only it runs all the checks instantly, but it works as a
[Git hook](https://git-scm.com/book/uz/v2/Customizing-Git-Git-Hooks),
which means that it runs all the checks right after a programmer runs a
**git commit** command on his/her local machine. It is even capable of
**failing** the commit attempt if the commit message the programmer just
provided happens to be non-syntax-compliant.

### Proof of concept

We won’t be setting up `Commitlint` for this specific syntax as it would
make the article too technical. Nevertheless, I will show you how it
currently works in one of our repos:

#### Bad commit message

<div class="imgblock">

!["Failed commit"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330885/blog/git-steroids/failed-commit_vnt8vj.gif)

<div class="title">

Figure 4. Failed commit

</div>

</div>

The commit we entered was:

<div class="imgblock">

!["Bad commit message"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330883/blog/git-steroids/bad-commit_b9awue.webp)

<div class="title">

Figure 5. Bad Commit message

</div>

</div>

The `Commitlint` output was:

<div class="imgblock">

!["Bad commit message"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330884/blog/git-steroids/commitlint-fail_ovnl4l.webp)

<div class="title">

Figure 6. Failed Commitlint output

</div>

</div>

Notice how `Commitlint` dynamically tells the programmer what specific
rules his/her commit message is not following, making the fix process a
lot easier. The commit attempt was also stopped by `Commitlint`, as it
doesn’t allow commits to pass unless their message is syntax compliant.

#### Good commit message

<div class="imgblock">

!["Passed commit"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330883/blog/git-steroids/passed-commit_mwoo1p.gif)

<div class="title">

Figure 7. Passed commit

</div>

</div>

The commit we entered was:

<div class="imgblock">

!["Good commit message"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330882/blog/git-steroids/good-commit_nbu7ax.webp)

<div class="title">

Figure 8. Good Commit message

</div>

</div>

The `Commitlint` output was:

<div class="imgblock">

!["Passed commit message"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330883/blog/git-steroids/commitlint-pass_keuy2m.webp)

<div class="title">

Figure 9. Passed Commitlint output

</div>

</div>

Notice how `Commitlint` tells the programmer that all checks passed and
proceeds to accept the commit.

## A little bit of Data Analytics

Now that we have defined a commit message syntax, I would like to show
you a few very simple [`Chartio`](https://chartio.com/) charts we are
now able to generate from our
[Integrates](https://gitlab.com/fluidattacks/integrates) repository:

### Pie chart of monthly commit types for February, 2019

<div class="imgblock">

!["Monthly commit types"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330883/blog/git-steroids/types-chart_yf7adu.webp)

<div class="title">

Figure 10. Monthly commit types for February, 2019

</div>

</div>

This chart allows us to know the percentage of commits for every type in
a month.

One possible interpretation can be:

During February, 2019, out of 132 commits, 39.4% of them (52) had
developing a new feature as their purpose.

### Pie chart of monthly commit scopes for February, 2019

<div class="imgblock">

!["Monthly commit scopes"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330882/blog/git-steroids/scopes-chart_rfkoac.webp)

<div class="title">

Figure 11. Monthly commit scopes

</div>

</div>

This chart allows us to know the percentage of commits for every scope
in a month.

One possible interpretation can be:

During February, 2019, out of 132 commits, 33.3% of them (44) were
focused on the back-end of the site.

### Heatmap chart of monthly commit types vs scopes for February, 2019

<div class="imgblock">

!["Monthly commit heatmap"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330884/blog/git-steroids/heatmap-chart_w1uw1h.webp)

<div class="title">

Figure 12. Monthly commit heatmap

</div>

</div>

This chart allows us to know:

- What type/scope combinations were mostly used.

- What type/scope combinations were never used.

- In general, we can get insights about what programmers did and where
  they did it.

One possible interpretation can be:

During February, 2019, out of 132 commits, 20 of them were feat(back),
leading us to think that programmers spent a considerable amount of
their time programming new functionalities in the back-end of the site.

### It does not end here

Now that we have a commit message syntax and our `Git` logs are growing
everyday, it is up to us to think what we want to do with the normalized
data we’re getting.

Many different charts and analysis can be done, it is just a matter of
asking ourselves:

1. What do we want to know?

2. Can we know it with the data we currently have?

if so, lets make it happen\!

## Conclusion

In this article we’ve covered from the importance of `Git` logs to what
benefits we can obtain by standardizing our commit message syntax and
implementing tools for checks like `Commitlint`, being Data Analytics
the most important one.

I invite you to check the commit history of our public repository:

- [Product](https://gitlab.com/fluidattacks/product/commits/master)

### Want to get more technical?

Make sure to visit our [Commit Message Documentation
Page](https://gitlab.com/fluidattacks/default/wikis/Commit-and-MR-Messages).
There you will be able to find more detailed information regarding our
commit message syntax and other interesting topics like expanding syntax
checks to `Gitlab` Merge Requests.

That was it\! Have a good one\!
