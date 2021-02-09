{ integratesPkgs
, path
, ...
} @ attrs:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path integratesPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path integratesPkgs;
in
makeDerivation {
  builder = path "/makes/packages/integrates/mobile/test/builder.sh";
  envBashLibCommon = path "/makes/utils/common/template.sh";
  envSearchPaths = makeSearchPaths [ integratesPkgs.nodejs-12_x ];
  envSetupIntegratesMobileDevRuntime = import (path "/makes/packages/integrates/mobile/config/dev-runtime") attrs.copy;
  envSrcIntegratesMobile = path "/integrates/mobile";
  name = "integrates-mobile-test";
}
