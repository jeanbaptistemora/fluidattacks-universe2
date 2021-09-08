{ fromYaml
, inputs
, makeDerivation
, makeScript
, projectPath
, ...
}:
let
  lib = inputs.nixpkgs.lib;

  # Load data
  compliance = fromYaml (
    builtins.readFile (
      projectPath "/makes/makes/criteria/src/compliance/data.yaml"
    )
  );
  requirements = fromYaml (
    builtins.readFile (
      projectPath "/makes/makes/criteria/src/requirements/data.yaml"
    )
  );
  vulnerabilities = fromYaml (
    builtins.readFile (
      projectPath "/makes/makes/criteria/src/vulnerabilities/data.yaml"
    )
  );

  # List of all definitions in <standard>.<definition> format
  definitions =
    let
      standardDefinitions = id: builtins.map
        (def: "${id}.${def}")
        (builtins.attrNames compliance.${id}.definitions);
    in
    lib.lists.flatten (
      builtins.attrValues (
        builtins.mapAttrs (id: _: standardDefinitions id) compliance
      )
    );

  # List of referenced items
  referenced = { field, data }: lib.lists.unique (
    lib.lists.flatten (
      builtins.map (x: x.${field}) (builtins.attrValues data)
    )
  );

  # List of unreferenced items
  unreferenced = { referencedItems, items }:
    lib.lists.subtractLists referencedItems items;

  # JSON output
  output = makeDerivation {
    env = {
      envUnreferenced = builtins.toJSON {
        compliance = unreferenced {
          referencedItems = referenced {
            field = "references";
            data = requirements;
          };
          items = definitions;
        };
        requirements = unreferenced {
          referencedItems = referenced {
            field = "requirements";
            data = vulnerabilities;
          };
          items = builtins.attrNames requirements;
        };
      };
    };
    searchPaths.bin = [ inputs.nixpkgs.jq ];
    builder = ''
      echo "$envUnreferenced" | jq . > "$out"
    '';
    name = "criteria-unreferenced";
  };
in
makeScript {
  replace = {
    __argOutput__ = output;
  };
  entrypoint = ''
    cat __argOutput__
  '';
  name = "criteria-unreferenced";
}
