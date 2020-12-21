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
          skims-bin = import ../makes/skims/bin attrs;
          skims-parsers-antlr = import ../makes/skims/parsers/antlr attrs;
        };
      }
)
