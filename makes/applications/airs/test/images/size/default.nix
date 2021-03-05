{ nixpkgs
, makeEntrypoint
, path
, ...
}:
makeEntrypoint {
  name = "airs-test-images-size";
  searchPaths = {
    envPaths = [
      nixpkgs.gnugrep
      nixpkgs.optipng
    ];
    envUtils = [
      "/makes/utils/git"
    ];
  };
  template = path "/makes/applications/airs/test/images/size/entrypoint.sh";
}
