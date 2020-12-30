attrs @ {
  commonPkgs,
  ...
}:

let
  dockerBuild = import ../../../../makes/utils/bash-lib/docker-build commonPkgs;
in
  dockerBuild {
    context = ../../../../makes/common/deploy/oci-ci/context;
    name = "common-deploy-oci-ci";
    tag = "registry.gitlab.com/fluidattacks/product/makes:ci";
  }
