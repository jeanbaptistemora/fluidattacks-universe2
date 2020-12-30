attrs @ {
  outputs,
  pkgsSkims,
  ...
}:

let
  config = import ../../../makes/skims/config attrs.copy;
  makeEntrypoint = import ../../../makes/utils/make-entrypoint pkgsSkims;
in
  makeEntrypoint {
    arguments = {
      envUtilsBashLibAws = import ../../../makes/utils/bash-lib/aws pkgsSkims;
      envUtilsBashLibSops = import ../../../makes/utils/bash-lib/sops pkgsSkims;
      envBenchmarkRepo = pkgsSkims.fetchzip {
        url = "https://github.com/OWASP/Benchmark/archive/9a0c25a5f8443245c676965d20d22d5f93da3f99.zip";
        sha256 = "QwtG90KPleNRU9DrNYTdBlcjR6vcmLTiC6G57x1Ayw4=";
      };
      envPython = "${pkgsSkims.python38}/bin/python";
      envSkims = outputs.apps.skims.program;
      envSrcSkimsSkims = ../../../skims/skims;
      envSrcSkimsTest = ../../../skims/test;
      envTapJson = outputs.apps.observes-tap-json.program;
      envTargetRedshift = outputs.apps.observes-target-redshift.program;
    };
    location = "/bin/skims-benchmark";
    name = "skims-benchmark";
    template = ../../../makes/skims/benchmark/entrypoint.sh;
  }
