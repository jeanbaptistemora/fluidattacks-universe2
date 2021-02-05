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
    envSetupIntegratesDevelopmentFront = import (path "/makes/packages/integrates/front/config/development") attrs.copy;
    envSetupIntegratesRuntimeFront = import (path "/makes/packages/integrates/front/config/runtime") attrs.copy;
  };
  name = "integrates-front";
  template = path "/makes/applications/integrates/front/entrypoint.sh";
}
