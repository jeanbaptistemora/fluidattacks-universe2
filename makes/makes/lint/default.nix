{ makesPkgs
, ...
} @ _:
let
  makeEntrypoint = import ../../../makes/utils/make-entrypoint makesPkgs;
in
makeEntrypoint {
  arguments = {
    envFind = "${makesPkgs.findutils}/bin/find";
    envNixLinter = "${makesPkgs.nix-linter}/bin/nix-linter";
    envNixpkgsFmt = "${makesPkgs.nixpkgs-fmt}/bin/nixpkgs-fmt";
    envSort = "${makesPkgs.coreutils}/bin/sort";
    envShellcheck = "${makesPkgs.shellcheck}/bin/shellcheck";
  };
  location = "/bin/makes-lint";
  name = "makes-lint";
  template = ../../../makes/makes/lint/template.sh;
}
