{ outputs
, path
, skimsPkgs
, ...
} @ _:
let
  ociDeploy = import (path "/makes/utils/oci-deploy") path skimsPkgs;
in
ociDeploy {
  oci = outputs.packages.skims-oci-build;
  name = "skims-oci-deploy";
  registry = "gitlab";
  tag = "registry.gitlab.com/fluidattacks/product/skims";
}
