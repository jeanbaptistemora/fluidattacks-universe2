pkgs:

pkgs.python38.withPackages (ps: with ps; [
  matplotlib
  pip
  python_magic
  selenium
  setuptools
  wheel
])
