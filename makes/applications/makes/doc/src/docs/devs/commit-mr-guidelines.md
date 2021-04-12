---
id: commit-mr-guidelines
title: Commit and MR guidelines
sidebar_label: Commit and MR guidelines
slug: /dev
---

## Syntax

Valid commit messages have the structure:

```
[product]\[type]([scope]): #[issue-number]{.issue-part} [title] // This is the commit title
               // This blank line separates the commit title from the commit body
[body]         // This is the commit body. It CAN have multiple lines
```

- **[variable]** are **required** variables that must be replaced in a final commit message (**[]** symbols must be removed)
- **{variable}** are **optional** variables that must be replaced or removed in a final commit message (**{}** symbols must be removed)
- **// Comment** are comments that must be removed in a final commit message

## Rules

The following rules must be met for a commit message to be valid, the **product** rule only required for the integrates repository:

1. **[type]** variable has to be one of the following:
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
2. **[scope]** variable has to be one of the following:
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
3. **[product]** variable has to be one of the following:
	
    ```
    forces // Changes in forces
    integrates // Changes in Integrates
    all // Changes that affect both integrates and forces
    ```

3. A **Commit title** must exist.

4. A **Commit title** must **not** contain the '**:**' character.

5. **Commit title** must have 60 characters or less.

6. **Commit title** must be lower case.

7. **Commit title** must not finish with a dot '**.**'.

8. **Commit title** must reference an issue.

9. **Commit title** must be meaningful. Avoid using things like ``feat(build)[integrates]: #5.1 feature``.

10. If **commit title** has **sol** type, it must reference issue **#0**.

11. A **blank line** between commit title and commit body must exist.

12. A **commit body** must exist.

13. Lines in **commit body** must have 72 characters or less.

### Possible combinations

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

## Recommendations

- Try to itemize your commit body:
    ```
    - Add feature X in file Y
    - Run script Z
    - Remove file A with B purpose
    ```

- Do **not** use the word '**part**' for splitting commits or MRs for a single issue. Use **#[issue-number]{.issue-part}** instead as shown in [Example](#Example)

## Example

Here is an example of a compliant commit message (Notice how the issue has a '**.1**' right after, meaning that such commit is the part 1 for solving the issue):

```
integrates\feat(build): #13.1 add type_check

- Add type_check function
- Remove unnecessary print_output function
```

## Merge Request Messages

### Differences with commit messages

Merge Request commits are like commit messages with only three differences:

1. Merge Request [type] has to be the most relevant type of all its commits. The relevance list is:
    ```
    rever
    feat
    perf
    fix
    refac
    test
    style
    sol
    ```
    Where ``revert`` has the highest and ``sol`` the lowest relevance.
    
    For example, if your MR has one ``feat``, one ``test`` and one ``style`` commit, the [type] of 
    your MR must be ``feat``.
2. They **can** (not mandatory) implement a ``Closes #{issue-number}`` in their footer, which triggers the automatic closing of the referenced issue once the MR gets accepted

### Example

Here is an example of a compliant Merge Request Message:

```
integrates\feat(build): #13.3 new checks to dangerfile

- Add type_check
- Add deltas_check
- Add commit_number check

Closes #13
```

Issue number 13 will be automatically closed once this MR is accepted due to the ``Closes #13`` footer.
