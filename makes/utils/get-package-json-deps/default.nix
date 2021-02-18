path: pkgs:

packageJsonPath:
let
  nix = import (path "/makes/utils/nix") path pkgs;
  packageJson = builtins.fromJSON (builtins.readFile (path packageJsonPath));
  devDeps = pkgs.lib.attrsets.mapAttrsToList (name: version: "${name}@${version}") packageJson.devDependencies;
  prodDeps = pkgs.lib.attrsets.mapAttrsToList (name: version: "${name}@${version}") packageJson.dependencies;
in
{
  development = nix.sortCaseless devDeps;
  production = nix.sortCaseless prodDeps;
}
