path: pkgs:
let
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;
in
makeTemplate {
  arguments = {
    envTypescriptRequirements = {
      dependencies = [ ];
      name = "lint-typescript";
      requirements = {
        direct = [
        ];
        inherited = [
        ];
      };
    };
  };
  template = path "/makes/utils/lint-typescript/template.sh";
}
