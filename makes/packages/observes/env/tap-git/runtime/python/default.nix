{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-tap-git-runtime-python";
  requirements = {
    direct = [
      "GitPython==3.1.14"
    ];
    inherited = [
      "gitdb==4.0.7"
      "smmap==4.0.0"
    ];
  };
  python = nixpkgs.python38;
}
