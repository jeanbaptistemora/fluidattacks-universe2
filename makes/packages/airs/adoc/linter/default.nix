{ nixpkgs
, makeTemplate
, path
, ...
}:
makeTemplate {
  arguments = {
    envAcceptedKeywordsFile = path "/makes/packages/airs/adoc/linter/acepted_keywords.lst";
  };
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
