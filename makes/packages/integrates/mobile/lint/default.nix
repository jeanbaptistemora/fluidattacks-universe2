{ integratesPkgs
, path
, ...
} @ attrs:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path integratesPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path integratesPkgs;
in
makeDerivation {
  builder = path "/makes/packages/integrates/mobile/lint/builder.sh";
  envSearchPaths = makeSearchPaths [ integratesPkgs.nodejs-12_x ];
  envSetupIntegratesMobileDevelopment = import (path "/makes/packages/integrates/mobile/config/development") attrs.copy;
  envSetupIntegratesMobileRuntime = import (path "/makes/packages/integrates/mobile/config/runtime") attrs.copy;
  envSrcIntegratesMobile = path "/integrates/mobile";
  envUtilsCommon = path "/makes/utils/common/template.sh";
  name = "integrates-mobile-lint";
}
