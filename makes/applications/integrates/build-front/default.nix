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
    envSearchPaths = makeSearchPaths [ integratesPkgs.nodejs ];
    envSetupIntegratesDevelopmentFront = import (path "/makes/packages/integrates/config-development/front") attrs.copy;
    envSetupIntegratesRuntimeFront = import (path "/makes/packages/integrates/config-runtime/front") attrs.copy;
  };
  name = "integrates-build-front";
  template = path "/makes/applications/integrates/build-front/entrypoint.sh";
}
