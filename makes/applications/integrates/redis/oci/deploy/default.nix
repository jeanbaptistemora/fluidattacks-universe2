{ integratesPkgs
, outputs
, path
, ...
} @ _:
let
  ociDeploy = import (path "/makes/utils/oci-deploy") path integratesPkgs;
in
ociDeploy {
  oci = outputs.packages."integrates/redis/oci/build";
  name = "integrates-redis-oci-deploy";
  registry = "registry.gitlab.com";
  tag = "fluidattacks/product/integrates/redis:$CI_COMMIT_REF_NAME";
}
