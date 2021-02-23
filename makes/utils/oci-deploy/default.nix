path: pkgs:

{ name
, oci
, registry ? "docker.io"
, tag
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path pkgs;
in
makeEntrypoint {
  arguments = {
    envOci = oci;
    envRegistry = registry;
    envTag = "${registry}/${tag}";
  };
  inherit name;
  searchPaths = {
    envPaths = [
      pkgs.skopeo
    ];
  };
  template = path "/makes/utils/oci-deploy/entrypoint.sh";
}
