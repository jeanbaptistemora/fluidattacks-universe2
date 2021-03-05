{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  searchPaths = {
    envSources = [ packages.reviews.runtime ];
  };
  name = "reviews";
  template = path "/makes/applications/reviews/entrypoint.sh";
}
