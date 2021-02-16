{ path
, reviewsPkgs
, ...
} @ _:
let
  buildPythonRequirements = import (path "/makes/utils/build-python-requirements") path reviewsPkgs;
  makeTemplate = import (path "/makes/utils/make-template") path reviewsPkgs;
in
makeTemplate {
  arguments = {
    envSrcReviews = path "/reviews/src";
  };
  name = "reviews-runtime";
  searchPaths = {
    envPaths = [
      reviewsPkgs.python38
    ];
    envPythonPaths = [
      (path "/reviews/src")
    ];
    envPython38Paths = [
      (buildPythonRequirements {
        dependencies = [ ];
        name = "skims-runtime";
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
        python = reviewsPkgs.python38;
      })
    ];
  };
  template = path "/makes/packages/reviews/runtime/template.sh";
}
