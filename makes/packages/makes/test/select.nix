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
            # Select derivations belonging to the product
            (nixpkgs.lib.strings.hasPrefix product name)
            # Prevent infinite recursion
            && !(nixpkgs.lib.strings.hasPrefix "makes.test" name)
          ))
          (packagesFlattened));
  };
  builder = "echo $envBuilt > $out";
  name = "makes-test-${product}";
}
