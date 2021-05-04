---
id: installation
title: DevSecOps Installation
sidebar_label: Installation
slug: /machine/agent/installation
---

You can use the DevSeCops agent on any OS that Docker can run on.
You can also integrate the agent into your `CI/CD`
to ensure that your software is built and shipped
without previously reported vulnerabilities in our *ASM*.
In order to install the agent you need to do the following:

**1.** Make sure you own an DevSecOps agent token.
This token can be generated in our ASM scope section
(Organization>Groups>GroupName>Scope),
where you will find the DevSecOps Agent Token section.

![DevSevOps Generation Section](/img/machine/agent/installation/devsecops_token_section.png)

Click on the **Manage Token** button and a pop-up will appear
where you can **Generate** the token or click on **Reveal Token**
in case you already generated one.

![DevSevOps Generation Modal](/img/machine/agent/installation/devsecops_token_modal.png)

**2.** Make sure your execution environment has the required dependencies:
    - Docker
**3.** Install docker by following the official guide:
    - https://docs.docker.com/engine/install/
**4.** Having Docker installed, pull the image:
`docker pull fluidattacks/forces:new`.

## Options

* `--token`: Your DevSecOps agent token [required].
* `--dynamic / --static`: Run only DAST / SAST vulnerabilities. (optional)
* `--verbose <number>`: Declare the level of detail of the report (default 3)
    - `1`: Show only the number of open, closed and accepted vulnerabilities.
    - `2`: Show only open vulnerabilities.
    - `3`: Show open and closed vulnerabilities.
    - `4`: Show open, closed and accepted vulnerabilities.
    - You can use `-v`, `-vv`, `-vvv`, `-vvvv` instead of `--verbose`.
* `--strict / --lax`: Run forces in strict mode (default `--lax`).
* `--repo-path`: Git repository path (optional)

## Examples

Run the Docker image:

1. To check `all` vulnerabilities including static and dynamic
    - `docker run --rm fluidattacks/forces:new forces --token <your-token>`.
1. To check only `static` vulnerabilities
    - `docker run --rm fluidattacks/forces:new forces --static --strict --token <your-token>`.
1. To check only `dynamyc` vulnerabilities
    - `docker run --rm fluidattacks/forces:new forces --dynamic --strict --token <your-token>`.
