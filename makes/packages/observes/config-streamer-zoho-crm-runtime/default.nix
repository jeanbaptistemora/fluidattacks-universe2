{ nixpkgs
, path
, ...
}:
let
  buildPythonRequirements = import (path "/makes/utils/build-python-requirements") path nixpkgs;
  makeTemplate = import (path "/makes/utils/make-template") path nixpkgs;
in
makeTemplate {
  arguments = {
    envPython = "${nixpkgs.python38}/bin/python";
    envPythonRequirements = buildPythonRequirements {
      dependencies = [
      ];
      name = "observes-streamer-zoho-crm-runtime";
      requirements = {
        direct = [
          "click==7.1.2"
          "ratelimiter==1.2.0"
          "requests==2.25.0"
        ];
        inherited = [
          "certifi==2020.12.5"
          "chardet==3.0.4"
          "idna==2.10"
          "urllib3==1.26.2"
        ];
      };
      python = nixpkgs.python38;
    };
    envSrcObservesStreamerZohoCrmEntrypoint = path "/observes/singer/streamer_zoho_crm/streamer_zoho_crm/__init__.py";
    envUtilsBashLibPython = path "/makes/utils/python/template.sh";
  };
  name = "observes-config-zoho-crm-runtime";
  template = path "/makes/packages/observes/config-streamer-zoho-crm-runtime/template.sh";
}
