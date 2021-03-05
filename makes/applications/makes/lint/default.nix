{ nixpkgs
, path
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs;
in
makeEntrypoint {
  arguments = {
    envFind = "${nixpkgs.findutils}/bin/find";
    envNixLinter = "${nixpkgs.nix-linter}/bin/nix-linter";
    envNixpkgsFmt = "${nixpkgs.nixpkgs-fmt}/bin/nixpkgs-fmt";
    envMakes = path "/";
    envShellcheck = "${nixpkgs.shellcheck}/bin/shellcheck";
  };
  name = "makes-lint";
  template = path "/makes/applications/makes/lint/template.sh";
}
