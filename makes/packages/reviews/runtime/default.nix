{ buildPythonRequirements
, makeTemplate
, packages
, path
, nixpkgs
, ...
}:
makeTemplate {
  arguments = {
    envSrcReviews = path "/reviews/src";
  };
  name = "reviews-runtime";
  searchPaths = {
    envPaths = [
      nixpkgs.python38
    ];
    envPythonPaths = [
      (path "/reviews/src")
    ];
    envPython38Paths = [
      (buildPythonRequirements {
        dependencies = [ ];
        name = "reviews-runtime";
        requirements = {
          direct = [
            "click==7.1.2"
            "dynaconf==3.0.0"
            "pygit2==1.2.1"
            "python-gitlab==2.4.0"
          ];
          inherited = [
            "cached-property==1.5.2"
            "certifi==2020.12.5"
            "cffi==1.14.5"
            "chardet==4.0.0"
            "idna==2.10"
            "pycparser==2.20"
            "requests==2.25.1"
            "urllib3==1.26.3"
          ];
        };
        python = nixpkgs.python38;
      })
    ];
    envNodeBinaries = [
      packages.makes.commitlint
    ];
    envNodeLibraries = [
      packages.makes.commitlint
    ];
  };
  template = path "/makes/packages/reviews/runtime/template.sh";
}
