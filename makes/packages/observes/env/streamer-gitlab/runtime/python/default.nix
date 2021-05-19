{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-streamer-gitlab-runtime-python";
  requirements = {
    direct = [
      "aioextensions==20.8.2087641"
      "aiohttp==3.6.2"
      "asgiref==3.2.10"
    ];
    inherited = [
      "async-timeout==3.0.1"
      "attrs==20.3.0"
      "chardet==3.0.4"
      "idna==3.1"
      "multidict==4.7.6"
      "uvloop==0.14.0"
      "yarl==1.6.3"
    ];
  };
  python = nixpkgs.python38;
}
