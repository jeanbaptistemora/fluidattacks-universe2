{ outputs
, path
, skimsPkgs
, ...
} @ _:
let
  ociDeploy = import (path "/makes/utils/bash-lib/oci-deploy") skimsPkgs;
in
ociDeploy {
  oci = outputs.packages.skims-oci-build;
  name = "skims-oci-deploy";
  registry = "gitlab";
  tag = "registry.gitlab.com/fluidattacks/product/skims";
}
