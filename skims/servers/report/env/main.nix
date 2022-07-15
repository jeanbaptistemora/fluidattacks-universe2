{
  makePythonPypiEnvironment,
  inputs,
  ...
}:
makePythonPypiEnvironment {
  name = "report";
  searchPathsRuntime = {
    bin = [
      inputs.nixpkgs.git
      inputs.nixpkgs.curl
      inputs.nixpkgs.python39Packages.pycurl
    ];
    pythonPackage = [
      "${inputs.nixpkgs.python39Packages.pycurl}/lib/python3.9/site-packages/"
    ];
  };
  sourcesYaml = ./pypi-sources.yaml;
}
