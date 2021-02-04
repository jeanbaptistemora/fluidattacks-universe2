{ integratesPkgs
, outputs
, path
, ...
} @ _:
let
  ociDeploy = import (path "/makes/utils/oci-deploy") path integratesPkgs;
in
ociDeploy {
  oci = outputs.packages."integrates/storage/oci";
  name = "integrates-storage-oci-deploy";
  registry = "registry.gitlab.com";
  tag = "fluidattacks/product/integrates/storage:$CI_COMMIT_REF_NAME";
}
