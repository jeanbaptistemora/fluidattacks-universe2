{ makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envReviewsRuntime = packages.reviews.runtime;
    envSrcReviews = path "/reviews/src/";
  };
  builder = path "/makes/packages/reviews/lint/builder.sh";
  name = "reviews-lint";
  searchPaths = {
    envUtils = [ "/makes/utils/lint-python" ];
  };
}
