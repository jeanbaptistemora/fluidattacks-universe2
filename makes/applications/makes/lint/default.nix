{ makesPkgs
, path
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path makesPkgs;
in
makeEntrypoint {
  arguments = {
    envFind = "${makesPkgs.findutils}/bin/find";
    envNixLinter = "${makesPkgs.nix-linter}/bin/nix-linter";
    envNixpkgsFmt = "${makesPkgs.nixpkgs-fmt}/bin/nixpkgs-fmt";
    envMakes = path "/";
    envShellcheck = "${makesPkgs.shellcheck}/bin/shellcheck";
  };
  name = "makes-lint";
  template = path "/makes/applications/makes/lint/template.sh";
}
