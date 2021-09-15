# https://github.com/fluidattacks/makes
{ inputs
, ...
}:
{
  deployContainerImage = {
    images = {
      makesProd = {
        src = inputs.product.makes-oci;
        registry = "registry.gitlab.com";
        tag = "fluidattacks/product/makes:latest";
      };
    };
  };
  imports = [
    ./ci/makes.nix
    ./compute/makes.nix
    ./criteria/makes.nix
    ./dns/makes.nix
    ./foss/makes.nix
    ./kubernetes/makes.nix
    ./okta/makes.nix
    ./pipeline/makes.nix
    ./secrets/makes.nix
    ./users/makes.nix
    ./vpc/makes.nix
  ];
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
}
