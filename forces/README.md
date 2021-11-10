[![License](https://img.shields.io/pypi/l/skims)](../LICENSE)

You can use forces on any operating system using docker.
You can also integrate forces into your `CI/CD` to ensure that your software is built and shipped without previously reported vulnerabilities in **ASM**.

# Installation

1. Make sure you own an DevSecOps agent token. Follow this [guide](https://docs.fluidattacks.com/machine/agent/installation/) to generate it.
2. Make sure your execution environment has the required dependencies.
   - docker
3. The host machine must have the following permissions:
   - pull docker images
   - run docker containers
   - attach volumes to docker containers
4. Be sure to use forces within a git repository.

# Options

- `--token`: Your DevSecOps agent token [required]
- `-v`, `-vv`, `-vvv`, `-vvvv`: Declare the level of detail of the report (default 3)
  - 1: It only shows the number of open, closed and accepted vulnerabilities
  - 2: Only show open vulnerabilities
  - 3: Show open and closed vulnerabilities
  - 4: Show open, closed and accepted vulnerabilities
- `--strict / --lax`: Run forces in strict mode (default `--lax`)
- `--repo-path`: Git repository path (optional)
- `--repo-name`: Name of the repository in which it is running (nickname in Git Roots)
- `--dynamic`: Only check DAST vulnerabilities
- `--static`: Only check SAST vulnerabilities
- If you do not specify `--dynamic/--static` all vulnerabilities are checked

# Examples

How to use the docker image:
`docker run --rm -ti -v "$PWD:/src" fluidattacks/forces:new forces --token <your-token> --repo-name <repository name>`

_Note_: To run the container you must pass the working repository as a volume to the `/src` directory (`--volume "<path to repo>:/src"`), the path is used to extract information from the repository

## Use in some CI\CD

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


## Development

To run the local tests, the local integrates backend must be deployed.

Run each command in a different terminal:

```bash
m . /integrates/back
m . /integrates/cache
m . /dynamoDb/forces
m . /integrates/storage
```

to run the tests, run the command

```bash
m . /forces/test
```
