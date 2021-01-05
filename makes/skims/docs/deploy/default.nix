_ @ {
  outputs,
  skimsPkgs,
  ...
}:

let
  makeEntrypoint = import ../../../../makes/utils/make-entrypoint skimsPkgs;
in
  makeEntrypoint {
    arguments = {
      envSkimsDocsBuild = outputs.packages.skims-docs-build;
      envUtilsBashLibAws = import ../../../../makes/utils/bash-lib/aws skimsPkgs;
    };
    location = "/bin/skims-docs-deploy";
    name = "skims-docs-deploy";
    template = ../../../../makes/skims/docs/deploy/entrypoint.sh;
  }
