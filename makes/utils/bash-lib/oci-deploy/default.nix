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
  location = "/bin/${name}";
  inherit name;
  template = path "/makes/utils/bash-lib/oci-deploy/entrypoint.sh";
}
