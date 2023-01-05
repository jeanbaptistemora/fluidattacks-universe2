{
  nixpkgs,
  python_version,
  src,
}: let
  metadata = let
    _metadata = (builtins.fromTOML (builtins.readFile ./pyproject.toml)).project;
    file_str = builtins.readFile "${src}/${_metadata.name}/__init__.py";
    match = builtins.match ".*__version__ *= *\"(.+?)\"\n.*" file_str;
    version = builtins.elemAt match 0;
  in
    _metadata // {inherit version;};
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
