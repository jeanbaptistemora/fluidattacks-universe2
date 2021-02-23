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
    envConmon = "${pkgs.conmon}/bin/conmon";
    envOci = oci;
    envPodman = "${pkgs.podman}/bin/podman";
    envRegistry = registry;
    envRunc = "${pkgs.runc}/bin/runc";
    envTag = "${registry}/${tag}";
  };
  inherit name;
  searchPaths = {
    envPaths = [
      pkgs.utillinux
    ];
  };
  template = path "/makes/utils/oci-deploy/entrypoint.sh";
}
