{ fetchzip
, makeEntrypoint
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envAndroguardRepository = fetchzip {
      url = "https://github.com/androguard/androguard/archive/8d091cbb309c0c50bf239f805cc1e0931b8dcddc.zip";
      sha256 = "IdN5CNBgVqFWSZk/nwX11KE5llLxQ2Hyrb69P3uXRuA=";
    };
  };
  name = "skims-test-mocks-mobile";
  template = path "/makes/applications/skims/test/mocks/mobile/entrypoint.sh";
}
