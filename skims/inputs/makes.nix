{
  fetchGithub,
  fromJsonFile,
  inputs,
  projectPath,
  ...
}: {
  inputs = {
    skimsAndroguard = fetchGithub {
      owner = "androguard";
      repo = "androguard";
      rev = "8d091cbb309c0c50bf239f805cc1e0931b8dcddc";
      sha256 = "sSNs51JvBAAEUmMY84wlmuB0nVdIyc+sBTFjr1nZl7g=";
    };
    skimsBenchmarkOwasp = fetchGithub {
      owner = "OWASP-Benchmark";
      repo = "BenchmarkJava";
      rev = "53732be42f3e780fd98d40b32f538062b3b19da9";
      sha256 = "0frrvrl4nyy8rllcpvgxazv9ybv61z49knhd6k0pmnasz2a53zga";
    };
    skimsNistTestSuites = fetchGithub {
      owner = "fluidattacks";
      repo = "NIST-SARD-Test-Suites";
      rev = "7189c65ab6e398180e3f2aa2de683466b4412821";
      sha256 = "CDLX3Xa7nCmzdJdAjlSzdlFIaUx3cg7GPiqc5c8Dj6Q=";
    };
    skimsVulnerableApp = fetchGithub {
      owner = "SasanLabs";
      repo = "VulnerableApp";
      rev = "f5334e84faadbfb4beec42849a2e8acc5e37a276";
      sha256 = "gVY9VPo0+2xHdbME61MH/JaMP8pyqWh5k7im3O8hNAc=";
    };
    skimsVulnerableJsApp = fetchGithub {
      owner = "fluidattacks";
      repo = "vulnerable_js_app";
      rev = "1282fbde196abb5a77235ba4dd5a64f46dac6e52";
      sha256 = "0sc6zx9zf2v5m2a0hfccynyn93mcx97ks6ksdf9larha6l5r977f";
    };
    skimsTestPythonCategories =
      fromJsonFile
      (projectPath "/skims/test/test_groups.json");
    skimsTestPythonCategoriesCI =
      builtins.filter
      (category: category != "_" && category != "all")
      (inputs.skimsTestPythonCategories);
    skimsTreeSitterCSharp = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-c-sharp";
      rev = "7a47daeaf0d410dd1a91c97b274bb7276dd96605";
      sha256 = "1GRKI+/eh7ESlX24qA+A5rSdC1lUXACiBOUlgktcMlI=";
    };
    skimsTreeSitterDart = fetchGithub {
      owner = "UserNobody14";
      repo = "tree-sitter-dart";
      rev = "c667fd401c736e208c73b7bb9267557b67b23491";
      sha256 = "11ib2Vm4t+JfzaH9Lz2N7sm6aK7YSzoUy87+jsRHnEc=";
    };
    skimsTreeSitterGo = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-go";
      rev = "eb306e6e60f393df346cfc8cbfaf52667a37128a";
      sha256 = "7LD8wR4Gg4OadYaXTSbGPe5iAOagRPGJSpO51uW0ow8=";
    };
    skimsTreeSitterHcl = fetchGithub {
      owner = "MichaHoffmann";
      repo = "tree-sitter-hcl";
      rev = "0ff887f2a60a147452d52db060de6b42f42f1441";
      sha256 = "L4B2qtGqrtyLHyUMx1p0t4aKncm72dUE+e19Fv5iqUA=";
    };
    skimsTreeSitterJava = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-java";
      rev = "2efe37f92d2e6aeb25186e9da07455bb4a30163c";
      sha256 = "09v3xg1356ghc2n0yi8iqkp80lbkav0jpfgz8iz2j1sl7ihbvkyw";
    };
    skimsTreeSitterJavaScript = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-javascript";
      rev = "45b9ce2a2588c0e6d616b0ee2a710b1fcb99c5b5";
      sha256 = "nU0mVkGG6Sr4OstRFCIrbUGJnAHMZ9+lCDTJAFf392c=";
    };
    skimsTreeSitterJson = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-json";
      rev = "73076754005a460947cafe8e03a8cf5fa4fa2938";
      sha256 = "wbE7CQ6l1wlhJdAoDVAj1QzyvlYnevbrlVCO0TMU7to=";
    };
    skimsTreeSitterKotlin = fetchGithub {
      owner = "fwcd";
      repo = "tree-sitter-kotlin";
      rev = "48bfb38abd93f8d617877d7bb7f92a6bb1166285";
      sha256 = "0g9xag3m52yw6527dwhxwbk3g63xfrjjixmzn7ab0r0ffvp6dn76";
    };
    skimsTreeSitterPhp = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-php";
      rev = "435fa00006c0d1515c37fbb4dd6a9de284af75ab";
      sha256 = "05k4h58gi616gv41r0qqdb1x4rs8y94vghn2r10yczisgzq4vbad";
    };
    skimsTreeSitterPython = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-python";
      rev = "9e53981ec31b789ee26162ea335de71f02186003";
      sha256 = "D2++Xg7dRfjGM2r4cxaXGQnBOAX5JBREcEAJeNa7Y9M=";
    };
    skimsTreeSitterRuby = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-ruby";
      rev = "1fedb2a117f89b7df05550255a022f6e25bb7975";
      sha256 = "0r8gp511ldp0h4f9v7pjcfmrldc68vad5vxphlknm4kvknm7ysfc";
    };
    skimsTreeSitterScala = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-scala";
      rev = "0a3dd53a7fc4b352a538397d054380aaa28be54c";
      sha256 = "1lwyipn5b36fskr8cm60qjblj2chf8336zkqbsifq49z1lj0wvpi";
    };
    skimsTreeSitterSwift = fetchGithub {
      owner = "fluidattacks";
      repo = "tree-sitter-swift";
      rev = "462813c6c589e5ffc859d4ed43dbd2ba6cba8013";
      sha256 = "ZKoYlzcntlHXED1pSSxYL7rQPG0b4mp/3ulbQ0457hE=";
    };
    skimsTreeSitterTsx = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-typescript";
      rev = "0ab9d99867435a7667c5548a6617a6bf73dbd830";
      sha256 = "Nx+K7Ic/ePKAXPIMlrRn6zELYE59f/FnnZ/LM5ELaU8=";
    };
    skimsTreeSitterYaml = fetchGithub {
      owner = "jgomezb11";
      repo = "tree-sitter-yaml";
      rev = "22d5085be4f1e17d4b33e0e2c1e679bef85f61ed";
      sha256 = "ZgHatgSiv87nclDkUthXtf5RS3k6rYaOCnaR1rzl6wA=";
    };
  };
}
