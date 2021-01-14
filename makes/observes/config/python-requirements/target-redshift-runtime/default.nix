{ observesPkgs
, ...
} @ _:
let
  buildPythonRequirements = import ../../../../../makes/utils/build-python-requirements observesPkgs;
in
buildPythonRequirements {
  dependencies = [
    observesPkgs.postgresql
  ];
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
}
