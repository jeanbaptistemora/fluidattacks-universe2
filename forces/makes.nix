# https://github.com/fluidattacks/forces
{
  makeSearchPaths,
  outputs,
  ...
}: {
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
        ];
        python = "3.10";
        src = "/forces/forces";
      };
      forcesTests = {
        searchPaths.source = [
          outputs."/forces/config/development"
          outputs."/forces/config/runtime"
        ];
        python = "3.10";
        src = "/forces/test";
      };
    };
  };
  secretsForAwsFromGitlab = {
    prodForces = {
      roleArn = "arn:aws:iam::205810638802:role/prod_integrates";
      duration = 3600;
    };
  };
  secretsForEnvFromSops = {
    forcesDev = {
      vars = ["DOCKER_HUB_PASS" "DOCKER_HUB_USER"];
      manifest = "/integrates/secrets/development.yaml";
    };
    forcesProd = {
      vars = ["DOCKER_HUB_PASS" "DOCKER_HUB_USER"];
      manifest = "/integrates/secrets/production.yaml";
    };
  };
}
