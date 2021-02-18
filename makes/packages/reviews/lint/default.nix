{ makeDerivation
, packages
, path
, reviewsPkgs
, ...
} @ _:
makeDerivation reviewsPkgs {
  builder = path "/makes/packages/reviews/lint/builder.sh";
  envUtilsLintPython = import (path "/makes/utils/lint-python") path reviewsPkgs;
  envReviewsRuntime = packages.reviews.runtime;
  envSrcReviews = path "/reviews/src/";
  name = "reviews-lint";
}
