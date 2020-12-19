{
  flake,
  pkgsSrcSkims,
  self,
}:

flake.lib.eachDefaultSystem (
  system:
    let
      attrs = {
        pkgsSkims = import pkgsSrcSkims { inherit system; };
      };
    in
      {
        packages = {
          skims-parsers-antlr = import ../makes/skims/parsers/antlr attrs;
        };
      }
)
