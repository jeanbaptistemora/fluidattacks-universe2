{ integratesPkgs
, path
, ...
} @ attrs:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path integratesPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path integratesPkgs;
in
makeEntrypoint {
  arguments = {
    envSearchPaths = makeSearchPaths [
      integratesPkgs.nodejs
      integratesPkgs.patch
    ];
    envSetupIntegratesDevelopmentFront = import (path "/makes/packages/integrates/front/config/development") attrs.copy;
    envSetupIntegratesRuntimeFront = import (path "/makes/packages/integrates/front/config/runtime") attrs.copy;
  };
  name = "integrates-front-build";
  template = path "/makes/applications/integrates/front/build/entrypoint.sh";
}
