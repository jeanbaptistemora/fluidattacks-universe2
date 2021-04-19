---
id: merge-requests
title: Merge Requests
sidebar_label: Merge Requests
slug: /development/stack/git/merge-requests
---

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
