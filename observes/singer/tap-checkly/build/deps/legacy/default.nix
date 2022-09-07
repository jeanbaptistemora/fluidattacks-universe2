# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  extras,
  pythonPkgs,
  pythonVersion,
}: let
  legacy-purity = extras.legacy-purity."${pythonVersion}".pkg.overridePythonAttrs (
    old: {
      propagatedBuildInputs = map (x:
        if x.pname == "fa_purity"
        then pythonPkgs.fa-purity
        else x)
      old.propagatedBuildInputs;
    }
  );
  replace_purity = old: {
    propagatedBuildInputs = map (x:
      if x.pname == "purity"
      then legacy-purity
      else x)
    old.propagatedBuildInputs;
  };
in {
  inherit legacy-purity;
  legacy-paginator = extras.legacy-paginator."${pythonVersion}".pkg.overridePythonAttrs replace_purity;
  legacy-singer-io = extras.legacy-singer-io."${pythonVersion}".pkg.overridePythonAttrs replace_purity;
}
