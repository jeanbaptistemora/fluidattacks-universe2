{ nixpkgs
, path
, ...
}:
let
  dockerBuild = import (path "/makes/utils/docker-build") path nixpkgs;
in
dockerBuild {
  context = ".";
  name = "makes-deploy-oci-batch";
  tag = "registry.gitlab.com/fluidattacks/product/makes:batch";
}
