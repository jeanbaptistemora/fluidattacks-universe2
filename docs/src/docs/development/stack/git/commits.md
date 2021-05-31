---
id: commits
title: Commits
sidebar_label: Commits
slug: /development/stack/git/commits
---

## Developer commits

### Syntax

Valid commit messages
have the structure:

```
[product]\[type]([scope]): #[issue-number]{.issue-part} [title] // This is the commit title
               // This blank line separates the commit title from the commit body
[body]         // This is the commit body. It CAN have multiple lines
```

- **[variable]** are **required** variables
  that must be replaced
  in a final commit message
  (**[]** symbols must be removed)
- **{variable}** are **optional** variables
  that must be replaced
  or removed
  in a final commit message
  (**{}** symbols must be removed)
- **// Comment** are comments
  that must be removed
  in a final commit message

### Rules

The following rules must be met
for a commit message to be valid,
the **product** rule only required
for the integrates repository:

1. **[type]** variable has to be
   one of the following:
    ```
    rever  // Revert to a previous commit in history
    feat   // New feature
    perf   // Improves performance
    fix    // Bug fix
    refac  // Neither fixes a bug or adds a feature
    test   // Adding missing tests or correcting existing tests
    style  // Do not affect the meaning of the code (formatting, etc)
    sol    // Hacking solution only for writepus and training repo
    ```
2. **[scope]** variable has to be
   one of the following:
    ```
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
3. **[product]** variable has to be
   one of the following:
	
    ```
    forces // Changes in forces
    integrates // Changes in Integrates
    all // Changes that affect both integrates and forces
    ```

3. A **Commit title**
   must exist.

4. A **Commit title**
   must **not** contain
   the '**:**' character.

5. **Commit title**
   must have 60 characters
   or less.

6. **Commit title**
   must be lower case.

7. **Commit title**
   must not finish
   with a dot '**.**'.

8. **Commit title**
   must reference
   an issue.

9. **Commit title**
   must be meaningful.
   Avoid using things like
   ``feat(build)[integrates]: #5.1 feature``.

10. If **commit title**
    has **sol** type,
    it must reference
    issue **#0**.

11. A **blank line**
    between commit title
    and commit body
    must exist.

12. A **commit body**
    must exist.

13. Lines in **commit body**
    must have 72 characters
    or less.

#### Possible combinations

Below is a table explaining
all the possible combinations
between types and scopes
for a commit message
(Types are columns, scopes are rows):

|  | <b>rever</b> | <b>feat</b> | <b>perf</b> | <b>fix</b> | <b>refac</b> | <b>test</b> | <b>style</b> |
|:-----:|:-----------------------------------------:|:------------------------------------------------------------:|:------------------------------------:|:-------------------------------------:|:----------------------------------------:|:----------------------------------:|:-----------------------------------------:|
| <b>front</b> | Revert front-end to a previous version | Add new feature to front-end | Improve perf in front-end | Fix something in front-end | Change something in front-end | Add tests for front-end | Change front-end code style |
| <b>back</b> | Revert back-end to a previous version | Add new feature to back-end | Improve perf in back-end | Fix something in back-end | Change something in back-end | Add tests for back-end | Change back-end code style |
| <b>infra</b> | Revert infra to a previous version | Add new feature to infra | Improve perf in infra | Fix something in infra | Change something in infra | Add tests for infra | Change infra code style |
| <b>conf</b> | Revert config files to previous a version | Add new feature to config files | NA | Fix something in config files | Change something in config files | NA | Change config files code style |
| <b>build</b> | Revert building tools to previous a version | Add new feature to building tools or add a new building tool | Improve building perf | Fix something in building tools | Change something in building tools | Add tests for building tools | Change building tools code style |
| <b>job</b> | Revert jobs to previous a version | Add new feature to jobs or add a new job | Improve jobs perf | Fix something in jobs | Change something in jobs | Add tests for jobs | Change jobs code style |
| <b>cross</b> | Revert several scopes to previous a version | Add new feature for several scopes | Improve perf in several system parts | Fix something in several system parts | Change something in several system parts | Add tests for several system parts | Change code style in several system parts |
| <b>doc</b> | Revert doc to a previous version | Add new doc | NA | Fix something in doc | Change something in doc | NA | Change doc style |

Where:
- **perf** is performance.
- **infra** is infrastructure.
- **config** is configuration.
- **doc** is documentation.
- **NA** is not applicable.

### Recommendations

- Try to itemize your commit body:
    ```
    - Add feature X in file Y
    - Run script Z
    - Remove file A with B purpose
    ```

- Do **not** use the word '**part**'
  for splitting commits
  or MRs for a single issue.
  Use **#[issue-number]{.issue-part}**
  instead as shown in [Example](#Example)

### Example

Here is an example
of a compliant commit message
(Notice how the issue has
a '**.1**' right after,
meaning that such commit
is the part 1 for solving
the issue):

```
integrates\feat(build): #13.1 add type_check

- Add type_check function
- Remove unnecessary print_output function
```

## Analyst commits

Commit messages are divided into three categories:
- Drills
- Forces exploits
- Others

The following templates contain the following symbols:
- [variable] are required variables that must be replaced in a final commit message
  ([] symbols must be removed)
- {variable} are optional variables that must be replaced or removed in a final commit message
  ({} symbols must be removed)
- // Comment are comments that must be removed in a final commit message

General rules:
- Commit title must be meaningful. Avoid using things like ``feat(build): #5.1 feature``.
- Lines in commit body must have 72 characters or less.

### Drills daily commit

```
drills([scope]): [subscription] - [coverage]%, [tested_lines] el, [tested_inputs] ei
                      // This blank line separates the commit title from the commit body
- [#] el, [#] ei      // Commit body
- [#] vl, [#] vi      // Commit body
- [#]% Total coverage // Commit body
```

- [scope] is one of:
  - lines
  - inputs
  - cross

### Drills enumeration commit

```
drills(enum): [subscription] - [coverage]%, [new_lines] nl, [new_inputs] ni
```

### Drills configuration/resources commit

```
drills(conf): [subscription] - [comments]
```

### Forces fix exploits commits

```
fix(exp): #[issue_number] [subscription] [tag]
```

- [tag] is one of:
  -  asserts-ch, Change in asserts
  -  asserts-fn, False negative in a product
  -  asserts-fp, False positive in a product
  -  service-logic, Error in exploit construction
  -  toe-availability, If the ToE is no longer reachable or available
  -  toe-location, Change in the ToE, like path deletion/movement, etc
  -  toe-resource, Change in the environment, like renaming or deletion

### Other commits

```
[type]([scope]): #[issue_number].[issue_part] [comment]
                      // This blank line separates the commit title from the commit body
- Comment 1           // Commit body
- Comment 2           // Commit body
```

[type] variable has to be one of the following:
- rever  // Revert to a previous commit in history
- feat   // New feature
- perf   // Improves performance
- fix    // Bug fix
- refac  // Neither fixes a bug or adds a feature
- test   // Adding missing tests or correcting existing tests
- style  // Do not affect the meaning of the code (formatting, etc)

[scope] variable has to be one of the following:
- front  // Front-End change
- back   // Back-End change
- infra  // Infrastructure change
- conf   // Configuration files change
- build  // Build system, CI, compilers, etc (scons, webpack...)
- job    // asynchronous or schedule tasks (backups, maintenance...)
- cross  // Mix of two or more scopes
- exp    // Changes over exploits
