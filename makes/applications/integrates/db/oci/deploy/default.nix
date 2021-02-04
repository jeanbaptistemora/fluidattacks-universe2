{ integratesPkgs
, outputs
, path
, ...
} @ _:
let
  ociDeploy = import (path "/makes/utils/oci-deploy") path integratesPkgs;
in
ociDeploy {
  oci = outputs.packages."integrates/db/oci";
  name = "integrates-db-oci-deploy";
  registry = "registry.gitlab.com";
  tag = "fluidattacks/product/integrates/db:$CI_COMMIT_REF_NAME";
}
