{ makesPkgs
, path
, ...
} @ _:
let
  dockerBuild = import (path "/makes/utils/bash-lib/docker-build") path makesPkgs;
in
dockerBuild {
  context = path "/makes/makes/deploy/oci-ci/context";
  name = "makes-deploy-oci-ci";
  tag = "registry.gitlab.com/fluidattacks/product/makes:ci";
}
