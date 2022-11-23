{
  python_version,
  legacy_pkgs,
  src,
}: let
  supported = ["python38" "python39" "python310"];
  python =
    if (builtins.elem python_version supported)
    then python_version
    else abort "Python version not supported";
  metadata = (builtins.fromTOML (builtins.readFile ./pyproject.toml)).tool.poetry;
  lib = {
    buildEnv = legacy_pkgs."${python_version}".buildEnv.override;
    buildPythonPackage = legacy_pkgs."${python}".pkgs.buildPythonPackage;
  };
  python_pkgs = legacy_pkgs."${python}Packages";
  self_pkgs = import ./build/pkg {
    inherit src lib metadata python_pkgs;
  };
in
  self_pkgs
