# https://github.com/fluidattacks/makes
{ config
, outputs
, ...
}:
{
  deployContainerImage = {
    images = {
      makesProd = {
        src = config.inputs.product.makes-oci;
        registry = "registry.gitlab.com";
        tag = "fluidattacks/product/makes:latest";
      };
    };
  };
  deployTerraform = {
    modules = {
      makesCi = {
        authentication = [ outputs."/secretsForAwsFromEnv/makesProd" ];
        src = "/makes/applications/makes/ci/src/terraform";
        version = "0.13";
      };
    };
  };
  formatBash = {
    enable = true;
    targets = [ "/" ];
  };
  formatNix = {
    enable = true;
    targets = [ "/" ];
  };
  formatPython = {
    enable = true;
    targets = [ "/" ];
  };
  formatTerraform = {
    enable = true;
    targets = [ "/" ];
  };
  lintBash = {
    enable = true;
    targets = [ "/" ];
  };
  lintNix = {
    enable = true;
    targets = [ "/" ];
  };
  lintTerraform = {
    modules = {
      makesCi = {
        authentication = [ outputs."/secretsForAwsFromEnv/makesDev" ];
        src = "/makes/applications/makes/ci/src/terraform";
        version = "0.13";
      };
    };
  };
  secretsForAwsFromEnv = {
    makesDev = {
      accessKeyId = "MAKES_DEV_AWS_ACCESS_KEY_ID";
      secretAccessKey = "MAKES_DEV_AWS_SECRET_ACCESS_KEY";
    };
    makesProd = {
      accessKeyId = "MAKES_PROD_AWS_ACCESS_KEY_ID";
      secretAccessKey = "MAKES_PROD_AWS_SECRET_ACCESS_KEY";
    };
  };
  testTerraform = {
    modules = {
      makesCi = {
        authentication = [ outputs."/secretsForAwsFromEnv/makesDev" ];
        src = "/makes/applications/makes/ci/src/terraform";
        version = "0.13";
      };
    };
  };
}
