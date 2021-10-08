# https://github.com/fluidattacks/forces
{ outputs
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
        src = outputs."/forces/container";
        registry = "docker.io";
        tag = "fluidattacks/forces:$CI_COMMIT_REF_NAME";
      };
      forcesProd = {
        src = outputs."/forces/container";
        registry = "docker.io";
        tag = "fluidattacks/forces:new";
      };
    };
  };
  deployTerraform = {
    modules = {
      forces = {
        setup = [ outputs."/secretsForAwsFromEnv/forcesProd" ];
        src = "/forces/infra";
        version = "0.14";
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
  lintTerraform = {
    modules = {
      forces = {
        setup = [ outputs."/secretsForAwsFromEnv/forcesDev" ];
        src = "/forces/infra";
        version = "0.14";
      };
    };
  };
  secretsForAwsFromEnv = {
    forcesDev = {
      accessKeyId = "FORCES_DEV_AWS_ACCESS_KEY_ID";
      secretAccessKey = "FORCES_DEV_AWS_SECRET_ACCESS_KEY";
    };
    forcesProd = {
      accessKeyId = "FORCES_PROD_AWS_ACCESS_KEY_ID";
      secretAccessKey = "FORCES_PROD_AWS_SECRET_ACCESS_KEY";
    };
  };
  testTerraform = {
    modules = {
      forces = {
        setup = [ outputs."/secretsForAwsFromEnv/forcesDev" ];
        src = "/forces/infra";
        version = "0.14";
      };
    };
  };
}
