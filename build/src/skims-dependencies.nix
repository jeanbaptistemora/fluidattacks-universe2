pkgs: {
  build = [
    pkgs.awscli
    pkgs.gnutar
    pkgs.gradle
    pkgs.python38Packages.poetry
  ];

  runtime = [
    pkgs.git
    pkgs.graphviz
    pkgs.jdk11
    pkgs.nodejs
    pkgs.python38
  ];

  overriden = {
    overridenPyPkgPyGraphviz = pkgs.python38Packages.pygraphviz;
  };
}
