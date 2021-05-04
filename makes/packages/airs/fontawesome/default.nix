{ nixpkgs
, makeTemplate
, path
, ...
}:
makeTemplate {
  name = "airs-fontawesome";
  searchPaths = {
    envPaths = [
      nixpkgs.nodejs
    ];
  };
  template = path "/makes/packages/airs/fontawesome/template.sh";
}
