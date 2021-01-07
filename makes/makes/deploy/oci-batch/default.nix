{ makesPkgs
, ...
} @ _:
let
  dockerBuild = import ../../../../makes/utils/bash-lib/docker-build makesPkgs;
in
dockerBuild {
  context = ".";
  name = "makes-deploy-oci-batch";
  tag = "registry.gitlab.com/fluidattacks/product/makes:batch";
}
