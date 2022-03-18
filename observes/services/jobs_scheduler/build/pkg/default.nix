{
  lib,
  pythonPkgs,
  src,
  metadata,
}: let
  runtime_deps = [
    pythonPkgs.click
    pythonPkgs.purity
    pythonPkgs.pytz
    pythonPkgs.utils-logger
    pythonPkgs.types-click
    pythonPkgs.types-pytz
  ];
  dev_deps = [
    pythonPkgs.mypy
    pythonPkgs.pytest
    pythonPkgs.toml
    pythonPkgs.types-toml
  ];
  build_pkg = propagatedBuildInputs:
    (import ./build.nix) {
      nativeBuildInputs = [pythonPkgs.poetry] ++ dev_deps;
      inherit lib src metadata propagatedBuildInputs;
    };
in {
  runtime = build_pkg runtime_deps;
  dev = build_pkg (runtime_deps ++ dev_deps);
}
