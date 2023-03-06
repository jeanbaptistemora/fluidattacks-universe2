{
  inputs,
  makeTemplate,
  name,
  env,
  bins,
}:
makeTemplate {
  inherit name;
  searchPaths = {
    bin =
      bins
      ++ [
        env
      ];
  };
  replace = {
    __argPython__ = inputs.nixpkgs.python310;
    __argPythonEnv__ = env;
    __argPythonEntry__ = ./vs_settings.py;
  };
  template = ./template.sh;
}
