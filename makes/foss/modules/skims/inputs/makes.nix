{ fetchGithub
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
    envVulnerableApp = fetchGithub {
      owner = "SasanLabs";
      repo = "VulnerableApp";
      rev = "f5334e84faadbfb4beec42849a2e8acc5e37a276";
      sha256 = "gVY9VPo0+2xHdbME61MH/JaMP8pyqWh5k7im3O8hNAc=";
    };
    envVulnerableJsApp = fetchGithub {
      owner = "fluidattacks";
      repo = "vulnerable_js_app";
      rev = "83c469acfe5b3ac86e9479abaa490185806d9cdc";
      sha256 = "01zc3hwnjghyirhcbc3l3nnqv3rmgiw1q41ccc57rai80k3wjhgd";
    };
  };
}
