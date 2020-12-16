pkgs: {
  build = [
    pkgs.python38Packages.poetry
  ];

  runtime = [
    pkgs.awscli
    pkgs.git
    pkgs.python38
  ];
}
