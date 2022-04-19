{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "skims-benchmark-owasp";
  replace = {
    __argBenchmarkRepo__ = inputs.skimsBenchmarkOwaspRepo;
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.python38
      outputs."/skims"
    ];
    source = [outputs."/skims/config/runtime"];
  };
  entrypoint = ./entrypoint.sh;
}
