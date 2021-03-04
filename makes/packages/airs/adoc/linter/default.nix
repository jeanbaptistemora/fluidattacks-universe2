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
      airsPkgs.pcre
    ];
  };
  template = path "/makes/packages/airs/adoc/linter/template.sh";
}
