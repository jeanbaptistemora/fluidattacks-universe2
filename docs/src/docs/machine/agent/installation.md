---
id: installation
title: DevSecOps Installation
sidebar_label: Installation
slug: /machine/agent/installation
---

You can use the DevSeCops agent
on any [x86_64](https://en.wikipedia.org/wiki/X86-64)
machine in which [Docker](https://www.docker.com/) is installed.
You can also integrate the agent
into your `CI/CD` to ensure
that your software is built and shipped
without previously reported vulnerabilities
in our _ARM_.

To install the agent
you need to do the following:

1. Make sure you have
   a DevSecOps agent token.

   This token can be generated
   in our ARM scope section
   (Organization>Groups>GroupName>Scope),
   where you will find
   the DevSecOps Agent Token section.

![DevSevOps Generation Section](https://res.cloudinary.com/fluid-attacks/image/upload/v1663687225/docs/machine/agent/installation/dev_token_section.png)

Click on the **Manage Token** button
and a pop-up will appear
where you can **Generate** the token
or click on **Reveal Token**
in case you already generated one.

![DevSevOps Generation Modal](https://res.cloudinary.com/fluid-attacks/image/upload/v1663687225/docs/machine/agent/installation/manage_toke.png)

> **Note:** The DevSecOps token is valid for 180 days.

1. Make sure your execution environment
   has the required dependencies:
   - Docker (>= 20.10.10)
1. Install docker by following
   the official guide:
   - <https://docs.docker.com/engine/install/>.

## Options

- `--token`: Your DevSecOps agent token (required).
- `--dynamic / --static`: Check for only DAST / SAST vulnerabilities
  respectively (optional).
- `--verbose`: Declare the level of detail of the report (default `vvv`).
  - `v`: Show only the number of vulnerable, safe and accepted finds.
  - `vv`: Show only vulnerable finds.
  - `vvv`: Show vulnerable and safe finds.
  - `vvvv`: Show vulnerable, safe and accepted finds.
  - You can use `-v`, `-vv`, `-vvv`, `-vvvv`.
- `--strict / --lax`: Run forces in strict mode (default `--lax`).
- `--repo-name`: Git repository name (optional).
- `--breaking`: Strict mode severity customization.
  Vulnerable finds
  with a severity below this threshold
  will not break the pipeline.
  This option takes values
  between 0.0 (recommended) all the way up to 10.0 (optional).

Note: Strict mode customization like severity thresholds
and grace periods for new vulnerabilities
can also be set in the ARM organization's Policies tab.
In the case of `--breaking`,
the value passed to this CLI option takes
precedence over the value set in ARM.

## Examples

:::tip
The `--rm` and
`--ti` parameters are optional.
Thus, you can define the best way according to your context.
:::

Run the Docker image:

1. Pull the container image:

   ```sh
   docker pull fluidattacks/forces:new
   ```

1. Run the container image, for instance:

   - To check `all` finds including static and dynamic:

     ```sh
     docker run --rm -ti fluidattacks/forces:new forces --token <your-token> -vvv
     ```

   - To check only `static` vulnerabilities:

     ```sh
     docker run --rm -ti fluidattacks/forces:new forces --static --strict --token <your-token>
     ```

   - To check only `dynamic` vulnerabilities:

     ```sh
     docker run --rm -ti fluidattacks/forces:new forces --dynamic --strict --token <your-token>
     ```

   - To break the pipeline only if vulnerable finds
     with a severity above 4.5 are found:

     ```sh
     docker run --rm -ti fluidattacks/forces:new forces --dynamic --strict --token <your-token> --breaking 4.5
     ```

## Examples in some CI\CD

In `GitLab` add these lines to your `.gitlab-ci.yml`

```yaml
forces:
  image:
    name: fluidattacks/forces:new
  script:
    - forces --token <your-token> --strict --repo-name <repository name>
```

In `Azure DevOps` add these lines to you configuration file:

```yaml
jobs:
  - forces:
    container: fluidattacks/forces:new
    options: --volume "$PWD:/src"
    steps:
    - bash: forces --token <your-token> --repo-name <repository name>
```

In `Jenkins`, the configuration file should look like this:

```groovy
pipeline {
  agent {
    label 'label'
  }
  environment {
    TOKEN = "test"
  }
  stages {
    stage('Forces') {
      steps {
        script {
          sh """
            docker pull fluidattacks/forces:new
            docker run --volume "$PWD:/src" fluidattacks/forces:new forces --token ${TOKEN} --repo-name <repository name>
          """
        }
      }
    }
  }
}
```

## Troubleshooting

1. Please make sure that your Docker engine version is >= 20.10.10.

   ```sh
   $ docker --version

   Docker version 20.10.10, build v20.10.10
   ```

   This is important because the agent
   uses a [GNU libc](https://www.gnu.org/software/libc/) version >= 2.34,
   and the
   default [seccomp](https://en.wikipedia.org/wiki/Seccomp) profile
   of Docker <= 20.10.9
   [is not adjusted to support the clone syscall](https://github.com/moby/moby/blob/v20.10.9/profiles/seccomp/default.json)
   of GNU libc
   [introduced in version 2.34](https://sourceware.org/git/?p=glibc.git;a=commit;h=d8ea0d0168b190bdf138a20358293c939509367f).

1. Please check that your Docker installation is working.

   If it is, you should be able to run a Hello World:

   ```sh
   $ docker run hello-world

   Hello from Docker!
   This message shows that your installation appears to be working correctly.
   ...
   ```

   Otherwise,
   please refer to the Docker documentation
   and the Docker installation steps.

1. If after following the steps above
   you still experience issues running the agent,
   feel free to contact us at [help@fluidattacks.com](mailto:help@fluidattacks.com)
   and we'll do our best to help.

   Please include in the report as much information as possible
   to help us reproduce the problem, for example:

   - The Docker Engine and Server version: `$ docker info`.
   - The host fingerprint: `$ uname -a`.
   - The value of `$ docker inspect fluidattacks/forces:new`.
   - The organization, group, and repository name you are executing the agent on.
