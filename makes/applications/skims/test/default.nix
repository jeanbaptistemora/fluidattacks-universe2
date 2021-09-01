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
      url = "https://github.com/fluidattacks/vulnerable_js_app/archive/fd82c915e250fe930c6134cf2e8e57a15672a514.tar.gz";
      sha256 = "0f3ynrriiqw5rm9pf3a7rln244ja7hxzgb6lrvxr1jz2x0rz988z";
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
