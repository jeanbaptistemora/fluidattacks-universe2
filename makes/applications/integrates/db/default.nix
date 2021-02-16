{ integratesPkgs
, makeEntrypoint
, packages
, path
, ...
} @ _:
makeEntrypoint integratesPkgs {
  arguments = {
    envAws = "${integratesPkgs.awscli}/bin/aws";
    envDynamoData = path "/makes/applications/integrates/db/data";
    envDynamoZip = integratesPkgs.fetchurl {
      url = "https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_2020-05-19.zip";
      sha256 = "0lqxrbiqnvac8rq8x41pm76mb5bh4rxhfzj5yxji6n9q0m1wxbqq";
    };
    envJava = "${integratesPkgs.openjdk_headless}/bin/java";
    envSed = "${integratesPkgs.gnused}/bin/sed";
    envTerraform = "${integratesPkgs.terraform}/bin/terraform";
    envTerraformModule = path "/makes/applications/integrates/db";
    envUnzip = "${integratesPkgs.unzip}/bin/unzip";
  };
  name = "integrates-db";
  searchPaths = {
    envPaths = [
      packages.makes.done
      packages.makes.kill-port
      packages.makes.wait
    ];
  };
  template = path "/makes/applications/integrates/db/entrypoint.sh";
}
