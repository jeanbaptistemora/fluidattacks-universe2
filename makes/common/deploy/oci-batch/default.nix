attrs @ {
  pkgsCommon,
  ...
}:

let
  dockerBuild = import ../../../../makes/utils/bash-lib/docker-build pkgsCommon;
in
  dockerBuild {
    context = ".";
    name = "common-deploy-oci-batch";
    tag = "registry.gitlab.com/fluidattacks/product/makes:batch";
  }
