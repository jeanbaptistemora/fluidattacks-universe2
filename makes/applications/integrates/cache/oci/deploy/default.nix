{ integratesPkgs
, outputs
, path
, ...
} @ _:
let
  ociDeploy = import (path "/makes/utils/oci-deploy") path integratesPkgs;
in
ociDeploy {
  oci = outputs.packages."integrates/cache/oci";
  name = "integrates-cache-oci-deploy";
  registry = "registry.gitlab.com";
  tag = "fluidattacks/product/integrates/cache:$CI_COMMIT_REF_NAME";
}
