---
id: installation
title: DevSecOps Installation
sidebar_label: Installation
slug: /machine/agent/installation
---

You can use the DevSeCops agent
on any OS that Docker can run on.
You can also integrate the agent
into your `CI/CD` to ensure
that your software is built and shipped
without previously reported vulnerabilities
in our *ASM*.
In order to install the agent
you need to do the following:

1. Make sure you own
  an DevSecOps agent token.
  This token can be generated
  in our ASM scope section
  (Organization>Groups>GroupName>Scope),
  where you will find
  the DevSecOps Agent Token section.

  ![DevSevOps Generation Section](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211894/docs/machine/agent/installation/devsecops_token_section_jpex40.webp)

  Click on the **Manage Token** button
  and a pop-up will appear
  where you can **Generate** the token
  or click on **Reveal Token**
  in case you already generated one.

  ![DevSevOps Generation Modal](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211889/docs/machine/agent/installation/devsecops_token_modal_ivw8th.webp)

1. Make sure your execution environment
  has the required dependencies:
    - Docker
1. Install docker by following
  the official guide:
    - https://docs.docker.com/engine/install/
1. Having Docker installed,
  pull the image:
  `docker pull fluidattacks/forces:new`.

## Options

- `--token`: Your DevSecOps agent token [required].
- `--dynamic / --static`: Run only DAST / SAST vulnerabilities. (optional)
- `--verbose`: Declare the level of detail of the report (default vvv)
    - `v`: Show only the number of open,
    closed and accepted vulnerabilities.
    - `vv`: Show only open vulnerabilities.
    - `vvv`: Show open and closed vulnerabilities.
    - `vvvv`: Show open, closed
    and accepted vulnerabilities.
    - You can use `-v`, `-vv`, `-vvv`, `-vvvv`.
- `--strict / --lax`: Run forces in strict mode (default `--lax`).
- `--repo-name`: Git repository name (optional)

## Examples

Run the Docker image:

1. To check `all` vulnerabilities
  including static and dynamic
    - `docker run --rm -ti fluidattacks/forces:new
    forces --token <your-token> -vvv`.
1. To check only `static` vulnerabilities
    - `docker run --rm -ti fluidattacks/forces:new
    forces --static --strict --token <your-token>`.
1. To check only `dynamic` vulnerabilities
    - `docker run --rm -ti fluidattacks/forces:new
    forces --dynamic --strict --token <your-token>`.
