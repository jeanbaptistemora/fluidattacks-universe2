{ nixpkgs2
, makeTemplate
, path
, ...
}:
makeTemplate {
  name = "integrates-back-probes-lib";
  searchPaths = {
    envPaths = [
      nixpkgs2.awscli
      nixpkgs2.curl
      nixpkgs2.gnugrep
    ];
  };
  template = path "/makes/packages/integrates/back/probes/lib/template.sh";
}
