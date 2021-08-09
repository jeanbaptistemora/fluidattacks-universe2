# https://github.com/fluidattacks/forces
{ config
, outputs
, ...
}:
{
  imports = [
    ./pipeline/makes.nix
  ];
  deployContainerImage = {
    images = {
      forcesDev = {
        src = config.inputs.product.forces-oci-build;
        registry = "docker.io";
        tag = "fluidattacks/forces:$CI_COMMIT_REF_NAME";
      };
      forcesProd = {
        src = config.inputs.product.forces-oci-build;
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
