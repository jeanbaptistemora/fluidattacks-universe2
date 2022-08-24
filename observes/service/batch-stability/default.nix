{
  nixpkgs,
  src,
}: let
  python_version = "python310";
  metadata = (builtins.fromTOML (builtins.readFile "${src}/pyproject.toml")).tool.poetry;
  deps = import ./build/deps {
    inherit nixpkgs python_version;
  };
  self_pkgs = import ./build/pkg {
    inherit src metadata;
    lib = deps.lib;
    python_pkgs = deps.python_pkgs;
  };
  checks = import ./check {self_pkg = self_pkgs.pkg;};
in
  self_pkgs // {check = checks;}
