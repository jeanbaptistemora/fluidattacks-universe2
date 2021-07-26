{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-singer-io-runtime-python";
  requirements = {
    direct = [
      "jsonschema==3.2.0"
      "pytz==2021.1"
      "returns==0.16.0"
    ];
    inherited = [
      "attrs==21.2.0"
      "pyrsistent==0.18.0"
      "six==1.16.0"
      "typing-extensions==3.10.0.0"
    ];
  };
  python = nixpkgs.python38;
}
