# https://github.com/fluidattacks/forces
{ outputs
, projectPath
, ...
}:
{
  imports = [
    ./dev/makes.nix
    ./pipeline/makes.nix
  ];
  deployContainerImage = {
    images = {
      forcesDev = {
        credentials = {
          token = "DOCKER_HUB_PASS";
          user = "DOCKER_HUB_USER";
        };
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
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
          outputs."/secretsForAwsFromEnv/prodForces"
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
          outputs."/forces/config-runtime"
        ];
        python = "3.8";
        src = "/forces/forces";
      };
      forcesTests = {
        searchPaths.source = [
          outputs."/forces/config-development"
          outputs."/forces/config-runtime"
        ];
        python = "3.8";
        src = "/forces/test";
      };
    };
  };
  secretsForAwsFromEnv = {
    prodForces = {
      accessKeyId = "PROD_FORCES_AWS_ACCESS_KEY_ID";
      secretAccessKey = "PROD_FORCES_AWS_SECRET_ACCESS_KEY";
      sessionToken = "AWS_SESSION_TOKEN";
    };
  };
  secretsForEnvFromSops = {
    forcesDev = {
      vars = [ "DOCKER_HUB_PASS" "DOCKER_HUB_USER" ];
      manifest = "/forces/secrets-dev.yaml";
    };
    forcesProd = {
      vars = [ "DOCKER_HUB_PASS" "DOCKER_HUB_USER" ];
      manifest = "/forces/secrets-prod.yaml";
    };
  };
  dynamoDb = {
    forces = {
      host = "127.0.0.1";
      port = "8022";
      infra = projectPath "/makes/foss/units/integrates/db/infra";
      data = [
        (projectPath "/forces/test/data")
      ];
    };
  };
}
