{ integratesPkgs
, outputs
, path
, ...
} @ _:
let
  ociDeploy = import (path "/makes/utils/oci-deploy") path integratesPkgs;
in
ociDeploy {
  oci = outputs.packages."integrates/build/oci/redis";
  name = "integrates-deploy-oci-redis";
  registry = "registry.gitlab.com";
  tag = "fluidattacks/product/integrates/redis:$CI_COMMIT_REF_NAME";
}
