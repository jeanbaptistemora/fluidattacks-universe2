{ nixpkgs
, makeTemplate
, path
, ...
}:
makeTemplate {
  name = "integrates-back-probes-lib";
  searchPaths = {
    envPaths = [
      nixpkgs.awscli
      nixpkgs.curl
      nixpkgs.gnugrep
    ];
  };
  template = path "/makes/packages/integrates/back/probes/lib/template.sh";
}
