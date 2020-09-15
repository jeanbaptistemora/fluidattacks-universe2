[![PyPI](https://img.shields.io/pypi/v/skims)](https://pypi.org/project/skims)
[![Status](https://img.shields.io/pypi/status/skims)](https://pypi.org/project/skims)
[![Downloads](https://img.shields.io/pypi/dm/skims)](https://pypi.org/project/skims)
[![License](https://img.shields.io/pypi/l/skims)](../LICENSE)

You can use forces on any operating system that python can run on, you can see the status of the package in [Pypi](https://pypi.org/project/forces/).
You can also integrate forces into your `CI/CD` to ensure that your software is built and shipped without previously reported vulnerabilities in **integrates**.

# Installation

1. Make sure you own an integrates API token. Follow this [guide](https://community.fluidattacks.com/t/integrates-api-access/540/1) to generate it.
2. Make sure your execution environment has the required dependencies.
   - git
   - python3.8
   - pip
3. Install forces by running the following command:
    - Windows: `python -m pip install forces`
    - Linux and Mac OS: `python3.8 -m pip install forces`
4. You can also make use of the Docker image `docker pull fluidattacks/forces:new`.
5. Be sure to use forces within a git repository.

# Options

- `--token`: Your token for integrates API [required]
- `--verbose <number>`: Declare the level of detail of the report (default 3)
  - 1: It only shows the number of open, closed and accepted vulnerabilities
  - 2: Only show open vulnerabilities
  - 3: Show open and closed vulnerabilities
  - 4: Show open, closed and accepted vulnerabilities
  - You can use `-v`, `-vv`, `-vvv`, `-vvvv` instead of `--verbose`
- `--strict / --lax`: Run forces in strict mode (default `--lax`)
- `--repo-path`: Git repository path (optional)
- `--dynamic`: Only check DAST vulnerabilities
- `--static`: Only check SAST vulnerabilities
- If you do not specify `--dynamic/--static` all vulnerabilities are checked

# Examples

In your local environment you execute:
`forces --token <your-token>`

You can also use the Docker image:
`docker run --rm fluidattacks/forces:new forces --token <your-token>`

## Use in some CI\CD

In `GitLab` add these lines to your `.gitlab-ci.yml`

```yaml
forces:
  image:
    name: fluidattacks/forces:new
    entrypoint: [""]
  script:
    - forces --token <your-token> --strict
```

In `Azure DevOps` add these lines to you configuration file:

```yaml
jobs:
  - forces:
    container: fluidattacks/forces:new
    steps:
    - bash: forces --token <your-token>
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
            docker run fluidattacks/forces:new --token ${TOKEN}
          """
        }
      }
    }
  }
}
```
