{
  legacyPkgs,
  localLib,
  pythonVersion,
  system,
}: let
  legacy-paginator = import localLib.legacy-paginator {
    src = localLib.legacy-paginator;
    inherit legacyPkgs localLib pythonVersion system;
  };
  legacy-purity = import localLib.legacy-purity {
    src = localLib.legacy-purity;
    inherit legacyPkgs pythonVersion system;
  };
  legacy-singer-io = import localLib.legacy-singer-io {
    src = localLib.legacy-singer-io;
    inherit legacyPkgs localLib pythonVersion system;
  };
in {
  legacy-paginator = legacy-paginator.pkg;
  legacy-purity = legacy-purity.pkg;
  legacy-singer-io = legacy-singer-io.pkg;
}
