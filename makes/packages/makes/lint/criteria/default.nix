{ makeDerivation
, nixpkgs
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envSrcVulnerabilitiesSchema = path "/makes/applications/makes/criteria/src/vulnerabilities/schema.json";
    envSrcVulnerabilitiesSchemaData = path "/makes/applications/makes/criteria/src/vulnerabilities/data.yaml";
  };
  builder = path "/makes/packages/makes/lint/criteria/builder.sh";
  name = "makes-lint-criteria";
  searchPaths = {
    envPaths = [
      nixpkgs.git
    ];
    envNodeBinaries = [
      packages.makes.ajv
    ];
    envNodeLibraries = [
      packages.makes.ajv
    ];
  };
}
