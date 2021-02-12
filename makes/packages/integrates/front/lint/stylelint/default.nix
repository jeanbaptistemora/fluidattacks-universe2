{ integratesPkgs
, path
, ...
} @ attrs:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path integratesPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths-deprecated") path integratesPkgs;
in
makeDerivation {
  builder = path "/makes/packages/integrates/front/lint/stylelint/builder.sh";
  envBashLibCommon = path "/makes/utils/common/template.sh";
  envSearchPaths = makeSearchPaths [ integratesPkgs.nodejs ];
  envSetupIntegratesFrontDevRuntime = import (path "/makes/packages/integrates/front/config/dev-runtime") attrs.copy;
  envSrcIntegratesFront = path "/integrates/front";
  name = "integrates-front-lint-stylelint";
}
