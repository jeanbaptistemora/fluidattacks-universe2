{ lib
, pythonPkgs
, src
, metadata
}:
let
  runtime_deps = [
    pythonPkgs.redshift-client
  ];
  dev_deps = [
    pythonPkgs.mypy
  ];
  build_pkg = propagatedBuildInputs: (import ./build.nix) {
    nativeBuildInputs = [ pythonPkgs.poetry ] ++ dev_deps;
    inherit lib src metadata propagatedBuildInputs;
  };
in
{
  runtime = build_pkg runtime_deps;
  dev = build_pkg (runtime_deps ++ dev_deps);
}
