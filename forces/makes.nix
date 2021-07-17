# https://github.com/fluidattacks/makes
{ config
, ...
}:
{
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
}
