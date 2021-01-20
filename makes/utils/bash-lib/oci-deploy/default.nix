pkgs:

{ name
, oci
, registry
, tag
}:
let
  makeEntrypoint = import ../../../../makes/utils/make-entrypoint pkgs;
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
  template = ../../../../makes/utils/bash-lib/oci-deploy/entrypoint.sh;
}
