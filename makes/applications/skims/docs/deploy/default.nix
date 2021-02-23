{ packages
, path
, skimsPkgs
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path skimsPkgs;
in
makeEntrypoint {
  arguments = {
    envSkimsDocsBuild = packages.skims.docs.build;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path skimsPkgs;
  };
  name = "skims-docs-deploy";
  template = path "/makes/applications/skims/docs/deploy/entrypoint.sh";
}
