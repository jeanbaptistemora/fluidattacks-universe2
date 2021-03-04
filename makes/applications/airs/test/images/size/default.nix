{ airsPkgs
, makeEntrypoint
, path
, ...
}:
makeEntrypoint airsPkgs {
  name = "airs-test-images-size";
  searchPaths = {
    envPaths = [
      airsPkgs.gnugrep
      airsPkgs.optipng
    ];
    envUtils = [
      "/makes/utils/git"
    ];
  };
  template = path "/makes/applications/airs/test/images/size/entrypoint.sh";
}
