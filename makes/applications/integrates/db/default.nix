{ integratesPkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envDb = path "/makes/applications/integrates/db";
    envDynamoZip = integratesPkgs.fetchurl {
      url = "https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_2020-05-19.zip";
      sha256 = "0lqxrbiqnvac8rq8x41pm76mb5bh4rxhfzj5yxji6n9q0m1wxbqq";
    };
  };
  name = "integrates-db";
  searchPaths = {
    envPaths = [
      integratesPkgs.awscli
      integratesPkgs.gnused
      integratesPkgs.openjdk_headless
      integratesPkgs.terraform
      integratesPkgs.unzip
      packages.makes.done
      packages.makes.kill-port
      packages.makes.wait
    ];
  };
  template = path "/makes/applications/integrates/db/entrypoint.sh";
}
