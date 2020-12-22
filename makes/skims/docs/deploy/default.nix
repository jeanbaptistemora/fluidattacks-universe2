attrs @ {
  outputs,
  pkgsSkims,
  ...
}:

let
  makeEntrypoint = import ../../../../makes/utils/make-entrypoint pkgsSkims;
in
  makeEntrypoint {
    arguments = {
      envSkimsDocsBuild = outputs.packages.skims-docs-build;
      envShell = "${pkgsSkims.bash}/bin/bash";
      envAwscli = "${pkgsSkims.awscli}/bin/aws";
    };
    location = "/bin/skims-docs-deploy";
    name = "skims-docs-deploy";
    template = ../../../../makes/skims/docs/deploy/entrypoint.sh;
  }
