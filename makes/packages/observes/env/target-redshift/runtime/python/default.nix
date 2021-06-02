{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-target-redshift-runtime-python";
  dependencies = [
    nixpkgs.postgresql
  ];
  requirements = {
    direct = [
      "click==7.1.2"
      "jsonschema==3.2.0"
      "psycopg2==2.8.4"
      "returns==0.16.0"
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
  python = nixpkgs.python38;
}
