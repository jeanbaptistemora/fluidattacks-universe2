{ outputs
, skimsPkgs
, ...
} @ _:
let
  ociDeploy = import ../../../makes/utils/bash-lib/oci-deploy skimsPkgs;
in
ociDeploy {
  oci = outputs.packages.skims-oci-build;
  name = "skims-oci-deploy";
  tag = "registry.gitlab.com/fluidattacks/product/skims";
}
