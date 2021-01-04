pkgs:

{
  context,
  name,
  tag,
}:

let
  makeEntrypoint = import ../../../../makes/utils/make-entrypoint pkgs;
in
  makeEntrypoint {
    arguments = {
      envDocker = "${pkgs.docker}/bin/docker";
      envDockerContext = context;
      envTag = tag;
    };
    location = "/bin/${name}";
    name = name;
    template = ../../../../makes/utils/bash-lib/docker-build/entrypoint.sh;
  }
