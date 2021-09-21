{ fetchzip
, packages
, makeEntrypoint
, path
, skimsBenchmarkOwaspRepo
, ...
}:
makeEntrypoint {
  arguments = {
    envAndroguardRepo = fetchzip {
      url = "https://github.com/androguard/androguard/archive/8d091cbb309c0c50bf239f805cc1e0931b8dcddc.zip";
      sha256 = "IdN5CNBgVqFWSZk/nwX11KE5llLxQ2Hyrb69P3uXRuA=";
    };
    envBenchmarkRepo = skimsBenchmarkOwaspRepo;
    envNISTTestSuites = fetchzip {
      url = "https://github.com/fluidattacks/NIST-SARD-Test-Suites/archive/7189c65ab6e398180e3f2aa2de683466b4412821.tar.gz";
      sha256 = "CDLX3Xa7nCmzdJdAjlSzdlFIaUx3cg7GPiqc5c8Dj6Q=";
    };
    envVulnerableAppRepo = fetchzip {
      url = "https://github.com/SasanLabs/VulnerableApp/archive/f5334e84faadbfb4beec42849a2e8acc5e37a276.tar.gz";
      sha256 = "gVY9VPo0+2xHdbME61MH/JaMP8pyqWh5k7im3O8hNAc=";
    };
    envVulnerableJsAppRepo = fetchzip {
      url = "https://github.com/fluidattacks/vulnerable_js_app/archive/3e93dfc1b448225e941aa8affb91c0a9e337104b.tar.gz";
      sha256 = "0gnv9m9gvd16lsxnbkp17iqv2zdkfr2gmaq031ra5f7pc3d5graq";
    };
  };
  name = "skims-test";
  searchPaths = {
    envPaths = [
      packages.makes.wait
      packages.makes.kill-port
      packages.makes.kill-tree
      packages.skims.test.mocks.http
      packages.skims.test.mocks.ssl.safe
      packages.skims.test.mocks.ssl.unsafe
    ];
    envSources = [
      packages.skims.config-development
      packages.skims.config-runtime
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/env"
    ];
  };
  template = path "/makes/applications/skims/test/entrypoint.sh";
}
