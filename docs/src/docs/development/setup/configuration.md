---
id: configuration
title: Last Step
sidebar_label: configuration
slug: /development/setup/configuration
---

You have almost finished the configuration.

1. Install sops:

   ```bash
   nix-env -i sops
   ```

1. Configure the mailmap, adding your name to the file
   Look file in the root folder of the repository as
   `.mailmap`.

With these steps you have finished the configuration.

The last step is loading to change to the repository.

1. You will receive issue.

1. Read and work it out.

1. When you have resolved issue, add the file
   make a commit following the syntax rules
   specified in the [guide](https://docs.fluidattacks.com/development/stack/commitlint).

1. Check if the commit message is valid:

   ```bash
   m . /lintGitCommitMsg
   ```

1. Push your commit to the repository.

1. If the pipeline fails, you must enter the job that failed and fix it.

1. If the pipeline is correct, you can make a merge request.

1. You can approve the merge request when it passes the pipeline.
