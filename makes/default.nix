{
  flake,
  pkgsSrcCommon,
  pkgsSrcSkims,
  self,
}:

flake.lib.eachDefaultSystem (
  system:
    let
      attrs = {
        pkgsCommon = import pkgsSrcSkims { inherit system; };
        pkgsSkims = import pkgsSrcSkims { inherit system; };
        self = self;
      };
    in
      {
        apps = {
          skims = {
            program = "${import ../makes/skims/bin attrs}";
            type = "app";
          };
        };
        packages = {
          skims-bin = import ../makes/skims/bin attrs;
          skims-parsers-antlr = import ../makes/skims/parsers/antlr attrs;
          skims-parsers-babel = import ../makes/skims/parsers/babel attrs;
        };
      }
)
