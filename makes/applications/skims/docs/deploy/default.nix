{ packages
, path
, nixpkgs
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs;
in
makeEntrypoint {
  arguments = {
    envSkimsDocsBuild = packages.skims.docs.build;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path nixpkgs;
  };
  name = "skims-docs-deploy";
  template = path "/makes/applications/skims/docs/deploy/entrypoint.sh";
}
