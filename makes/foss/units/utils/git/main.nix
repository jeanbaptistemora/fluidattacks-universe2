{ inputs
, makeTemplate
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
      (inputs.legacy.importUtility "env")
    ];
  };
  template = ./template.sh;
}
