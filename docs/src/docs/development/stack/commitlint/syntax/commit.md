---
id: commit
title: Commit
sidebar_label: Commit
slug: /development/stack/commitlint/syntax/commit
---

## Syntax

Valid commit messages
have the structure:

```markup
[product]\[type]([scope]): #[issue-number] [title] // This is the commit title
               // This blank line separates the commit title from the commit body
[body]         // This is the commit body. It CAN have multiple lines
```

- **[variable]** are **required** variables
  that must be replaced
  in a final commit message
  (**[]** symbols must be removed)
- **// Comment** are comments
  that must be removed
  in a final commit message

## Rules

The following rules must be met
for a commit message to be valid,
the **product** rule only required
for the integrates repository:

1. **[type]** variable has to be
   one of the following:

   ```markup
   rever  // Revert to a previous commit in history
   feat   // New feature
   perf   // Improves performance
   fix    // Bug fix
   refac  // Neither fixes a bug or adds a feature
   test   // Adding missing tests or correcting existing tests
   style  // Do not affect the meaning of the code (formatting, etc)
   sol    // Hacking solution only for writepus and training repo
   ```

1. **[scope]** variable has to be
   one of the following:

   ```markup
   front  // Front-End change
   back   // Back-End change
   infra  // Infrastructure change
   conf   // Configuration files change
   build  // Build system, CI, compilers, etc (scons, webpack...)
   job    // asynchronous or schedule tasks (backups, maintenance...)
   cross  // Mix of two or more scopes
   doc    // Documentation only changes
   vbd    // Vulnerable by design hacking solution only for writeups repo
   code   // Programming challenge solution only for training repo
   hack   // ctf-hacking challenge solution only for training repo
   ```

1. **[product]** variable has to be:

   ```markup
   integrates // Changes that affect both integrates and forces
   ```

1. A **Commit title**
   must exist.

1. A **Commit title**
   must **not** contain
   the '**:**' character.

1. **Commit title**
   must have 60 characters
   or less.

1. **Commit title**
   must be lower case.

1. **Commit title**
   must not finish
   with a dot '**.**'.

1. **Commit title**
   must reference
   an issue.

1. **Commit title**
   must be meaningful.
   Avoid using things like
   `feat(build)[integrates]: #5 feature`.

1. If **commit title**
   has **sol** type,
   it must reference
   issue **#0**.

1. A **blank line**
   between commit title
   and commit body
   must exist.

1. A **commit body**
   must exist.

1. Lines in **commit body**
   must have 72 characters
   or less.

### Possible combinations

Below is a table explaining
all the possible combinations
between types and scopes
for a commit message
(Types are columns, scopes are rows):

|           |                  **rever**                  |                           **feat**                           |               **perf**               |                **fix**                |                **refac**                 |              **test**              |                 **style**                 |
| :-------: | :-----------------------------------------: | :----------------------------------------------------------: | :----------------------------------: | :-----------------------------------: | :--------------------------------------: | :--------------------------------: | :---------------------------------------: |
| **front** |   Revert front-end to a previous version    |                 Add new feature to front-end                 |      Improve perf in front-end       |      Fix something in front-end       |      Change something in front-end       |      Add tests for front-end       |        Change front-end code style        |
| **back**  |    Revert back-end to a previous version    |                 Add new feature to back-end                  |       Improve perf in back-end       |       Fix something in back-end       |       Change something in back-end       |       Add tests for back-end       |        Change back-end code style         |
| **infra** |     Revert infra to a previous version      |                   Add new feature to infra                   |        Improve perf in infra         |        Fix something in infra         |        Change something in infra         |        Add tests for infra         |          Change infra code style          |
| **conf**  |  Revert config files to previous a version  |               Add new feature to config files                |                  NA                  |     Fix something in config files     |     Change something in config files     |                 NA                 |      Change config files code style       |
| **build** | Revert building tools to previous a version | Add new feature to building tools or add a new building tool |        Improve building perf         |    Fix something in building tools    |    Change something in building tools    |    Add tests for building tools    |     Change building tools code style      |
|  **job**  |      Revert jobs to previous a version      |           Add new feature to jobs or add a new job           |          Improve jobs perf           |         Fix something in jobs         |         Change something in jobs         |         Add tests for jobs         |          Change jobs code style           |
| **cross** | Revert several scopes to previous a version |              Add new feature for several scopes              | Improve perf in several system parts | Fix something in several system parts | Change something in several system parts | Add tests for several system parts | Change code style in several system parts |
|  **doc**  |      Revert doc to a previous version       |                         Add new doc                          |                  NA                  |         Fix something in doc          |         Change something in doc          |                 NA                 |             Change doc style              |

Where:

- **perf** is performance.
- **infra** is infrastructure.
- **config** is configuration.
- **doc** is documentation.
- **NA** is not applicable.

## Recommendations

- Try to itemize your commit body:

  ```text
  - Add feature X in file Y
  - Run script Z
  - Remove file A with B purpose
  ```

## Example

Here is an example
of a compliant commit message:

```markup
integrates\feat(build): #13 add type_check

- Add type_check function
- Remove unnecessary print_output function
```

:::tip free trial
**Search for vulnerabilities in your apps for free
with our automated security testing!**
Start your [21-day free trial](https://fluidattacks.com/free-trial/)
and discover the benefits of our [Continuous Hacking](https://fluidattacks.com/services/continuous-hacking/)
[Machine Plan](https://fluidattacks.com/plans/).
If you prefer a full service
that includes the expertise of our ethical hackers,
don't hesitate to [contact us](https://fluidattacks.com/contact-us/)
for our Continuous Hacking Squad Plan.
:::
