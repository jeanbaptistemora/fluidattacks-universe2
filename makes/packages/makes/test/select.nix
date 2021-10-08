product:

{ makeDerivation
, nixpkgs
, packagesFlattened
, ...
}:
makeDerivation {
  arguments = {
    envBuilt =
      builtins.attrValues
        (nixpkgs.lib.attrsets.filterAttrs
          (name: _: (
            # Exclude broken jobs
            name != "asserts.doc.build"
            && name != "observes.test.postgres-client"
            && name != "observes.test.streamer-zoho-crm"
            # Select derivations belonging to the product
            && (nixpkgs.lib.strings.hasPrefix product name)
            # Prevent infinite recursion
            && !(nixpkgs.lib.strings.hasPrefix "makes.test" name)
          ))
          packagesFlattened);
  };
  builder = "echo $envBuilt > $out";
  name = "makes-test-${product}";
}
