path: pkgs:

{ context
, name
, tag
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path pkgs;
in
makeEntrypoint {
  arguments = {
    envDocker = "${pkgs.docker}/bin/docker";
    envDockerContext = context;
    envTag = tag;
  };
  inherit name;
  template = path "/makes/utils/docker-build/entrypoint.sh";
}
