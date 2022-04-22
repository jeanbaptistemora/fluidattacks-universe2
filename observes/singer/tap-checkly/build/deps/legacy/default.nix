{
  legacyPkgs,
  localLib,
  purity,
  pythonVersion,
  system,
}: let
  legacy-purity-output = import localLib.legacy-purity {
    src = localLib.legacy-purity;
    inherit legacyPkgs pythonVersion system;
  };
  legacy-purity = legacy-purity-output.pkg.overridePythonAttrs (
    old: {
      propagatedBuildInputs = map (x:
        if x.pname == "fa_purity"
        then purity
        else x)
      old.propagatedBuildInputs;
    }
  );
  legacy-paginator = import localLib.legacy-paginator {
    src = localLib.legacy-paginator;
    inherit legacyPkgs localLib pythonVersion system;
  };
  legacy-singer-io = import localLib.legacy-singer-io {
    src = localLib.legacy-singer-io;
    inherit legacyPkgs localLib pythonVersion system;
  };
  replace_purity = old: {
    propagatedBuildInputs = map (x:
      if x.pname == "purity"
      then legacy-purity
      else x)
    old.propagatedBuildInputs;
  };
in {
  inherit legacy-purity;
  legacy-paginator = legacy-paginator.pkg.overridePythonAttrs replace_purity;
  legacy-singer-io = legacy-singer-io.pkg.overridePythonAttrs replace_purity;
}
