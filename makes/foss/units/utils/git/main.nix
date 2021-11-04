{ inputs
, makeTemplate
, outputs
, ...
}:
makeTemplate {
  replace = {
    __argGit__ = "${inputs.nixpkgs.git}/bin/git";
  };
  name = "utils-bash-lib-git";
  searchPaths = {
    bin = [
      inputs.nixpkgs.git
    ];
    source = [
      (outputs."/utils/env")
    ];
  };
  template = ./template.sh;
}
