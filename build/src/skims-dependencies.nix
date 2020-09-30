pkgs: {
  build = [
    pkgs.awscli
    pkgs.gnutar
    pkgs.gradle
    pkgs.graphviz
    pkgs.python38Packages.poetry
  ];

  runtime = [
    pkgs.git
    pkgs.jdk11
    pkgs.nodejs
    pkgs.python38
  ];
}
