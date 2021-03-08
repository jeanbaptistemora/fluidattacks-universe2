{ makeEntrypoint
, nixpkgs
, nixpkgs2
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envMakes = path "/";
  };
  name = "makes-lint";
  searchPaths = {
    envPaths = [
      nixpkgs.findutils
      nixpkgs.nixpkgs-fmt
      nixpkgs.shellcheck
      nixpkgs2.nix-linter
    ];
  };
  template = path "/makes/applications/makes/lint/template.sh";
}
