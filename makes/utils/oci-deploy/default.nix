path: pkgs:

{ name
, oci
, registry
, tag
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path pkgs;
in
makeEntrypoint {
  arguments = {
    envDocker = "${pkgs.docker}/bin/docker";
    envOci = oci;
    envRegistry = registry;
    envTag = tag;
  };
  inherit name;
  template = path "/makes/utils/oci-deploy/entrypoint.sh";
}
