{ makesPkgs
, ...
} @ _:
let
  dockerBuild = import ../../../../makes/utils/bash-lib/docker-build makesPkgs;
in
dockerBuild {
  context = ../../../../makes/makes/deploy/oci-ci/context;
  name = "makes-deploy-oci-ci";
  tag = "registry.gitlab.com/fluidattacks/product/makes:ci";
}
