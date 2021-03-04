{ airsPkgs
, makeTemplate
, path
, ...
}:
makeTemplate airsPkgs {
  name = "airs-adoc-linter";
  searchPaths = {
    envPaths = [
      airsPkgs.gnugrep
    ];
  };
  template = path "/makes/packages/airs/adoc/linter/template.sh";
}
