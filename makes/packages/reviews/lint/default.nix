{ makeDerivation
, path
, reviewsPkgs
, ...
} @ attrs:
makeDerivation reviewsPkgs {
  builder = path "/makes/packages/reviews/lint/builder.sh";
  envUtilsLintPython = import (path "/makes/utils/lint-python") path reviewsPkgs;
  envReviewsRuntime = import (path "/makes/packages/reviews/runtime") attrs.copy;
  envSrcReviews = path "/reviews/src/";
  name = "reviews-lint";
}
