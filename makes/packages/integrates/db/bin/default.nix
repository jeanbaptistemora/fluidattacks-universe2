{ integratesPkgs
, outputs
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path integratesPkgs;
in
makeEntrypoint {
  arguments = {
    envAws = "${integratesPkgs.awscli}/bin/aws";
    envDynamoData = path "/makes/packages/integrates/db/data";
    envDynamoZip = integratesPkgs.fetchurl {
      url = "https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_2020-05-19.zip";
      sha256 = "0lqxrbiqnvac8rq8x41pm76mb5bh4rxhfzj5yxji6n9q0m1wxbqq";
    };
    envJava = "${integratesPkgs.openjdk_headless}/bin/java";
    envKillPidListeningOnPort = import (path "/makes/utils/kill-pid-listening-on-port") path integratesPkgs;
    envSed = "${integratesPkgs.gnused}/bin/sed";
    envTerraform = "${integratesPkgs.terraform}/bin/terraform";
    envTerraformModule = path "/makes/packages/integrates/db/bin";
    envUnzip = "${integratesPkgs.unzip}/bin/unzip";
    envWait = outputs.apps."makes/wait".program;
  };
  name = "integrates-db";
  template = path "/makes/packages/integrates/db/bin/entrypoint.sh";
}
