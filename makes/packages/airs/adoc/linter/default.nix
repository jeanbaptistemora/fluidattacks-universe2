{ nixpkgs
, makeTemplate
, path
, ...
}:
makeTemplate {
  name = "airs-adoc-linter";
  searchPaths = {
    envPaths = [
      nixpkgs.diction
      nixpkgs.gnugrep
      nixpkgs.pcre
    ];
  };
  template = path "/makes/packages/airs/adoc/linter/template.sh";
}
