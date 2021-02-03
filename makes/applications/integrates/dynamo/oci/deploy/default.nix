{ integratesPkgs
, outputs
, path
, ...
} @ _:
let
  ociDeploy = import (path "/makes/utils/oci-deploy") path integratesPkgs;
in
ociDeploy {
  oci = outputs.packages."integrates/dynamo/oci";
  name = "integrates-dynamo-oci-deploy";
  registry = "registry.gitlab.com";
  tag = "fluidattacks/product/integrates/dynamo:$CI_COMMIT_REF_NAME";
}
