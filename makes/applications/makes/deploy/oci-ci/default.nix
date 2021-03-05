{ nixpkgs
, path
, ...
}:
let
  dockerBuild = import (path "/makes/utils/docker-build") path nixpkgs;
in
dockerBuild {
  context = path "/makes/applications/makes/deploy/oci-ci/context";
  name = "makes-deploy-oci-ci";
  tag = "registry.gitlab.com/fluidattacks/product/makes:ci";
}
