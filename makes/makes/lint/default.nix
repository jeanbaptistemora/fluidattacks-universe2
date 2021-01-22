{ makesPkgs
, path
, ...
} @ _:
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
  location = "/bin/makes-lint";
  name = "makes-lint";
  template = path "/makes/makes/lint/template.sh";
}
