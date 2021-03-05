{ airsPkgs
, makeDerivation
, path
, ...
}:
makeDerivation {
  arguments = {
    envAirs = path "/airs";
  };
  builder = path "/makes/packages/airs/test/images/format/builder.sh";
  name = "airs-test-images-format";
  searchPaths = {
    envPaths = [
      airsPkgs.file
      airsPkgs.findutils
      airsPkgs.gnugrep
    ];
  };
}
