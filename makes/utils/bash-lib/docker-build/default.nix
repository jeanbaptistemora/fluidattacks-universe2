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
  location = "/bin/${name}";
  inherit name;
  template = path "/makes/utils/bash-lib/docker-build/entrypoint.sh";
}
