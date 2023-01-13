---
id: onboarding
title: Onboarding
sidebar_label: Onboarding
slug: /development/setup/onboarding
---

Below you will find a list of steps you must do to start

- Receive your Fluid credentials at your registered personal email.
- Attend the induction meeting (via invitation link sent to your
  personal email).
- Configure Okta following the instructions to access your
  corporate email.
- Login with your Fluid credentials to your corporate email.
- Watch Health & Security videos shared with you.
- Setup your email signature.
- Send the presentation email to people@fluidattacks.com
- Send the google sheet with your tentative schedule email to your
  direct manager.
- Create a Gitlab account with your corporate email as suggested by your
  direct manager.

## Configure your machine

1. [Install Linux](https://www.youtube.com/watch?v=ycTh_x-hzro&t=159s).
1. Register with your Fluid Credentials at timedoctor.com
   via invitation link sent to your email).
1. command to run timedoctor on linux:
   export QTWEBENGINE_DISABLE_SANDBOX=1 && ~/timedoctor2/timedoctor2
1. [Install VScode](https://code.visualstudio.com/download).
1. [Install Git](https://docs.gitlab.com/ee/topics/git/how_to_install_git/index.html).
1. [Create key ssh](https://docs.gitlab.com/ee/user/ssh.html).
1. Configure key in your Gitlab.
1. Clone repository with ssh.
1. when the repository cloning is complete enter the root folder

```sh
cd universe
```

1. [Configure Git Username and Email](https://linuxize.com/post/how-to-configure-git-username-and-email/).
1. [Create a GPG key and configure the key in your Gitlab](https://docs.gitlab.com/ee/user/project/repository/gpg_signed_commits/).
1. [Install nix](https://nixos.org/download.html). Choose Single user installation
1. Install makes with this command
   nix-env -if https://github.com/fluidattacks/makes/archive/22.11.tar.gz
1. [Read the guide to do a local test with makes](https://docs.fluidattacks.com/development/stack/makes/).
