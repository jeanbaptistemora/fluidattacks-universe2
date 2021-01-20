{ outputs
, path
, skimsPkgs
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path skimsPkgs;
in
makeEntrypoint {
  arguments = {
    envSkimsDocsBuild = outputs.packages.skims-docs-build;
    envUtilsBashLibAws = import (path "/makes/utils/bash-lib/aws") path skimsPkgs;
  };
  location = "/bin/skims-docs-deploy";
  name = "skims-docs-deploy";
  template = path "/makes/skims/docs/deploy/entrypoint.sh";
}
