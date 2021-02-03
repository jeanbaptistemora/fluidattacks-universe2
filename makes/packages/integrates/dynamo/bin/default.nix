{ integratesPkgs
, integratesPkgsTerraform
, outputs
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path integratesPkgs;
in
makeEntrypoint {
  arguments = {
    envDynamoZip = integratesPkgs.fetchurl {
      url = "https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_2020-05-19.zip";
      sha256 = "0lqxrbiqnvac8rq8x41pm76mb5bh4rxhfzj5yxji6n9q0m1wxbqq";
    };
    envJava = "${integratesPkgs.jdk11}/bin/java";
    envKillPidListeningOnPort = import (path "/makes/utils/kill-pid-listening-on-port") path integratesPkgs;
    envTerraform = "${integratesPkgsTerraform.terraform_0_13}/bin/terraform";
    envTerraformModule = path "/makes/packages/integrates/dynamo/bin";
    envUnzip = "${integratesPkgs.unzip}/bin/unzip";
    envWait = outputs.apps."makes/wait".program;
  };
  name = "integrates-dynamo";
  template = path "/makes/packages/integrates/dynamo/bin/entrypoint.sh";
}
