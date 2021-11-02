{ inputs
, makeDerivation
, outputs
, ...
}:
makeDerivation {
  builder = ./builder.sh;
  name = "tree-sitter-languages";
  searchPaths = {
    bin = [
      inputs.nixpkgs.python38
      inputs.nixpkgs.binutils-unwrapped
    ];
    rpath = [ inputs.nixpkgs.gcc.cc.lib ];
    source = [ outputs."/skims/config-runtime/pypi" ];
  };
  env = {
    envBuildPy = ./build.py;
    envTreeSitterCSharp = inputs.skimsTreeSitterCSharp;
    envTreeSitterDart = inputs.skimsTreeSitterDart;
    envTreeSitterGo = inputs.skimsTreeSitterGo;
    envTreeSitterJava = inputs.skimsTreeSitterJava;
    envTreeSitterJavaScript = inputs.skimsTreeSitterJavaScript;
    envTreeSitterKotlin = inputs.skimsTreeSitterKotlin;
    envTreeSitterPhp = inputs.skimsTreeSitterPhp;
    envTreeSitterRuby = inputs.skimsTreeSitterRuby;
    envTreeSitterScala = inputs.skimsTreeSitterScala;
    envTreeSitterTsx = inputs.skimsTreeSitterTsx;
  };
}
