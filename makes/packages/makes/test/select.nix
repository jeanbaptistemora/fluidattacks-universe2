product:

{ makeDerivation
, makesPkgs
, packagesFlattened
, ...
}:
makeDerivation makesPkgs {
  arguments = {
    envBuilt =
      builtins.attrValues
        (makesPkgs.lib.attrsets.filterAttrs
          (name: _: (
            # Select derivations belonging to the product
            (makesPkgs.lib.strings.hasPrefix product name)
            # Prevent infinite recursion
            && !(makesPkgs.lib.strings.hasPrefix "makes.test" name)
          ))
          (packagesFlattened));
  };
  builder = "echo $envBuilt > $out";
  name = "makes-test-${product}";
}
