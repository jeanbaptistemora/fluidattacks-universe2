{ inputs
, makeNodeJsEnvironment
, makeScript
, outputs
, ...
}:
let
  inspectorEnvironment = makeNodeJsEnvironment {
    name = "graphql-inspector-env";
    nodeJsVersion = "16";
    packageJson = ./npm/package.json;
    packageLockJson = ./npm/package-lock.json;
  };
in
makeScript {
  name = "integrates-web-check-schema-changes";
  searchPaths = {
    bin = [ inputs.nixpkgs.kubectl ];
    source = [
      inspectorEnvironment
      outputs."/utils/aws"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
