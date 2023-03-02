{
  nixpkgs,
  python_version,
  src,
}: let
  metadata = let
    _metadata = (builtins.fromTOML (builtins.readFile ../pyproject.toml)).project;
    file_str = builtins.readFile "${src}/${_metadata.name}/__init__.py";
    match = builtins.match ".*__version__ *= *\"(.+?)\"\n.*" file_str;
    version = builtins.elemAt match 0;
  in
    _metadata // {inherit version;};
  deps = import ./deps {
    inherit nixpkgs python_version;
  };

  runtime_deps = with deps.python_pkgs; [
    fa-purity
    utils-logger
  ];
  build_deps = with deps.python_pkgs; [flit-core];
  test_deps = with deps.python_pkgs; [
    arch-lint
    mypy
    pylint
    pytest
  ];
  bin_deps = [
    nixpkgs.tap-google-sheets
    nixpkgs.sops
  ];

  pkg = import ./pkg {
    inherit src metadata runtime_deps test_deps build_deps;
    lib = deps.lib;
  };
  env = import ./env.nix {
    inherit pkg runtime_deps test_deps;
    lib = deps.lib;
  };
  check = import ./check.nix {inherit pkg;};
in {inherit pkg env check bin_deps;}
