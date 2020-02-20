pkgs:

pkgs.python38.withPackages (ps: with ps; [
  matplotlib
  pip
  python_magic
  setuptools
  wheel
])
