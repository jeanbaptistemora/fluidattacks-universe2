{ inputs
, makeTemplate
, ...
}:
makeTemplate {
  replace = {
    __argAcceptedKeywordsFile__ = ./acepted_keywords.lst;
  };
  name = "airs-adoc-linter";
  searchPaths = {
    bin = [
      inputs.nixpkgs.diction
      inputs.nixpkgs.gnugrep
      inputs.nixpkgs.pcre
    ];
  };
  template = ./template.sh;
}
