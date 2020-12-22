attrs @ {
  pkgsCommon,
  ...
}:

let
  makeEntrypoint = import ../../../../makes/utils/make-entrypoint pkgsCommon;
in
  makeEntrypoint {
    arguments = {
      envDocker = "${pkgsCommon.docker}/bin/docker";
      envDockerContext = ../../../../makes/common/deploy/oci/context;
      envShell = "${pkgsCommon.bash}/bin/bash";
    };
    name = "common-deploy-oci";
    template = ../../../../makes/common/deploy/oci/entrypoint.sh;
  }
