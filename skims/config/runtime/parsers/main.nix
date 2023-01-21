{
  inputs,
  makeDerivation,
  outputs,
  ...
}:
makeDerivation {
  builder = ./builder.sh;
  name = "tree-sitter-languages";
  searchPaths = {
    bin = [
      inputs.nixpkgs.python38
      inputs.nixpkgs.binutils-unwrapped
    ];
    rpath = [inputs.nixpkgs.gcc.cc.lib];
    source = [outputs."/skims/config/runtime/pypi"];
  };
  env = {
    envBuildPy = ./build.py;
    envTreeSitterCSharp = inputs.skimsTreeSitterCSharp;
    envTreeSitterDart = inputs.skimsTreeSitterDart;
    envTreeSitterGo = inputs.skimsTreeSitterGo;
    envTreeSitterHcl = inputs.skimsTreeSitterHcl;
    envTreeSitterJava = inputs.skimsTreeSitterJava;
    envTreeSitterJavaScript = inputs.skimsTreeSitterJavaScript;
    envTreeSitterJson = inputs.skimsTreeSitterJson;
    envTreeSitterKotlin = inputs.skimsTreeSitterKotlin;
    envTreeSitterPhp = inputs.skimsTreeSitterPhp;
    envTreeSitterPython = inputs.skimsTreeSitterPython;
    envTreeSitterRuby = inputs.skimsTreeSitterRuby;
    envTreeSitterScala = inputs.skimsTreeSitterScala;
    envTreeSitterTsx = inputs.skimsTreeSitterTsx;
    envTreeSitterYaml = inputs.skimsTreeSitterYaml;
  };
}
