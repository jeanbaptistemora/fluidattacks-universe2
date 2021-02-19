{ integratesPkgs
, packages
, path
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path integratesPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths-deprecated") path integratesPkgs;
in
makeDerivation {
  arguments = {
    envSearchPaths = makeSearchPaths [ integratesPkgs.nodejs-12_x ];
    envSetupIntegratesMobileDevRuntime = packages.integrates.mobile.config.dev-runtime;
    envSrcIntegratesMobile = path "/integrates/mobile";
    envUtilsCommon = path "/makes/utils/common/template.sh";
  };
  builder = path "/makes/packages/integrates/mobile/lint/builder.sh";
  name = "integrates-mobile-lint";
  searchPaths = {
    envPaths = [ integratesPkgs.bash ];
  };
}
