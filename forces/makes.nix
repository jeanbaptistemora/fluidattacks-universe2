# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# https://github.com/fluidattacks/forces
{
  makeSearchPaths,
  outputs,
  projectPath,
  ...
}: {
  imports = [
    ./pipeline/makes.nix
  ];
  dev = {
    forces = {
      source = [
        outputs."/forces/config/development"
        outputs."/forces/config/runtime"
        (makeSearchPaths {
          pythonPackage = ["$PWD/forces"];
        })
      ];
    };
  };
  deployContainerImage = {
    images = {
      forcesDev = {
        credentials = {
          token = "DOCKER_HUB_PASS";
          user = "DOCKER_HUB_USER";
        };
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/forcesDev"
        ];
        src = outputs."/forces/container";
        registry = "docker.io";
        tag = "fluidattacks/forces:$CI_COMMIT_REF_NAME";
      };
      forcesProd = {
        credentials = {
          token = "DOCKER_HUB_PASS";
          user = "DOCKER_HUB_USER";
        };
        setup = [
          outputs."/secretsForAwsFromGitlab/prodForces"
          outputs."/secretsForEnvFromSops/forcesProd"
        ];
        src = outputs."/forces/container";
        registry = "docker.io";
        tag = "fluidattacks/forces:new";
      };
    };
  };
  lintPython = {
    modules = {
      forces = {
        searchPaths.source = [
          outputs."/forces/config/runtime"
          outputs."/forces/config/typing-stubs"
        ];
        python = "3.8";
        src = "/forces/forces";
      };
      forcesTests = {
        searchPaths.source = [
          outputs."/forces/config/development"
          outputs."/forces/config/runtime"
          outputs."/forces/config/typing-stubs"
        ];
        python = "3.8";
        src = "/forces/test";
      };
    };
  };
  secretsForAwsFromGitlab = {
    prodForces = {
      roleArn = "arn:aws:iam::205810638802:role/prod_forces";
      duration = 3600;
    };
  };
  secretsForEnvFromSops = {
    forcesDev = {
      vars = ["DOCKER_HUB_PASS" "DOCKER_HUB_USER"];
      manifest = "/forces/secrets-dev.yaml";
    };
    forcesProd = {
      vars = ["DOCKER_HUB_PASS" "DOCKER_HUB_USER"];
      manifest = "/forces/secrets-prod.yaml";
    };
  };
  dynamoDb = {
    forces = {
      host = "127.0.0.1";
      port = "8022";
      infra = projectPath "/integrates/db/dynamodb/infra";
      data = [
        (projectPath "/forces/test/data")
      ];
    };
  };
}
