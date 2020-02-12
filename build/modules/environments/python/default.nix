pkgs:

pkgs.python38.withPackages (ps: with ps; [
  pip
  setuptools
  wheel
])
