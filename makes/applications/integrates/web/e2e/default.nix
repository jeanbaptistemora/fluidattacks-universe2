{ integratesPkgs
, packages
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path integratesPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path integratesPkgs;
in
makeEntrypoint {
  arguments = {
    envFirefox = integratesPkgs.firefox;
    envGeckodriver = integratesPkgs.geckodriver;
    envSearchPaths = makeSearchPaths [
      packages."integrates/web/e2e/pypi"
    ];
    envUtilsAws = import (path "/makes/utils/aws") path integratesPkgs;
    envUtilsSops = import (path "/makes/utils/sops") path integratesPkgs;
  };
  name = "integrates-web-e2e";
  template = path "/makes/applications/integrates/web/e2e/entrypoint.sh";
}
