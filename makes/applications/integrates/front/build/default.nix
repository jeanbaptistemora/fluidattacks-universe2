{ integratesPkgs
, path
, ...
} @ attrs:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path integratesPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths-deprecated") path integratesPkgs;
in
makeEntrypoint {
  arguments = {
    envSearchPaths = makeSearchPaths [
      integratesPkgs.nodejs
      integratesPkgs.patch
    ];
    envSetupIntegratesFrontDevRuntime = import (path "/makes/packages/integrates/front/config/dev-runtime") attrs.copy;
  };
  name = "integrates-front-build";
  template = path "/makes/applications/integrates/front/build/entrypoint.sh";
}
