{ lib
, pythonPkgs
, src
}:
let
  runtime_deps = [
    pythonPkgs.bugsnag
  ];
  dev_deps = runtime_deps ++ [
    pythonPkgs.mypy
  ];
  build_pkg = propagatedBuildInputs: (import ./build.nix) {
    nativeBuildInputs = [ pythonPkgs.poetry ];
    inherit lib src propagatedBuildInputs;
  };
in
{
  runtime = build_pkg runtime_deps;
  dev = build_pkg dev_deps;
}
