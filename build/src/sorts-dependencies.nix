pkgs: {
  build = [
    pkgs.python38Packages.poetry
  ];

  runtime = [
    pkgs.git
    pkgs.python38
  ];
}
