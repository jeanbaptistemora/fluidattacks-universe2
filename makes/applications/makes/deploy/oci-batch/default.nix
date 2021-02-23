{ makesPkgs
, path
, ...
}:
let
  dockerBuild = import (path "/makes/utils/docker-build") path makesPkgs;
in
dockerBuild {
  context = ".";
  name = "makes-deploy-oci-batch";
  tag = "registry.gitlab.com/fluidattacks/product/makes:batch";
}
