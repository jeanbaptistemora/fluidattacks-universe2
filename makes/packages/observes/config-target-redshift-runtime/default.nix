{ observesPkgs
, path
, ...
} @ _:
let
  buildPythonRequirements = import (path "/makes/utils/build-python-requirements") path observesPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths-deprecated") path observesPkgs;
  makeTemplate = import (path "/makes/utils/make-template") path observesPkgs;
in
makeTemplate {
  arguments = {
    envPython = "${observesPkgs.python37}/bin/python";
    envPythonRequirements = buildPythonRequirements {
      dependencies = [
        observesPkgs.postgresql
      ];
      name = "observes-target-redshift-runtime";
      requirements = {
        direct = [
          "jsonschema==3.2.0"
          "psycopg2==2.8.4"
        ];
        inherited = [
          "attrs==20.3.0"
          "importlib-metadata==3.4.0"
          "pyrsistent==0.17.3"
          "six==1.15.0"
          "typing-extensions==3.7.4.3"
          "zipp==3.4.0"
        ];
      };
      python = observesPkgs.python37;
    };
    envSearchPaths = makeSearchPaths [
      observesPkgs.postgresql
    ];
    envSrcObservesTargetRedshiftEntrypoint = path "/observes/singer/target_redshift/target_redshift/__init__.py";
    envUtilsBashLibPython = path "/makes/utils/python/template.sh";
  };
  name = "observes-config-redshift-runtime";
  template = path "/makes/packages/observes/config-target-redshift-runtime/template.sh";
}
