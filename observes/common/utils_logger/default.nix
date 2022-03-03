{ python_version, legacy_pkgs, src }:
let
  supported = [ "python38" "python39" "python310" ];
  python = if (builtins.elem python_version supported) then python_version else abort "Python version not supported";
  metadata = (builtins.fromTOML (builtins.readFile ./pyproject.toml)).tool.poetry;
  lib = {
    buildPythonPackage = legacy_pkgs."${python}".pkgs.buildPythonPackage;
  };
  pythonPkgs = legacy_pkgs."${python}Packages";
  self_pkgs = import ./build/pkg {
    inherit src lib metadata pythonPkgs;
  };
  build_env = pkg: legacy_pkgs."${python}".buildEnv.override {
    extraLibs = [ pkg ];
    ignoreCollisions = false;
  };
in
{
  env.runtime = build_env self_pkgs.runtime;
  env.dev = build_env self_pkgs.dev;
  pkg = self_pkgs.runtime;
}
