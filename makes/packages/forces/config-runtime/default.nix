{ buildPythonRequirements
, makeTemplate
, nixpkgs
, path
, ...
}:
makeTemplate {
  arguments = {
    envSrcForces = path "/forces";
  };
  name = "forces-config-runtime";
  searchPaths = {
    envPaths = [
      nixpkgs.git
      nixpkgs.python38
    ];
    envPython38Paths = [
      (buildPythonRequirements {
        dependencies = [ ];
        name = "forces-runtime";
        requirements = {
          direct = [
            "aioextensions==20.8.2087641"
            "aiogqlc==2.0.0b1"
            "aiohttp==3.6.2"
            "bugsnag==3.7.1"
            "click==7.1.2"
            "GitPython==3.1.7"
            "more-itertools==8.5.0"
            "oyaml==0.9"
            "python-dateutil==2.8.1"
            "pytz==2020.1"
            "uvloop==0.14.0"
          ];
          inherited = [
            "async-timeout==3.0.1"
            "attrs==20.3.0"
            "chardet==3.0.4"
            "gitdb==4.0.5"
            "idna==3.1"
            "multidict==4.7.6"
            "PyYAML==5.3.1"
            "six==1.15.0"
            "smmap==3.0.4"
            "WebOb==1.8.6"
            "yarl==1.6.3"
          ];
        };
        python = nixpkgs.python38;
      })
    ];
    envPythonPaths = [
      (path "/forces")
    ];
  };
  template = path "/makes/packages/forces/config-runtime/template.sh";
}
