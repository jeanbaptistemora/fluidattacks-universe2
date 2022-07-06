{
  observesIndex,
  nixpkgs,
  projectPath,
  python_version,
  src,
  system,
}: let
  metadata = let
    _metadata = (builtins.fromTOML (builtins.readFile ./pyproject.toml)).project;
    file_str = builtins.readFile "${src}/${_metadata.name}/__init__.py";
    match = builtins.match ".*__version__ *= *\"(.+?)\"\n.*" file_str;
    version = builtins.elemAt match 0;
  in
    _metadata // {inherit version;};
  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    buildPythonPackage = nixpkgs."${python_version}".pkgs.buildPythonPackage;
    fetchPypi = nixpkgs.python3Packages.fetchPypi;
  };
  python_pkgs = import ./build/deps {
    inherit observesIndex nixpkgs lib projectPath python_version system;
  };
  self_pkgs = import ./build/pkg {
    inherit src lib metadata python_pkgs;
  };
  checks = import ./check {self_pkg = self_pkgs.pkg;};
in
  self_pkgs // {check = checks;}
