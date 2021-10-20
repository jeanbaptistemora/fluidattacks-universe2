{ fetchGithub
, inputs
, makeDerivation
, outputs
, ...
}:
makeDerivation {
  builder = ./builder.sh;
  name = "tree-sitter-languages";
  searchPaths = {
    bin = [ inputs.nixpkgs.python38 ];
    rpath = [ inputs.nixpkgs.gcc.cc.lib ];
    source = [ outputs."/skims/config-runtime/pypi" ];
  };
  env = {
    envBuildPy = ./build.py;
    envTreeSitterCSharp = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-c-sharp";
      rev = "851ac4735f66ec9c479096cc21bf58519da49faa";
      sha256 = "UHw5JQ++iYLTyqL8KH1impRxXJ2oJAQRoD79nLVQgMw=";
    };
    envTreeSitterGo = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-go";
      rev = "eb306e6e60f393df346cfc8cbfaf52667a37128a";
      sha256 = "7LD8wR4Gg4OadYaXTSbGPe5iAOagRPGJSpO51uW0ow8=";
    };
    envTreeSitterJava = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-java";
      rev = "2efe37f92d2e6aeb25186e9da07455bb4a30163c";
      sha256 = "09v3xg1356ghc2n0yi8iqkp80lbkav0jpfgz8iz2j1sl7ihbvkyw";
    };
    envTreeSitterJavaScript = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-javascript";
      rev = "45b9ce2a2588c0e6d616b0ee2a710b1fcb99c5b5";
      sha256 = "nU0mVkGG6Sr4OstRFCIrbUGJnAHMZ9+lCDTJAFf392c=";
    };
    envTreeSitterKotlin = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-kotlin";
      rev = "48bfb38abd93f8d617877d7bb7f92a6bb1166285";
      sha256 = "5thm7nYOZLDUsb/2KGV2fZg35uId8nZEMdyLUsdTPT0=";
    };
    envTreeSitterPhp = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-php";
      rev = "435fa00006c0d1515c37fbb4dd6a9de284af75ab";
      sha256 = "05k4h58gi616gv41r0qqdb1x4rs8y94vghn2r10yczisgzq4vbad";
    };
    envTreeSitterTsx = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-typescript";
      rev = "3e897ea5925f037cfae2e551f8e6b12eec2a201a";
      sha256 = "1qJsaeJzcbSTDe9hqc9SjPhGG0RNaolTYQLuwgryIsw=";
    };
  };
}
