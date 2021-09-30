{ fetchGithub
, fromJsonFile
, projectPath
, ...
}:
{
  inputs = {
    skimsAndroguard = fetchGithub {
      owner = "androguard";
      repo = "androguard";
      rev = "8d091cbb309c0c50bf239f805cc1e0931b8dcddc";
      sha256 = "IdN5CNBgVqFWSZk/nwX11KE5llLxQ2Hyrb69P3uXRuA=";
    };
    skimsBenchmarkOwasp = fetchGithub {
      owner = "owasp";
      repo = "benchmark";
      rev = "1cfe52ea6dc49bebae12e6ceb20356196f0e9ac8";
      sha256 = "pcNMJJJ2cRxh4Kgq0ElOIyBJemJu4qggxY3Debjbcms=";
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
    skimsTestPythonCategories = fromJsonFile
      (projectPath "/skims/test/test_groups.json");
  };
}
