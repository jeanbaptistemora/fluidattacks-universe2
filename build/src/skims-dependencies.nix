pkgs: rec {
  build = [
    pkgs.awscli
    pkgs.gnutar
    pkgs.gradle
    pkgs.python38Packages.poetry
  ];

  overriden = {
    overridenPyPkgPyGraphviz = pkgs.python38Packages.pygraphviz;
  };

  runtime = (builtins.attrValues overriden) ++ [
    pkgs.git
    pkgs.graphviz
    pkgs.jdk11
    pkgs.nodejs
    pkgs.python38
  ];
}
