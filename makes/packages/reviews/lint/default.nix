{ makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envSrcReviews = path "/reviews/src";
  };
  builder = path "/makes/packages/reviews/lint/builder.sh";
  name = "reviews-lint";
  searchPaths = {
    envSources = [ packages.reviews.runtime ];
    envUtils = [ "/makes/utils/lint-python" ];
  };
}
