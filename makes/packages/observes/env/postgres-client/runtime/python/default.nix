{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-postgres-client-runtime-python";
  dependencies = [
    nixpkgs.postgresql
  ];
  requirements = {
    direct = [
      "Deprecated==1.2.12"
      "psycopg2==2.8.6"
      "returns==0.16.0"
    ];
    inherited = [
      "typing-extensions==3.7.4.3"
      "wrapt==1.12.1"
    ];
  };
  python = nixpkgs.python38;
}
