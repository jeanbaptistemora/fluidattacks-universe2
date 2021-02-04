{ integratesPkgs
, outputs
, path
, ...
} @ _:
let
  ociDeploy = import (path "/makes/utils/oci-deploy") path integratesPkgs;
in
ociDeploy {
  oci = outputs.packages."integrates/back/oci";
  name = "integrates-back-oci-deploy";
  registry = "registry.gitlab.com";
  tag = "fluidattacks/product/integrates/back:$CI_COMMIT_REF_NAME";
}
