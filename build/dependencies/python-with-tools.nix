pkgs:

let
  python = pkgs.python37.withPackages (ps: with ps; [
    matplotlib
    pip
    python_magic
    selenium
    setuptools
    wheel
  ]);
in
  [
    python
  ]
