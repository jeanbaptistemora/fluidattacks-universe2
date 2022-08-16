{
  inputs,
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  replace = {
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
    __argSrcSkimsVendor__ = projectPath "/skims/vendor";
    __argSrcSkimsStatic__ = projectPath "/skims/static";
  };
  name = "integrates-scheduler";
  searchPaths = {
    bin = [
      inputs.nixpkgs.python39
      outputs."/melts"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
