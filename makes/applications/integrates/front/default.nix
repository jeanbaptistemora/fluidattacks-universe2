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
    envSearchPaths = makeSearchPaths [ integratesPkgs.nodejs ];
    envSetupIntegratesFrontDevRuntime = import (path "/makes/packages/integrates/front/config/dev-runtime") attrs.copy;
  };
  name = "integrates-front";
  template = path "/makes/applications/integrates/front/entrypoint.sh";
}
